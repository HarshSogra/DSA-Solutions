#!/usr/bin/env python3
"""Sync accepted LeetCode submissions and regenerate repository progress."""
from __future__ import annotations
import json, os, re, sys
from collections import Counter
from pathlib import Path
from urllib import request

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
REGISTRY = DATA / "problems.json"
SYNC_STATE = DATA / "leetcode_sync.json"
LEETCODE_USERNAME = os.getenv("LEETCODE_USERNAME", "HarshSogra") or "HarshSogra"
SESSION = os.getenv("LEETCODE_SESSION", "").strip()
CSRF = os.getenv("LEETCODE_CSRF_TOKEN", "").strip()
CF_CLEARANCE = os.getenv("LEETCODE_CF_CLEARANCE", "").strip()
API = "https://leetcode.com/graphql/"

RECENT_QUERY = """
query recentAcSubmissions($username: String!, $limit: Int!) {
  recentAcSubmissionList(username: $username, limit: $limit) { id title titleSlug timestamp }
}
"""
DETAIL_QUERY = """
query submissionDetails($submissionId: Int!) {
  submissionDetails(submissionId: $submissionId) {
    code timestamp statusCode lang { name verboseName }
    question { questionFrontendId title titleSlug difficulty topicTags { name slug } }
  }
}
"""

TOPIC_FOLDERS = [
    ("Array", "01-Arrays"), ("String", "02-Strings"), ("Hash Table", "03-Hashing"),
    ("Two Pointers", "04-Two-Pointers"), ("Sliding Window", "05-Sliding-Window"),
    ("Binary Search", "06-Binary-Search"), ("Linked List", "07-Linked-List"),
    ("Stack", "08-Stack"), ("Queue", "09-Queue"), ("Recursion", "10-Recursion"),
    ("Backtracking", "11-Backtracking"), ("Tree", "12-Trees"),
    ("Binary Search Tree", "13-BST"), ("Heap", "14-Heap"), ("Priority Queue", "14-Heap"),
    ("Greedy", "15-Greedy"), ("Graph", "16-Graphs"),
    ("Breadth-First Search", "16-Graphs"), ("Depth-First Search", "16-Graphs"),
    ("Dynamic Programming", "17-Dynamic-Programming"), ("Trie", "18-Tries"),
]
FOLDER_TARGETS = {
    "01-Arrays":30,"02-Strings":20,"03-Hashing":20,"04-Two-Pointers":15,"05-Sliding-Window":15,
    "06-Binary-Search":20,"07-Linked-List":20,"08-Stack":15,"09-Queue":10,"10-Recursion":15,
    "11-Backtracking":15,"12-Trees":30,"13-BST":15,"14-Heap":15,"15-Greedy":15,"16-Graphs":30,
    "17-Dynamic-Programming":40,"18-Tries":10,
}
LANG_EXT = {
    "python":"py","python3":"py","cpp":"cpp","c++":"cpp","java":"java","javascript":"js",
    "typescript":"ts","c":"c","c#":"cs","csharp":"cs","golang":"go","go":"go","rust":"rs",
    "kotlin":"kt","swift":"swift","ruby":"rb","php":"php","scala":"scala","mysql":"sql",
    "mssql":"sql","postgresql":"sql",
}

def slugify(value: str) -> str:
    return re.sub(r"[^a-zA-Z0-9]+", "-", value).strip("-").lower() or "problem"

def load_json(path: Path, default):
    if not path.exists(): return default
    try: return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError: return default

