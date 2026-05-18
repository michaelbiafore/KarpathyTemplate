"""Chapter scanner, classifier, and summary assembler.

Provides utilities for the /summarize-chapters slash command:
- Scanning md_out/ for numbered chapter files
- Classifying chapters as content vs. front/back matter
- Assembling individual summary files into a concatenated summary

The actual summarization is performed by Claude Code subagents (no API key needed).
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
    "toc", "endnotes", "appendix",
]

MIN_FILE_SIZE = 500


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


def is_content_chapter(title: str, file_size: int) -> bool:
    """Determine if a chapter file contains actual content (not front/back matter)."""
    title_lower = title.lower()
    if any(pat in title_lower for pat in SKIP_PATTERNS):
        return False
    if re.match(r"^Part\d{4}\b", title):
        return False
    # Skip part dividers like "Part I:", "Part II:", etc.
    if re.match(r"^Part\s+[IVXLC]+\b", title):
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
    """Scan, classify, and assemble chapter summaries."""

    def __init__(self, md_dir: Path, output_dir: Path | None = None):
        self.md_dir = md_dir
        self.output_dir = output_dir or md_dir
        self.book_title = extract_book_title(md_dir)

    def find_chapter_files(self) -> list[Path]:
        """Find numbered chapter files matching NNN_*.md pattern."""
        return sorted(
            p for p in self.md_dir.glob("[0-9][0-9][0-9]_*.md")
            if not p.name.startswith("Sum_")
        )

    def scan(self) -> list[dict]:
        """Scan for content chapters, returning metadata for each.

        Returns list of dicts with keys: path, filename, title, word_count, target_min, target_max
        """
        results = []
        for path in self.find_chapter_files():
            raw = path.read_text(encoding="utf-8")
            title = _extract_frontmatter_title(raw) or path.stem
            file_size = path.stat().st_size

            if not is_content_chapter(title, file_size):
                continue

            body = _strip_frontmatter(raw)
            word_count = len(body.split())
            target_min = word_count // 20
            target_max = word_count // 5

            results.append({
                "path": str(path),
                "filename": path.name,
                "title": title,
                "word_count": word_count,
                "target_min": target_min,
                "target_max": target_max,
            })
        return results

    def assemble(self) -> Path:
        """Concatenate all Sum_NNN_*.md files into Sum_<BookTitle>.md."""
        self.output_dir.mkdir(parents=True, exist_ok=True)

        sum_files = sorted(self.output_dir.glob("Sum_[0-9][0-9][0-9]_*.md"))
        concat_lines = [f"# Summary: {self.book_title}", ""]

        for sum_path in sum_files:
            # Derive chapter title from the original chapter file
            original_name = sum_path.name[4:]  # strip "Sum_"
            original_path = self.md_dir / original_name
            if original_path.exists():
                raw = original_path.read_text(encoding="utf-8")
                title = _extract_frontmatter_title(raw) or original_path.stem
            else:
                title = sum_path.stem[4:]  # strip "Sum_" from stem

            summary_text = sum_path.read_text(encoding="utf-8")
            concat_lines.append("---")
            concat_lines.append("")
            concat_lines.append(f"## {title}")
            concat_lines.append("")
            concat_lines.append(summary_text)
            concat_lines.append("")

        safe_book = sanitize_filename(self.book_title)
        concat_path = self.output_dir / f"Sum_{safe_book}.md"
        concat_path.write_text("\n".join(concat_lines), encoding="utf-8")
        return concat_path


def main(args: list[str] | None = None) -> int:
    """CLI entry point: scan chapters or assemble summaries."""
    parser = argparse.ArgumentParser(
        prog="epub2md-summarize",
        description="Scan chapter files and assemble summaries.",
    )
    sub = parser.add_subparsers(dest="command")

    scan_p = sub.add_parser("scan", help="List content chapters as JSON")
    scan_p.add_argument("md_dir", type=Path, nargs="?", default=Path("md_out"))

    asm_p = sub.add_parser("assemble", help="Concatenate Sum_NNN_*.md files")
    asm_p.add_argument("md_dir", type=Path, nargs="?", default=Path("md_out"))
    asm_p.add_argument("-o", "--output", type=Path, default=None)

    parsed = parser.parse_args(args)

    if parsed.command == "scan":
        if not parsed.md_dir.is_dir():
            print(f"Error: Directory not found: {parsed.md_dir}", file=sys.stderr)
            return 1
        summarizer = ChapterSummarizer(parsed.md_dir)
        chapters = summarizer.scan()
        print(json.dumps(chapters, indent=2))
        return 0

    elif parsed.command == "assemble":
        if not parsed.md_dir.is_dir():
            print(f"Error: Directory not found: {parsed.md_dir}", file=sys.stderr)
            return 1
        summarizer = ChapterSummarizer(parsed.md_dir, parsed.output)
        path = summarizer.assemble()
        print(f"Assembled: {path}")
        return 0

    else:
        parser.print_help()
        return 1


if __name__ == "__main__":
    sys.exit(main())
