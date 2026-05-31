/* =========================================================================
   Tasks Dashboard — data layer + UI
   Single source of truth: data/tasks.json in the GitHub repo.
   All reads/writes go through the GitHub Contents API.
   ========================================================================= */

/* ---- Config -------------------------------------------------------------
   Non-secret defaults live here. A gitignored config.js may set
   window.TASKS_CONFIG = { owner, repo, branch, path, token } to override
   them (handy for local dev). On the live site config.js is absent, so the
   token is collected via the Connect panel and kept in localStorage.        */
const CFG = Object.assign({
  owner:  'calum7macleod',
  repo:   'dashboards',
  branch: 'main',
  path:   'data/tasks.json'
}, (window.TASKS_CONFIG || {}));

const TOKEN_KEY = 'dashboards_gh_token';
function getToken() { return (window.TASKS_CONFIG && window.TASKS_CONFIG.token) || localStorage.getItem(TOKEN_KEY) || ''; }
function setToken(t) { if (t) localStorage.setItem(TOKEN_KEY, t.trim()); else localStorage.removeItem(TOKEN_KEY); }

/* ---- Constants ---------------------------------------------------------- */
const AREAS = ['Real Estate', 'Health', 'Content', 'Finance', 'Investing', 'Tasks'];
const AREA_COLOR = {
  'Real Estate': '#58a6ff',
  'Health':      '#3fb950',
  'Content':     '#d2a8ff',
  'Finance':     '#e3b341',
  'Investing':   '#56d364',
  'Tasks':       '#f0883e'
};
const PRIO_LABEL = { high: 'High', medium: 'Medium', low: 'Low' };

/* ---- App state ---------------------------------------------------------- */
const state = {
  tasks: [],
  sha: null,            // current sha of tasks.json (null = file does not exist yet)
  activeArea: 'all',    // 'all' or an area name
  filterPriority: '',
  search: '',
  showDone: false,
  loaded: false
};

