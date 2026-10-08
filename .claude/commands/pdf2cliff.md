Turn a PDF — an article or a 450-page book — into an illustrated, page-budgeted
"cliff notes" summary delivered as **one portable HTML file** you can attach to
an email.

Three stages: summarize every chapter, synthesize one overall summary at the
requested length, then render it to self-contained HTML in the house style from
`Refs/formatted_transcript_style.html`. The summarization is done by Claude Code
Agent subagents — no `ANTHROPIC_API_KEY`, no API billing.

The deliberate bias is **figure-heavy**: roughly 1.2 graphics per finished page,
with the prose budget reduced to make room. This is a command for illustrated
source material.

## Usage

```
/pdf2cliff <target-pages> <path-to.pdf>
/pdf2cliff <path-to.pdf> <target-pages>     # same thing, order does not matter
```

The one knob is `<target-pages>`: how many pages the finished summary should run
to. Arguments are told apart by shape, not position — a bare integer is the page
target, anything ending in `.pdf` is the source — so either order works and
neither can be mistaken for the other.

```
/pdf2cliff 3 "A:/_Wikis/KarpathyTemplate/inbox/The Ontology Pipeline_13pp.pdf"
/pdf2cliff 12 "A:/_Wikis/KarpathyTemplate/inbox/An Illustrated Guide to AI Agents_451pp.pdf"
```

## Path contract

Resolve the vault root once, absolutely, and build every path from it. Nothing
depends on the working directory or on a sibling repository:

```bash
ROOT="$(git rev-parse --show-toplevel)"
PDF2MD="$ROOT/scripts/pdf2md/.venv/Scripts/pdf2md.exe"
[ -x "$PDF2MD" ] || PDF2MD="$ROOT/scripts/pdf2md/.venv/bin/pdf2md"
SUMMARIZE="$ROOT/scripts/pdf2md/.venv/Scripts/pdf2md-summarize.exe"
[ -x "$SUMMARIZE" ] || SUMMARIZE="$ROOT/scripts/pdf2md/.venv/bin/pdf2md-summarize"
STYLE="$ROOT/Refs/formatted_transcript_style.html"
BUILDER="$ROOT/scripts/md2cliff_html.py"
```

If `$PDF2MD` is missing, bootstrap once and continue:
`cd "$ROOT/scripts/pdf2md" && uv venv && uv pip install -e .`

## Pipeline

### 1. Parse and validate

- Split `$ARGUMENTS`. The token matching `^[0-9]+$` is `PAGES`; the token ending
  in `.pdf` (case-insensitive) is `PDF`.
- Both must be present. If either is missing, print the usage block and stop.
- `PAGES` must be between 1 and 60. Outside that, stop and say so.
- Resolve the PDF to an absolute path and confirm it exists.

### 2. Compute the budget

This is the whole mechanism for hitting the requested length, so compute it
explicitly rather than eyeballing it. The numbers are in CSS pixels because
that is what actually determines length — a word count alone ignores headings,
the contents panel and figure margins, which in a short illustrated document
account for more height than the prose does.

```
FIGURES    = max(1, round(0.8 * PAGES))
SECTIONS   = max(2, round(1.3 * PAGES))  # `##` headings; the real length lever
HEADING_PX = 190 + SECTIONS * 120        # contents panel + headings
PROSE_PX   = PAGES * 1000 - 260 - HEADING_PX - FIGURES * 490
WORDS      = max(120, round(PROSE_PX / 2.95))
```

Where the constants come from, all calibrated against a headless-Chromium
render of a real output file:

| Constant | Meaning |
|---|---|
| `1000` | usable CSS px in one page |
| `260` | fixed document chrome — body padding, title, subtitle |
| `490` | a figure plus its margins and caption, averaged |
| `2.95` | px per prose word (28px line / 9.5 words per line, measured) |
| `120` | a heading plus its generous top margin, averaged over `##` and `###` |
| `190` | the boxed contents panel |

Worked examples: 3 pages → 2 figures, 4 sections, ~370 words; 12 pages → 10
figures, 16 sections, ~1,660 words.

