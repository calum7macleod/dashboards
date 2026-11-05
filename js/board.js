/* board.js - content production board. Reads data/content.json at runtime, writes it via the GitHub Contents API.
   Spec: handoff h0113 (Content -> Manager, 5 Nov 2026). Content owns content.json; this page is Calum's hand on it. */
'use strict';

const OWNER = 'calum7macleod', REPO = 'dashboards', BRANCH = 'main', PATH = 'data/content.json';
const DEFAULT_STAGES = ['idea', 'hooked', 'scripted', 'filmed', 'edited', 'scheduled', 'posted', 'measured'];
const STATUS_TO_STAGE = { template: 'idea', drafted: 'hooked', committed: 'scripted', scripted: 'scripted', final: 'scripted', superseded: null, posted: 'posted' };
const REFRESH_MS = 60000;

const $ = id => document.getElementById(id);
const state = { data: null, sha: null, open: new Set(), filter: localStorage.getItem('board_filter') || 'All', pending: [], saving: false, undo: null };

function todayStr(d) { d = d || new Date(); return d.getFullYear() + '-' + String(d.getMonth() + 1).padStart(2, '0') + '-' + String(d.getDate()).padStart(2, '0'); }
function shortDate(s) { if (!s) return ''; const d = new Date(s + 'T00:00:00'); return isNaN(d) ? s : d.toLocaleDateString('en-GB', { day: 'numeric', month: 'short' }); }
function esc(s) { return String(s == null ? '' : s).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c])); }
function cap(s) { return s ? s[0].toUpperCase() + s.slice(1) : ''; }

/* ---------- github ---------- */
function getToken() { return localStorage.getItem('dashboards_gh_token') || localStorage.getItem('crm_pat') || ''; }
function setToken(t) { t = (t || '').trim(); if (!t) return; localStorage.setItem('dashboards_gh_token', t); localStorage.setItem('crm_pat', t); }
function headers(write) { const h = { 'Accept': 'application/vnd.github+json' }; const t = getToken(); if (t) h['Authorization'] = 'Bearer ' + t; if (write) h['Content-Type'] = 'application/json'; return h; }
const url = `https://api.github.com/repos/${OWNER}/${REPO}/contents/${PATH}`;
function b64enc(s) { return btoa(unescape(encodeURIComponent(s))); }
function b64dec(s) { return decodeURIComponent(escape(atob(s.replace(/\n/g, '')))); }
async function fetchFile() {
  const r = await fetch(`${url}?ref=${BRANCH}&t=${Date.now()}`, { headers: headers(false), cache: 'no-store' });
  if (r.status === 401 || r.status === 403) { openGate(); throw new Error('token'); }
  if (!r.ok) throw new Error('load ' + r.status);
  const j = await r.json(); return { sha: j.sha, data: JSON.parse(b64dec(j.content)) };
}
async function putFile(data, sha, message) {
  const body = { message, branch: BRANCH, content: b64enc(JSON.stringify(data, null, 2) + '\n'), sha };
  const r = await fetch(url, { method: 'PUT', headers: headers(true), body: JSON.stringify(body) });
  if (r.status === 401 || r.status === 403) { openGate(); throw new Error('token'); }
  if (r.status === 409) return null;
  if (!r.ok) throw new Error('save ' + r.status);
  return (await r.json()).content.sha;
}

/* ---------- mutations with 409 replay ---------- */
function mutate(fn, label) { fn(state.data); state.pending.push({ fn, label }); render(); saveSoon(); }
let saveTimer = null;
function saveSoon() { clearTimeout(saveTimer); saveTimer = setTimeout(save, 400); }
async function save() {
  if (state.saving || !state.pending.length) return;
  state.saving = true; sync('saving');
  try {
    const mine = state.pending.slice(); let sha = null;
    for (let i = 0; i < 3 && !sha; i++) {
      sha = await putFile(state.data, state.sha, `content: ${mine.map(m => m.label).join('; ').slice(0, 120)} (board)`);
      if (!sha) { const fresh = await fetchFile(); state.data = fresh.data; state.sha = fresh.sha; mine.forEach(m => m.fn(state.data)); }
    }
    if (!sha) throw new Error('save conflict');
    state.sha = sha; state.pending = state.pending.filter(p => !mine.includes(p));
    sync('saved ' + new Date().toLocaleTimeString('en-GB', { hour: '2-digit', minute: '2-digit' }));
  } catch (e) { sync('save failed - ' + e.message); console.error(e); }
  finally { state.saving = false; if (state.pending.length) saveSoon(); }
}
function sync(t) { $('sync').textContent = t; }

