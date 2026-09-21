# agents/ - the instruction files for Calum's Claude system

One file per agent. A Claude Project's instructions = `_shared.md` + `<agent>.md` + the PRIVATE block (from the private repo, pasted by hand) + the GitHub token (typed by hand). Nothing secret lives in this folder. This folder is public.

## Paste order for a new account
1. Customize > Connectors: connect Google Calendar, Google Drive, Plaud, PropertyIndex, Windsor.ai, Canva, GitHub Integration.
2. Projects > New project, eight times, named: Claude Manager, PA, Content, Designer, Mentor, Market, Finance, Life Coach.
3. In each project's instructions paste, in this order: `_shared.md`, then the agent's file, then the private block, then the token line: `GITHUB TOKEN: <token>`.
4. Upload knowledge files the agent's file names under "Knowledge".
5. Scheduled tasks: `schedules.md` has the prompts. Create them in Cowork > Scheduled.
6. Weekly meeting: `weekly-meeting.md`.

## The token rule
The fine-grained GitHub token (dashboards + crm-inbox only, Contents read/write) is typed into Project instructions by hand. It is never committed to any repo, never pasted in a chat, never on a screen. If it ever appears anywhere, rotate it.

## State files (start packs)
Each agent reads ONE small state file at session start. They live in `data/state/` (business) and `personal/state/` in the private repo (personal + money). Under two pages each. History is archived, not carried.

## Changing an agent
Edit the file here first, then re-paste into the project. The file is the truth; the project is a copy.
