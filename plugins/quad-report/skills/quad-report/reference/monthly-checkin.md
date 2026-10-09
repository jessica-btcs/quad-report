# Monthly check-in

The numbers fill most of quadrant i. The story behind them, how each goal in
quadrant ii is moving, and all of quadrant iii come from the owner, and this
is how you get them. Run it every month, after the numbers and before the
slide.

## How to ask

- **One question at a time.** Wait for the answer before the next one.
- **Made for talking.** Say up front that they can answer out loud (the
  microphone in ChatGPT or Claude) and ramble. Long, messy answers are fine;
  condensing them is your job, not theirs.
- **Recall, not judgment.** If mail, calendar or Teams is connected, first
  offer a dated list of what happened this month (signed agreements, hires,
  closed projects, missed deadlines) as a memory aid. They decide what was a
  win and what was a miss. You never do.
- **Show last month.** For each question, show what they said last month
  (from `history/`) so they can say "same" or "that one's done."

## The questions

0. **Quadrant i: show the KPIs first** (actual, plan, variance), then ask
   **"Anything behind any of these you want on the slide?"** Their reason goes
   into that KPI's status line, alongside the source (84 characters). A KPI
   they say nothing about keeps a status line that names its source and
   nothing more; do not explain a miss on their behalf.
1. **"What went well this month?"** Up to three. These are the
   accomplishments.
2. **"What didn't go the way you wanted?"** Up to three. These are the
   shortfalls. Measure against what they meant to do, not against the KPIs;
   the KPIs already have their own quadrant.
3. **"How's it going getting things off your desk, building or fixing
   processes?"** One line. (Classic wording: how's it going in building and
   improving processes in your position.)
4. **Each core strategy, by name: "Did this move this month?"** Moved, stuck,
   or done, plus a few words if they want. Mark a strategy `stalled` only
   when they say it did not move. `quad_data.py annotate` then counts how
   many months it has been stuck.
5. **Quadrant ii, each goal by name, showing its bullets: "Where does this
   one stand?"** Update each bullet's progress (88 characters) or the status
   line in their words, or keep last month's if nothing changed. A goal they
   say is finished gets `"flag": "done"`.
6. **"What do you want to ask the group about?"** Up to three short topics
   for the call-topics line. Optional; blank is fine.

## Quadrant iv

Do not ask what is on their mind, and do not suggest anything. Offer exactly
this, once, at the end: "Quadrant iv is yours. Want to dictate it now so I
type it in word for word, or leave it blank to write by hand?" If they
dictate, enter their words with only the trimming needed to fit (84
characters per line, two per block). Never add, reword the meaning, or fill a
block they skipped.

## Before you build

- **Condense to fit,** keeping their words and their meaning: 58 characters
  for an accomplishment or shortfall, 86 for the process line, 40 for a
  strategy. Cut filler, not facts. Never add a number, name or result they
  did not say.
- **Read it back** as the slide will show it, quadrant by quadrant, and ask
  "Anything to change?" Build only after they say it is right.
- If they skip a question, leave that space blank on the slide. A blank line
  is honest; an invented win is not.