/* ---------- load / refresh ---------- */
async function load(first) {
  try {
    const f = await fetchFile();
    if (state.pending.length || state.saving) return;
    const changed = f.sha !== state.sha;
    state.data = f.data; state.sha = f.sha;
    if (changed || first) render();
    if (first) sync('loaded');
  } catch (e) { if (e.message !== 'token') sync('load failed - ' + e.message); }
}
setInterval(() => { if (document.visibilityState === 'visible' && !state.saving && !state.pending.length) load(false); }, REFRESH_MS);
document.addEventListener('visibilitychange', () => { if (document.visibilityState === 'visible') load(false); });

/* ---------- derived ---------- */
function stages() { return Array.isArray(state.data.stages) && state.data.stages.length ? state.data.stages : DEFAULT_STAGES; }
function stageOf(c) { if (c.stage) return c.stage; const s = STATUS_TO_STAGE[c.status]; return s === undefined ? 'idea' : s; }
function pipeline() { return (state.data.pipeline || []).filter(c => stageOf(c) !== null); }
function seriesList() { const n = {}; pipeline().forEach(c => { const s = c.series || 'No series'; n[s] = (n[s] || 0) + 1; }); return Object.entries(n).sort((a, b) => b[1] - a[1]); }
function cardsIn(stage) {
  return pipeline().filter(c => stageOf(c) === stage && (state.filter === 'All' || (c.series || 'No series') === state.filter))
    .sort((a, b) => String(b.stageDate || b.created || '').localeCompare(String(a.stageDate || a.created || '')));
}

/* ---------- render ---------- */
function render() {
  if (!state.data) return;
  const list = seriesList();
  $('chips').innerHTML = [`<button class="chip${state.filter === 'All' ? ' on' : ''}" data-f="All">All<span class="n">${pipeline().length}</span></button>`]
    .concat(list.map(([s, n]) => `<button class="chip${state.filter === s ? ' on' : ''}" data-f="${esc(s)}">${esc(s)}<span class="n">${n}</span></button>`)).join('');
  const board = $('board'); const sx = board.scrollLeft; board.innerHTML = '';
  for (const st of stages()) {
    const cards = cardsIn(st);
    const col = document.createElement('div'); col.className = 'col'; col.dataset.stage = st;
    col.innerHTML = `<div class="colhead"><span class="eyebrow">${esc(cap(st))}</span><span class="count">${cards.length}</span></div><div class="cards" data-stage="${esc(st)}"></div>`;
    const wrap = col.querySelector('.cards');
    cards.forEach(c => wrap.appendChild(cardEl(c, st)));
    if (!cards.length) wrap.innerHTML = '<div class="empty">Nothing here.</div>';
    board.appendChild(col);
  }
  board.scrollLeft = sx;
  initSortables();
}
function cardEl(c, st) {
  const sts = stages(), i = sts.indexOf(st), prev = sts[i - 1], next = sts[i + 1];
  const el = document.createElement('div'); el.className = `card${state.open.has(c.id) ? ' open' : ''}`; el.dataset.id = c.id;
  const platforms = Array.isArray(c.platforms) ? c.platforms : (c.platforms ? String(c.platforms).split(/[,/ ]+/) : []);
  el.innerHTML = `
    <div class="t">${esc(c.title)}</div>
    ${c.hook ? `<div class="h">${esc(c.hook)}</div>` : ''}
    <div class="m">
      ${c.series ? `<span class="s">${esc(c.series)}</span>` : ''}
      ${c.stageDate || c.created ? `<span>${esc(cap(st))} ${shortDate(c.stageDate || c.created)}</span>` : ''}
      ${c.postDate ? `<span class="p">Post ${shortDate(c.postDate)}</span>` : ''}
      ${platforms.map(p => `<span class="pl">${esc(p)}</span>`).join('')}
    </div>
    <div class="detail">
      ${c.notes ? `<div>${esc(c.notes)}</div>` : ''}
      <div class="acts">
        ${prev ? `<button class="act" data-move="${esc(prev)}">◀ ${esc(cap(prev))}</button>` : ''}
        ${next ? `<button class="act next" data-move="${esc(next)}">${esc(cap(next))} ▶</button>` : ''}
        <select data-jump><option value="">Move to…</option>${sts.filter(s => s !== st).map(s => `<option value="${esc(s)}">${esc(cap(s))}</option>`).join('')}</select>
        <input type="date" data-post value="${esc(c.postDate || '')}" title="Post date">
      </div>
    </div>`;
  return el;
}
function initSortables() {
  if (!window.Sortable) return;
  document.querySelectorAll('.cards').forEach(el => new Sortable(el, { group: 'cards', animation: 150, delay: 200, delayOnTouchOnly: true, ghostClass: 'sortable-ghost', filter: 'button,select,input', preventOnFilter: false,
    onEnd: ev => { const id = ev.item.dataset.id, to = ev.to.dataset.stage; if (to && to !== stageOf(find(id))) moveCard(id, to); else render(); } }));
}

