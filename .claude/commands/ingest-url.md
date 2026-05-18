Ingest a web article into the second brain wiki.

## Instructions

1. **Check for duplicates first**: Search `sources/` for files that already contain this URL in their frontmatter (`source:` field). If found, tell the user and ask if they want to re-ingest or skip.

2. **Extract the article**, choosing the right tool for the URL type:

   - **Substack URLs** (any `*.substack.com/p/*` or Substack custom domains where figures matter): use the vendored Playwright-based fetcher. It downloads all figures alongside the markdown and writes directly into `sources/substack/`:
     ```bash
     uv run scripts/fetch_substack.py "$ARGUMENTS" -c cookies_substack.json -o sources/substack
     ```
     Output: `sources/substack/<slug>.md` + `sources/substack/<slug>_figs/`. Skip step 4 (the source is already saved); add frontmatter to the file in place. Do **not** use defuddle for Substack — defuddle's `--md` mode strips images.

   - **PDFs** (URL ending in `.pdf`, or user supplied a local PDF path): convert to markdown first via the vendored `pdf2md` package, then `Read` the resulting `.md`:
     ```bash
     scripts/pdf2md/.venv/Scripts/pdf2md.exe "<file-or-downloaded-path>" -o /tmp/pdf_out
     ```
     If `scripts/pdf2md/.venv/` does not exist yet, bootstrap once with `cd scripts/pdf2md && uv venv && uv pip install -e .`. Do **not** call `Read` on a `.pdf` directly — it renders each page as an image, which is far slower and far more token-expensive than text extraction.

   - **Other web articles**: use defuddle:
     ```bash
     npx defuddle parse "$ARGUMENTS" -p title
     npx defuddle parse "$ARGUMENTS" --md -o /tmp/defuddle-output.md
     ```
     Then read `/tmp/defuddle-output.md`. If defuddle fails, fall back to WebFetch. Note: defuddle drops images — if the article relies on figures, prefer one of the figure-aware paths above or capture screenshots manually.

3. **Determine the best category** from the categories listed in CLAUDE.md (currently: `stpa`, `hitl`, `red`, `ontology`, `manage`, `hardware`, `jobs`, `robots`, `geo`, `commercial`, `finance`, `coding`). If it's a research paper, Substack post, or YouTube transcript, prefer the source-type folder (`arxiv`, `substack`, `youtube`) instead. If the article doesn't fit any category well, ask the user. Always re-check CLAUDE.md's Categories table — it is the source of truth and may have been personalized.

4. **Save the raw source** to `sources/<category>/<kebab-case-title>.md` with frontmatter:
   ```yaml
   ---
   title: "<article title>"
   source: "<the URL>"
   author: "<author if found>"
   published: <date if found>
   created: <today's date>
   tags:
     - <relevant tags>
   ---
   ```
   Followed by the extracted markdown content.

5. **Follow the full ingest workflow** from CLAUDE.md (see "Efficiency Rules"):
   - Scan `wiki/index.md` first; only open pages that plausibly overlap
   - Create a wiki summary page in `wiki/<category>/`
   - Apply the **second-mention rule** for entity pages — inline on first mention, promote on second
   - Add **forward** `[[wikilinks]]` from the new page to related existing pages (lazy backlinks — don't edit other pages just to reciprocate)
   - Cap `## Related` at ~8 links; aim to touch 2-5 pages total
   - Update `wiki/index.md`
   - Append to `wiki/log.md`

6. Use proper Obsidian-flavored markdown: YAML frontmatter, callouts, highlights, nested tags, short wikilinks.

7. Report what pages were created/updated when done.
