# Quad Report (maintainer notes)

The source for the Quad Report skill that BTCS shares with the group. Members
never see this folder; they get packages built from it.

## Layout

```
plugins/quad-report/skills/quad-report/   THE skill. The only place to edit the method.
  VERSION                                 bump on every release (tools/release.py --bump)
.claude-plugin/marketplace.json           makes this repo a Claude plugin marketplace
.agents/plugins/marketplace.json          ...and a ChatGPT desktop / Codex one
plugins/quad-report/plugin.json           ChatGPT plugin manifest (version synced by release.py)
platforms/chatgpt|copilot/instructions.md the short instructions for each platform
data-template/                            the empty "Quad Report Data" folder members get
member-docs/QUICKSTART.md                 what members read
tests/                                    run before every release
tools/release.py                          tests, then builds every platform into dist/
release.json                              set github_repo here to turn on update checks
```

## How members' data works

Each member has a "Quad Report Data" folder in their own drive:
`quad-profile.json`, `history/YYYY-MM.json`, `out/`. The skill never stores
anything in its own folder, so replacing the skill on update loses nothing.
`quad_data.py` is the only thing that writes history.

When a release needs a new profile field: bump `PROFILE_SCHEMA_VERSION` in
`quad_data.py` and add the field and its question to `MIGRATIONS`. Each
member's next run asks for just that field.

## Releasing

1. Edit the skill. Add a `## x.y.z` entry to CHANGELOG.md in plain words.
2. `python tools/release.py --bump patch` (or minor / major).
3. Follow the three publish steps it prints.

How each platform gets the update:

| Platform | Member installs | Update reaches them |
|---|---|---|
| ChatGPT (web) | builds a Project from the ChatGPT pack | release email with the new pack |
| ChatGPT desktop / Codex | plugin from this repo (`.agents/plugins/marketplace.json`) | push a tag |
| Claude desktop / Code | plugin from this repo's marketplace | push a tag; the marketplace serves it |
| claude.ai | uploads the skill zip | release email with the new zip |
| Copilot | Copilot agent with the Copilot pack | release email with the new pack |
