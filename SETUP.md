# SETUP

Onboarding doc for using this wiki on a fresh machine. If you just want to
**read** the wiki, skip to [Reading-only setup](#reading-only-setup) — it's
a 2-minute install.

If you want to **ingest new content** (URLs, PDFs, EPUBs), follow the full
setup. None of it is hard, but there are several independent pieces.

---

## Quick reference

| You want to... | What you need installed |
|---|---|
| Read the wiki in Obsidian | Obsidian only |
| Use Claude Code with the wiki (queries, `/maintain-wiki`) | Obsidian + Claude Code |
| Ingest non-Substack web articles via `/ingest-url` | + Node.js + `npm install -g defuddle` |
| Ingest **Substack** URLs (incl. paywalled) via `/ingest-url` | + `uv` + Playwright Chromium + your own `cookies_substack.json` |
| Ingest **PDFs** via `/ingest-inbox` or `/ingest-url` | + `uv` + bootstrap `scripts/pdf2md/` venv |
| Ingest **EPUBs** via `/ingest-epub` | + `uv` + bootstrap `scripts/epub2md/` venv |

---

## Reading-only setup

1. Install [Obsidian](https://obsidian.md) (free for personal use).
2. Clone this wiki:
   ```bash
   git clone <repo-url> ts_FMs
   ```
3. In Obsidian: **File → Open Vault → Open folder as vault → pick `ts_FMs/`**.
4. Done. All ~50 wiki pages, ~600 figures, and ~50 source clippings are
   readable in Obsidian's preview mode immediately.

That's the whole reading-only path. No Python, no Node, no Claude Code
required.

---

## Full setup (for ingesting new content)

### 1. Prerequisites

Install these once per machine:

- **[Obsidian](https://obsidian.md)** — free, all platforms
- **[Claude Code](https://www.anthropic.com/claude-code)** — desktop app or
  CLI; an Anthropic account is needed
- **[Node.js](https://nodejs.org)** — needed for the `defuddle` web
  scraper. Any LTS version works.
- **[uv](https://docs.astral.sh/uv/)** — Python environment manager. Install
  once via:
  ```bash
  # Windows PowerShell
  irm https://astral.sh/uv/install.ps1 | iex
  
  # macOS / Linux
  curl -LsSf https://astral.sh/uv/install.sh | sh
  ```

### 2. Clone the wiki

```bash
git clone <repo-url> ts_FMs
cd ts_FMs
```

### 3. One-time external-tool installs

```bash
# defuddle — for non-Substack web articles
npm install -g defuddle

# Playwright Chromium — for Substack scraping (downloads a Chromium binary,
# ~150 MB, one-time)
uv run --with playwright playwright install chromium
```

### 4. Bootstrap the two vendored Python packages

These are **self-contained Python packages** vendored into the wiki repo at
`scripts/epub2md/` and `scripts/pdf2md/`. Each has its own `uv` virtual
environment that needs to be created once per machine.

```bash
# EPUB ingestion (drives /ingest-epub)
cd scripts/epub2md
uv venv
uv pip install -e .
cd ../..

# PDF ingestion (drives the PDF branch of /ingest-inbox and /ingest-url)
cd scripts/pdf2md
uv venv
uv pip install -e .
cd ../..
```

Each `uv venv` creates a `.venv/` directory inside the package; both are
gitignored. Total disk: ~400 MB across both venvs (mostly PyMuPDF and
lxml binaries).

After this, the slash commands `/ingest-epub`, `/ingest-inbox`, and
`/ingest-url` will find the binaries at:
- `scripts/epub2md/.venv/Scripts/epub2md.exe`
- `scripts/epub2md/.venv/Scripts/epub2md-summarize.exe`
- `scripts/pdf2md/.venv/Scripts/pdf2md.exe`

(Replace `Scripts/` with `bin/` and drop `.exe` on macOS / Linux.)

### 5. Cookies for paywalled Substack content (only if you want it)

If you want `/ingest-url` to handle Substack content behind a paywall you
subscribe to, you need to provide your own browser cookies:

1. In a Chrome / Edge / Firefox session that's **logged into your
   Substack account**, install the
   [EditThisCookie](https://www.editthiscookie.com/) browser extension.
2. Navigate to a Substack page (any page on `*.substack.com`).
3. Click the EditThisCookie icon → **Export → JSON**.
4. Save the JSON as `cookies_substack.json` in the **wiki root**
   (next to `CLAUDE.md`).

The file is gitignored and stays local. The `scripts/fetch_substack.py`
script auto-discovers it from the wiki root.

If you don't do this, `/ingest-url` on Substack URLs will work for free
articles only (paywalled content will return a partial article).

### 6. Verify the setup

Quick smoke tests:

```bash
# defuddle
npx defuddle --help

# epub2md
scripts/epub2md/.venv/Scripts/epub2md.exe --help

# pdf2md
scripts/pdf2md/.venv/Scripts/pdf2md.exe --help

# Substack fetcher (PEP 723 — no separate venv to bootstrap)
uv run scripts/fetch_substack.py --help
```

All four should print usage information without errors.

In Claude Code from the wiki root:

```
/help        # confirms slash commands are loaded
```

You should see `/ingest-epub`, `/ingest-inbox`, `/ingest-url`, and
`/maintain-wiki` in the list.

---

## Common issues

### "uv: command not found" after installing uv

The installer adds `uv` to a per-user bin directory that may not be on
your shell's PATH. Restart your terminal, or add the install path
explicitly. On Windows the default is `C:\Users\<you>\.local\bin`.

### "playwright: chromium not found" when running fetch_substack.py

You skipped step 3, or installed Chromium for a different Python
environment. Re-run `uv run --with playwright playwright install chromium`
from the wiki root.

### `/ingest-url` works for Substack but says "paywalled — partial article"

Either your `cookies_substack.json` is missing (step 5), or your cookies
have expired (Substack invalidates session cookies periodically). Re-export
from a logged-in browser.

### PDF ingest is mysteriously slow

If a PDF takes more than a minute or two to ingest, you might be falling
into the "Read on .pdf" trap (which renders each page as an image). The
correct path is `pdf2md` first, then `Read` on the resulting `.md`. The
slash commands handle this automatically; if you find yourself in a manual
loop, see `feedback_pdf_ingestion.md` in your local Claude memory.

### "No EPUB metadata found" for a specific book

Some EPUBs ship with placeholder metadata (e.g., `<dc:title>Book Title</dc:title>`).
The vendored `epub2md` (commit `879684c`) has fallback logic that reads the
first spine item or first TOC entry instead. If that still fails, pass
`--slug <override>` to `/ingest-epub`.

### MathML in EPUBs renders as garbage

`epub2md`'s MathML→LaTeX conversion uses [pandoc](https://pandoc.org).
Install pandoc separately and ensure it's on PATH. (Most technical EPUBs
use image-based math rather than MathML, so this is rarely needed.)

---

## What's where

```
ts_FMs/
├── CLAUDE.md                    Wiki schema + operations
├── README.md                    Public-facing intro
├── SETUP.md                     This file
├── cookies_substack.json        (Local only, gitignored — your cookies)
├── .claude/
│   ├── commands/                Slash command definitions
│   │   ├── ingest-epub.md
│   │   ├── ingest-inbox.md
│   │   ├── ingest-url.md
│   │   └── maintain-wiki.md
│   ├── skills/                  Bundled Obsidian skills
│   └── settings.local.json      (Per-machine permissions, gitignored)
├── scripts/
│   ├── README.md                Routing table for which tool handles what
│   ├── fetch_substack.py        PEP 723 self-installing Substack scraper
│   ├── epub2md/                 Vendored EPUB→Markdown package + venv
│   └── pdf2md/                  Vendored PDF→Markdown package + venv
├── sources/                     Raw, immutable source material
│   ├── ai/, arxiv/, books/, chronos/, financial-markets/,
│   │   hedge-funds/, moirai/, substack/, tft/, tsmixer/, youtube/
├── wiki/                        LLM-generated wiki pages
│   ├── index.md                 The catalog (Claude reads this first)
│   ├── log.md                   Append-only change log
│   └── ai/, chronos/, financial-markets/, hedge-funds/, moirai/, ...
├── inbox/                       Drop zone for new captures
│   ├── README.md
│   └── processed/               Where /ingest-inbox moves notes after use
├── Clippings/                   Default Obsidian Web Clipper output dir
└── plans/                       Ad-hoc planning docs (not part of wiki)
```

`inbox/` and `Clippings/` are gitignored — they're local-only capture
zones.

---

## Sharing the wiki

If you're handing this repo to someone else, point them at this file. The
ingestion functionality is fully self-contained — no external repos to
clone. They'll need to bootstrap the two venvs (step 4) and install
external tools (step 3), but everything else travels with the repo.

The two pieces they have to provide for themselves:

1. Their own `cookies_substack.json` if they want paywalled Substack
   ingest (your cookies are personal and gitignored).
2. Their own Anthropic credentials for Claude Code.

That's it.
