#!/usr/bin/env python3
"""One-time migration for the Today page (spec tools/specs/2026-09-28-today-page.md, section 3).
Reads a tasks.json, writes tasks.json (live only, with band/bandSince) and an archive of done tasks.
Usage: python3 migrate-tasks-2026-09-28.py <in tasks.json> <out tasks.json> <out archive.json> [YYYY-MM-DD]
"""
import json, sys, datetime as dt

src, out_tasks, out_arch = sys.argv[1], sys.argv[2], sys.argv[3]
today = dt.date.fromisoformat(sys.argv[4]) if len(sys.argv) > 4 else dt.date.today()
week_end = today + dt.timedelta(days=6 - today.weekday())          # Sunday of this ISO week
month_end = (today.replace(day=28) + dt.timedelta(days=4)).replace(day=1) - dt.timedelta(days=1)

PERSONAL = ("tal", "baby", "boxing", "boxica", "gym", "ice bath", "doctor", "dentist", "visa", "car ",
            "family", "birthday", "home ", "flat", "sleep", "whoop", "coach", "health", "holiday",
            "email clean", "apps tidy", "files into", "calendar", "sunday am")

def d(s):
    try: return dt.date.fromisoformat(str(s)[:10])
    except Exception: return None

data = json.load(open(src))
tasks = data["tasks"]
live, done, mapping = [], [], []
for t in tasks:
    if t.get("status") in ("done", "killed"):
        done.append(t); continue
    due, created, snz = d(t.get("due")), d(t.get("created")), d(t.get("snoozedUntil"))
    if snz and snz > today:        band = "year"
    elif due and due <= today:     band = "today"
    elif due and due <= week_end:  band = "week"
    elif due and due <= month_end: band = "month"
    elif due:                      band = "year"
    elif created and (today - created).days <= 7: band = "today"
    else:                          band = "month"
    t["band"], t["bandSince"] = band, today.isoformat()
    if t.get("area") == "Tasks":
        new = "Personal" if any(k in t.get("title", "").lower() for k in PERSONAL) else "Real Estate"
        mapping.append(f"  {t['title'][:50]!r}: Tasks -> {new}")
        t["area"] = new
    live.append(t)

# order: top3 first (1-3), then existing order, within each band
for band in ("today", "week", "month", "year"):
    rows = [t for t in live if t["band"] == band]
    rows.sort(key=lambda t: (0 if t.get("top3") else 1, t.get("order") or 999))
    for i, t in enumerate(rows, 1): t["order"] = i

data["tasks"] = live
json.dump(data, open(out_tasks, "w"), indent=2, ensure_ascii=False); open(out_tasks, "a").write("\n")
json.dump({"archived": today.isoformat(), "tasks": done}, open(out_arch, "w"), indent=2, ensure_ascii=False); open(out_arch, "a").write("\n")

from collections import Counter
print(f"in: {len(tasks)} tasks -> live {len(live)}, archived {len(done)}")
print("bands:", dict(Counter(t['band'] for t in live)))
print("areas:", dict(Counter(t['area'] for t in live)))
print("area mapping (Tasks ->):"); print("\n".join(mapping) or "  none")
