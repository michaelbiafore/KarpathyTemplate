# PLAN — Update CLAUDE.md

Status: **proposed, not yet applied**
Date: 2026-04-24
Target file: `CLAUDE.md` (project root)

## Context

The repo already has a thorough, well-tuned `CLAUDE.md`. It defines the wiki schema, page format, three operations (ingest / query / lint), Obsidian-specific rules, and efficiency rules (index-first lookup, second-mention rule, lazy backlinks, link cap, touch budget). Those sections are load-bearing and should not be touched.

The gaps below are about **onboarding context** for future Claude instances — what kind of repo this is, what external tooling it depends on, and what state files are expected to be mutated on every operation. They are additive, not corrective.

## Proposed changes

### 1. Add the standard `/init` header at the top (required prefix, currently missing)

Insert at the very top of `CLAUDE.md`, before the existing `# LLM Wiki — Schema` heading:

```markdown
# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.
```

Rationale: This is the conventional `/init` prefix that future tooling and Claude instances expect to find. Costs nothing; aligns with convention.

### 2. Add a "Repository Type" note up top

Insert immediately after the existing intro paragraph (the one that mentions Karpathy's pattern), before the `## Architecture` section:

> ## Repository Type
>
> This is **not a software project** — it is an Obsidian vault plus a Claude Code harness. There are no build, test, or compilation commands. "Linting" here means running `/lint-wiki` against the content, not a code linter. All work is reading and writing markdown under `sources/`, `wiki/`, and `inbox/`. There is no `package.json`, no test runner, no CI.

Rationale: Future Claude should not waste cycles looking for build/test commands or treating this like a codebase. A single explicit paragraph short-circuits that.

### 3. Add a "Tooling & Dependencies" section

Insert after `## Slash Commands`, before `## Operations`:

> ## Tooling & Dependencies
>
> - **`/ingest-url` shells out to `npx defuddle`** — Node.js and the `defuddle` npm package must be installed (`npm install -g defuddle`). The `Bash(npx defuddle:*)` permission is pre-allowed in `.claude/settings.local.json`. If defuddle fails, fall back to `WebFetch`.
> - **Bundled Obsidian skills** in `.claude/skills/`: `defuddle`, `obsidian-markdown`, `obsidian-bases`, `obsidian-cli`, `json-canvas`. Prefer these when manipulating Obsidian-specific syntax (callouts, frontmatter, `.base` files, `.canvas` files) instead of hand-rolling.
> - **No package manifest** at the project root — this is a content vault, not an npm/python project.

Rationale: The defuddle dependency is implicit in the `ingest-url` command file but not surfaced in `CLAUDE.md`. The skills are loaded by the harness but never referenced — Claude should know they exist before reaching for raw text manipulation.

### 4. Add a "State Files" section

Insert after the new Tooling section, before `## Operations`:

> ## State Files
>
> Two files are mutated on nearly every operation:
>
> - **`wiki/index.md`** — flat list of pages grouped under the 7 category headers. This is the **primary lookup** during ingest and query. Read it first, before globbing `wiki/`.
> - **`wiki/log.md`** — append-only markdown table with columns `| Date | Action | Pages Affected | Details |`. Every ingest, inbox processing event, and lint pass adds a row.

Rationale: These two files are referenced throughout the operations sections but never described in one place. New Claude instances should see them as the wiki's state, not as ordinary pages.

### 5. Clarify auto-fix scope in the Lint operation

In `### 3. Lint`, replace step 6:

> 6. **Report** findings and fix what can be fixed automatically

with:

> 6. **Report** findings. Auto-fix the safe cases without asking: missing entries in `wiki/index.md`, broken `[[wikilinks]]` whose target has an obvious rename, missing `wiki/log.md` rows for known events. **Ask before** rewriting content claims, merging pages, or deleting orphans.

Rationale: "Fix what can be fixed automatically" is ambiguous. Drawing the line between mechanical fixes (safe to auto-apply) and content judgments (need user approval) prevents Claude from silently rewriting pages.

## Out of scope — deliberately NOT changing

These sections are tight and load-bearing; do not touch:

- Wiki Page Format template
- Obsidian-Specific Rules (wikilink format, callouts, highlights, nested tags)
- Naming Conventions
- Source Types table
- Operations 1 (Ingest) and 2 (Query) — the workflows are correct as written
- Efficiency Rules block — the core insight that keeps ingest cost flat as the wiki grows
- Second-mention rule, lazy-backlink rule, link cap, touch budget

## Order of application

When applying this plan, do edits in this order so the file reads coherently after each step:

1. Prepend the `/init` header (change 1)
2. Insert "Repository Type" after the intro (change 2)
3. Insert "Tooling & Dependencies" after Slash Commands (change 3)
4. Insert "State Files" after Tooling (change 4)
5. Edit Lint step 6 in place (change 5)

Each is a localized insert or single-line edit — no risk of clobbering existing structure.

## Verification after applying

- `CLAUDE.md` opens with the standard `/init` prefix.
- A fresh Claude instance reading only `CLAUDE.md` understands: (a) this is a content repo, (b) defuddle is required for `/ingest-url`, (c) `wiki/index.md` is the primary lookup, (d) which lint fixes are safe to auto-apply.
- All existing schema rules remain byte-identical.
