# Scheduled tasks (Cowork > Scheduled). Create each with these prompts. Each runs as its own session with connectors.

## INBOX SWEEP - 06:30 and 18:30 Dubai, daily (runs as the PA)
Read agents/_shared.md and agents/pa.md from calum7macleod/dashboards. Then: Google Calendar for the next 24h; Plaud recordings since the last sweep (transcripts); Meta lead forms if a source is connected; data/buyers.json next-touch dates due today or overdue; data/tasks.json due today. Write ONE file: data/triage/YYYY-MM-DD-{am|pm}.json with {newLeads, repliesOwed, viewingsToDebrief, touchesDue, expiring, notes}. Do NOT write any other file. Append your receipt to data/log.jsonl. Output a five-line summary.

## MARKET DAILY SCAN - 06:45 Dubai, daily (runs as Market)
Read agents/_shared.md and agents/market.md. Scan UAE property news and developer releases for the last 24h (off-plan launches, Abu Dhabi and Dubai, policy, rates, macro). Write ten lines max into the "Daily" section of data/state/market.md (replace yesterday's). If anything is a content story, append a handoff to data/handoffs.json for Content with the claim, receipt and angle. Append receipt to data/log.jsonl. Output the ten lines.

## MARKET WEEKLY PULSE - Sunday 06:45 Dubai (runs as Market)
Read agents/_shared.md and agents/market.md. Launches this week and next; psf table for the projects Calum sells (from data/dld and PropertyIndex where Dubai; developer releases where Abu Dhabi); what changed; open questions closed or killed. Write data/market/pulse-YYYY-MM-DD.md and the summary into data/state/market.md. Append receipt. Output the summary.

## CONTENT SCOREBOARD - Friday 17:00 Dubai (runs as Content)
Read agents/_shared.md and agents/content.md. Read data/content-metrics.json (the Uploader appended this week's analytics) and data/buyers.json for source = socials. Write the scoreboard into data/state/content.md and metrics into data/content.json: winner, loser, why, deals-from-socials line. Append receipt. Output winner, loser, why.

## SUNDAY MEETING PREP - Sunday 07:00 Dubai (runs as the PA)
Read agents/_shared.md, agents/pa.md, agents/weekly-meeting.md and data/log.jsonl for the last 7 days. Write data/state/meeting-YYYY-MM-DD.md in the weekly-meeting format with each agent's section drafted from the log and state files. Append receipt. Output the agenda.
