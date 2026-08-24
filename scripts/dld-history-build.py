#!/usr/bin/env python3
"""
DLD full-history builder — run on the droplet (2GB RAM safe, chunked).
Downloads the complete Dubai Pulse DLD transactions file, aggregates
per-area monthly stats, writes compact JSONs, pushes them to GitHub.

Usage:
  python3 dld-history-build.py                      # download + build + push
  python3 dld-history-build.py --csv /path/file.csv # use an already-downloaded csv
  python3 dld-history-build.py --no-push            # build only

Requires: pip3 install pandas requests
Set env GH_TOKEN before running (do NOT hardcode).
"""
import os, sys, json, base64, argparse, math
import pandas as pd, requests

# Dubai Pulse open-data: DLD Transactions (full history CSV, ~1-2 GB)
CSV_URL = "https://www.dubaipulse.gov.ae/dataset/00768c45-f014-4cc6-937d-2b17dcab53fb/resource/a37511b0-ea36-485d-bf4f-4ab9f6a90dc7/download/transactions.csv"
REPO   = "calum7macleod/dashboards"
BRANCH = "main"
OUTDIR = "out-dld-history"

SALE_PROCS = {"Sell", "Sale", "Delayed Sell", "Sell - Pre registration"}

def download(dest="transactions.csv"):
    if os.path.exists(dest) and os.path.getsize(dest) > 1e8:
        print(f"using existing {dest}"); return dest
    print("downloading full transactions file (large, be patient)...")
    with requests.get(CSV_URL, stream=True, timeout=120) as r:
        r.raise_for_status()
        with open(dest, "wb") as f:
            for chunk in r.iter_content(1 << 20):
                f.write(chunk)
    print(f"done: {os.path.getsize(dest)/1e6:.0f} MB")
    return dest

def build(csv_path):
    os.makedirs(OUTDIR, exist_ok=True)
    usecols = ["instance_date","procedure_name_en","area_name_en","prop_type_en",
               "actual_worth","procedure_area","rooms_en","project_name_en"]
    agg = {}      # (area, month) -> lists
    proj = {}     # (project, month) -> lists   (Lagoons projects only, keeps size sane)
    n=0
    for chunk in pd.read_csv(csv_path, usecols=lambda c: c in usecols,
                             chunksize=250_000, low_memory=True):
        n+=len(chunk)
        chunk = chunk[chunk["procedure_name_en"].isin(SALE_PROCS)]
        chunk = chunk.dropna(subset=["instance_date","actual_worth","area_name_en"])
        chunk = chunk[chunk["actual_worth"] > 50_000]           # junk filter
        chunk["m"] = pd.to_datetime(chunk["instance_date"], errors="coerce", dayfirst=True).dt.strftime("%Y-%m")
        chunk = chunk.dropna(subset=["m"])
        psm = chunk["actual_worth"] / chunk["procedure_area"].replace(0, math.nan)
        for (a,m), g in chunk.groupby(["area_name_en","m"]):
            d = agg.setdefault((a,m), {"v":[], "psm":[]})
            d["v"] += g["actual_worth"].tolist()
            d["psm"] += psm.loc[g.index].dropna().tolist()
        lag = chunk[chunk["project_name_en"].astype(str).str.contains("LAGOONS", na=False)]
        for (p,m), g in lag.groupby(["project_name_en","m"]):
            d = proj.setdefault((p,m), {"v":[]})
            d["v"] += g["actual_worth"].tolist()
        print(f"\r{n:,} rows processed", end="")
    print()

    def med(x): return round(float(pd.Series(x).median()),0) if x else None
    areas = {}
    for (a,m), d in agg.items():
        areas.setdefault(a, {})[m] = {"n":len(d["v"]), "med":med(d["v"]), "medPsm":med(d["psm"])}
    with open(f"{OUTDIR}/citywide-monthly.json","w") as f:
        json.dump(areas, f, separators=(",",":"))
    lagoons = {}
    for (p,m), d in proj.items():
        lagoons.setdefault(p, {})[m] = {"n":len(d["v"]), "med":med(d["v"])}
    with open(f"{OUTDIR}/lagoons-projects-monthly.json","w") as f:
        json.dump(lagoons, f, separators=(",",":"))
    print("built:", {f: f"{os.path.getsize(OUTDIR+'/'+f)/1e6:.1f} MB" for f in os.listdir(OUTDIR)})

def push():
    tok = os.environ.get("GH_TOKEN")
    if not tok: sys.exit("set GH_TOKEN env var first")
    for fn in os.listdir(OUTDIR):
        path = f"data/dld/history/{fn}"
        url  = f"https://api.github.com/repos/{REPO}/contents/{path}"
        h = {"Authorization": f"Bearer {tok}"}
        sha = requests.get(url, headers=h, params={"ref":BRANCH}).json().get("sha")
        body = {"message": f"DLD history: {fn}", "branch": BRANCH,
                "content": base64.b64encode(open(f"{OUTDIR}/{fn}","rb").read()).decode()}
        if sha: body["sha"] = sha
        r = requests.put(url, headers=h, json=body)
        print(path, "->", r.json().get("commit",{}).get("sha","FAILED")[:8])

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv"); ap.add_argument("--no-push", action="store_true")
    a = ap.parse_args()
    csvp = a.csv or download()
    build(csvp)
    if not a.no_push: push()
