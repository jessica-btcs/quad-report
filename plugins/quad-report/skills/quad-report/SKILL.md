---
name: quad-report
description: Builds the monthly Vistage Quad Report one-pager from the owner's own financials and time records. Use when the owner says "quad report", "quad", "build my quad", "set up my quad report", "Vistage one-pager", or asks to prepare for their Vistage or peer-group meeting. Runs a setup interview on first use, reconciles the books against the time system before trusting any number, builds quadrants i, ii and iii from data, and deliberately leaves quadrant iv blank for the owner to write.
---

# Quad Report

A one-slide monthly report for a peer-advisory meeting, after the Sherpa
Alliance Quad Report (© Sherpa Alliance, 2004), used with permission. Four
quadrants: how we did, this year's goals, how we get there, what's on my mind.

The slide is the easy part. The hard part is producing a number that means
something. Read `reference/methodology.md` before computing anything.

## Two folders, never mixed

- **This skill folder** holds the method and the tools. It is replaced on
  every update. Never write anything the owner needs into it.
- **The owner's data folder**, "Quad Report Data", lives in their own
  OneDrive, Google Drive or SharePoint. It holds `quad-profile.json`,
  `history/` and `out/`. Nothing in an update touches it, and it works the
  same whichever AI they use.

`quad_data.py` is the only thing that writes `history/`. Use it; do not write
history files by hand.

## Step 0: find the data folder

Do this before anything else, every run.

1. **A folder you can read and write** (Claude desktop or Claude Code with a
   folder connected, a synced OneDrive or Google Drive folder on their
   computer): look for a folder named "Quad Report Data" or one containing
   `quad-profile.json`. If `~/.quad-report/data-path` exists, it holds the
   path from last time. Once found, write the path there.
2. **A drive connector you can read but not write** (claude.ai, ChatGPT):
   read `quad-profile.json` and the latest `history/` file through it.
3. **Neither:** ask the owner to attach `quad-profile.json` and last month's
   history file from their Quad Report Data folder. Copy them into a working
   folder with the same layout.

Then run `python3 quad_data.py status <data_dir> --check-updates` and act on
what it says:

- `python_pptx: false` → install it (`pip install python-pptx`) before going on.
  `python_docx: false` matters only for issue forms; install `python-docx`
  when they ask for one.
- `profile_found: false` → first run. Go to `reference/setup-interview.md`.
  Run `quad_data.py init <data_dir>` first so the folder exists.
- `needs_migration: true` → this skill is newer than their profile. Ask only
  the questions in `missing_fields`, one small batch, write the answers into
  the profile, and set `schema_version` to the current value. Never guess a
  missing field.
- `update.available: true` → tell them once, in one line, at the end of the
  run: a newer version is out, and how to get it on their platform (see
  `reference/updating.md`). Never block the run on it.
- `suggested_period` → the month to offer when they did not name one.
- `annual_review_due: true` → a new fiscal year has started (or the plan was
  never dated). Before the monthly check-in, run the annual review in
  `reference/setup-interview.md`: theme, goals, core strategies and KPI
  targets, each confirmed or replaced. Never carry them into a new year
  without asking.

**If you could not write to their folder,** finish by handing them every file
that changed (the profile, the new history file, the slide) and say exactly
where each goes: "Save this into Quad Report Data/history/". The run is not
done until those files are back in their folder, because next month depends
on them.

## Order of work

1. **Read the profile.** It holds the company, the definition of every
   metric, the targets and the basis each was set on, the goals and
   strategies, and what is connected. No profile means no run: do setup first.
2. **Gather.** Pull the period's revenue, delivery cost, operating cost and
   cash from whatever the profile says is connected. Fall back to uploads.
3. **Reconcile, then decide whether to proceed.** See "The trust gate" below.
4. **Compute** the KPIs exactly as the profile defines them. Never redefine a
   metric mid-year.
5. **Monthly check-in. Never skip it.** Follow `reference/monthly-checkin.md`:
   one question at a time, made for answering out loud, covering what is
   behind the KPIs, each goal, what went well, what didn't, the process line,
   each core strategy, and topics for the group. Quadrant iii, the goal
   updates and any explanation on a KPI come from these answers and nowhere
   else. Read the condensed answers back and build only after the owner says
   they are right. If they named topics for the group, ask whether they want
   to prep an Issue Processing Form; only on a yes, follow
   `reference/issue-prep.md` once the slide is delivered.
6. **Write the config** (`quad-config.schema.json`), with `period` like
   "September 2026", then run
   `python3 quad_data.py annotate <data_dir> config.json`. It sets trend
   direction and STUCK flags from history. Do not set those by eye.
7. **Build** with
   `python3 build_quad.py config.json <data_dir>/out/YYYY-MM.pptx`.
   Quadrant iv renders with blank writing lines unless the owner dictated
   their own words in the check-in. Every build ends with a layout check
   (`layout_check.py`): every word inside its box, every box on the page. If
   it prints LAYOUT CHECK FAILED (exit code 3), shorten exactly the items it
   names, keeping the owner's meaning and every fact, and build again. Repeat
   until it says clean. If an item cannot get shorter without losing
   something that matters, ask the owner what to cut. This applies after
   every edit the owner asks for, not just the first build.
