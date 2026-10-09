# Issue prep: the Opportunity / Issue Processing Form

When the owner names a topic for the group, they may want to bring it as an
issue. This prepares the Opportunity / Issue Processing Form for it, in the
form's own layout, from their answers.

## Ask, never assume

At the end of the monthly check-in, if they named any topics for the group,
ask once: **"Want to prep an Issue Processing Form for any of these?"** Name
the topics. If they say no, drop it. Also run this whenever they ask for it
directly ("prep my issue", "issue processing form", "fill out my issue
form").

## The form

`fill_issue.py` draws the form itself: the same sections, prompts and layout
as the one the group uses, without branding. Nothing needs to be supplied;
never ask the owner for a blank form.

If they keep their own branded copy in `<data_dir>/templates/` (any .docx
with "issue" in the name, `quad_data.py status` reports it as `issue_form`),
fill that one instead with `--form`. Run `fill_issue.py check <form.docx>`
first; if boxes are missing, their copy has different wording, so say which
and use the drawn form.

## The questions

One at a time, made for answering out loud, like the check-in. Each maps to
a box on the form.

**Header** (ask once, then remember in the profile under `vistage`):
- **Vistage member:** their name as it goes on the form. Default to
  `company.report_by`; confirm.
- **Vistage group #:** ask the first time, save as `vistage.group_number`.
- **Meeting date:** the next meeting from `meeting` in the profile. Confirm.

**The issue:**
1. **"What's the issue or opportunity, in a sentence or two?"** The form asks
   for "the heart in no uncertain terms." If they ramble, tighten it to one or
   two plain sentences and read it back.
2. **"Why does it matter?"** Effect on dollars, people, products, customers,
   vendors, family, timing, the future.
3. **"What's it worth, in dollars?"** Their number. If they do not know,
   offer to work one out from their own figures with the arithmetic shown,
   and let them pick or say "not sized yet." Never put a number there they
   did not agree to.
4. **"What do you want to happen?"** The ideal outcome.
5. **Background,** as short bullets: how and when it started, who the
   players are, the forces at work, where things stand today, what happens if
   nothing changes. Ask these as one conversational question with prompts;
   they can skip any.
6. **"What are your options?"** Every action they have considered, including
   doing nothing. List theirs only.
7. **"Which way are you leaning?"** The direction they plan to take now.
8. **"What do you want from the group?"** Missing options, a gut check, what
   others would do differently.

## Hard rules

- **The issue is theirs, like quadrant iv.** Do not suggest options, stakes,
  players or a direction they did not raise. You may ask "anything else you
  have considered?" once; you may not offer one. The group's job is to find
  the options they are missing, and an AI's list in the box gets in the way
  of that.
- **Tighten, don't add.** Condense their words so each box reads cleanly.
  Keep every fact they gave and add none.
- **Fit one page.** One or two sentences for the issue, two or three for
  significance and outcome, up to five bullets for background, options and
  help. Longer answers push the form onto a second page; trim and say so.
- **Read the whole form back,** box by box, before filling it. Fill only after
  they say it is right.
- **It is private.** Issues often name people. It stays in their folder and
  this conversation.

## Filling it

Write `issue.json` (keys: `member`, `meeting_date`, `group`,
`dollar_value`, `issue`, `significant`, `ideal_outcome`, `background` as a
list, `options` as a list, `direction`, `help` as a list), then:

```
python3 fill_issue.py fill issue.json <data_dir>/out/YYYY-MM-issue-<short-name>.docx [--form <their copy>]
```

Save `issue.json` to `<data_dir>/issues/YYYY-MM-<short-name>.json` so it can
be picked up again next month. Hand over the .docx, never a PDF; they may
edit it before the meeting. On a platform that cannot run Python, give them
the text for each box in order, labeled exactly as the form labels it.
