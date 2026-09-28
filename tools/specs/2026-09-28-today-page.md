# SPEC - Today page (task dashboard v2)
Written 28 Sep 2026 by Claude Manager from Calum's answers this morning. For Claude Code (cloud session). Queue item 2, part 1.
Rules: node --check before every commit; one edit at a time, verify each; NEVER hardcode data in pages - everything reads data/*.json at runtime; bump ?v=N on JS changes; re-pull after any failed run.

## 0. What Calum said (the brief)
- Uses it at the desk and on the phone all day - "almost want it always there".
- Everything goes in, categorised: work, buyer follow-ups, content, personal and routine.
- It dies because: one day not touched and it's gone (overdue wall); setting priorities and dates is hard; too much on screen.
- Wants: headline only, tap to open the rest. Today in focus; This week and Month collapsed, zoom out on demand.
- Tasks arrive both ways: voice note to the PA (files them) and typed straight into the page.
- Ticking "Call Janani" logs the call on the buyer record too.
- No cap on Today - he orders it himself.

## 1. Facts (verified 28 Sep)
- data/tasks.json: {tasks[], units[], contentIdeas[], buildLog[]}. 282 tasks: 42 active, 240 done in the same file. Fields: order, top3, id, title, area, priority, status, difficulty, due, created, notes, completed, snoozedUntil. priority is 173/282 "high" - meaningless. area: Real Estate, Content, Tasks, Finance, Health, Investing.
- tasks.html + js/tasks.js (801 lines) already write tasks.json via the Contents API with a token in localStorage key 'dashboards_gh_token'; crm.html uses key 'crm_pat'. Sortable drag exists (initSortables), undo exists (undoLast), snooze exists.
- data/buyers.json live buyers carry: buyer, phone, score, stage, lastContact, nextTouch (YYYY-MM-DD), touchReason, touches[], nextStep. crm.html writes buyers.json the same way (sha-based PUT).
- PA's Saturday board (A1, B3g...) lives in chat/state, not in tasks.json. Content agent and PA both write tasks.json.

## 2. Decisions
- NEW page today.html + js/today.js. tasks.html stays as the full view (units, ideas, build log, productivity) and gets one link to Today. Hub links Today first.
- Bands replace dates as the organising idea. Four bands: today | week | month | someday (labels: Today, This week, This month, Someday). New task fields: band, bandSince (YYYY-MM-DD, set whenever band changes). due stays and means a real deadline only. Today open; the other three collapsed with counts; Someday is the parking lot and sits last.
- Nothing renders as overdue. A Today item not done today stays in Today; the row shows an age badge (days since bandSince) once it's 1d or more. No red.
- No priority, difficulty, points or top3 anywhere on the page. Fields stay in the file for agents; the page ignores them. Order is the priority: drag within Today, persisted to order.
- Categories = area, one list, colour dot per area. Add 'Personal' to the area list. Filter chips (All + each area) under the add box; filter is remembered in localStorage.
- Buyer follow-ups are merged into Today at render time, not copied into tasks.json: every live buyer (stage not Won/Lost) with nextTouch <= today becomes a row "Call {buyer} - {touchReason}" in a Buyers category, sorted score desc then oldest nextTouch. Expanded: phone as a tel: link, score, stage, nextStep, a date pill for nextTouch.
- Tick on a buyer row writes buyers.json: lastContact = today; touches gets an entry in the existing touch shape (read one record with touches to match it; type 'call', note ''); nextTouch = today + 3 days (ASSUMPTION - editable in the expanded row; the PA reconciles at checkpoint). Row disappears.
- Tick on a task: status 'done', completed = today, row fades, 5-second undo toast. Done today is a collapsed band at the bottom ("Done today (4)").
- MOVE, any direction, same gesture in every band: swipe a row on phone (hover on desk) reveals chips for the other three bands + Kill. One tap moves it (band + bandSince = today, order last in the new band) and the row slides to its new band. Desk also supports drag between bands (Sortable groups). Moving is the core interaction - it must be one gesture and one tap, never a menu inside a menu. Kill = status 'killed', never deleted; the archive job clears it.
- Roll (client-side on every load and refresh): any band with due <= today -> today; month with due within this ISO week -> week; someday with snoozedUntil <= today -> today; bandSince = today on any roll. Undone today items are never touched.
- Always there: manifest.json + apple-mobile-web-app meta + icons so Add to Home Screen opens full-screen; auto-refresh every 60 s while the tab is visible (re-fetch tasks + buyers, re-render, keep expanded rows open, never lose text in the add box). No service worker.
- Token: read 'dashboards_gh_token' first, fall back to 'crm_pat', write both when the gate is used. One gate for all pages from here.
- Mobile-first: 380 px, 44 px tap targets, headline row = circle + title + area dot + age badge + due date only if set. Brand: colours and fonts from design-system/ (read it - never the AI defaults).

## 3. Migration (one-time, tools/migrate-tasks-2026-09-28.py, run once, commit the result)
- Every active task gets band + bandSince: due <= today -> today; due within this ISO week -> week; due within this month -> month; else someday; no due -> today if created within 7 days else month; snoozedUntil > today -> someday. bandSince = today. top3 true -> order 1-3 in today.
- area 'Tasks' -> 'Real Estate' unless the title is obviously personal (then 'Personal'); print the mapping for review.
- 240 done tasks -> data/archive/tasks-done-2026.json (same shape), removed from tasks.json. Print counts before/after. units, contentIdeas, buildLog untouched.
- Hand the printed mapping to the PA: `python3 tools/agentkit.py handoff PA "Today page migration: <counts>, area mapping in the commit"`.

## 4. agentkit.py additions (do these AFTER tools/specs/2026-09-23-agentkit-v2.md has landed - same file)
- `task "<title>" [area] [today|week|month|someday]` - append a task with band/bandSince, order last in band. The PA's fast intake.
- `tasks-roll` - same roll rule as the page, for the 07:30 brief.
- `tasks-archive` - done or killed older than 7 days -> data/archive/tasks-done-<year>.json.
- `tasks-due` reads band: prints Today (with age), then Week.

## 5. Acceptance tests
1. Phone (380 px): opens on Today only; This week, This month and Someday show as collapsed bands with counts; every row is one line.
2. Type "test task" + Enter: appears at the top of Today; tasks.json gains it with band today, bandSince today, area = the selected chip.
3. Tick it: row fades, undo toast 5 s, tasks.json status done + completed today; "Done today (1)" band shows it.
4. Swipe/hover on a Today row -> This week: band week, row moves. Open This week, swipe that row -> Today: it is back, one gesture + one tap each way. Same from This month and Someday. Desk: drag a row from This week into Today, band updates in the file. Then set a week task's due to yesterday in the file, reload: it rolls into Today with bandSince today.
5. A task moved to Today two days ago shows "2d"; nothing on the page is red.
6. A live buyer with nextTouch <= today appears as "Call ..." in Today; tick: buyers.json lastContact today, touches +1 in the existing shape, nextTouch = today+3; row gone. crm.html still loads and shows the same buyer.
7. Leave the tab open; append a task via agentkit; within 60 s it appears with no reload and the add box keeps its text.
8. Add to Home Screen on iPhone: opens full-screen, no browser chrome.
9. No priority, difficulty, points or top3 visible anywhere on today.html.
10. tasks.html still loads and works; the only change is the Today link. node --check passes on js/today.js; ?v bumped.
11. After migration: tasks.json has 42 tasks (all with band), archive file has 240, counts printed in the commit message.

## 6. Out of scope (next specs)
- The call system page for Jake's start (h0016) - builds on the buyer merge here.
- Login (queue item 3). The token still lives in localStorage on a public site.
- Notifications - a static page can't ping; needs a service.
