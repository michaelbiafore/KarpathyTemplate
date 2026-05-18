# scripts/epub2md/

Vendored copy of [EPUB2MD4Claude](https://github.com/michaelbiafore/EPUB2MD4Claude),
adapted for the ts-fms wiki's `/ingest-epub` slash command. Provides two
console scripts: `epub2md` (EPUB → structured Markdown chapters + images)
and `epub2md-summarize` (chapter scanner + summary assembler).

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
.venv/Scripts/epub2md.exe path/to/book.epub -o sources/books/<slug>

# List content chapters as JSON (used by the slash command)
.venv/Scripts/epub2md-summarize.exe scan sources/books/<slug>

# Concatenate per-chapter Sum_*.md files into Sum_<book-title>.md
.venv/Scripts/epub2md-summarize.exe assemble sources/books/<slug>
```

Don't run these by hand for routine ingest — use `/ingest-epub` instead.

## Output structure

For an EPUB with title `<title>`, `epub2md ... -o sources/books/<slug>`
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
  Sum_NNN_<chapter_name>.md       One summary per content chapter (skips
                                  cover, copyright, contents, dedication,
                                  acknowledgments, index, etc., and
                                  anything < 500 bytes).
  Sum_<book-title>.md             Concatenated whole-book summary.
```

## Routing — when to use which tool

The wiki has three vendored ingestion paths, each for a different source
shape:

| Source | Tool | Slash command |
|---|---|---|
| Substack URL | `scripts/fetch_substack.py` (PEP 723 self-installing) | `/ingest-url` |
| `.pdf` file | `pdf2md` (planned vendoring at `scripts/pdf2md/`) | `/ingest-inbox`, `/ingest-url` |
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
