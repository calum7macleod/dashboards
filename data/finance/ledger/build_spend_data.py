#!/usr/bin/env python3
"""build_spend_data.py - spend-data.json from ledger.csv for the spending report. Finance owns. Run after ledger.py build."""
import csv, collections, json, datetime, re, sys
rows = list(csv.DictReader(open('ledger.csv')))
ORDER = ['Jan 26','Feb 26','Mar 26','Apr 26','May 26','Jun 26','Jul 26','Aug 26','Sep 26']
SP = {'spend','refund','debt_cost','cash_withdrawal'}
ASOF = sys.argv[1] if len(sys.argv) > 1 else datetime.date.today().isoformat()
MONTHS_ELAPSED = 9.0
def f(x): return round(float(x), 2)
def clean(s):
    s = re.sub(r'^ipp transfer (.+?) ref .*$', r'\1', s); s = re.sub(r'^sent money to ', '', s); s = re.sub(r'^card transaction of .*? issued by ', '', s)
    s = re.sub(r'(cardless cash withdrawal|atm cash withdrawal).*', 'cash withdrawal', s); s = re.sub(r'\s*,\s*(dubai|abu dhabi|abudhabi|dxb)\s*$', '', s)
    return re.sub(r'\s+', ' ', s).strip()[:34]
D = {'asOf': ASOF, 'months': ORDER}
cat = collections.defaultdict(lambda: [0.0]*9); sub = collections.defaultdict(lambda: [0.0]*9); inc = [0.0]*9; tot = [0.0]*9
region = {'AED': [0.0]*9, 'GBP': [0.0]*9}; fees = [0.0]*9; eat = {'Deliveries': [0.0]*9, 'Eating out': [0.0]*9, 'Groceries': [0.0]*9}
merch = collections.defaultdict(lambda: [0.0, 0]); unacc = []; notcounted = collections.defaultdict(float); dow = collections.defaultdict(float); cov = collections.defaultdict(set)
tal = [0.0]*9; incdetail = []; byacct = collections.defaultdict(lambda: [0.0]*9)
for r in rows:
    a = f(r['amount_aed']); mi = ORDER.index(r['month']) if r['month'] in ORDER else None
    if mi is None: continue
    cov[r['account']].add(r['month'])
    if 'Tal (one pot' in r['sub'] and a < 0 and not r['pair_id']: tal[mi] += -a
    if r['type'] == 'income':
        mi2 = mi-1 if (r['date'] >= '2026-09-01' and r['date'] <= '2026-09-07' and 'Salary' in r['description']) else mi
        inc[mi2] += a; incdetail.append({'date': r['date'], 'aed': round(a), 'desc': clean(r['description'].lower()), 'countedIn': ORDER[mi2]})
    if r['type'] in SP:
        cat[r['category']][mi] += -a; sub[(r['category'], r['sub'])][mi] += -a; tot[mi] += -a; byacct[r['account'].split()[0]][mi] += -a
        ccy = r.get('txn_ccy') or r['currency']; region['AED' if ccy == 'AED' else 'GBP'][mi] += -a
        if r['category'] == 'Fees': fees[mi] += -a
        if r['category'] == 'Deliveries' and 'delivery' in r['sub'].lower(): eat['Deliveries'][mi] += -a
        elif r['category'] == 'Deliveries' or 'eating out' in r['sub'].lower(): eat['Eating out'][mi] += -a
        elif r['category'] == 'Base Food': eat['Groceries'][mi] += -a
        key = clean((r['merchant'] or r['description']).lower()); merch[key][0] += -a; merch[key][1] += 1
        if r['type'] != 'refund': dow[r['dow']] += -a
        if r['category'] == 'Unaccounted' and -a >= 300: unacc.append({'date': r['date'], 'account': r['account'], 'aed': round(-a), 'desc': r['description'][:60]})
    if r['type'] == 'passthrough': notcounted['Pass-through for co-investors / Pod Factory (net)'] += a
    if r['type'] == 'investment': notcounted['Investments (own): Modon, Binance, Vantage deposits'] += -a
for i in range(9):
    cat['Tal share (50% of money sent)'][i] = tal[i]*0.5; sub[('Tal share (50% of money sent)', 'other 50% = her/pot')][i] = tal[i]*0.5; tot[i] += tal[i]*0.5
