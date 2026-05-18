# PLAN — Making the wiki shareable

Status: **conversation captured for reference; tracked implementation in PLAN_ingest-epub_01.md (EPUB vendoring) and follow-up pdf2md vendoring + SETUP.md / CLAUDE.md polish**
Date: 2026-04-28
Conversation between: user and Claude (Opus 4.7, 1M context)

This file captures the strategic conversation about what a recipient of this
wiki repo would need to do to use it productively, including the EPUB and
PDF ingestion functionality. It led to the execution sequence at the bottom.

---

## User's question

> First, tell me what the procedure will be if/when I want to share this wiki,
> and the EPUB functionality, with someone else. Will I have to get them to
> clone the EPUB2MD4Claude repo?

---

## Claude's answer

Good question to think through before we land more vendored code. Short
answer: **no, they don't need to clone EPUB2MD4Claude separately** —
vendoring puts the package source inside the wiki repo. But there are some
gaps in the broader sharing story you should know about.

### What a recipient gets after `git clone <wiki>`

| Capability | Works out of the box? | One-time setup |
|---|---|---|
| Read all wiki content + images in Obsidian | ✅ Yes | None |
| Run Claude Code in the repo (queries, `/maintain-wiki`) | ✅ Yes | None |
| `/ingest-url` on **non-paywalled** non-Substack URLs (defuddle path) | ✅ Yes | `npm install -g defuddle` |
| `/ingest-url` on **Substack** URLs | ⚠️ Partial | Install `uv` + `uv run --with playwright playwright install chromium` (one-time) + recipient must export *their own* `cookies_substack.json` from a logged-in browser session |
| `/ingest-epub` (once we land the plan) | ⚠️ With setup | Install `uv` + `cd scripts/epub2md && uv venv && uv pip install -e .` (one-time) |
| `/ingest-inbox` or `/ingest-url` on **PDFs** | ❌ **Currently broken for sharing** | See below |

### The pdf2md gap

`pdf2md` is *not* vendored. The slash commands at
`.claude/commands/ingest-inbox.md` and `ingest-url.md` reference it by name
— but on this machine that resolves via the venv at
`A:\Packages\PDF2MD4Claude\.venv\Scripts\pdf2md.exe`, which doesn't exist
anywhere else. A recipient would need to:

1. Clone `michaelbiafore/PDF2MD4Claude` from GitHub (assuming it's public)
2. Bootstrap *its* venv with `uv pip install -e .`
3. Add the venv binary to `PATH` so the bare `pdf2md` invocation works

That's three external dependencies a recipient might not realize they need.
**The same vendoring pattern we're about to use for `epub2md` would fix
this** — copy `pdf2md` into `scripts/pdf2md/`, single
`uv venv` + `uv pip install -e .` to bootstrap. Worth doing alongside the
EPUB work.

### Cookies and Playwright are unavoidable per-recipient setup

`cookies_substack.json` is gitignored on purpose (it's authentication
material). You can't share yours. A recipient who wants paywalled Substack
ingest has to log into their own Substack account and export their own
cookies via EditThisCookie or similar. The `scripts/fetch_substack.py`
README explains this; that doc would also be the place to document the
Playwright binary install.

### Recommendation

If sharing this wiki is a real goal, three additions before that becomes
painless:

1. **Vendor `pdf2md` the same way we're about to vendor `epub2md`** — copy
   the package into `scripts/pdf2md/`, pin upstream commit, document setup.
   Eliminates the PDF2MD4Claude external dependency and is parallel to what
   we're already planning. Maybe 30 minutes of work.

2. **Add a `SETUP.md` or `Onboarding` section to the README** at the wiki
   root covering the full new-machine setup: install Obsidian, install
   Claude Code, install uv, install Node (for defuddle), install Playwright
   Chromium, bootstrap the two venvs, instructions for cookies. ~15 minutes.

3. **Update `CLAUDE.md`** to point future Claude instances at the setup doc
   when they encounter a new clone with no venv (so they bootstrap
   automatically rather than failing on first PDF / EPUB invocation).
   ~5 minutes.

### Order suggested

- **Now:** execute `PLAN_ingest-epub_01.md` — get the EPUB vendoring done
  while it's fresh
- **Right after:** vendor `pdf2md` the same way (small follow-up commit)
- **Then:** write `SETUP.md` and `CLAUDE.md` updates as a final pre-share
  polish

---

## User accepted the recommendation

The user accepted this plan and asked Claude to execute it in the suggested
order. Implementation tracked in:

- `PLAN_ingest-epub_01.md` — the EPUB vendoring plan (already drafted)
- This file — for the strategic question that prompted the broader work
- A future `PLAN_VendorPdf2md.md` (if needed) — likely small enough to skip
  and just execute, mirroring the EPUB approach
- A future `SETUP.md` at the wiki root — onboarding doc for new clones
- Updates to `CLAUDE.md` — point future Claude at SETUP.md on fresh clones
