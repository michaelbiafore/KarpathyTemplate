# PLAN — `/ingest-vault` slash command

Status: **proposed, not yet implemented**
Date: 2026-04-26
Target file: `.claude/commands/ingest-vault.md` (to be created later)

## Goal

A one-shot slash command that incorporates the contents of an existing Obsidian vault — call it the **source vault** — into this Karpathy-style wiki (the **target vault**), as faithfully as possible while still respecting the target's three-layer architecture (`sources/` immutable raw, `wiki/` derived knowledge, `inbox/` quick capture) and the schema in `CLAUDE.md`.

The command must be **non-destructive to the source vault** (read-only) and **idempotent on the target vault** (re-running it should not duplicate work).

## Usage

```
/ingest-vault <source_vault_path> [--dry-run] [--limit N] [--since YYYY-MM-DD]
```

- `source_vault_path` — absolute path to the root of the source Obsidian vault
- `--dry-run` — discover and classify, but write nothing. Default for the first invocation.
- `--limit N` — process at most N notes (useful for testing)
- `--since YYYY-MM-DD` — only ingest notes whose file mtime or frontmatter `date` is on/after this date

## Why this is harder than `/ingest-url`

`/ingest-url` ingests one well-shaped artifact (a clean article) into one well-defined slot (`sources/<category>/`). A vault is a mixed bag:

- Notes vary in shape: clipped articles, daily notes, project notes, MOCs, atomic concept notes, fleeting ideas, half-finished drafts.
- The sources-vs-wiki distinction this repo enforces does not exist in most Obsidian vaults — they conflate raw and derived material in one folder tree.
- Filenames are typically Title Case (`Some Note.md`) while this vault uses kebab-case (`some-note.md`) — every wikilink needs rewriting.
- Wikilinks may point to notes that don't exist in the source vault either, or to notes the user does not want ingested.
- The source vault may be enormous (1k+ notes); blind ingest would blow past every efficiency rule in CLAUDE.md.

So the command is a **pipeline with a human-in-the-loop checkpoint**, not a one-shot import.

## Phased pipeline

### Phase 1 — Discovery (always runs, writes nothing)

1. Walk `source_vault_path` recursively. Collect every `.md` file. Skip:
   - `.obsidian/`, `.trash/`, `.git/`
   - Anything matching `**/templates/**`, `**/_attachments/**`, `**/Excalidraw/**` (configurable later)
   - Files smaller than ~50 bytes (effectively empty)
2. For each note, extract:
   - filename, relative path within source vault, size, mtime
   - YAML frontmatter (if present)
   - presence of: a `source:` / `url:` field; outbound `[[wikilinks]]`; embedded images `![[...]]`; web clipper signatures (`tags: clippings`, certain authors plugins use)
   - rough word count and a one-line opener (first non-empty line of body)
3. Build an in-memory inventory. Persist to `plans/ingest-vault-inventory.json` so a later phase can resume without re-walking.

### Phase 2 — Classification (LLM-assisted, writes nothing)

For each inventoried note, decide a target slot. Rules in priority order:

1. **Has a `source:` or `url:` field, or matches a Web Clipper template** → `sources/<category>/` (raw layer). Pick the category from CLAUDE.md (currently `ai`, `business-development`, `financial-markets`, `hedge-funds`); fall back to a source-type folder (`arxiv`, `substack`, `youtube`, `books`) when the URL host or frontmatter makes it obvious (arxiv.org, substack.com, youtube.com, etc.).
2. **Matches a daily-note pattern** (`YYYY-MM-DD.md` or similar) → `inbox/` for later triage. Daily notes are usually fragmented thoughts — exactly what `/ingest-inbox` is designed to absorb.
3. **Looks like an atomic wiki page** (single topic, has prose, has wikilinks, no `source:` field, > ~150 words) → `wiki/<category>/` directly. Apply the second-mention rule retroactively only when the user opts in (see open questions).
4. **Anything else** (very short notes, fleeting ideas, drafts) → `inbox/`.
5. **Cannot classify with confidence** → flag for the user; do NOT auto-route.

