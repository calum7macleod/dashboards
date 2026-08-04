/**
 * WA->CRM BRIDGE v1.3 (read-only, CAPTURE-ALL) - Calum MacLeod
 * Logs EVERY 1:1 conversation, inbound + outbound. Groups and status skipped.
 * No keyword filter - triage/matching happens downstream (Max), verified with Calum.
 * HARD BLOCKLIST: ./blocklist.txt on the server (one number per line). Blocked
 * numbers are never logged, never pushed, and never leave the box. File is
 * re-read every 10 min so additions take effect without a restart.
 * HARD RULES: never sends messages. Blocklist stays server-side only.
 */
const { Client, LocalAuth } = require('whatsapp-web.js');
const qrcode = require('qrcode-terminal');
const https = require('https');
const fs = require('fs');

const GH_TOKEN = process.env.GH_TOKEN; // set in environment - never hardcode
const REPO = 'calum7macleod/dashboards';           // read-side: buyers/stock for match tagging
const INBOX_REPO = process.env.INBOX_REPO || REPO; // write-side: point at a PRIVATE repo when ready
const INBOX_PATH = 'data/wa-inbox.json';
const BLOCKLIST_FILE = './blocklist.txt';
const PUSH_EVERY_MS = 15 * 60 * 1000;      // batch every 15 min
const FAST_FLUSH_MS = 45 * 1000;           // ...or 45s after the last message in a burst

let KNOWN = new Set();      // phone numbers from buyers.json + stock.json (tagging only)
let BLOCKED = new Set();    // server-side blocklist, last-9 normalised
let queue = [];
let dirty = 0;

function ghGet(repo, path) {
  return new Promise((res, rej) => {
    https.get({ host: 'api.github.com', path: `/repos/${repo}/contents/${path}?ref=main`,
      headers: { Authorization: `Bearer ${GH_TOKEN}`, 'User-Agent': 'wa-bridge', Accept: 'application/vnd.github+json' } },
      r => { let b = ''; r.on('data', d => b += d); r.on('end', () => res(JSON.parse(b))); }).on('error', rej);
  });
}
function ghPut(repo, path, contentObj, sha, msg) {
  const body = JSON.stringify({ message: msg, content: Buffer.from(JSON.stringify(contentObj, null, 1)).toString('base64'), sha, branch: 'main' });
  return new Promise((res, rej) => {
    const req = https.request({ host: 'api.github.com', path: `/repos/${repo}/contents/${path}`, method: 'PUT',
      headers: { Authorization: `Bearer ${GH_TOKEN}`, 'User-Agent': 'wa-bridge', 'Content-Type': 'application/json', 'Content-Length': Buffer.byteLength(body) } },
      r => { let b = ''; r.on('data', d => b += d); r.on('end', () => r.statusCode < 300 ? res(JSON.parse(b)) : rej(new Error(`${r.statusCode}: ${b.slice(0,200)}`))); });
    req.on('error', rej); req.write(body); req.end();
  });
}

async function loadKnownNumbers() {
  try {
    const fresh = new Set();
    for (const f of ['data/buyers.json', 'data/stock.json']) {
      const meta = await ghGet(REPO, f);
      const arr = JSON.parse(Buffer.from(meta.content, 'base64').toString());
      const list = Array.isArray(arr) ? arr : (arr.buyers || arr.stock || []);
      for (const rec of list) {
        for (const v of Object.values(rec)) {
          if (typeof v === 'string' && /\d{7,}/.test(v.replace(/[\s-]/g,''))) {
            const digits = v.replace(/\D/g, '');
            if (digits.length >= 9 && digits.length <= 15) fresh.add(digits.slice(-9));
          }
        }
      }
    }
    if (fresh.size) KNOWN = fresh;
    console.log(`[bridge] known numbers loaded: ${KNOWN.size}`);
  } catch (e) { console.error('[bridge] known-load failed', e.message); }
}

function loadBlocklist() {
  try {
    const lines = fs.readFileSync(BLOCKLIST_FILE, 'utf8').split(/\r?\n/);
    BLOCKED = new Set(lines.map(l => l.replace(/\D/g, '').slice(-9)).filter(d => d.length === 9));
    console.log(`[bridge] blocklist loaded: ${BLOCKED.size}`);
  } catch (_) {
    if (BLOCKED.size === 0) console.log('[bridge] no blocklist file yet - ALL non-group chats are being logged');
  }
}

const client = new Client({ authStrategy: new LocalAuth({ dataPath: './session' }), puppeteer: { headless: true, args: ['--no-sandbox'] } });
client.on('qr', qr => { console.log('\nSCAN THIS WITH WHATSAPP (Linked devices > Link a device):\n'); qrcode.generate(qr, { small: true }); });
client.on('ready', () => console.log('[bridge] connected, listening (read-only, capture-all).'));

async function handle(msg, fromMe) {
  try {
    const from = String(msg.from || ''), to = String(msg.to || '');
    if (from.endsWith('@g.us') || to.endsWith('@g.us')) return;               // groups skipped v1
    if (from === 'status@broadcast' || to === 'status@broadcast') return;     // stories skipped
    const body = msg.body || `[${msg.type}]`;
    const rawNum = (fromMe ? to : from).replace(/@.*/, '');
    const num9 = rawNum.replace(/\D/g, '').slice(-9);
    if (BLOCKED.has(num9)) return;                                            // hard blocklist - silent, nothing logged
    const known = KNOWN.has(num9);
    console.log(`[bridge] rx ${fromMe?'->':'<-'} ${num9} len:${(body||'').length} known:${known}`);
    dirty = Date.now();                                                       // fast-flush timer
    let name = '';
    try { name = (msg._data && (msg._data.notifyName || msg._data.pushName)) || ''; } catch (_) {}
    queue.push({
      at: new Date((msg.timestamp || Date.now() / 1000) * 1000).toISOString(),
      dir: fromMe ? 'out' : 'in',
      contact: name || rawNum,
      number: rawNum,
      known,
      text: String(body).slice(0, 1200)
    });
  } catch (e) { console.error('[bridge] handle err', e && e.message); }
}
client.on('message', m => handle(m, false));
client.on('message_create', m => { if (m.fromMe) handle(m, true); });

async function flush() {
  if (!queue.length) return;
  const batch = queue.splice(0, queue.length);
  try {
    let sha, inbox = [];
    try { const meta = await ghGet(INBOX_REPO, INBOX_PATH); sha = meta.sha; inbox = JSON.parse(Buffer.from(meta.content, 'base64').toString()); } catch (_) {}
    if (!Array.isArray(inbox)) inbox = [];
    inbox.push(...batch);
    if (inbox.length > 4000) inbox = inbox.slice(-4000);                      // rolling window
    await ghPut(INBOX_REPO, INBOX_PATH, inbox, sha, `wa-bridge: +${batch.length} messages`);
    console.log(`[bridge] pushed ${batch.length} (${new Date().toISOString()})`);
  } catch (e) { console.error('[bridge] push failed, requeueing', e.message); queue.unshift(...batch); }
}
setInterval(flush, PUSH_EVERY_MS);
setInterval(() => { if (dirty && Date.now() - dirty > FAST_FLUSH_MS) { dirty = 0; flush(); } }, 15 * 1000);

loadBlocklist();
loadKnownNumbers().then(() => client.initialize());
setInterval(loadKnownNumbers, 6 * 60 * 60 * 1000);   // refresh known numbers 6-hourly
setInterval(loadBlocklist, 10 * 60 * 1000);          // re-read blocklist every 10 min
