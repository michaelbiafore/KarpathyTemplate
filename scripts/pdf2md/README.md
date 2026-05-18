# scripts/pdf2md/

Vendored copy of PDF2MD4Claude. Provides two console scripts: `pdf2md`
(PDF → structured Markdown chapters + extracted images) and
`pdf2md-summarize` (chapter summary helper). Used by `/ingest-inbox` and
`/ingest-url` whenever a `.pdf` file or URL is encountered.

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
.venv/Scripts/pdf2md.exe path/to/paper.pdf -o /tmp/pdf_out

# View the help
.venv/Scripts/pdf2md.exe --help
```

The slash commands `/ingest-inbox` and `/ingest-url` handle PDF routing
automatically — don't run `pdf2md.exe` by hand for routine ingest.

## What it produces

For an input PDF, `pdf2md` produces:

- **Single-document PDFs** (papers, blog-post prints): one
  `01_Full_Document.md` plus `images/`, `Table_of_Contents.md`,
  `ChapterAbstracts.md`.
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