8. **QC.** Recompute every KPI from source and diff it against the config
   before handing anything over. Report the diff.
9. **Archive** with
   `python3 quad_data.py archive <data_dir> config.json --run run.json`,
   where `run.json` records `{"tier", "sources", "reconciliation":
   {"labor_gap_pct", "fee_gap_pct"}, "zero_rate_hours", "qc_diff"}`. If the
   month is already archived it refuses: ask the owner before re-running
   with `--replace` (the old file is kept, never deleted).
10. **Deliver** the .pptx. Never a PDF: the owner edits this before the
    meeting. The hand-off note says the tier, both reconciliation gaps, and
    any zero-rate hours.

## Hard rules

**The slide comes from `build_quad.py` and nothing else.** Never draw the
slide yourself, never write your own python-pptx code for it, and never edit
the .pptx after the script has built it. Any change the owner asks for, a
number, a word, a label, goes into the config and the script runs again. If
the script will not run, say so and fix that; do not hand over a slide you
made another way.

**Never hand over a slide that failed the layout check.** No words outside
their box, nothing off the page, nothing cut off mid-sentence. Fix the text,
not the layout.

**The quadrant layout is correct as built. Do not rearrange it.** iv is top
left, iii top right, i bottom left, ii bottom right, with the headings on the
outer edge of the page. It looks out of order next to a normal reading grid
and that is on purpose: Scot Dietz's original spirals counter-clockwise from
the bottom left. Moving i and ii to the top, renumbering, or putting headings
at the top of every panel is a mistake, even when it looks tidier.

**Quadrant iv is the owner's.** Their worries are not derivable from their
financials. Generating it produces plausible sentences that aren't theirs, and
a peer group can tell. Even offering a shortlist anchors them. Put the headings
on the page and stop. The one exception: if the owner dictates quadrant iv
themselves, type in their words, trimmed only to fit.

**Never invent a win, a shortfall or a strategy update.** Quadrant iii is
what the owner told you in the check-in, condensed. A question they skipped
stays blank on the slide.

**Never invent a target or a goal.** Ask. If the owner has a planning deck,
lift the goals verbatim; do not paraphrase them into something tidier.

**Never score a KPI against a target set on a different basis.** If a
definition changes, the target is restated with it or the KPI is not scored.

**Every figure names its source.** If part of a number is reconstructed rather
than reported, the status line says so. "Per the tracker" is a lie when only a
third of it came from the tracker.

**The slide states today's methodology only.** No "was X on the old basis"
comparisons. The owner is not interested in defending last month's mistake to
their peers.

**American English** in all generated copy: color, organize, formalize, analyze.

**Delivery cost comes from the time system, not from accounts payable.**
Vendor invoices lag the work. See the methodology reference.

**Their data stays theirs.** Never send their numbers, files or company name
anywhere except their own data folder and this conversation. The update check
only downloads a version number; it sends nothing.

## The trust gate

Before any KPI is rendered, reconcile the time system's total labor cost for
the year to date against the ledger's labor lines.

- Within 5%: proceed, and print the gap in the hand-off note.
- 5% to 15%: proceed, print the gap, and name the likely cause. Run the
  zero-rate audit (below) first, because a missing cost rate on one project is
  the usual culprit.
- Over 15%: do not render gross margin or net profit. Report what is wrong and
  what would fix it. A Quad with a quietly wrong margin is worse than no Quad.

**Zero-rate audit, every run.** List any hours logged with no cost rate, by
person and by project. Those hours are invisible margin. One real case: a
contractor's 149 hours on two projects had no rate, which was 11% of the
annual contractor line and 15 points of gross margin.

## Tiers

The skill runs at whatever tier the owner's data supports, and the hand-off
note says which.

- **Tier 0.** Uploaded P&L. Works. Milestone timing cannot be corrected, so
  single months are noisy. Say so.
- **Tier 1.** Accounting connector. Revenue and cost by month, still on
  invoice timing.
- **Tier 2.** Accounting plus a time system with cost rates. Real margin,
  real break-even, work-month revenue.

## Files in this folder

- `build_quad.py`: the slide generator. Needs python-pptx and nothing else.
- `layout_check.py`: measures every text box on a built slide against
  Calibri's real character widths. build_quad.py runs it on every build.
- `quad_data.py`: the data folder: status, migration check, trends and stall
  flags, archiving. Standard library only.
- `quad-config.schema.json`: what a monthly config may contain.
- `quad-profile.schema.json`: what the profile holds.
- `reference/methodology.md`: revenue basis, cost basis, break-even, the
  reconciliation. Read this before computing.
- `reference/setup-interview.md`: the first-run interview.
- `reference/layout.md`: the Sherpa layout and both label sets.
- `reference/monthly-checkin.md`: the questions behind quadrant iii, every month.
- `reference/issue-prep.md`: filling the owner's own Vistage Issue Processing
  Form for a topic they want to bring to the group, only when they ask.
- `fill_issue.py`: fills that form's answer boxes. Needs python-docx.
- `reference/updating.md`: how an owner gets a new version on each platform.
- `examples/`: a sample config and its rendered slide. Build it first to see
  the output before connecting anything.
- `VERSION`: this skill's version.
