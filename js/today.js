/* today.js - the Today page. Spec: tools/specs/2026-09-28-today-page.md
   Reads data/tasks.json and data/buyers.json at runtime. Writes both via the GitHub Contents API. */
'use strict';

const OWNER = 'calum7macleod', REPO = 'dashboards', BRANCH = 'main';
const TASKS_PATH = 'data/tasks.json', BUYERS_PATH = 'data/buyers.json';
const BANDS = [['today', 'Today'], ['week', 'This week'], ['month', 'This month'], ['year', 'This year']];
const AREAS = ['Real Estate', 'Content', 'Finance', 'Health', 'Investing', 'Personal'];
const AREA_COLOUR = { 'Real Estate': '#C9A84C', 'Content': '#E8C96B', 'Finance': '#8FA898', 'Health': '#7FB69B', 'Investing': '#B8A47C', 'Personal': '#F5EDE0', 'Buyers': '#E8C96B' };
const REFRESH_MS = 60000, NEXT_TOUCH_DAYS = 3, CALLS_SHOWN = 5;

const $ = id => document.getElementById(id);
const state = { tasks: null, tasksSha: null, buyers: null, buyersSha: null, open: new Set(), acts: new Set(),
                filter: localStorage.getItem('today_filter') || 'All', newArea: localStorage.getItem('today_area') || 'Real Estate',
                bandsOpen: JSON.parse(localStorage.getItem('today_bands') || '{"today":true}'), allCalls: false, pending: [], saving: false, undo: null };

/* ---------- dates ---------- */
function todayStr(d) { d = d || new Date(); return d.getFullYear() + '-' + String(d.getMonth() + 1).padStart(2, '0') + '-' + String(d.getDate()).padStart(2, '0'); }
function addDays(s, n) { const d = new Date(s + 'T00:00:00'); d.setDate(d.getDate() + n); return todayStr(d); }
function weekEnd() { const d = new Date(); const dow = (d.getDay() + 6) % 7; return addDays(todayStr(d), 6 - dow); }
function monthEnd() { const d = new Date(); return todayStr(new Date(d.getFullYear(), d.getMonth() + 1, 0)); }
function daysBetween(a, b) { return Math.round((new Date(b + 'T00:00:00') - new Date(a + 'T00:00:00')) / 86400000); }
function shortDate(s) { const d = new Date(s + 'T00:00:00'); return d.toLocaleDateString('en-GB', { weekday: 'short', day: 'numeric' }); }
function longDate() { return new Date().toLocaleDateString('en-GB', { weekday: 'long', day: 'numeric', month: 'long' }); }

/* ---------- github ---------- */
function getToken() { return localStorage.getItem('dashboards_gh_token') || localStorage.getItem('crm_pat') || ''; }
function setToken(t) { t = (t || '').trim(); if (!t) return; localStorage.setItem('dashboards_gh_token', t); localStorage.setItem('crm_pat', t); }
function headers(write) { const h = { 'Accept': 'application/vnd.github+json' }; const t = getToken(); if (t) h['Authorization'] = 'Bearer ' + t; if (write) h['Content-Type'] = 'application/json'; return h; }
function url(path) { return `https://api.github.com/repos/${OWNER}/${REPO}/contents/${path}`; }
function b64enc(s) { return btoa(unescape(encodeURIComponent(s))); }
function b64dec(s) { return decodeURIComponent(escape(atob(s.replace(/\n/g, '')))); }

async function fetchFile(path) {
  const r = await fetch(`${url(path)}?ref=${BRANCH}&t=${Date.now()}`, { headers: headers(false), cache: 'no-store' });
  if (r.status === 401 || r.status === 403) { openGate(); throw new Error('token'); }
  if (!r.ok) throw new Error(path + ' ' + r.status);
  const j = await r.json();
  return { sha: j.sha, data: JSON.parse(b64dec(j.content)) };
}
async function putFile(path, data, sha, message) {
  const body = { message, branch: BRANCH, content: b64enc(JSON.stringify(data, null, 2) + '\n') };
  if (sha) body.sha = sha;
  const r = await fetch(url(path), { method: 'PUT', headers: headers(true), body: JSON.stringify(body) });
  if (r.status === 401 || r.status === 403) { openGate(); throw new Error('token'); }
  if (r.status === 409) return null;
  if (!r.ok) throw new Error('save ' + r.status);
  return (await r.json()).content.sha;
}

