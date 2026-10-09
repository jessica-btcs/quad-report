#!/usr/bin/env python3
"""Quad Report data folder: the member's profile and month-by-month history.

The skill (this folder) is replaced on every update. The data folder is the
member's own, in their own OneDrive / Google Drive / SharePoint, and nothing
in an update ever touches it. This script is the only thing that writes
history, so the rules live in one place.

    python3 quad_data.py init     <data_dir>
    python3 quad_data.py status   <data_dir> [--check-updates] [--period YYYY-MM]
    python3 quad_data.py annotate <data_dir> <config.json>
    python3 quad_data.py archive  <data_dir> <config.json> [--run run.json] [--replace]

Every command prints JSON on stdout. Needs only the standard library.
"""
import json, os, re, sys, shutil
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
PROFILE = "quad-profile.json"
PROFILE_SCHEMA_VERSION = 1
HISTORY_SCHEMA_VERSION = 1
MONTHS = ["january","february","march","april","may","june","july",
          "august","september","october","november","december"]

# Fields each profile schema version requires. When a release adds a field,
# bump PROFILE_SCHEMA_VERSION, add an entry here with the question to ask,
# and the next run asks the member for only that field.
MIGRATIONS = {
    1: [
        ("company.name",               "What is the company called?"),
        ("company.report_by",          "Whose name goes on the report?"),
        ("company.fiscal_year_start_month", "Which month does your fiscal year start (1 to 12)?"),
        ("meeting.weekday",            "Which weekday is your group meeting?"),
        ("meeting.week_of_month",      "Which week of the month (1 to 4, or 'last')?"),
        ("billing_models",             "Which billing models do you use?"),
        ("revenue_basis",              "Revenue basis: earned, invoiced or collected?"),
        ("books.platform",             "Which accounting system, or 'upload'?"),
        ("books.salaried_delivery_in", "Where does salaried delivery pay sit: cost of sales or operating expenses?"),
        ("time_system.platform",       "Where do hours live, or 'none'?"),
        ("kpis",                       "Your KPIs, each with a target and the basis it was set on."),
        ("goals",                      "Your goals for this year, word for word from your planning deck."),
        ("strategies",                 "Your core strategies, up to six, each an action ending in -ing."),
        ("output.labels",              "Plain English or the classic wording?"),
        ("output.period",              "Report the month or a rolling quarter?"),
    ],
}


def out(obj, code=0):
    print(json.dumps(obj, indent=2, ensure_ascii=False))
    sys.exit(code)


def skill_version():
    try:
        return open(os.path.join(HERE, "VERSION"), encoding="utf-8").read().strip()
    except OSError:
        return "unknown"


def load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def save(path, obj):
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2, ensure_ascii=False)
        f.write("\n")
    os.replace(tmp, path)


def get_path(obj, dotted):
    for part in dotted.split("."):
        if not isinstance(obj, dict) or part not in obj:
            return None
        obj = obj[part]
    return obj


def period_key(cfg):
    """'2026-09' from config.period_key, or from a period like 'September 2026'."""
    if cfg.get("period_key"):
        return cfg["period_key"]
    m = re.search(r"([A-Za-z]+)\s+(\d{4})", cfg.get("period", ""))
    if m and m.group(1).lower() in MONTHS:
        return f"{m.group(2)}-{MONTHS.index(m.group(1).lower()) + 1:02d}"
    m = re.search(r"(\d{4})-(\d{2})", cfg.get("period", ""))
    if m:
        return f"{m.group(1)}-{m.group(2)}"
    return None


def history(data_dir):
    """Archived months, oldest first, as (key, config). Reads pre-release files
       (a bare config) as well as current ones ({schema_version, config, ...})."""
    hdir = os.path.join(data_dir, "history")
    rows = []
    if not os.path.isdir(hdir):
        return rows
    for name in sorted(os.listdir(hdir)):
        m = re.fullmatch(r"(\d{4}-\d{2})\.json", name)
        if not m:
            continue
        rec = load(os.path.join(hdir, name))
        rows.append((m.group(1), rec.get("config", rec) if "schema_version" in rec else rec))
    return rows


def next_month(key):
    y, m = map(int, key.split("-"))
    return f"{y + (m == 12)}-{m % 12 + 1:02d}"


# ---------- commands ----------

