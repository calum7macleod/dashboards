# MEMORY.md - Long-Term Memory

## About Me
- Name: Max
- Role: Personal assistant to Calum, 24/7

## About Calum
- Name: Calum
- Based in Dubai (GMT+4)
- First session: 2026-03-29

## Key Decisions & Context

### Finance Dashboard Updates
- **Process:** Calum sends bank screenshots whenever he wants
- **My job:** Parse and update finance/finance-dashboard.html
- **Nudge rule:** If 3+ days since last update, I ask for new screenshots
- Accounts tracked: ADIB, Wise (GBP), and others
- Dashboard URL: https://calum7macleod.github.io/dashboards/ (GitHub Pages deploy)

### Cost Optimization (2026-04-02)
- Disabled 30-minute heartbeat polling (was burning $40/day)
- Now using Haiku-4.5 (cheaper) vs Sonnet
- Estimated savings: ~$1,050/month

### Dashboard Build System (built 2026-04-05)
- `build-finance.js` → transactions.json + cc-balances.json → finance.html
- `build-realestate.js` → realestate/data.json → realestate.html
- Run scripts from `/home/user/.openclaw/workspace/`
- Deploy: `cd /tmp/dashboards-deploy && git add . && git commit && git push`
- Both dashboards live: https://calum7macleod.github.io/dashboards/
- Finance: Transactions (Jan-Apr, 400 txs), CC Balances (10 cards: 9 UK + ADIB), Categories, Summary, Trends
- Real Estate: Deals (17, newest first), Buyers (13 active, ranked by priority), Stock (15 active), Analysis, Archive
- **Model:** Haiku for maintenance (cheap). Switch to Sonnet only for new features.

### Sales Manager Role (Starting 7 Apr)
- Daily morning brief: 7:30 AM Dubai time
  - Board progress (2026 vs AED 3M target)
  - Top 3 deals (hot prospects)
  - One action item to focus on
- Weekly review: Monday 8:00 AM
  - Full pipeline (buyers/sellers/deals)
  - On-track calculation
  - Weekly focus
- Track all buyer/seller updates → dashboard
- Log deals as they close
- Flag stalled deals (2+ days no contact)

### Trading & MT4 Access
- Calum does day trading on MT4 (forex/stocks)
- Machine is WSL2 (Linux container on Windows)
- Desktop control tools were removed to save tokens with Haiku
- **TODO (Sunday):** Figure out lightweight way for me to monitor MT4 without token burn
  - Options: log file parsing, API exports, periodic screenshots only, etc.

### Bank Account Notes
**UK Bank (Classic Account):**
- Chronically overdrawn (-£2,271 as of Apr 2)
- Should clear soon
- Pet insurance (AGRIA) bounced — likely to cancel

**Dubai Accounts:**
- Mashreq: Main salary account (White & White salary ~AED 46k/month)
- ADIB: Credit card account (over 70k limit, murabaha ~2.1-2.4k/month)
- Wise: GBP account for NC500 Pods income + trading
- IPP transfers: Paying Tallia Flaher, Ganesh Muddam, and others

**Pass-Through Money (Don't Include in Cashflow):**
- Lewis John Page +AED 50k (loan from friend, not income)
- Joshua Urquhart transfers (all for Josh's property purchase, not Calum's)

**Business Expenses:**
- Contentus (Ali Vids) — content creation charges
- ADNOC — fuel/business expense


### Health Accountability (started 2026-04-20)
- Ice bath every morning — 10 mins (Mon/Wed/Fri: 05:20, Tue/Thu: 05:30). If missed → do at night.
- Boxica every morning after ice bath
- Phone away by 8PM, asleep by 9PM
- Hydration: water + electrolytes daily
- Whoop recovery: track daily
- Log file: health/health-log.json
- Check-ins: post-gym 07:15, evening wind-down 20:00
