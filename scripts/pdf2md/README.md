# scripts/pdf2md/

Vendored copy of PDF2MD4Claude. Provides two console scripts: `pdf2md`
(PDF → structured Markdown chapters + extracted images) and
`pdf2md-summarize` (chapter scanner, book-summary planner, and summary
assembler). Used by `/ingest-pdf`, `/ingest-inbox`, and `/ingest-url`
whenever a `.pdf` file or URL is encountered, and by `/summarize-chapters`
for LLM summarization.

## Upstream pin

==**Vendored from upstream commit `f50b9ed`**== ("Add image extraction,
chapter summarizer, and README", 2026-04-26).

Source repo: local at `A:\Packages\PDF2MD4Claude\` — no GitHub remote
configured upstream as of vendoring time. The commit `f50b9ed` exists
in the local upstream's history but is not published. If the upstream
gets a remote later, this README should be updated with the URL.

To reproduce this vendored state from the upstream:

```bash
cd A:/Packages/PDF2MD4Claude
git checkout f50b9ed
# src/pdf2md/ here matches scripts/pdf2md/src/pdf2md/ in the wiki
```

## One-time setup

Bootstrap the venv once per machine (after cloning the wiki, before first
PDF ingest):

```bash
cd scripts/pdf2md
uv venv
uv pip install -e .
```

This creates `scripts/pdf2md/.venv/` (gitignored) and installs the
`pdf2md-vendored` package in editable mode. Two console scripts become
available at:

- `scripts/pdf2md/.venv/Scripts/pdf2md.exe`
- `scripts/pdf2md/.venv/Scripts/pdf2md-summarize.exe`

The slash commands `/ingest-inbox` and `/ingest-url` invoke `pdf2md.exe`
by full venv path; the venv does **not** need to be activated.

## Usage

```bash
# Convert a PDF to per-chapter Markdown + extract images
.venv/Scripts/pdf2md.exe /absolute/path/to/paper.pdf -o /absolute/out/dir

# View the help
.venv/Scripts/pdf2md.exe --help
```

The slash commands `/ingest-pdf`, `/ingest-inbox`, and `/ingest-url` handle
PDF routing automatically — don't run `pdf2md.exe` by hand for routine ingest.

## Summaries: two different things

| Artifact | Produced by | How |
|---|---|---|
| `ChapterAbstracts.md` | `pdf2md` during conversion | **Regex heuristics** (`abstract_writer.py`) — a first-paragraph excerpt plus keyword lists. Offline, free, and not a real summary. |
| `Sum_<NN>_<chapter>.md` | `/summarize-chapters` | **LLM**, one Claude Code subagent per content chapter, key figures/equations embedded. |
| `Book_Summary_<Title>.md` | `/summarize-chapters` | **LLM**, one subagent synthesizing the whole book *from the chapter summaries*. |
| `Sum_<Title>.md` | `pdf2md-summarize assemble` | Mechanical stitch: the book-level summary followed by every chapter summary. |

No API key is involved. The LLM work is done by Claude Code subagents
dispatched by the slash command; this package never calls a model.

## The `pdf2md-summarize` CLI

Three subcommands, all mechanical — they tell the subagents what to read and
then join up the results:

```bash
# 1. Which chapters are real content, and how long should each summary be?
pdf2md-summarize scan <absolute-md-dir>

# 2. Which chapter summaries exist, which are missing, how long should the
#    book-level summary be, and where should it be written?
pdf2md-summarize book-plan <absolute-md-dir>

# 3. Stitch the book-level summary + all chapter summaries into one file.
pdf2md-summarize assemble <absolute-md-dir>

# Group adjacent sections into bundles under a word cap, for a finely
# chaptered book where one subagent per chapter would be wasteful.
pdf2md-summarize bundle <absolute-md-dir> --max-words 6000

# List whatever Sum_* files exist, however they were produced.
pdf2md-summarize summaries <absolute-md-dir>
```

`bundle` exists because a 450-page title can split into 150+ TOC entries
averaging a few hundred words each; bundling cuts that to ~20 subagent calls
without losing reading order. `summaries` is the bundle-agnostic companion —
it reports what is on disk rather than deriving expectations from the chapter
list, which is what a whole-book or cliff-notes synthesis stage needs.

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

## What it produces

For an input PDF, `pdf2md` produces:

- **Single-document PDFs** (papers, blog-post prints): one
  `01_Full_Document.md` plus `images/`, `Table_of_Contents.md`,
  `ChapterAbstracts.md`. Not worth summarizing — the wiki page is the summary.
- **Multi-chapter PDFs** (books, theses): one `NN_<chapter_name>.md`
  per detected chapter (via TOC heuristics) plus the same supporting
  files.

Image extraction has filters to drop tiny images (`--min-image-size`,
default 80×80) and recurring images like page-headers (`--image-
recurrence-threshold`, default 0.30 = 30% of pages). These keep the
extracted image count manageable on long PDFs.

## Why a real venv (not PEP 723)?

Same reason as `scripts/epub2md/`: multi-module package with two
`[project.scripts]` entry points. PEP 723 inline metadata is for
single-file scripts; multi-module packages need a real venv + editable
install.

## Routing reminder

| Source shape | Tool | Slash command |
|---|---|---|
| Substack URL | `scripts/fetch_substack.py` (PEP 723) | `/ingest-url` |
| **`.pdf` file** | **`scripts/pdf2md/` (this dir)** | **`/ingest-inbox`, `/ingest-url`** |
| `.epub` file | `scripts/epub2md/` (vendored package) | `/ingest-epub` |
| Other web article | `defuddle` (Node.js) | `/ingest-url` |

## Note on the prior absolute-path references

Before this vendoring, the slash command files
`.claude/commands/ingest-inbox.md` and `.claude/commands/ingest-url.md`
referenced `pdf2md` either by bare command name (assuming PATH) or by
the absolute Windows path
`A:\Packages\PDF2MD4Claude\.venv\Scripts\pdf2md.exe`. Neither would
resolve on a recipient's machine. Both slash commands have been updated
to invoke this vendored copy at `scripts/pdf2md/.venv/Scripts/pdf2md.exe`.