def cmd_init(data_dir):
    made = []
    for sub in ("", "history", "out", "issues", "templates"):
        p = os.path.join(data_dir, sub)
        if not os.path.isdir(p):
            os.makedirs(p)
            made.append(sub or ".")
    readme = os.path.join(data_dir, "README.md")
    if not os.path.exists(readme):
        shutil.copy(os.path.join(HERE, "data-folder-README.md"), readme)
        made.append("README.md")
    out({"ok": True, "data_dir": os.path.abspath(data_dir), "created": made})


def annual_review_due(prof, period):
    """Goals, core strategies, theme and KPI targets are set once a year. Due
       when they have never been dated, or were last set before the start of
       the fiscal year that `period` falls in."""
    set_on = prof.get("plan_set")
    if not set_on:
        return True
    fsm = get_path(prof, "company.fiscal_year_start_month") or 1
    y, m = map(int, period.split("-"))
    fy_start = f"{y if m >= fsm else y - 1}-{int(fsm):02d}"
    return set_on < fy_start


def cmd_status(data_dir, check_updates=False, period=None):
    res = {"skill_version": skill_version(), "data_dir": os.path.abspath(data_dir)}
    try:
        import pptx  # noqa: F401
        res["python_pptx"] = True
    except ImportError:
        res["python_pptx"] = False
    try:
        import docx  # noqa: F401
        res["python_docx"] = True
    except ImportError:
        res["python_docx"] = False
    res["data_dir_exists"] = os.path.isdir(data_dir)
    ppath = os.path.join(data_dir, PROFILE)
    res["profile_found"] = os.path.exists(ppath)
    if res["profile_found"]:
        prof = load(ppath)
        v = prof.get("schema_version", 0)
        res["profile_schema_version"] = v
        missing = []
        for ver in range(1, PROFILE_SCHEMA_VERSION + 1):
            for field, question in MIGRATIONS.get(ver, []):
                if get_path(prof, field) in (None, "", []):
                    missing.append({"field": field, "ask": question})
        res["missing_fields"] = missing
        res["needs_migration"] = v < PROFILE_SCHEMA_VERSION or bool(missing)
    tdir = os.path.join(data_dir, "templates")
    res["issue_form"] = None
    if os.path.isdir(tdir):
        res["issue_form"] = next((os.path.join(tdir, f) for f in sorted(os.listdir(tdir))
                                  if f.lower().endswith(".docx") and "issue" in f.lower()), None)
    hist = history(data_dir)
    res["months_on_file"] = [k for k, _ in hist]
    res["last_month"] = hist[-1][0] if hist else None
    res["suggested_period"] = next_month(hist[-1][0]) if hist else None
    if res["profile_found"]:
        res["annual_review_due"] = annual_review_due(
            prof, period or res["suggested_period"] or datetime.now().strftime("%Y-%m"))
    if check_updates:
        res["update"] = update_check()
    out(res)


def update_check():
    """GET a public version.json. Sends nothing about the member. Silent on
       failure, because sandboxes (ChatGPT, claude.ai) often have no internet."""
    try:
        url = open(os.path.join(HERE, "update-url.txt"), encoding="utf-8").read().strip()
    except OSError:
        return {"checked": False, "reason": "no update address in this build"}
    try:
        from urllib.request import urlopen
        with urlopen(url, timeout=5) as r:
            latest = json.loads(r.read().decode("utf-8"))
    except Exception as e:  # noqa: BLE001
        return {"checked": False, "reason": f"could not reach the update address ({type(e).__name__})"}
    mine = skill_version()

    def tup(v):
        return tuple(int(x) for x in re.findall(r"\d+", v)[:3]) if v else ()
    return {"checked": True, "installed": mine, "latest": latest.get("version"),
            "available": tup(latest.get("version", "")) > tup(mine),
            "notes": latest.get("notes", "")}