> [!warning] Section count is the lever people forget
> Headings are expensive in this stylesheet — `h2` carries a 2.6rem top margin
> plus 1.2rem padding and a rule, about 95px before a word is set, and the
> contents panel costs another ~190px. A first pass on a 3-page target came
> back with 8 headings and overshot by 22% on heading cost alone, even after
> the prose was cut 37%. Pass `SECTIONS` to the subagent as a hard cap.

> [!note] Why only 0.8 figures per page, given the figure-heavy brief
> Because each figure already eats roughly half a page in this stylesheet
> (17px type, 1.65 line-height, an 880px column). At 0.8/page the figures still
> occupy about 40% of the total area — genuinely figure-dominated — while
> leaving prose that is readable rather than vestigial. Pushing to 1.2/page
> drives a 3-page budget down to under 100 words, which is not a summary.

State `WORDS` and `FIGURES` to the user before starting. The renderer's own
estimate in step 6 is the authority on length; these numbers only aim the
first draft.

### 3. Derive the slug and convert

```bash
SLUG="<author-or-topic>-<short-title>"          # kebab-case, <= 40 chars
WORK="$ROOT/sources/books/$SLUG"
"$PDF2MD" "$PDF" -o "$WORK" -v
```

The converted chapters and `images/` stay in `sources/` as the durable record,
so a later `/ingest-pdf` or `/ingest-epub`-style wiki ingest reuses them instead
of re-converting. Confirm `$WORK` has chapter files and a non-empty `images/`.

> [!note] If `images/` is empty
> There is nothing to illustrate with. Say so and ask whether to continue
> text-only before spending subagent time.

### 4. Summarize the chapters

First find out how finely the book is chaptered — this decides the whole shape
of the stage:

```bash
"$SUMMARIZE" scan "$WORK" | python -c "import json,sys; d=json.load(sys.stdin); print(len(d),'content chapters,',sum(c['word_count'] for c in d),'words')"
```

**Single chapter** (a paper or article — `01_Full_Document.md`): skip the
chapter stage entirely and jump to step 5, which reads the source directly.
Summarizing one chapter only to summarize the summary loses detail for nothing.

**2 to ~30 chapters**: one subagent per chapter.

```
/summarize-chapters "$WORK" --tool pdf --max-parallel 3 --no-book-summary
```

`--no-book-summary` is deliberate: that command's own synthesis is sized by its
own formula, and step 5 needs one written to `PAGES` instead.

**More than ~30 chapters — bundle them.** A 450-page illustrated title can
split into 150+ TOC entries averaging a few hundred words each. One subagent
per entry is slow and wasteful, so group adjacent sections:

```bash
"$SUMMARIZE" bundle "$WORK" --max-words 6000
```

Each bundle carries `chapters[]` (absolute paths, in reading order),
`word_count`, `figure_count`, `target_min`/`target_max`, and the absolute
`summary_path` to write. Dispatch one subagent per **bundle**, 3 at a time,
with the chapter-subagent prompt from `/summarize-chapters` step 4 adapted to
read every file in `chapters[]` and write one combined summary to
`summary_path`. Tell it to keep the sections' own headings so the result still
reads front-to-back.

> [!warning] Duplicate and overlapping chapter files
> `pdf2md` gives every TOC entry the full text of the page it starts on, so
> entries that share a start page come out carrying that page verbatim. In the
> 451-page test book: 8 groups of body-identical files, 10 redundant copies
> (6% of all chapter files, 3% of the words), plus partial page-boundary
> overlap in which 23 of 157 adjacent pairs shared more than 80% of their
> lines. `scan` and `bundle` word counts run high accordingly.
>
> These files are **not** byte-identical — the frontmatter `title`,
> `chapter_number` and the H1 all differ — so a checksum or `cmp` comparison
> will not find them. Compare bodies with the frontmatter and title lines
> stripped. Tell the chapter/bundle subagents to attribute shared material to
> the chapter it belongs to and summarize it once; the prompts below do.

> [!note] Why 6000 words
> It keeps a bundle inside a comfortable single-subagent read while cutting
> 151 chapters to ~20 bundles — about 7 batches instead of 51. Raise it to
> trade fidelity for speed; lower it if summaries come back too compressed.

