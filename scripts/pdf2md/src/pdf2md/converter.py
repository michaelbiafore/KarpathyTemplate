"""Convert extracted PDF text to clean Markdown."""

import re
from typing import Optional

from .chapter_splitter import Chapter


class MarkdownConverter:
    """Convert raw PDF text to clean Markdown format."""

    # Common page header/footer patterns to remove
    HEADER_FOOTER_PATTERNS = [
        r"^\d+\s*\|\s*.+$",  # "123 | Chapter Title" style
        r"^.+\s*\|\s*\d+$",  # "Chapter Title | 123" style
        r"^\d+$",  # Standalone page numbers
        r"^Page\s+\d+\s*(of\s+\d+)?$",  # "Page X of Y"
        r"^Chapter\s+\d+$",  # Repeated chapter headers
    ]

    # Figure/table detection patterns
    FIGURE_PATTERN = r"(Figure|Fig\.?)\s*(\d+[\.-]?\d*)"
    TABLE_PATTERN = r"(Table)\s*(\d+[\.-]?\d*)"

    def __init__(self, image_extractor=None):
        self._header_footer_re = [
            re.compile(p, re.IGNORECASE | re.MULTILINE)
            for p in self.HEADER_FOOTER_PATTERNS
        ]
        self.image_extractor = image_extractor

    def convert(self, chapter: Chapter, include_frontmatter: bool = True) -> str:
        """Convert chapter to Markdown format.

        Args:
            chapter: Chapter object with raw_text
            include_frontmatter: Whether to add YAML frontmatter

        Returns:
            Formatted Markdown string
        """
        text = chapter.raw_text

        # Clean the text
        text = self._remove_headers_footers(text)
        text = self._normalize_whitespace(text)
        text = self._detect_and_format_lists(text)
        text = self._format_figures_tables(text)
        text = self._format_code_blocks(text)
        text = self._substitute_image_markers(text)

        # Build final markdown
        parts = []

        if include_frontmatter:
            parts.append(self._create_frontmatter(chapter))

        # Add chapter title as H1
        parts.append(f"# {chapter.title}\n")

        # Add content
        parts.append(text)

        return "\n".join(parts)

    def _create_frontmatter(self, chapter: Chapter) -> str:
        """Generate YAML frontmatter for chapter."""
        lines = [
            "---",
            f'title: "{chapter.title}"',
            f"chapter_number: {chapter.number}",
            f"page_start: {chapter.start_page + 1}",  # 1-indexed for display
            f"page_end: {chapter.end_page + 1}",
        ]

        if chapter.parent_title:
            lines.append(f'part: "{chapter.parent_title}"')

        lines.append("---")
        return "\n".join(lines)

    def _remove_headers_footers(self, text: str) -> str:
        """Remove common page headers and footers."""
        lines = text.split("\n")
        cleaned_lines = []

        for line in lines:
            stripped = line.strip()
            is_header_footer = False

            for pattern in self._header_footer_re:
                if pattern.match(stripped):
                    is_header_footer = True
                    break

            if not is_header_footer:
                cleaned_lines.append(line)

        return "\n".join(cleaned_lines)

    def _normalize_whitespace(self, text: str) -> str:
        """Normalize whitespace while preserving paragraph breaks."""
        # Replace multiple spaces with single space
        text = re.sub(r"[ \t]+", " ", text)

        # Normalize line endings
        text = text.replace("\r\n", "\n").replace("\r", "\n")

        # Replace 3+ newlines with 2 (paragraph break)
        text = re.sub(r"\n{3,}", "\n\n", text)

        # Remove trailing whitespace from lines
        lines = [line.rstrip() for line in text.split("\n")]
        text = "\n".join(lines)

        return text.strip()

    def _detect_and_format_lists(self, text: str) -> str:
        """Detect and format bullet and numbered lists."""
        lines = text.split("\n")
        formatted_lines = []

        for line in lines:
            stripped = line.strip()

            # Detect bullet points (various markers)
            bullet_match = re.match(r"^[•●○◦▪▸►-]\s*(.+)$", stripped)
            if bullet_match:
                formatted_lines.append(f"- {bullet_match.group(1)}")
                continue

            # Detect numbered lists
            number_match = re.match(r"^(\d+)[.)]\s*(.+)$", stripped)
            if number_match:
                formatted_lines.append(f"{number_match.group(1)}. {number_match.group(2)}")
                continue

            formatted_lines.append(line)

        return "\n".join(formatted_lines)

    def _format_figures_tables(self, text: str) -> str:
        """Convert figure and table references to Markdown placeholders.

        When an image has already been emitted for this figure number (via the
        image extractor), leave the original text alone so we don't clutter the
        chapter with `[Figure X: *description*]` next to a real image.
        """
        known_ids = (
            self.image_extractor.caption_ids
            if self.image_extractor is not None
            else set()
        )

        def figure_sub(match: re.Match) -> str:
            fig_id = match.group(2)
            if fig_id in known_ids:
                return match.group(0)  # keep original "Figure 3.2" text reference
            return f"[Figure {fig_id}: *description*]"

        def table_sub(match: re.Match) -> str:
            tbl_id = match.group(2)
            if tbl_id in known_ids:
                return match.group(0)
            return f"[Table {tbl_id}: *description*]"

        text = re.sub(self.FIGURE_PATTERN, figure_sub, text, flags=re.IGNORECASE)
        text = re.sub(self.TABLE_PATTERN, table_sub, text, flags=re.IGNORECASE)
        return text

    def _substitute_image_markers(self, text: str) -> str:
        """Replace ⟪IMG:xref⟫ markers with Markdown image blocks."""
        if self.image_extractor is None:
            return text

        by_xref = self.image_extractor.by_xref

        def replace(match: re.Match) -> str:
            xref = int(match.group(1))
            img = by_xref.get(xref)
            if img is None:
                return ""
            alt = img.caption or f"Figure on page {img.page_num + 1}"
            # Escape any bracket chars in alt text for Markdown safety
            alt_safe = alt.replace("]", ")").replace("[", "(")
            block = f"\n\n![{alt_safe}]({img.rel_path})\n"
            if img.caption:
                block += f"\n*{img.caption}*\n"
            return block

        marker_re = re.compile(r"⟪IMG:(\d+)⟫")
        return marker_re.sub(replace, text)

    def _format_code_blocks(self, text: str) -> str:
        """Detect and format code blocks.

        Looks for patterns that suggest code:
        - Lines starting with common keywords (def, class, function, etc.)
        - Lines with specific syntax patterns
        - Consecutive lines with consistent indentation
        """
        lines = text.split("\n")
        formatted_lines = []
        in_code_block = False
        code_buffer = []

        code_indicators = [
            r"^\s*(def|class|function|const|let|var|import|from|public|private)\s+",
            r"^\s*[\w]+\s*[({]\s*$",  # Function calls, object literals
            r"^\s*return\s+",
            r"^\s*if\s*\(",
            r"^\s*for\s*\(",
            r"^\s*while\s*\(",
            r".*[{};]\s*$",  # Lines ending with braces or semicolons
        ]

        code_pattern = re.compile("|".join(code_indicators))

        for line in lines:
            looks_like_code = bool(code_pattern.match(line))

            if looks_like_code and not in_code_block:
                # Start code block
                in_code_block = True
                code_buffer = [line]
            elif in_code_block:
                # Check if still in code
                if looks_like_code or (line.startswith("    ") and line.strip()):
                    code_buffer.append(line)
                else:
                    # End code block
                    if len(code_buffer) >= 2:  # Only format if multiple lines
                        formatted_lines.append("```")
                        formatted_lines.extend(code_buffer)
                        formatted_lines.append("```")
                    else:
                        formatted_lines.extend(code_buffer)

                    in_code_block = False
                    code_buffer = []
                    formatted_lines.append(line)
            else:
                formatted_lines.append(line)

        # Handle any remaining code buffer
        if code_buffer:
            if len(code_buffer) >= 2:
                formatted_lines.append("```")
                formatted_lines.extend(code_buffer)
                formatted_lines.append("```")
            else:
                formatted_lines.extend(code_buffer)

        return "\n".join(formatted_lines)

    def convert_text(self, text: str) -> str:
        """Convert arbitrary text to Markdown (without chapter context).

        Useful for converting index or other non-chapter content.
        """
        text = self._remove_headers_footers(text)
        text = self._normalize_whitespace(text)
        text = self._detect_and_format_lists(text)
        return text
