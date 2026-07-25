# sources/

Layer 1 — raw, immutable source material. **Never edit files here after ingest.**

Sources are organized by type (see the Source Types table in `CLAUDE.md`):

- Web articles → `sources/<category>/` (via `defuddle`)
- Research papers → `sources/arxiv/` (PDF converted via `scripts/pdf2md` first)
- Other PDFs → `sources/<category>/` (convert with `scripts/pdf2md` first)
- Books → `sources/books/<slug>/` (via `/ingest-epub`)
- Substack → `sources/substack/` (via `scripts/fetch_substack.py`)
- YouTube → `sources/youtube/`

Category and type subfolders are created lazily on first ingest — this folder starts empty by design.
