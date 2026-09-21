#!/usr/bin/env python3
"""agentkit - tiny GitHub Contents API toolkit for Calum's agents.
Setup in a session:
  curl -s https://raw.githubusercontent.com/calum7macleod/dashboards/main/tools/agentkit.py -o agentkit.py
  export GH_TOKEN=<token>   export AGENT=<your agent name>
Commands:
  read <path>                     print a file (dashboards repo; prefix private: for crm-inbox)
  get <path>                      save file to ./<basename> and print its sha
  put <path> <localfile> "<msg>"  create/update a file (handles sha)
  buyers-index                    one line per active buyer
  buyer "<name or phone>"         full record(s) matching
  tasks-due [YYYY-MM-DD]          active tasks due on/before date (default today) + no-date inbox count
  deals-month [YYYY-MM]           deals this month + board sum
  handoffs [to]                   open handoffs (optionally to one agent)
  handoff <to> "<item>"           add an open handoff from $AGENT
  close-handoff <id>              mark a handoff done
  log "<did>" [file1,file2]       append receipt to data/log.jsonl
  state [agent]                   print data/state/<agent>.md (default $AGENT)
"""
import sys, os, json, base64, urllib.request, datetime
TOKEN=os.environ.get("GH_TOKEN"); AGENT=os.environ.get("AGENT","unknown")
if not TOKEN: sys.exit("set GH_TOKEN first")
H={"Authorization":"Bearer "+TOKEN,"Accept":"application/vnd.github+json","Content-Type":"application/json"}
def repo_path(p):
    return ("crm-inbox",p[8:]) if p.startswith("private:") else ("dashboards",p)
def api(repo,p): return f"https://api.github.com/repos/calum7macleod/{repo}/contents/{p}"
def getfile(p):
    repo,pp=repo_path(p)
    m=json.load(urllib.request.urlopen(urllib.request.Request(api(repo,pp)+"?ref=main",headers=H)))
    return base64.b64decode(m["content"]).decode(), m["sha"]
def putfile(p,text,msg):
    repo,pp=repo_path(p); sha=None
    try: sha=getfile(p)[1]
    except Exception: pass
    body={"message":msg,"content":base64.b64encode(text.encode()).decode(),"branch":"main"}
    if sha: body["sha"]=sha
    r=json.load(urllib.request.urlopen(urllib.request.Request(api(repo,pp),data=json.dumps(body).encode(),method="PUT",headers=H)))
    return r["commit"]["sha"][:7]
def jload(p): return json.loads(getfile(p)[0])
def today(): return (datetime.datetime.now(datetime.timezone.utc)+datetime.timedelta(hours=4)).strftime("%Y-%m-%d")
a=sys.argv[1:] or ["help"]; c=a[0]
if c=="help": print(__doc__)
elif c=="read": print(getfile(a[1])[0])
elif c=="get":
    t,s=getfile(a[1]); open(os.path.basename(a[1]),"w").write(t); print(s)
elif c=="put": print("Done -",a[1],putfile(a[1],open(a[2]).read(),a[3] if len(a)>3 else f"{AGENT}: update {a[1]}"))
elif c=="buyers-index":
    b=jload("data/buyers.json"); b=b if isinstance(b,list) else b.get("buyers",[])
    live=[x for x in b if str(x.get("status","")).lower() in ("active","won","new")]
    for x in sorted(live,key=lambda r:(r.get("order") is None, r.get("order") or 9999)):
        print(f"{x.get('order')}|{x.get('buyer')}|s{x.get('score')}|{x.get('budget') or '?'}|{x.get('beds') or '?'}bd|{x.get('stage') or x.get('status')}|touch {x.get('nextTouch') or '-'}|{str(x.get('nextStep') or '')[:60]}")
    print(f"-- {len(live)} live of {len(b)}")
elif c=="buyer":
    q=a[1].lower().replace(" ",""); b=jload("data/buyers.json"); b=b if isinstance(b,list) else b.get("buyers",[])
    for x in b:
        if q in str(x.get("buyer","")).lower().replace(" ","") or q in str(x.get("phone","")).replace(" ",""): print(json.dumps(x,indent=1,ensure_ascii=False))
elif c=="tasks-due":
    d=a[1] if len(a)>1 else today(); t=jload("data/tasks.json")["tasks"]
    due=[x for x in t if x.get("status")=="active" and x.get("due") and x["due"]<=d]
    for x in sorted(due,key=lambda r:r["due"]): print(f"{x['due']}|{x.get('priority')}|{'TOP3 ' if x.get('top3') else ''}{x['title'][:90]}|{x['id']}")
    print(f"-- {len(due)} due by {d}; {sum(1 for x in t if x.get('status')=='active' and not x.get('due'))} in inbox (no date)")
elif c=="deals-month":
    m=a[1] if len(a)>1 else today()[:7]; d=jload("data/deals.json"); d=d if isinstance(d,list) else d.get("deals",[])
    rows=[x for x in d if str(x.get("date","")).startswith(m)]
    for x in rows: print(f"{x['date']}|{x.get('unit')}|{x.get('buyer')}|{x.get('price')}|board {x.get('myBoard')}|take {x.get('myTakeHome')}|pay {x.get('payMonth')}|paid {x.get('paid')}")
    print(f"-- {len(rows)} deals, board {sum(float(x.get('myBoard') or 0) for x in rows):,.0f}")
elif c=="handoffs":
    h=jload("data/handoffs.json"); to=a[1].lower() if len(a)>1 else None
    for x in h:
        if x.get("status")=="open" and (not to or str(x.get("to","")).lower()==to): print(f"{x['id']}|{x['date']}|{x['from']} -> {x['to']}|{x['item']}")
elif c=="handoff":
    h,s=getfile("data/handoffs.json"); h=json.loads(h)
    hid=f"h{len(h)+1:04d}"; h.append({"id":hid,"date":today(),"from":AGENT,"to":a[1],"item":a[2],"status":"open"})
    print("Done - handoff",hid,putfile("data/handoffs.json",json.dumps(h,indent=1,ensure_ascii=False)+"\n",f"{AGENT}: handoff to {a[1]}"))
elif c=="close-handoff":
    h,s=getfile("data/handoffs.json"); h=json.loads(h)
    for x in h:
        if x["id"]==a[1]: x["status"]="done"
    print("Done - closed",a[1],putfile("data/handoffs.json",json.dumps(h,indent=1,ensure_ascii=False)+"\n",f"{AGENT}: close {a[1]}"))
elif c=="log":
    t,s=getfile("data/log.jsonl")
    line=json.dumps({"date":today(),"agent":AGENT,"did":a[1],"wrote":(a[2].split(",") if len(a)>2 else [])},ensure_ascii=False)
    print("Done - receipt",putfile("data/log.jsonl",t.rstrip("\n")+"\n"+line+"\n",f"{AGENT}: receipt"))
elif c=="state":
    ag=(a[1] if len(a)>1 else AGENT).lower().replace(" ","")
    names={"pa":"core","personalassistant":"core","max":"core","claudemanager":"manager","lifecoach":"private:personal/state/lifecoach.md"}
    p=names.get(ag,ag); p=p if p.startswith("private:") else f"data/state/{p}.md"
    print(getfile(p)[0])
else: print("unknown command"); print(__doc__)
