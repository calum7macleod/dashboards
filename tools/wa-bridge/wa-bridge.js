/**
 * WA->CRM BRIDGE v1.5 (read-only, CAPTURE-ALL incl groups, SELF-HEALING) - Calum MacLeod
 * 1:1 chats  -> crm-inbox data/wa-inbox.json  (rolling 4000)
 * Group chats -> crm-inbox data/wa-groups.json (rolling 3000, separate so noise never evicts clients)
 * No keyword filter - triage/matching happens downstream (Max), verified with Calum.
 * BLOCKLIST (numbers AND group ids, one per line, last-9 matched):
 *   - server-side ./blocklist.txt (never leaves the box)
 *   - PLUS blocklist.txt at the root of the PRIVATE inbox repo (Max-manageable remotely)
 *   Both merged, re-read every 10 min. Blocked = silently dropped, nothing logged.
 * HARD RULES: never sends messages. Voice notes/media logged as [ptt]/[image] markers (no download yet).
 */
const { Client, LocalAuth } = require('whatsapp-web.js');
const qrcode = require('qrcode-terminal');
const https = require('https');
const fs = require('fs');

const GH_TOKEN = process.env.GH_TOKEN; // set in environment - never hardcode
const REPO = 'calum7macleod/dashboards';           // read-side: buyers/stock for match tagging
const INBOX_REPO = process.env.INBOX_REPO || REPO; // write-side: private repo
const INBOX_PATH = 'data/wa-inbox.json';
const GROUPS_PATH = 'data/wa-groups.json';
const BLOCKLIST_FILE = './blocklist.txt';
const PUSH_EVERY_MS = 15 * 60 * 1000;      // batch every 15 min
const FAST_FLUSH_MS = 45 * 1000;           // ...or 45s after the last message in a burst

let KNOWN = new Set();      // phone numbers from buyers.json + stock.json (tagging only)
let BLOCKED = new Set();    // merged blocklist, last-9 normalised
let queue1 = [];            // 1:1 messages
let queueG = [];            // group messages
let dirty = 0;

function ghGet(repo, path) {
  return new Promise((res, rej) => {
    const rq = https.get({ host: 'api.github.com', path: `/repos/${repo}/contents/${path}?ref=main`,
      headers: { Authorization: `Bearer ${GH_TOKEN}`, 'User-Agent': 'wa-bridge', Accept: 'application/vnd.github+json' }, timeout: 30000 },
      r => { let b = ''; r.on('data', d => b += d); r.on('end', () => res(JSON.parse(b))); });
    rq.on('timeout', () => { rq.destroy(); rej(new Error('ghGet timeout')); });
    rq.on('error', rej);
  });
}
function ghPut(repo, path, contentObj, sha, msg) {
  const body = JSON.stringify({ message: msg, content: Buffer.from(JSON.stringify(contentObj, null, 1)).toString('base64'), sha, branch: 'main' });
  return new Promise((res, rej) => {
    const req = https.request({ host: 'api.github.com', path: `/repos/${repo}/contents/${path}`, method: 'PUT',
      headers: { Authorization: `Bearer ${GH_TOKEN}`, 'User-Agent': 'wa-bridge', 'Content-Type': 'application/json', 'Content-Length': Buffer.byteLength(body) } },
      r => { let b = ''; r.on('data', d => b += d); r.on('end', () => r.statusCode < 300 ? res(JSON.parse(b)) : rej(new Error(`${r.statusCode}: ${b.slice(0,200)}`))); });
    req.setTimeout(30000, () => { req.destroy(); rej(new Error('ghPut timeout')); });
    req.on('error', rej); req.write(body); req.end();
  });
}

const last9 = s => String(s).replace(/\D/g, '').slice(-9);

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

async function loadBlocklist() {
  const fresh = new Set();
  try {
    for (const l of fs.readFileSync(BLOCKLIST_FILE, 'utf8').split(/\r?\n/)) {
      const d = last9(l); if (d.length === 9) fresh.add(d);
    }
  } catch (_) {}
  try {
    const meta = await ghGet(INBOX_REPO, 'blocklist.txt');
    if (meta && meta.content) {
      for (const l of Buffer.from(meta.content, 'base64').toString().split(/\r?\n/)) {
        const d = last9(l); if (d.length === 9) fresh.add(d);
      }
    }
  } catch (_) {}
  BLOCKED = fresh;
  console.log(BLOCKED.size ? `[bridge] blocklist loaded: ${BLOCKED.size}` : '[bridge] blocklist EMPTY - all non-status chats are being logged');
}

