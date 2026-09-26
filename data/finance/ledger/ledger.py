#!/usr/bin/env python3
"""ledger.py - Finance's reconciliation engine (data/finance/ledger/). Owner: Finance.
Usage:
  python3 ledger.py legacy finance.json          # normalise the old finance.json transactions into canonical rows
  python3 ledger.py build rows/*.json            # merge canonical row files -> ledger.csv, transfers.json, summary.json
  python3 ledger.py tieout balances.json         # per account-month: opening + rows = closing?
Every statement parser (adib_cc_pdf, bos_csv, wise_csv, amex_csv ...) emits canonical rows; build() does the rest.
Sign convention: amount is signed from the account's view: + money in, - money out. Spend is negative.
"""
import sys, json, csv, hashlib, re, datetime, collections, glob

# ---------- reference tables ----------
USD_AED = 3.6725
FX_DEFAULT = {"GBP": 4.75, "USD": USD_AED, "EUR": 4.05, "AED": 1.0}   # "around" - overwritten by fx.json (effective rates from our own conversions)
OWN_ACCOUNTS = ["ADIB", "ADIB CC", "Mashreq", "BoS", "Wise", "Binance", "Tal Card"]
OWN_CARDS = ["MBNA", "M&S", "HSBC", "Barclaycard", "Santander", "Tesco", "Virgin", "Amex", "American Express", "Aqua", "BA Amex"]
CARD_RX = re.compile("|".join(re.escape(c) for c in OWN_CARDS), re.I)
TRANSFER_RX = re.compile(r"transfer|tfr|ziina|wise|binance|card payment in|payment received|thank you|own account|mashreq|adib|bank of scotland|\bbos\b|c ?l ?macleod|calum", re.I)
DEBT_COST_RX = re.compile(r"interest|profit|late fee|annual fee|fx fee|conversion fee|markup|overlimit|charge", re.I)
CASH_RX = re.compile(r"\batm\b|cash withdrawal|cash advance|quasi cash", re.I)
INCOME_RX = re.compile(r"wps|salary|commission|airbnb|payout|refund|cashback", re.I)
INVEST_RX = re.compile(r"binance|kraken|coinbase|tara|modon|hudayriyat|reem", re.I)

def load_fx():
    try: return {**FX_DEFAULT, **json.load(open("fx.json"))}
    except Exception: return FX_DEFAULT

def fx_rate(fx, ccy, month):
    v = fx.get(ccy, 1.0)
    if isinstance(v, dict): return v.get(month, v.get("default", FX_DEFAULT.get(ccy, 1.0)))
    return v

def norm_desc(s): return re.sub(r"[^a-z0-9]+", " ", str(s).lower()).strip()

def row_hash(account, date, amount, desc):
    return hashlib.sha1(f"{account}|{date}|{round(float(amount),2)}|{norm_desc(desc)}".encode()).hexdigest()[:12]

def month_label(date):  # 'Mon YY'
    return datetime.date.fromisoformat(date).strftime("%b %y")

def canonical(account, currency, date, amount, description, source, merchant=None, category=None, sub=None, typ=None, extra=None):
    """Build one canonical row. Parsers call this."""
    d = datetime.date.fromisoformat(date)
    r = {"id": None, "date": date, "month": d.strftime("%b %y"), "dow": d.strftime("%a"), "account": account,
         "currency": currency, "amount": round(float(amount), 2), "amount_aed": None, "type": typ, "category": category,
         "sub": sub, "description": str(description).strip(), "merchant": merchant or norm_desc(description)[:40],
         "pair_id": None, "flags": [], "source": source, "hash": row_hash(account, date, amount, description)}
    if extra: r.update(extra)
    return r

# ---------- typing ----------
def guess_type(r):
    """First-pass type. Human confirms one-legged / Unaccounted rows; merchants.json overrides."""
    d = r["description"]; a = r["amount"]
    if r.get("type"): return r["type"]
    if r["account"] in ("Binance",) : return "investment"
    if CASH_RX.search(d): return "cash_withdrawal" if a < 0 else "transfer"
    if DEBT_COST_RX.search(d) and a < 0 and not TRANSFER_RX.search(d): return "debt_cost"
    if CARD_RX.search(d) and r["account"] not in OWN_CARDS:  # paying one of our cards from a bank account
        return "card_repayment" if a < 0 else "borrowing"
    if r["account"] in OWN_CARDS or r["account"] == "ADIB CC":
        if a > 0 and TRANSFER_RX.search(d): return "card_repayment"          # credit onto the card = repayment leg
        if a > 0: return "refund"
    if INVEST_RX.search(d): return "investment"
    if TRANSFER_RX.search(d): return "transfer"
    if a > 0 and INCOME_RX.search(d): return "income"
    if a > 0: return "income"   # unexplained credit - flagged below
    return "spend"

