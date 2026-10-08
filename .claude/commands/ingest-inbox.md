Process all notes in the inbox folder, classifying and integrating them into the wiki.

## Instructions

1. List all `.md` files in `inbox/` — **exclude** `README.md` and anything in `inbox/processed/`
2. If no files to process, say "Inbox is empty" and stop.
3. For each note:
   a. Read the content.
      - **For `.epub` files:** stop and use `/ingest-epub <path>` instead — it has a dedicated pipeline for books (chapter extraction, summarization via subagents, wiki page synthesis). Do not improvise.
      - **For PDFs:** convert to markdown first via the vendored `pdf2md` package, then `Read` the resulting `.md`:
        ```bash
        ROOT="$(git rev-parse --show-toplevel)"
        PDF2MD="$ROOT/scripts/pdf2md/.venv/Scripts/pdf2md.exe"
        [ -x "$PDF2MD" ] || PDF2MD="$ROOT/scripts/pdf2md/.venv/bin/pdf2md"
        OUT_DIR="$(mktemp -d)/pdf_out"
        "$PDF2MD" "<path>" -o "$OUT_DIR"
        ```
        If `$ROOT/scripts/pdf2md/.venv/` does not exist yet, bootstrap once: `cd "$ROOT/scripts/pdf2md" && uv venv && uv pip install -e .`. If the PDF is a multi-chapter book, stop and use `/ingest-pdf` instead — it routes books into `sources/books/<slug>/` and runs `/summarize-chapters` over them. Do **not** call `Read` on a `.pdf` directly — it renders each page as an image, which is far slower and far more token-expensive than text extraction.
   b. Determine the best category from those listed in CLAUDE.md (currently: `stpa`, `hitl`, `red`, `ontology`, `manage`, `hardware`, `jobs`, `robots`, `geo`, `commercial`, `finance`, `coding`; or a source-type folder: `books`, `arxiv`, `substack`, `youtube`). Always re-check CLAUDE.md's Categories table — it is the source of truth and may have been personalized. If unclear, ask the user.
   c. Decide: should this be merged into an existing wiki page, or does it warrant a new page?
   d. If **merging**: update the existing wiki page with the new information, add to Key Points or Notes section
   e. If **new page**: create a wiki page in `wiki/<category>/` following the standard template (frontmatter, callouts, highlights, wikilinks)
   f. Add cross-references to related existing pages (update both sides)
   g. Update `wiki/index.md` if new pages were created
   h. Append to `wiki/log.md`
4. After processing, move the original note to `inbox/processed/` (create the folder if needed)
5. Report what was processed and what pages were created/updated.