notcounted['Other 50% of money sent to Tal (one pot)'] = round(sum(tal)*0.5)
# cash advance cost
adv = []; cashfees = 0.0
for r in rows:
    if 'cash advance ->' in r['sub'] and float(r['amount']) < 0: adv.append((r['account'], r['date'], -float(r['amount'])))
    if r['type'] == 'debt_cost' and 'cash' in r['description'].lower() and r['currency'] == 'GBP': cashfees += -float(r['amount'])
end = datetime.date.fromisoformat(ASOF); est = 0.0; per = collections.defaultdict(lambda: [0.0, 0.0, 0.0])
for acc, dt, amt in adv:
    d0 = datetime.date.fromisoformat(dt); until = min(end, datetime.date(2026, 7, 31)) if acc == 'Aqua' and d0 < datetime.date(2026, 7, 31) else end
    i = amt*0.023*max(0, (until-d0).days)/30.4; est += i; per[acc][0] += amt; per[acc][1] += i
for r in rows:
    if r['type'] == 'debt_cost' and 'cash' in r['description'].lower() and r['currency'] == 'GBP': per[r['account']][2] += -float(r['amount'])
still = sum(a for acc, dt, a in adv if acc != 'Aqua' or dt > '2026-07-31')
D['cashAdvanceCost'] = {'totalGBP': round(sum(a for _, _, a in adv)), 'explicitFeesGBP': round(cashfees), 'estInterestGBP': round(est), 'costSoFarGBP': round(cashfees+est), 'stillOutstandingGBP': round(still), 'runningPerMonthGBP': round(still*0.023),
  'perCard': [{'card': k, 'advancedGBP': round(v[0]), 'feesGBP': round(v[2]), 'estInterestGBP': round(v[1])} for k, v in sorted(per.items(), key=lambda kv: -kv[1][0])],
  'secondOrder': 'June drain pushed Virgin, Barclaycard, Santander, Aqua over limit -> overlimit fees, then 9 bounced payments (Jun-Sep) with late fees. Estimate 2.3%/mo cash rate; Aqua advances counted repaid 31 Jul.'}
D['byCategory'] = {k: [round(x) for x in v] for k, v in sorted(cat.items(), key=lambda kv: -sum(kv[1]))}
D['bySub'] = [{'category': k[0], 'sub': k[1], 'months': [round(x) for x in v], 'total': round(sum(v))} for k, v in sorted(sub.items(), key=lambda kv: -sum(kv[1])) if sum(v) >= 500]
D['byAccount'] = {k: [round(x) for x in v] for k, v in sorted(byacct.items(), key=lambda kv: -sum(kv[1]))}
D['total'] = [round(x) for x in tot]; D['income'] = [round(x) for x in inc]; D['incomeDetail'] = sorted(incdetail, key=lambda x: x['date'])
D['region'] = {k: [round(x) for x in v] for k, v in region.items()}; D['fees'] = [round(x) for x in fees]; D['eating'] = {k: [round(x) for x in v] for k, v in eat.items()}
D['topMerchants'] = [{'merchant': k, 'aed': round(v[0]), 'n': v[1]} for k, v in sorted(merch.items(), key=lambda kv: -kv[1][0])[:30]]
D['unaccounted'] = sorted(unacc, key=lambda x: -x['aed'])[:40]; D['notCounted'] = {k: round(v) for k, v in notcounted.items() if v}; D['byDow'] = {k: round(v) for k, v in dow.items()}
D['coverage'] = {k: sorted(v, key=ORDER.index) for k, v in cov.items()}
D['coverageNote'] = {'ADIB CC': 'Statements Jan-Aug (8, every one ties to the printed balance); September from app screenshots, 30/30 days', 'ADIB': 'Current account: Feb-Apr screenshots only - statements still wanted', 'Amex Black / BA': 'not yet in the ledger', 'Tal accounts': 'one pot - her card spend invisible; 50% of money sent to her counted as spend', 'Binance': 'ignored per Calum'}
D['vantage'] = {'depositsUSD': 14894, 'withdrawalsUSD': 3024, 'equityUSD': 6000, 'lossUSD': 5870, 'lossAED': 21560}
D['monthsElapsed'] = MONTHS_ELAPSED
json.dump(D, open('spend-data.json', 'w'), indent=1)
print('total', round(sum(tot)), 'per month', round(sum(tot)/MONTHS_ELAPSED), 'income', round(sum(inc)), 'fees', round(sum(fees)))
print('by month', [round(x) for x in tot])
print('by account', {k: round(sum(v)) for k, v in D['byAccount'].items()})