/* ---- Small helpers ------------------------------------------------------ */
const $  = (id) => document.getElementById(id);
const esc = (s) => String(s == null ? '' : s).replace(/[&<>"']/g, c => ({ '&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;' }[c]));
const uid = () => (crypto.randomUUID ? crypto.randomUUID() : 't_' + Date.now().toString(36) + Math.random().toString(36).slice(2, 8));

function todayStr(d) {
  d = d || new Date();
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;
}
function addDaysStr(days) {
  const d = new Date();
  d.setDate(d.getDate() + days);
  return todayStr(d);
}
function prettyDate(iso) {
  if (!iso) return '';
  const [y, m, dd] = iso.split('-').map(Number);
  const d = new Date(y, m - 1, dd);
  return d.toLocaleDateString('en-GB', { day: 'numeric', month: 'short' });
}
function dueState(iso) {
  if (!iso) return '';
  const t = todayStr();
  if (iso < t) return 'overdue';
  if (iso === t) return 'today';
  return '';
}

/* UTF-8 safe base64 (handles emoji / accents in titles & notes) */
function b64encode(str) { return btoa(unescape(encodeURIComponent(str))); }
function b64decode(str) { return decodeURIComponent(escape(atob(str.replace(/\n/g, '')))); }

/* =========================================================================
   GitHub Contents API
   ========================================================================= */
function apiUrl() {
  return `https://api.github.com/repos/${CFG.owner}/${CFG.repo}/contents/${CFG.path}`;
}
function ghHeaders(write) {
  const h = { 'Accept': 'application/vnd.github+json' };
  const tok = getToken();
  if (tok) h['Authorization'] = 'Bearer ' + tok;
  if (write) h['Content-Type'] = 'application/json';
  return h;
}

/* Fetch tasks.json (+ its sha). Returns true on success. */
async function loadTasks() {
  setSaveState('saving', 'Loading…');
  try {
    const res = await fetch(`${apiUrl()}?ref=${encodeURIComponent(CFG.branch)}&t=${Date.now()}`, {
      headers: ghHeaders(false),
      cache: 'no-store'
    });
    if (res.status === 404) {                 // file not created yet
      state.tasks = [];
      state.sha = null;
    } else if (!res.ok) {
      throw new Error(`GitHub read failed (${res.status})`);
    } else {
      const json = await res.json();
      state.sha = json.sha;
      const parsed = JSON.parse(b64decode(json.content || ''));
      state.tasks = normalise(Array.isArray(parsed) ? parsed : (parsed.tasks || []));
    }
    autoWake();
    state.loaded = true;
    setSaveState('ok', 'Synced');
    render();
    return true;
  } catch (err) {
    setSaveState('error', 'Load failed');
    toast(err.message || 'Could not load tasks', true);
    render();
    return false;
  }
}

/* Persist current state.tasks back to GitHub. Serialised + 409-safe. */
let writeChain = Promise.resolve();
function saveTasks() {
  if (!getToken()) { openGate(); return Promise.resolve(false); }
  setSaveState('saving', 'Saving…');
  writeChain = writeChain.then(() => putOnce(true)).then(
    () => { setSaveState('ok', 'Synced'); return true; },
    (err) => { setSaveState('error', 'Save failed'); toast(err.message || 'Save failed', true); return false; }
  );
  return writeChain;
}

async function putOnce(allowRetry) {
  const body = {
    message: `tasks: update (${todayStr()})`,
    content: b64encode(JSON.stringify({ tasks: state.tasks }, null, 2) + '\n'),
    branch: CFG.branch
  };
  if (state.sha) body.sha = state.sha;

  const res = await fetch(apiUrl(), { method: 'PUT', headers: ghHeaders(true), body: JSON.stringify(body) });

  if (res.status === 409 && allowRetry) {      // sha conflict — refresh and retry once
    await refreshSha();
    return putOnce(false);
  }
  if (res.status === 401 || res.status === 403) {
    openGate();
    throw new Error('GitHub rejected the token (check it has Contents write access)');
  }
  if (!res.ok) {
    let msg = `Save failed (${res.status})`;
    try { const e = await res.json(); if (e.message) msg += ': ' + e.message; } catch (_) {}
    throw new Error(msg);
  }
  const out = await res.json();
  if (out.content && out.content.sha) state.sha = out.content.sha;
}

async function refreshSha() {
  const res = await fetch(`${apiUrl()}?ref=${encodeURIComponent(CFG.branch)}&t=${Date.now()}`, { headers: ghHeaders(false), cache: 'no-store' });
  state.sha = res.ok ? (await res.json()).sha : null;
}

/* =========================================================================
   Mutations  (optimistic: update memory + UI, then persist)
   ========================================================================= */
function mutate(fn) { fn(); render(); saveTasks(); }

function addTask({ title, area, priority, due, notes }) {
  state.tasks.unshift({
    id: uid(),
    title: title.trim(),
    area,
    priority,
    status: 'active',
    due: due || null,
    created: todayStr(),
    notes: (notes || '').trim() || null,
    completed: null,
    snoozedUntil: null
  });
}

function findTask(id) { return state.tasks.find(t => t.id === id); }

function toggleDone(id) {
  const t = findTask(id); if (!t) return;
  if (t.status === 'done') { t.status = 'active'; t.completed = null; }
  else { t.status = 'done'; t.completed = todayStr(); t.snoozedUntil = null; }
}
function snooze(id) {
  const t = findTask(id); if (!t) return;
  if (t.status === 'snoozed') { t.status = 'active'; t.snoozedUntil = null; }
  else { t.status = 'snoozed'; t.snoozedUntil = addDaysStr(7); t.completed = null; }
}
function removeTask(id) {
  const i = state.tasks.findIndex(t => t.id === id);
  if (i > -1) state.tasks.splice(i, 1);
}

/* Snoozed tasks whose timer has elapsed return to active automatically. */
function autoWake() {
  const t = todayStr();
  state.tasks.forEach(task => {
    if (task.status === 'snoozed' && task.snoozedUntil && task.snoozedUntil <= t) {
      task.status = 'active';
      task.snoozedUntil = null;
    }
  });
}

/* Backfill any missing fields on load so older/manual records are safe. */
function normalise(arr) {
  return arr.map(t => ({
    id: t.id || uid(),
    title: t.title || '(untitled)',
    area: AREAS.includes(t.area) ? t.area : 'Tasks',
    priority: ['high', 'medium', 'low'].includes(t.priority) ? t.priority : 'medium',
    status: ['active', 'done', 'snoozed'].includes(t.status) ? t.status : 'active',
    due: t.due || null,
    created: t.created || todayStr(),
    notes: t.notes || null,
    completed: t.completed || null,
    snoozedUntil: t.snoozedUntil || null
  }));
}

/* =========================================================================
   Rendering
   ========================================================================= */
function visibleTasks() {
  return state.tasks.filter(t => {
    if (state.activeArea !== 'all' && t.area !== state.activeArea) return false;
    if (state.filterPriority && t.priority !== state.filterPriority) return false;
    if (!state.showDone && t.status === 'done') return false;
    if (state.search) {
      const q = state.search.toLowerCase();
      if (!(t.title.toLowerCase().includes(q) || (t.notes || '').toLowerCase().includes(q))) return false;
    }
    return true;
  });
}

/* Sort: active first, then snoozed, then done. Within, by priority, then due. */
const STATUS_ORDER = { active: 0, snoozed: 1, done: 2 };
const PRIO_ORDER = { high: 0, medium: 1, low: 2 };
function sortTasks(list) {
  return list.slice().sort((a, b) => {
    if (STATUS_ORDER[a.status] !== STATUS_ORDER[b.status]) return STATUS_ORDER[a.status] - STATUS_ORDER[b.status];
    if (PRIO_ORDER[a.priority] !== PRIO_ORDER[b.priority]) return PRIO_ORDER[a.priority] - PRIO_ORDER[b.priority];
    if (a.due && b.due) return a.due < b.due ? -1 : a.due > b.due ? 1 : 0;
    if (a.due) return -1;
    if (b.due) return 1;
    return 0;
  });
}

function render() {
  renderTabs();
  renderStats();
  renderList();
  renderDoneToday();
}

function renderTabs() {
  const counts = {};
  AREAS.forEach(a => counts[a] = 0);
  let allActive = 0;
  state.tasks.forEach(t => {
    if (t.status !== 'done') { counts[t.area] = (counts[t.area] || 0) + 1; allActive++; }
  });
  const tab = (key, label, n) =>
    `<div class="tab ${state.activeArea === key ? 'active' : ''}" data-area="${esc(key)}">${esc(label)}<span class="tab-n">${n}</span></div>`;
  $('tabs').innerHTML =
    tab('all', 'All', allActive) +
    AREAS.map(a => tab(a, a, counts[a] || 0)).join('');
  document.querySelectorAll('.tab').forEach(el => el.addEventListener('click', () => {
    state.activeArea = el.dataset.area;
    render();
  }));
}

function renderStats() {
  const t = todayStr();
  const active = state.tasks.filter(x => x.status === 'active').length;
  const high = state.tasks.filter(x => x.status === 'active' && x.priority === 'high').length;
  const doneToday = state.tasks.filter(x => x.status === 'done' && x.completed === t).length;
  const snoozed = state.tasks.filter(x => x.status === 'snoozed').length;
  const overdue = state.tasks.filter(x => x.status === 'active' && x.due && x.due < t).length;

  $('count-active').textContent = active;
  $('count-high').textContent = high;

  $('stats').innerHTML = [
    statCard('Active Tasks', active, overdue ? `${overdue} overdue` : 'Nothing overdue'),
    statCard('High Priority', high, 'Need attention'),
    statCard('Done Today', doneToday, 'Keep it up'),
    statCard('Snoozed', snoozed, 'Resting')
  ].join('');
}
function statCard(title, value, sub) {
  return `<div class="card"><div class="card-title">${title}</div><div class="stat-value">${value}</div><div class="stat-sub">${esc(sub)}</div></div>`;
}

function renderList() {
  const list = sortTasks(visibleTasks());
  if (!list.length) {
    $('task-list').innerHTML = `<div class="card empty">${state.loaded ? 'No tasks here. Add one with <b>+ New Task</b>.' : 'Loading…'}</div>`;
    return;
  }
  $('task-list').innerHTML = list.map(taskCard).join('');
  document.querySelectorAll('#task-list [data-act]').forEach(el => {
    el.addEventListener('click', () => {
      const id = el.dataset.id, act = el.dataset.act;
      if (act === 'done') mutate(() => toggleDone(id));
      else if (act === 'snooze') mutate(() => snooze(id));
      else if (act === 'delete') {
        const tsk = findTask(id);
        if (confirm(`Delete "${tsk ? tsk.title : 'this task'}"?`)) mutate(() => removeTask(id));
      }
    });
  });
}

function taskCard(t) {
  const ds = dueState(t.due);
  const dueHtml = t.due
    ? `<span class="due ${ds}">📅 ${ds === 'today' ? 'Today' : ds === 'overdue' ? 'Overdue · ' + prettyDate(t.due) : prettyDate(t.due)}</span>`
    : '';
  const snoozeHtml = t.status === 'snoozed' && t.snoozedUntil
    ? `<span class="due">💤 until ${prettyDate(t.snoozedUntil)}</span>` : '';
  const notesHtml = t.notes ? `<div class="task-notes">${esc(t.notes)}</div>` : '';
  return `
  <div class="task-card prio-${t.priority} ${t.status === 'done' ? 'is-done' : ''} ${t.status === 'snoozed' ? 'is-snoozed' : ''}">
    <button class="check ${t.status === 'done' ? 'done' : ''}" data-act="done" data-id="${t.id}" title="${t.status === 'done' ? 'Mark active' : 'Mark done'}"></button>
    <div class="task-body">
      <div class="task-title">${esc(t.title)}</div>
      <div class="task-meta">
        <span class="area-badge"><span class="area-dot" style="background:${AREA_COLOR[t.area] || '#8b949e'}"></span>${esc(t.area)}</span>
        <span class="badge badge-${t.priority}">${PRIO_LABEL[t.priority]}</span>
        ${dueHtml}${snoozeHtml}
      </div>
      ${notesHtml}
    </div>
    <div class="task-actions">
      <button class="icon-btn" data-act="snooze" data-id="${t.id}" title="${t.status === 'snoozed' ? 'Unsnooze' : 'Snooze 7 days'}">${t.status === 'snoozed' ? '⏰' : '💤'}</button>
      <button class="icon-btn danger" data-act="delete" data-id="${t.id}" title="Delete">🗑</button>
    </div>
  </div>`;
}

function renderDoneToday() {
  const t = todayStr();
  const done = state.tasks.filter(x => x.status === 'done' && x.completed === t);
  if (!done.length) {
    $('done-today').innerHTML = `<div class="empty" style="padding:18px">Nothing completed yet today.</div>`;
    return;
  }
  $('done-today').innerHTML = done.map(x => `
    <div class="done-row">
      <span class="done-tick">✓</span>
      <span class="done-title">${esc(x.title)}</span>
      <span class="area-badge"><span class="area-dot" style="background:${AREA_COLOR[x.area] || '#8b949e'}"></span>${esc(x.area)}</span>
    </div>`).join('');
}

/* =========================================================================
   Sync indicator + toast
   ========================================================================= */
function setSaveState(kind, text) {
  const el = $('save-dot');
  if (!el) return;
  el.className = 'save-dot' + (kind === 'saving' ? ' saving' : kind === 'error' ? ' error' : '');
  $('save-text').textContent = text;
}
let toastTimer;
function toast(msg, isErr) {
  const el = $('toast');
  el.textContent = msg;
  el.className = 'toast show' + (isErr ? ' err' : '');
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => { el.className = 'toast' + (isErr ? ' err' : ''); }, 3200);
}

/* =========================================================================
   Connect gate
   ========================================================================= */
function openGate() {
  $('gate').classList.add('show');
  $('gate-token').focus();
}
function closeGate() { $('gate').classList.remove('show'); }

/* =========================================================================
   Wiring
   ========================================================================= */
function fillAreaSelect() {
  $('f-area').innerHTML = AREAS.map(a => `<option value="${esc(a)}">${esc(a)}</option>`).join('');
}

function submitNewTask() {
  const title = $('f-title').value.trim();
  if (!title) { toast('Give the task a title', true); $('f-title').focus(); return; }
  if (!getToken()) { openGate(); toast('Connect GitHub first to save', true); return; }
  mutate(() => addTask({
    title,
    area: $('f-area').value,
    priority: $('f-priority').value,
    due: $('f-due').value || null,
    notes: $('f-notes').value
  }));
  // reset form
  $('f-title').value = ''; $('f-due').value = ''; $('f-notes').value = '';
  $('f-priority').value = 'medium';
  $('form-card').classList.remove('open');
}

function wire() {
  fillAreaSelect();

  $('btn-new').addEventListener('click', () => {
    const c = $('form-card');
    c.classList.toggle('open');
    if (c.classList.contains('open')) $('f-title').focus();
  });
  $('f-cancel').addEventListener('click', () => $('form-card').classList.remove('open'));
  $('f-add').addEventListener('click', submitNewTask);
  $('f-title').addEventListener('keydown', e => { if (e.key === 'Enter') submitNewTask(); });
  $('f-notes').addEventListener('keydown', e => { if (e.key === 'Enter') submitNewTask(); });

  $('filter-priority').addEventListener('change', e => { state.filterPriority = e.target.value; render(); });
  $('filter-search').addEventListener('input', e => { state.search = e.target.value; render(); });
  $('toggle-done').addEventListener('change', e => { state.showDone = e.target.checked; render(); });

  $('btn-refresh').addEventListener('click', () => loadTasks());
  $('btn-settings').addEventListener('click', () => {
    if ($('gate').classList.contains('show')) closeGate();
    else { $('gate-token').value = getToken(); openGate(); }
  });
  $('gate-save').addEventListener('click', () => {
    const t = $('gate-token').value.trim();
    if (!t) { toast('Paste a token first', true); return; }
    setToken(t);
    $('gate-token').value = '';
    closeGate();
    toast('Connected to GitHub');
    loadTasks();
  });
  $('gate-token').addEventListener('keydown', e => { if (e.key === 'Enter') $('gate-save').click(); });
}

/* ---- Boot --------------------------------------------------------------- */
function init() {
  $('header-date').textContent = new Date().toLocaleDateString('en-GB', { weekday: 'long', day: 'numeric', month: 'long', year: 'numeric' });
  wire();
  render();          // paint skeleton immediately
  loadTasks();       // then pull live data (read works without a token on a public repo)
}

if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
else init();
