# FINANCE STATE - start pack (private). Updated 2026-09-26 by Finance. All figures "around" until reconciled.

## Commissions owed (take-home)
- Sep payday 30 Sep: ~Đ314,100 (Michael, Ankur, Mohamed, Georgia, Zel, Mahmoud, Umer, P218) - reconcile vs payslip.
- Oct: ~Đ152,300 (Syed, Jayde, Zaid, Anshuman) + Tara A2-209 ~9,500 - all transfer after the 1 Oct exit; written confirmation they pay to Calum still OPEN.
- Stuck Jan/Feb: ~Đ65,300 (Jose, Majid x2) - chase or write off in the exit conversation.

## Burn and runway
Baseline from Oct ~Đ118,600/mo (rent accrual, Modon accrual, editors, Meta, Tal + bills, UK card minimums). 5 Sep model: runway runs out mid-January without new deals or Jake income. Oct/Nov payouts are the bridge, not upside. Jake first real pay ~Dec.

## Positions (31 Aug)
Mashreq ~Đ2K · BoS ~-£616 · ADIB card ~Đ64.6K owed of 70K limit (40% pa). UK cards on minimums (~£1,400/mo). Full balances in finance/finance.json.

## Open reconciliations
- BoS DONE 26 Sep: statement 2 Jan-25 Sep, 591 rows, balance chain clean, closing -GBP2,565.88 (31 Aug -616 ties to prior position). In finance.json with currency GBP, negative = out; 101 screenshot rows marked retired (delete pending Calum). Canonical rows: data/finance/ledger/rows/bos-2026.json.
- BoS findings: it is a conduit + debt-service account, not a spending account. YTD GBP: in 28.8K from UAE via Nium (x20), 25.2K F/FLOW CALUM MACLE 31 Jul (TFR - own Lloyds-group account? UNIDENTIFIED), 9.4K CALUM LACHLAN MACL in; out 30.6K to C L MACLEOD (x60, UNIDENTIFIED own account - the real UK spend probably lives there), 37.5K to 12 UK cards, 15.5K to Tal, 4.2K Mum, 4K Kevin, 1.6K Alex, 1.2K Corrina. Real consumption via BoS ~3-4K YTD (Apple, pet insurance, accountant). OD interest 513 YTD (~2.2/day, ~40% EAR on ~2.5-3K). 14 returned DDs Feb-Jul = card payments bouncing at the OD ceiling (~3K), then re-presented.
- Waiting: all other statements (ADIB, ADIB CC, Mashreq, Wise, Binance, 12 UK cards) + the two unidentified UK accounts above. Person legs (Tal, Corrina, Mum, Kevin, Alex, S/Ewen Macleod, Pod Factory, Page LJ, Clerwood, Richmond, Reid, James Gibson, L G Price, Flaher TV) go on ONE resolve list once everything is in.
- 26 Sep: FULL-YEAR REBUILD from statements in progress. Method + engine in data/finance/ledger/ (METHOD.md, ledger.py). Old finance.json transactions are NOT trusted: mixed sign conventions (Jan-Apr positive=spend, Aug statement-style), BoS rows in GBP with no currency field, card repayments and Binance counted as spend. Rebuild supersedes them; dashboard totals for Jan-Aug unreliable until it lands.
- Calum pulling all 2026 statements (banks, Wise, Binance, 12 UK cards) - checklist in METHOD.md s10.
Aug unknowns identified (Cara = Tal gift, Kevin = debt, Alex = friend, Seller Network = callouts). Wise statement needed. UK card screenshots outstanding. Sep expected ~Đ103K cash out vs ~101K known.

## Rules
Budget Đ30K flat discretionary; flag hot categories immediately; Deliveries category = eating proxy. No new spend lines without a plan.
