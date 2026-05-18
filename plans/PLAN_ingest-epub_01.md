# PLAN — `/ingest-epub` slash command

Status: **proposed, not yet applied**
Date: 2026-04-28
Target: a new `.claude/commands/ingest-epub.md` slash command + supporting vendored code

## 1. Goal

Promote the manual EPUB-ingest workflow that just ran successfully on Peixeiro's
*Time Series Forecasting Using Foundation Models* (Manning, 2025) into a single
slash command. End state:

```
/ingest-epub <path-to-book.epub>
```

…produces source clippings + figures + chapter summaries + per-chapter wiki
pages + a book-overview wiki page + index/log updates, all in one invocation.

The command **vendors** the existing `EPUB2MD4Claude` package
(`A:\Packages\EPUB2MD4Claude\`) into this wiki repo so the workflow keeps working
even if the upstream project evolves. This matches the precedent set by the
already-vendored `pdf2md` (`scripts/` plus a vendored package reference at
`A:\Packages\PDF2MD4Claude\` pinned to commit `f50b9ed`) and
`fetch_substack.py` (`scripts/fetch_substack.py`, vendored from
`A:\Packages\Transcript2MDSlides\`).

## 2. Context — what the Peixeiro run actually did

The user's manual workflow that produced commit `c823e6f` was, in order:

1. Ran upstream `epub2md "Peixeiro_TSFM.epub" -o md_out` in
   `A:\Packages\EPUB2MD4Claude\`. Output: ~24 chapter `.md` files
   (`000_Cover.md` … `024_References.md`), a `Table_of_Contents.md`, an
   `Index.md`, a `ChapterAbstracts.md`, and an `images/` directory with 124
   chapter figures (`CH04_F01_Peixeiro2.png` etc.) plus equation images
   (`peixeiro2-ch1-eqs-0x.png`) and book-meta images (`cover.jpg`,
   `Peixeiro_author-photo.jpg`, `manning_m.jpg`).
2. Ran the upstream `/summarize-chapters` slash command in that repo, which
   internally called `epub2md-summarize scan md_out` (returns JSON list of
   content chapters with target word ranges), then dispatched a Task subagent
   per chapter to write `Sum_NNN_<title>.md` files, then called
   `epub2md-summarize assemble md_out` to concatenate into
   `Sum_<book-title>.md`.
3. The user manually copied the 19 `Sum_*.md` files plus the 124 images into
   `A:\_Wikis\ts_FMs\inbox\` and `inbox/images/`.
4. I (Claude) then read each chapter summary in turn and wrote 11 wiki pages
   plus updated index/log — the per-chapter / book-overview / new-entity
   pattern documented in `wiki/log.md`.

The new `/ingest-epub` command should **automate steps 1–3** and **drive step 4
via the same per-chapter synthesis loop** — same outputs, no manual movement.

## 3. User experience

```
/ingest-epub A:\path\to\book.epub                       # default behaviour
/ingest-epub <path> --slug peixeiro-tsfm-2025           # override book slug
/ingest-epub <path> --skip-synthesis                    # stop after step 2
/ingest-epub <path> --max-parallel 5                    # bump subagent batch
```

Default behaviour:

1. Auto-derive a book slug from EPUB metadata (`<author-last>-<title-slug>-<year>`,
   sanitized + truncated to ~40 chars).
2. Convert the EPUB to chapter markdown + extract images, both into
   `sources/books/<slug>/`.
3. Summarize each content chapter via Task subagents (skip front/back matter as
   the upstream `is_content_chapter` predicate does). Write
   `Sum_NNN_<title>.md` files into the same directory.
4. Concatenate the per-chapter summaries into `Sum_<book-title>.md` in the same
   directory.
5. Synthesize wiki pages from the summaries:
   - One book-overview page (`wiki/ai/<slug>-book.md` by default — overridable)
   - One per-chapter page for each substantive chapter, named
     `<slug>-ch<N>-<topic>.md` for chapters that cover existing models, or just
     `<topic>.md` for chapters that introduce a new entity worth its own page
   - Cross-reference existing entity pages where applicable
6. Update `wiki/index.md` (add a Books subsection entry plus any new entity
   pages) and append a batch entry to `wiki/log.md`.
7. Report: sources written, summaries produced, wiki pages created/updated,
   total runtime.

Failure modes that the slash command should handle gracefully:

- Path doesn't exist or isn't an EPUB → fail fast with clear error
- `uv` not installed → fail fast with install instructions
- venv not yet bootstrapped → bootstrap it, log the one-time delay
- Slug already exists at `sources/books/<slug>/` → ask for `--force` or
  `--slug <override>` (don't silently overwrite)
- A subagent fails on a chapter → log the failure, continue with remaining
  chapters, surface the failed chapter in the final report

## 4. File layout

Adding the following to the wiki repo:

```
scripts/
  fetch_substack.py            (existing, untouched)
  README.md                    (existing — extend with epub2md notes)
  epub2md/                     <-- NEW vendored package
    pyproject.toml             (mirrors upstream — name + deps + scripts)
    README.md                  (vendoring notes — version pinned, dirty-tree caveat)
    src/
      epub2md/
        __init__.py
        __main__.py
        cli.py
        extractor.py
        converter.py
        toc_generator.py
        index_generator.py
        abstract_writer.py
        summarizer.py

.claude/commands/
  ingest-epub.md               <-- NEW slash command spec

.gitignore                     (extend: scripts/epub2md/.venv/)
```

**Why `scripts/epub2md/` rather than top-level `src/`?** The wiki is an Obsidian
vault, not a Python project. Per the existing CLAUDE.md framing, scoping
Python tooling under `scripts/` keeps the vault clean. Mirrors the `pdf2md`
external-package convention.

**Why a real venv** (vs. PEP 723 inline metadata like fetch_substack.py)?
The upstream package is **8 modules with two console_scripts entry points** and a
non-trivial dependency graph (`ebooklib`, `beautifulsoup4`, `lxml`,
`markdownify`). Inline metadata works for single-script tools; multi-module
packages with `[project.scripts]` need a real venv + `pip install -e` to expose
console scripts.

**Output goes directly to `sources/books/<slug>/`**, not to a separate
intermediate dir. Rationale: the chapter `.md` files **are** the immutable raw
source per the wiki's Karpathy-style architecture. There's no value in a
two-step "epub → md_out/ → sources/" copy when one step works. The summaries
land in the same directory because they're derived artifacts that belong with
their source.

**No `inbox_epub/` directory.** The user floated this option; I'm proposing
against it. Rationale: the inbox/ pattern is for *raw drops* the user hasn't
processed yet. By the time the slash command finishes step 4, the summaries
are already organized by book — they're not raw drops. Putting them in
`sources/books/<slug>/` is correct from the schema's perspective and avoids
inbox pollution if multiple books are ingested.

## 5. Vendoring strategy

### 5.1 What to copy

Copy these files verbatim from `A:\Packages\EPUB2MD4Claude\src\epub2md\`:
- `__init__.py`, `__main__.py`, `cli.py`, `extractor.py`, `converter.py`,
  `toc_generator.py`, `index_generator.py`, `abstract_writer.py`,
  `summarizer.py`

Copy and adapt:
- `pyproject.toml` — keep the `[project.scripts]` block and the `dependencies`
  list; update `name` to something like `epub2md-vendored` to avoid PyPI
  collision risk; keep `requires-python = ">=3.10"`.

Do **not** copy:
- The upstream `epub_in/`, `md_out/`, `plans/`, `.venv/` directories
- The upstream `.claude/commands/summarize-chapters.md` — we'll port the
  relevant orchestration logic into `.claude/commands/ingest-epub.md` directly,
  not as a separate slash command (the user wants `/ingest-epub` as the single
  entry point).
- `EPUB_Plan_01.md`, `Mandate.md`, etc. — internal planning docs, not relevant.

### 5.2 Pinning the upstream commit

The upstream repo (`A:\Packages\EPUB2MD4Claude\`) is at HEAD `a84a173` ("Initial
commit: EPUB-to-Markdown converter with chapter summarization", 2026-03-04).
**The working tree is dirty**: tracked files `cli.py`, `converter.py`,
`extractor.py`, `.claude/commands/summarize-chapters.md`, and
`.claude/settings.local.json` have uncommitted modifications, and `plans/` is
untracked.

==This is the same caveat that applied to the pdf2md vendoring.== The vendored
copy must reflect the **actually-installed working-tree state**, not HEAD alone.
The vendoring step in §6 takes a literal byte-for-byte copy of the current
working tree, so this is handled correctly. The slash command's commit message
should note both the HEAD SHA and that the working tree was dirty (with file
list).

Recommended: before vendoring, prompt the user to either commit the EPUB2MD4Claude
working tree or accept that we vendor the dirty state. (Same offer the pdf2md
work surfaced. The user committed pdf2md's working tree at that point and we
got the clean reference `f50b9ed`. They'll likely want to do the same here.)

### 5.3 Setup

One-time bootstrap after vendoring:

```bash
cd scripts/epub2md
uv venv
uv pip install -e .
```

After that, two console scripts are available at
`scripts/epub2md/.venv/Scripts/epub2md.exe` and
`scripts/epub2md/.venv/Scripts/epub2md-summarize.exe`. The slash command
invokes them by full path so the venv doesn't need to be activated.

## 6. Implementation steps (in order)

The plan executor should run these in sequence. Each is small and reversible.

### Step 1 — Create `scripts/epub2md/` skeleton

```bash
mkdir -p scripts/epub2md/src/epub2md
```

### Step 2 — Vendor the package source

Copy from `A:\Packages\EPUB2MD4Claude\src\epub2md\` to `scripts/epub2md/src/epub2md/`:

```bash
cp "A:/Packages/EPUB2MD4Claude/src/epub2md/"*.py scripts/epub2md/src/epub2md/
```

Verify file count matches (8 `.py` files + `__pycache__/` which gets pruned next).

Remove `__pycache__/` if present:

```bash
rm -rf scripts/epub2md/src/epub2md/__pycache__
```

### Step 3 — Adapt `pyproject.toml`

Write `scripts/epub2md/pyproject.toml` mirroring upstream but with:
- `name = "epub2md-vendored"` (avoid PyPI namespace collision)
- `version = "0.1.0+vendored.<date>"` (e.g. `0.1.0+vendored.20260428`) so we can
  see at a glance that this is the vendored copy
- Same `[project.scripts]` block (`epub2md`, `epub2md-summarize`)
- Same dependencies block

Plus a `[tool.hatch.build.targets.wheel]` block with
`packages = ["src/epub2md"]` matching upstream.

### Step 4 — Write `scripts/epub2md/README.md`

Should include:
- Vendored from `A:\Packages\EPUB2MD4Claude\` at commit `a84a173` plus a
  dirty-tree note listing the modified files
- One-time setup: `uv venv && uv pip install -e .` from inside `scripts/epub2md/`
- The two CLI commands and their args
- Note that the slash command `/ingest-epub` invokes these by full venv path
- Routing rules vs. fetch_substack.py (Substack URLs) and pdf2md (PDFs) — same
  table format as the existing `scripts/README.md`

### Step 5 — Bootstrap the venv

```bash
cd scripts/epub2md
uv venv
uv pip install -e .
```

Verify both scripts work:
```bash
.venv/Scripts/epub2md.exe --help
.venv/Scripts/epub2md-summarize.exe --help
```

### Step 6 — Update `.gitignore`

Add:
```
scripts/epub2md/.venv/
```

(The `Input/` line for upstream Transcript2MDSlides is already there from the
fetch_substack work; pattern is the same.)

### Step 7 — Write `.claude/commands/ingest-epub.md`

This is the actual slash command. Outline:

```markdown
Ingest an EPUB book into the wiki: extract chapters + images, summarize each
chapter via subagents, then synthesize wiki pages.

## Usage

/ingest-epub <path-to.epub> [options]

## Instructions

1. **Validate inputs.**
   - Confirm `$ARGUMENTS` is a path that exists and ends in `.epub`.
   - Reject otherwise with a clear error.

2. **Derive book slug from EPUB metadata.**
   - Run a small inline Python via uv:
     ```
     uv run --with ebooklib python -c "
       import ebooklib; from ebooklib import epub; ...
     "
     ```
   - Or call a helper subcommand we add to `epub2md` (e.g.,
     `epub2md metadata <path>`) that prints title/author/year as JSON.
   - Slug = `<author-last>-<title-slug>-<year>`, kebab-case, ~40 chars.
   - If `sources/books/<slug>/` already exists, ask for `--force` or
     `--slug <override>`.

3. **Convert EPUB → markdown.**
   - `scripts/epub2md/.venv/Scripts/epub2md.exe "<path>" -o sources/books/<slug>`
   - Verify chapter `.md` files + `images/` directory + `Table_of_Contents.md`
     + `ChapterAbstracts.md` were created.

4. **Scan for content chapters.**
   - `scripts/epub2md/.venv/Scripts/epub2md-summarize.exe scan sources/books/<slug>`
   - Parse the JSON output. Each entry: `{path, filename, title, word_count,
     target_min, target_max}`.

5. **Summarize each content chapter via Agent subagents.**
   - For each chapter in the scan results, dispatch an Agent (subagent_type:
     "general-purpose") with a prompt that:
     - Reads the chapter file at `path`
     - Writes a summary between `target_min` and `target_max` words
     - Preserves key concepts, arguments, examples, chapter structure
     - Uses markdown headings that mirror the chapter's section structure
     - For math-heavy chapters, includes 3-8 key equation `![](images/...)`
       references inline (after using Read to view the actual image files)
     - For figure-heavy chapters, includes the most architecturally-significant
       figures only
     - Writes output to `sources/books/<slug>/Sum_<original_filename>`
     - Does NOT include YAML frontmatter in the summary
   - Launch in batches of `--max-parallel` (default 3) to avoid rate limits.

6. **Assemble concatenated summary.**
   - `scripts/epub2md/.venv/Scripts/epub2md-summarize.exe assemble sources/books/<slug>`
   - Produces `Sum_<book-title>.md` in the same directory.

7. **Add YAML frontmatter to each `Sum_*.md` file.**
   - Inline Python or sed/awk to prepend frontmatter with title, book, author,
     publisher, published, created, tags. Same shape as the Peixeiro batch.

8. **Synthesize wiki pages.**
   - Read the concatenated `Sum_<book-title>.md` to understand book scope.
   - Read each substantive chapter summary to inform per-chapter wiki pages.
   - Decide per chapter:
     - **Skip if the chapter is a part-divider, references, preface, or other
       non-substantive content** (the `is_content_chapter` predicate already
       filtered most of these in step 5, but a few short stubs may survive).
     - **Create a per-chapter wiki page** named
       `<slug>-ch<N>-<topic>.md` for chapters covering models that already
       have entity pages in the wiki.
     - **Create a new entity page** named `<topic>.md` for chapters introducing
       genuinely new models / concepts with no existing wiki page.
   - Always create one **book-overview wiki page**: `<slug>-book.md`.
   - Embed figures liberally per the standing user direction — vault-relative
     paths into `sources/books/<slug>/images/`.
   - Cross-reference existing entity pages where they exist.

9. **Update `wiki/index.md`.**
   - Add a Books subsection entry under AI (or whichever category the book
     belongs to) with the book-overview page as parent and per-chapter pages
     as bulleted children.
   - Add any new entity pages to their respective category sections.

10. **Append to `wiki/log.md`.**
    - One batch entry covering the whole ingest, listing sources written,
      summaries produced, wiki pages created, what was skipped and why.

11. **Report.**
    - Output a brief summary: book title, slug, # chapters summarized, # wiki
      pages created, total runtime.

## Notes

- For long books (>30 chapters), batch the subagent dispatches to avoid
  overwhelming the rate limiter. Default batch size = 3 in parallel.
- For math-heavy books (image-based equations), the subagent prompt explicitly
  instructs the agent to view a sample of `images/...` referenced in the
  chapter and embed key equation references inline. Keep equation embeds
  modest (3-8 per chapter) so summaries don't bloat.
- For chapters that almost entirely overlap with already-covered models
  (e.g., a chapter on Chronos when chronos.md, chronos-bolt.md, chronos-2.md,
  chronosx.md already exist), prefer creating one focused chapter page that
  cross-references the entity pages over duplicating their content.
```

Length target: ~300-400 lines. Detailed enough that future Claude can execute
without reading this PLAN file as well.

### Step 8 — Update root `scripts/README.md`

Add a section at the bottom routing between the three vendored tools:

| URL / file pattern | Tool | Slash command |
|---|---|---|
| Substack URL | `scripts/fetch_substack.py` (PEP 723) | `/ingest-url` |
| `.pdf` file | `pdf2md` (`A:\Packages\PDF2MD4Claude\`) | `/ingest-inbox`, `/ingest-url` |
| `.epub` file | `scripts/epub2md/` (vendored package) | `/ingest-epub` |
| Other web article | `defuddle` | `/ingest-url` |

### Step 9 — Add a feedback memory

Save `feedback_epub_ingestion.md` in the project memory dir documenting:
- For EPUB files, use `/ingest-epub` not `/ingest-inbox` or `/ingest-url`
- Why: extracting EPUB structure manually is error-prone; the slash command
  handles chapter splitting, image extraction, summary generation, and wiki
  synthesis in one step
- One-time setup: `cd scripts/epub2md && uv venv && uv pip install -e .`

Index in `MEMORY.md` alongside the existing PDF and Substack ingestion memories.

### Step 10 — Test on the Peixeiro EPUB

Re-run `/ingest-epub` on the original Peixeiro EPUB if the user can locate it
(or any other EPUB they have handy). Compare:
- Time vs. the manual Peixeiro run (should be much shorter)
- Wiki page output quality vs. the existing `peixeiro-ch*.md` pages
- Number of figures preserved (should match or exceed 124)

If output is comparable, commit the whole package as a single commit (the
"Peixeiro book" precedent: large but coherent). If output drifts, debug.

## 7. Open questions / decisions to confirm with the user

1. **Vendor location** — `scripts/epub2md/` per §4, or top-level `src/epub2md/`?
   I lean `scripts/epub2md/` for vault-cleanliness; happy to flip if the user
   prefers Python-project conventions.

2. **Sources output dir** — directly to `sources/books/<slug>/`, or via an
   intermediate `epub_out/<slug>/` that gets moved? I lean direct (matches
   the Peixeiro precedent and the wiki schema).

3. **Summary location** — same dir as chapter sources (per §4), separate
   `inbox_epub/` (per the user's prompt suggestion), or main `inbox/`?
   I lean same dir; rationale in §4.

4. **Wiki-page naming convention** — `<slug>-ch<N>-<topic>.md` (matches
   Peixeiro), or just `<topic>.md` for everything? Mixed approach where new
   entity pages get clean names and chapter pages get prefixed (matches what
   I did for Peixeiro)?

5. **Auto-promotion of new models to entity pages** — Step 8 of the slash
   command says "create a new entity page for chapters introducing genuinely
   new models". This is a judgment call. Should the command emit a *proposal*
   and ask the user to confirm, or just decide and proceed? I lean proceed
   (matches Peixeiro behavior — Lag-Llama and Time-LLM got dedicated entity
   pages without explicit per-page user confirmation).

6. **Should `/ingest-epub` also support EPUB-via-URL?** I.e., download an
   EPUB from a URL, then run the same pipeline. Out of scope for v1 but worth
   flagging — `wget` + the same pipeline is mechanical.

7. **Pinning the upstream commit** — the working tree of EPUB2MD4Claude is
   dirty. Should we ask the user to commit that work in the upstream repo
   before vendoring (so we can pin a clean SHA)? This is what the user did for
   pdf2md after the same flag, and it worked well.

8. **`--skip-synthesis` flag** — useful for large books where the user wants
   to manually drive step 8 (wiki synthesis) after reviewing the summaries.
   Default off; flag it as on-demand. Keep in v1.

9. **Logging / artifacts** — should the slash command write a per-run
   `<slug>-ingest-log.json` for debugging? Useful for re-runs and partial
   failures. Probably yes; minimal cost.

10. **Cleanup on failure** — if step 5 (subagent dispatch) fails partway, the
    `sources/books/<slug>/` dir is left half-populated. Should the command
    rollback (delete the dir) or preserve for forensics? I lean preserve —
    the user can `rm -rf` manually. Rolling back is dangerous if the user
    interrupted mid-flow on purpose.

## 8. Estimated effort

- Steps 1–6 (vendoring + venv bootstrap): ~10 minutes
- Step 7 (writing the slash command spec): ~30-45 minutes (it's the long file)
- Step 8 (scripts/README update): ~5 minutes
- Step 9 (feedback memory): ~5 minutes
- Step 10 (test run on Peixeiro EPUB): ~10-30 minutes depending on book size
  and # subagents

Total: ~1-2 hours of focused work, single session.

## 9. Risks

1. **Upstream working-tree drift.** EPUB2MD4Claude has uncommitted local
   changes. If we vendor without pinning, future debugging will be hard.
   Mitigation: prompt the user to commit upstream (per §5.2) before vendoring.

2. **Math-equation handling.** The Peixeiro book had image-based equations and
   the subagent prompt for `summarize-chapters` already handles this. We
   inherit that prompt. For non-Peixeiro books with different equation formats
   (LaTeX in the EPUB, MathML, etc.), behavior may degrade. v1 accepts this;
   v2 could add equation-format detection.

3. **Subagent rate limits.** Dispatching 20 subagents in batches of 3 for a
   10-chapter book is fine. Dispatching 50 subagents for a 50-chapter
   reference book might hit rate limits or context limits. The `--max-parallel`
   flag is the operator's escape valve.

4. **Auto-detected book slug collisions.** Two different "Foundation Models"
   books would yield similar slugs. The `--slug` override and the
   already-exists check in step 2 mitigate this.

5. **Wiki-page naming consistency.** I observed in the Peixeiro ingest that
   mixing `peixeiro-ch<N>-<topic>.md` for existing-model chapters and clean
   `<topic>.md` for new-entity chapters is a *deliberate* mix that buys
   discoverability for new entities. Future books should follow the same
   convention. The slash command spec needs to be explicit about this.

## 10. After this lands

Cleanup follow-ups, in priority order:

1. **Rerun the Peixeiro book under the new command** to validate output
   quality against the manually-produced Peixeiro pages. Diff the wiki pages.
   If close, leave the manual pages alone (they were written and reviewed
   carefully); if drift detected, file specific issues.

2. **Document upstream-EPUB2MD4Claude commit** in the wiki's CLAUDE.md
   alongside pdf2md and fetch_substack references (the "External tool
   dependencies" section).

3. **Consider a `/ingest-pdf-book` companion** — the same wiki-page synthesis
   logic applied to multi-chapter PDFs (textbooks, theses) using `pdf2md`'s
   chapter-splitting output. Would share most of step 8's logic with
   `/ingest-epub`. Open question whether to factor out a shared helper.

4. **Prune the `Sum_*.md` interim files** after wiki pages are written, if
   they're not needed as standalone source artifacts. Probably leave them
   for now — they're searchable, useful for re-synthesis, and live next to
   the chapter sources.
