# MANAGER STATE - start pack. Updated 2026-09-21 by Max.

## Build queue (in order)
1. Dashboard architecture v2 - task tracking first (Mission Control), then Today tab rebuilt around: who do I call, what's about to lapse, where's the money this month. (Task F1, Mon 28.)
2. Login for the dashboards - repo private (GitHub Pro) + Cloudflare Access in front of the domain, or move off public hosting. Finance data stays in the main repo on the strength of this.
3. Proper matching - off-plan tags captured at intake (budget, timeline, finance, purpose, base, what they'd move for), launch-to-shortlist in seconds. Own workstream.
4. Lost/Archived view built for revival.
5. Plaud direct to profile: recording > transcript > proposed update > one-tap confirm.
6. Meta lead forms into the Inbox sweep (source TBC: email connector or webhook).
7. Normalise buyer status values (Won vs Closed Won vs Active) and give tools/agentkit.py buyers-index a clean 'live' rule (Uploader finding, 21 Sep).
8. Archive the old data/context.md and journal history into the private repo; core.md is the state now.

## System health
21 Sep: nine agent files written; start packs seeded; log and handoffs seeded. Scheduled tasks not yet created. No receipts yet from any agent other than Max.

## Schemas
See agents/_shared.md ownership table. Buyer, seller, deal, task, viewing, offer record shapes are in the Lewis brief (content-assets/lewis/crm-build-brief.md) section 3.