/* ---------- mutations: applied to state now, replayed on a fresh copy if someone else wrote first ---------- */
function mutate(file, fn, label) {
  fn(file === 'tasks' ? state.tasks : state.buyers);
  state.pending.push({ file, fn, label });
  render();
  saveSoon();
}
let saveTimer = null;
function saveSoon() { clearTimeout(saveTimer); saveTimer = setTimeout(save, 400); }
async function save() {
  if (state.saving || !state.pending.length) return;
  state.saving = true; sync('saving');
  try {
    for (const file of ['tasks', 'buyers']) {
      const mine = state.pending.filter(p => p.file === file);
      if (!mine.length) continue;
      const path = file === 'tasks' ? TASKS_PATH : BUYERS_PATH;
      let attempts = 0, sha = null;
      while (attempts < 3) {
        attempts++;
        const data = file === 'tasks' ? state.tasks : state.buyers;
        sha = await putFile(path, data, file === 'tasks' ? state.tasksSha : state.buyersSha, `${file}: ${mine.map(m => m.label).join('; ').slice(0, 120)} (today page)`);
        if (sha) break;
        // 409: someone wrote first. Reload, replay our mutations on their copy, try again.
        const fresh = await fetchFile(path);
        if (file === 'tasks') { state.tasks = fresh.data; state.tasksSha = fresh.sha; } else { state.buyers = fresh.data; state.buyersSha = fresh.sha; }
        mine.forEach(m => m.fn(file === 'tasks' ? state.tasks : state.buyers));
      }
      if (!sha) throw new Error('save conflict');
      if (file === 'tasks') state.tasksSha = sha; else state.buyersSha = sha;
      state.pending = state.pending.filter(p => p.file !== file);
    }
    sync('saved ' + new Date().toLocaleTimeString('en-GB', { hour: '2-digit', minute: '2-digit' }));
  } catch (e) {
    sync('save failed - ' + e.message); console.error(e);
  } finally {
    state.saving = false;
    if (state.pending.length) saveSoon();
  }
}
function sync(t) { $('sync').textContent = t; }

/* ---------- load + roll + refresh ---------- */
async function load(first) {
  try {
    const [t, b] = await Promise.all([fetchFile(TASKS_PATH), fetchFile(BUYERS_PATH)]);
    if (state.pending.length || state.saving) return; // never clobber unsaved work
    const changed = t.sha !== state.tasksSha || b.sha !== state.buyersSha;
    state.tasks = t.data; state.tasksSha = t.sha; state.buyers = b.data; state.buyersSha = b.sha;
    if (roll()) saveSoon();
    if (changed || first) render();
    if (first) sync('loaded');
  } catch (e) { if (e.message !== 'token') sync('load failed - ' + e.message); }
}
function roll() {
  const today = todayStr(), we = weekEnd(), me = monthEnd();
  let moved = 0;
  for (const t of state.tasks.tasks) {
    if (t.status !== 'active') continue;
    if (!t.band) { // legacy record: place it once
      t.band = t.due && t.due <= today ? 'today' : t.due && t.due <= we ? 'week' : t.due && t.due <= me ? 'month' : t.due ? 'year' : 'today';
      t.bandSince = today; moved++; continue;
    }
    let to = null;
    if (t.band !== 'today' && t.due && t.due <= today) to = 'today';
    else if (t.band === 'month' && t.due && t.due <= we) to = 'week';
    else if (t.band === 'year' && t.due && t.due <= me) to = 'month';
    else if (t.band === 'year' && t.snoozedUntil && t.snoozedUntil <= today) to = 'today';
    if (to) { t.band = to; t.bandSince = today; t.order = 999; moved++; }
  }
  if (moved) state.pending.push({ file: 'tasks', fn: () => {}, label: 'roll ' + moved });
  return moved > 0;
}
setInterval(() => { if (document.visibilityState === 'visible' && !state.saving && !state.pending.length) load(false); }, REFRESH_MS);
document.addEventListener('visibilitychange', () => { if (document.visibilityState === 'visible') load(false); });

