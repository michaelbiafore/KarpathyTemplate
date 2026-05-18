"""Generate Table of Contents Markdown file."""

from pathlib import Path
from typing import Optional

from .chapter_splitter import BookStructure, Chapter, ChapterSplitter


class TOCGenerator:
    """Generate Table of Contents as Markdown."""

    def __init__(self, structure: BookStructure, splitter: ChapterSplitter):
        self.structure = structure
        self.splitter = splitter

    def generate(self, output_dir: Optional[Path] = None) -> str:
        """Generate Table of Contents Markdown.

        Args:
            output_dir: If provided, generate relative links to chapter files

        Returns:
            Formatted Markdown TOC
        """
        lines = [
            "# Table of Contents",
            "",
            f"**{self.structure.title}**",
            "",
        ]

        # Front matter
        if self.structure.front_matter:
            lines.extend(self._format_entry(
                self.structure.front_matter,
                output_dir,
                prefix=""
            ))

        # Track current part for grouping
        current_part = None

        # Main chapters
        for chapter in self.structure.chapters:
            # Check if we're in a new part
            if chapter.parent_title and chapter.parent_title != current_part:
                current_part = chapter.parent_title
                lines.append("")
                lines.append(f"## {current_part}")
                lines.append("")

            lines.extend(self._format_entry(chapter, output_dir))

        # Back matter
        if self.structure.back_matter:
            lines.append("")
            lines.append("## Appendices")
            lines.append("")
            for chapter in self.structure.back_matter:
                lines.extend(self._format_entry(chapter, output_dir, prefix=""))

        return "\n".join(lines)

    def _format_entry(
        self,
        chapter: Chapter,
        output_dir: Optional[Path],
        prefix: Optional[str] = None
    ) -> list[str]:
        """Format a single TOC entry.

        Args:
            chapter: Chapter to format
            output_dir: Output directory for relative links
            prefix: Optional prefix override (None = use level-based indent)

        Returns:
            List of formatted lines
        """
        # Determine indentation based on level
        if prefix is not None:
            indent = prefix
        else:
            indent = "  " * (chapter.level - 1)

        # Build entry text
        title = chapter.title
        page_ref = f"(p. {chapter.start_page + 1})"  # 1-indexed for display

        # Create link if output_dir provided
        if output_dir:
            filename = self.splitter.get_chapter_filename(chapter)
            entry = f"{indent}- [{title}](./{filename}) {page_ref}"
        else:
            entry = f"{indent}- {title} {page_ref}"

        return [entry]

    def write(self, output_path: Path) -> None:
        """Write TOC to file.

        Args:
            output_path: Full path to output file
        """
        content = self.generate(output_path.parent)
        output_path.write_text(content, encoding="utf-8")
