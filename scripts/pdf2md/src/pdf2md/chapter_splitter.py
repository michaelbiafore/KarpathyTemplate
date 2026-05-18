"""Chapter boundary detection and content splitting."""

import re
from dataclasses import dataclass, field
from typing import Optional

from .extractor import PDFExtractor, TOCEntry


@dataclass
class Chapter:
    """Represents a chapter with its content and metadata."""
    number: int
    title: str
    level: int  # TOC level (1 = chapter, 2 = section, etc.)
    start_page: int  # 0-indexed
    end_page: int  # 0-indexed, inclusive
    raw_text: str = ""
    parent_title: Optional[str] = None  # For sub-chapters, the parent chapter title


@dataclass
class BookStructure:
    """Complete structure of the book."""
    title: str
    chapters: list[Chapter] = field(default_factory=list)
    front_matter: Optional[Chapter] = None  # Preface, Introduction, etc.
    back_matter: list[Chapter] = field(default_factory=list)  # Appendices, Index
    index_start_page: int = -1
    index_end_page: int = -1


class ChapterSplitter:
    """Split PDF into chapters based on TOC structure."""

    # Patterns for identifying special sections
    FRONT_MATTER_PATTERNS = [
        r"^preface",
        r"^foreword",
        r"^introduction",
        r"^acknowledgment",
        r"^about\s+the\s+author",
    ]

    BACK_MATTER_PATTERNS = [
        r"^appendix",
        r"^index$",
        r"^glossary",
        r"^bibliography",
        r"^references",
    ]

    PART_PATTERN = r"^part\s+[IVX\d]+"

    def __init__(self, extractor: PDFExtractor, image_extractor=None):
        self.extractor = extractor
        self.image_extractor = image_extractor
        self._toc: Optional[list[TOCEntry]] = None

    @property
    def toc(self) -> list[TOCEntry]:
        """Get cached TOC entries."""
        if self._toc is None:
            self._toc = self.extractor.get_toc()
        return self._toc

    def _is_front_matter(self, title: str) -> bool:
        """Check if title matches front matter patterns."""
        title_lower = title.lower().strip()
        for pattern in self.FRONT_MATTER_PATTERNS:
            if re.match(pattern, title_lower):
                return True
        return False

    def _is_back_matter(self, title: str) -> bool:
        """Check if title matches back matter patterns."""
        title_lower = title.lower().strip()
        for pattern in self.BACK_MATTER_PATTERNS:
            if re.match(pattern, title_lower):
                return True
        return False

    def _is_part_header(self, title: str) -> bool:
        """Check if title is a Part header (Part I, Part II, etc.)."""
        return bool(re.match(self.PART_PATTERN, title.lower().strip(), re.IGNORECASE))

    def _sanitize_filename(self, title: str, max_length: int = 60) -> str:
        """Convert chapter title to filesystem-safe name.

        Args:
            title: Original chapter title
            max_length: Maximum filename length

        Returns:
            Sanitized filename (without extension)
        """
        # Remove chapter number prefix if present (e.g., "Chapter 1: " or "1. ")
        title = re.sub(r"^(chapter\s+)?\d+[\.:]\s*", "", title, flags=re.IGNORECASE)

        # Replace special characters with underscores
        sanitized = re.sub(r"[^\w\s-]", "", title)
        sanitized = re.sub(r"[\s]+", "_", sanitized)

        # Remove leading/trailing underscores
        sanitized = sanitized.strip("_")

        # Truncate if too long
        if len(sanitized) > max_length:
            sanitized = sanitized[:max_length].rstrip("_")

        return sanitized

    def split(self) -> BookStructure:
        """Split the PDF into chapters based on TOC.

        Returns:
            BookStructure with all chapters and metadata
        """
        toc = self.toc
        total_pages = self.extractor.page_count

        if not toc:
            # No TOC found - treat entire document as single chapter
            return self._create_single_chapter_structure(total_pages)

        structure = BookStructure(title=self._extract_book_title())

        # Find index section
        index_start, index_end = self.extractor.find_index_pages()
        structure.index_start_page = index_start
        structure.index_end_page = index_end

        # Process TOC entries
        chapter_num = 0
        current_part = None

        for i, entry in enumerate(toc):
            # Determine end page
            if i + 1 < len(toc):
                # End at next entry's start page - 1
                end_page = toc[i + 1].page_num - 2  # -2 because page_num is 1-indexed
            else:
                # Last entry - end at index start or document end
                if index_start > 0:
                    end_page = index_start - 1
                else:
                    end_page = total_pages - 1

            start_page = entry.page_num - 1  # Convert to 0-indexed

            # Ensure valid page range
            start_page = max(0, start_page)
            end_page = max(start_page, min(end_page, total_pages - 1))

            # Track Part headers
            if self._is_part_header(entry.title):
                current_part = entry.title
                continue  # Don't create separate file for Part headers

            # Create chapter object
            chapter = Chapter(
                number=chapter_num,
                title=entry.title,
                level=entry.level,
                start_page=start_page,
                end_page=end_page,
                parent_title=current_part if entry.level > 1 else None,
            )

            # Extract text content (with image markers if we have an image extractor)
            if self.image_extractor is not None:
                chapter.raw_text = self.extractor.get_text_range_with_images(
                    start_page, end_page, self.image_extractor
                )
            else:
                chapter.raw_text = self.extractor.get_text_range(
                    start_page, end_page
                )

            # Categorize chapter
            if self._is_front_matter(entry.title):
                structure.front_matter = chapter
            elif self._is_back_matter(entry.title):
                structure.back_matter.append(chapter)
            else:
                chapter_num += 1
                chapter.number = chapter_num
                structure.chapters.append(chapter)

        return structure

    def _create_single_chapter_structure(self, total_pages: int) -> BookStructure:
        """Create structure when no TOC is available."""
        structure = BookStructure(title="Untitled")

        chapter = Chapter(
            number=1,
            title="Full Document",
            level=1,
            start_page=0,
            end_page=total_pages - 1,
        )
        if self.image_extractor is not None:
            chapter.raw_text = self.extractor.get_text_range_with_images(
                0, total_pages - 1, self.image_extractor
            )
        else:
            chapter.raw_text = self.extractor.get_text_range(0, total_pages - 1)
        structure.chapters.append(chapter)

        return structure

    def _extract_book_title(self) -> str:
        """Try to extract book title from PDF metadata or first page."""
        metadata = self.extractor.get_metadata()
        if metadata.get("title"):
            return metadata["title"]

        # Fallback: Try to get title from first page
        first_page_text = self.extractor.get_page_text(0)
        lines = [line.strip() for line in first_page_text.split("\n") if line.strip()]
        if lines:
            return lines[0][:100]  # First non-empty line, truncated

        return "Untitled"

    def get_chapter_filename(self, chapter: Chapter) -> str:
        """Generate filename for a chapter.

        Format: XX_Title_Sanitized.md
        """
        sanitized = self._sanitize_filename(chapter.title)
        return f"{chapter.number:02d}_{sanitized}.md"
