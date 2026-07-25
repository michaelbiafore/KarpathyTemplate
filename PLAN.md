# PLAN — Reset KarpathyTemplate to a clean starter template

**Goal.** Turn this working vault back into a bare-bones, shareable template a new user can clone, edit `## Categories` in `CLAUDE.md` to taste, and then fill with their own material using the existing `.claude/` commands and skills. Remove all *inserted* (ingested/generated/personal) material while preserving every piece of machinery.

**Scope (per instruction).** Clean only `inbox/`, `wiki/`, and `sources/`. Do **not** touch `scripts/` or `.claude/` (commands, skills, or any code they call), and keep `CLAUDE.md` exactly as-is (the new user re-writes the Categories table themselves). Items outside these three directories are collected under **§7 Recommended follow-ups** and are NOT executed as part of the core plan without explicit go-ahead.

---

## 1. Preserve — do not modify or delete

- `CLAUDE.md` — kept verbatim, including its current personalized Categories table (the new user edits it).
- `.claude/commands/` — all 5 slash commands (`ingest-url`, `ingest-inbox`, `ingest-pdf`, `ingest-epub`, `maintain-wiki`).
- `.claude/skills/` — all 5 skills (defuddle, json-canvas, obsidian-bases, obsidian-cli, obsidian-markdown) and their `references/`.
- `.claude/settings.local.json`.
- `scripts/` — entire tree: `epub2md/`, `pdf2md/`, `fetch_substack.py`, `README.md`, and any vendored source they call. (Venvs remain gitignored per CLAUDE.md; nothing here is touched.)
- `README.md`, `SETUP.md`, `.obsidian/`, `images/` — untouched by the core plan (see §7 for optional notes).

---

## 2. What is being removed — inventory

| Area | Item | Tracked in git? | Count |
|------|------|-----------------|-------|
| `wiki/` | Category page folders: `aisoft/`, `cyber/`, `evals/`, `gitlab/`, `skills/`, `LIST/` | untracked | 31 pages |
| `wiki/` | `index.md`, `log.md` — **reset, not deleted** | tracked | 2 |
| `sources/` | `books/`, `cyber/`, `evals/`, `gitlab/`, `skills/`, `youtube/` (all raw ingested material) | untracked | 722 files |
| `inbox/` | `processed/`, loose `.html`/`.excalidraw`, `images/*`, `Prefect_*.pdf`, `README.md` | mixed | 34 files |

---

## 3. Clean `wiki/`

1. **Delete the category page folders** (all untracked, plain filesystem delete):
   - `wiki/aisoft/`, `wiki/cyber/`, `wiki/evals/`, `wiki/gitlab/`, `wiki/skills/`, `wiki/LIST/`
   - Rationale: CLAUDE.md states category subfolders under `wiki/` are created **lazily on first ingest**, so a clean template must not pre-create them.
2. **Reset `wiki/index.md`** to an empty scaffold whose category headers mirror the *current* `CLAUDE.md` Categories table (Agent Runtime, Agentic Cybersecurity, GitLab, Skills, System Engineering, AlgoTrading, PolyEcon, Data, Agentic Software Engineering, Evals) plus the Source-Type Indexes (Books, Arxiv, Substack, YouTube). Remove every page entry and the personal-only sections that were never in CLAUDE.md (`ELSA`, `Ken`, `Lodge`, `VRUI`). See §6 for the exact scaffold.
3. **Reset `wiki/log.md`** to a single bootstrap entry (see §6).

End state: `wiki/` contains only `index.md` and `log.md`, both scaffolded — matching the "bootstrap state" CLAUDE.md describes.

---

## 4. Clean `sources/`

1. **Delete all contents** of `sources/` (all 722 files, all untracked): `books/`, `cyber/`, `evals/`, `gitlab/`, `skills/`, `youtube/`, including the `*_figs/` and per-book `images/` trees.
2. Leave `sources/` present but empty. Since git does not track empty directories, add a single tracked placeholder so the folder survives a clone:
   - Option A (recommended): a short `sources/README.md` — one line explaining raw sources land here, organized by type per CLAUDE.md's Source Types table.
   - Option B: an empty `sources/.gitkeep`.
   - Do **not** recreate `sources/books/README.md` or `sources/youtube/README.md` — CLAUDE.md says those are created lazily on first ingest of that type.

End state: `sources/` empty except one placeholder — matching CLAUDE.md's "`sources/` is empty" bootstrap statement.

---

## 5. Clean `inbox/`

`inbox/` is a local capture zone (gitignored per CLAUDE.md), but it currently holds ingested material **and** several stale tracked files that contradict the gitignore intent. Clean both:

1. **Delete untracked capture residue:**
   - `inbox/processed/` (entire folder — the archive of already-ingested notes)
   - `inbox/Broad Small Edge Tools.excalidraw`
   - `inbox/What_Are_AI_Evals_Really_About_FORMATTED_TRANSCRIPT.html`
   - contents of `inbox/images/` (the loose PNG/JPEG figures)
