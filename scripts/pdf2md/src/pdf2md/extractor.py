"""PDF text and structure extraction using PyMuPDF."""

import fitz
from pathlib import Path
from dataclasses import dataclass
from typing import Optional


@dataclass
class TOCEntry:
    """Represents a table of contents entry."""
    level: int
    title: str
    page_num: int


@dataclass
class PageContent:
    """Represents extracted content from a single page."""
    page_num: int
    text: str
    blocks: list  # Raw block data for advanced processing


class PDFExtractor:
    """Extract text and structure from PDF files."""

    def __init__(self, pdf_path: str | Path):
        self.pdf_path = Path(pdf_path)
        self.doc: Optional[fitz.Document] = None

    def open(self) -> None:
        """Open the PDF document."""
        if not self.pdf_path.exists():
            raise FileNotFoundError(f"PDF not found: {self.pdf_path}")
        self.doc = fitz.open(self.pdf_path)

    def close(self) -> None:
        """Close the PDF document."""
        if self.doc:
            self.doc.close()
            self.doc = None

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    @property
    def page_count(self) -> int:
        """Return total number of pages."""
        if not self.doc:
            raise RuntimeError("PDF not opened. Call open() first.")
        return len(self.doc)

    def get_toc(self) -> list[TOCEntry]:
        """Extract table of contents from PDF.

        Returns list of TOCEntry objects with level, title, and page number.
        """
        if not self.doc:
            raise RuntimeError("PDF not opened. Call open() first.")

        raw_toc = self.doc.get_toc()
        entries = []

        for item in raw_toc:
            level, title, page = item[0], item[1], item[2]
            # Clean up title - remove extra whitespace
            title = " ".join(title.split())
            entries.append(TOCEntry(level=level, title=title, page_num=page))

        return entries

    def get_page_text(self, page_num: int) -> str:
        """Extract text from a single page (0-indexed).

        Args:
            page_num: Zero-indexed page number

        Returns:
            Extracted text content
        """
        if not self.doc:
            raise RuntimeError("PDF not opened. Call open() first.")

        if page_num < 0 or page_num >= len(self.doc):
            raise ValueError(f"Page {page_num} out of range (0-{len(self.doc)-1})")

        page = self.doc[page_num]
        return page.get_text()

    def get_page_content(self, page_num: int) -> PageContent:
        """Extract detailed content from a single page.

        Includes raw block data for advanced analysis (font sizes, positions).
        """
        if not self.doc:
            raise RuntimeError("PDF not opened. Call open() first.")

        page = self.doc[page_num]
        text = page.get_text()
        blocks = page.get_text("dict")["blocks"]

        return PageContent(page_num=page_num, text=text, blocks=blocks)

    def get_text_range(self, start_page: int, end_page: int) -> str:
        """Extract text from a range of pages (inclusive).

        Args:
            start_page: Starting page (0-indexed)
            end_page: Ending page (0-indexed, inclusive)

        Returns:
            Combined text from all pages in range
        """
        if not self.doc:
            raise RuntimeError("PDF not opened. Call open() first.")

        texts = []
        for page_num in range(start_page, min(end_page + 1, len(self.doc))):
            texts.append(self.get_page_text(page_num))

        return "\n\n".join(texts)

    def get_text_range_with_images(
        self,
        start_page: int,
        end_page: int,
        image_extractor,
    ) -> str:
        """Extract text from a page range with ⟪IMG:xref⟫ markers in reading order.

        Markers are inserted where image blocks appear, matched back to the
        ExtractedImage objects via (page, bbox) position.
        """
        if not self.doc:
            raise RuntimeError("PDF not opened. Call open() first.")

        page_parts = []
        for page_num in range(start_page, min(end_page + 1, len(self.doc))):
            page = self.doc[page_num]
            blocks = page.get_text("dict")["blocks"]
            blocks_sorted = sorted(
                blocks, key=lambda b: (b["bbox"][1], b["bbox"][0])
            )

            buffer = []
            for block in blocks_sorted:
                btype = block.get("type", 0)
                if btype == 0:
                    text = self._block_text_with_lines(block)
                    if text:
                        buffer.append(text)
                elif btype == 1:
                    bbox = fitz.Rect(block["bbox"])
                    img = image_extractor.image_for_page_bbox(page_num, bbox)
                    if img is not None:
                        buffer.append(f"\n\n⟪IMG:{img.xref}⟫\n\n")
            page_parts.append("\n".join(buffer))

        return "\n\n".join(page_parts)

    @staticmethod
    def _block_text_with_lines(block: dict) -> str:
        lines = []
        for line in block.get("lines", []):
            spans = [span.get("text", "") for span in line.get("spans", [])]
            lines.append("".join(spans))
        return "\n".join(lines).strip()

    def detect_headings_by_font(self, page_num: int, min_size: float = 14.0) -> list[dict]:
        """Detect potential headings by analyzing font sizes.

        Useful as fallback when TOC is missing or incomplete.

        Args:
            page_num: Page to analyze
            min_size: Minimum font size to consider as heading

        Returns:
            List of potential headings with text and font size
        """
        if not self.doc:
            raise RuntimeError("PDF not opened. Call open() first.")

        page = self.doc[page_num]
        blocks = page.get_text("dict")["blocks"]
        headings = []

        for block in blocks:
            if block.get("type") == 0:  # Text block
                for line in block.get("lines", []):
                    for span in line.get("spans", []):
                        size = span.get("size", 0)
                        text = span.get("text", "").strip()
                        if size >= min_size and text:
                            headings.append({
                                "text": text,
                                "size": size,
                                "font": span.get("font", ""),
                                "flags": span.get("flags", 0)  # Bold, italic, etc.
                            })

        return headings

    def find_index_pages(self) -> tuple[int, int]:
        """Attempt to locate index section at end of document.

        Searches last 30 pages for "Index" heading.

        Returns:
            Tuple of (start_page, end_page) for index section, or (-1, -1) if not found
        """
        if not self.doc:
            raise RuntimeError("PDF not opened. Call open() first.")

        total_pages = len(self.doc)
        search_start = max(0, total_pages - 30)

        for page_num in range(search_start, total_pages):
            text = self.get_page_text(page_num)
            # Look for standalone "Index" as section header
            lines = text.split("\n")
            for line in lines[:5]:  # Check first few lines of page
                cleaned = line.strip()
                if cleaned.lower() == "index" or cleaned.lower().startswith("index"):
                    return (page_num, total_pages - 1)

        return (-1, -1)

    def get_metadata(self) -> dict:
        """Extract PDF metadata (title, author, etc.)."""
        if not self.doc:
            raise RuntimeError("PDF not opened. Call open() first.")

        return {
            "title": self.doc.metadata.get("title", ""),
            "author": self.doc.metadata.get("author", ""),
            "subject": self.doc.metadata.get("subject", ""),
            "creator": self.doc.metadata.get("creator", ""),
            "page_count": len(self.doc),
        }
