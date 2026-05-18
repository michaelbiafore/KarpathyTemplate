"""Table of Contents generation for converted EPUB."""

from pathlib import Path

from .extractor import TOCEntry
from .converter import ConvertedChapter


class TOCGenerator:
    """Generate Markdown Table of Contents from EPUB structure."""

    def __init__(self, book_title: str, book_author: str):
        self.book_title = book_title
        self.book_author = book_author

    def generate(
        self,
        toc_entries: list[TOCEntry],
        chapters: list[ConvertedChapter],
        max_level: int | None = None,
    ) -> str:
        """Generate Table of Contents markdown."""
        # Build href to filename mapping
        href_to_filename = self._build_href_map(chapters)

        lines = [
            f"# {self.book_title}",
            "",
            f"**Author:** {self.book_author}",
            "",
            "---",
            "",
            "## Table of Contents",
            "",
        ]

        # Generate TOC entries
        self._generate_entries(toc_entries, href_to_filename, lines, max_level)

        return "\n".join(lines)

    def _build_href_map(
        self, chapters: list[ConvertedChapter]
    ) -> dict[str, str]:
        """Build mapping from EPUB href to generated filename."""
        href_map = {}
        for chapter in chapters:
            # Map both with and without fragment
            base_href = chapter.source_href.split("#")[0]
            href_map[base_href] = chapter.filename
            href_map[chapter.source_href] = chapter.filename

            # Also map just the filename part
            filename_only = Path(base_href).name
            if filename_only not in href_map:
                href_map[filename_only] = chapter.filename

        return href_map

    def _generate_entries(
        self,
        entries: list[TOCEntry],
        href_map: dict[str, str],
        lines: list[str],
        max_level: int | None,
        current_level: int = 0,
    ) -> None:
        """Recursively generate TOC entries."""
        for entry in entries:
            if max_level is not None and entry.level > max_level:
                continue

            indent = "  " * entry.level
            filename = self._resolve_filename(entry.href, href_map)

            if filename:
                lines.append(f"{indent}- [{entry.title}](./{filename})")
            else:
                # No corresponding file, just show title
                lines.append(f"{indent}- {entry.title}")

            # Process children
            if entry.children:
                self._generate_entries(
                    entry.children, href_map, lines, max_level, current_level + 1
                )

    def _resolve_filename(
        self, href: str, href_map: dict[str, str]
    ) -> str | None:
        """Resolve EPUB href to generated filename."""
        if not href:
            return None

        # Try direct match
        if href in href_map:
            return href_map[href]

        # Try without fragment
        base_href = href.split("#")[0]
        if base_href in href_map:
            return href_map[base_href]

        # Try just filename
        filename_only = Path(base_href).name
        if filename_only in href_map:
            return href_map[filename_only]

        return None

    def write(
        self,
        toc_entries: list[TOCEntry],
        chapters: list[ConvertedChapter],
        output_dir: Path,
        max_level: int | None = None,
    ) -> Path:
        """Write Table of Contents to file."""
        content = self.generate(toc_entries, chapters, max_level)
        output_path = output_dir / "Table_of_Contents.md"
        output_path.write_text(content, encoding="utf-8")
        return output_path
