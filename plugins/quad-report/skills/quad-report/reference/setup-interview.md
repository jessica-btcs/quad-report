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

- Where hours live, if anywhere.
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

- Their annual goals, **lifted verbatim** from their planning deck if they have
  one. Ask them to upload it. Do not paraphrase.
- The core strategies, up to six, phrased as ongoing work.

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
