Ingest a local PDF (paper, report, slide deck) into the second brain wiki:
convert to markdown via the vendored `pdf2md` package, then run the standard
ingest flow.

This is the clean entry point for a PDF **file on disk**. For a PDF at a URL,
use `/ingest-url <url>` (it downloads then routes here). For PDFs already
sitting in `inbox/`, `/ingest-inbox` picks them up. For books (`.epub`), use
`/ingest-epub` instead — it has a dedicated chapter-by-chapter pipeline.

This command uses the vendored `pdf2md` package at `scripts/pdf2md/` (PDF2MD4Claude,
pinned at commit `f50b9ed`). One-time bootstrap if `scripts/pdf2md/.venv/` does
not exist yet:

```bash
cd scripts/pdf2md && uv venv && uv pip install -e .
```

If the venv is missing when this command runs, run the bootstrap first before
the conversion step.

## Usage

```
/ingest-pdf <path-to.pdf>                    # default behaviour
/ingest-pdf <path> --category <cat>          # force a category, skip the prompt
```

## Instructions

### 1. Validate input

- Confirm `$ARGUMENTS` parses to a path that exists and ends in `.pdf`.
- If it doesn't, print usage and stop.
- If the path is a URL (starts with `http`), stop and tell the user to run
  `/ingest-url <url>` instead.

### 2. Check for duplicates

Search `sources/` for a file that already records this PDF in its frontmatter
(`source:` field matching the filename or path). If found, tell the user and
ask whether to re-ingest or skip.

### 3. Convert PDF → markdown

Do **not** call `Read` on a `.pdf` directly — it renders each page as an image,
which is far slower and far more token-expensive than text extraction. Convert
first:

```bash
scripts/pdf2md/.venv/Scripts/pdf2md.exe "<PDF-PATH>" -o /tmp/pdf_out
```

Then `Read` the resulting `.md` from `/tmp/pdf_out`. If the package name is
arxiv-shaped (`NNNN.NNNNN.pdf`) or the content is clearly a research paper,
prefer the `arxiv` source folder in the next step.

### 4. Determine the best category

Pick from the Categories table in CLAUDE.md — it is the source of truth and may
have been personalized, so always re-check it. If it's a research paper, prefer
the `arxiv` source-type folder. If `--category` was passed, use it. If nothing
fits well, ask the user.

### 5. Save the raw source

Write the converted markdown to `sources/<category>/<kebab-case-title>.md` (or
`sources/arxiv/` for papers) with frontmatter:

```yaml
---
title: "<document title>"
source: "<original PDF filename or path>"
author: "<author if found>"
published: <date if found>
created: <today's date>
tags:
  - <relevant tags>
---
```

Followed by the extracted markdown content. If `pdf2md` emitted figures
alongside the markdown, move them next to the source (e.g.
`sources/<category>/<slug>_figs/`) and keep the relative image references intact.

Never leave the only copy in `/tmp` — `sources/` is the immutable record.

### 6. Follow the full ingest workflow

Per CLAUDE.md's Operations → Ingest and the Efficiency invariants:

- Scan `wiki/index.md` first; only open pages that plausibly overlap.
- Create a wiki summary page in `wiki/<category>/` using the standard template
  (frontmatter, callouts, `==highlights==`, nested tags, short wikilinks).
- Apply the **second-mention rule** for entity pages — inline on first mention,
  promote to their own page only on a second source.
- Add **forward** `[[wikilink|Display Text]]` links from the new page to related
  existing pages (lazy backlinks — don't edit other pages just to reciprocate).
- Cap `## Related` at ~8 links; aim to touch 2–5 pages total.
- Update `wiki/index.md`.
- Append to `wiki/log.md`.

### 7. Report

Report which source file was written and which wiki pages were created/updated.

## Routing reminder

| Source shape | Tool | Slash command |
|---|---|---|
| Substack URL | `scripts/fetch_substack.py` | `/ingest-url` |
| **`.pdf` file (local)** | **`scripts/pdf2md/` (this command)** | **`/ingest-pdf`** |
| `.pdf` at a URL | `scripts/pdf2md/` | `/ingest-url` |
| `.pdf` in `inbox/` | `scripts/pdf2md/` | `/ingest-inbox` |
| `.epub` file | `scripts/epub2md/` | `/ingest-epub` |
| Other web article | `defuddle` (`npx defuddle`) | `/ingest-url` |
