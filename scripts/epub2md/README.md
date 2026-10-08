# scripts/epub2md/

Vendored copy of [EPUB2MD4Claude](https://github.com/michaelbiafore/EPUB2MD4Claude),
adapted for the ts-fms wiki's `/ingest-epub` slash command. Provides two
console scripts: `epub2md` (EPUB → structured Markdown chapters + images)
and `epub2md-summarize` (chapter scanner, book-summary planner, and
summary assembler).

## Upstream pin

==**Vendored from upstream commit `879684c`, tag `vendored-2026-04-28`.**==

That commit is the snapshot at which the package was vendored into this
repo. The full commit message and diff explain the four substantive
changes since the upstream's initial commit (`a84a173`):

- `extractor.py` — image extraction + smarter title fallback
- `converter.py` — CSS roles + MathML→LaTeX + verbose logging
- `cli.py` — wires up image extraction and verbose flag
- `.claude/commands/summarize-chapters.md` — math-equation handling guidance

Both `.claude/settings.local.json` (per-machine permissions) and the
upstream repo's untracked `plans/` directory are *not* part of this
vendoring. Those are local state in the upstream that aren't relevant to
the wiki integration.

To reproduce this vendored state from upstream:

```bash
git clone https://github.com/michaelbiafore/EPUB2MD4Claude.git
cd EPUB2MD4Claude
git checkout vendored-2026-04-28
# src/epub2md/ here matches scripts/epub2md/src/epub2md/ in the wiki
```

## One-time setup

Bootstrap the venv once per machine (after cloning the wiki, before first
use of `/ingest-epub`):

```bash
cd scripts/epub2md
uv venv
uv pip install -e .
```

This creates `scripts/epub2md/.venv/` (gitignored) and installs the
`epub2md-vendored` package in editable mode. Two console scripts become
available at:

- `scripts/epub2md/.venv/Scripts/epub2md.exe`
- `scripts/epub2md/.venv/Scripts/epub2md-summarize.exe`

The slash command invokes them by full path; the venv does **not** need to
be activated.

## Usage

```bash
# Convert an EPUB to per-chapter Markdown + images
.venv/Scripts/epub2md.exe /absolute/path/to/book.epub \n    -o /absolute/path/to/sources/books/<slug>

# List content chapters as JSON (used by the slash command)
.venv/Scripts/epub2md-summarize.exe scan /absolute/path/to/sources/books/<slug>
```

Don't run these by hand for routine ingest — use `/ingest-epub` instead.

## Summaries: two different things

| Artifact | Produced by | How |
|---|---|---|
| `ChapterAbstracts.md` | `epub2md` during conversion | **Regex heuristics** (`abstract_writer.py`) — a first-paragraph excerpt plus keyword lists. Offline, free, and not a real summary. |
| `Sum_<NN>_<chapter>.md` | `/summarize-chapters` | **LLM**, one Claude Code subagent per content chapter, key figures/equations embedded. |
| `Book_Summary_<Title>.md` | `/summarize-chapters` | **LLM**, one subagent synthesizing the whole book *from the chapter summaries*. |
| `Sum_<Title>.md` | `epub2md-summarize assemble` | Mechanical stitch: the book-level summary followed by every chapter summary. |

No API key is involved. The LLM work is done by Claude Code subagents
dispatched by the slash command; this package never calls a model.

## The `epub2md-summarize` CLI

Three subcommands, all mechanical — they tell the subagents what to read and
then join up the results:

```bash
# 1. Which chapters are real content, and how long should each summary be?
epub2md-summarize scan <absolute-md-dir>

# 2. Which chapter summaries exist, which are missing, how long should the
#    book-level summary be, and where should it be written?
epub2md-summarize book-plan <absolute-md-dir>

# 3. Stitch the book-level summary + all chapter summaries into one file.
epub2md-summarize assemble <absolute-md-dir>
```

`scan` emits `path`, `filename`, `title`, `word_count`, `target_min`,
`target_max`, `figure_count`, `summary_path`. `book-plan` emits
`chapter_summaries[]`, `missing_summaries[]`, `total_summary_words`,
`target_min`/`target_max`, `book_summary_path`, `concatenated_path`.

> [!important] Path contract
> `md_dir` is **required** and resolved to an absolute path; every path emitted
> is absolute. There is no `md_out` default, nothing depends on the working
> directory, and nothing assumes a sibling repository is checked out nearby.

`assemble` exits **1** rather than writing a title-only stub when no
`Sum_<NN>_*.md` files exist yet, so a failed summarization run cannot look like
a successful one. It is idempotent — re-running is safe. Avoid `-o`: the
summaries carry relative `images/...` references that only resolve while they
sit beside the `images/` directory.

## Output structure

For an EPUB with title `<title>`, `epub2md ... -o <abs>/sources/books/<slug>`
produces:

```
sources/books/<slug>/
  000_<chapter_name>.md           One file per spine item, with YAML
  001_<chapter_name>.md           frontmatter (title, source_file).
  ...
  Table_of_Contents.md            Nested list with chapter links.
  Index.md                        Alphabetical book index, if present.
  ChapterAbstracts.md             Auto-generated 3-12-line abstracts.
  images/                         All images extracted from the EPUB.
    *.png, *.jpg, ...
```

After `/ingest-epub` completes summarization, the same directory also
contains:

```
  Sum_NNN_<chapter_name>.md       One LLM summary per content chapter (skips
                                  cover, copyright, contents, dedication,
                                  acknowledgments, index, part dividers, and
                                  anything < 500 bytes).
  Book_Summary_<title>.md         LLM whole-book synthesis, written from the
                                  per-chapter summaries above.
  Sum_<book-title>.md             The book-level summary followed by every
                                  per-chapter summary.
```

## Routing — when to use which tool

The wiki has three vendored ingestion paths, each for a different source
shape:

| Source | Tool | Slash command |
|---|---|---|
| Substack URL | `scripts/fetch_substack.py` (PEP 723 self-installing) | `/ingest-url` |
| `.pdf` file | `scripts/pdf2md/` (vendored) | `/ingest-pdf`, `/ingest-inbox`, `/ingest-url` |
| **`.epub` file** | **`scripts/epub2md/` (this dir)** | **`/ingest-epub`** |
| Other web article | `defuddle` (Node.js, `npm install -g defuddle`) | `/ingest-url` |

## Why a real venv (not PEP 723)?

Unlike `scripts/fetch_substack.py` (single-file PEP 723), this is a
multi-module package with two `[project.scripts]` entry points. PEP 723
inline metadata works for single-file scripts; multi-module packages with
console scripts need a real venv + editable install.

## Known limitations

- **MathML → LaTeX** conversion in `converter.py` requires `pandoc` on
  PATH. Without pandoc, math expressions fall back to placeholder
  rendering. Install pandoc separately if your EPUB uses MathML (most
  technical EPUBs use image-based math, not MathML — see the
  `summarize-chapters.md` prompt for the image-based math story).
- **No EPUB-via-URL** support yet. Pass a local file path. Download
  separately if needed.
