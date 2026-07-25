# LLM Wiki Starter Kit

A personal knowledge base managed by Claude Code. Based on [Andrej Karpathy's LLM Wiki pattern](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f).

You feed it sources (web articles, PDFs, EPUB books, Substack posts, quick notes). Claude compiles them into a living wiki of summary pages, entity pages, and cross-references. Everything viewable in Obsidian. All of it gets denser and more connected as you use it.

## What's Inside

```
llm-wiki-starter-kit/
  sources/        Raw, immutable source material (articles, PDFs, books, transcripts)
  inbox/          Quick capture for fleeting thoughts and drops
  wiki/           LLM-generated knowledge pages — Claude writes and maintains this
  CLAUDE.md       The schema that tells Claude how the wiki operates
  SETUP.md        Full new-machine setup walkthrough (read this to enable ingest)
  .claude/
    commands/     5 slash commands: /ingest-url, /ingest-inbox, /ingest-pdf,
                  /ingest-epub, /maintain-wiki
    skills/       5 Obsidian Skills by Steph Ango (Obsidian CEO)
  scripts/        Vendored, self-contained ingestion tooling (travels with the repo):
    pdf2md/         PDF → Markdown  (papers, reports, slide decks)
    epub2md/        EPUB → Markdown (books: per-chapter pages + images)
    fetch_substack.py   Substack posts (incl. paywalled, with your cookies)
```

Everything under `scripts/` is vendored into this repo — there are no external
repositories to clone. A new user only bootstraps two local Python venvs (see
below); the ingestion code itself ships with the kit.

## Setup

**To just read and query the wiki** (queries, `/maintain-wiki`, `/ingest-url` on
plain web articles):

1. Open this folder in Obsidian as a new vault
2. Right-click the folder → "New Terminal at Folder"
3. Run: `claude`
4. Claude Code loads the skills, commands, and schema automatically.

**To ingest PDFs, EPUBs, or Substack posts**, you need a couple of one-time
installs. This is the "everything travels with the repo" part — the tools are
already here, they just need their environments built once per machine:

```bash
# Prerequisite: uv (Python env manager) — https://docs.astral.sh/uv/
#   Windows:  irm https://astral.sh/uv/install.ps1 | iex
#   mac/Linux: curl -LsSf https://astral.sh/uv/install.sh | sh

# Bootstrap the vendored PDF tool (drives /ingest-pdf + PDF drops)
cd scripts/pdf2md && uv venv && uv pip install -e . && cd ../..

# Bootstrap the vendored EPUB tool (drives /ingest-epub)
cd scripts/epub2md && uv venv && uv pip install -e . && cd ../..
```

Each command builds a local `.venv/` (gitignored — never committed) from the
vendored source and PyPI dependencies. **Full walkthrough — including Node.js
for web articles, Playwright for Substack, and Substack cookies — is in
[`SETUP.md`](SETUP.md).**

## Personalize It (Optional, 10 minutes)

Current categories are defined in the **Categories table in `CLAUDE.md`** — that table is the single source of truth (the slash commands and `wiki/index.md` reference it). To change them, you have two options:

**Option A — edit `CLAUDE.md` directly.** Open `CLAUDE.md`, edit the rows in the Categories table (folder slug + scope description), and save. The next ingest will use the new categories. You can also pre-create matching empty folders under `sources/` and `wiki/`, or let them be created lazily on first use.

**Option B — let Claude interview you.** Paste this prompt into Claude:

> I want to personalize this knowledge base. Interview me about my interests, what I read about most, and what I want to go deeper on. Based on my answers, suggest 4-7 categories. Once I approve them, update CLAUDE.md's Categories table, rename any existing subfolders in `sources/` and `wiki/` to match, update the category headers in `wiki/index.md`, and confirm when everything is done.

Claude will ask a few questions, suggest categories, and update every file that needs changing in one pass.

## The Commands

The wiki runs on three operations — **ingest**, **query**, **lint**. Ingest has
one command per source shape (Claude routes automatically); query is just asking
Claude a question; lint is `/maintain-wiki`.

| Command | What it does |
|---------|--------------|
| `/ingest-url <url>` | Fetches a web article (Defuddle), a Substack post (`fetch_substack.py`), or a PDF at a URL (`pdf2md`) — routes by URL shape — and compiles it into the wiki |
| `/ingest-pdf <path>` | Converts a local PDF (paper, report, slide deck) to markdown via the vendored `pdf2md`, then runs the full ingest |
| `/ingest-epub <path>` | Extracts an EPUB into per-chapter markdown + images via `epub2md`, summarizes chapters, and synthesizes wiki pages |
| `/ingest-inbox` | Classifies and integrates every drop in `inbox/` (markdown, PDFs, etc.) into the wiki |
| `/maintain-wiki` | Health-checks the wiki: broken links, orphans, missing cross-refs, content gaps |

## Daily Rhythm

- When you read something good, clip with [Obsidian Web Clipper](https://obsidian.md/clipper), save the URL, or drop the PDF/EPUB into `inbox/`
- Run `/ingest-url`, `/ingest-pdf`, or `/ingest-epub` as sources come in
- Drop fleeting thoughts into `inbox/` anytime
- End of week: `/ingest-inbox` then `/maintain-wiki`

## Requirements

- [Obsidian](https://obsidian.md)
- [Claude Code](https://www.anthropic.com/claude-code)
- [Node.js](https://nodejs.org) — for Defuddle web scraping (`npm install -g defuddle`)
- [uv](https://docs.astral.sh/uv/) — for the vendored `pdf2md` / `epub2md` tools and the Substack fetcher

Only Obsidian + Claude Code are needed to read and query. Node/uv are needed only
for the ingest paths that use them. See [`SETUP.md`](SETUP.md) for the full matrix.

## Credits

- Pattern: [Andrej Karpathy](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)
- Obsidian Skills: [Steph Ango](https://github.com/kepano/obsidian-skills)
- Vendored ingestion tools: `epub2md` ([EPUB2MD4Claude](https://github.com/michaelbiafore/EPUB2MD4Claude)), `pdf2md`, `fetch_substack.py`
- Implementation: [The AI Maker](https://theaimaker.substack.com)
