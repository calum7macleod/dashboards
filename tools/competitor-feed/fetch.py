#!/usr/bin/env python3
# Competitor feed: IG Business Discovery -> data/competitor-feed.json -> push to repo
# Env required (in /etc/competitor-feed.env, NEVER committed):
#   IG_TOKEN=<long-lived page token>  IG_BUSINESS_ID=<own IG business user id>  GH_TOKEN=<github pat>
import os, json, urllib.request, urllib.parse, base64, statistics, datetime

TOKEN=os.environ["IG_TOKEN"]; ME=os.environ["IG_BUSINESS_ID"]; GH=os.environ["GH_TOKEN"]
cfg=json.load(open(os.path.join(os.path.dirname(__file__),"config.json")))

def get(url):
    with urllib.request.urlopen(url, timeout=30) as r: return json.load(r)

out={"fetchedAt":datetime.datetime.utcnow().isoformat()+"Z","accounts":[]}
for h in cfg["handles"]:
    fields=(f"business_discovery.username({h})"
            f"{{username,followers_count,media_count,"
            f"media.limit({cfg['per_handle_media']})"
            f"{{caption,like_count,comments_count,media_type,media_product_type,permalink,timestamp}}}}")
    url=f"https://graph.facebook.com/v21.0/{ME}?fields={urllib.parse.quote(fields,safe='(){},.')}&access_token={TOKEN}"
    try:
        bd=get(url)["business_discovery"]
        posts=[]
        for m in bd.get("media",{}).get("data",[]):
            eng=(m.get("like_count") or 0)+(m.get("comments_count") or 0)
            posts.append({"ts":m.get("timestamp"),"type":m.get("media_product_type") or m.get("media_type"),
                          "likes":m.get("like_count"),"comments":m.get("comments_count"),"eng":eng,
                          "permalink":m.get("permalink"),"caption":(m.get("caption") or "")[:180]})
        med=statistics.median([p["eng"] for p in posts]) if posts else 0
        for p in posts:
            p["vsBaseline"]=round(p["eng"]/med,2) if med else None
            p["breakout"]=bool(med and p["eng"]>=cfg["breakout_multiple"]*med)
        out["accounts"].append({"handle":h,"followers":bd.get("followers_count"),
                                "mediaCount":bd.get("media_count"),"medianEng":med,"posts":posts})
        print(f"{h}: {len(posts)} posts, median eng {med}, breakouts {sum(p['breakout'] for p in posts)}")
    except Exception as e:
        out["accounts"].append({"handle":h,"error":str(e)}); print(f"{h}: ERROR {e}")

# push to repo via GitHub API
body=json.dumps(out,indent=1).encode()
api="https://api.github.com/repos/calum7macleod/dashboards/contents/data/competitor-feed.json"
req=urllib.request.Request(api,headers={"Authorization":f"Bearer {GH}","Accept":"application/vnd.github+json"})
sha=None
try: sha=get_existing=json.load(urllib.request.urlopen(req))["sha"]
except Exception: pass
payload={"message":f"competitor-feed: weekly pull {out['fetchedAt']}","content":base64.b64encode(body).decode()}
if sha: payload["sha"]=sha
req=urllib.request.Request(api,data=json.dumps(payload).encode(),method="PUT",
    headers={"Authorization":f"Bearer {GH}","Accept":"application/vnd.github+json","Content-Type":"application/json"})
print("push:",urllib.request.urlopen(req).status)
