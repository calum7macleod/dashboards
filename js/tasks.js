/* =========================================================================
   Tasks Dashboard — data layer + UI
   Single source of truth: data/tasks.json in the GitHub repo.
   All reads/writes go through the GitHub Contents API.

   File shape:
     { tasks: [...], units: [...], contentIdeas: [...], buildLog: [...] }
   ========================================================================= */

/* ---- Config ------------------------------------------------------------- */
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
  'Tasks':       '#f0883e',
  'General':     '#8b949e'
};
const PRIO_LABEL = { high: 'High', medium: 'Medium', low: 'Low' };
const DIFFICULTY = { easy: 1, medium: 3, hard: 5, intense: 8 };
const DIFF_LABEL = { easy: 'Easy', medium: 'Medium', hard: 'Hard', intense: 'Intense' };

const SECTIONS = [
  { key: 'tasks',        label: 'Tasks' },
  { key: 'units',        label: 'Units' },
  { key: 'content',      label: 'Content Ideas' },
  { key: 'build',        label: 'Build Log' },
  { key: 'productivity', label: 'Productivity' }
];
const CONTENT_STATUS = ['Idea', 'In Progress', 'Done'];
const BUILD_STATUS = ['Idea', 'Queued', 'In Progress', 'Done'];

/* ---- App state ---------------------------------------------------------- */
const state = {
  tasks: [],
  units: [],
  contentIdeas: [],
  buildLog: [],
  sha: null,
  section: 'tasks',
  activeArea: 'all',
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
function addDaysStr(days) { const d = new Date(); d.setDate(d.getDate() + days); return todayStr(d); }
function prettyDate(iso) {
  if (!iso) return '';
  const [y, m, dd] = iso.split('-').map(Number);
  return new Date(y, m - 1, dd).toLocaleDateString('en-GB', { day: 'numeric', month: 'short' });
}
function weekday(iso) {
  const [y, m, dd] = iso.split('-').map(Number);
  return new Date(y, m - 1, dd).toLocaleDateString('en-GB', { weekday: 'short' });
}
function dueState(iso) {
  if (!iso) return '';
  const t = todayStr();
  if (iso < t) return 'overdue';
  if (iso === t) return 'today';
  return '';
}

function b64encode(str) { return btoa(unescape(encodeURIComponent(str))); }
function b64decode(str) { return decodeURIComponent(escape(atob(str.replace(/\n/g, '')))); }

/* =========================================================================
   GitHub Contents API
   ========================================================================= */
function apiUrl() { return `https://api.github.com/repos/${CFG.owner}/${CFG.repo}/contents/${CFG.path}`; }
function ghHeaders(write) {
  const h = { 'Accept': 'application/vnd.github+json' };
  const tok = getToken();
  if (tok) h['Authorization'] = 'Bearer ' + tok;
  if (write) h['Content-Type'] = 'application/json';
  return h;
}

async function loadTasks() {
  setSaveState('saving', 'Loading…');
  try {
    const res = await fetch(`${apiUrl()}?ref=${encodeURIComponent(CFG.branch)}&t=${Date.now()}`, { headers: ghHeaders(false), cache: 'no-store' });
    if (res.status === 404) {
      state.tasks = []; state.units = []; state.contentIdeas = []; state.buildLog = []; state.sha = null;
    } else if (!res.ok) {
      throw new Error(`GitHub read failed (${res.status})`);
    } else {
      const json = await res.json();
      state.sha = json.sha;
      const parsed = JSON.parse(b64decode(json.content || ''));
      const obj = Array.isArray(parsed) ? { tasks: parsed } : parsed;
      state.tasks        = normaliseTasks(obj.tasks || []);
      state.units        = normaliseUnits(obj.units || []);
      state.contentIdeas = normaliseContent(obj.contentIdeas || []);
      state.buildLog     = normaliseBuild(obj.buildLog || []);
    }
    autoWake();
    state.loaded = true;
    setSaveState('ok', 'Synced');
    render();
    return true;
  } catch (err) {
    setSaveState('error', 'Load failed');
    toast(err.message || 'Could not load data', true);
    render();
    return false;
  }
}

let writeChain = Promise.resolve();
function save() {
  if (!getToken()) { openGate(); return Promise.resolve(false); }
  setSaveState('saving', 'Saving…');
  writeChain = writeChain.then(() => putOnce(true)).then(
    () => { setSaveState('ok', 'Synced'); return true; },
    (err) => { setSaveState('error', 'Save failed'); toast(err.message || 'Save failed', true); return false; }
  );
  return writeChain;
}

async function putOnce(allowRetry) {
  const payload = { tasks: state.tasks, units: state.units, contentIdeas: state.contentIdeas, buildLog: state.buildLog };
  const body = {
    message: `tasks: update (${todayStr()})`,
    content: b64encode(JSON.stringify(payload, null, 2) + '\n'),
    branch: CFG.branch
  };
  if (state.sha) body.sha = state.sha;

  const res = await fetch(apiUrl(), { method: 'PUT', headers: ghHeaders(true), body: JSON.stringify(body) });
  if (res.status === 409 && allowRetry) { await refreshSha(); return putOnce(false); }
  if (res.status === 401 || res.status === 403) { openGate(); throw new Error('GitHub rejected the token (needs Contents write access)'); }
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
   Normalisers  (backfill missing fields so manual edits stay safe)
   ========================================================================= */
function normaliseTasks(arr) {
  return arr.map(t => ({
    order: (typeof t.order === 'number' ? t.order : null),
    top3: t.top3 === true,
    id: t.id || uid(),
    title: t.title || '(untitled)',
    area: AREAS.includes(t.area) ? t.area : 'Tasks',
    priority: ['high', 'medium', 'low'].includes(t.priority) ? t.priority : 'medium',
    status: ['active', 'done', 'snoozed'].includes(t.status) ? t.status : 'active',
    difficulty: DIFFICULTY[t.difficulty] ? t.difficulty : 'medium',
    due: t.due || null,
    created: t.created || todayStr(),
    notes: t.notes || null,
    completed: t.completed || null,
    snoozedUntil: t.snoozedUntil || null
  }));
}
function normaliseUnits(arr) {
  return arr.map(u => ({
    id: u.id || uid(),
    unitNumber: u.unitNumber || '',
    development: u.development || '',
    notes: u.notes || null,
    dateAdded: u.dateAdded || todayStr()
  }));
}
function normaliseContent(arr) {
  return arr.map(c => ({
    id: c.id || uid(),
    title: c.title || '(untitled)',
    format: ['Reel', 'Carousel', 'Post', 'Story'].includes(c.format) ? c.format : 'Reel',
    status: CONTENT_STATUS.includes(c.status) ? c.status : 'Idea',
    priority: ['high', 'medium', 'low'].includes(c.priority) ? c.priority : 'medium',
    notes: c.notes || null,
    created: c.created || todayStr()
  }));
}
function normaliseBuild(arr) {
  return arr.map(b => ({
    id: b.id || uid(),
    title: b.title || '(untitled)',
    area: (AREAS.concat('General')).includes(b.area) ? b.area : 'General',
    priority: ['high', 'medium', 'low'].includes(b.priority) ? b.priority : 'medium',
    status: BUILD_STATUS.includes(b.status) ? b.status : 'Idea',
    notes: b.notes || null,
    created: b.created || todayStr()
  }));
}

/* =========================================================================
   Mutations  (optimistic: update memory + UI, then persist)
   ========================================================================= */
function mutate(fn) { fn(); render(); save(); }

/* --- tasks (unchanged behaviour) --- */
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
function removeTask(id) { const i = state.tasks.findIndex(t => t.id === id); if (i > -1) state.tasks.splice(i, 1); }
function autoWake() {
  const t = todayStr();
  state.tasks.forEach(task => {
    if (task.status === 'snoozed' && task.snoozedUntil && task.snoozedUntil <= t) { task.status = 'active'; task.snoozedUntil = null; }
  });
}

/* =========================================================================
   Rendering — top level
   ========================================================================= */
function render() {
  renderSectionTabs();
  updateHeaderCounts();
  SECTIONS.forEach(s => { const el = $('sec-' + s.key); if (el) el.hidden = (state.section !== s.key); });
  if (state.section === 'tasks') renderTasksSection();
  else if (state.section === 'units') renderUnits();
  else if (state.section === 'content') renderContent();
  else if (state.section === 'build') renderBuild();
  else if (state.section === 'productivity') renderProductivity();
}

function updateHeaderCounts() {
  $('count-active').textContent = state.tasks.filter(x => x.status === 'active').length;
  $('count-high').textContent = state.tasks.filter(x => x.status === 'active' && x.priority === 'high').length;
}

function renderSectionTabs() {
  const counts = {
    tasks: state.tasks.filter(t => t.status === 'active').length,
    units: state.units.length,
    content: state.contentIdeas.filter(c => c.status !== 'Done').length,
    build: state.buildLog.filter(b => b.status !== 'Done').length,
    productivity: scoreForDate(todayStr())
  };
  $('section-tabs').innerHTML = SECTIONS.map(s =>
    `<div class="tab ${state.section === s.key ? 'active' : ''}" data-sec="${s.key}">${esc(s.label)}<span class="tab-n">${counts[s.key]}</span></div>`
  ).join('');
  document.querySelectorAll('#section-tabs .tab').forEach(el => el.addEventListener('click', () => {
    state.section = el.dataset.sec; render();
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }));
}

/* =========================================================================
   TASKS section  (logic preserved from Phase 1)
   ========================================================================= */
function renderTasksSection() { renderAreaTabs(); renderStats(); renderList(); renderDoneToday(); }

function renderAreaTabs() {
  const counts = {}; AREAS.forEach(a => counts[a] = 0);
  let allActive = 0;
  state.tasks.forEach(t => { if (t.status !== 'done') { counts[t.area] = (counts[t.area] || 0) + 1; allActive++; } });
  const tab = (key, label, n) => `<div class="tab ${state.activeArea === key ? 'active' : ''}" data-area="${esc(key)}">${esc(label)}<span class="tab-n">${n}</span></div>`;
  $('tabs').innerHTML = tab('all', 'All', allActive) + AREAS.map(a => tab(a, a, counts[a] || 0)).join('');
  document.querySelectorAll('#tabs .tab').forEach(el => el.addEventListener('click', () => { state.activeArea = el.dataset.area; render(); }));
}

function renderStats() {
  const t = todayStr();
  const active = state.tasks.filter(x => x.status === 'active').length;
  const high = state.tasks.filter(x => x.status === 'active' && x.priority === 'high').length;
  const doneToday = state.tasks.filter(x => x.status === 'done' && x.completed === t).length;
  const snoozed = state.tasks.filter(x => x.status === 'snoozed').length;
  const overdue = state.tasks.filter(x => x.status === 'active' && x.due && x.due < t).length;
  $('stats').innerHTML = [
    statCard('Active Tasks', active, overdue ? `${overdue} overdue` : 'Nothing overdue'),
    statCard('High Priority', high, 'Need attention'),
    statCard('Done Today', doneToday, 'Keep it up'),
    statCard('Snoozed', snoozed, 'Resting')
  ].join('');
}
function statCard(title, value, sub, subColor) {
  return `<div class="card"><div class="card-title">${title}</div><div class="stat-value">${value}</div><div class="stat-sub"${subColor ? ` style="color:${subColor}"` : ''}>${esc(sub)}</div></div>`;
}

const STATUS_ORDER = { active: 0, snoozed: 1, done: 2 };
const PRIO_ORDER = { high: 0, medium: 1, low: 2 };
function sortTasks(list) {
  return list.slice().sort((a, b) => {
    if (STATUS_ORDER[a.status] !== STATUS_ORDER[b.status]) return STATUS_ORDER[a.status] - STATUS_ORDER[b.status];
    if (PRIO_ORDER[a.priority] !== PRIO_ORDER[b.priority]) return PRIO_ORDER[a.priority] - PRIO_ORDER[b.priority];
    if (a.due && b.due) return a.due < b.due ? -1 : a.due > b.due ? 1 : 0;
    if (a.due) return -1; if (b.due) return 1; return 0;
  });
}
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
function endOfWeekStr() { const d = new Date(); const diff = (7 - d.getDay()) % 7; d.setDate(d.getDate() + diff); return todayStr(d); }
function endOfMonthStr() { const d = new Date(); return todayStr(new Date(d.getFullYear(), d.getMonth() + 1, 0)); }
function taskGroup(t) {
  if (t.status === 'done') return 'done';
  if (t.status === 'snoozed') return 'snoozed';
  if (!t.due) return 'nodate';
  const td = todayStr();
  if (t.due < td) return 'overdue';
  if (t.due === td) return 'today';
  if (t.due <= endOfWeekStr()) return 'week';
  if (t.due <= endOfMonthStr()) return 'month';
  return 'later';
}
const GROUPS = [['overdue','Overdue'],['today','Today'],['week','This Week'],['month','This Month'],['later','Later'],['nodate','No Date'],['snoozed','Snoozed'],['done','Completed']];
function groupSort(list) {
  return list.slice().sort((a, b) => {
    const ao = a.order == null ? 1e9 : a.order, bo = b.order == null ? 1e9 : b.order;
    if (ao !== bo) return ao - bo;
    if (PRIO_ORDER[a.priority] !== PRIO_ORDER[b.priority]) return PRIO_ORDER[a.priority] - PRIO_ORDER[b.priority];
    if (a.due && b.due) return a.due < b.due ? -1 : 1;
    if (a.due) return -1; if (b.due) return 1; return 0;
  });
}
function renderList() {
  const vis = visibleTasks();
  const top3 = state.tasks.filter(t => t.top3 && t.status === 'active');
  let html = '';
  html += `<div class="group-header top3-header"><span>◆ Top 3 Today</span><span class="group-n">${top3.length}/3</span></div>`;
  html += `<div class="task-group top3-zone" data-group="top3">` + (top3.length ? groupSort(top3).map(taskCard).join('') : `<div class="top3-empty">Drag your three most important tasks here.</div>`) + `</div>`;
  if (!vis.length && !top3.length) {
    $('task-list').innerHTML = html + `<div class="card empty">${state.loaded ? 'No tasks here. Add one with <b>+ New Task</b>.' : 'Loading…'}</div>`;
    initSortables();
    return;
  }
  const buckets = {};
  vis.forEach(t => { if (t.top3 && t.status === 'active') return; const g = taskGroup(t); (buckets[g] = buckets[g] || []).push(t); });
  GROUPS.forEach(([key, label]) => {
    const items = buckets[key] || [];
    if (!items.length && !['today','week','month','nodate'].includes(key)) return;
    const nStyle = key === 'overdue' ? ' style="color:#f85149"' : '';
    html += `<div class="group-header"><span>${label}</span><span class="group-n"${nStyle}>${items.length}</span></div>`;
    html += `<div class="task-group" data-group="${key}">` + groupSort(items).map(taskCard).join('') + `</div>`;
  });
  $('task-list').innerHTML = html;
  document.querySelectorAll('#task-list [data-act]').forEach(el => el.addEventListener('click', () => {
    const id = el.dataset.id, act = el.dataset.act;
    if (act === 'done') mutate(() => toggleDone(id));
    else if (act === 'snooze') mutate(() => snooze(id));
    else if (act === 'delete') { const tsk = findTask(id); if (confirm(`Delete "${tsk ? tsk.title : 'this task'}"?`)) mutate(() => removeTask(id)); }
  }));
  initSortables();
}
function applyGroupDate(t, group) {
  if (group === 'top3') { t.top3 = true; if (!t.due || t.due > todayStr()) t.due = todayStr(); if (t.status === 'snoozed') { t.status = 'active'; t.snoozedUntil = null; } return; }
  t.top3 = false;
  if (group === 'today' || group === 'overdue') t.due = todayStr();
  else if (group === 'week') t.due = endOfWeekStr() === todayStr() ? todayStr() : endOfWeekStr();
  else if (group === 'month') t.due = endOfMonthStr();
  else if (group === 'later') { const d = new Date(); const nm = new Date(d.getFullYear(), d.getMonth() + 2, 0); t.due = todayStr(nm); }
  else if (group === 'nodate') t.due = null;
  else if (group === 'snoozed') { t.status = 'snoozed'; t.snoozedUntil = addDaysStr(7); return; }
  if (t.status === 'snoozed') { t.status = 'active'; t.snoozedUntil = null; }
}
function initSortables() {
  if (typeof Sortable === 'undefined') return;
  document.querySelectorAll('#task-list .task-group').forEach(el => {
    new Sortable(el, {
      group: 'tasks', handle: '.drag-handle', animation: 150, ghostClass: 'drag-ghost',
      onMove: (evt) => {
        if (evt.to.dataset.group === 'top3') {
          const n = evt.to.querySelectorAll('[data-tid]').length;
          if (evt.from !== evt.to && n >= 3) return false;
        }
        return true;
      },
      onEnd: (evt) => {
        const t = findTask(evt.item.dataset.tid);
        const toGroup = evt.to.dataset.group;
        if (t && toGroup) applyGroupDate(t, toGroup);
        const ids = Array.from(evt.to.querySelectorAll('[data-tid]')).map(x => x.dataset.tid);
        ids.forEach((id, i) => { const x = findTask(id); if (x) x.order = i + 1; });
        render(); save();
      }
    });
  });
}
function taskCard(t) {
  const ds = dueState(t.due);
  const dueHtml = t.due ? `<span class="due ${ds}">📅 ${ds === 'today' ? 'Today' : ds === 'overdue' ? 'Overdue · ' + prettyDate(t.due) : prettyDate(t.due)}</span>` : '';
  const snoozeHtml = t.status === 'snoozed' && t.snoozedUntil ? `<span class="due">💤 until ${prettyDate(t.snoozedUntil)}</span>` : '';
  const diffHtml = `<span class="badge badge-diff-${t.difficulty}" title="${DIFFICULTY[t.difficulty]} pts">${DIFF_LABEL[t.difficulty]}</span>`;
  const notesHtml = t.notes ? `<div class="task-notes">${esc(t.notes)}</div>` : '';
  return `
  <div class="task-card prio-${t.priority} ${t.status === 'done' ? 'is-done' : ''} ${t.status === 'snoozed' ? 'is-snoozed' : ''}" data-tid="${t.id}">
    <span class="drag-handle" title="Drag to reorder">⠿</span>
    <button class="check ${t.status === 'done' ? 'done' : ''}" data-act="done" data-id="${t.id}" title="${t.status === 'done' ? 'Mark active' : 'Mark done'}"></button>
    <div class="task-body">
      <div class="task-title">${esc(t.title)}</div>
      <div class="task-meta">
        <span class="area-badge"><span class="area-dot" style="background:${AREA_COLOR[t.area] || '#8b949e'}"></span>${esc(t.area)}</span>
        <span class="badge badge-${t.priority}">${PRIO_LABEL[t.priority]}</span>
        ${diffHtml}${dueHtml}${snoozeHtml}
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
  if (!done.length) { $('done-today').innerHTML = `<div class="empty" style="padding:18px">Nothing completed yet today.</div>`; return; }
  $('done-today').innerHTML = done.map(x => `
    <div class="done-row">
      <span class="done-tick">✓</span>
      <span class="done-title">${esc(x.title)}</span>
      <span class="pts">+${DIFFICULTY[x.difficulty]} pts</span>
      <span class="area-badge"><span class="area-dot" style="background:${AREA_COLOR[x.area] || '#8b949e'}"></span>${esc(x.area)}</span>
    </div>`).join('');
}

/* =========================================================================
   UNITS section
   ========================================================================= */
function renderUnits() {
  const rows = state.units.slice().sort((a, b) => (a.dateAdded < b.dateAdded ? 1 : -1));
  if (!rows.length) { $('u-tbody').innerHTML = `<tr><td colspan="5"><div class="empty">No units yet. Add one with <b>+ Add Unit</b>.</div></td></tr>`; return; }
  $('u-tbody').innerHTML = rows.map(u => `
    <tr>
      <td style="font-weight:600;white-space:nowrap">${esc(u.unitNumber)}</td>
      <td style="white-space:nowrap">${esc(u.development)}</td>
      <td style="color:#8b949e">${esc(u.notes || '')}</td>
      <td style="color:#6e7681;white-space:nowrap">${prettyDate(u.dateAdded)}</td>
      <td class="text-right"><button class="icon-btn danger" data-act="del-unit" data-id="${u.id}" title="Delete">🗑</button></td>
    </tr>`).join('');
  document.querySelectorAll('#u-tbody [data-act="del-unit"]').forEach(el => el.addEventListener('click', () => {
    const u = state.units.find(x => x.id === el.dataset.id);
    if (confirm(`Delete unit "${u ? u.unitNumber : ''}"?`)) mutate(() => { const i = state.units.findIndex(x => x.id === el.dataset.id); if (i > -1) state.units.splice(i, 1); });
  }));
}
function submitUnit() {
  const num = $('u-number').value.trim();
  if (!num) { toast('Enter a unit number', true); $('u-number').focus(); return; }
  if (!getToken()) { openGate(); toast('Connect GitHub first to save', true); return; }
  mutate(() => state.units.unshift({ id: uid(), unitNumber: num, development: $('u-dev').value.trim(), notes: $('u-notes').value.trim() || null, dateAdded: todayStr() }));
  $('u-number').value = ''; $('u-dev').value = ''; $('u-notes').value = '';
  $('u-form').classList.remove('open');
}

/* =========================================================================
   CONTENT IDEAS section
   ========================================================================= */
function renderContent() {
  const list = state.contentIdeas.slice().sort((a, b) => {
    const sd = (a.status === 'Done') - (b.status === 'Done'); if (sd) return sd;
    return PRIO_ORDER[a.priority] - PRIO_ORDER[b.priority];
  });
  if (!list.length) { $('c-list').innerHTML = `<div class="card empty">No content ideas yet. Add one with <b>+ Add Idea</b>.</div>`; return; }
  $('c-list').innerHTML = list.map(c => `
    <div class="task-card prio-${c.priority} ${c.status === 'Done' ? 'is-done' : ''}">
      <div class="task-body">
        <div class="task-title">${esc(c.title)}</div>
        <div class="task-meta">
          <span class="tag">${esc(c.format)}</span>
          <span class="badge badge-${c.priority}">${PRIO_LABEL[c.priority]}</span>
          ${statusSelect(c.id, 'content', c.status, CONTENT_STATUS)}
        </div>
        ${c.notes ? `<div class="task-notes">${esc(c.notes)}</div>` : ''}
      </div>
      <div class="task-actions">
        <button class="icon-btn" data-act="promote-content" data-id="${c.id}" title="Promote to task">⇧</button>
        <button class="icon-btn danger" data-act="del-content" data-id="${c.id}" title="Delete">🗑</button>
      </div>
    </div>`).join('');
  wireStatusSelects('content');
  document.querySelectorAll('#c-list [data-act="promote-content"]').forEach(el => el.addEventListener('click', () => {
    const c = state.contentIdeas.find(x => x.id === el.dataset.id);
    if (!c) return;
    mutate(() => {
      state.tasks.unshift({ id: uid(), title: c.title, area: 'Content', priority: c.priority || 'medium', difficulty: 'medium', status: 'active', due: null, created: todayStr(), notes: c.notes || null, completed: null, snoozedUntil: null, order: null, top3: false });
      c.status = 'In Progress';
    });
    toast('Promoted to task — drag it into a day bucket');
  }));
  document.querySelectorAll('#c-list [data-act="del-content"]').forEach(el => el.addEventListener('click', () => {
    const c = state.contentIdeas.find(x => x.id === el.dataset.id);
    if (confirm(`Delete "${c ? c.title : 'this idea'}"?`)) mutate(() => { const i = state.contentIdeas.findIndex(x => x.id === el.dataset.id); if (i > -1) state.contentIdeas.splice(i, 1); });
  }));
}
function submitContent() {
  const title = $('c-title').value.trim();
  if (!title) { toast('Give the idea a title', true); $('c-title').focus(); return; }
  if (!getToken()) { openGate(); toast('Connect GitHub first to save', true); return; }
  mutate(() => state.contentIdeas.unshift({ id: uid(), title, format: $('c-format').value, status: $('c-status').value, priority: $('c-priority').value, notes: $('c-notes').value.trim() || null, created: todayStr() }));
  $('c-title').value = ''; $('c-notes').value = ''; $('c-status').value = 'Idea'; $('c-priority').value = 'medium';
  $('c-form').classList.remove('open');
}

/* =========================================================================
   BUILD LOG section
   ========================================================================= */
function renderBuild() {
  const list = state.buildLog.slice().sort((a, b) => {
    const sd = (a.status === 'Done') - (b.status === 'Done'); if (sd) return sd;
    return PRIO_ORDER[a.priority] - PRIO_ORDER[b.priority];
  });
  if (!list.length) { $('b-list').innerHTML = `<div class="card empty">Nothing logged yet. Add one with <b>+ Add Item</b>.</div>`; return; }
  $('b-list').innerHTML = list.map(b => `
    <div class="task-card prio-${b.priority} ${b.status === 'Done' ? 'is-done' : ''}">
      <div class="task-body">
        <div class="task-title">${esc(b.title)}</div>
        <div class="task-meta">
          <span class="area-badge"><span class="area-dot" style="background:${AREA_COLOR[b.area] || '#8b949e'}"></span>${esc(b.area)}</span>
          <span class="badge badge-${b.priority}">${PRIO_LABEL[b.priority]}</span>
          ${statusSelect(b.id, 'build', b.status, BUILD_STATUS)}
        </div>
        ${b.notes ? `<div class="task-notes">${esc(b.notes)}</div>` : ''}
      </div>
      <div class="task-actions">
        <button class="icon-btn danger" data-act="del-build" data-id="${b.id}" title="Delete">🗑</button>
      </div>
    </div>`).join('');
  wireStatusSelects('build');
  document.querySelectorAll('#b-list [data-act="del-build"]').forEach(el => el.addEventListener('click', () => {
    const b = state.buildLog.find(x => x.id === el.dataset.id);
    if (confirm(`Delete "${b ? b.title : 'this item'}"?`)) mutate(() => { const i = state.buildLog.findIndex(x => x.id === el.dataset.id); if (i > -1) state.buildLog.splice(i, 1); });
  }));
}
function submitBuild() {
  const title = $('b-title').value.trim();
  if (!title) { toast('Give the item a title', true); $('b-title').focus(); return; }
  if (!getToken()) { openGate(); toast('Connect GitHub first to save', true); return; }
  mutate(() => state.buildLog.unshift({ id: uid(), title, area: $('b-area').value, priority: $('b-priority').value, status: $('b-status').value, notes: $('b-notes').value.trim() || null, created: todayStr() }));
  $('b-title').value = ''; $('b-notes').value = ''; $('b-status').value = 'Idea'; $('b-priority').value = 'medium';
  $('b-form').classList.remove('open');
}

/* Inline status editor shared by content + build */
function statusSelect(id, kind, current, options) {
  return `<select class="mini-select" data-status="${kind}" data-id="${id}">` +
    options.map(o => `<option ${o === current ? 'selected' : ''}>${o}</option>`).join('') + `</select>`;
}
function wireStatusSelects(kind) {
  document.querySelectorAll(`[data-status="${kind}"]`).forEach(sel => sel.addEventListener('change', () => {
    const arr = kind === 'content' ? state.contentIdeas : state.buildLog;
    const item = arr.find(x => x.id === sel.dataset.id);
    if (item) mutate(() => { item.status = sel.value; });
  }));
}

/* =========================================================================
   PRODUCTIVITY section  (derived from completed tasks' difficulty points)
   ========================================================================= */
function dailyMap() {
  const map = {};
  state.tasks.forEach(t => {
    if (t.status === 'done' && t.completed && DIFFICULTY[t.difficulty]) {
      const d = t.completed;
      if (!map[d]) map[d] = { points: 0, count: 0 };
      map[d].points += DIFFICULTY[t.difficulty];
      map[d].count++;
    }
  });
  return map;
}
function scoreForDate(d) { const m = dailyMap()[d]; return m ? m.points : 0; }
function band(score) {
  if (score >= 46) return { label: 'Elite', color: '#d2a8ff' };
  if (score >= 26) return { label: 'Strong', color: '#3fb950' };
  if (score >= 11) return { label: 'Solid', color: '#58a6ff' };
  return { label: 'Slow day', color: '#8b949e' };
}
function bandPill(score) { const b = band(score); return `<span class="band-pill" style="background:${b.color}22;color:${b.color}">${b.label}</span>`; }

function renderProductivity() {
  const map = dailyMap();
  const today = todayStr();
  const todayScore = map[today] ? map[today].points : 0;

  // last 7 days (chronological)
  const days = [];
  for (let i = 6; i >= 0; i--) { const d = addDaysStr(-i); days.push({ date: d, points: map[d] ? map[d].points : 0, count: map[d] ? map[d].count : 0 }); }
  const weekTotal = days.reduce((s, d) => s + d.points, 0);
  const allScores = Object.values(map).map(m => m.points);
  const bestDay = allScores.length ? Math.max(...allScores) : 0;

  // stats
  $('p-stats').innerHTML = [
    statCard("Today's Score", todayScore, band(todayScore).label, band(todayScore).color),
    statCard('This Week', weekTotal, 'Last 7 days'),
    statCard('Best Day', bestDay, 'All time'),
    statCard('Daily Avg (7d)', Math.round(weekTotal / 7), 'Points / day')
  ].join('');

  // 7-day bar chart
  const max = Math.max(...days.map(d => d.points), 10);
  $('p-bars').innerHTML = days.map(d => {
    const pct = Math.round((d.points / max) * 100);
    const c = band(d.points).color;
    return `
      <div class="pbar ${d.date === today ? 'is-today' : ''}">
        <div class="pcol">
          <div class="pval">${d.points}</div>
          <div class="fill" style="height:${pct}%;background:${c}"></div>
        </div>
        <div class="pday">${weekday(d.date)}<b>${Number(d.date.slice(8, 10))}</b></div>
      </div>`;
  }).join('');

  // history log (all dates desc)
  const hist = Object.keys(map).sort((a, b) => (a < b ? 1 : -1));
  if (!hist.length) { $('p-history').innerHTML = `<tr><td colspan="4"><div class="empty">No completed tasks yet — finish a task to start scoring.</div></td></tr>`; return; }
  $('p-history').innerHTML = hist.map(d => `
    <tr>
      <td style="white-space:nowrap">${weekday(d)} ${prettyDate(d)}${d === today ? ' <span style="color:#58a6ff">· today</span>' : ''}</td>
      <td class="text-right">${map[d].count}</td>
      <td class="text-right" style="font-weight:700;color:#fff">${map[d].points}</td>
      <td>${bandPill(map[d].points)}</td>
    </tr>`).join('');
}

/* =========================================================================
   Sync indicator + toast + gate
   ========================================================================= */
function setSaveState(kind, text) {
  const el = $('save-dot'); if (!el) return;
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
function openGate() { $('gate').classList.add('show'); $('gate-token').focus(); }
function closeGate() { $('gate').classList.remove('show'); }

/* =========================================================================
   Wiring
   ========================================================================= */
function toggleForm(formId, focusId) {
  const c = $(formId); c.classList.toggle('open');
  if (c.classList.contains('open') && focusId) $(focusId).focus();
}
function submitNewTask() {
  const title = $('f-title').value.trim();
  if (!title) { toast('Give the task a title', true); $('f-title').focus(); return; }
  if (!getToken()) { openGate(); toast('Connect GitHub first to save', true); return; }
  mutate(() => state.tasks.unshift({
    id: uid(), title, area: $('f-area').value, priority: $('f-priority').value,
    status: 'active', difficulty: $('f-difficulty').value, due: $('f-due').value || null,
    created: todayStr(), notes: $('f-notes').value.trim() || null, completed: null, snoozedUntil: null
  }));
  $('f-title').value = ''; $('f-due').value = ''; $('f-notes').value = '';
  $('f-priority').value = 'medium'; $('f-difficulty').value = 'medium';
  $('form-card').classList.remove('open');
}

function wire() {
  $('f-area').innerHTML = AREAS.map(a => `<option value="${esc(a)}">${esc(a)}</option>`).join('');

  // tasks
  $('btn-new').addEventListener('click', () => toggleForm('form-card', 'f-title'));
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

  // units
  $('u-new').addEventListener('click', () => toggleForm('u-form', 'u-number'));
  $('u-cancel').addEventListener('click', () => $('u-form').classList.remove('open'));
  $('u-add').addEventListener('click', submitUnit);
  $('u-number').addEventListener('keydown', e => { if (e.key === 'Enter') submitUnit(); });

  // content ideas
  $('c-new').addEventListener('click', () => toggleForm('c-form', 'c-title'));
  $('c-cancel').addEventListener('click', () => $('c-form').classList.remove('open'));
  $('c-add').addEventListener('click', submitContent);
  $('c-title').addEventListener('keydown', e => { if (e.key === 'Enter') submitContent(); });

  // build log
  $('b-new').addEventListener('click', () => toggleForm('b-form', 'b-title'));
  $('b-cancel').addEventListener('click', () => $('b-form').classList.remove('open'));
  $('b-add').addEventListener('click', submitBuild);
  $('b-title').addEventListener('keydown', e => { if (e.key === 'Enter') submitBuild(); });

  // gate
  $('gate-save').addEventListener('click', () => {
    const t = $('gate-token').value.trim();
    if (!t) { toast('Paste a token first', true); return; }
    setToken(t); $('gate-token').value = ''; closeGate(); toast('Connected to GitHub'); loadTasks();
  });
  $('gate-token').addEventListener('keydown', e => { if (e.key === 'Enter') $('gate-save').click(); });
}

/* ---- Boot --------------------------------------------------------------- */
function init() {
  $('header-date').textContent = new Date().toLocaleDateString('en-GB', { weekday: 'long', day: 'numeric', month: 'long', year: 'numeric' });
  wire();
  render();
  loadTasks();
}
if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
else init();
