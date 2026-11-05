#!/usr/bin/env python3
"""agentkit - tiny GitHub Contents API toolkit for Calum's agents.
Setup in a session:
  curl -s https://raw.githubusercontent.com/calum7macleod/dashboards/main/tools/agentkit.py -o agentkit.py
  export GH_TOKEN=<token>   export AGENT=<your agent name>
Commands:
  read <path>                     print a file (dashboards repo; prefix private: for crm-inbox; files over 1MB handled)
  get <path>                      save file to ./<basename> + ./<basename>.sha (the sha guards your later put)
  put <path> <localfile> "<msg>"  write the file. Uses the sha from your get; if the file changed since, it REFUSES - re-get, redo, put again
  buyers-index [all]              one line per live buyer (stage not Won/Lost); 'all' = everyone, live first
  buyers-check                    rule violations in buyers + archive-buyers (status must follow stage; dates; stray stages)
  buyer "<name or phone>"         full record(s) matching
  owner "<unit|name|cluster>"     DAMAC Lagoons owner rows matching (private repo, 3+ chars, max 50 rows, never the file)
  tasks-due                       Today band (with days in band), then This week; plus any dated task past due
  task "<title>" [area] [band]    add a task (band today|week|month|year, default today)
  tasks-roll                      dated tasks into the right band (same rule as today.html) - the PA's 07:30 step
  tasks-archive                   done/killed older than 7 days -> data/archive/tasks-done-<year>.json
  deals-month [YYYY-MM]           deals signed in month with commission
  handoffs [to]                   open handoffs (optionally to one agent)
  handoff <to> "<item>"           add an open handoff from $AGENT
  close-handoff <id>              mark a handoff done
  issue <type> "<what>"           log a system fault the moment it happens (type: tool|data|rule|access|asked) -> data/issues.jsonl
  issues [open|all] [agent]       list issues (default open)
  fix <id> "<what changed>"       close an issue (Manager)
  log "<did>" [file1,file2]       append receipt to data/log.jsonl
  state [agent]                   print data/state/<agent>.md (default $AGENT)
  board [stage]                   content board: count per stage, then cards (id|title|series|stageDate|postDate); one stage or all
  stage <id> <stage> [postDate]   move a content card: sets stage + stageDate=today; posted also sets status/postDate
  card add "<title>" --stage <stage> --series "<series>" [--hook "..."] [--post YYYY-MM-DD] [--notes "..."]   new card, next cN
  card edit <id> [--title "..."] [--hook "..."] [--series "..."] [--post YYYY-MM-DD] [--notes "..."]        change fields
Writes that read-modify-write (handoff, log, issue, stage, card, task...) retry automatically if another agent wrote first.
"""
import sys, os, json, base64, urllib.request, urllib.error, datetime, time, re
TOKEN=os.environ.get("GH_TOKEN"); AGENT=os.environ.get("AGENT","unknown")
if not TOKEN: sys.exit("set GH_TOKEN first")
H={"Authorization":"Bearer "+TOKEN,"Accept":"application/vnd.github+json","Content-Type":"application/json"}
def repo_path(p):
    return ("crm-inbox",p[8:]) if p.startswith("private:") else ("dashboards",p)
def api(repo,p): return f"https://api.github.com/repos/calum7macleod/{repo}/contents/{p}"
class Conflict(Exception): pass
def getfile(p):
    repo,pp=repo_path(p)
    m=json.load(urllib.request.urlopen(urllib.request.Request(api(repo,pp)+"?ref=main",headers=H)))
    if m.get("encoding")=="none" or m.get("size",0)>1000000:
        raw=urllib.request.urlopen(urllib.request.Request(api(repo,pp)+"?ref=main",headers=dict(H,Accept="application/vnd.github.raw+json"))).read().decode()
        return raw, m["sha"]
    return base64.b64decode(m["content"]).decode(), m["sha"]
def putfile(p,text,msg,sha=None):
    """PUT with the sha the caller read. No sha = fresh sha (new file or caller accepts last-write-wins). 409 -> Conflict."""
    repo,pp=repo_path(p)
    if sha is None:
        try: sha=getfile(p)[1]
        except Exception: pass
    body={"message":msg,"content":base64.b64encode(text.encode()).decode(),"branch":"main"}
    if sha: body["sha"]=sha
    try:
        r=json.load(urllib.request.urlopen(urllib.request.Request(api(repo,pp),data=json.dumps(body).encode(),method="PUT",headers=H)))
    except urllib.error.HTTPError as e:
        if e.code==409: raise Conflict(p)
        raise
    return r["commit"]["sha"][:7]
