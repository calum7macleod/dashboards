/**
 * WA->CRM BRIDGE (read-only) - Calum MacLeod
 * Linked-device listener: reads business chats, pushes to repo for CRM intake.
 * HARD RULES: never sends messages. Personal chats never logged.
 */
const { Client, LocalAuth } = require('whatsapp-web.js');
const qrcode = require('qrcode-terminal');
const https = require('https');

const GH_TOKEN = process.env.GH_TOKEN; // set in environment - never hardcode
const REPO = 'calum7macleod/dashboards';
const INBOX_PATH = 'data/wa-inbox.json';
const PUSH_EVERY_MS = 15 * 60 * 1000;      // batch every 15 min
const PROPERTY_WORDS = /\b(unit|villa|townhouse|apartment|bed|beds|price|aed|million|offer|viewing|view|lagoons|damac|cluster|handover|mortgage|payment plan|launch|off ?plan|dld|noc|deposit|listing|sqft|sq ft|tara|hudayriyat|reem|malta|costa|santorini|portofino|nice|marbella|monte carlo)\b/i;

let KNOWN = new Set();      // phone numbers from buyers.json + stock.json
let queue = [];

function ghGet(path) {
  return new Promise((res, rej) => {
    https.get({ host: 'api.github.com', path: `/repos/${REPO}/contents/${path}?ref=main`,
      headers: { Authorization: `Bearer ${GH_TOKEN}`, 'User-Agent': 'wa-bridge', Accept: 'application/vnd.github+json' } },
      r => { let b = ''; r.on('data', d => b += d); r.on('end', () => res(JSON.parse(b))); }).on('error', rej);
  });
}
function ghPut(path, contentObj, sha, msg) {
  const body = JSON.stringify({ message: msg, content: Buffer.from(JSON.stringify(contentObj, null, 1)).toString('base64'), sha, branch: 'main' });
  return new Promise((res, rej) => {
    const req = https.request({ host: 'api.github.com', path: `/repos/${REPO}/contents/${path}`, method: 'PUT',
      headers: { Authorization: `Bearer ${GH_TOKEN}`, 'User-Agent': 'wa-bridge', 'Content-Type': 'application/json', 'Content-Length': Buffer.byteLength(body) } },
      r => { let b = ''; r.on('data', d => b += d); r.on('end', () => r.statusCode < 300 ? res(JSON.parse(b)) : rej(new Error(`${r.statusCode}: ${b.slice(0,200)}`))); });
    req.on('error', rej); req.write(body); req.end();
  });
}

async function loadKnownNumbers() {
  try {
    for (const f of ['data/buyers.json', 'data/stock.json']) {
      const meta = await ghGet(f);
      const arr = JSON.parse(Buffer.from(meta.content, 'base64').toString());
      const text = JSON.stringify(arr);
      (text.match(/\+?\d{9,15}/g) || []).forEach(n => KNOWN.add(n.replace(/\D/g, '').slice(-9)));
    }
    console.log(`[bridge] known numbers loaded: ${KNOWN.size}`);
  } catch (e) { console.error('[bridge] known-load failed', e.message); }
}

function isBusiness(msg, chat, body) {
  if (chat.isGroup) return false;                                   // groups skipped v1
  const num = (msg.from || '').replace(/\D/g, '').slice(-9);
  if (KNOWN.has(num)) return true;                                  // known CRM contact
  if (PROPERTY_WORDS.test(body || '')) return true;                 // property signals
  return false;                                                     // else personal -> never logged
}

const client = new Client({ authStrategy: new LocalAuth({ dataPath: './session' }), puppeteer: { headless: true, args: ['--no-sandbox'] } });
client.on('qr', qr => { console.log('\nSCAN THIS WITH WHATSAPP (Linked devices > Link a device):\n'); qrcode.generate(qr, { small: true }); });
client.on('ready', () => console.log('[bridge] connected, listening (read-only).'));

async function handle(msg, fromMe) {
  try {
    const chat = await msg.getChat();
    const body = msg.body || `[${msg.type}]`;
    if (!isBusiness(msg, chat, body) && !(fromMe && PROPERTY_WORDS.test(body))) {
      // for outbound: also keep call-receipt style messages to known numbers
      const num = (msg.to || '').replace(/\D/g, '').slice(-9);
      if (!(fromMe && KNOWN.has(num))) return;
    }
    queue.push({
      at: new Date(msg.timestamp * 1000).toISOString(),
      dir: fromMe ? 'out' : 'in',
      contact: chat.name || chat.id.user,
      number: (fromMe ? msg.to : msg.from || '').replace(/@.*/, ''),
      text: body.slice(0, 1200)
    });
  } catch (e) { console.error('[bridge] handle err', e.message); }
}
client.on('message', m => handle(m, false));
client.on('message_create', m => { if (m.fromMe) handle(m, true); });

setInterval(async () => {
  if (!queue.length) return;
  const batch = queue.splice(0, queue.length);
  try {
    let sha, inbox = [];
    try { const meta = await ghGet(INBOX_PATH); sha = meta.sha; inbox = JSON.parse(Buffer.from(meta.content, 'base64').toString()); } catch {}
    inbox.push(...batch);
    if (inbox.length > 4000) inbox = inbox.slice(-4000);            // rolling window
    await ghPut(INBOX_PATH, inbox, sha, `wa-bridge: +${batch.length} messages`);
    console.log(`[bridge] pushed ${batch.length} (${new Date().toISOString()})`);
  } catch (e) { console.error('[bridge] push failed, requeueing', e.message); queue.unshift(...batch); }
}, PUSH_EVERY_MS);

loadKnownNumbers().then(() => client.initialize());
setInterval(loadKnownNumbers, 6 * 60 * 60 * 1000);                  // refresh known numbers 6-hourly
