# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This is a personal knowledge base (LLM Wiki) managed by Claude, based on [Andrej Karpathy's LLM Wiki pattern](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f). The wiki is built incrementally from raw sources and maintained through three operations: **ingest**, **query**, and **lint**.

**Repo type — read this first.** This is an Obsidian vault, not a code project. There is no build, test, or lint toolchain, no `package.json` at the wiki root, no CI. All work is reading and writing markdown under `sources/`, `wiki/`, and `inbox/`.

**External tooling for ingestion.** Three separate paths, all opt-in:
- `npx defuddle` — non-Substack web articles. Install once: `npm install -g defuddle`.
- `scripts/epub2md/` (vendored Python package, drives `/ingest-epub`) — EPUB books. One-time bootstrap per machine: `cd scripts/epub2md && uv venv && uv pip install -e .`.
- `scripts/pdf2md/` (vendored Python package, drives `/ingest-pdf` and the PDF branch of `/ingest-inbox` and `/ingest-url`) — PDF papers/books. Bootstrap: `cd scripts/pdf2md && uv venv && uv pip install -e .`.
- `scripts/md2cliff_html.py` (PEP 723 self-installing, drives the render step of `/pdf2cliff`) — Markdown + images → one portable HTML file. No bootstrap beyond `uv`.
- `scripts/fetch_substack.py` (PEP 723 self-installing) — Substack URLs. No bootstrap needed beyond `uv` being installed and a one-time `uv run --with playwright playwright install chromium`.

**Onboarding for new clones.** If you're operating in a fresh clone of this repo and any of `scripts/epub2md/.venv/` or `scripts/pdf2md/.venv/` don't exist, the corresponding ingest path will fail. Bootstrap the missing venv before invoking the slash command, or point the user at `SETUP.md` for the full new-machine setup walkthrough.

**Current state.** The wiki is in **bootstrap state**: `wiki/` contains only `index.md` and `log.md` (both scaffolded, no entries under any category yet); `sources/` is empty. Don't expect existing pages to cross-link against — the index-first lookup will return an empty index until the first ingest lands. On the first ingest, create the relevant `wiki/<category>/` and `sources/<category>/` folders lazily.

## Architecture

```
sources/          → Layer 1: Raw, immutable source material (articles, PDFs, notes, books, transcripts)
wiki/             → Layer 2: LLM-generated knowledge pages (summaries, entity pages, cross-references)
                    Must contain index.md (catalog) and log.md (append-only change log).
inbox/            → Quick capture for fleeting thoughts — processed into wiki via /ingest-inbox.
                    GITIGNORED — local-only capture zone, won't appear in a fresh clone.
inbox/processed/  → Where /ingest-inbox moves notes after integrating them
inbox/images/     → Inbox-local figures referenced by inbox notes (move alongside the note when ingesting)
Clippings/        → Default drop folder for Obsidian Web Clipper. Drops are already markdown
                    (clipper output, not raw URLs) — ingest the markdown content directly,
                    don't try to /ingest-url the source URL inside the clipping. Move/delete after.
                    GITIGNORED — local-only capture zone.
images/           → Vault-wide image store (Obsidian-managed attachments). Source-specific images live with their source (e.g. sources/books/<slug>/images/, sources/substack/<slug>_figs/).
scripts/          → Vendored ingestion tooling (epub2md/, pdf2md/, fetch_substack.py). Not part of the wiki content. See SETUP.md for one-time bootstrap.
                    Note: scripts/epub2md/.venv/ and scripts/pdf2md/.venv/ are GITIGNORED — bootstrap them on each new machine.
Refs/             → Reference assets used by commands, not wiki content. Holds
                    formatted_transcript_style.html, the house style /pdf2cliff renders into.
cliffs/           → Output folder for /pdf2cliff. One self-contained HTML per source per
                    target length. Derived artifacts — do not lint, do not index.
plans/            → Ad-hoc planning docs. NOT part of the wiki — do not lint, do not index, do not ingest.
cookies_substack.json → (Wiki root, GITIGNORED) Per-user Substack cookies for paywalled-content ingest. See SETUP.md §5.
CLAUDE.md         → Layer 3: This file — the schema that governs how the wiki operates
```