def cmd_annotate(data_dir, cfg_path):
    """Write trend and stalled flags into the config from history, so neither
       is ever eyeballed. Trend: direction vs last month, and how many months
       running. Stalled: a goal or strategy whose text and status have not
       changed for two months or more."""
    cfg = load(cfg_path)
    key = period_key(cfg)
    if not key:
        out({"ok": False, "error": "config has no period like 'September 2026' or period_key '2026-09'"}, 1)
    prior = [(k, c) for k, c in history(data_dir) if k < key]
    notes = []

    for k in cfg.get("kpis", []):
        series = []
        for _, c in prior:
            match = next((x for x in c.get("kpis", []) if x.get("name") == k.get("name")), None)
            series.append(match.get("actual") if match else None)
        series.append(k.get("actual"))
        if len(series) < 2 or series[-1] is None or series[-2] is None:
            continue
        def d(a, b):
            if a is None or b is None:
                return None
            tol = abs(b) * 0.01 if b else 0
            return "flat" if abs(a - b) <= tol else ("up" if a > b else "down")
        cur = d(series[-1], series[-2])
        run = 1
        i = len(series) - 2
        while i >= 1 and d(series[i], series[i - 1]) == cur:
            run += 1
            i -= 1
        word = {"up": "rising", "down": "falling", "flat": "steady"}[cur]
        k["trend"] = {"direction": cur, "label": word, **({"months": run} if run >= 2 else {})}
        notes.append(f"{k['name']}: {word}" + (f" {run} months" if run >= 2 else ""))

    def sig_goal(g):
        return json.dumps([g.get("theme") or g.get("goal"), g.get("bullets"), g.get("status")], sort_keys=True)

    def sig_strat(s):
        return s if isinstance(s, str) else s.get("text", "")

    for g in cfg.get("breakthrough_goals", []):
        if g.get("flag") in ("done", "closed"):
            continue
        name = g.get("theme") or g.get("goal")
        months = 1
        for _, c in reversed(prior):
            old = next((x for x in c.get("breakthrough_goals", []) if (x.get("theme") or x.get("goal")) == name), None)
            if old and sig_goal(old) == sig_goal(g):
                months += 1
            else:
                break
        if months >= 3:  # unchanged across this month and the two before = no change for 2+ months
            g["flag"], g["stalled_months"] = "stalled", months - 1
            notes.append(f"goal '{name}': stuck {months - 1} months")
        elif g.get("flag") == "stalled":
            g["flag"], g["stalled_months"] = None, None

    shortfalls = " ".join((cfg.get("strategy_status") or {}).get("shortfalls") or []).lower()
    for s in cfg.get("core_strategies", []):
        if isinstance(s, str):
            continue
        text = sig_strat(s)
        months = 1
        for _, c in reversed(prior):
            old = next((x for x in c.get("core_strategies", []) if sig_strat(x) == text), None)
            if old and isinstance(old, dict) and old.get("flag") == "stalled":
                months += 1
            else:
                break
        # A strategy is only marked stalled by the run itself; this keeps it
        # marked and counts how long. It never invents a stall.
        if s.get("flag") == "stalled" and months >= 2:
            notes.append(f"strategy '{text}': stuck {months} months")

    save(cfg_path, cfg)
    out({"ok": True, "period_key": key, "months_of_history_used": len(prior), "notes": notes})


def cmd_archive(data_dir, cfg_path, run_path=None, replace=False):
    cfg = load(cfg_path)
    key = period_key(cfg)
    if not key:
        out({"ok": False, "error": "config has no period like 'September 2026' or period_key '2026-09'"}, 1)
    hdir = os.path.join(data_dir, "history")
    os.makedirs(hdir, exist_ok=True)
    dest = os.path.join(hdir, f"{key}.json")
    if os.path.exists(dest) and not replace:
        out({"ok": False, "error": f"{key} is already archived. That file is the record of what was "
             "reported. Ask the owner before replacing it, then re-run with --replace.",
             "existing": dest}, 2)
    kept = None
    if os.path.exists(dest):
        stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        kept = os.path.join(hdir, f"{key}.replaced-{stamp}.json")
        os.replace(dest, kept)
    rec = {
        "schema_version": HISTORY_SCHEMA_VERSION,
        "skill_version": skill_version(),
        "period_key": key,
        "archived_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "config": cfg,
        "run": load(run_path) if run_path else {},
    }
    save(dest, rec)
    out({"ok": True, "archived": dest, "previous_version_kept_as": kept})


def main(argv):
    if len(argv) < 3:
        sys.exit(__doc__)
    cmd, data_dir, rest = argv[1], argv[2], argv[3:]
    flags = {a for a in rest if a.startswith("--")}
    pos = [a for a in rest if not a.startswith("--")]
    if cmd == "init":
        cmd_init(data_dir)
    elif cmd == "status":
        per = rest[rest.index("--period") + 1] if "--period" in rest else None
        cmd_status(data_dir, "--check-updates" in flags, per)
    elif cmd == "annotate" and pos:
        cmd_annotate(data_dir, pos[0])
    elif cmd == "archive" and pos:
        run = None
        if "--run" in rest:
            run = rest[rest.index("--run") + 1]
            pos = [p for p in pos if p != run]
        cmd_archive(data_dir, pos[0], run, "--replace" in flags)
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main(sys.argv)