def modify(p,fn,msg,tries=4):
    """read -> fn(text)->newtext -> write with that sha; if someone wrote in between, re-read and redo. Never clobbers."""
    for i in range(tries):
        try: text,sha=getfile(p)
        except urllib.error.HTTPError as e:
            if e.code!=404: raise
            text,sha="",None
        try: return putfile(p,fn(text),msg,sha)
        except Conflict:
            if i==tries-1: raise
            time.sleep(0.4*(i+1))
def jmodify(p,fn,msg,indent=1):
    return modify(p,lambda t:json.dumps(fn(json.loads(t) if t.strip() else []),indent=indent,ensure_ascii=False)+"\n",msg)
def jload(p): return json.loads(getfile(p)[0])
def today(): return (datetime.datetime.now(datetime.timezone.utc)+datetime.timedelta(hours=4)).strftime("%Y-%m-%d")
a=sys.argv[1:] or ["help"]; c=a[0]
if c=="help": print(__doc__)
elif c=="read": print(getfile(a[1])[0])
elif c=="get":
    t,sha=getfile(a[1]); fn=os.path.basename(a[1]); open(fn,"w").write(t); open(fn+".sha","w").write(a[1]+" "+sha); print("Done -",fn,sha)
elif c=="put":
    fn=a[2]; sha=None
    try:
        rp,rs=open(fn+".sha").read().split(); sha=rs if rp==a[1] else None
    except Exception: pass
    if sha is None: print("warning: no sha from a get for this path - writing over whatever is there")
    try: print("Done -",a[1],putfile(a[1],open(fn).read(),a[3] if len(a)>3 else f"{AGENT}: update {a[1]}",sha))
    except Conflict: sys.exit(f"REFUSED - {a[1]} changed since your get. Re-get it, redo your edit, put again. Nothing was written.")
elif c=="buyers-index":
    b=jload("data/buyers.json"); b=b if isinstance(b,list) else b.get("buyers",[])
    isl=lambda x: x.get("stage") not in ("Won","Lost") and not str(x.get("status","")).lower().startswith("closed")
    live=[x for x in b if isl(x)]
    rows=live if not (len(a)>1 and a[1]=="all") else live+[x for x in b if x.get("stage")=="Won"]+[x for x in b if not isl(x) and x.get("stage")!="Won"]
    for x in sorted(rows,key=lambda r:(not isl(r), r.get("order") is None, r.get("order") or 9999)):
        print(f"{x.get('order')}|{x.get('buyer')}|s{x.get('score')}|{x.get('budget') or '?'}|{x.get('beds') or '?'}bd|{x.get('stage') or x.get('status')}|touch {x.get('nextTouch') or '-'}|{str(x.get('nextStep') or '')[:60]}")
    print(f"-- {len(live)} live of {len(b)}")
elif c=="buyers-check":
    STAGES=("Longer Term","New","Qualified","Viewing","Offer","Won","Lost"); derived={"Won":"Closed Won","Lost":"Closed Lost"}
    n=k=0
    for f in ("data/buyers.json","data/archive-buyers.json"):
        try: b=jload(f)
        except Exception as e: print(f"{f}: cannot read ({e})"); continue
        b=b if isinstance(b,list) else b.get("buyers",[])
        for x in b:
            st=x.get("stage"); want=derived.get(st,"Active"); probs=[]
            if st not in STAGES: probs.append(f"stage '{st}' not in list")
            if x.get("status")!=want: probs.append(f"status '{x.get('status')}' should be '{want}'")
            if x.get("closedDate"): probs.append("closedDate (deprecated)")
            if st=="Won" and not x.get("closedWon"): k+=1
            if st=="Lost" and not x.get("closedLost"): k+=1
            for pr in probs: n+=1; print(f"{f.split('/')[-1]}|{x.get('id')}|{x.get('buyer')}|{pr}")
    print(f"-- {n} violations, {k} closed without a date")
elif c=="buyer":
    q=a[1].lower().replace(" ",""); b=jload("data/buyers.json"); b=b if isinstance(b,list) else b.get("buyers",[])
    for x in b:
        if q in str(x.get("buyer","")).lower().replace(" ","") or q in str(x.get("phone","")).replace(" ",""): print(json.dumps(x,indent=1,ensure_ascii=False))
