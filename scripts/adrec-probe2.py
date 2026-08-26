#!/usr/bin/env python3
"""ADREC probe v2 - deep endpoint discovery for adinteract.co (Next.js aware)."""
import re, json, sys, requests
S=requests.Session()
S.headers.update({"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36",
 "Accept":"text/html,application/json,*/*","Referer":"https://adinteract.co/"})
BASE="https://adinteract.co"

def get(u,**k):
    try: return S.get(u,timeout=25,**k)
    except Exception as e: print("ERR",u[:70],str(e)[:50]); return None

html=get(BASE+"/").text if get(BASE+"/") else ""
print("homepage bytes:",len(html))

# 1) buildId for /_next/data
bid=re.search(r'"buildId":"([^"]+)"',html)
print("buildId:", bid.group(1) if bid else "NOT FOUND")

# 2) all script bundles
scripts=re.findall(r'src="(/_next/[^"]+\.js)"',html)+re.findall(r'src="(/[^"]+\.js)"',html)
scripts=list(dict.fromkeys(scripts))
print("script bundles:",len(scripts))

# 3) __NEXT_DATA__ inline json
nd=re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>',html,re.S)
if nd:
    try:
        j=json.loads(nd.group(1)); print("__NEXT_DATA__ keys:",list(j.keys()))
        # dig for api paths inside
        s=json.dumps(j)
        for m in set(re.findall(r'(/api/[A-Za-z0-9_\-/\.\?=&%]+)',s))|set(re.findall(r'(https?://[^"\\]*\.(?:supabase|vercel|workers\.dev|railway|fly\.dev)[^"\\]*)',s)):
            print("  NEXTDATA ref:",m[:110])
    except Exception as e: print("NEXT_DATA parse err",e)

# 4) scan bundles for real API bases (supabase/rest, cloudflare, vercel serverless, absolute apis)
patterns=[r'https?://[a-z0-9\-]+\.supabase\.co[^"\'`]*',
          r'https?://[a-z0-9\-]+\.workers\.dev[^"\'`]*',
          r'https?://[a-z0-9\-]+\.vercel\.app[^"\'`]*',
          r'https?://[a-z0-9\-]+\.railway\.app[^"\'`]*',
          r'https?://api\.[a-z0-9\-\.]+[^"\'`]*',
          r'/api/[A-Za-z0-9_\-/]+',
          r'/rest/v1/[A-Za-z0-9_\-/]+',
          r'\.from\(["\']([a-z_]+)["\']\)']
hits=set()
for s in scripts[:25]:
    r=get(BASE+s)
    if not r: continue
    b=r.text
    for p in patterns:
        for m in re.findall(p,b): hits.add(m if isinstance(m,str) else m)
print("\n=== candidate data refs in bundles ===")
for h in sorted(hits): print(" ",h[:130])

# 5) supabase tables guess
sb=[h for h in hits if 'supabase' in h]
if sb:
    print("\nSUPABASE base found:",sb[0][:80])
    print(">>> Likely a Supabase backend - Max can query its REST API directly with the anon key from the bundle.")

# 6) try _next/data route if buildId known
if bid:
    for pg in ["index","area/al-reem-island"]:
        u=f"{BASE}/_next/data/{bid.group(1)}/{pg}.json"
        r=get(u)
        if r and r.status_code==200 and r.text.lstrip()[:1] in "{[":
            print("NEXT DATA WORKS:",u,"->",len(r.text),"bytes")
