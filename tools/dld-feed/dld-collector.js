/**
 * DLD FEED COLLECTOR v1.0 - runs on droplet under pm2 (--cron-restart daily, --no-autorestart)
 * Pulls Dubai Land Department open-data transactions (gateway JSON API, verified reachable),
 * filters to watched projects (config in repo), aggregates citywide daily summary,
 * pushes compact JSON to dashboards repo data/dld/. Read-only against DLD; polite paging.
 * Config: tools/dld-feed/config.json in repo (Max edits watchlist; no server touch needed).
 */
const https = require('https');

const GH_TOKEN = process.env.GH_TOKEN;
const REPO = 'calum7macleod/dashboards';
const GATEWAY = 'gateway.dubailand.gov.ae';
const UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/126';

function ghGet(path) {
  return new Promise((res, rej) => {
    https.get({ host: 'api.github.com', path: `/repos/${REPO}/contents/${path}?ref=main`,
      headers: { Authorization: `Bearer ${GH_TOKEN}`, 'User-Agent': 'dld-feed', Accept: 'application/vnd.github+json' } },
      r => { let b = ''; r.on('data', d => b += d); r.on('end', () => res(JSON.parse(b))); }).on('error', rej);
  });
}
function ghPut(path, contentObj, sha, msg) {
  const body = JSON.stringify({ message: msg, content: Buffer.from(JSON.stringify(contentObj)).toString('base64'), sha, branch: 'main' });
  return new Promise((res, rej) => {
    const req = https.request({ host: 'api.github.com', path: `/repos/${REPO}/contents/${path}`, method: 'PUT',
      headers: { Authorization: `Bearer ${GH_TOKEN}`, 'User-Agent': 'dld-feed', 'Content-Type': 'application/json', 'Content-Length': Buffer.byteLength(body) } },
      r => { let b = ''; r.on('data', d => b += d); r.on('end', () => r.statusCode < 300 ? res(JSON.parse(b)) : rej(new Error(`${r.statusCode}: ${b.slice(0,200)}`))); });
    req.on('error', rej); req.write(body); req.end();
  });
}
function dldPage(fromMDY, toMDY, take, skip) {
  const body = JSON.stringify({ P_FROM_DATE: fromMDY, P_TO_DATE: toMDY, P_GROUP_ID: '', P_IS_OFFPLAN: '', P_IS_FREE_HOLD: '', P_AREA_ID: '', P_USAGE_ID: '', P_PROP_TYPE_ID: '', P_TAKE: String(take), P_SKIP: String(skip), P_SORT: 'TRANSACTION_NUMBER_ASC' });
  return new Promise((res, rej) => {
    const req = https.request({ host: GATEWAY, path: '/open-data/transactions', method: 'POST',
      headers: { 'Content-Type': 'application/json', 'User-Agent': UA, 'Content-Length': Buffer.byteLength(body) }, timeout: 40000 },
      r => { let b = ''; r.on('data', d => b += d); r.on('end', () => { try { res(JSON.parse(b)); } catch (e) { rej(new Error('bad json: ' + b.slice(0, 120))); } }); });
    req.on('timeout', () => { req.destroy(); rej(new Error('timeout')); });
    req.on('error', rej); req.write(body); req.end();
  });
}
const sleep = ms => new Promise(r => setTimeout(r, ms));
const mdy = d => `${String(d.getMonth() + 1).padStart(2, '0')}/${String(d.getDate()).padStart(2, '0')}/${d.getFullYear()}`;
const iso = d => d.toISOString().slice(0, 10);

function slim(r) {
  return { n: r.TRANSACTION_NUMBER, d: (r.INSTANCE_DATE || '').slice(0, 10), proj: r.PROJECT_EN || '', mp: r.MASTER_PROJECT_EN || '', area: r.AREA_EN || '', v: r.TRANS_VALUE, sqm: r.ACTUAL_AREA || r.PROCEDURE_AREA || null, r: r.ROOMS_EN || '', op: r.IS_OFFPLAN ? 1 : 0, proc: r.PROCEDURE_EN || '', t: r.PROP_SB_TYPE_EN || r.PROP_TYPE_EN || '', use: r.USAGE_EN || '' };
}

