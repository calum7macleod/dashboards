# FINANCE LEDGER - method (Finance owns this folder). Written 2026-09-26.

Purpose: one ledger, every account, Jan-Sep 2026, reconciled to the dirham. Spend counted once. Transfers counted never.

## 1. Every account is its own ledger
Accounts (own money): ADIB current, ADIB CC *789, Mashreq, BoS current (GBP, overdraft), Wise (per currency: GBP, AED, USD, EUR), Binance (USDT/USD), Tal Card (supplementary - confirm which account it bills to).
Liabilities (own cards): MBNA 1 *1654, MBNA 2 *3318, M&S *0340, HSBC *9345, Barclaycard Plat *3001, Santander Everyday, Tesco Clubcard, Virgin Money, Amex Gold, Amex Black, BA Amex, Aqua.
Personal debts (no statements - balances only): Mum, Kevin, Corrina, others in finance.json > personalDebts.

## 2. Every row gets a TYPE. Type decides whether it counts - category only says what it was.
| type | counts as spend? | example |
|---|---|---|
| spend | YES | Deliveroo, Boxica, rent, Meta ads |
| refund | YES (negative, nets the category) | Amazon refund |
| debt_cost | YES | card interest, OD interest, Murabaha profit share, FX fees, late fees |
| cash_withdrawal | YES (category Cash until explained) | ATM |
| income | no (income) | WPS commission, Airbnb payout, refund of deposit |
| transfer | no (own money moving) | Mashreq -> ADIB, BoS -> Wise -> ADIB |
| card_repayment | no (paying own card) | BoS -> Amex 8,200 ; ADIB -> card *789 30,000 |
| debt_principal | no (balance sheet) | Murabaha principal, repayment to Mum |
| investment | no (asset swap) | ADIB -> Binance, Tara instalment, Hudayriyat |
| borrowing | no (liability up) | money in from Mum, BT onto Barclaycard |

The spend on a card is the line items ON the card statement. The payment TO the card is never spend. If a card statement is missing, its repayment is the only trace and gets typed `card_repayment` with flag `statement_missing` - the spend behind it is invisible until the statement lands.

## 3. Transfer matching (the double-count killer)
Candidate = any row whose description names one of our own accounts or cards, or is a bank-to-bank transfer / Ziina / Wise / Binance deposit-withdrawal.
Match = opposite-sign row on another own account, within +/-4 days, amount equal after FX within 2% (cross-currency) or exact (same currency). Both legs get the same `pair_id`; net zero.
Unmatched leg = flagged `one_legged`: either the other statement is missing or it is actually external (a friend, a supplier). Each one gets resolved by hand, none silently counted.
Cross-currency pairs give the true effective FX rate - the fee is the gap between market rate and effective rate, typed `debt_cost` sub `FX fee`.

## 4. Dedupe
Row hash = account + date + amount + normalised description. Same hash from two files = the same statement uploaded twice or overlapping periods; second copy dropped and reported. Legitimate identical rows (two 84.00 Deliveroos same day) survive because the bank reference differs.

## 5. Currency
Native currency kept on every row. Report in AED. USD at 3.6725 (peg). GBP at the month's effective rate from our own Wise/BoS conversions where we have one; otherwise the monthly mid-rate in fx.json marked "around". Never mix GBP and AED in one total (the old ledger did - BoS rows were logged with no currency).

## 6. Tie-out (the proof it's complete)
Per account per month: statement opening balance + sum(rows) = statement closing balance. Delta 0 = complete. Any delta is named as `Unaccounted` for that account-month until found. Card balances in ccBalances must equal the card statement closing balance on the statement date.

## 7. Categories (dashboard keeps the 14; `sub` carries the detail)
Base Food (groceries) · Deliveries (eating proxy) · Life (rent, DEWA, phone, home, transport, personal) · Business (Modon accrual, editors, Meta/Google, software, licence, client hospitality) · Entertainment (bars, nights out, travel, gifts to friends) · Health (Boxica, gym, medical, supplements, Whoop) · Family (Tal allowance, baby, family gifts) · Fees (interest + bank/FX fees = cost of debt) · Loan (principal only, type debt_principal - not spend) · Investing (type investment) · Saving (type transfer) · Gambling · Cash (new sub of Other: withdrawals) · Other · Unaccounted.
Merchant -> category map lives in merchants.json and grows with every statement; every merchant classified once, then automatic.

## 8. Outputs
- ledger.csv - every row, canonical schema (below)
- transfers.json - matched pairs and one-legged flags
- tieout.md - per account per month, delta
- summary.json - spend by category by month (AED), income, debt cost, cash withdrawals, net worth line (cash + crypto + property paid-in - cards - personal debt)
- report.html - charts: monthly spend vs income; category stack; weekday vs weekend; time-of-day (card rows carry it); Deliveries trend; debt balance trend; cost-of-debt line; transfer matrix

## 9. Canonical row schema
{id, date (YYYY-MM-DD), month (Mon YY), dow, account, currency, amount (signed, + in / - out), amount_aed, type, category, sub, description, merchant, pair_id, flags[], source (file), hash}

## 10. What to pull (period 1 Jan - 26 Sep 2026, one file per account, closing balance visible)
Order of preference: CSV/XLSX export > PDF statement > screenshots.
- ADIB current: CSV from app (Statements > download) - all of 2026
- ADIB CC *789: monthly PDF statements Jan-Sep (9 files) - the app CSV misses fees
- Mashreq: CSV/XLSX export 2026
- BoS: CSV export (app > Statements > export) 2026 incl. overdraft interest lines
- Wise: CSV statement per currency balance, 2026 - this also gives the real FX rates
- Binance: Transaction History CSV + Deposit/Withdrawal history 2026
- UK cards x12: monthly PDF statements Jan-Sep (Amex offers CSV - take it). Where cleared/closed, last statement + closing letter
- Personal debts: one line each - who, opening balance 1 Jan, payments made, balance today
- Tal Card: which account does it bill to, and its statements if separate
Name files: <account>-<YYYYMM or 2026>.<ext>. Drop them all at once; partial sets create one-legged transfers.
