# Setup interview

Run once, on first use. Produces `quad-profile.json` in the owner's Quad
Report Data folder (see SKILL.md step 0), shaped by
`quad-profile.schema.json`, with `schema_version` set. Takes 20 to 40 minutes.
Pull anything you can from a connector first so the owner answers fewer
questions, and show them what you pulled rather than asking them to confirm
numbers blind.

**Before the interview, build the sample** (`examples/sample-config.json`)
and show them the slide, so they see where this is going and you know the
plumbing works.

Ask these in small batches, not as a wall. **Save the profile after every
batch.** Owners get pulled away; the next chat picks up where this one
stopped, because `quad_data.py status` lists what is still missing.

## What to ask them to bring

If nothing is connected, ask for these exports. Name them exactly; "a recent
P&L" gets you one 12-month total, which is useless for trends.

- **Profit and loss, by month, last 12 months, accrual basis.** One column
  per month. If their fiscal year started recently, prior year plus year to
  date. Cash basis puts revenue in the month the money landed; say so on the
  hand-off if that is all they have.
- **Balance sheet as of the last month end**, for the cash line.
- **Sales by customer, by month, accrual**, parent customers only if their
  system has sub-jobs. Optional; it shows concentration.
- **A time export**: person, date, hours, project, and cost per entry, for
  the same 12 months. Optional; it is the difference between tier 1 and 2.
- **Their billing tracker**, if they keep one.
- **Their annual planning deck.**

## Company

- Company name, who reports, fiscal year start.
- Annual theme, if they have one.
- Their multi-year vision in one line, if they have one.
- Meeting cadence: which weekday and which week of the month. The run date
  computes from this; do not read it from a calendar.

## Billing models — the question that decides the methodology

> Which of these do you use? Time and materials, fixed fee, milestone or gated
> payments, deposits or retainers, subscription.

Anything other than pure time and materials forces the earned-revenue basis.
If they bill milestones, ask where the work-month mapping lives: a billing
tracker, the SOWs, or nowhere yet.

## Books

- Accounting platform, or upload.
- **Where does salaried delivery pay sit in your books: cost of sales or
  operating expenses?** Most say operating expenses. That is the single
  biggest cause of an overstated gross margin.
- Who on the team does client work, and roughly what share of their time.
- Contractors or a bench, and whether their rates are recorded anywhere.

## Time

- Where hours live, if anywhere. Examples to offer if they are unsure what
  counts: services firms use Harvest, Toggl Track, Clockify, BigTime, Kantata
  or Productive; construction and trades use Procore, Buildertrend, JobTread,
  Knowify or Foundation; field service uses ServiceTitan, Jobber or Housecall
  Pro; job shops use JobBOSS, ProShop or their ERP's job costing; some run it
  inside QuickBooks Online Projects or QuickBooks Time. Payroll hours alone
  still help.
- **Are cost rates set for every person and every project?** Run the zero-rate
  audit at the end of setup and show them what is missing. This is usually the
  first real value the skill delivers.

## KPIs

Default set: revenue, gross margin, operating overhead, net profit, cash
reserve. The owner may add more.

For each: the number, the target, **and the basis the target was set on**,
recorded next to it. Ask what the target means in their words. Do not propose
a target. If they ask for a view, compute what their current mix supports and
show the arithmetic, then let them choose.

## Goals and strategies

These are set once a year. Never skip them; a profile without goals and
strategies is not finished.

- **Their annual goals, lifted verbatim** from their planning deck if they
  have one. Ask them to upload it. Do not paraphrase. Up to four, each with a
  theme and one or two measurable lines, or a single SMART goal.
- **Their core strategies, up to six.** Ask: "What are the few things you're
  working on all year that move those goals?" The Quad states each one as an
  action ending in "-ing" (the classic heading is "Core Strategies: Actions
  Ending in 'ing'"): "Hiring and certifying crew leads," "Closing the books
  by the 5th." If they answer with nouns or goals ("crew leads," "faster
  close"), offer the "-ing" version in their own words and let them approve
  or change it. Each fits in 40 characters. Do not invent a strategy they did
  not name; fewer than six is fine.
- **Set `plan_set`** in the profile to the month these were agreed, as
  YYYY-MM. That is how the next fiscal year knows to ask again.

## Annual review

When `quad_data.py status` says `annual_review_due: true`, run this before
the monthly check-in. It is the start of a new fiscal year (or the plan was
never dated).

1. Show this year's theme, goals, core strategies and KPI targets from the
   profile, and last month's status for each.
2. Ask, one at a time: **"New theme for the year?"**, **"Your goals for this
   year?"** (ask for the new planning deck and lift them verbatim), **"Your
   core strategies for this year?"** (same "-ing" rule, up to six), and **"Your
   KPI targets for this year, and the basis each is set on?"**
3. "Keep it" is a fine answer to any of them. Never carry a goal forward
   silently; confirm each.
4. Write the answers to the profile and set `plan_set` to this month.

## Output

- Reporting period: the month, or a rolling quarter. Default to the month,
  because that is the period the owner recognizes. Offer rolling only if their
  billing is lumpy, and label it on the slide if used.
- Plain English or the classic Sherpa wording.
- Confirm where their Quad Report Data folder lives, and that it is in a
  backed-up drive (OneDrive, Google Drive, SharePoint).

## Last

Tell them plainly: everything runs against their own connected accounts, in
their own workspace. Nobody who shared this skill with them can see their
numbers.