elif c=="owner":
    q=(a[1] if len(a)>1 else "").strip().lower()
    if len(q)<3: sys.exit("owner needs 3+ characters: a unit, an owner name or a cluster")
    recs=jload("private:data/owners/damac-lagoons-owners.json")["records"]
    hits=[r for r in recs if q in str(r.get("unit_number") or "").lower() or q in str(r.get("name") or "").lower() or q in str(r.get("cluster") or "").lower()]
    for r in hits[:50]: print(f"{r.get('cluster')}|{r.get('unit_number')}|{r.get('name')}|{r.get('mobile_e164') or r.get('mobile') or '-'}|{r.get('country') or ''}|size {r.get('size_raw') or r.get('size') or '?'}")
    print(f"-- {len(hits)} matches"+(" (showing 50)" if len(hits)>50 else "")+" - extracted 2026-09-07, verify before quoting")
elif c=="tasks-due":
    d=today(); t=jload("data/tasks.json")["tasks"]; act=[x for x in t if x.get("status")=="active"]
    age=lambda x:(datetime.date.fromisoformat(d)-datetime.date.fromisoformat(x["bandSince"])).days if x.get("bandSince") else 0
    for band,label in (("today","TODAY"),("week","THIS WEEK")):
        rows=sorted([x for x in act if x.get("band")==band],key=lambda r:(r.get("order") is None, r.get("order") or 9999))
        print(f"-- {label} ({len(rows)})")
        for x in rows: print(f"{x.get('order')}|{x.get('area')}|{'◆'*(x.get('score') or 0)}|{x['title'][:80]}|{str(age(x))+'d' if age(x) else ''}|{x.get('due') or ''}|{x['id']}")
    late=[x for x in act if x.get("due") and x["due"]<d and x.get("band")!="today"]
    if late: print(f"-- {len(late)} dated past due outside Today - run tasks-roll")
elif c=="task":
    if len(a)<2: sys.exit('usage: task "<title>" [area] [today|week|month|year]')
    area=a[2] if len(a)>2 else "Real Estate"; band=(a[3] if len(a)>3 else "today").lower()
    if band not in ("today","week","month","year"): sys.exit("band is today|week|month|year")
    import uuid; tid=str(uuid.uuid4())
    def f(d):
        n=max([x.get("order") or 0 for x in d["tasks"] if x.get("status")=="active" and x.get("band")==band]+[0])+1
        d["tasks"].append({"order":n,"top3":False,"id":tid,"title":a[1],"area":area,"priority":"medium","status":"active","difficulty":"medium","due":None,"created":today(),"notes":"","completed":None,"snoozedUntil":None,"band":band,"bandSince":today()}); return d
    print("Done - task",tid[:8],band,jmodify("data/tasks.json",f,f"{AGENT}: task {a[1][:50]}",indent=2))
elif c=="tasks-roll":
    d=today(); dd=datetime.date.fromisoformat(d); we=(dd+datetime.timedelta(days=6-dd.weekday())).isoformat(); me=(dd.replace(day=28)+datetime.timedelta(days=4)).replace(day=1)-datetime.timedelta(days=1); me=me.isoformat()
    moved=[]
    def f(data):
        for t in data["tasks"]:
            if t.get("status")!="active": continue
            to=None; due=t.get("due")
            if not t.get("band"): to="today" if (due and due<=d) else "week" if (due and due<=we) else "month" if (due and due<=me) else "year" if due else "today"
            elif t["band"]!="today" and due and due<=d: to="today"
            elif t["band"]=="month" and due and due<=we: to="week"
            elif t["band"]=="year" and due and due<=me: to="month"
            elif t["band"]=="year" and t.get("snoozedUntil") and t["snoozedUntil"]<=d: to="today"
            if to: moved.append(f"{t['title'][:50]} -> {to}"); t["band"]=to; t["bandSince"]=d; t["order"]=999
        return data
    if not moved: jload("data/tasks.json")
    r=jmodify("data/tasks.json",f,f"{AGENT}: tasks-roll",indent=2) if True else None
    for m in moved: print(" ",m)
    print(f"Done - rolled {len(moved)}",r)
