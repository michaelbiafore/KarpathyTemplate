"""Extract and generate Index from PDF."""

import re
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional

import pdfplumber

from .extractor import PDFExtractor


@dataclass
class IndexEntry:
    """Represents a single index entry."""
    term: str
    page_refs: list[str] = field(default_factory=list)  # Can include ranges like "45-67"
    sub_entries: list["IndexEntry"] = field(default_factory=list)


class IndexGenerator:
    """Extract and format book index."""

    def __init__(self, pdf_path: str | Path, extractor: PDFExtractor):
        self.pdf_path = Path(pdf_path)
        self.extractor = extractor
        self._entries: Optional[list[IndexEntry]] = None

    def extract(self, start_page: int, end_page: int) -> list[IndexEntry]:
        """Extract index entries from specified page range.

        Uses pdfplumber for better multi-column detection.

        Args:
            start_page: Starting page (0-indexed)
            end_page: Ending page (0-indexed, inclusive)

        Returns:
            List of IndexEntry objects
        """
        entries = []
        current_letter = None
        current_entry = None

        with pdfplumber.open(self.pdf_path) as pdf:
            for page_num in range(start_page, min(end_page + 1, len(pdf.pages))):
                page = pdf.pages[page_num]
                text = page.extract_text() or ""

                # Process lines
                for line in text.split("\n"):
                    line = line.strip()
                    if not line:
                        continue

                    # Skip page numbers and headers
                    if self._is_header_footer(line):
                        continue

                    # Check for letter section header (A, B, C, etc.)
                    if self._is_letter_header(line):
                        current_letter = line[0].upper()
                        continue

                    # Parse index entry
                    entry = self._parse_entry(line)
                    if entry:
                        # Check if sub-entry (indented)
                        if line.startswith("  ") or line.startswith("\t"):
                            if current_entry:
                                current_entry.sub_entries.append(entry)
                        else:
                            current_entry = entry
                            entries.append(entry)

        self._entries = entries
        return entries

    def _is_header_footer(self, line: str) -> bool:
        """Check if line is a page header/footer."""
        # Check for standalone numbers (page numbers)
        if re.match(r"^\d+$", line):
            return True
        # Check for "Index" header
        if line.lower() == "index":
            return True
        # Check for page number patterns
        if re.match(r"^(Index\s*)?\|\s*\d+$", line, re.IGNORECASE):
            return True
        return False

    def _is_letter_header(self, line: str) -> bool:
        """Check if line is a single letter section header."""
        return len(line) == 1 and line.isalpha()

    def _parse_entry(self, line: str) -> Optional[IndexEntry]:
        """Parse a single index entry line.

        Expected formats:
        - "term, 45, 67, 89"
        - "term, 45-67"
        - "term (see also other term), 45"
        """
        # Remove leading whitespace for sub-entries but track it
        line = line.strip()

        if not line:
            return None

        # Try to split on last comma before page numbers
        # Pattern: term followed by page numbers
        match = re.match(r"^(.+?),?\s*([\d,\s\-–]+)$", line)

        if match:
            term = match.group(1).strip().rstrip(",")
            pages_str = match.group(2)

            # Parse page references
            page_refs = []
            for part in re.split(r"[,\s]+", pages_str):
                part = part.strip()
                if part and (part.isdigit() or re.match(r"^\d+[-–]\d+$", part)):
                    # Normalize dash
                    part = part.replace("–", "-")
                    page_refs.append(part)

            if term:
                return IndexEntry(term=term, page_refs=page_refs)

        # Entry without page numbers (cross-reference)
        if line and not re.match(r"^[\d,\s\-–]+$", line):
            return IndexEntry(term=line, page_refs=[])

        return None

    def generate(self) -> str:
        """Generate Index Markdown from extracted entries.

        Returns:
            Formatted Markdown index
        """
        if not self._entries:
            return "# Index\n\n*No index entries found.*"

        lines = ["# Index", ""]

        current_letter = None

        for entry in self._entries:
            # Get first letter for grouping
            first_letter = entry.term[0].upper() if entry.term else ""

            if first_letter.isalpha() and first_letter != current_letter:
                current_letter = first_letter
                lines.append("")
                lines.append(f"## {current_letter}")
                lines.append("")

            # Format main entry
            lines.append(self._format_entry(entry))

            # Format sub-entries
            for sub in entry.sub_entries:
                lines.append(self._format_entry(sub, indent="  "))

        return "\n".join(lines)

    def _format_entry(self, entry: IndexEntry, indent: str = "") -> str:
        """Format a single index entry as Markdown."""
        if entry.page_refs:
            refs = ", ".join(entry.page_refs)
            return f"{indent}- **{entry.term}**: pp. {refs}"
        else:
            return f"{indent}- **{entry.term}**"

    def write(self, output_path: Path, start_page: int, end_page: int) -> None:
        """Extract and write index to file.

        Args:
            output_path: Full path to output file
            start_page: Index start page (0-indexed)
            end_page: Index end page (0-indexed, inclusive)
        """
        self.extract(start_page, end_page)
        content = self.generate()
        output_path.write_text(content, encoding="utf-8")
