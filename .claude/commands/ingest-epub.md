Ingest an EPUB book into the wiki: extract chapters + images, summarize each
chapter via subagents, then synthesize wiki pages with figures embedded.

This command vendors the [EPUB2MD4Claude](https://github.com/michaelbiafore/EPUB2MD4Claude)
package locally (at `scripts/epub2md/`, pinned to upstream tag
`vendored-2026-04-28`). One-time bootstrap if `scripts/epub2md/.venv/` does
not exist yet:

```bash
cd scripts/epub2md && uv venv && uv pip install -e .
```

If the venv is missing when this command runs, run the bootstrap first
before the conversion step.

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
scripts/epub2md/.venv/Scripts/python.exe -c "
from pathlib import Path
from epub2md.extractor import EPUBExtractor
e = EPUBExtractor(Path(r'<EPUB-PATH>'))
print(repr(e.title), '|', repr(e.author))
"
```

Construct slug as `<author-last>-<short-title>-<year>`, kebab-case,
lowercased, sanitized (alphanumeric + hyphens only), truncated to ~40
chars. Example: *Time Series Forecasting Using Foundation Models* by
Marco Peixeiro, 2025 → `peixeiro-tsfm-2025`.

If `sources/books/<slug>/` already exists:
- If `--force` is set, proceed (overwrite chapter files; image dir will
  be replaced).
- Otherwise stop and ask the user to use `--slug <override>` or `--force`.

### 3. Convert EPUB → markdown + images

```bash
scripts/epub2md/.venv/Scripts/epub2md.exe "<EPUB-PATH>" -o "sources/books/<slug>" -v
```

Verify the output dir has at least:
- One or more `NNN_*.md` chapter files
- `Table_of_Contents.md`
- `images/` directory with > 0 images
- `ChapterAbstracts.md`

### 4. Scan for content chapters

```bash
scripts/epub2md/.venv/Scripts/epub2md-summarize.exe scan "sources/books/<slug>"
```

Parse the JSON output. Each entry has `{path, filename, title, word_count, target_min, target_max}`.
Front/back matter (cover, contents, dedication, copyright, index, etc.) and
chapters under 500 bytes are auto-filtered out.

If `--skip-synthesis` was passed, jump to step 8 (frontmatter) and stop.

### 5. Summarize each content chapter via Agent subagents

For each chapter in the scan results, dispatch an `Agent` (subagent_type:
`general-purpose`) with the prompt template below. Launch in batches of
`--max-parallel` (default **3**) — call multiple Agent tools in a single
message for parallelism, wait for the batch to complete, then start the
next batch. This avoids subagent rate-limit issues on long books.

**Prompt template:**

```
Read the chapter at {path}. Write a summary of this book chapter between
{target_min} and {target_max} words.

Preserve key concepts, arguments, examples, and chapter structure.
Use markdown formatting with headings that mirror the chapter's sections.
Write the summary to {path_dir}/Sum_{filename}.
Do NOT include YAML frontmatter in the summary.

## Image Handling — Math Equations

This book may use image-based math: equations appear as
`![](images/<file>.png)` or similar references. The actual image files
are on disk at `{path_dir}/images/` and you can view them with the Read
tool to see what each equation contains.

Your key task: identify the most important equations in the chapter and
INCLUDE their exact `![](images/...)` references in your summary. To do
this:
1. Scan the chapter for all `![](images/...)` references.
2. Use the Read tool to view a sample of the referenced image files so
   you know what equations / figures they represent.
3. Select the equations that are most important — defining formulas, key
   theorems, central results, or equations that later sections build
   upon.
4. Include those image references inline in your summary at the
   appropriate location, preserving the exact markdown syntax.

Guidelines:
- Aim to include 3-8 key equation / figure images per chapter (fewer for
  short chapters).
- Prioritize: definitions, theorem statements, main results, and
  equations referenced repeatedly throughout the chapter.
- For large figure images (diagrams, block diagrams, charts), include
  them only if they are central to the chapter's argument.
- Do NOT include every image — only those essential to understanding key
  concepts.
```

If a subagent fails on a chapter, log the failure but continue with
remaining chapters. The final report should surface failed chapters.

### 6. Assemble concatenated summary

```bash
scripts/epub2md/.venv/Scripts/epub2md-summarize.exe assemble "sources/books/<slug>"
```

Produces `Sum_<book-title>.md` in the same directory.

### 7. Add YAML frontmatter to each `Sum_*.md`

For each `Sum_*.md` file in `sources/books/<slug>/`, prepend frontmatter
matching this shape (use the metadata extracted in step 2):

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

### 8. Synthesize wiki pages

This is the judgment-heavy step. The pattern, drawn from the Peixeiro
ingest:

#### 8a. Read the book overview

Read the concatenated `Sum_<book-title>.md`. Skim each per-chapter
summary. Identify:
- **What the book is about** (top-level scope, target audience, era)
- **Which chapters cover models/topics that already have wiki pages**
  (look in `wiki/index.md` first per the index-first rule)
- **Which chapters introduce models/topics with no existing wiki page**
  (candidates for new entity pages)
- **Which chapters are too short / part-divider-only / references** to
  warrant a dedicated wiki page

#### 8b. Decide page set

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

#### 8c. Write the wiki pages

Each page should embed **3-6 figures liberally**, drawn from
`sources/books/<slug>/images/`, via vault-relative paths:

```markdown
![Caption describing the figure](../../sources/books/<slug>/images/<file>.png)
```

For pages in `wiki/<category>/`, the relative path is
`../../sources/books/<slug>/images/<file>.png` regardless of category.

Cross-reference existing entity pages where they exist (use
`[[wikilink|Display Text]]` style) and forward-link to other chapter
pages.

#### 8d. Apply the second-mention rule

If any model / framework / concept named in this book has been
substantively mentioned in a prior wiki source but doesn't have its own
entity page yet, this is the second substantive mention and merits
promotion. Create the entity page now and cross-link it from the chapter
page that introduced it. (Track these as "promotion candidates" notes
inline if you defer.)

### 9. Update `wiki/index.md`

Pick the category from CLAUDE.md's Categories table that best fits the
book's primary topic. Under that category section, add a "Books"
subsection (create if missing) with a parent entry for the new book and
bulleted children for each per-chapter page. If new entity pages were
created in step 8d, add them under the same category — or under whichever
category the entity belongs to if it's broader than the book's scope.

Always re-check CLAUDE.md's Categories table — it is the source of truth
and may have been personalized.

### 10. Append to `wiki/log.md`

One batch row covering the whole ingest. Include:
- The book title and slug
- Source files written (`sources/books/<slug>/`) with file count and image count
- Wiki pages created (full list)
- New entity pages promoted (if any) and the promotion rationale
- Skipped chapters and the reason (front matter, < 500 bytes, etc.)
- Touch budget note (this will exceed the 5-page soft cap; that's
  expected for a book ingest)

### 11. Report

Final report to the user:

```
Book ingested: <title>
Slug: <slug>
Chapters summarized: N (skipped M as front/back matter)
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
- **Math-heavy books:** the subagent prompt explicitly handles image-based
  math. Trust it; don't try to pre-process equations yourself.
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
| `.pdf` file | `pdf2md` (planned at `scripts/pdf2md/`) | `/ingest-inbox`, `/ingest-url` |
| **`.epub` file** | **`scripts/epub2md/` (this command)** | **`/ingest-epub`** |
| Other web article | `defuddle` (`npx defuddle`) | `/ingest-url` |
