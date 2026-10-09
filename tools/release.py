#!/usr/bin/env python3
"""Build a Quad Report release from the one source folder.

    python tools/release.py            check, test, and build dist/v<VERSION>/
    python tools/release.py --bump minor   bump VERSION first (patch | minor | major)

The skill in plugins/quad-report/skills/quad-report/ is the single source.
Everything in dist/ is generated from it, so the platforms never drift apart:

    dist/v1.0.0/
      claude-plugin/        nothing to upload; members get it from the GitHub marketplace
      claude-ai/            quad-report-skill-v1.0.0.zip   (Settings > upload a skill)
      chatgpt/              instructions.md + knowledge/   (paste into the shared GPT)
      copilot/              instructions.md + knowledge/ + blank template
      member/               Quad-Report-Data-starter.zip + the quickstart
      RELEASE-NOTES.md      the CHANGELOG entry, for the release email
"""
import json, os, re, shutil, subprocess, sys, tempfile, zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILL = os.path.join(ROOT, "plugins", "quad-report", "skills", "quad-report")
SKIP = {"__pycache__", "update-url.txt.example"}


def die(msg):
    sys.exit(f"\nRelease stopped: {msg}\n")


def rd(p):
    with open(p, encoding="utf-8") as f:
        return f.read()


def wr(p, s):
    with open(p, "w", encoding="utf-8") as f:
        f.write(s)


def skill_files():
    for base, dirs, files in os.walk(SKILL):
        dirs[:] = [d for d in dirs if d not in SKIP]
        for f in files:
            if f not in SKIP and not f.endswith((".pyc", ".tmp")):
                full = os.path.join(base, f)
                yield full, os.path.relpath(full, SKILL)


def bump(kind):
    v = [int(x) for x in rd(os.path.join(SKILL, "VERSION")).strip().split(".")]
    i = {"major": 0, "minor": 1, "patch": 2}[kind]
    v[i] += 1
    v[i + 1:] = [0] * (2 - i)
    wr(os.path.join(SKILL, "VERSION"), ".".join(map(str, v)) + "\n")


def changelog_entry(version):
    m = re.search(rf"^## {re.escape(version)}\b.*?$(.*?)(?=^## |\Z)", rd(os.path.join(ROOT, "CHANGELOG.md")), re.M | re.S)
    if not m or not m.group(1).strip():
        die(f"CHANGELOG.md has no entry for {version}. Write what changed, for the owner, then run again.")
    return m.group(1).strip()


def sync_versions(version, rel):
    pj = os.path.join(ROOT, "plugins", "quad-report", ".claude-plugin", "plugin.json")
    mj = os.path.join(ROOT, ".claude-plugin", "marketplace.json")
    p = json.loads(rd(pj)); p["version"] = version; wr(pj, json.dumps(p, indent=2) + "\n")
    m = json.loads(rd(mj))
    for pl in m["plugins"]:
        if pl["name"] == "quad-report":
            pl["version"] = version
    wr(mj, json.dumps(m, indent=2) + "\n")
    url_file = os.path.join(SKILL, "update-url.txt")
    if rel.get("github_repo"):
        url = f"https://raw.githubusercontent.com/{rel['github_repo']}/{rel.get('branch', 'main')}/version.json"
        wr(url_file, url + "\n")
        return url
    if os.path.exists(url_file):
        os.remove(url_file)
    return None


def clear(path):
    """Remove an old build. OneDrive can hold a folder open while it syncs, so
       retry, then move it aside rather than fail the release."""
    import time
    for _ in range(5):
        if not os.path.exists(path):
            return
        try:
            shutil.rmtree(path)
            return
        except PermissionError:
            time.sleep(2)
    aside = f"{path}.old-{int(time.time())}"
    os.replace(path, aside)
    print(f"  (OneDrive was holding the old build; moved it to {os.path.basename(aside)}, delete it when you like)")


def zip_dir(src_pairs, dest, prefix):
    with zipfile.ZipFile(dest, "w", zipfile.ZIP_DEFLATED) as z:
        for full, rel in src_pairs:
            z.write(full, os.path.join(prefix, rel).replace(os.sep, "/"))