elif c=="tasks-archive":
    cutoff=(datetime.date.fromisoformat(today())-datetime.timedelta(days=7)).isoformat(); yr=today()[:4]; moved=[]
    def f(data):
        keep=[]
        for t in data["tasks"]:
            if t.get("status") in ("done","killed") and (t.get("completed") or "0000")<=cutoff: moved.append(t)
            else: keep.append(t)
        data["tasks"]=keep; return data
    r=jmodify("data/tasks.json",f,f"{AGENT}: tasks-archive {len(moved)}",indent=2)
    if moved:
        def g(arch):
            arch=arch if isinstance(arch,dict) else {"archived":today(),"tasks":[]}; arch["tasks"].extend(moved); arch["archived"]=today(); return arch
        modify(f"data/archive/tasks-done-{yr}.json",lambda t:json.dumps(g(json.loads(t) if t.strip() else {}),indent=2,ensure_ascii=False)+"\n",f"{AGENT}: archive {len(moved)} tasks")
    print(f"Done - archived {len(moved)} (done/killed before {cutoff})",r)
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
    hid=[None]
    def f(h): hid[0]=f"h{len(h)+1:04d}"; h.append({"id":hid[0],"date":today(),"from":AGENT,"to":a[1],"item":a[2],"status":"open"}); return h
    r=jmodify("data/handoffs.json",f,f"{AGENT}: handoff to {a[1]}"); print("Done - handoff",hid[0],r)
elif c=="close-handoff":
    def f(h):
        for x in h:
            if x["id"]==a[1]: x["status"]="done"
        return h
    print("Done - closed",a[1],jmodify("data/handoffs.json",f,f"{AGENT}: close {a[1]}"))
elif c=="log":
    line=json.dumps({"date":today(),"agent":AGENT,"did":a[1],"wrote":(a[2].split(",") if len(a)>2 else [])},ensure_ascii=False)
    print("Done - receipt",modify("data/log.jsonl",lambda t:t.rstrip("\n")+("\n" if t.strip() else "")+line+"\n",f"{AGENT}: receipt"))
elif c=="issue":
    TYPES=("tool","data","rule","access","asked")
    if len(a)<3 or a[1] not in TYPES: sys.exit(f'usage: issue <type> "<what>"  - type is one of: {" | ".join(TYPES)}')
    iid=[None]
    def f(t):
        n=sum(1 for l in t.splitlines() if l.strip()); iid[0]=f"i{n+1:04d}"
        line=json.dumps({"id":iid[0],"date":today(),"agent":AGENT,"type":a[1],"what":a[2],"status":"open"},ensure_ascii=False)
        return t.rstrip("\n")+("\n" if t.strip() else "")+line+"\n"
    r=modify("data/issues.jsonl",f,f"{AGENT}: issue {a[1]}"); print("Done - issue",iid[0],r)
elif c=="issues":
    mode=a[1] if len(a)>1 and a[1] in ("open","all") else "open"; ag=(a[2] if len(a)>2 else (a[1] if len(a)>1 and a[1] not in ("open","all") else None))
    try: rows=[json.loads(l) for l in getfile("data/issues.jsonl")[0].splitlines() if l.strip()]
    except Exception: rows=[]
    rows=[r for r in rows if (mode=="all" or r.get("status")=="open") and (not ag or str(r.get("agent","")).lower()==ag.lower())]
    for r in rows: print(f"{r['id']}|{r['date']}|{r['agent']}|{r['type']}|{r['what']}"+(f"|FIXED {r.get('fixDate')}: {r.get('fix')}" if r.get("status")=="fixed" else ""))
    print(f"-- {sum(1 for r in rows if r.get('status')=='open')} open")
elif c=="fix":
    if len(a)<3: sys.exit('usage: fix <id> "<what changed>"')
    def f(t):
        out=[]; hit=False
        for l in t.splitlines():
            if not l.strip(): continue
            r=json.loads(l)
            if r["id"]==a[1]: r.update({"status":"fixed","fix":a[2],"fixedBy":AGENT,"fixDate":today()}); hit=True
            out.append(json.dumps(r,ensure_ascii=False))
        if not hit: raise SystemExit(f"no issue {a[1]}")
        return "\n".join(out)+"\n"
    print("Done - fixed",a[1],modify("data/issues.jsonl",f,f"{AGENT}: fix {a[1]}"))
elif c=="board":
    d=jload("data/content.json"); st=d.get("stages") or ["idea","hooked","scripted","filmed","edited","scheduled","posted","measured"]
    pipe=[x for x in d.get("pipeline",[]) if x.get("status")!="superseded"]
    only=a[1].lower() if len(a)>1 else None
    if only and only not in st: sys.exit(f"stage must be one of: {' | '.join(st)}")
    print(" ".join(f"{k}:{sum(1 for x in pipe if (x.get('stage') or 'idea')==k)}" for k in st))
    for k in st:
        if only and k!=only: continue
        rows=sorted([x for x in pipe if (x.get("stage") or "idea")==k],key=lambda x:(x.get("boardOrder") if isinstance(x.get("boardOrder"),int) else -1, "~" if isinstance(x.get("boardOrder"),int) else str(x.get("stageDate") or x.get("created") or "")),reverse=False)
        if rows: print(f"-- {k} ({len(rows)})")
        for x in rows: print(f"{x.get('id')}|{str(x.get('title',''))[:60]}|{x.get('series','')}|{x.get('stageDate') or x.get('created') or ''}|{x.get('postDate') or ''}")
