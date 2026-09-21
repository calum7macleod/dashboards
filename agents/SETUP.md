# SETUP - the new account, start to finish (about 45 minutes)

Do it in this order. Each step has a check. Nothing on the old account gets touched until step 9 passes.

## 1. Settings (5 min)
- Settings > Profile: name Calum, work "real estate broker", Instructions for Claude = the voice block (already pasted).
- Settings > Capabilities: Memory ON. Confirm Cowork and Scheduled show in the sidebar.
- Check: sidebar shows Projects, Scheduled, Customize.

## 2. Connectors (10 min) - Customize > Connectors
Connect: Google Calendar, Google Drive (the Google account that holds today's calendar - moving it is E4 next week), Plaud (approve reading recordings), PropertyIndex, Canva, GitHub Integration.
Check: each shows a tick. Open one new chat and ask "what's on my calendar tomorrow" - answer comes back.

## 3. Projects (20 min) - Projects > New project, nine times
Name · paste file into instructions · description (one line below) · save. Order: PA first (you use it most), then Uploader, Finance, Mentor, Content, Market, Designer, Life Coach, Claude Manager.
| Project | Paste | Description |
|---|---|---|
| PA (Max) | PROJECT-pa.txt | Everyday chat. Runs the book, the board and the day. |
| Uploader | PROJECT-uploader.txt | Drop screenshots and statements here. Extracts and files. |
| Finance | PROJECT-finance.txt | Money. Bookkeeping, cash plan, coaching. |
| Mentor | PROJECT-mentor.txt | Deals and plans. Advice, not admin. |
| Content | PROJECT-content.txt | What we film, why, and what it brought in. |
| Market | PROJECT-market.txt | Off-plan research, news, receipts, story ideas. |
| Designer | PROJECT-designer.txt | Decks, PDFs, carousels. One brand. |
| Life Coach | PROJECT-life-coach.txt | Personal. Sleep, training, focus, the standard. |
| Claude Manager | PROJECT-claude-manager.txt | The system itself. Agents, dashboards, builds. |
Knowledge: PA and Market get the Lagoons owner data file (private) when you upload it; nothing else needed - the repo is the knowledge.
If a paste is rejected as too long: move the private block (the last section) into that project's Knowledge as a file and paste the rest.
Check: in each project, send the first message "Read your start pack and tell me in three lines where we are." A correct three lines = the paste worked and the token works.

## 4. First message to each project (5 min, part of step 3)
That first message is also the initialisation. Expect: the clock verified, the state file summarised, "no open handoffs" or the list. If an agent asks where the repo is, the paste is missing the shared section.

## 5. Scheduled tasks (5 min) - Cowork > Scheduled > New task > Create with Claude
Five tasks from agents/schedules.md: Inbox sweep 06:30 + 18:30 daily, Market daily scan 06:45, Market weekly pulse Sunday 06:45, Content scoreboard Friday 17:00, Sunday meeting prep 07:00. Paste each prompt as written. Run the Inbox one by hand once.
Check: data/triage/ has a file dated today.

## 6. Claude Code (5 min)
Sign in on the new account (desktop app > Code, or terminal). Clone calum7macleod/dashboards. The Claude Manager writes CLAUDE.md and hooks on its first build spec - nothing to do yet.
Check: `claude` opens in the repo folder.

## 7. Apps
Phone: sign out old, sign in new. Desktop app: move to the new account after step 9.

## 8. Old account
Leave it. Cancel 24h before its next billing date (task B3h). Export is done.

## 9. Dry run (Tuesday morning)
In the PA: "morning brief". Then "add this buyer" with a contact card. Then "log Deliveroo 40 ADIB" in Finance. Check the live site shows the buyer and the dashboard the spend. Pass = the switch is done.

## Daily shape once live
07:30 PA brief (Inbox file already waiting) · few minutes Mentor · few minutes Life Coach · work · Uploader for anything bulk · 19:30 PA scoreboard. Friday: analytics screenshots to the Uploader. Sunday: the meeting, chaired by the PA.
