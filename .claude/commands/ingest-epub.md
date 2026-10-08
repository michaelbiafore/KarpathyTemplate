Ingest an EPUB book into the wiki: extract chapters + images, summarize each
chapter via subagents, then synthesize wiki pages with figures embedded.

This command vendors the [EPUB2MD4Claude](https://github.com/michaelbiafore/EPUB2MD4Claude)
package locally (at `scripts/epub2md/`, pinned to upstream tag
`vendored-2026-04-28`).

## Path contract

Resolve the vault root once, absolutely, and build every other path from it.
Nothing here depends on the working directory or on any sibling repository
being checked out nearby:

```bash
ROOT="$(git rev-parse --show-toplevel)"
EPUB2MD="$ROOT/scripts/epub2md/.venv/Scripts/epub2md.exe"      # Windows
[ -x "$EPUB2MD" ] || EPUB2MD="$ROOT/scripts/epub2md/.venv/bin/epub2md"   # POSIX
VENV_PY="$ROOT/scripts/epub2md/.venv/Scripts/python.exe"
[ -x "$VENV_PY" ] || VENV_PY="$ROOT/scripts/epub2md/.venv/bin/python"
```

One-time bootstrap if `$ROOT/scripts/epub2md/.venv/` does not exist yet — run
it before the conversion step:

```bash
cd "$ROOT/scripts/epub2md" && uv venv && uv pip install -e .
```

## Usage

```
/ingest-epub <path-to.epub>                   # default behaviour
/ingest-epub <path> --slug <override>         # override book slug
/ingest-epub <path> --max-parallel 5          # bump subagent batch size
/ingest-epub <path> --skip-synthesis          # stop after summary assembly
```

## Pipeline

### 1. Validate input

- Confirm `$ARGUMENTS` parses to a path that exists and ends in `.epub`.
- If it doesn't, print usage and stop.

### 2. Derive book slug

Read the EPUB's metadata (title, author, year) using a one-liner
against the vendored package:

```bash
"$VENV_PY" -c "
from pathlib import Path
from epub2md.extractor import EPUBExtractor
e = EPUBExtractor(Path(r'<ABSOLUTE-EPUB-PATH>'))
print(repr(e.title), '|', repr(e.author))
"
```

Construct slug as `<author-last>-<short-title>-<year>`, kebab-case,
lowercased, sanitized (alphanumeric + hyphens only), truncated to ~40
chars. Example: *Time Series Forecasting Using Foundation Models* by
Marco Peixeiro, 2025 → `peixeiro-tsfm-2025`.

If `$ROOT/sources/books/<slug>/` already exists:
- If `--force` is set, proceed (overwrite chapter files; image dir will
  be replaced).
- Otherwise stop and ask the user to use `--slug <override>` or `--force`.

### 3. Convert EPUB → markdown + images

```bash
BOOK_DIR="$ROOT/sources/books/<slug>"
"$EPUB2MD" "<ABSOLUTE-EPUB-PATH>" -o "$BOOK_DIR" -v
```

Verify the output dir has at least:
- One or more `NNN_*.md` chapter files
- `Table_of_Contents.md`
- `images/` directory with > 0 images
- `ChapterAbstracts.md`

### 4. Summarize the chapters and the book

Delegate to `/summarize-chapters`, which handles the scan, the per-chapter
Agent subagents, the book-level synthesis subagent, and the final assembly:

```
/summarize-chapters "$BOOK_DIR" --tool epub --max-parallel <N>
```

Pass `--max-parallel` through from this command (default **3**). That command
produces, all inside `$BOOK_DIR`:

| File | Content |
|---|---|
| `Sum_<NNN>_<chapter>.md` | one LLM summary per content chapter, key equations/figures embedded |
| `Book_Summary_<Title>.md` | whole-book synthesis, built from the chapter summaries |
| `Sum_<Title>.md` | the book-level summary followed by every chapter summary |

Front/back matter and sub-500-byte chapters are filtered out by its `scan`
step; part dividers (`Part0001`, `Part I:`) are dropped too. Note any chapters
it reports as failed and carry them into the final report.

If `--skip-synthesis` was passed, stop after this step and jump to step 5
(frontmatter) — the summaries are on disk and the wiki pages are the part being
skipped.

### 5. Add YAML frontmatter to each `Sum_*.md`

For each `Sum_*.md` and `Book_Summary_*.md` file in `$BOOK_DIR`, prepend
frontmatter matching this shape (use the metadata extracted in step 2):

```yaml
---
title: "<chapter title from H1>"
book: "<book title>"
author: "<author>"
publisher: "<publisher if known>"
published: <year if known>
created: <today's date in YYYY-MM-DD>
tags:
  - books
  - <slug>
  - ai/time-series-forecasting          # or other relevant category
  - ai/foundation-models                  # if applicable
---
```

A small Python loop with `pathlib` is the simplest implementation; see
how the Peixeiro batch did it (commit `c823e6f`) for a working example.

> [!warning] Do this after step 4, never before
> `assemble` strips frontmatter from the book-level summary when it embeds it,
> and it rewrites `Sum_<Title>.md` wholesale. Frontmatter added here survives
> only because step 4 has already finished. If you re-run
> `/summarize-chapters` afterwards, re-apply this step.

### 6. Synthesize wiki pages

This is the judgment-heavy step. The pattern, drawn from the Peixeiro
ingest:

#### 6a. Read the book overview

Start with `Book_Summary_<Title>.md` — the book-level synthesis from step 4. It
already states the scope, the argument, the named frameworks, and the
takeaways, which is most of what this step needs. Then read the per-chapter
summaries in `Sum_<Title>.md` for the detail the synthesis compressed away.

> [!warning] Don't synthesize wiki pages from the book-level summary alone
> It is deliberately lossy. The per-chapter/new-entity decision in 6b and the
> second-mention rule in 6d both depend on knowing what each individual chapter
> covers, so you still need a pass over the chapter summaries.

Identify:
- **What the book is about** (top-level scope, target audience, era)
- **Which chapters cover models/topics that already have wiki pages**
  (look in `wiki/index.md` first per the index-first rule)
- **Which chapters introduce models/topics with no existing wiki page**
  (candidates for new entity pages)
- **Which chapters are too short / part-divider-only / references** to
  warrant a dedicated wiki page

#### 6b. Decide page set

For each substantive chapter, decide between:
- **Per-chapter page** named `<slug>-ch<N>-<topic>.md` for chapters
  covering existing models. Goal: capture what *this book* says about
  that model — its tutorial code, specific benchmarks, author's
  perspective — without duplicating the entity page.
- **New entity page** named `<topic>.md` (clean name, no `<slug>-` prefix)
  for chapters introducing a new model with no existing wiki page. The
  chapter content *is* the entity page.

Always create one **book-overview wiki page**: `<slug>-book.md`, with:
- Book metadata + summary (from frontmatter and the concatenated file)
- Top takeaways (3-5 bullets, drawn from the most important chapters)
- Hyperlinks to all per-chapter pages
- Capstone results, if the book has them
- Related links to existing entity pages

#### 6c. Write the wiki pages

Each page should embed **3-6 figures liberally**, drawn from
`$BOOK_DIR/images/`, via vault-relative paths:

```markdown
![Caption describing the figure](../../sources/books/<slug>/images/<file>.png)
```

For pages in `wiki/<category>/`, the relative path is
`../../sources/books/<slug>/images/<file>.png` regardless of category.

Cross-reference existing entity pages where they exist (use
`[[wikilink|Display Text]]` style) and forward-link to other chapter
pages.

#### 6d. Apply the second-mention rule

If any model / framework / concept named in this book has been
substantively mentioned in a prior wiki source but doesn't have its own
entity page yet, this is the second substantive mention and merits
promotion. Create the entity page now and cross-link it from the chapter
page that introduced it. (Track these as "promotion candidates" notes
inline if you defer.)

### 7. Update `wiki/index.md`

Pick the category from CLAUDE.md's Categories table that best fits the
book's primary topic. Under that category section, add a "Books"
subsection (create if missing) with a parent entry for the new book and
bulleted children for each per-chapter page. If new entity pages were
created in step 6d, add them under the same category — or under whichever
category the entity belongs to if it's broader than the book's scope.

Always re-check CLAUDE.md's Categories table — it is the source of truth
and may have been personalized.

### 8. Append to `wiki/log.md`

One batch row covering the whole ingest. Include:
- The book title and slug
- Source files written (`sources/books/<slug>/`) with file count and image count
- Wiki pages created (full list)
- New entity pages promoted (if any) and the promotion rationale
- Skipped chapters and the reason (front matter, < 500 bytes, etc.)
- Touch budget note (this will exceed the 5-page soft cap; that's
  expected for a book ingest)

### 9. Report

Final report to the user:

```
Book ingested: <title>
Slug: <slug>
Chapters summarized: N (skipped M as front/back matter, K failed)
Book-level summary: Book_Summary_<Title>.md (<words> words)
Stitched summary: Sum_<Title>.md
Figures preserved: <count>
Wiki pages created: <count> (list paths)
New entity pages: <count> (if any)
Total runtime: <minutes>
Failed chapters: <list> (if any)
```

## Notes

- **Long books (>30 chapters):** the default `--max-parallel 3` keeps
  subagent rate consumption modest. Bump to 5 if the book is short and
  you want speed.
- **Math-heavy books:** the chapter-subagent prompt in `/summarize-chapters`
  explicitly handles image-based math. Trust it; don't try to pre-process
  equations yourself.
- **`ChapterAbstracts.md` is not a summary.** `epub2md` emits it during
  conversion from regex heuristics (`abstract_writer.py`) — a first-paragraph
  excerpt plus keyword lists. The LLM summaries are the `Sum_*` and
  `Book_Summary_*` files from step 4. Don't build wiki pages off the
  abstracts file.
- **Books overlapping existing wiki coverage:** prefer focused per-chapter
  pages that cross-reference existing entity pages over duplicating their
  content. Example: a chapter on STPA in a book that follows after the
  wiki already has `stpa.md` and a few related entity pages — write a
  single `<slug>-ch<N>-stpa.md` that captures the book's specific
  treatment (case studies, the author's framing) and links to the
  existing pages rather than restating their content.
- **Don't synthesize first, then realize you should have read more.** Read
  every substantive chapter summary before deciding the page set, even
  if that means a longer read pass. The second-mention rule and the
  decision between per-chapter and new-entity pages depend on having the
  full picture.
- **Cleanup on failure:** if you abort partway, leave the populated
  `sources/books/<slug>/` directory in place. The user can `rm -rf` if
  they want a clean slate. Auto-rollback risks deleting work the user
  intended to keep.

## Routing reminder

| Source shape | Tool | Slash command |
|---|---|---|
| Substack URL | `scripts/fetch_substack.py` | `/ingest-url` |
| `.pdf` file | `scripts/pdf2md/` (vendored package) | `/ingest-pdf`, `/ingest-inbox`, `/ingest-url` |
| **`.epub` file** | **`scripts/epub2md/` (this command)** | **`/ingest-epub`** |
| Other web article | `defuddle` (`npx defuddle`) | `/ingest-url` |
