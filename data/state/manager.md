# MANAGER STATE - start pack. Updated 2026-09-21 14:55 by Claude Manager.

## Gate
NOTHING BUILDS until the dry run passes (Tue 22 Sep). Specs only until then. Calum, 21 Sep.

## Build queue (in order) - reordered 21 Sep, Calum approved: old 7 > 1 > 2 > rest
1. Normalise buyer status values (Won vs Closed Won vs Active) and give tools/agentkit.py buyers-index a clean 'live' rule (Uploader finding, 21 Sep). Goes first because the Today tab reads status. SPEC DUE for Claude Code: Wed 23 Sep.
   - 1b (proposed, same file, same session): agentkit `owner <unit|name|cluster>` command - raw media type for files over 1MB, returns matching rows only (handoff h0002 from PA). Awaiting Calum's yes to bundle.
2. Dashboard architecture v2 - task tracking first (Mission Control), then Today tab rebuilt around: who do I call, what's about to lapse, where's the money this month. (Task F1, Mon 28.)
3. Login for the dashboards - repo private (GitHub Pro) + Cloudflare Access in front of the domain, or move off public hosting. Finance data stays in the main repo on the strength of this.
4. Proper matching - off-plan tags captured at intake (budget, timeline, finance, purpose, base, what they'd move for), launch-to-shortlist in seconds. Own workstream.
5. Lost/Archived view built for revival.
6. Plaud direct to profile: recording > transcript > proposed update > one-tap confirm.
7. Meta lead forms into the Inbox sweep (source TBC: email connector or webhook).
8. Archive the old data/context.md and journal history into the private repo; core.md is the state now.

## Open handoffs to Manager
- h0002 (PA, 21 Sep): 1) agentkit owner command - see 1b. 2) one line for _shared.md Source of truth pointing at private:data/owners/README.md - line proposed to Calum 21 Sep, lands after the command ships, Calum approves the rule change.

## System health
21 Sep 14:55: receipts in log from Max, PA, mentor, content. None yet from uploader, designer, market (handoff written, no receipt), finance, lifecoach. Scheduled tasks not yet created.
Finding: raw.githubusercontent.com caches ~5 min - handoffs.json read as [] via raw while h0001/h0002 were live. Agents read state through agentkit (API), never raw. Add to _shared.md at next rule edit.

## Schemas
See agents/_shared.md ownership table. Buyer, seller, deal, task, viewing, offer record shapes are in the Lewis brief (content-assets/lewis/crm-build-brief.md) section 3.
