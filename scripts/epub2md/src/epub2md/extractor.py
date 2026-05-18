"""EPUB structure and content extraction."""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterator

import ebooklib
from ebooklib import epub


@dataclass
class TOCEntry:
    """Represents a table of contents entry."""
    level: int
    title: str
    href: str
    children: list["TOCEntry"] = field(default_factory=list)


@dataclass
class ChapterContent:
    """Represents extracted chapter content."""
    title: str
    href: str
    content: bytes
    order: int


class EPUBExtractor:
    """Extract structure and content from EPUB files."""

    def __init__(self, epub_path: str | Path):
        self.epub_path = Path(epub_path)
        self.book = epub.read_epub(str(self.epub_path))
        self._spine_items: list[epub.EpubItem] | None = None

    # Titles that look like unfilled placeholders in EPUB metadata
    _PLACEHOLDER_TITLES = {"book title", "untitled", "title", "unknown title", "book"}

    @property
    def title(self) -> str:
        """Get book title, falling back if metadata looks like a placeholder."""
        metadata = self.book.get_metadata("DC", "title")
        if metadata:
            raw = metadata[0][0]
            if raw.strip().lower() not in self._PLACEHOLDER_TITLES:
                return raw
        # Fall back to the first spine item's title
        for item in self.spine_items:
            item_title = getattr(item, "title", None) or ""
            if item_title.strip():
                return item_title.strip()
        # Fall back to the first TOC entry's title
        toc = self.book.toc
        if toc:
            first = toc[0]
            toc_title = first.title if hasattr(first, "title") else (first[0].title if isinstance(first, tuple) else "")
            if toc_title and toc_title.strip().lower() not in self._PLACEHOLDER_TITLES:
                return toc_title.strip()
        return self.epub_path.stem

    @property
    def author(self) -> str:
        """Get book author."""
        metadata = self.book.get_metadata("DC", "creator")
        if metadata:
            return metadata[0][0]
        return "Unknown"

    @property
    def spine_items(self) -> list[epub.EpubItem]:
        """Get ordered list of document items from spine."""
        if self._spine_items is None:
            self._spine_items = []
            for item_id, _ in self.book.spine:
                item = self.book.get_item_with_id(item_id)
                if item is not None:
                    self._spine_items.append(item)
        return self._spine_items

    def get_toc(self) -> list[TOCEntry]:
        """Extract table of contents as hierarchical structure."""
        return list(self._parse_toc(self.book.toc, level=0))

    def _parse_toc(
        self, toc_items: list, level: int
    ) -> Iterator[TOCEntry]:
        """Recursively parse TOC items."""
        for item in toc_items:
            if isinstance(item, epub.Link):
                yield TOCEntry(
                    level=level,
                    title=item.title or "Untitled",
                    href=item.href,
                )
            elif isinstance(item, tuple):
                # Section with children: (Section, [children])
                section, children = item
                entry = TOCEntry(
                    level=level,
                    title=section.title if hasattr(section, 'title') else "Untitled",
                    href=section.href if hasattr(section, 'href') else "",
                )
                entry.children = list(self._parse_toc(children, level + 1))
                yield entry

    def get_flat_toc(self, max_level: int | None = None) -> list[TOCEntry]:
        """Get flattened TOC list, optionally limited by depth."""
        result = []
        self._flatten_toc(self.get_toc(), result, max_level)
        return result

    def _flatten_toc(
        self,
        entries: list[TOCEntry],
        result: list[TOCEntry],
        max_level: int | None,
    ) -> None:
        """Flatten nested TOC into a list."""
        for entry in entries:
            if max_level is None or entry.level <= max_level:
                result.append(entry)
            if entry.children:
                self._flatten_toc(entry.children, result, max_level)

    def get_chapters(self) -> Iterator[ChapterContent]:
        """Iterate over all chapters in reading order."""
        for order, item in enumerate(self.spine_items):
            if item.get_type() == ebooklib.ITEM_DOCUMENT:
                # Try to find title from TOC
                title = self._find_title_for_href(item.get_name())
                yield ChapterContent(
                    title=title,
                    href=item.get_name(),
                    content=item.get_content(),
                    order=order,
                )

    def _find_title_for_href(self, href: str) -> str:
        """Find TOC title matching a given href."""
        # Normalize href (remove fragment)
        base_href = href.split("#")[0]

        def search_toc(entries: list[TOCEntry]) -> str | None:
            for entry in entries:
                entry_base = entry.href.split("#")[0] if entry.href else ""
                if entry_base == base_href or entry_base.endswith(base_href):
                    return entry.title
                if entry.children:
                    found = search_toc(entry.children)
                    if found:
                        return found
            return None

        found = search_toc(self.get_toc())
        if found:
            return found

        # Fallback to filename
        return Path(href).stem.replace("_", " ").replace("-", " ").title()

    def get_item_by_href(self, href: str) -> epub.EpubItem | None:
        """Get an item by its href."""
        # Remove fragment
        base_href = href.split("#")[0]

        for item in self.book.get_items():
            if item.get_name() == base_href or item.get_name().endswith(base_href):
                return item
        return None

    def has_index(self) -> bool:
        """Check if the EPUB has an index section."""
        for entry in self.get_flat_toc():
            if "index" in entry.title.lower():
                return True

        # Check spine items
        for item in self.spine_items:
            name = item.get_name().lower()
            if "index" in name and "index.x" not in name:
                return True

        return False

    def get_index_content(self) -> bytes | None:
        """Get the index chapter content if it exists."""
        # First try TOC
        for entry in self.get_flat_toc():
            if "index" in entry.title.lower():
                item = self.get_item_by_href(entry.href)
                if item:
                    return item.get_content()

        # Then try spine items
        for item in self.spine_items:
            name = item.get_name().lower()
            if "index" in name and "index.x" not in name:
                return item.get_content()

        return None

    def extract_images(self, output_dir: Path) -> int:
        """Extract all images from the EPUB to output_dir/images/.
        Returns the number of images extracted.
        """
        images_dir = output_dir / "images"
        images_dir.mkdir(parents=True, exist_ok=True)
        count = 0
        for item in self.book.get_items_of_type(ebooklib.ITEM_IMAGE):
            filename = Path(item.get_name()).name
            (images_dir / filename).write_bytes(item.get_content())
            count += 1
        return count