/* ---------- derived ---------- */
const ord = t => Number.isFinite(t.order) ? t.order : 999;
function liveTasks(band) {
  return state.tasks.tasks.filter(t => t.status === 'active' && t.band === band && (state.filter === 'All' || t.area === state.filter))
    .sort((a, b) => ord(a) - ord(b));
}
function buyerCalls() {
  if (state.filter !== 'All' && state.filter !== 'Buyers') return [];
  const today = todayStr();
  return state.buyers.filter(b => !['Won', 'Lost'].includes(b.stage) && !/^closed/i.test(b.status || '') && b.nextTouch && b.nextTouch <= today)
    .sort((a, b) => (b.score || 0) - (a.score || 0) || a.nextTouch.localeCompare(b.nextTouch));
}
function doneToday() { const today = todayStr(); return state.tasks.tasks.filter(t => t.status === 'done' && t.completed === today); }

/* ---------- render ---------- */
function esc(s) { return String(s == null ? '' : s).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c])); }
function render() {
  if (!state.tasks || !state.buyers) return;
  $('h-date').textContent = longDate();
  renderChips();
  const wrap = $('bands'); const scroll = window.scrollY;
  wrap.innerHTML = '';
  for (const [key, label] of BANDS) wrap.appendChild(renderBand(key, label));
  wrap.appendChild(renderDone());
  initSortables();
  window.scrollTo(0, scroll);
}
function renderChips() {
  const chips = ['All', ...AREAS, 'Buyers'];
  $('chips').innerHTML = chips.map(a => `<button class="chip${state.filter === a ? ' on' : ''}" data-area="${esc(a)}">${a === 'All' ? '' : `<span class="dot" style="background:${AREA_COLOUR[a]}"></span>`}${esc(a)}</button>`).join('');
  const pill = $('areapill'); pill.children[0].style.background = AREA_COLOUR[state.newArea]; pill.children[1].textContent = state.newArea;
}
function renderBand(key, label) {
  const tasks = liveTasks(key), calls = key === 'today' ? buyerCalls() : [];
  const open = !!state.bandsOpen[key];
  const band = document.createElement('div'); band.className = `band ${key}${open ? ' open' : ''}`; band.dataset.band = key;
  band.innerHTML = `<div class="bandhead"><span class="car">▶</span><span class="eyebrow">${esc(label)}</span><span class="count">${tasks.length + calls.length}</span></div><div class="list"></div>`;
  const list = band.querySelector('.list');
  if (calls.length) {
    const show = state.allCalls ? calls : calls.slice(0, CALLS_SHOWN);
    list.insertAdjacentHTML('beforeend', `<div class="rule"><span class="eyebrow">Calls</span><i></i><span class="count">${calls.length}</span></div>`);
    show.forEach(b => list.appendChild(buyerRow(b)));
    if (calls.length > show.length) list.insertAdjacentHTML('beforeend', `<button class="act" data-allcalls style="margin:4px 0 8px 54px">Show all ${calls.length} calls</button>`);
    else if (state.allCalls && calls.length > CALLS_SHOWN) list.insertAdjacentHTML('beforeend', `<button class="act" data-allcalls style="margin:4px 0 8px 54px">Show top ${CALLS_SHOWN}</button>`);
    if (tasks.length) list.insertAdjacentHTML('beforeend', `<div class="rule"><span class="eyebrow">Tasks</span><i></i></div>`);
  }
  const sortList = document.createElement('div'); sortList.className = 'sortlist'; sortList.dataset.band = key;
  tasks.forEach(t => sortList.appendChild(taskRow(t)));
  list.appendChild(sortList);
  if (!tasks.length && !calls.length) list.insertAdjacentHTML('beforeend', `<div class="empty">Nothing here.</div>`);
  return band;
}
function taskRow(t) {
  const today = todayStr(), age = t.bandSince ? daysBetween(t.bandSince, today) : 0;
  const row = document.createElement('div'); row.className = `row task${state.open.has(t.id) ? ' open' : ''}${state.acts.has(t.id) ? ' acts-open' : ''}`; row.dataset.id = t.id; row.dataset.key = t.id;
  const moves = BANDS.filter(b => b[0] !== t.band).map(b => `<button class="act" data-move="${b[0]}">${b[1]}</button>`).join('');
  row.innerHTML = `
    <div class="main">
      <button class="tick" aria-label="Done"><span></span></button>
      <div class="title"><span class="dot" style="background:${AREA_COLOUR[t.area] || '#8FA898'};margin-right:8px;vertical-align:1px"></span>${esc(t.title)}</div>
      ${t.score ? `<span class="badge score">${'◆'.repeat(t.score)}</span>` : ''}
      ${age >= 1 ? `<span class="badge">${age}d</span>` : ''}
      ${t.due ? `<span class="badge due">${shortDate(t.due)}</span>` : ''}
      <button class="more" aria-label="More">⋯</button>
    </div>
    <div class="acts">${moves}<button class="act date" data-pick>Date</button><button class="act kill" data-kill>Delete</button></div>
    <div class="detail">
      <div class="scorerow"><span>Importance</span>${[1, 2, 3, 4, 5].map(n => `<button class="sc${(t.score || 0) >= n ? ' on' : ''}" data-sc="${n}">◆</button>`).join('')}</div>
      <textarea data-notes placeholder="Notes">${esc(t.notes)}</textarea>
      <div class="meta">
        <select data-area>${AREAS.map(a => `<option${a === t.area ? ' selected' : ''}>${a}</option>`).join('')}</select>
        <input type="date" data-due value="${esc(t.due || '')}">
        <span>${t.created ? 'added ' + shortDate(t.created) : ''}</span>
      </div>
    </div>`;
  return row;
}
function buyerRow(b) {
  const today = todayStr(), late = daysBetween(b.nextTouch, today);
  const row = document.createElement('div'); row.className = `row buyer${state.open.has('b:' + b.id) ? ' open' : ''}${state.acts.has('b:' + b.id) ? ' acts-open' : ''}`; row.dataset.buyer = b.id; row.dataset.key = 'b:' + b.id;
  row.innerHTML = `
    <div class="main">
      <button class="tick" aria-label="Called"><span></span></button>
      <div class="title">Call ${esc(b.buyer)}${b.touchReason ? ' - ' + esc(b.touchReason) : ''}</div>
      ${late >= 1 ? `<span class="badge">${late}d</span>` : ''}
      <span class="badge due">${b.score ? '★' + b.score : ''}</span>
      <button class="more" aria-label="More">⋯</button>
    </div>
    <div class="acts"><button class="act" data-push="1">Tomorrow</button><button class="act" data-push="3">3 days</button><button class="act" data-push="7">Next week</button><button class="act kill" data-drop>Remove</button></div>
    <div class="detail">
      <div>${b.phone ? `<a href="tel:${esc(b.phone.replace(/\s+/g, ''))}">${esc(b.phone)}</a> · ` : ''}${esc(b.stage)} · score ${esc(b.score || '-')}</div>
      ${b.nextStep ? `<div style="margin-top:6px">${esc(b.nextStep)}</div>` : ''}
      <div class="meta"><span>next touch</span><input type="date" data-next value="${esc(b.nextTouch)}"><span>last ${b.lastContact ? shortDate(b.lastContact) : '-'}</span></div>
    </div>`;
  return row;
}
function renderDone() {
  const done = doneToday(), open = !!state.bandsOpen.done;
  const band = document.createElement('div'); band.className = `band done${open ? ' open' : ''}`; band.dataset.band = 'done';
  band.innerHTML = `<div class="bandhead"><span class="car">▶</span><span class="eyebrow">Done today</span><span class="count">${done.length}</span></div><div class="list">${done.map(t => `<div class="row done" data-id="${esc(t.id)}"><div class="main"><button class="tick" data-undone aria-label="Not done"><span></span></button><div class="title" style="color:var(--muted);text-decoration:line-through">${esc(t.title)}</div></div></div>`).join('') || '<div class="empty">Nothing yet.</div>'}</div>`;
  return band;
}

