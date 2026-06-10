# Tirtayasa Skills Collection

A grab bag of handy skills for CLI-based AI agents. Think of this repo as a toolbox you can plug into your agent when you want it to debug better, write cleaner plans, review code, make decks, or just stay more organized.

Each skill lives in its own folder with a `SKILL.md` file, plus any extra notes or scripts it needs to do the job.

## Categories

- `engineering/skills/` — software engineering, debugging, testing, architecture, frontend, React, FastAPI, Jupyter Notebook, and database guidance.
- `product-management/skills/` — PRDs, issue creation, triage, planning, and documentation-driven decision making.
- `business/skills/` — lead research, marketing reports, deep research, and user research synthesis.
- `productivity/skills/` — handoffs, presentation work, skill authoring, and high-level context prompts.

## Skills by Category

| Category | Skills |
| --- | --- |
| Engineering | `code-reviewer`, `diagnose`, `frontend-ui-engineering`, `impeccable`, `improve-codebase-architecture`, `react-best-practices`, `postgres-best-practices`, `tdd`, `fastapi-best-practices`, `jupyter-notebook` |
| Product management | `grill-with-docs`, `setup-matt-pocock-skills`, `to-issues`, `to-prd`, `triage` |
| Business | `lead-research-assistant`, `performance-report`, `research-synthesis`, `deep-research` |
| Productivity | `handoff`, `pptx`, `write-a-skill`, `zoom-out` |

## Folder Structure

```text
.
├── engineering/
│   └── skills/
├── product-management/
│   └── skills/
├── business/
│   └── skills/
├── productivity/
│   └── skills/
└── agent/
```

## Installing Skills Elsewhere

Use the `skills` CLI through `npx` to add skills directly from this GitHub repository:

Example:

```bash
# Add one skill
npx skills add https://github.com/abdtirtayasa24/myworkflows-skills --skill code-reviewer

# Add another skill
npx skills add https://github.com/abdtirtayasa24/myworkflows-skills --skill tdd
```

Replace the value after `--skill` with the folder name of the skill you want to install, such as `diagnose`, `pptx`, `triage`, or `research-synthesis`.

To see available options for your installed CLI version, run:

```bash
npx skills --help
```

## Usage Notes

- Keep each skill folder intact. Some skills include supporting files referenced by `SKILL.md`.
- Read a skill's `description` field to understand when it should trigger.
- If two skills overlap, choose the one that best matches the user's main intent.
- Some skills assume a software repository with issue tracking, documentation, tests, or project context files.
- Skills can be copied individually; you do not need to install every category.

## Assumptions and Requirements

- Each skill folder contains a `SKILL.md` entry point.
- Your CLI AI agent supports loading skills from local folders.
- Supporting files should stay beside the skill that references them.
- No runtime dependencies are installed by this repository itself.
