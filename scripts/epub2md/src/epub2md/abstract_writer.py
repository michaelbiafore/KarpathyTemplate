"""Chapter abstract/summary generation."""

import re
import warnings
from pathlib import Path

from bs4 import BeautifulSoup, XMLParsedAsHTMLWarning

# Suppress XML parsing warning - EPUB content is XHTML but we parse as HTML
warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)

from .converter import ConvertedChapter


class AbstractWriter:
    """Generate chapter abstracts from EPUB content."""

    def __init__(self, min_lines: int = 3, max_lines: int = 12):
        self.min_lines = min_lines
        self.max_lines = max_lines

    def generate_abstract(self, html_content: bytes, title: str) -> str:
        """Generate abstract for a single chapter."""
        soup = BeautifulSoup(html_content, "lxml")

        # Remove script, style, and navigation elements
        for tag in soup.find_all(["script", "style", "nav", "head"]):
            tag.decompose()

        # Extract key information
        opening_paragraphs = self._extract_opening_paragraphs(soup)
        section_headings = self._extract_section_headings(soup)
        key_concepts = self._extract_key_concepts(soup)

        # Build abstract
        abstract_lines = []

        # Add opening content (first 2-3 sentences)
        if opening_paragraphs:
            abstract_lines.append(opening_paragraphs)
            abstract_lines.append("")

        # Add key topics if we have section headings
        if section_headings:
            topics = ", ".join(section_headings[:5])
            abstract_lines.append(f"**Key topics:** {topics}")

        # Add key concepts if found
        if key_concepts:
            concepts = ", ".join(key_concepts[:5])
            abstract_lines.append(f"**Key concepts:** {concepts}")

        # Ensure we have at least min_lines
        abstract = "\n".join(abstract_lines)

        # If too short, try to add more content
        if len(abstract_lines) < self.min_lines and opening_paragraphs:
            abstract = self._expand_abstract(soup, abstract)

        return abstract

    def _extract_opening_paragraphs(self, soup: BeautifulSoup) -> str:
        """Extract first meaningful paragraphs."""
        paragraphs = []
        total_sentences = 0

        for p in soup.find_all("p"):
            text = p.get_text(strip=True)
            if not text or len(text) < 20:
                continue

            # Skip navigation or header-like paragraphs
            if text.lower().startswith(("chapter", "part", "section")):
                if len(text) < 50:
                    continue

            paragraphs.append(text)
            total_sentences += text.count(".") + text.count("!") + text.count("?")

            # Stop after 3-4 sentences
            if total_sentences >= 4:
                break

            # Or after 2 substantial paragraphs
            if len(paragraphs) >= 2:
                break

        if not paragraphs:
            return ""

        # Join and limit to ~3 sentences
        combined = " ".join(paragraphs)
        sentences = re.split(r"(?<=[.!?])\s+", combined)
        return " ".join(sentences[:3])

    def _extract_section_headings(self, soup: BeautifulSoup) -> list[str]:
        """Extract section headings as key topics."""
        headings = []

        for tag in ["h2", "h3", "h4"]:
            for heading in soup.find_all(tag):
                text = heading.get_text(strip=True)
                if text and len(text) < 100:
                    # Clean up heading text
                    text = re.sub(r"^\d+[\.\)]\s*", "", text)  # Remove numbering
                    if text and text not in headings:
                        headings.append(text)

        return headings

    def _extract_key_concepts(self, soup: BeautifulSoup) -> list[str]:
        """Extract key concepts from emphasized text."""
        concepts = set()

        # Look for emphasized text
        for tag in ["strong", "b", "em", "i"]:
            for el in soup.find_all(tag):
                text = el.get_text(strip=True)
                # Filter to likely concept names (capitalized, reasonable length)
                if text and 3 < len(text) < 50:
                    if text[0].isupper() or "_" in text:
                        # Clean up
                        text = text.strip(".,;:()[]")
                        if text:
                            concepts.add(text)

        # Also look for terms in code tags (technical concepts)
        for code in soup.find_all("code"):
            text = code.get_text(strip=True)
            if text and 2 < len(text) < 30:
                concepts.add(text)

        return sorted(concepts)[:10]

    def _expand_abstract(self, soup: BeautifulSoup, current: str) -> str:
        """Expand abstract if too short."""
        # Try to find aside or callout content
        for aside in soup.find_all(["aside", "blockquote"]):
            text = aside.get_text(strip=True)
            if text and len(text) > 50:
                # Add first sentence of aside
                sentences = re.split(r"(?<=[.!?])\s+", text)
                if sentences:
                    current += f"\n\n*Note:* {sentences[0]}"
                    break

        return current

    def generate_all(
        self,
        chapters: list[ConvertedChapter],
        html_contents: dict[str, bytes],
    ) -> str:
        """Generate abstracts for all chapters."""
        lines = [
            "# Chapter Abstracts",
            "",
            "Auto-generated summaries for each chapter.",
            "",
            "---",
            "",
        ]

        for chapter in chapters:
            # Skip very short chapters (likely front/back matter)
            content = html_contents.get(chapter.source_href, b"")
            if len(content) < 500:
                continue

            abstract = self.generate_abstract(content, chapter.title)

            if abstract:
                lines.append(f"## {chapter.title}")
                lines.append("")
                lines.append(f"*File: [{chapter.filename}](./{chapter.filename})*")
                lines.append("")
                lines.append(abstract)
                lines.append("")
                lines.append("---")
                lines.append("")

        return "\n".join(lines)

    def write(
        self,
        chapters: list[ConvertedChapter],
        html_contents: dict[str, bytes],
        output_dir: Path,
    ) -> Path:
        """Generate and write chapter abstracts to file."""
        content = self.generate_all(chapters, html_contents)
        output_path = output_dir / "ChapterAbstracts.md"
        output_path.write_text(content, encoding="utf-8")
        return output_path