2. **`git rm` the stale tracked files** (they show as deletions in the working tree already; finalize by removing from the index so they leave the template's history going forward):
   - `inbox/Prefect_study_guide_PERPMAX_30pp.pdf`
   - `inbox/images/*.png`, `inbox/images/*.jpeg` (10 files)
   - `inbox/README.md` (empty) — replace with a fresh one (next step) rather than leaving the empty tracked file.
3. **Recreate a minimal capture zone:**
   - `inbox/README.md` — 2–3 lines: "Drop fleeting notes, clipped articles, and PDFs here, then run `/ingest-inbox`."
   - keep an empty `inbox/images/` (add `.gitkeep`) for inbox-local figures.

End state: `inbox/` holds only `README.md` (+ empty `images/`) — a clean capture zone with no processed content.

---

## 6. Exact reset content for the two scaffold files

**`wiki/index.md`** — keep the existing header/prose, replace the body with empty category sections mirroring CLAUDE.md:

```markdown
---
title: Wiki Index
date: <ingest date of first use>
tags:
  - meta/index
---

# Wiki Index

The catalog of every page in this wiki. Claude reads this file **first** during ingest and query to decide what already exists — keep entries up-to-date and use `[[filename|Display Text]]` style.

Categories below mirror CLAUDE.md's Categories table. Add new pages under the section that matches their primary topic; a page may also appear in a second section when it spans two categories.

See also: [[log|Change Log]]

## Agent Runtime — `runtime/`
<!-- Add entries as: - [[filename|Display Text]] — one-line hook -->

## Agentic Cybersecurity — `cyber/`

## GitLab — `gitlab/`

## Skills — `skills/`

## System Engineering — `sys/`

## AlgoTrading — `algotrade/`

## PolyEcon — `polyecon/`

## Data — `data/`

## Agentic Software Engineering — `aisoft/`

## Evals — `evals/`

## Source-Type Indexes

### Books

### Arxiv Papers

### Substack

### YouTube
```

**`wiki/log.md`** — reset to header + a single bootstrap entry:

```markdown
---
title: Wiki Change Log
date: <today>
tags:
  - meta/log
---

# Wiki Change Log

Append-only record of ingests, edits, and lint runs. Newest entries at the bottom. Each entry should include date, what was ingested or maintained, and which wiki pages were created or updated.

Format:

```
## YYYY-MM-DD — short headline

- **Ingested:** <source path or URL>
- **Created:** [[page1|Page 1]], [[page2|Page 2]]
- **Updated:** [[page3|Page 3]] (what changed and why)
- **Notes:** any skipped sources, promotion candidates, touch-budget overruns
```

---

## <today> — wiki bootstrap

- **Created:** [[index|Wiki Index]], [[log|Change Log]]
- **Notes:** Initial scaffolding. Categories mirror CLAUDE.md. No source ingests yet.
```

> Note: if `CLAUDE.md`'s Categories table is later edited by the new user, `wiki/index.md` headers should be updated to match — the README's personalization flow already covers this.

---

## 7. Recommended follow-ups (outside the stated inbox/wiki/sources scope)

Not part of the core clean (they live outside the three directories) but worth doing before publishing the template. **Flagged for your approval — none executed by default.**

1. **Add a `.gitignore`.** There is currently none, yet CLAUDE.md repeatedly says `inbox/`, `Clippings/`, `cookies_substack.json`, and `scripts/*/.venv/` are gitignored. Without it, a new user's captures, cookies, and venvs get committed. Proposed entries:
   ```
   inbox/
   Clippings/
   cookies_substack.json
   scripts/epub2md/.venv/
   scripts/pdf2md/.venv/
   **/__pycache__/
   .DS_Store
   .obsidian/workspace.json
   .obsidian/graph.json
   ```
   (If `inbox/` is gitignored, keep its `README.md`/`.gitkeep` tracked with `!inbox/README.md`, or document inbox as create-on-first-run.)
2. **`Clippings/`** — a capture zone like `inbox/`. Delete `Clippings/Late-Bound Sagas_…md` (tracked → `git rm`) so no clipped article ships in the template.
3. **Root personal residue** — remove/untrack `cookies_substack.json` (personal Substack credentials — should never ship), `.DS_Store`.
4. **`plans/`** — contains the user's ad-hoc planning docs (`PLAN_MakeWikiShareable.md`, etc.). CLAUDE.md says `plans/` is not part of the wiki. Either delete for the template or keep intentionally.
5. **`README.md` drift** — says "3 slash commands" and "5 skills"; there are now **5 commands** (adds `ingest-pdf`, `ingest-epub`). Update the count/list so the template's front door matches reality. (SETUP.md should be spot-checked similarly.)
6. **`.obsidian/`** — `workspace.json`/`graph.json` capture the current user's pane layout; harmless but personal. Optionally reset or gitignore (see §7.1).

---

## 8. Verification checklist

After executing §3–§5:

- [ ] `find wiki -type f` lists exactly `wiki/index.md` and `wiki/log.md`.
- [ ] `wiki/index.md` category headers match `CLAUDE.md`'s Categories table; zero page entries.
- [ ] `find sources -type f` lists only the single placeholder (`README.md` or `.gitkeep`).
- [ ] `find inbox -type f` lists only `README.md` (and `images/.gitkeep`).
- [ ] `git status` shows the tracked inbox files removed and index/log reset; no stray deletions elsewhere.
- [ ] `.claude/`, `scripts/`, and `CLAUDE.md` are byte-for-byte unchanged (`git diff --stat` touches nothing under them).
- [ ] Sanity: a category subfolder does **not** exist under `wiki/` or `sources/` (they must be created lazily on first ingest).
```
