# Updating

The owner's Quad Report Data folder is never touched by an update. Only the
skill changes. When `quad_data.py status --check-updates` says a newer
version is out, tell them the one line that matches where they run it:

- **Claude desktop or Claude Code (plugin):** updates arrive on their own
  once Sync automatically is on (Customize > Plugins > the btcs-quad-report
  marketplace). Otherwise, select that marketplace and click Check for
  updates. In Claude Code: `/plugin`, Marketplaces, btcs-quad-report, Enable
  auto-update.
- **claude.ai (uploaded skill):** download the new skill zip from the link
  in the release email, then in Customize > Skills upload it in place of the
  old one.
- **ChatGPT (the shared Quad Report GPT):** nothing to do. The GPT is updated
  in one place and everyone has it in their next chat.
- **Copilot:** replace the files in their Copilot agent's knowledge with the
  new Copilot pack.

If the new version needs something new in their profile, the next run asks
for it (`missing_fields`) rather than guessing.
