# MANAGER STATE - start pack. Updated 2026-11-05 16:40 by Claude Manager.

## Gate
None. Claude Code is not usable (no local toolchain; cloud route never delivered). Manager builds directly, tests in jsdom/node, Calum tests on device.

## Build queue (in order)
1. Login - private repo (GitHub Pro) + Cloudflare Access, or move off public hosting. The token lives in localStorage on a public site and finance data is public. NEXT.
2. Call system page (h0016) - calls.html exists (unknown author, 5 Nov) - Calum to confirm whether it is the call system; if so close h0016, else build from the Today page's Calls block.
3. Matching tags at intake (budget, timeline, finance, purpose, base, what they'd move for). Own workstream.
4. Lost/Archived revival view - needs the PA migration (h0119) first.
5. Plaud direct to profile. 6. Meta lead forms into intake. 7. Whoop connector (Calum interested 11 Oct; register a Whoop developer app first). 8. Archive old context.md/journal to private repo.
9. Scheduled sweeps - all deleted 5 Oct except Market daily (read-only chat). Reinstate only via an external cron calling the API. Calendar connector is on the Google account Calum is losing.

## Shipped by Manager
- 28 Sep Today page (today.html, js/today.js v4): bands, no overdue, importance 1-5, Delete, Ctrl+Z, buyer calls merged; migration of tasks.json.
- 28 Sep CRM notes render (dated entries, 3 then more).
- 5 Nov Content production board (board.html, js/board.js v4): columns from stages, drag order (boardOrder), bin, undo; agentkit board/stage/card add/card edit.
- 5 Nov agentkit v2 (tools/agentkit.py): conflict-safe writes (modify = read/apply/write with retry), sha-guarded get/put (put refuses stale writes), large files, buyers-index stage rule, buyers-check, owner, issue/issues/fix, task/tasks-roll/tasks-archive. Tested: 3 simultaneous receipts all land; stale put refused.
- 5 Nov CRM: Lost sorted by close date (buyers + sellers), closedWon/closedLost written everywhere, seller filter Calum/Lewis/Both/Keep, KEEP/NET/carry badges.
- 5 Nov Finance: finance.html excludes retired rows, AED-only sums with other currencies aside, signConvention flag; data/schemas/finance.md written.
- 5 Nov Uploader start pack created (data/state/uploader.md); shared rules: staging delete rule, uploader state file, issue command live, get/put conflict rule.

## Open handoffs to Manager (after 5 Nov triage)
- h0016 call system - see queue 2. h0096 PIX locked (free plan) - Calum decides pay or stop quoting psf. h0103 Uploader account names - needs card names from Calum.

## Awaiting Calum (re-pastes)
- agents/_shared.md (5 Nov) into all ten Projects: issue command live (fallback line removed), staging rule, uploader state file, get/put rule.
- agents/pa.md: scores first, tasks rule, inline sweep (Oct) + tasks-roll/task command (5 Nov).
- agents/content.md: THE BOARD ritual.

## Issues protocol
Live: `agentkit.py issue <type> "<what>"`, Manager opens every conversation with `issues` + a fix per line, closes with `fix`. data/issues.jsonl created 5 Nov (empty).

## System health (5 Nov)
Receipts 5 Oct-5 Nov: content 81, Uploader 40, Finance 32, Designer 25, Fitness 19 (NO agent file in repo - undocumented), PA 12, Projects 4, Market 0, Mentor 0, Life Coach 0. data/state/finance.md 32KB (trim - handed to Finance). Buyer data still unmigrated (h0119 to PA). PA's buyer migration from Sept (h0007) closed as superseded by h0119.

## Schemas
agents/_shared.md ownership table. Buyer rule: tools/specs/2026-09-23-agentkit-v2.md s1 (stage is truth). Tasks: bands - tools/specs/2026-09-28-today-page.md. Finance: data/schemas/finance.md. Content board: h0113/h0114 + card commands.