/* ---------- sortable ---------- */
function initSortables() {
  if (!window.Sortable) return;
  document.querySelectorAll('.sortlist').forEach(el => {
    new Sortable(el, { group: 'tasks', animation: 150, delay: 180, delayOnTouchOnly: true, ghostClass: 'sortable-ghost', chosenClass: 'sortable-chosen', filter: 'button,textarea,select,input,.detail,.acts', preventOnFilter: false,
      onEnd: ev => {
        const id = ev.item.dataset.id, toBand = ev.to.dataset.band, ids = [...ev.to.querySelectorAll('.row.task')].map(r => r.dataset.id);
        const today = todayStr();
        mutate('tasks', d => {
          const t = d.tasks.find(x => x.id === id); if (!t) return;
          if (t.band !== toBand) { t.band = toBand; t.bandSince = today; }
          ids.forEach((tid, i) => { const x = d.tasks.find(y => y.id === tid); if (x) x.order = i + 1; });
        }, 'reorder');
      } });
  });
}

/* ---------- actions ---------- */
function findTask(id) { return state.tasks.tasks.find(t => t.id === id); }
function moveTask(id, band) { const today = todayStr(); state.acts.delete(id); mutate('tasks', d => { const t = d.tasks.find(x => x.id === id); if (!t) return; t.band = band; t.bandSince = today; t.order = 999; }, 'move to ' + band); }
function tickTask(row, id) {
  row.classList.add('fade');
  setTimeout(() => {
    const today = todayStr();
    mutate('tasks', d => { const t = d.tasks.find(x => x.id === id); if (t) { t.status = 'done'; t.completed = today; } }, 'done');
    toast('Done', () => mutate('tasks', d => { const t = d.tasks.find(x => x.id === id); if (t) { t.status = 'active'; t.completed = null; } }, 'undo done'));
  }, 320);
}
function tickBuyer(row, id) {
  row.classList.add('fade');
  setTimeout(() => {
    const today = todayStr();
    mutate('buyers', d => { const b = d.find(x => x.id === id); if (!b) return; b.lastContact = today; b.touches = b.touches || []; b.touches.push({ date: today, channel: 'call', summary: 'Called (today page)' }); b.nextTouch = addDays(today, NEXT_TOUCH_DAYS); }, 'call logged');
    toast('Call logged, next touch in ' + NEXT_TOUCH_DAYS + ' days', () => mutate('buyers', d => { const b = d.find(x => x.id === id); if (!b) return; b.touches.pop(); b.nextTouch = today; b.lastContact = null; }, 'undo call'));
  }, 320);
}
function addTask(title) {
  const today = todayStr(), id = (crypto.randomUUID ? crypto.randomUUID() : 'x' + Date.now());
  mutate('tasks', d => { d.tasks.unshift({ order: -1, top3: false, id, title, area: state.newArea, priority: 'medium', status: 'active', difficulty: 'medium', due: null, created: today, notes: '', completed: null, snoozedUntil: null, band: 'today', bandSince: today });
    d.tasks.filter(t => t.status === 'active' && t.band === 'today').sort((a, b) => ord(a) - ord(b)).forEach((t, i) => t.order = i + 1); }, 'add ' + title.slice(0, 40));
}
let toastTimer = null;
function toast(text, undo) { $('toast-text').textContent = text; state.undo = undo || null; $('toast-undo').style.display = undo ? '' : 'none'; $('toast').classList.add('show'); clearTimeout(toastTimer); toastTimer = setTimeout(() => { $('toast').classList.remove('show'); state.undo = null; }, 5000); }
function openGate() { $('gate').classList.add('show'); sync('token needed'); }

