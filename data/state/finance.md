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
- Wise DONE 26 Sep: 685 rows Jan-Sep (GBP balance + 5 AED + 4 USD), chain clean, closing GBP 200.98. In finance.json (currency, negative = out); 44 screenshot rows retired (delete pending). Canonical: ledger/rows/wise-2026.json. Wise IS a spending account: Deliveroo Dubai, Cafu, Boxica, fittmeals, Meta ads (D20.2K May-Jun), OpenAI/Anthropic, editors (~D700/mo), travel. Effective GBP->AED from his own card rows in ledger/fx.json (4.87-5.00).
- Matched so far: BoS -> Wise top-ups 56 pairs GBP29.5K ("C L MACLEOD" out on BoS = Wise); Wise -> BoS 19 pairs GBP11.4K. Still one-legged: Wise top-ups GBP15.3K (ADIB CC card, expected), Wise -> "Calum Lachlan MacLeod" GBP9.8K (Nationwide, coming), NIUM in GBP28K (UAE side, coming), F/FLOW GBP25.2K (unidentified).
- VANTAGE / FUSION MARKETS (CFD/FX trading) via Wise card: deposits USD14,894 Mar-Jul, withdrawals USD3,024 Aug. Net ~D43.6K out. Typed investment until a Vantage equity statement proves otherwise - Finance treats it as loss. Category Gambling exists with budget 0 for a reason.
- Rebuild engine outputs live in ledger/out/ (ledger.csv, transfers.json, summary.json); merchants.json grows per statement.
- Property Account (UK current acct for 97 Methil Brae) DONE 26 Sep: 44 rows from screenshots, 4 rows missing 3 Jul-5 Aug (Calum to send one screenshot). Rent ~GBP508/mo via YM client account, Precise Mortgages 300.04 -> 287.80 from Jun, arranged OD interest ~GBP50/mo. Rent gets swept to BoS ("CALUM MACLEOD MONEY", 10 pairs) and Wise before the mortgage leaves, so the account runs overdrawn. Masked GBP300.04 credit Feb-May = mortgage amount: who pays it?
- Tesco Clubcard DONE (8 stmts to 4 Aug + Sep app row; 5 Aug-4 Sep stmt missing): balance ~GBP5.7K at 6,325 limit, 27.4%/yr, interest GBP1,198 YTD (~130-148/mo, half the monthly payment), 2 payment reversals + late fees, GBP937 cash advances to Wise (Jun-Jul) with cash fees.
- Virgin Money DONE (9 stmts to 3 Sep): 0% promo ended 3 May, interest went 20 -> ~195/mo (23.9%), GBP2,886 cash advances to Wise Mar-Jun, over limit Jul, DD bounced Jun + Jul, missed-payment flag Sep. Interest GBP797 YTD.
- Santander Everyday DONE 26 Sep: 30 app rows, balance GBP11,716 at 12,150 limit, 0% BT ended May, interest GBP1,052 YTD (~200-216/mo, 21.9%), GBP1,076 to Wise in Jun, overlimit fee, DD reversed May. Payments from BoS show as CALUM LACHLAN MACL - all matched.
- MBNA 1 DONE 26 Sep: 8 stmts to 6 Aug (+ Sep app row), GBP1,863 cash advances to Wise May-Jul (9 top-ups, GBP93 cash fees), interest 33-40/mo -> 87-95/mo since the advances; Apple Store Dubai D4,918 on this card in May + FX fee. Sep stmt page 3 needed.
- MBNA 2, M&S, HSBC, Barclaycard DONE 26 Sep (11 accounts in ledger, 208 pairs). All four dormant on minimums until JUNE, then every one drained into Wise by cash advance. M&S: unpaid DDs May+Jun, late fees Jul+Sep, 21 Sep min NOT paid. Barclaycard over limit 27 Jul. HSBC/MBNA2 small, same pattern.
- CASH ADVANCES card -> Wise 2026: GBP14,814 total (Mar 1,519 / Apr 759 / May 1,437 / Jun 8,633 / Jul 947 / Sep 1,519) across 9 cards (Aqua 2,733, Virgin 2,886, Barclaycard 2,035, M&S 1,964, MBNA1 1,863, Santander 1,110, Tesco 937, MBNA2 724, HSBC 562). Fees ~3% + cash-rate interest from day one. THE pattern of the year.
- UK card balances (latest stmts, GBP): Santander 11,716, Barclaycard 9,422, Virgin 9,706, MBNA1 8,159, M&S ~7,636, Tesco 5,727, Aqua 3,126, MBNA2 1,878, HSBC 1,424, BA Amex 62 = ~58.8K.
- Aqua DONE 26 Sep: NOT cleared. Paid to 29.60 on 31 Jul, then 18 Sep Emirates flight Mauritius GBP1,512 + FX 45, 21 Sep Wise cash advance 1,519 + fee 76. Balance 3,126 at 22 Sep, 38.5% purchases / 42% cash - dearest card. Cash advances YTD 2,733. Unpaid DD 9 Jul. 5 Sep 'cleared to 0' in ccBalances is stale.
- Cost of debt so far, 12 accounts, GBP6,322 YTD (~D13.9K): Tesco 1,261, Santander 1,064, Virgin 853, Aqua 818, MBNA 662, BoS 513, Wise 391, Property OD 336, M&S 214, Barclaycard 175, HSBC 34. Cash advances on 24-27% cards to top up Wise: GBP3,823 - the rule to write.
- 26 Sep data incident: Uploader appended Property rows while Finance held an older copy; Finance's PUT overwrote them; restored from commit 204c1e2. h0029 to Manager.
- Waiting: all other statements (ADIB, ADIB CC, Mashreq, Wise, Binance, 12 UK cards) + the two unidentified UK accounts above. Person legs (Tal, Corrina, Mum, Kevin, Alex, S/Ewen Macleod, Pod Factory, Page LJ, Clerwood, Richmond, Reid, James Gibson, L G Price, Flaher TV) go on ONE resolve list once everything is in.
- 26 Sep: FULL-YEAR REBUILD from statements in progress. Method + engine in data/finance/ledger/ (METHOD.md, ledger.py). Old finance.json transactions are NOT trusted: mixed sign conventions (Jan-Apr positive=spend, Aug statement-style), BoS rows in GBP with no currency field, card repayments and Binance counted as spend. Rebuild supersedes them; dashboard totals for Jan-Aug unreliable until it lands.
- Calum pulling all 2026 statements (banks, Wise, Binance, 12 UK cards) - checklist in METHOD.md s10.
Aug unknowns identified (Cara = Tal gift, Kevin = debt, Alex = friend, Seller Network = callouts). Wise statement needed. UK card screenshots outstanding. Sep expected ~Đ103K cash out vs ~101K known.

## Rules
Budget Đ30K flat discretionary; flag hot categories immediately; Deliveries category = eating proxy. No new spend lines without a plan.