def save_json(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

def graphql(query: str, variables: dict) -> dict:
    if not SESSION: raise RuntimeError("LEETCODE_SESSION is not configured.")
    cookies = [f"LEETCODE_SESSION={SESSION}"]
    if CSRF: cookies.append(f"csrftoken={CSRF}")
    if CF_CLEARANCE: cookies.append(f"cf_clearance={CF_CLEARANCE}")
    payload = json.dumps({"query":query,"variables":variables}).encode()
    headers = {"Content-Type":"application/json","Accept":"application/json","User-Agent":"Mozilla/5.0 (compatible; DSA-Solutions-LeetCode-Sync/1.0)","Referer":"https://leetcode.com/","Origin":"https://leetcode.com","Cookie":"; ".join(cookies)}
    try:
        req = request.Request(API, data=payload, headers=headers, method="POST")
        with request.urlopen(req, timeout=30) as response: body = json.loads(response.read().decode("utf-8"))
    except Exception as exc: raise RuntimeError(f"LeetCode GraphQL request failed: {exc}") from exc
    if body.get("errors"): raise RuntimeError(f"LeetCode GraphQL error: {body['errors']}")
    return body.get("data") or {}

def choose_folder(tags: list[dict]) -> str:
    names = {str(t.get("name","")).lower() for t in tags}
    for tag_name, folder in TOPIC_FOLDERS:
        if tag_name.lower() in names: return folder
    return "01-Arrays"

def write_problem(detail: dict) -> tuple[Path, Path]:
    q = detail["question"]; title=q["title"]; number=str(q.get("questionFrontendId") or ""); slug=q["titleSlug"]; tags=q.get("topicTags") or []
    folder=choose_folder(tags)
    problem_dir=ROOT/folder/(f"{number.zfill(4)}-{slugify(title)}" if number.isdigit() else slugify(title)); problem_dir.mkdir(parents=True,exist_ok=True)
    lang_name=(detail.get("lang") or {}).get("name","unknown"); ext=LANG_EXT.get(lang_name.lower(),"txt")
    solution_path=problem_dir/f"solution.{ext}"; solution_path.write_text(detail.get("code") or "",encoding="utf-8")
    tag_text=", ".join(t.get("name","") for t in tags) or "Not specified"; lc_url=f"https://leetcode.com/problems/{slug}/"
    readme_path=problem_dir/"README.md"
    readme_path.write_text(f"# {number}. {title}\n\n| Field | Value |\n|---|---|\n| Platform | LeetCode |\n| Difficulty | {q.get('difficulty','Unknown')} |\n| Language | {lang_name} |\n| Topics | {tag_text} |\n| Problem | [{title}]({lc_url}) |\n\n## Approach\n\nThis solution was synced automatically from my accepted LeetCode submission.\n\n## Complexity\n\n- Time: _To be documented_\n- Space: _To be documented_\n\n## Key Takeaway\n\n_Add the main insight/pattern after reviewing the solution._\n",encoding="utf-8")
    return solution_path, readme_path

def progress_data(registry: dict):
    entries=list(registry.values())
    difficulty=Counter(str(x.get("difficulty","Unknown")).upper() for x in entries)
    topic=Counter(x.get("folder","") for x in entries)
    patterns=Counter(tag for x in entries for tag in (x.get("tags") or []) if tag)
    return entries, difficulty, topic, patterns

def update_progress(registry: dict) -> None:
    entries,difficulty,topic,patterns=progress_data(registry)
    lines=["# 📊 DSA Progress Tracker","","This file is **updated automatically** by the LeetCode sync workflow. Do not edit the generated numbers manually.","","## Overall Progress","","| Metric | Count |","|---|---:|",f"| Problems Solved | {len(entries)} |",f"| Easy | {difficulty['EASY']} |",f"| Medium | {difficulty['MEDIUM']} |",f"| Hard | {difficulty['HARD']} |",f"| Patterns Practiced | {len(patterns)} |","| Patterns Mastered | _Manual review_ |"]
    lines += ["","## Topic Progress","","| Topic | Solved | Target | Progress |","|---|---:|---:|---:|"]
    for folder,target in FOLDER_TARGETS.items():
        count=topic[folder]; pct=min(100,round(count/target*100)) if target else 0; label=folder.split("-",1)[1].replace("-"," ")
        lines.append(f"| {label} | {count} | {target} | {pct}% |")
    lines += ["","## Pattern Progress","","These counts include **all LeetCode tags**, even when a problem is stored in another primary topic folder.","","| Pattern | Problems |","|---|---:|"]
    for pattern,count in sorted(patterns.items(),key=lambda x:(-x[1],x[0].lower())): lines.append(f"| {pattern} | {count} |")
    lines += ["","## Recent Synced Problems","","| # | Problem | Difficulty | Language |","|---:|---|---|---|"]
    for x in sorted(entries,key=lambda x:int(x.get("timestamp",0)),reverse=True)[:20]: lines.append(f"| {x.get('number','')} | [{x['title']}]({x['path']}) | {x.get('difficulty','')} | {x.get('language','')} |")
    lines += ["","## Notes","","- **Problems Solved, difficulty, topics, and pattern counts are automatic.**","- **Patterns Mastered is intentionally manual**: syncing a tag does not prove mastery.","- Review each problem README and add your own approach/complexity notes when useful.",""]
    (ROOT/"PROGRESS.md").write_text("\n".join(lines),encoding="utf-8")

def update_readme(registry: dict) -> None:
    path = ROOT / "README.md"
    if not path.exists(): return
    text = path.read_text(encoding="utf-8")
    entries,difficulty,topic,patterns=progress_data(registry)
    current = """<!-- AUTO-PROGRESS:START -->
| Metric | Count |
|---|---:|
| Problems Solved | **{total}** |
| Easy | {easy} |
| Medium | {medium} |
| Hard | {hard} |
| Patterns Practiced | {pattern_count} |
| Patterns Mastered | _Manual review_ |
<!-- AUTO-PROGRESS:END -->""".format(total=len(entries),easy=difficulty["EASY"],medium=difficulty["MEDIUM"],hard=difficulty["HARD"],pattern_count=len(patterns))
    if "<!-- AUTO-PROGRESS:START -->" in text and "<!-- AUTO-PROGRESS:END -->" in text:
        text = re.sub(r"<!-- AUTO-PROGRESS:START -->.*?<!-- AUTO-PROGRESS:END -->", current, text, flags=re.S)
    else:
        section = "## 📊 Current Progress\n\n" + current + "\n\nDetailed tracking: **[PROGRESS.md](PROGRESS.md)**"
        text = re.sub(r"## 📊 Current Progress\n.*?(?=\n## )", section + "\n\n", text, flags=re.S)
    # Keep topic statuses aligned with the synced primary folders.
    def topic_status(folder):
        count = topic[folder]; target = FOLDER_TARGETS[folder]
        if count >= target: return "🟢 Complete"
        if count > 0: return "🟡 In Progress"
        return "⬜ Not Started"
    for folder,target in FOLDER_TARGETS.items():
        label=folder.split("-",1)[1].replace("-"," ")
        pattern = rf"(\| \d{{2}} \| {re.escape(label)} \| {target} \| )[^|]+( \|)"
        text = re.sub(pattern, rf"\g<1>{topic_status(folder)}\g<2>", text)
    path.write_text(text, encoding="utf-8")

def main() -> int:
    registry=load_json(REGISTRY,{ }); state=load_json(SYNC_STATE,{"submission_ids":[]}); seen={str(x) for x in state.get("submission_ids",[])}
    recent=graphql(RECENT_QUERY,{"username":LEETCODE_USERNAME,"limit":20}).get("recentAcSubmissionList") or []
    if not recent: print(f"No recent accepted submissions found for @{LEETCODE_USERNAME}."); return 0
    changed=0
    for submission in sorted(recent,key=lambda x:int(x.get("timestamp",0))):
        sid=str(submission["id"])
        if sid in seen: continue
        detail=graphql(DETAIL_QUERY,{"submissionId":int(sid)}).get("submissionDetails")
        if not detail or not detail.get("code") or not detail.get("question"): print(f"Skipping submission {sid}: details/code unavailable."); continue
        solution_path,_=write_problem(detail); q=detail["question"]
        entry={"submission_id":sid,"title":q["title"],"title_slug":q["titleSlug"],"number":q.get("questionFrontendId",""),"difficulty":q.get("difficulty","Unknown"),"language":(detail.get("lang") or {}).get("verboseName") or (detail.get("lang") or {}).get("name","Unknown"),"tags":[t.get("name") for t in q.get("topicTags") or []],"folder":str(solution_path.parent.relative_to(ROOT)).split("/")[0],"path":str(solution_path.relative_to(ROOT)).replace("\\","/"),"timestamp":int(detail.get("timestamp") or submission.get("timestamp") or 0),"leetcode_url":f"https://leetcode.com/problems/{q['titleSlug']}/"}
        registry[q["titleSlug"]]=entry; seen.add(sid); changed+=1; print(f"Synced: {q.get('questionFrontendId','')}. {q['title']} [{entry['language']}]")
    save_json(REGISTRY,registry); save_json(SYNC_STATE,{"submission_ids":sorted(seen,key=int)[-500:]}); update_progress(registry); update_readme(registry); print(f"Done. New accepted submissions synced: {changed}"); return 0

if __name__ == "__main__":
    try: raise SystemExit(main())
    except Exception as exc: print(f"ERROR: {exc}",file=sys.stderr); raise SystemExit(1)