/* ---------- wiring ---------- */
function wire() {
  $('add').addEventListener('keydown', e => { if (e.key === 'Enter') { const v = e.target.value.trim(); if (v) { addTask(v); e.target.value = ''; } } });
  $('areapill').addEventListener('click', () => { state.newArea = AREAS[(AREAS.indexOf(state.newArea) + 1) % AREAS.length]; localStorage.setItem('today_area', state.newArea); renderChips(); });
  $('chips').addEventListener('click', e => { const c = e.target.closest('.chip'); if (!c) return; state.filter = c.dataset.area; localStorage.setItem('today_filter', state.filter); render(); });
  $('toast-undo').addEventListener('click', () => { if (state.undo) state.undo(); $('toast').classList.remove('show'); state.undo = null; });
  $('gate-save').addEventListener('click', () => { setToken($('gate-token').value); $('gate').classList.remove('show'); $('gate-token').value = ''; load(true); });

  const bands = $('bands');
  bands.addEventListener('click', e => {
    const head = e.target.closest('.bandhead');
    if (head) { const k = head.parentElement.dataset.band; state.bandsOpen[k] = !state.bandsOpen[k]; localStorage.setItem('today_bands', JSON.stringify(state.bandsOpen)); head.parentElement.classList.toggle('open'); return; }
    if (e.target.closest('[data-allcalls]')) { state.allCalls = !state.allCalls; render(); return; }
    const row = e.target.closest('.row'); if (!row) return;
    const id = row.dataset.id, bid = row.dataset.buyer;
    if (e.target.closest('[data-undone]')) { mutate('tasks', d => { const t = d.tasks.find(x => x.id === id); if (t) { t.status = 'active'; t.completed = null; } }, 'undone'); return; }
    if (e.target.closest('.tick')) { if (bid) tickBuyer(row, bid); else tickTask(row, id); return; }
    if (e.target.closest('.more')) { toggleActs(row.dataset.key); return; }
    if (e.target.closest('[data-sc]')) { const n = +e.target.closest('[data-sc]').dataset.sc; mutate('tasks', d => { const t = d.tasks.find(x => x.id === id); if (t) t.score = t.score === n ? null : n; }, 'score'); return; }
    if (e.target.closest('[data-push]')) { const n = +e.target.closest('[data-push]').dataset.push, to = addDays(todayStr(), n); state.acts.clear(); row.classList.add('fade'); setTimeout(() => { mutate('buyers', d => { const b = d.find(x => x.id === bid); if (b) b.nextTouch = to; }, 'push call'); toast('Call moved to ' + shortDate(to)); }, 320); return; }
    if (e.target.closest('[data-drop]')) { const was = state.buyers.find(x => x.id === bid); const prev = was && was.nextTouch; state.acts.clear(); row.classList.add('fade'); setTimeout(() => { mutate('buyers', d => { const b = d.find(x => x.id === bid); if (b) b.nextTouch = null; }, 'call removed'); toast('Removed from calls', () => mutate('buyers', d => { const b = d.find(x => x.id === bid); if (b) b.nextTouch = prev; }, 'undo remove')); }, 320); return; }
    if (e.target.closest('[data-move]')) { moveTask(id, e.target.closest('[data-move]').dataset.move); return; }
    if (e.target.closest('[data-kill]')) { row.classList.add('fade'); setTimeout(() => { mutate('tasks', d => { const t = d.tasks.find(x => x.id === id); if (t) { t.status = 'killed'; t.completed = todayStr(); } }, 'delete'); toast('Deleted', () => mutate('tasks', d => { const t = d.tasks.find(x => x.id === id); if (t) { t.status = 'active'; t.completed = null; } }, 'undo delete')); }, 320); return; }
    if (e.target.closest('[data-pick]')) { state.acts.delete(id); state.open.add(id); render(); const inp = bands.querySelector(`.row[data-id="${id}"] [data-due]`); if (inp && inp.showPicker) inp.showPicker(); return; }
    if (e.target.closest('.title')) { const key = bid ? 'b:' + bid : id; if (state.open.has(key)) state.open.delete(key); else state.open.add(key); row.classList.toggle('open'); return; }
  });
  bands.addEventListener('change', e => {
    const row = e.target.closest('.row'); if (!row) return;
    const id = row.dataset.id, bid = row.dataset.buyer, v = e.target.value;
    if (e.target.matches('[data-area]')) mutate('tasks', d => { const t = d.tasks.find(x => x.id === id); if (t) t.area = v; }, 'area');
    if (e.target.matches('[data-due]')) mutate('tasks', d => { const t = d.tasks.find(x => x.id === id); if (t) t.due = v || null; }, 'due');
    if (e.target.matches('[data-next]') && v) mutate('buyers', d => { const b = d.find(x => x.id === bid); if (b) b.nextTouch = v; }, 'next touch');
  });
  bands.addEventListener('focusout', e => {
    if (!e.target.matches('[data-notes]')) return;
    const row = e.target.closest('.row'), id = row.dataset.id, v = e.target.value;
    const t = findTask(id); if (t && t.notes !== v) mutate('tasks', d => { const x = d.tasks.find(y => y.id === id); if (x) x.notes = v; }, 'notes');
  });

  // swipe on a row (phone) = show the move chips. Same chips the ⋯ button shows on desk.
  let sx = 0, sy = 0, srow = null;
  bands.addEventListener('touchstart', e => { const m = e.target.closest('.main'); srow = m ? m.parentElement : null; if (!srow || !srow.dataset.key) { srow = null; return; } sx = e.touches[0].clientX; sy = e.touches[0].clientY; }, { passive: true });
  bands.addEventListener('touchend', e => { if (!srow) return; const dx = e.changedTouches[0].clientX - sx, dy = e.changedTouches[0].clientY - sy; if (Math.abs(dx) > 48 && Math.abs(dy) < 40) toggleActs(srow.dataset.key); srow = null; }, { passive: true });
}
function toggleActs(key) { if (state.acts.has(key)) state.acts.delete(key); else { state.acts.clear(); state.acts.add(key); } document.querySelectorAll('.row').forEach(r => r.classList.toggle('acts-open', state.acts.has(r.dataset.key))); }

wire();
if (!getToken()) openGate();
load(true);
