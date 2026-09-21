# Scheduled tasks (Cowork > Scheduled). Create each with these prompts. Each runs as its own session with connectors.

## INBOX SWEEP - 06:30 and 18:30 Dubai, daily (runs as the PA)
Read agents/_shared.md and agents/pa.md from calum7macleod/dashboards. Then: Google Calendar for the next 24h; Plaud recordings since the last sweep (transcripts); Windsor.ai Meta ads for new leads if available; data/buyers.json next-touch dates due today or overdue; data/tasks.json due today. Write ONE file: data/triage/YYYY-MM-DD-{am|pm}.json with {newLeads, repliesOwed, viewingsToDebrief, touchesDue, expiring, notes}. Do NOT write any other file. Append your receipt to data/log.jsonl. Output a five-line summary.

## LAGOONS REPORT - Monday and Thursday 06:45 Dubai (runs as Market)
Read agents/_shared.md and agents/market.md. Pull data/dld/lagoons.json and PropertyIndex for the last 7 days (Lagoons clusters). Write the report section into data/state/market.md (replace the previous one). Append receipt to data/log.jsonl. Output the headline lines.

## CONTENT SCOREBOARD - Friday 17:00 Dubai (runs as Content)
Read agents/_shared.md and agents/content.md. Pull Windsor.ai Instagram + TikTok + YouTube for the last 7 days per post. Write the scoreboard into data/state/content.md and metrics into data/content.json. Append receipt. Output winner, loser, why.

## SUNDAY MEETING PREP - Sunday 06:30 Dubai (runs as the PA)
Read agents/_shared.md, agents/pa.md, agents/weekly-meeting.md and data/log.jsonl for the last 7 days. Write data/state/meeting-YYYY-MM-DD.md in the weekly-meeting format with each agent's section drafted from the log and state files. Append receipt. Output the agenda.
