Produce LLM-written chapter summaries, a book-level summary, and one stitched
summary file for a directory of converted chapter Markdown — from either
`pdf2md` or `epub2md` output.

The summarization is done by Claude Code **Agent subagents**, so no
`ANTHROPIC_API_KEY` and no API billing are involved. The vendored Python
packages only do the mechanical parts (`scan`, `book-plan`, `assemble`).

> [!important] Not the same thing as `ChapterAbstracts.md`
> `pdf2md` / `epub2md` also emit `ChapterAbstracts.md` during conversion. That
> file is **regex heuristics** — a first-paragraph excerpt plus keyword lists
> from `abstract_writer.py`. It is not a summary and this command does not use
> it. The LLM artifacts this command produces are `Sum_*.md` and
> `Book_Summary_*.md`.

## Usage

```
/summarize-chapters <absolute-md-dir>                  # auto-detect the tool
/summarize-chapters <absolute-md-dir> --tool pdf       # force the pdf2md summarizer
/summarize-chapters <absolute-md-dir> --tool epub      # force the epub2md summarizer
/summarize-chapters <absolute-md-dir> --max-parallel 5 # bigger subagent batches
/summarize-chapters <absolute-md-dir> --no-book-summary  # chapters + concat only
```

## Path contract

This command uses **no relative paths and assumes no sibling repositories**.
Every path is built from one absolutely-resolved root, so it behaves the same
no matter which directory the session is in and does not care whether
`PDF2MD4Claude` or `EPUB2MD4Claude` are checked out anywhere nearby.

### 1. Resolve the vault root and the summarizer executable

```bash
ROOT="$(git rev-parse --show-toplevel)"
```

`$ROOT` is absolute. Resolve the console script for the chosen tool, trying the
Windows layout first and the POSIX layout second:

```bash
TOOL=pdf   # or epub, per --tool / the probe in step 2
SUMMARIZE=""
for cand in \
  "$ROOT/scripts/${TOOL}2md/.venv/Scripts/${TOOL}2md-summarize.exe" \
  "$ROOT/scripts/${TOOL}2md/.venv/bin/${TOOL}2md-summarize"; do
  [ -x "$cand" ] && SUMMARIZE="$cand" && break
done
[ -z "$SUMMARIZE" ] && echo "No ${TOOL}2md venv — bootstrap it first (see SETUP.md)"
```

If `$SUMMARIZE` is empty, the venv has not been bootstrapped on this machine.
Run it once, then continue:

```bash
cd "$ROOT/scripts/${TOOL}2md" && uv venv && uv pip install -e .
```

Also resolve the target directory to an absolute path before passing it on, in
case the user typed a relative one:

```bash
MD_DIR="$(cd "<the-dir-argument>" && pwd)"
```

If that fails, the directory does not exist — stop and say so.

### 2. Determine which tool produced the directory

If `--tool` was passed, use it. Otherwise probe the chapter filename width,
which differs between the two converters (`pdf2md` writes `{n:02d}_`,
`epub2md` writes `{n:03d}_`):

```bash
ls "$MD_DIR" | grep -cE '^[0-9]{2}_.+\.md$'    # > 0  → pdf
ls "$MD_DIR" | grep -cE '^[0-9]{3,4}_.+\.md$'  # > 0  → epub
```

- Only the 2-digit form matches → `--tool pdf`.
- Only the 3-or-4-digit form matches → `--tool epub`.
- **Both or neither match → stop and ask the user** which tool to use. Do not
  guess. (A PDF with 100+ chapters produces 3-digit names and will look like
  epub output; that is exactly the ambiguous case worth asking about.)

### 3. Scan for content chapters

```bash
"$SUMMARIZE" scan "$MD_DIR"
```

Returns a JSON array; each entry has `path`, `filename`, `title`,
`word_count`, `target_min`, `target_max`, `figure_count`, `summary_path` — all
paths absolute. Front/back matter (cover, contents, copyright, dedication,
index, appendix, part dividers) and chapters under 500 bytes are filtered out
already; do not re-filter.

If the array is empty, stop and report that no content chapters were found —
the directory is probably front matter only, or the conversion failed.

### 4. Summarize each chapter via Agent subagents

Dispatch one `Agent` (`subagent_type: general-purpose`) per scan entry. Launch
in batches of `--max-parallel` (default **3**) by putting multiple Agent calls
in a single message, waiting for the batch, then starting the next. This keeps
subagent rate consumption modest on long books.

**Prompt template** — substitute the scan fields:

```
Read the chapter at {path}. Write a summary of this book chapter between
{target_min} and {target_max} words.

Preserve key concepts, arguments, examples, and chapter structure.
Use markdown formatting with headings that mirror the chapter's own sections.
Write the summary to {summary_path}.
Do NOT include YAML frontmatter in the summary.

## Figures, diagrams, and image-based math

This chapter contains {figure_count} inline image reference(s) of the form
`![caption](images/<file>)`. The image files live in the `images/` directory
next to the chapter file and you can open them with the Read tool to see what
each one actually depicts — architectural diagrams, charts, UI screenshots,
conceptual illustrations, or (common in technical EPUBs) rendered equations.

Your task with them:
1. Scan the chapter for every `![...](images/...)` reference.
2. Use the Read tool on a sample of them so you know what they show.
3. Select the most important ones — architectural or system overviews,
   taxonomy and framework diagrams, headline-results charts, defining
   formulas, theorem statements, and any figure later sections build upon.
4. Include those references inline in your summary at the point where they
   belong, preserving the exact markdown syntax including the caption.
5. Keep or restate the italic caption line after each figure
   (e.g. `*Figure 4.1: The three stages of a RAG system*`) so it reads cleanly.

Guidelines:
- Include 1-4 figures for a prose chapter; up to 8 for a math-heavy chapter
  where the equations *are* the content. If figure_count is 0, write a
  text-only summary.
- Skip decorative, navigational, and UI-screenshot figures unless the chapter's
  whole point is that interface.
- If many figures are near-duplicates (a 10-screenshot walkthrough), include
  only the 1-2 most representative.
- Write the image reference EXACTLY as it appears in the chapter source. Never
  invent or adjust an image path — the summary sits in the same directory as
  the chapter, so the relative `images/...` path stays valid as written.
```

