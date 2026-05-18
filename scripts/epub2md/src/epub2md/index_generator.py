"""Index extraction and generation from EPUB."""

import re
import warnings
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path

from bs4 import BeautifulSoup, Tag, XMLParsedAsHTMLWarning

# Suppress XML parsing warning - EPUB content is XHTML but we parse as HTML
warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)

from .converter import ConvertedChapter


@dataclass
class IndexEntry:
    """Represents an index entry."""
    term: str
    references: list[str] = field(default_factory=list)
    subentries: list["IndexEntry"] = field(default_factory=list)


class IndexGenerator:
    """Extract and generate index from EPUB content."""

    def __init__(self):
        self.entries: dict[str, IndexEntry] = {}

    def parse_index_html(self, html_content: bytes) -> list[IndexEntry]:
        """Parse index from EPUB HTML content."""
        soup = BeautifulSoup(html_content, "lxml")
        entries = []

        # Look for index lists (ul, ol, dl)
        index_lists = soup.find_all(["ul", "ol", "dl"])

        for lst in index_lists:
            entries.extend(self._parse_list(lst))

        # If no lists found, try to parse as plain text
        if not entries:
            entries = self._parse_text_index(soup)

        return entries

    def _parse_list(self, lst: Tag) -> list[IndexEntry]:
        """Parse index entries from a list element."""
        entries = []

        if lst.name == "dl":
            # Definition list: dt = term, dd = references
            current_term = None
            for child in lst.children:
                if not hasattr(child, "name"):
                    continue
                if child.name == "dt":
                    current_term = child.get_text(strip=True)
                elif child.name == "dd" and current_term:
                    refs = self._extract_references(child)
                    entries.append(IndexEntry(term=current_term, references=refs))
                    current_term = None
        else:
            # Unordered/ordered list
            for li in lst.find_all("li", recursive=False):
                entry = self._parse_list_item(li)
                if entry:
                    entries.append(entry)

        return entries

    def _parse_list_item(self, li: Tag) -> IndexEntry | None:
        """Parse a single list item as an index entry."""
        # Get direct text content (term)
        term = ""
        refs = []

        # Extract text before any nested list
        for content in li.children:
            if hasattr(content, "name"):
                if content.name in ["ul", "ol"]:
                    break
                elif content.name == "a":
                    # This is a reference link
                    refs.append(content.get("href", ""))
                else:
                    term += content.get_text(strip=True)
            else:
                term += str(content).strip()

        term = term.strip().rstrip(",").rstrip(":")
        if not term:
            return None

        # Extract references from links
        for link in li.find_all("a", recursive=False):
            href = link.get("href", "")
            if href:
                refs.append(href)

        # Check for subentries (nested list)
        subentries = []
        nested_list = li.find(["ul", "ol"])
        if nested_list:
            subentries = self._parse_list(nested_list)

        return IndexEntry(term=term, references=refs, subentries=subentries)

    def _extract_references(self, element: Tag) -> list[str]:
        """Extract reference links from an element."""
        refs = []
        for link in element.find_all("a"):
            href = link.get("href", "")
            if href:
                refs.append(href)
        return refs

    def _parse_text_index(self, soup: Tag) -> list[IndexEntry]:
        """Parse index from plain text format."""
        entries = []
        text = soup.get_text()

        # Look for patterns like "Term, 123, 456" or "Term: see other"
        lines = text.split("\n")
        current_letter = ""

        for line in lines:
            line = line.strip()
            if not line:
                continue

            # Skip letter headings
            if len(line) == 1 and line.isupper():
                current_letter = line
                continue

            # Try to parse as "term, refs"
            match = re.match(r"^([^,]+),\s*(.+)$", line)
            if match:
                term = match.group(1).strip()
                refs_text = match.group(2).strip()
                # References could be page numbers or "see X"
                refs = [r.strip() for r in refs_text.split(",")]
                entries.append(IndexEntry(term=term, references=refs))

        return entries

    def generate(
        self,
        entries: list[IndexEntry],
        chapters: list[ConvertedChapter] | None = None,
    ) -> str:
        """Generate Index markdown from entries."""
        if not entries:
            return "# Index\n\nNo index available for this book.\n"

        # Build href to filename map if chapters provided
        href_map = {}
        if chapters:
            for chapter in chapters:
                base_href = chapter.source_href.split("#")[0]
                href_map[base_href] = chapter.filename
                href_map[Path(base_href).name] = chapter.filename

        # Group entries by first letter
        by_letter: dict[str, list[IndexEntry]] = defaultdict(list)
        for entry in entries:
            first = entry.term[0].upper() if entry.term else "#"
            if not first.isalpha():
                first = "#"
            by_letter[first].append(entry)

        lines = ["# Index", ""]

        # Generate entries by letter
        for letter in sorted(by_letter.keys()):
            lines.append(f"## {letter}")
            lines.append("")

            for entry in sorted(by_letter[letter], key=lambda e: e.term.lower()):
                lines.append(self._format_entry(entry, href_map, indent=0))

                for subentry in entry.subentries:
                    lines.append(self._format_entry(subentry, href_map, indent=1))

            lines.append("")

        return "\n".join(lines)

    def _format_entry(
        self,
        entry: IndexEntry,
        href_map: dict[str, str],
        indent: int,
    ) -> str:
        """Format a single index entry."""
        prefix = "  " * indent + "- "
        term = f"**{entry.term}**"

        if not entry.references:
            return f"{prefix}{term}"

        # Format references
        ref_parts = []
        for ref in entry.references:
            if ref.startswith("see ") or ref.isdigit():
                ref_parts.append(ref)
            else:
                # Try to resolve to chapter filename
                base_ref = ref.split("#")[0]
                filename = href_map.get(base_ref) or href_map.get(Path(base_ref).name)
                if filename:
                    ref_parts.append(f"[link](./{filename})")
                else:
                    ref_parts.append(ref)

        refs_str = ", ".join(ref_parts)
        return f"{prefix}{term}: {refs_str}"

    def write(
        self,
        index_content: bytes | None,
        chapters: list[ConvertedChapter],
        output_dir: Path,
    ) -> Path | None:
        """Parse index and write to file."""
        if index_content is None:
            return None

        entries = self.parse_index_html(index_content)
        if not entries:
            return None

        content = self.generate(entries, chapters)
        output_path = output_dir / "Index.md"
        output_path.write_text(content, encoding="utf-8")
        return output_path