Use a small-context classifier loop: 10–20 notes per LLM call, each call returns target folder + confidence + 1-line reason. Cache results in the inventory file.

### Phase 3 — User review checkpoint

Before any write, print a compact summary:
- Counts per target slot (e.g., `sources/ai`: 42, `inbox/`: 318, `wiki/ai/`: 11, flagged: 7)
- Sample of 5–10 notes per slot with their reason
- List of all flagged notes

Wait for the user to approve, edit the classification (e.g., "move all the daily notes to inbox/processed/ instead", "skip everything tagged #personal"), or abort.

If `--dry-run`, stop here and write only the report.

### Phase 4 — Filename + wikilink normalization

For each note that survived review:

1. **Compute the new filename**: kebab-case the title (frontmatter `title:` if present, else the H1, else the existing filename). Strip punctuation, collapse whitespace, lowercase, truncate to ~80 chars. Disambiguate collisions by appending a short hash of the original path.
2. **Build a rename map** `old_path → new_path` for every note in scope. Persist to `plans/ingest-vault-renames.json`.
3. **Rewrite wikilinks in the body**:
   - `[[Some Note]]` → `[[some-note|Some Note]]` (use the piped form per CLAUDE.md's wikilink rule)
   - `[[Some Note|Display Text]]` → `[[some-note|Display Text]]`
   - `[[Some Note#Heading]]` → `[[some-note#heading|Some Note > Heading]]`
   - Targets not in the rename map (links to notes that won't be ingested) — leave as-is but record them in `plans/ingest-vault-broken-links.md` for later cleanup.
4. **Embeds (`![[image.png]]`)** — see Attachments below.

### Phase 5 — Frontmatter normalization

Map the source frontmatter onto this vault's schema:

| Source field          | Target field              | Notes |
|-----------------------|---------------------------|-------|
| `title`               | `title`                   | Fall back to H1 then filename |
| `date` / `created`    | `date`                    | ISO YYYY-MM-DD; fall back to file mtime |
| `tags`                | `tags`                    | Convert flat tags to nested form (`#ai` → `ai/general`) only on user opt-in |
| `aliases`             | `aliases`                 | Pass through |
| `source` / `url`      | `source`                  | For sources/ files |
| `author`              | `author`                  | For sources/ files |
| anything else         | preserve under same key   | Don't drop user data |

Always inject `created: <today>` to record when the note was ingested into this vault.

### Phase 6 — Write

1. Write each transformed note to its target path. Use `Write` for new files. If a target file already exists:
   - **In `sources/`**: skip (sources/ is immutable). Log the conflict.
   - **In `wiki/`**: do NOT overwrite. Append the new content to the existing page under a `## Imported from <source vault>` heading, OR write to `<name>-imported.md` and flag for manual merge. Default to the latter — safer.
   - **In `inbox/`**: append a numeric suffix (`-1`, `-2`).
2. Update `wiki/index.md` — add an entry for every new wiki page (skip pages going to `inbox/` or `sources/`).
3. Append a single batch entry to `wiki/log.md`:
   `2026-04-26 | ingest-vault | <N> notes imported from <source_vault_path> | <breakdown>`

### Phase 7 — Post-import lint

Automatically run `/maintain-wiki` once Phase 6 finishes. Expected hits: many broken wikilinks (the ones we logged in Phase 4) and several orphan pages. The maintain pass turns the import into a clean baseline rather than leaving cruft for the user to discover later.

## Attachments

Three options, decide before implementing:

- **(A) Skip entirely** — embeds become broken links. Cleanest, loses information.
- **(B) Copy referenced attachments only** to `_attachments/` at the target vault root, rewrite embed paths. Preserves visual content; bounded blast radius.
- **(C) Mirror the source vault's attachment folder wholesale.** Largest disk footprint; preserves attachments not yet referenced.

Recommend **(B)** as the default. Ship (A) as `--no-attachments`.

## Idempotency and resumability

- All inventory, classification, and rename maps live under `plans/ingest-vault-*.json`. A subsequent run reads them rather than recomputing.
- Each note's target path is deterministic (kebab-case + path-hash for collisions), so re-running on the same source vault produces the same target paths.
- A note already present in the target vault (matched by `source` URL for `sources/`, by EntryID-equivalent for everything else — frontmatter `imported_from: <source_path>`) is skipped.
- Add `imported_from: <source_vault_path>` and `imported_at: <timestamp>` frontmatter on every imported note so future re-imports can detect prior work without scanning content.

## Safety

- **Source vault is read-only.** The command must never write to or delete from `source_vault_path`. Verify by canonicalizing both paths and refusing to run if `source_vault_path == cwd` or is a subpath of it.
- **Default to dry-run.** First invocation always reports without writing, even if the user omits the flag. Require explicit `--apply` (or a confirmation prompt) on the first real run.
- **No bulk wiki edits without sign-off.** The user-review checkpoint in Phase 3 is non-skippable — the command should not auto-route hundreds of notes silently.

## Reporting (end-of-run)

```
Ingested from: <source_vault_path>
Notes scanned: 1,247
Notes ingested: 893
  → sources/: 142 (ai: 87, business-development: 33, financial-markets: 22)
  → wiki/:    74 (across 4 categories)
  → inbox/:   677
Notes skipped: 354 (252 templates/empty, 89 already imported, 13 user-rejected)
Conflicts:    7 (listed in plans/ingest-vault-conflicts.md)
Broken links: 218 (listed in plans/ingest-vault-broken-links.md)
Wiki pages added to index: 74
Lint pass: ran clean / N issues (see wiki/log.md)
```

Append the same summary as a single row in `wiki/log.md`.

## Open questions to resolve before implementing

1. **Tag normalization.** This vault uses nested tags (`ai/coding`). Source vaults usually have flat tags. Auto-convert with an LLM, or pass through verbatim and let the user clean up via `/maintain-wiki`?
2. **Default bucket for unclassifiable notes.** `inbox/` (lets `/ingest-inbox` handle them) or `wiki/_unclassified/` (keeps them visible)?
3. **Daily notes.** Concatenate one month's daily notes into a single `inbox/2026-04-daily.md`, or import each as its own file?
4. **Existing wiki overlap.** When an imported note's topic matches an existing wiki page (`automation-calculus.md` already exists, source vault has `Automation Calculus.md`) — auto-merge, write side-by-side as `automation-calculus-imported.md`, or stop and ask per-conflict? Default proposed: side-by-side + flag.
5. **Wikilink rewrite scope.** Only rewrite links whose target is in the rename map, or also probe for "did you mean" matches against existing target-vault pages?
6. **Should the command modify CLAUDE.md** to add new categories that emerge from the import (e.g., source vault has lots of "Stoicism" notes that don't fit any current category)? Default proposed: never auto-edit CLAUDE.md; surface a recommendation in the end-of-run report.
7. **Attachment policy** (see Attachments section).

## Out of scope (v1)

- Two-way sync. This is a one-time import, not a live mirror.
- Plugin data and `.obsidian/workspace.json` migration.
- Canvas (`.canvas`) and Bases (`.base`) files. Add later via the matching skills.
- Note history / git log of the source vault.

## Implementation order

1. Phase 1 (discovery) — pure walker, no LLM. Smallest first slice.
2. Phase 2 (classification) — wire in the LLM classifier loop with caching.
3. Phase 3 (review checkpoint) — printing + parsing user edits.
4. Phases 4–6 (transform + write) — the actual ingest, gated behind `--apply`.
5. Phase 7 (auto-lint) — last; trivially calls `/maintain-wiki`.

Ship Phase 1+2+3 as a "preview-only" command first. Real writes come in a follow-up PR after the previewed classifications have been validated against a real source vault.