If a subagent fails on a chapter, log it and keep going — `book-plan` in the
next step reports every missing summary, and the final report must surface them.

### 5. Plan the book-level summary

```bash
"$SUMMARIZE" book-plan "$MD_DIR"
```

Returns JSON with `book_title`, `chapter_summaries[]` (absolute `path`, `title`,
`word_count`, `figure_count`), `missing_summaries[]`, `total_summary_words`,
`target_min`, `target_max`, `book_summary_path`, `concatenated_path`.

- If `missing_summaries` is non-empty, retry those chapters once (step 4), then
  proceed with whatever succeeded and report the rest as failed.
- If `--no-book-summary` was passed, skip to step 7.

### 6. Synthesize the book-level summary via one Agent subagent

Dispatch a **single** `Agent` (`subagent_type: general-purpose`). Its input is
the **chapter summaries**, not the raw chapters — that is the whole point of
doing it after step 4, and it keeps the synthesis affordable on a long book.

**Prompt template** — substitute from the `book-plan` JSON:

```
You are writing the book-level summary for "{book_title}".

Read these {chapter_summary_count} chapter summaries, in order:
{for each entry in chapter_summaries: "- {path}  ({title})"}

Write a single whole-book summary of between {target_min} and {target_max}
words to {book_summary_path}. Do NOT include YAML frontmatter.

This is a synthesis, not a concatenation — the per-chapter summaries already
exist and get appended to the same output file by a later step, so do not
restate them chapter by chapter. Instead produce:

## What this book is about
Scope, intended reader, and the problem the book sets out to solve.

## The argument
The spine of the book — the claim it builds, and how the parts advance it.
Where chapters depend on each other, say so. Name the organizing structure
(parts, a progression from theory to practice, a running case study).

## Key frameworks and concepts
The named models, methods, taxonomies, or formulas the book introduces or
leans on, each in a sentence or two. These are the entries most likely to
deserve their own wiki page later, so be precise about names.

## Top takeaways
3-6 bullets a reader could act on, each standing on its own.

## Caveats and gaps
What the book assumes, where it is dated, and what it explicitly does not
cover. Omit this section only if the summaries give you nothing for it.

You may include 1-3 of the single most important figures, reusing their exact
`![...](images/...)` references as they appear in the chapter summaries — the
output file sits in the same directory, so those paths stay valid. Choose only
figures that carry the book's central argument.

Ground every claim in the summaries you were given. Do not invent content, and
do not infer what unreadable or missing chapters said.
```

### 7. Assemble the single stitched file

Run this **last** — it picks up the book-level summary automatically and places
it ahead of the per-chapter summaries:

```bash
"$SUMMARIZE" assemble "$MD_DIR"
```

Writes `Sum_<BookTitle>.md` containing `## Book-Level Summary` (if step 6 ran)
followed by `## Per-Chapter Summaries`. It is idempotent — safe to re-run — and
it **fails with exit 1 rather than writing an empty stub** if no per-chapter
summaries exist.

Do not pass `-o` unless you have a specific reason: the summaries carry
relative `images/...` references that only resolve while they sit beside the
`images/` directory.

### 8. Report

```
Summarized: <book_title>
Directory:  <MD_DIR>            (tool: pdf | epub)
Chapters:   N summarized, M skipped as front/back matter, K failed
Book-level: Book_Summary_<Title>.md  (<word count> words)   | skipped
Stitched:   Sum_<Title>.md
Failed chapters: <list>         (omit the line when none)
```

## Artifacts produced

| File | Written by | Content |
|---|---|---|
| `Sum_<NNN>_<chapter>.md` | chapter subagents (step 4) | one LLM summary per content chapter, key figures embedded |
| `Book_Summary_<Title>.md` | book subagent (step 6) | whole-book synthesis built from the chapter summaries |
| `Sum_<Title>.md` | `assemble` (step 7) | book-level summary followed by every chapter summary |

All three land in `<MD_DIR>` alongside `images/`, which is what keeps the
embedded figure references valid.

## Notes

- **Long books (>30 chapters):** keep `--max-parallel` at 3. Bump to 5 only for
  short books where you want speed.
- **Papers and single-document PDFs:** `pdf2md` emits one
  `01_Full_Document.md`, so this command produces a single chapter summary plus
  a book-level summary over it — usually redundant. Prefer
  `--no-book-summary`, or skip the command entirely and let the ingest flow
  read the source directly.
- **Re-running:** chapter subagents overwrite their own `Sum_*` file, and
  `assemble` is idempotent, so re-running is safe. To force fresh summaries,
  delete the `Sum_*.md` and `Book_Summary_*.md` files first.
- **Where this fits:** `/ingest-epub` calls this command as its summarization
  step. `/ingest-pdf` calls it only for multi-chapter PDFs (books, theses).
