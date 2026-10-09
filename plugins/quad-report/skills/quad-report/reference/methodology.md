# Methodology

Most of the ways this report goes wrong are accounting problems, not slide
problems. Each rule below exists because skipping it produced a confident
wrong number.

## 1. Revenue basis

Three bases exist and they disagree:

| Basis | What it is | When it lies |
|---|---|---|
| Invoiced | The invoice date in the ledger | Any month where billing ran late or a milestone landed |
| Collected | Cash received | Always, for a monthly operating report |
| **Earned** | The month the work was done | Needs an invoice-to-work-month mapping |

**Pick one, print it on the slide, never mix two in one quadrant.**

**If the owner bills any milestones, deposits or fixed fees, earned is the only
honest basis.** Ask about billing models during setup; do not infer them.

How to get to earned:

- **Best: the owner's own billing tracker**, if they keep one, assigning each
  line to a work month. It is their record, it already handles holds and
  absorbed work, and it reconciles to what they send clients.
- **Next: invoice reference numbers.** Billing runs are sequential. A run dated
  the 1st of a month usually belongs to the previous month. Invoices with
  reference numbers out of sequence are late-billed work from an earlier run.
- **Milestones and deposits** attach to the delivery window the invoice line
  states, or to the months the time system shows the work in. A deposit taken
  before any work started is not revenue in the month it was invoiced.

Worked example of what goes wrong: one July read $159K of invoiced revenue.
$37K was the previous month's billing run dated the 1st, $18K was a deposit for
a build that had not started, and $25K was a milestone covering three months.
Real July was $92K. August, which read as a $19K loss, was a $20K profit.

## 2. Delivery cost basis

**Use the time system, not accounts payable.** Contractors invoice weeks after
they deliver. The ledger books their cost in the month they billed you, which
puts delivery cost in the wrong month and makes margin swing for no reason.

**Salaried and owner delivery time belongs in cost of sales.** Most small
business books put all W-2 payroll in operating expenses. If an owner or a
salaried person spends hours on client work, those hours are delivery cost.
Split each person's pay by their client-hours share and move that part up.

Effect in one real case: reported gross margin 61.2%, actual 43.4%.

**Classify client versus internal by project, not by a billable flag.** Time
systems mark almost everything billable. Internal projects (operations
backlogs, sales, marketing, internal meetings, recruiting) carry no delivery
cost against revenue; the salaries behind them sit in overhead and are charged
once, there.

**Rate-card value is not revenue.** A time system will price internal hours at
the rate card. In one case that inflated "billable value" by $159K against what
was actually invoiced. Never use a fees column as a revenue number without
stripping internal projects first.

## 3. Overhead and break-even

Break-even = overhead ÷ gross margin, with both sides on the same definition.

**Overhead is fixed cost with the delivery portion removed.** The common error
is to treat delivery salaries as fixed, count them in overhead, and also count
their hours in cost of sales. That double-counts and inflates break-even.

Worked example: a $48,100 monthly cost base contained $18,818 of delivery
salary. True overhead was $29,289. Break-even fell from a quoted $78,600 to
roughly $60,000 once both sides were defined consistently.

**Cash reserve** divides cash by overhead, not by total cost. If revenue stops,
variable delivery cost stops with it.

## 4. Margin targets

A blended gross margin target is a function of delivery mix, not ambition.
Compute, per person on client work, the cost rate and the realized bill rate.
Then show what blended margin different contractor shares buy. A target that
requires a mix the owner has no plan to reach is not a target.

Worth checking: realized bill rate against the rate card. Fixed-fee work often
realizes well under the rate the owner believes they charge.

## 5. Reconciliation

Every run, both ways:

- Time system total labor cost, year to date, against the ledger's labor lines
  (contractor cost of sales plus the delivery share of payroll).
- Time system client-project fee value against invoices, for the
  time-and-materials clients only.

Print both gaps. A clean reconciliation is roughly 3% or better. If the gap is
larger, run the zero-rate audit before looking anywhere else.

## 6. Wins and shortfalls

Use mail and calendar for **recall, not judgment**. Produce an evidence list of
what happened in the period, with dates. Present it and let the owner mark
which were wins and which were misses. Supply memory; the owner supplies the
verdict.