COUNTS_AS_SPEND = {"spend", "refund", "debt_cost", "cash_withdrawal"}

# ---------- build ----------
def build(files):
    fx = load_fx()
    rows, seen, dups = [], {}, []
    for f in files:   # dedupe ACROSS files only (re-uploaded / overlapping statements); repeats inside one statement are real (fee lines, two Deliveroos)
        for r in json.load(open(f)):
            if r["hash"] in seen and seen[r["hash"]] != f: dups.append({"hash": r["hash"], "first": seen[r["hash"]], "dup": f, "desc": r["description"], "amount": r["amount"]}); continue
            seen[r["hash"]] = f; rows.append(r)
    rows.sort(key=lambda r: (r["date"], r["account"]))
    for i, r in enumerate(rows):
        r["id"] = f"L{i+1:05d}"
        r["type"] = guess_type(r)
        r["amount_aed"] = round(r["amount"] * fx_rate(fx, r["currency"], r["month"]), 2)
        if r["type"] == "income" and not INCOME_RX.search(r["description"]): r["flags"].append("unexplained_credit")
        if not r.get("category"): r["category"] = "Unaccounted" if r["type"] in COUNTS_AS_SPEND else {"debt_cost": "Fees", "investment": "Investing", "cash_withdrawal": "Other"}.get(r["type"], "Other")
    pairs, one_legged = match_transfers(rows)
    write_ledger(rows)
    json.dump({"pairs": pairs, "one_legged": one_legged, "duplicates_dropped": dups}, open("transfers.json", "w"), indent=1)
    summ = summarise(rows)
    json.dump(summ, open("summary.json", "w"), indent=1)
    print(f"rows {len(rows)} | dups dropped {len(dups)} | pairs {len(pairs)} | one-legged {len(one_legged)}")
    for m, v in summ["by_month"].items(): print(m, {k: round(x) for k, x in v.items()})
    return rows

def match_transfers(rows, days=4, tol=0.02):
    cand = [r for r in rows if r["type"] in ("transfer", "card_repayment", "investment", "borrowing") and not r["pair_id"]]
    pairs, used = [], set()
    for a in cand:
        if a["id"] in used: continue
        da = datetime.date.fromisoformat(a["date"])
        best = None
        for b in cand:
            if b["id"] in used or b["id"] == a["id"] or b["account"] == a["account"]: continue
            if (a["amount"] > 0) == (b["amount"] > 0): continue
            if abs((datetime.date.fromisoformat(b["date"]) - da).days) > days: continue
            if a["currency"] == b["currency"]:
                ok = abs(abs(a["amount"]) - abs(b["amount"])) < 0.01
            else:
                ok = abs(abs(a["amount_aed"]) - abs(b["amount_aed"])) <= tol * max(abs(a["amount_aed"]), abs(b["amount_aed"]))
            if ok and (best is None or abs((datetime.date.fromisoformat(b["date"]) - da).days) < best[0]):
                best = (abs((datetime.date.fromisoformat(b["date"]) - da).days), b)
        if best:
            b = best[1]; pid = f"P{len(pairs)+1:04d}"
            a["pair_id"] = b["pair_id"] = pid; used.update([a["id"], b["id"]])
            p = {"pair_id": pid, "out": a["id"] if a["amount"] < 0 else b["id"], "in": b["id"] if a["amount"] < 0 else a["id"],
                 "from": (a if a["amount"] < 0 else b)["account"], "to": (b if a["amount"] < 0 else a)["account"],
                 "amount_out": (a if a["amount"] < 0 else b)["amount"], "amount_in": (b if a["amount"] < 0 else a)["amount"]}
            if a["currency"] != b["currency"]:  # implied effective rate - the real FX cost
                o, i = (a, b) if a["amount"] < 0 else (b, a)
                p["effective_rate"] = round(abs(i["amount"]) / abs(o["amount"]), 4); p["ccy"] = f"{o['currency']}->{i['currency']}"
            pairs.append(p)
    one = [{"id": r["id"], "date": r["date"], "account": r["account"], "amount": r["amount"], "currency": r["currency"], "type": r["type"], "desc": r["description"]}
           for r in cand if r["id"] not in used]
    for r in rows:
        if r["id"] in {o["id"] for o in one}: r["flags"].append("one_legged")
    return pairs, one

