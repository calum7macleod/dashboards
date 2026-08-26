#!/usr/bin/env python3
"""
ADREC collector - run on the droplet (or any machine with open internet).
Discovers ADInteract's transaction data endpoint, pulls all rows since 2019,
stores per-district JSON + a full dump, pushes to GitHub repo.

Usage:
  export GH_TOKEN=github_pat_...
  python3 adrec-collector.py            # discover + full pull + push
  python3 adrec-collector.py --probe    # just discover endpoints, print, exit
  python3 adrec-collector.py --no-push  # pull but don't push

Nightly cron (after first successful run):
  17 2 * * * cd /root && GH_TOKEN=$(cat /root/.ghtoken) python3 adrec-collector.py >> adrec.log 2>&1
"""
import os, sys, json, base64, re, time
import requests

REPO="calum7macleod/dashboards"; BRANCH="main"
S=requests.Session()
S.headers.update({"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36",
                  "Accept":"application/json, text/plain, */*",
                  "Referer":"https://adinteract.co/"})

BASE="https://adinteract.co"

def discover():
    """Find the JSON endpoint the dashboard calls."""
    found=[]
    # 1) parse homepage + its JS bundles for fetch/axios URLs
    try:
        html=S.get(BASE+"/",timeout=20).text
    except Exception as e:
        print("homepage fetch failed:",e); html=""
    scripts=re.findall(r'src="(/[^"]+\.js[^"]*)"',html)
    blobs=[html]
    for s in scripts[:12]:
        try: blobs.append(S.get(BASE+s,timeout=20).text)
        except Exception: pass
    cand=set()
    for b in blobs:
        for m in re.findall(r'["\'](/api/[A-Za-z0-9_\-/\.]*)["\']',b): cand.add(m)
        for m in re.findall(r'["\'](https?://[^"\']*adinteract[^"\']*/api/[^"\']*)["\']',b): cand.add(m)
        for m in re.findall(r'["\'](/_next/data/[^"\']+\.json)["\']',b): cand.add(m)
        for m in re.findall(r'["\'](/data/[A-Za-z0-9_\-/\.]*\.json)["\']',b): cand.add(m)
    # 2) common guesses
    for g in ["/api/transactions","/api/transactions?page=1","/api/sales","/api/txns",
              "/api/search","/api/districts","/api/stats","/api/latest",
              "/api/transactions?district=Al%20Reem%20Island&limit=50"]:
        cand.add(g)
    print(f"{len(cand)} candidate endpoints")
    for c in sorted(cand):
        url=c if c.startswith("http") else BASE+c
        try:
            r=S.get(url,timeout=15)
            ct=r.headers.get("content-type","")
            ok = r.status_code==200 and ("json" in ct or r.text.lstrip()[:1] in "[{")
            print(f"{r.status_code} {'JSON' if ok else ct[:20]:>20} {url[:100]}")
            if ok and len(r.text)>50: found.append((url,r.text[:400]))
        except Exception as e:
            print("ERR",url[:80],str(e)[:60])
    return found

def gh_put(path,obj,msg):
    tok=os.environ.get("GH_TOKEN")
    if not tok: sys.exit("set GH_TOKEN")
    url=f"https://api.github.com/repos/{REPO}/contents/{path}"
    h={"Authorization":f"Bearer {tok}"}
    sha=requests.get(url,headers=h,params={"ref":BRANCH}).json().get("sha")
    body={"message":msg,"branch":BRANCH,
          "content":base64.b64encode(json.dumps(obj,separators=(',',':')).encode()).decode()}
    if sha: body["sha"]=sha
    r=requests.put(url,headers=h,json=body)
    print(path,"->",r.json().get("commit",{}).get("sha","FAIL")[:8])

def paged_pull(url_tmpl):
    """Pull all pages from a discovered endpoint. Adjust per endpoint shape."""
    rows=[]; page=1
    while True:
        u=url_tmpl.format(page=page)
        r=S.get(u,timeout=30)
        if r.status_code!=200: break
        d=r.json()
        batch=d if isinstance(d,list) else d.get("transactions") or d.get("data") or d.get("rows") or d.get("results") or []
        if not batch: break
        rows+=batch
        print(f"page {page}: +{len(batch)} (total {len(rows)})")
        page+=1
        if page>4000: break
        time.sleep(0.35)
    return rows

if __name__=="__main__":
    hits=discover()
    print("\n=== WORKING JSON ENDPOINTS ===")
    for u,preview in hits:
        print("\n",u,"\n  preview:",preview[:200].replace("\n"," "))
    if "--probe" in sys.argv or not hits:
        if not hits: print("\nNo open JSON endpoints found. Send this output to Max - plan B is the Chrome-side harvest.")
        sys.exit(0)
    # naive: try the richest-looking endpoint with page param
    # (Max will refine once probe output is known)
    best=hits[0][0]
    tmpl=best+("&page={page}" if "?" in best else "?page={page}")
    rows=paged_pull(tmpl)
    if rows:
        out={"pulled":time.strftime("%Y-%m-%d %H:%M"),"source":"ADREC via ADInteract","count":len(rows),"rows":rows}
        json.dump(out,open("adrec-full.json","w"))
        print("saved adrec-full.json",len(rows),"rows")
        if "--no-push" not in sys.argv:
            # split if huge
            if len(json.dumps(out))>80_000_000:
                print("too large for single file - splitting by year")
                from collections import defaultdict
                by=defaultdict(list)
                for r in rows: by[str(r.get("date","")[:4] or "unknown")].append(r)
                for y,rr in by.items(): gh_put(f"data/adrec/tx-{y}.json",{"count":len(rr),"rows":rr},f"ADREC rows {y}")
            else:
                gh_put("data/adrec/transactions.json",out,"ADREC full transaction pull")
