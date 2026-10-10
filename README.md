# skills

My [Agent Skills](https://agentskills.io), in the open format that Claude Code,
Claude.ai, Codex, Cursor, Gemini CLI and other agents read.

Each skill is a folder under `skills/` holding a `SKILL.md`:

```
skills/
└── my-skill/
    ├── SKILL.md        # required: frontmatter (name, description) + instructions
    ├── references/     # optional: docs the agent reads on demand
    ├── scripts/        # optional: code the agent runs
    └── assets/         # optional: templates, data
```

## Skills

| Skill | What it does |
| --- | --- |
| [writing-guidelines](skills/writing-guidelines/SKILL.md) | How to write anything a person reads, plus a guide for prompts. Other skills that write load it. |
| [review-artifact](skills/review-artifact/SKILL.md) | A one-page review of a code change: a short introduction, then every hunk grouped by intent. |

## Install

**Claude Code**, as a plugin marketplace (updates arrive with `/plugin update`):

```
/plugin marketplace add jacknotjill/skills
/plugin install jacknotjill@jacknotjill
```

Skills then run as `/jacknotjill:<skill-name>`, or load on their own when a
task matches their description.

**Any agent**, with the [`skills` CLI](https://github.com/vercel-labs/skills):

```
npx skills add jacknotjill/skills              # pick from the list
npx skills add jacknotjill/skills --skill <name>
```

**By hand**: copy `skills/<name>/` into `~/.claude/skills/` (or your agent's
skills directory).

**Claude.ai**: zip a skill folder and upload it under Settings → Capabilities → Skills.

## Add a skill

1. Copy `template/SKILL.template.md` to `skills/<name>/SKILL.md`. The name is
   lowercase letters, digits and single hyphens, and must match the folder name.
2. Write the `description` as what the skill does and when to use it; it is
   all an agent sees before choosing to load the skill.
3. Run `uv run --with pyyaml scripts/validate_skills.py` (CI runs it too).

## License

[MIT](LICENSE)