async function main() {
  if (!GH_TOKEN) { console.error('[dld] no GH_TOKEN'); process.exit(1); }
  let cfg = { days_back: 14, seed_days: 120, page_size: 200, max_pages: 500, watch: [{ key: 'lagoons', match: ['damac lagoons'] }], keep_days_watch: 400, keep_days_summary: 400 };
  try { const m = await ghGet('tools/dld-feed/config.json'); cfg = Object.assign(cfg, JSON.parse(Buffer.from(m.content, 'base64').toString())); } catch (e) { console.error('[dld] config load failed, using defaults', e.message); }

  // seed run if no summary file yet
  let summarySha, summary = {};
  try { const m = await ghGet('data/dld/daily-summary.json'); summarySha = m.sha; summary = JSON.parse(Buffer.from(m.content, 'base64').toString()); } catch (_) {}
  const isSeed = !Object.keys(summary).length;
  const daysBack = isSeed ? cfg.seed_days : cfg.days_back;
  const to = new Date(); const from = new Date(Date.now() - daysBack * 86400000);
  console.log(`[dld] run ${isSeed ? 'SEED' : 'daily'}: ${iso(from)} -> ${iso(to)}`);

  const rows = [];
  let skip = 0, total = Infinity, pages = 0;
  while (skip < total && pages < cfg.max_pages) {
    let page;
    try { page = await dldPage(mdy(from), mdy(to), cfg.page_size, skip); }
    catch (e) { console.error(`[dld] page fail @${skip}: ${e.message} - retry once`); await sleep(5000); try { page = await dldPage(mdy(from), mdy(to), cfg.page_size, skip); } catch (e2) { console.error('[dld] retry failed, stopping pagination'); break; } }
    const result = page && page.response && page.response.result || [];
    if (!result.length) break;
    if (total === Infinity) { total = result[0].TOTAL || result.length; console.log(`[dld] total in window: ${total}`); }
    rows.push(...result.map(slim));
    skip += cfg.page_size; pages++;
    await sleep(1200);
  }
  console.log(`[dld] fetched ${rows.length} rows in ${pages} pages`);
  if (!rows.length) { console.error('[dld] zero rows - aborting without writes'); process.exit(1); }

  // citywide daily summary
  for (const r of rows) {
    if (!r.d) continue;
    const s = summary[r.d] = summary[r.d] || { count: 0, value: 0, offplan: 0, byArea: {} };
    if (s._seen && s._seen[r.n]) continue;
    s._seen = s._seen || {}; s._seen[r.n] = 1;
    s.count++; s.value += (r.v || 0); s.offplan += r.op;
    const a = r.area || '?'; s.byArea[a] = (s.byArea[a] || 0) + 1;
  }
  const cutS = iso(new Date(Date.now() - cfg.keep_days_summary * 86400000));
  for (const k of Object.keys(summary)) if (k < cutS) delete summary[k];
  // strip dedupe maps before storing (keep file small); dedupe only matters within run overlap
  const summaryOut = {};
  for (const [k, s] of Object.entries(summary)) summaryOut[k] = { count: s.count, value: Math.round(s.value), offplan: s.offplan, byArea: s.byArea };
  await ghPut('data/dld/daily-summary.json', summaryOut, summarySha, `dld-feed: summary ${iso(to)}`);
  console.log('[dld] pushed daily-summary.json');

  // watched projects - full slim rows, deduped, rolling window
  for (const w of cfg.watch) {
    const path = `data/dld/${w.key}.json`;
    let sha, existing = [];
    try { const m = await ghGet(path); sha = m.sha; existing = JSON.parse(Buffer.from(m.content, 'base64').toString()); } catch (_) {}
    if (!Array.isArray(existing)) existing = [];
    const match = s => w.match.some(m => (s || '').toLowerCase().includes(m.toLowerCase()));
    const fresh = rows.filter(r => match(r.proj) || match(r.mp) || match(r.area));
    const byN = new Map(existing.map(r => [r.n, r]));
    for (const r of fresh) byN.set(r.n, r);
    const cutW = iso(new Date(Date.now() - cfg.keep_days_watch * 86400000));
    const out = [...byN.values()].filter(r => r.d >= cutW).sort((a, b) => a.d < b.d ? -1 : 1);
    await ghPut(path, out, sha, `dld-feed: ${w.key} +${fresh.length} (${out.length} total)`);
    console.log(`[dld] pushed ${path}: +${fresh.length} fresh, ${out.length} in window`);
  }
  console.log('[dld] DONE');
}
main().catch(e => { console.error('[dld] fatal', e); process.exit(1); });
