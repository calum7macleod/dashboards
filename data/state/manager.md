# MANAGER STATE - start pack. Updated 2026-09-23 09:05 by Claude Manager.

## Gate
NOTHING BUILDS until Calum says the dry run (Tue 22 Sep) passed. PA's dry-run write landed 22 Sep; no pass/fail from Calum yet. Specs, rule edits and handoffs are not builds.

## Build queue (in order) - Calum approved 21 Sep
1. agentkit v2 - SPEC WRITTEN 23 Sep: tools/specs/2026-09-23-agentkit-v2.md. Covers: buyer status rule (stage is truth, status derived), buyers-check, owner lookup (h0002), issue/issues/fix, safe concurrent appends, crm.html line 665, Claude Code hook + CLAUDE.md. Gate lifted 23 Sep (Calum asked to proceed). BUILD ROUTE: Claude Code CLOUD session (claude.ai/code or desktop app > Cloud) on calum7macleod/dashboards - Calum's Windows box has no repo, no Git, no Python (Claude Code local reported 23 Sep). GH_TOKEN goes in as a cloud environment variable, never in chat. Watch for: api.github.com blocked by environment network settings. Prompt given to Calum 23 Sep ~10:30. Then: PA migration (h0007), close h0002, re-paste shared rules to ten Projects.
2. Dashboard v2 - Today page SHIPPED 28 Sep by Manager (Claude Code unavailable): today.html, js/today.js?v=1, manifest.json, icons/, tools/migrate-tasks-2026-09-28.py. Spec tools/specs/2026-09-28-today-page.md sections 1-3 done; section 4 (agentkit task/tasks-roll/tasks-archive) waits for agentkit v2. Tested in jsdom against real data (add, tick, undo, move both ways, buyer tick writes buyers.json, roll, 60s refresh keeps add-box text). NOT tested: real phone swipe, drag, Add to Home Screen - Calum tests, Manager fixes. Migration: 279 -> 35 live (25 today, 10 week), 244 archived. Then Mission Control / money view: who do I call, what's about to lapse, where's the money this month. (Task F1, Mon 28.) INPUTS collected: h0003 (tasks: difficulty text so points never compute - map easy/medium/hard to 1/3/5/8; archive 226 done tasks to data/archive/; overdue count + oldest; mixed id styles; buildLog/units empty; Top 3 not capped), h0004 (Lost sorted by closedLost desc, undated at bottom), h0005 (notes as ' | ' string, date-first entries - render split, gold eyebrow date, 3 then more; decision needed: keep string or migrate to notes[]).
3. Login - private repo (GitHub Pro) + Cloudflare Access, or move off public hosting. Finance data stays in main repo on the strength of this.
4. Matching tags at intake (budget, timeline, finance, purpose, base, what they'd move for). Own workstream.
5. Lost/Archived view for revival - uses lostReason from the h0007 migration.
6. Plaud direct to profile: recording > transcript > proposed update > one-tap confirm.
7. Meta lead forms into the Inbox sweep (source TBC: email connector or webhook).
8. Archive old data/context.md and journal history to the private repo; core.md is the state.

## Open handoffs to Manager
- h0002 (PA): owner command - in spec item 1. Close when it ships.
- h0003, h0004, h0005 (PA): dashboard inputs - folded into item 2 above. Close when item 2 is specced.
- h0006 (PA): Inbox sweep wrote no triage file 22-23 Sep. REVISED 23 Sep 09:20: Calum's sidebar shows PA · Inbox AM and PA · Inbox PM chats exist (PM unread) - the sweep appears to run but writes nothing. Likely no token/bash in that chat, or it reports a failure nobody reads. Waiting on Calum to paste the last Inbox PM reply. Also Market · Daily scan exists - same check. No Project exists yet for the tenth agent (Projects).

## Issues protocol (live from 23 Sep)
Agents log faults with `agentkit.py issue <type> "<what>"` the moment they happen (rule in _shared.md; handoff Manager until the command exists). Manager opens every conversation with the open list + a fix per line. Sunday: patterns by type.

## Scheduled runs - DELETED 5 Oct (h0006 closed by removal)
Root cause: unattended sandbox refuses token-bearing GitHub calls; Gmail relay rejected (Calum loses that Gmail soon). Calum deleted the PA scheduled tasks 5 Oct; kept Market daily scan as a read-only morning news chat (token-free prompt, no writes, output visible only to Calum in that chat). PA now sweeps inline at 07:30/19:30 (agents/pa.md). Market scans when it runs. Reinstate only via: a per-task permission setting (unverified), a Claude Doc relay, or an external cron calling the API (queue it after Login). Also: the Google Calendar connector is on the account Calum is losing - reconnect on the new one or the brief goes blind.

## System health
28 Sep 07:50: agentkit v2 (23 Sep spec) NOT shipped - no receipt, no issue command; the cloud session either never ran or failed silently. Asked Calum. 11 handoffs open to Manager: h0002-h0006 (known), h0015 content (Projects agent not in roster - now it is, close), h0016 PA (call system page - next spec after Today), h0020 uploader (finance.json sign inconsistency - Finance's file, route to Finance), h0022 Finance (dashboard rules: exclude 'retired', currency field - dashboard change, queue), h0029 Finance (concurrent write lost 44 finance rows - spec v2 2a addresses; also add rule: fetch sha immediately before PUT), h0038 uploader (no data/state/uploader.md - create it). Issues-via-handoff fallback is working: 4 of the 11 are logged issues.

23 Sep 09:05: receipts from Max, PA, mentor, content, Designer. None from uploader, market, finance, lifecoach, projects, inbox. Ten agents now (Projects added by Max 23 Sep - _shared.md already has its row). Scheduled tasks: none confirmed running (h0006).
Finding (access): Claude Code on Calum's Windows machine has no Git, no Python, no repo checkout - local builds impossible; all building goes through cloud sessions until that changes. Hooks (.claude/settings.json) still apply in cloud sessions once committed.
Findings: raw.githubusercontent.com cache serves stale files - rule added to _shared.md 23 Sep. Two closed-date fields (closedDate from crm.html, closedLost from PA) - fixed in spec 1. buyers-index over-counts live by 20 - fixed in spec 1.

## Agent file changes awaiting re-paste
- agents/pa.md 28 Sep: SCORES FIRST at 07:30 (Calum's ask), tasks rule now bands not dates/priority (matches today.html). Calum re-pastes the PA file into the PA Project. Until then the PA runs on the old text.

## Shared rules - Project instructions status
23 Sep ~10:00: Issues section + agentkit-not-raw/owner pointer pasted into all ten Projects by Calum (as one block at the end of the shared rules). All agents on the Issues rule from now. Fallback (handoff Manager) active until agentkit v2 ships the `issue` command. Next full re-paste only if _shared.md changes again.

## Schemas
See agents/_shared.md ownership table. Buyer canonical rule: tools/specs/2026-09-23-agentkit-v2.md section 1. Other record shapes: Lewis brief (content-assets/lewis/crm-build-brief.md) section 3.