Either way, note any chapters or bundles that failed and carry them into the
final report.

### 5. Synthesize the overall summary at the target length

```bash
"$SUMMARIZE" summaries "$WORK"
```

This lists the summary files that actually exist — it does not care whether
they came one-per-chapter or one-per-bundle — plus `book_title`, `images_dir`,
and `total_summary_words`.

Dispatch **one** Agent (`subagent_type: general-purpose`) with this prompt,
substituting the budget from step 2:

```
You are writing an illustrated cliff-notes summary of "{book_title}".

Read these {count} summaries, in order:
{for each entry in summaries: "- {path}  ({title})"}

[Single-chapter sources only: also read the original chapter file directly —
 it is short enough, and the full text gives better detail than its own
 summary. Use the summary mainly as a hint about which figures matter.]

Write it to {WORK}/cliff.md. No YAML frontmatter.

## Hard budget
- Prose: about {WORDS} words of body text, excluding captions. Within 10%.
- Figures: about {FIGURES} images. Within one or two.

These are tight. Spend the words on the load-bearing argument and let the
figures carry the rest — that is the point of this format, not a compromise.

## Structure
Use AT MOST {SECTIONS} `##` sections, and prefer no `###` subsections at all —
headings are expensive here and every one you add comes out of the prose and
figure budget.

Start with `## Table of Contents` followed by a bulleted list of the `##`
section headings that follow it (the stylesheet renders this list as a boxed
contents panel; it counts as one of your sections). Then the sections
themselves. Do NOT write an H1 — the renderer adds the title.

Write the contents entries as PLAIN TEXT, not as markdown links. The renderer
turns each one into a live in-page link automatically. For that to work, each
entry must repeat its section heading's text exactly — same words, same
punctuation, same order. Do not paraphrase, truncate or re-order them.

Use the stylesheet's vocabulary where the content calls for it:
- `> blockquote` for a claim worth quoting verbatim from the source
- a markdown table where the source genuinely tabulates something
- `**bold**` for the terms a reader should leave knowing
- `` `code` `` for literal identifiers, model names, API names

## Figures — the priority of this format
Every summary carries image references of the form `![caption](images/<file>)`.
The files are real, on disk at {images_dir}, and you can open them with the
Read tool to see what each one depicts.

1. Collect every `![...](images/...)` reference across all the summaries.
2. Read enough of the actual image files to know what they show. Do not choose
   from filenames alone.
3. Pick the {FIGURES} that carry the most meaning per unit of page space:
   system and architecture diagrams, taxonomies and frameworks, the chart that
   shows the headline result, a worked example that a paragraph could not
   replace. Prefer a figure over a paragraph whenever it would say the same
   thing.
4. Place each one in the section it belongs to, reproducing the reference
   EXACTLY as it appears in the summary — same path, same alt text. Never
   invent, edit, or guess an image path; a reference that does not resolve is
   dropped silently by the renderer.
5. Follow each figure with its caption on its own line as italics only:
   `*Figure 4.1: what it shows.*` The stylesheet styles a lone-italic
   paragraph as a caption. Note that `pdf2md` writes useless placeholder alt
   texts ("Figure on page 7"), so the italic line must be a real one-sentence
   description of what the figure actually shows — written from having looked
   at it — and what the reader should take from it.

Skip decorative, navigational, and screenshot figures unless the interface is
itself the subject. If several figures are near-duplicates, take the clearest.

Ground every claim in the summaries you were given. Do not invent content and
do not infer what a missing chapter said.
```

### 6. Render the portable HTML

```bash
mkdir -p "$ROOT/cliffs"
OUT="$ROOT/cliffs/$SLUG-cliff-${PAGES}pp.html"
uv run "$BUILDER" \
  --md "$WORK/cliff.md" \
  --images-dir "$WORK/images" \
  --style "$STYLE" \
  --out "$OUT" \
  --title "<document title>" \
  --subtitle "<author> · cliff notes · target ${PAGES} pages" \
  --target-pages "$PAGES"