/* ---------- actions ---------- */
function find(id) { return (state.data.pipeline || []).find(c => c.id === id); }
function moveCard(id, to) {
  const c = find(id); if (!c) return; const from = stageOf(c), prevDate = c.stageDate, prevStatus = c.status, today = todayStr();
  mutate(d => { const x = d.pipeline.find(y => y.id === id); if (!x) return; x.stage = to; x.stageDate = today; if (to === 'posted' && !x.postDate) x.postDate = today; if (to === 'posted') x.status = 'posted'; }, `${c.title.slice(0, 40)} -> ${to}`);
  toast(`${cap(to)}`, () => mutate(d => { const x = d.pipeline.find(y => y.id === id); if (!x) return; x.stage = from; x.stageDate = prevDate; x.status = prevStatus; }, 'undo move'));
}
let toastTimer = null;
function toast(text, undo) { $('toast-text').textContent = text; state.undo = undo || null; $('toast-undo').style.display = undo ? '' : 'none'; $('toast').classList.add('show'); clearTimeout(toastTimer); toastTimer = setTimeout(() => { $('toast').classList.remove('show'); state.undo = null; }, 5000); }
function openGate() { $('gate').classList.add('show'); sync('token needed'); }

/* ---------- wiring ---------- */
$('chips').addEventListener('click', e => { const c = e.target.closest('.chip'); if (!c) return; state.filter = c.dataset.f; localStorage.setItem('board_filter', state.filter); render(); });
$('toast-undo').addEventListener('click', () => { if (state.undo) state.undo(); $('toast').classList.remove('show'); state.undo = null; });
$('gate-save').addEventListener('click', () => { setToken($('gate-token').value); $('gate').classList.remove('show'); $('gate-token').value = ''; load(true); });
$('board').addEventListener('click', e => {
  const card = e.target.closest('.card'); if (!card) return; const id = card.dataset.id;
  const mv = e.target.closest('[data-move]'); if (mv) { moveCard(id, mv.dataset.move); return; }
  if (e.target.closest('select, input')) return;
  if (state.open.has(id)) state.open.delete(id); else state.open.add(id); card.classList.toggle('open');
});
$('board').addEventListener('change', e => {
  const card = e.target.closest('.card'); if (!card) return; const id = card.dataset.id, v = e.target.value;
  if (e.target.matches('[data-jump]') && v) { moveCard(id, v); return; }
  if (e.target.matches('[data-post]')) mutate(d => { const x = d.pipeline.find(y => y.id === id); if (x) x.postDate = v || null; }, 'post date');
});
document.addEventListener('keydown', e => { if ((e.ctrlKey || e.metaKey) && !e.shiftKey && e.key.toLowerCase() === 'z' && state.undo) { e.preventDefault(); state.undo(); $('toast').classList.remove('show'); state.undo = null; } });

if (!getToken()) openGate();
load(true);
