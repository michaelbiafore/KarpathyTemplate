"""Chapter scanner, classifier, and summary assembler.

Mechanical half of the LLM summarization pipeline driven by the
``/summarize-chapters`` slash command:

- ``scan``      -- find the content chapters (skipping front/back matter),
                   size each one, and emit absolute paths as JSON.
- ``book-plan`` -- list the per-chapter summaries produced by the chapter
                   subagents so a book-level subagent can synthesize a
                   whole-book summary *from those summaries*, and report any
                   that are missing.
- ``assemble``  -- stitch the book-level summary (when present) and every
                   per-chapter summary into a single ``Sum_<BookTitle>.md``.

No LLM call happens in this module. The chapter summaries and the book-level
summary are written by Claude Code subagents (no API key needed); this module
only tells them what to read and then joins the results together.

Path contract: every path accepted or emitted here is absolute. ``md_dir`` is a
required argument and is resolved with :meth:`pathlib.Path.resolve`, so nothing
depends on the working directory of the caller, on a ``md_out`` convention, or
on any sibling repository being checked out next to this one.
"""

import argparse
import json
import re
import sys
from pathlib import Path


SKIP_PATTERNS = [
    "cover", "title", "titlepage", "copyright", "dedication",
    "contents", "table of contents", "acknowledgment", "acknowledgement",
    "about the author", "about the contributor", "index", "colophon",
    "also by", "notes", "bibliography", "series page", "backad",
    "ebookregfront", "ebookregback", "front matter", "back matter",
    "toc", "endnotes", "appendix", "contributors",
    "other books you may enjoy", "free benefits", "unlock your",
]

CHAPTER_FILENAME_RE = re.compile(r"^(\d{2,4})_.+\.md$")
SUMMARY_FILENAME_RE = re.compile(r"^Sum_(\d{2,4})_.+\.md$")

#: Per-chapter summaries are ``Sum_<NNN>_<title>.md``; the book-level summary
#: written by the book subagent is ``Book_Summary_<BookTitle>.md``. The two
#: namespaces are deliberately disjoint so ``assemble`` can tell them apart.
BOOK_SUMMARY_PREFIX = "Book_Summary_"

MIN_FILE_SIZE = 500

#: A book-level summary should be a small fraction of the concatenated chapter
#: summaries -- long enough to carry the argument, short enough to read in one
#: sitting -- with a floor so short books still get a usable overview.
BOOK_TARGET_DIVISOR_MIN = 25
BOOK_TARGET_DIVISOR_MAX = 8
BOOK_TARGET_FLOOR_MIN = 300
BOOK_TARGET_FLOOR_SPAN = 400


def _extract_frontmatter_title(text: str) -> str | None:
    """Extract title from YAML frontmatter."""
    match = re.match(r"^---\s*\n(.*?)\n---", text, re.DOTALL)
    if not match:
        return None
    for line in match.group(1).splitlines():
        m = re.match(r'^title:\s*"?(.*?)"?\s*$', line)
        if m:
            return m.group(1)
    return None


def _strip_frontmatter(text: str) -> str:
    """Remove YAML frontmatter from Markdown text."""
    return re.sub(r"^---\s*\n.*?\n---\s*\n", "", text, count=1, flags=re.DOTALL)


def _count_figures(body: str) -> int:
    """Count inline image references pointing into the sibling images/ dir.

    EPUB books routinely render math as images with an empty alt text, so the
    alt group has to tolerate being empty.
    """
    return len(re.findall(r"!\[.*?\]\(images/[^)]+\)", body))


def is_content_chapter(title: str, file_size: int) -> bool:
    """Determine if a chapter file contains actual content (not front/back matter)."""
    title_lower = title.lower()
    if any(pat in title_lower for pat in SKIP_PATTERNS):
        return False
    # EPUB part dividers arrive both as "Part0001" ids and as "Part I:" titles.
    if re.match(r"^part\d{4}\b", title_lower):
        return False
    if re.match(r"^part\s+[ivxlc]+\b", title_lower):
        return False
    if file_size < MIN_FILE_SIZE:
        return False
    return True


def extract_book_title(md_dir: Path) -> str:
    """Extract book title from Table_of_Contents.md or fall back to directory name."""
    toc_path = md_dir / "Table_of_Contents.md"
    if toc_path.exists():
        text = toc_path.read_text(encoding="utf-8")
        # The first H1 heading is typically the book title
        for line in text.splitlines():
            if line.startswith("# ") and "table of contents" not in line.lower():
                return line[2:].strip()
    return md_dir.name


def sanitize_filename(name: str) -> str:
    """Create a filesystem-safe filename from a string."""
    safe = re.sub(r"[^\w\s-]", "", name)
    safe = re.sub(r"\s+", "_", safe.strip())
    return safe[:60].rstrip("_")