def main():
    if "--bump" in sys.argv:
        bump(sys.argv[sys.argv.index("--bump") + 1])
    version = rd(os.path.join(SKILL, "VERSION")).strip()
    if not re.fullmatch(r"\d+\.\d+\.\d+", version):
        die(f"VERSION is '{version}', expected something like 1.2.0")
    rel = json.loads(rd(os.path.join(ROOT, "release.json")))
    notes = changelog_entry(version)
    url = sync_versions(version, rel)

    print(f"Testing v{version} ...")
    t = subprocess.run([sys.executable, "-m", "unittest", "discover", "-s", os.path.join(ROOT, "tests")],
                       capture_output=True, text=True)
    if t.returncode:
        print(t.stderr)
        die("tests failed. Nothing was built.")

    dist = os.path.join(ROOT, "dist", f"v{version}")
    clear(dist)
    files = list(skill_files())

    # Claude plugin: served straight from the repo, nothing to package.
    os.makedirs(os.path.join(dist, "claude-plugin"))
    wr(os.path.join(dist, "claude-plugin", "README.md"),
       "Nothing to upload. Commit, tag and push; members get it from the GitHub marketplace.\n")

    # claude.ai: an uploadable skill zip with the skill folder at its root.
    os.makedirs(os.path.join(dist, "claude-ai"))
    zip_dir(files, os.path.join(dist, "claude-ai", f"quad-report-skill-v{version}.zip"), "quad-report")

    # ChatGPT and Copilot: instructions plus a flat knowledge folder.
    for plat in ("chatgpt", "copilot"):
        k = os.path.join(dist, plat, "knowledge")
        os.makedirs(k)
        for full, rel_path in files:
            name = os.path.basename(rel_path)
            if os.path.exists(os.path.join(k, name)):
                die(f"two skill files are both called {name}; the flat {plat} knowledge folder needs unique names")
            shutil.copy(full, os.path.join(k, name))
        shutil.copy(os.path.join(ROOT, "platforms", plat, "instructions.md"), os.path.join(dist, plat))
        if len(rd(os.path.join(ROOT, "platforms", plat, "instructions.md"))) > 7500:
            die(f"platforms/{plat}/instructions.md is over 7,500 characters; GPT and Copilot agents cap instructions near 8,000")

    # Copilot gets a blank slide to type into, since it cannot run the generator.
    blank = json.loads(rd(os.path.join(SKILL, "examples", "sample-config.json")))
    blank.update({"theme": "", "report_by": "", "period": "", "date": "", "vision": "", "label_overrides": {}})
    for k in blank["kpis"]:
        k.update({"actual": None, "target": None, "status": "", "trend": {}})
    blank["breakthrough_goals"], blank["core_strategies"] = [], []
    blank["strategy_status"] = {"accomplishments": [], "shortfalls": [], "process": ""}
    with tempfile.TemporaryDirectory() as td:
        c = os.path.join(td, "blank.json")
        wr(c, json.dumps(blank))
        subprocess.run([sys.executable, os.path.join(SKILL, "build_quad.py"), c,
                        os.path.join(dist, "copilot", "Quad-Report-blank-template.pptx")],
                       check=True, capture_output=True)

    # Member starter: the empty data folder, and the quickstart.
    os.makedirs(os.path.join(dist, "member"))
    tmpl = os.path.join(ROOT, "data-template")
    pairs = [(os.path.join(b, f), os.path.relpath(os.path.join(b, f), tmpl))
             for b, _, fs in os.walk(tmpl) for f in fs]
    zip_dir(pairs, os.path.join(dist, "member", "Quad-Report-Data-starter.zip"), "Quad Report Data")
    shutil.copy(os.path.join(ROOT, "member-docs", "QUICKSTART.md"), os.path.join(dist, "member"))

    wr(os.path.join(dist, "RELEASE-NOTES.md"), f"# Quad Report {version}\n\n{notes}\n")
    if url:
        first_item = notes.split("\n- ")[0].lstrip("- ")
        wr(os.path.join(ROOT, "version.json"),
           json.dumps({"version": version, "notes": " ".join(first_item.split())}, indent=2) + "\n")

    print(f"\nBuilt dist/v{version}/")
    print("  update check: " + (f"on ({url})" if url else "off (set github_repo in release.json to turn it on)"))
    print("\nTo publish:")
    print(f"  1. git add -A && git commit -m \"Quad Report {version}\" && git tag v{version} && git push -u origin main --tags")
    print("  2. ChatGPT: in the shared GPT, replace Knowledge with dist/.../chatgpt/knowledge/* and paste instructions.md")
    print("  3. claude.ai and Copilot members: send the release email with RELEASE-NOTES.md and the zip / Copilot pack")


if __name__ == "__main__":
    main()
