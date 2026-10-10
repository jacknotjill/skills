# Agent guidance

This repository publishes Agent Skills (https://agentskills.io/specification).
It is public, so never commit secrets, internal hostnames or employer-private
details into a skill.

## Layout

- `skills/<name>/SKILL.md`: one directory per skill. Only skills go here,
  because every installer discovers everything under `skills/`.
- `template/`: the starting point for a new skill. It sits outside `skills/`
  so installers don't pick it up.
- `.claude-plugin/marketplace.json`: exposes the whole repo as one Claude Code
  plugin. Its entry has `"source": "./"` and no `skills` list, so new skills
  under `skills/` load without editing this file.
- `scripts/validate_skills.py`: checks frontmatter against the spec. CI runs it.

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

## Checks

```bash
uv run --with pyyaml scripts/validate_skills.py
claude plugin validate .
```