def summarise(rows):
    by_month = collections.defaultdict(lambda: collections.defaultdict(float))
    cat = collections.defaultdict(lambda: collections.defaultdict(float))
    dow = collections.defaultdict(float); acct = collections.defaultdict(float)
    for r in rows:
        m = r["month"]; a = r["amount_aed"]
        if r["type"] in COUNTS_AS_SPEND:
            by_month[m]["spend"] += -a; cat[m][r["category"]] += -a; dow[r["dow"]] += -a; acct[r["account"]] += -a
            if r["type"] == "debt_cost": by_month[m]["debt_cost"] += -a
            if r["type"] == "cash_withdrawal": by_month[m]["cash_out"] += -a
        elif r["type"] == "income": by_month[m]["income"] += a
        elif r["type"] == "investment" and a < 0: by_month[m]["invested"] += -a
        elif r["type"] == "card_repayment" and a < 0 and not r["pair_id"]: by_month[m]["card_repay_unmatched"] += -a
    for m in by_month: by_month[m]["net"] = by_month[m]["income"] - by_month[m]["spend"]
    return {"asOf": datetime.date.today().isoformat(), "fx": load_fx(), "by_month": by_month, "by_category": cat,
            "by_dow": dow, "by_account": acct, "note": "AED. spend = spend+refund+debt_cost+cash_withdrawal. Transfers/repayments/investing excluded."}

def write_ledger(rows, path="ledger.csv"):
    cols = ["id","date","month","dow","account","currency","amount","amount_aed","type","category","sub","description","merchant","pair_id","flags","source","hash"]
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols); w.writeheader()
        for r in rows: w.writerow({**{c: r.get(c) for c in cols}, "flags": ";".join(r["flags"])})

# ---------- tie-out ----------
def tieout(rows, balances):
    """balances.json: [{account, month, currency, opening, closing, statement_date}] from the statements themselves."""
    out = []
    for b in balances:
        s = sum(r["amount"] for r in rows if r["account"] == b["account"] and r["month"] == b["month"])
        delta = round(b["opening"] + s - b["closing"], 2)
        out.append({**b, "rows_sum": round(s, 2), "delta": delta, "ok": abs(delta) < 0.01})
    return out

# ---------- legacy import (old finance.json: positive = spend, BoS in GBP with no currency field) ----------
def legacy(path):
    d = json.load(open(path)); out = []
    gbp_accounts = {"BoS", "Tesco Clubcard", "Virgin Money", "Santander Everyday", "M&S", "MBNA 1", "MBNA 2", "HSBC", "Barclaycard Plat", "Wise"}
    for t in d["transactions"]:
        try:
            mo = datetime.datetime.strptime(t["month"], "%b %y"); date = mo.replace(day=int(t.get("day") or 1)).date().isoformat()
        except Exception: continue
        acc = t.get("account") or "-"; ccy = "GBP" if acc in gbp_accounts else "AED"
        if acc == "Wise": ccy = t.get("currency", "GBP")
        out.append(canonical(acc, ccy, date, -float(t["amount"]), t.get("description", ""), "legacy:finance.json",
                             category=t.get("category"), sub=t.get("sub"), extra={"legacy_category": t.get("category")}))
    json.dump(out, open("rows_legacy.json", "w"), indent=0)
    print(f"legacy rows {len(out)} -> rows_legacy.json")

if __name__ == "__main__":
    c = sys.argv[1] if len(sys.argv) > 1 else "help"
    if c == "legacy": legacy(sys.argv[2])
    elif c == "build":
        files = [f for pat in sys.argv[2:] for f in glob.glob(pat)]; build(files)
    elif c == "tieout":
        rows = list(csv.DictReader(open("ledger.csv")))
        for r in rows: r["amount"] = float(r["amount"])
        res = tieout(rows, json.load(open(sys.argv[2])))
        for x in res: print(f"{x['account']:12} {x['month']} open {x['opening']:>10.2f} rows {x['rows_sum']:>10.2f} close {x['closing']:>10.2f} delta {x['delta']:>9.2f} {'OK' if x['ok'] else 'GAP'}")
    else: print(__doc__)
