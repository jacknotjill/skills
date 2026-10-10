# Agent guidance

This repository publishes Agent Skills (https://agentskills.io/specification).
It is public, so never commit secrets, internal hostnames or employer-private
details into a skill.

## Layout

- `skills/<name>/SKILL.md`: one directory per skill. Only skills go here,
  because every installer discovers everything under `skills/`.
- `template/SKILL.template.md`: the starting point for a new skill. Installers
  scan the whole repo for files named `SKILL.md`, so the template is named
  differently.
- `.claude-plugin/marketplace.json`: exposes the whole repo as one Claude Code
  plugin. Its entry has `"source": "./"` and no `skills` list, so new skills
  under `skills/` load without editing this file.
- `scripts/validate_skills.py`: checks frontmatter against the spec. CI runs it.
- `scripts/vendor.sh` and `THIRD_PARTY.md`: skills copied from other repos
  (`show-me`, `visual-pr`, `grill-me`, `grilling`). Never edit those folders;
  refresh them with the script so they stay identical to upstream.

## Writing a skill

- Frontmatter needs `name` (matches the directory; `a-z`, `0-9`, single
  hyphens, max 64 chars) and `description` (max 1024 chars, says what the skill
  does and when to use it). Optional: `license`, `compatibility`, `metadata`,
  `allowed-tools`. Keep to these fields so the skill works in every agent.
- Keep `SKILL.md` under 500 lines. Move detail to `references/`, code to
  `scripts/`, templates and data to `assets/`, linked one level deep with
  relative paths.
- Don't add a `SKILL.md` at the repository root; it would turn the whole repo
  into one skill for some installers.

## Skills that write

Any skill whose output people read (docs, pages, messages, prompts) loads
`writing-guidelines`. Link it as `../writing-guidelines/SKILL.md` and name it,
so the agent can find it whether the skills are installed together or not.

## Checks

```bash
uv run --with pyyaml scripts/validate_skills.py
claude plugin validate .
```