elif c=="stage":
    was=[None]
    def f(d):
        st=d.get("stages") or ["idea","hooked","scripted","filmed","edited","scheduled","posted","measured"]
        if len(a)<3 or a[2].lower() not in st: raise SystemExit(f"usage: stage <id> <stage> [postDate]  - stage is one of: {' | '.join(st)}")
        x=next((y for y in d.get("pipeline",[]) if y.get("id")==a[1]),None)
        if not x: raise SystemExit(f"no card with id {a[1]} - run: agentkit.py board")
        was[0]=x.get("stage"); x["stage"]=a[2].lower(); x["stageDate"]=today(); x.pop("boardOrder",None)
        if len(a)>3: x["postDate"]=a[3]
        if x["stage"]=="posted": x["status"]="posted"; x["postDate"]=x.get("postDate") or today()
        return d
    r=jmodify("data/content.json",f,f"{AGENT}: {a[1]} -> {a[2].lower() if len(a)>2 else '?'}",indent=2); print("Done -",a[1],f"{was[0]} -> {a[2].lower()}",r)
elif c=="card":
    def flags(args):
        f={}; i=0
        while i<len(args):
            if args[i].startswith("--") and i+1<len(args): f[args[i][2:]]=args[i+1]; i+=2
            else: i+=1
        return f
    STATUS={"idea":"template","hooked":"drafted","posted":"posted"}; sub=a[1] if len(a)>1 else ""; made=[None]
    if sub=="add":
        if len(a)<3: sys.exit('usage: card add "<title>" --stage <stage> --series "<series>" [--hook "..."] [--post YYYY-MM-DD] [--notes "..."]')
        f=flags(a[3:]); stg=f.get("stage","idea").lower()
        def add(d):
            st=d.get("stages") or ["idea","hooked","scripted","filmed","edited","scheduled","posted","measured"]
            if stg not in st: raise SystemExit(f"stage must be one of: {' | '.join(st)}")
            n=max([int(re.sub(r"\D","",x.get("id","")) or 0) for x in d.get("pipeline",[])]+[0])+1
            x={"id":f"c{n}","title":a[2],"series":f.get("series",""),"status":STATUS.get(stg,"scripted"),"priority":"medium","created":today(),"postDate":f.get("post") or None,"hook":f.get("hook",""),"notes":f.get("notes",""),"stage":stg,"stageDate":today()}
            if stg=="posted" and not x["postDate"]: x["postDate"]=today()
            d.setdefault("pipeline",[]).append(x); made[0]=x["id"]; return d
        r=jmodify("data/content.json",add,f"{AGENT}: card add",indent=2); print("Done -",made[0],stg,r)
    elif sub=="edit":
        if len(a)<3: sys.exit('usage: card edit <id> [--title "..."] [--hook "..."] [--series "..."] [--post YYYY-MM-DD] [--notes "..."]')
        f=flags(a[3:]); ch=[]
        def ed(d):
            x=next((y for y in d.get("pipeline",[]) if y.get("id")==a[2]),None)
            if not x: raise SystemExit(f"no card with id {a[2]} - run: agentkit.py board")
            for k,fld in (("title","title"),("hook","hook"),("series","series"),("post","postDate"),("notes","notes")):
                if k in f: x[fld]=f[k]; ch.append(fld)
            if not ch: raise SystemExit("nothing to change - pass --title/--hook/--series/--post/--notes")
            return d
        r=jmodify("data/content.json",ed,f"{AGENT}: card edit {a[2]}",indent=2); print("Done -",a[2],"edited",",".join(ch),r)
    else: sys.exit("usage: card add ... | card edit <id> ...")
elif c=="state":
    ag=(a[1] if len(a)>1 else AGENT).lower().replace(" ","")
    names={"pa":"core","personalassistant":"core","max":"core","claudemanager":"manager","lifecoach":"private:personal/state/lifecoach.md"}
    p=names.get(ag,ag); p=p if p.startswith("private:") else f"data/state/{p}.md"
    print(getfile(p)[0])
else: print("unknown command"); print(__doc__)