**Bootstrap note.** `wiki/index.md` and `wiki/log.md` must exist before any ingest runs (the index-first lookup and log-append steps depend on them). Category subfolders under `wiki/` and `sources/` are created lazily on first use — no need to pre-create the whole tree.

## Categories

These are the starter categories. If they don't match your interests, ask Claude to personalize them (see the personalization prompt in the README).

| Category | Folder | Scope |
|----------|--------|-------|
| Agent Runtime | `runtime/` |Governed Beng Hong space in which agentic workflows run|
| Agentic Cybersecurity | `cyber/` | Attack surfaces and patterns for agentic systems |
| GitLab | `gitlab/`| Migrate repos and proficiency from GitHub. GitForPMs presentation. |
| Skills | `skills/` | Small-edge skills like "energy correlation", signature-based methods like "Levy Area" correlation, changepoint detection, conformal prediction, topological data analysis (TDA) definition of market regimes, sheaf-over-network based definitions of data inconsistency (data fusion),  |
| System Engineering | `sys/`| Architectural principles including STPA (System Theoretic Process Analysis) for proactively blocking bad system states |
| AlgoTrading | `algotrade/` | Stefan Jansen, Jason Strimpel and Matt Dancho |
| PolyEcon | `polyecon/` | Politics and Economics of AI, including skill atrophy, job loss  |
| Data | `data/` | Data sources and flows |
| Agentic Software Engineering | `aisoft`| Best practices for AI software engineering, after Kieran Klaassen (Every), Andre Karpathy, Boris Cherny, John Kim (Meta), IndyDevDan (Dan Shipper, Every), David Ondrej and Nate B Jones and Len Bass and SuperLinear Academy guys: Yan Wang https://github.com/grapeot and Yuzheng Sun https://maven.com/superlinear/aibuilders |
| Evals | `evals/` | General problem of finding a small number of end-to-end tests and a (possibly multi-dim) metric(s) such that a "pass" on the suite of eval e-t0-e tests gives high confidence the entire agentic system can be trusted in business-critical production uses |




## Wiki Page Format

Every wiki page must follow this template using Obsidian-flavored markdown:

```markdown
---
title: Page Title
date: YYYY-MM-DD
tags:
  - category/topic
  - category/subtopic
aliases:
  - Alternative Name
---

# Page Title

> [!abstract] Summary
> 2-3 sentence overview of the topic.

## Key Points

- Bullet points capturing the core ideas
- Each point should stand on its own
- Include specific claims, data, or frameworks
- Use ==highlights== for key stats or insights

## Notes

Deeper discussion, context, or personal synthesis. This section connects ideas across sources and categories. Use [[wikilinks]] to connect to other pages.

> [!tip] Optional callouts
> Use callouts for tips, warnings, quotes, or examples where appropriate.

## Related

- [[Related Page 1]]
- [[Related Page 2]]

<!-- Max ~8 links. Pick the strongest, most direct connections. Skip weak "same general topic" links. -->

## References

- [[Source File Name]]
- [External link title](https://example.com)
```

### Obsidian-Specific Rules

- Use YAML **frontmatter** with `title`, `date`, `tags`, and `aliases`
- Tags use **nested hierarchy**: `ai/coding`, `health/nutrition`, `productivity/planning`
- **Always use `[[filename|Display Text]]` format** for wikilinks (e.g., `[[claude-code|Claude Code]]`) — Obsidian resolves by filename, not title, and our files use kebab-case
- Do not use bare `[[Display Text]]` — it won't resolve when the filename differs from the display text
- Use **callouts** (`> [!type]`) for summaries, tips, warnings, quotes, and examples
- Use `==highlights==` for key stats or standout insights
- Use standard markdown `[text](url)` for external URLs only

## Naming Conventions

- File names: `kebab-case.md` (e.g., `spaced-repetition.md`, `protein-intake.md`)
- Use descriptive names — the file name should tell you what the page is about
- Entity pages (people, concepts, frameworks) use the entity name: `andrew-huberman.md`, `pomodoro-technique.md`

## Source Types

Sources are organized by type within `sources/`:

| Type | Folder | Notes |
|------|--------|-------|
| Web Articles | `sources/<category>/` | Web articles, blog posts. Fetched via `defuddle`. |
| Research Papers | `sources/arxiv/` | Arxiv (and other similar) research papers. PDFs converted via vendored `pdf2md` first. |
| PDFs (other) | `sources/<category>/` | Non-arxiv PDFs (papers, reports, slide decks). Always convert with vendored `pdf2md` first — never `Read` a `.pdf` directly (it renders each page as an image and is far slower / more token-expensive). |
| Books (PDF) | `sources/books/<slug>/` | Multi-chapter PDFs. Same layout as EPUB books: per-chapter markdown, `images/`, and LLM summaries from `/summarize-chapters`. |
| Books | `sources/books/<slug>/` | EPUBs ingested via `/ingest-epub`; produces per-chapter markdown + an `images/` folder. |
| Substack | `sources/substack/` | Free or paywalled posts via `scripts/fetch_substack.py`. Figures land in `<slug>_figs/`. |
| YouTube | `sources/youtube/` | Video transcripts and screenshots. |

See `sources/books/README.md` and `sources/youtube/README.md` for recommended formats (created lazily on first ingest of that type).

**Routing reference.** `scripts/README.md` holds the canonical source-shape → tool routing table (Substack URL → `fetch_substack.py`, `.pdf` → `pdf2md`, `.epub` → `epub2md`, other web → `defuddle`). Consult it when in doubt about which ingestion path applies; the slash commands themselves implement these rules.

## Slash Commands

| Command | Usage | What it does |
|---------|-------|--------------|
| `/ingest-url` | `/ingest-url <url>` | Fetches an article and runs full ingest. Routes by URL shape: Substack URLs → `scripts/fetch_substack.py` (Playwright + cookies, downloads figures); `.pdf` URLs → vendored `pdf2md`; other web → defuddle. |
| `/ingest-inbox` | `/ingest-inbox` | Processes all `.md` files in `inbox/`. For PDFs, calls vendored `pdf2md` first; for `.epub`, redirects the user to `/ingest-epub`. |
| `/ingest-pdf` | `/ingest-pdf <path-to.pdf>` | Converts a local PDF (paper, report, slide deck) to markdown via vendored `pdf2md`, then runs the full ingest. Multi-chapter PDFs (books, theses) route into `sources/books/<slug>/` and get summarized via `/summarize-chapters`. |
| `/ingest-epub` | `/ingest-epub <path-to.epub>` | Extracts EPUB chapters + images into `sources/books/<slug>/`, then delegates to `/summarize-chapters` and synthesizes per-chapter and book-overview wiki pages. |
| `/summarize-chapters` | `/summarize-chapters <absolute-md-dir> [--tool pdf\|epub]` | Produces LLM chapter summaries (one Agent subagent each), an LLM book-level summary synthesized from them, and one stitched `Sum_<Title>.md`. Works on `pdf2md` or `epub2md` output. No API key. |
| `/pdf2cliff` | `/pdf2cliff <target-pages> <path-to.pdf>` | Illustrated, page-budgeted "cliff notes" of a PDF, delivered as one **portable** self-contained HTML file for emailing. Summarizes chapters, synthesizes an overall summary to the page target, renders it in the `Refs/` house style. Figure-heavy by design. Output in `cliffs/`. |
| `/maintain-wiki` | `/maintain-wiki` | Health-checks the wiki for broken links, orphans, gaps, contradictions. |

## Available Skills

Skills installed under `.claude/skills/`. Reach for them when the matching situation comes up:

| Skill | When to use |
|-------|-------------|
| `defuddle` | Extract clean markdown from a URL (already wired into `/ingest-url`; use directly for ad-hoc URL reads) |
| `obsidian-markdown` | Questions about Obsidian-flavored markdown — wikilinks, callouts, frontmatter, embeds, highlights |
| `obsidian-cli` | Programmatic vault operations: search, create, manage notes/tasks/properties from the command line |
| `obsidian-bases` | Create or edit `.base` files (database-style views over notes with filters, formulas, summaries) |
| `json-canvas` | Create or edit `.canvas` files (visual canvases, mind maps, flowcharts) |

## Operations

### 1. Ingest

When the user adds a new source or asks to ingest something:

1. **Read** the source material thoroughly
2. **Classify** it into one or more categories
3. **Scan `wiki/index.md` first** to see what pages already exist — don't glob the whole wiki. Only open individual pages that plausibly overlap with the source. The index is the primary lookup.
4. **Create** a wiki summary page in `wiki/<category>/` following the page format above
5. **Update** existing wiki pages only if the new source *materially* adds to, contradicts, or refines them (new facts, new frameworks, stronger data). Skip pages where the overlap is only thematic.
6. **Entity pages — second-mention rule**: Only create a page for a person, concept, or framework when it appears in **two or more distinct sources**. On first mention, leave it as inline text in the summary page. When a second source brings it up, promote it to its own page and link both sources. Exception: the user explicitly asks for it.
7. **Add forward `[[wikilinks]]`** from the new page to directly-relevant existing pages. Do **not** edit other pages just to add a backlink — Obsidian surfaces backlinks natively in its UI. Only update another page if the new source genuinely changes its content.
8. **Cap links**: aim for ~8 entries in `## Related` per page. Pick the strongest connections; drop weak "same general topic" links.
9. **Update `wiki/index.md`** — add the new page(s) under the appropriate category
10. **Append to `wiki/log.md`** — record what was ingested and what pages were created/updated

A single source should typically touch **2-5 wiki pages** (the new summary + a small number of genuinely affected pages). If you find yourself editing more than 5, you are probably pattern-matching on topic overlap rather than material change — stop and reassess.

### 2. Query

When the user asks a question:

1. **Search** relevant wiki pages using Grep/Glob
2. **Read** the most relevant pages
3. **Synthesize** an answer drawing from multiple pages
4. **Cite** which wiki pages informed the answer using `[[wikilinks]]`
5. **Promote** (if the answer is substantial): ask the user if this should become a new wiki page

### 3. Lint

When the user asks to lint or maintain the wiki:

1. **Check for contradictions** — do any pages make conflicting claims?
2. **Find stale claims** — are any pages based on outdated information?
3. **Detect orphan pages** — pages missing from `wiki/index.md` *and* not linked from any other page (under lazy backlinks, `wiki/index.md` is the authoritative reachability check)
4. **Verify cross-references** — do all `[[wikilinks]]` point to pages that exist?
5. **Identify gaps** — based on existing pages, are there obvious topics that should have pages but don't?
6. **Report** findings and fix what can be fixed automatically
7. **Log** the lint run in `wiki/log.md`

## Rules

Hard constraints on every ingest, query, and lint. The Operations section above defines the *workflow*; this section defines the *invariants* that workflow must preserve.

**Content invariants**
- Never modify files in `sources/` — they are immutable raw material.
- Always update `wiki/index.md` and `wiki/log.md` when adding or substantively changing pages.
- Prefer updating an existing page over creating a near-duplicate. Keep summaries concise — quick reference, not source reproduction.
- A page may appear in multiple category sections of the index when it genuinely spans two categories.

**Linking conventions (Obsidian)**
- Use short `[[wikilinks]]` for all internal links — Obsidian resolves by filename, so full paths are unnecessary.
- In `wiki/index.md` and any prose, always use `[[filename|Display Text]]` (e.g., `[[late-bound-sagas|Late-Bound Sagas]]`). Bare `[[Display Text]]` won't resolve when filenames are kebab-case and titles are Title Case.

**Efficiency invariants** (keep ingest cost bounded as the wiki grows — these are also enforced by the numbered Ingest steps above; restated here as the canonical rule list):
- **Index-first lookup.** Read `wiki/index.md` before globbing the wiki. Only open pages the index suggests are relevant.
- **Second-mention rule.** Don't create a page for a person/concept/framework on first mention — leave it inline. Promote to its own page only on a second source. Exception: user explicitly asks.
- **Forward links only (lazy backlinks).** Add `[[wikilinks]]` from the new page to existing pages. Don't open other pages just to add a reciprocal backlink — Obsidian's backlink pane shows them automatically. Only edit another page when the new source materially changes its content.
- **Link cap.** Target ~8 links max in `## Related`. Prefer strong, direct connections.
- **Touch budget.** A typical ingest modifies 2–5 pages. If the count climbs higher, you're probably pattern-matching on topic overlap rather than material change — stop and reassess.