const client = new Client({ authStrategy: new LocalAuth({ dataPath: './session' }), puppeteer: { headless: true, args: ['--no-sandbox'] } });
client.on('qr', qr => { console.log('\nSCAN THIS WITH WHATSAPP (Linked devices > Link a device):\n'); qrcode.generate(qr, { small: true }); });
let READY = false, BOOT = Date.now();
client.on('ready', () => { READY = true; console.log('[bridge] connected, listening (read-only, capture-all v1.5 self-healing).'); });
client.on('disconnected', r => { console.error('[bridge] WA disconnected:', r, '- restarting in 10s'); setTimeout(() => process.exit(1), 10000); });
// WATCHDOG: WA Web reloads silently kill the hooks while the process looks alive (the 4-Aug zombie).
// Every 5 min: probe client state; not CONNECTED or probe throws -> exit, pm2 revives us on the saved session.
setInterval(() => {
  if (!READY) { if (Date.now() - BOOT > 10 * 60 * 1000) { console.error('[bridge] never became ready in 10min - restarting'); process.exit(1); } return; }
  client.getState().then(st => {
    if (st !== 'CONNECTED') { console.error(`[bridge] watchdog: state=${st} - restarting in 10s`); setTimeout(() => process.exit(1), 10000); }
  }).catch(e => { console.error('[bridge] watchdog probe failed:', e.message, '- restarting in 10s'); setTimeout(() => process.exit(1), 10000); });
}, 5 * 60 * 1000);

async function handle(msg, fromMe) {
  try {
    const from = String(msg.from || ''), to = String(msg.to || '');
    if (from === 'status@broadcast' || to === 'status@broadcast') return;     // stories skipped
    const isGroup = from.endsWith('@g.us') || to.endsWith('@g.us');
    const body = msg.body || `[${msg.type}]`;
    const groupId = isGroup ? (fromMe ? to : from).replace(/@.*/, '') : '';
    const personRaw = isGroup
      ? (fromMe ? 'me' : String(msg.author || '').replace(/@.*/, ''))
      : (fromMe ? to : from).replace(/@.*/, '');
    const num9 = last9(personRaw);
    if (BLOCKED.has(num9) || (groupId && BLOCKED.has(last9(groupId)))) return; // hard blocklist - silent
    const known = KNOWN.has(num9);
    console.log(`[bridge] rx ${fromMe?'->':'<-'}${isGroup?'g':' '} ${num9 || groupId.slice(-9)} len:${(body||'').length} known:${known}`);
    dirty = Date.now();                                                       // fast-flush timer
    let name = '';
    try { name = (msg._data && (msg._data.notifyName || msg._data.pushName)) || ''; } catch (_) {}
    const rec = {
      at: new Date((msg.timestamp || Date.now() / 1000) * 1000).toISOString(),
      dir: fromMe ? 'out' : 'in',
      contact: name || personRaw,
      number: personRaw,
      known,
      text: String(body).slice(0, 1200)
    };
    if (isGroup) { rec.group = groupId; queueG.push(rec); } else { queue1.push(rec); }
  } catch (e) { console.error('[bridge] handle err', e && e.message); }
}
client.on('message', m => handle(m, false));
client.on('message_create', m => { if (m.fromMe) handle(m, true); });

async function flushOne(path, batch, cap) {
  if (!batch.length) return;
  try {
    let sha, arr = [];
    try { const meta = await ghGet(INBOX_REPO, path); sha = meta.sha; arr = JSON.parse(Buffer.from(meta.content, 'base64').toString()); } catch (_) {}
    if (!Array.isArray(arr)) arr = [];
    arr.push(...batch);
    if (arr.length > cap) arr = arr.slice(-cap);
    await ghPut(INBOX_REPO, path, arr, sha, `wa-bridge: +${batch.length}`);
    console.log(`[bridge] pushed ${batch.length} -> ${path} (${new Date().toISOString()})`);
    batch.length = 0;
  } catch (e) { console.error('[bridge] push failed, requeueing', e.message); }
}
async function flush() {
  if (queue1.length) { const b = queue1.splice(0); await flushOne(INBOX_PATH, b, 4000); if (b.length) queue1.unshift(...b); }
  if (queueG.length) { const b = queueG.splice(0); await flushOne(GROUPS_PATH, b, 3000); if (b.length) queueG.unshift(...b); }
}
setInterval(flush, PUSH_EVERY_MS);
setInterval(() => { if (dirty && Date.now() - dirty > FAST_FLUSH_MS) { dirty = 0; flush(); } }, 15 * 1000);

loadBlocklist();
loadKnownNumbers().then(() => client.initialize().catch(e => { console.error('[bridge] init failed:', e.message, '- restarting in 15s'); setTimeout(() => process.exit(1), 15000); }));
setInterval(loadKnownNumbers, 6 * 60 * 60 * 1000);   // refresh known numbers 6-hourly
setInterval(loadBlocklist, 10 * 60 * 1000);          // re-read blocklists (local + repo) every 10 min
