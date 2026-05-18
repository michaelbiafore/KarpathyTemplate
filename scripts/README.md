# scripts/

Vendored helper scripts and packages for the wiki's ingest workflows. These
were copied into this repo so the wiki keeps working even if the originating
projects evolve in incompatible directions.

## Routing — when to use which tool

| Source shape | Tool | Slash command |
|---|---|---|
| Substack URL | `scripts/fetch_substack.py` (PEP 723 self-installing) | `/ingest-url` |
| `.pdf` file | `scripts/pdf2md/` (vendored package) | `/ingest-inbox`, `/ingest-url` |
| `.epub` file | `scripts/epub2md/` (vendored package) | `/ingest-epub` |
| Other web article | `defuddle` (Node.js, `npm install -g defuddle`) | `/ingest-url` |

## scripts/epub2md/ (vendored package)

EPUB ingestion via the `epub2md` console script + the Python helper
`epub2md-summarize`. Vendored from
[EPUB2MD4Claude](https://github.com/michaelbiafore/EPUB2MD4Claude) at
upstream tag `vendored-2026-04-28`. See `scripts/epub2md/README.md` for
the upstream pin, one-time `uv venv` bootstrap, and CLI usage.

The slash command `/ingest-epub <book.epub>` drives the whole pipeline
(EPUB extraction → chapter summaries via subagents → wiki page synthesis).
See `.claude/commands/ingest-epub.md`.

## scripts/pdf2md/ (vendored package)

PDF ingestion via the `pdf2md` console script. Vendored from a local
`A:\Packages\PDF2MD4Claude\` repo (no GitHub remote configured upstream)
at commit `f50b9ed`. See `scripts/pdf2md/README.md` for the upstream
pin, one-time `uv venv` bootstrap, and CLI usage.

`/ingest-inbox` and `/ingest-url` invoke this for any `.pdf` input. Do
not call `Read` on a `.pdf` directly — see the speed-up note in
`.claude/commands/ingest-inbox.md`.

## fetch_substack.py

Fetches a Substack article (including paywalled content the cookies grant
access to), downloads all figures alongside the markdown, and writes both
into the wiki's `sources/substack/` tree.

**Vendored from:** `A:/Packages/Transcript2MDSlides/scripts/fetch_substack.py`
**Customizations applied here:**
- PEP 723 inline metadata so `uv run` auto-installs deps (no separate venv).
- `--output-dir` / `-o` flag (default `sources/substack`) — output lands
  directly in the wiki structure, no move step needed.
- Markdown filename uses the bare slug (no `_RAW_SUBSTACK` suffix), since
  this copy writes directly into the wiki rather than a staging `Input/`.

### One-time setup

Playwright needs a browser binary. Run once per machine:

```bash
uv run --with playwright playwright install chromium
```

(Skip if you've already installed Chromium for Playwright in another project
on this machine.)

### Cookies

For paywalled content, place an EditThisCookie-exported JSON at the wiki
root as `cookies_substack.json` (already gitignored). The script discovers
it automatically from there or from `~/cookies_substack.json`. Override
with `-c <path>`.

### Usage

```bash
# From the wiki root, default output dir = sources/substack
uv run scripts/fetch_substack.py "https://aihorizonforecast.substack.com/p/some-article"

# Override output dir (e.g. when ingesting into a different category folder)
uv run scripts/fetch_substack.py "<url>" -o sources/chronos

# Explicit cookies path
uv run scripts/fetch_substack.py "<url>" -c cookies_substack.json
```

Output:
- `<output-dir>/<slug>.md` — the article markdown
- `<output-dir>/<slug>_figs/` — all figures referenced by the markdown,
  filenames `fig_01.png`, `fig_02.png`, ... in document order

The slash command `/ingest-url` calls this script automatically when given
a Substack URL. For non-Substack web articles, `/ingest-url` falls back
to defuddle. For PDFs, both `/ingest-url` and `/ingest-inbox` use
`pdf2md` (PDF2MD4Claude) — see `.claude/commands/ingest-url.md` and
`.claude/commands/ingest-inbox.md` for the routing rules.
