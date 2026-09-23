# MANAGER STATE - start pack. Updated 2026-09-23 09:05 by Claude Manager.

## Gate
NOTHING BUILDS until Calum says the dry run (Tue 22 Sep) passed. PA's dry-run write landed 22 Sep; no pass/fail from Calum yet. Specs, rule edits and handoffs are not builds.

## Build queue (in order) - Calum approved 21 Sep
1. agentkit v2 - SPEC WRITTEN 23 Sep: tools/specs/2026-09-23-agentkit-v2.md. Covers: buyer status rule (stage is truth, status derived), buyers-check, owner lookup (h0002), issue/issues/fix, safe concurrent appends, crm.html line 665, Claude Code hook + CLAUDE.md. Waiting on: Calum pastes it into Claude Code. Then: PA migration (h0007), close h0002, re-paste shared rules to ten Projects.
2. Dashboard architecture v2 - task tracking first (Mission Control), then Today tab: who do I call, what's about to lapse, where's the money this month. (Task F1, Mon 28.) INPUTS collected: h0003 (tasks: difficulty text so points never compute - map easy/medium/hard to 1/3/5/8; archive 226 done tasks to data/archive/; overdue count + oldest; mixed id styles; buildLog/units empty; Top 3 not capped), h0004 (Lost sorted by closedLost desc, undated at bottom), h0005 (notes as ' | ' string, date-first entries - render split, gold eyebrow date, 3 then more; decision needed: keep string or migrate to notes[]).
3. Login - private repo (GitHub Pro) + Cloudflare Access, or move off public hosting. Finance data stays in main repo on the strength of this.
4. Matching tags at intake (budget, timeline, finance, purpose, base, what they'd move for). Own workstream.
5. Lost/Archived view for revival - uses lostReason from the h0007 migration.
6. Plaud direct to profile: recording > transcript > proposed update > one-tap confirm.
7. Meta lead forms into the Inbox sweep (source TBC: email connector or webhook).
8. Archive old data/context.md and journal history to the private repo; core.md is the state.

## Open handoffs to Manager
- h0002 (PA): owner command - in spec item 1. Close when it ships.
- h0003, h0004, h0005 (PA): dashboard inputs - folded into item 2 above. Close when item 2 is specced.
- h0006 (PA): Inbox sweep wrote no triage file 22-23 Sep. Diagnosis: no Inbox receipt in the log, ever - the scheduled task never ran (not "ran and couldn't write"). Fix is Calum's: create the scheduled task; add "log a receipt every run, even when empty". Close on first receipt.

## Issues protocol (live from 23 Sep)
Agents log faults with `agentkit.py issue <type> "<what>"` the moment they happen (rule in _shared.md; handoff Manager until the command exists). Manager opens every conversation with the open list + a fix per line. Sunday: patterns by type.

## System health
23 Sep 09:05: receipts from Max, PA, mentor, content, Designer. None from uploader, market, finance, lifecoach, projects, inbox. Ten agents now (Projects added by Max 23 Sep - _shared.md already has its row). Scheduled tasks: none confirmed running (h0006).
Findings: raw.githubusercontent.com cache serves stale files - rule added to _shared.md 23 Sep. Two closed-date fields (closedDate from crm.html, closedLost from PA) - fixed in spec 1. buyers-index over-counts live by 20 - fixed in spec 1.

## Pending re-paste (Calum, once, after agentkit v2 ships)
agents/_shared.md changed 23 Sep: Issues section, agentkit-not-raw, owner-data pointer. Re-paste into all ten Projects. Don't re-paste before v2 ships - the rule points at a command that doesn't exist yet (fallback line covers it, but one paste is better than two).

## Schemas
See agents/_shared.md ownership table. Buyer canonical rule: tools/specs/2026-09-23-agentkit-v2.md section 1. Other record shapes: Lewis brief (content-assets/lewis/crm-build-brief.md) section 3.
