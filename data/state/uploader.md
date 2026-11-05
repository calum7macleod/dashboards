# UPLOADER STATE - start pack. Created 2026-11-05 by Claude Manager (h0038/h0098). You own this file: update it at the end of every session.

## How to use this file
One screen. What you appended last, what sits in staging waiting for an owner, what you keep having to ask. Trim anything older than a month.

## Last sessions (newest first, one line each)
- 2026-11-05: file created by Manager - fill in from your next session.

## Staging - files waiting for their owner to ingest (data/staging/)
- 2026-09-23-jake-nazer-reels-hooks.json - owner Content
- 2026-09-26-bos-csv-jan-aug.json - owner Finance
- 2026-09-26-wise-csv.json - owner Finance
- adrec-transactions-2019-2026.csv.gz + README - owner Finance
- statements/ - owner Finance
Rule (5 Nov): staging files are transient. The agent that ingests one deletes it - you never delete. If a file has sat here over two weeks, handoff to its owner.

## Account names you will see on statements (names only - never numbers)
See agents/uploader.md. Missing from that list on 1 Nov: Nationwide FlexDirect (personal), the UK cards - Calum to confirm names (h0103).

## Standing reminders
- Append only. Duplicates checked before they land. Unreadable digit = flagged, never invented.
- Every append ends with a handoff to the file's owner and a receipt.
- Something broken or missing: `agentkit.py issue <type> "<what>"` the moment it happens.