class ChapterSummarizer:
    """Scan and classify chapters, plan the book summary, assemble the result.

    Args:
        md_dir: Directory holding the converted chapter Markdown. Required, and
            resolved to an absolute path.
        output_dir: Where summaries are read from and written to. Defaults to
            ``md_dir``, which is almost always what you want -- summaries embed
            ``images/...`` references relative to their own directory, so moving
            them elsewhere breaks those references.
    """

    def __init__(self, md_dir: Path, output_dir: Path | None = None):
        self.md_dir = Path(md_dir).resolve()
        self.output_dir = Path(output_dir).resolve() if output_dir else self.md_dir
        self.book_title = extract_book_title(self.md_dir)

    @property
    def safe_book_title(self) -> str:
        return sanitize_filename(self.book_title)

    @property
    def book_summary_path(self) -> Path:
        """Absolute path the book-level subagent should write to."""
        return self.output_dir / f"{BOOK_SUMMARY_PREFIX}{self.safe_book_title}.md"

    @property
    def concatenated_path(self) -> Path:
        """Absolute path of the single stitched-together summary file."""
        return self.output_dir / f"Sum_{self.safe_book_title}.md"

    def find_chapter_files(self) -> list[Path]:
        """Find numbered chapter files, excluding any summary output."""
        return sorted(
            p for p in self.md_dir.iterdir()
            if p.is_file()
            and CHAPTER_FILENAME_RE.match(p.name)
            and not p.name.startswith("Sum_")
            and not p.name.startswith(BOOK_SUMMARY_PREFIX)
        )

    def find_summary_files(self) -> list[Path]:
        """Find the per-chapter summary files written by the chapter subagents."""
        return sorted(
            p for p in self.output_dir.iterdir()
            if p.is_file() and SUMMARY_FILENAME_RE.match(p.name)
        )

    def summary_path_for(self, chapter_path: Path) -> Path:
        """Absolute path of the summary that belongs to a given chapter file."""
        return self.output_dir / f"Sum_{chapter_path.name}"

    def _chapter_title(self, chapter_path: Path) -> str:
        if chapter_path.exists():
            raw = chapter_path.read_text(encoding="utf-8")
            return _extract_frontmatter_title(raw) or chapter_path.stem
        return chapter_path.stem

    def _content_chapters(self) -> list[tuple[Path, str]]:
        """Content chapter files paired with their titles, front matter dropped."""
        kept = []
        for path in self.find_chapter_files():
            raw = path.read_text(encoding="utf-8")
            title = _extract_frontmatter_title(raw) or path.stem
            if is_content_chapter(title, path.stat().st_size):
                kept.append((path, title))
        return kept

    def scan(self) -> list[dict]:
        """Scan for content chapters, returning metadata for each.

        Returns a list of dicts with keys: path, filename, title, word_count,
        target_min, target_max, figure_count, summary_path. All paths absolute.
        """
        results = []
        for path, title in self._content_chapters():
            body = _strip_frontmatter(path.read_text(encoding="utf-8"))
            word_count = len(body.split())
            target_min = max(50, word_count // 20)
            target_max = max(target_min + 50, word_count // 5)

            results.append({
                "path": str(path),
                "filename": path.name,
                "title": title,
                "word_count": word_count,
                "target_min": target_min,
                "target_max": target_max,
                "figure_count": _count_figures(body),
                "summary_path": str(self.summary_path_for(path)),
            })
        return results

    def book_plan(self) -> dict:
        """Describe the inputs and target for the book-level summary subagent.

        The book-level summary is synthesized from the *chapter summaries*, not
        from the raw chapters, so this reports exactly which summary files exist,
        which are still missing (a chapter subagent that failed), and how long
        the result should be.
        """
        chapter_summaries = []
        missing = []
        total_words = 0

        for chapter_path, title in self._content_chapters():
            summary_path = self.summary_path_for(chapter_path)
            if not summary_path.exists():
                missing.append({
                    "chapter_filename": chapter_path.name,
                    "title": title,
                    "expected_summary_path": str(summary_path),
                })
                continue

            body = _strip_frontmatter(summary_path.read_text(encoding="utf-8"))
            words = len(body.split())
            total_words += words
            chapter_summaries.append({
                "path": str(summary_path),
                "summary_filename": summary_path.name,
                "chapter_filename": chapter_path.name,
                "title": title,
                "word_count": words,
                "figure_count": _count_figures(body),
            })

        target_min = max(BOOK_TARGET_FLOOR_MIN, total_words // BOOK_TARGET_DIVISOR_MIN)
        target_max = max(target_min + BOOK_TARGET_FLOOR_SPAN,
                         total_words // BOOK_TARGET_DIVISOR_MAX)

        images_dir = self.md_dir / "images"
        return {
            "book_title": self.book_title,
            "md_dir": str(self.md_dir),
            "output_dir": str(self.output_dir),
            "images_dir": str(images_dir) if images_dir.is_dir() else None,
            "chapter_summaries": chapter_summaries,
            "missing_summaries": missing,
            "chapter_summary_count": len(chapter_summaries),
            "total_summary_words": total_words,
            "target_min": target_min,
            "target_max": target_max,
            "book_summary_path": str(self.book_summary_path),
            "concatenated_path": str(self.concatenated_path),
        }

    def find_book_summary(self) -> Path | None:
        """Locate the book-level summary, if a subagent has written one."""
        exact = self.book_summary_path
        if exact.exists():
            return exact
        candidates = sorted(
            p for p in self.output_dir.iterdir()
            if p.is_file()
            and p.name.startswith(BOOK_SUMMARY_PREFIX)
            and p.suffix == ".md"
        )
        return candidates[0] if candidates else None

    def assemble(self) -> Path:
        """Stitch the book-level summary and all chapter summaries into one file.

        Returns the path of the written file.

        Raises:
            FileNotFoundError: if no per-chapter summaries exist yet. Writing a
                title-only stub in that case would silently look like success.
        """
        self.output_dir.mkdir(parents=True, exist_ok=True)

        sum_files = self.find_summary_files()
        if not sum_files:
            raise FileNotFoundError(
                f"No per-chapter summaries (Sum_<NNN>_*.md) found in {self.output_dir}. "
                "Run the chapter-summary subagents first -- see the "
                "/summarize-chapters slash command."
            )

        lines = [f"# Summary: {self.book_title}", ""]

        book_summary = self.find_book_summary()
        if book_summary:
            body = _strip_frontmatter(book_summary.read_text(encoding="utf-8")).strip()
            lines.append("## Book-Level Summary")
            lines.append("")
            lines.append(body)
            lines.append("")
            lines.append("---")
            lines.append("")
            lines.append("## Per-Chapter Summaries")
            lines.append("")

        for sum_path in sum_files:
            original_path = self.md_dir / sum_path.name[4:]  # strip "Sum_"
            title = self._chapter_title(original_path)
            lines.append("---")
            lines.append("")
            lines.append(f"## {title}")
            lines.append("")
            lines.append(sum_path.read_text(encoding="utf-8").strip())
            lines.append("")

        concat_path = self.concatenated_path
        concat_path.write_text("\n".join(lines), encoding="utf-8")
        return concat_path


def _resolved_dir(raw: str) -> Path:
    """argparse type: resolve to an absolute directory path."""
    return Path(raw).expanduser().resolve()


def main(args: list[str] | None = None) -> int:
    """CLI entry point: scan chapters, plan the book summary, or assemble."""
    parser = argparse.ArgumentParser(
        prog="epub2md-summarize",
        description="Scan EPUB-derived chapter files, plan the book-level summary, "
                    "and assemble summaries. All paths are absolute; md_dir is "
                    "required.",
    )
    sub = parser.add_subparsers(dest="command")

    scan_p = sub.add_parser("scan", help="List content chapters as JSON")
    scan_p.add_argument("md_dir", type=_resolved_dir,
                        help="Directory of converted chapter Markdown")

    plan_p = sub.add_parser(
        "book-plan",
        help="List the per-chapter summaries and the book-summary target, as JSON",
    )
    plan_p.add_argument("md_dir", type=_resolved_dir)
    plan_p.add_argument("-o", "--output", type=_resolved_dir, default=None,
                        help="Directory holding the Sum_* files (default: md_dir)")

    asm_p = sub.add_parser(
        "assemble",
        help="Concatenate the book-level summary (if any) and all Sum_<NNN>_*.md files",
    )
    asm_p.add_argument("md_dir", type=_resolved_dir)
    asm_p.add_argument("-o", "--output", type=_resolved_dir, default=None,
                       help="Directory holding the Sum_* files (default: md_dir). "
                            "Pointing this elsewhere breaks the relative images/ "
                            "references embedded in the summaries.")

    parsed = parser.parse_args(args)

    if parsed.command is None:
        parser.print_help()
        return 1

    if not parsed.md_dir.is_dir():
        print(f"Error: Directory not found: {parsed.md_dir}", file=sys.stderr)
        return 1

    if parsed.command == "scan":
        summarizer = ChapterSummarizer(parsed.md_dir)
        print(json.dumps(summarizer.scan(), indent=2))
        return 0

    if parsed.command == "book-plan":
        summarizer = ChapterSummarizer(parsed.md_dir, parsed.output)
        print(json.dumps(summarizer.book_plan(), indent=2))
        return 0

    if parsed.command == "assemble":
        summarizer = ChapterSummarizer(parsed.md_dir, parsed.output)
        try:
            path = summarizer.assemble()
        except FileNotFoundError as exc:
            print(f"Error: {exc}", file=sys.stderr)
            return 1
        print(f"Assembled: {path}")
        return 0

    parser.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