```

The builder prints a JSON report: `words`, `figures`, `estimated_pages`,
`pages_delta`, `html_bytes`, `missing_images`, `over_max_bytes`.

What it guarantees, and why each matters for email:

| Concern | How it is handled |
|---|---|
| Unknown paths on the recipient's machine | every image embedded as a `data:` URI; zero external references |
| Gmail/Outlook strip `<head><style>` | every inlinable declaration also written as a `style=` attribute |
| `var(--accent)` unsupported in mail clients | custom properties resolved to literal values at build time |
| Web fonts unavailable | system font stack only, as the reference stylesheet already specifies |
| Figure lettering too large or soft | a figure is never upscaled past its intrinsic pixel width |
| One figure eating a whole page | portrait figures capped at half column, any figure capped at 820px tall |
| 25 MB mail attachment limits | images downscaled to 2x display width, oversized PNGs re-encoded; warns past `--max-bytes` |
| Contents panel should be navigable | every entry auto-linked to its section's heading id; `toc_links` and `toc_unlinked` reported |

#### Live contents links

The renderer links the contents panel for you — it matches each list entry
against the heading ids that python-markdown has already stamped on every
`##`/`###`, so slugs cannot drift from the ids actually emitted. Matching is on
heading text: exact first, then a unique prefix match either way round. An
entry matching nothing is left as plain text, because a dead `#fragment` is
worse than no link.

Check `toc_links` and `toc_unlinked` in the report. Anything in `toc_unlinked`
means that entry's wording drifted from its heading — send the exact heading
text back to the subagent rather than hand-editing the HTML.

> [!note] Where the links work
> In-page `#fragment` links work in any browser, which is how an attachment is
> normally read, and the stylesheet's `scroll-behavior: smooth` applies there
> too. Some webmail clients rewrite or strip in-body anchors when a message is
> displayed inline, so treat the links as a bonus for the attachment rather
> than a guarantee for every preview pane.

### 7. Close the loop on length

Read `pages_delta` from the report.

- Within **±20%** of `PAGES`: done.
- Outside it: send the cliff subagent **one** revision instruction — cut or add
  the specific number of words and figures the delta implies — then re-run step
  6. Do this at most twice; the estimate is a model, not a measurement, and
  chasing it further is not worth the tokens.
- `toc_unlinked` non-empty: those contents entries did not match a heading.
  Give the subagent the exact heading text and have it fix the entry wording.
- `missing_images` non-empty: those references did not resolve and were dropped.
  Tell the subagent the exact filenames it got wrong and have it substitute real
  ones from the pool.
- `over_max_bytes` true: re-run step 6 with `--retina 1` first; if still over,
  cut the largest figures.

### 8. Report

```
Cliff notes: <title>
Source:      <PDF>  (<n> pages)
Summarized:  N chapters
Budget:      <PAGES> pages -> ~<WORDS> words + ~<FIGURES> figures
Rendered:    <estimated_pages> est. pages, <figures> figures, <toc_links> live contents links
Output:      <OUT>  (<size> MB, fully self-contained)
Dropped figures: <list>        (omit when none)
```

Tell the user the file is ready to attach to an email as-is.

## Notes

- **This command does not write wiki pages.** It produces a deliverable. The
  conversion and chapter summaries it leaves in `$WORK` are exactly what
  `/ingest-pdf` needs, so run that afterwards if you also want the material in
  the wiki — it will not redo the expensive work.
- **Cost scales with the source, not the target.** A 451-page book needs every
  chapter summarized before the overall summary can be written, whether you
  asked for 5 pages or 30. Stage 4 is the expensive one.
- **Long books:** keep `--max-parallel` at 3. Chapter count, not page count,
  drives subagent volume.
- **Re-running at a different length is cheap.** The chapter summaries persist
  in `$WORK`, so a second `/pdf2cliff` on the same PDF skips straight to stage
  5 if the `Sum_*` files are already there. Check before re-converting.
- **`ChapterAbstracts.md` is not used.** `pdf2md` writes it from regex
  heuristics during conversion; it is not a summary. Stages 4 and 5 are the LLM
  work.
- **`cliffs/` is the output folder.** One HTML per source per target length.
