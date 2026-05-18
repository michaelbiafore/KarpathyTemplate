"""Generate chapter abstracts/summaries."""

import re
from pathlib import Path
from typing import Optional

from .chapter_splitter import BookStructure, Chapter


class AbstractWriter:
    """Generate chapter summaries/abstracts."""

    # Target length for abstracts (in lines)
    MIN_LINES = 3
    MAX_LINES = 12

    def __init__(self, structure: BookStructure):
        self.structure = structure

    def generate_abstract(self, chapter: Chapter) -> str:
        """Generate a summary abstract for a single chapter.

        Strategy:
        1. Extract first 2-3 paragraphs
        2. Identify section headings within chapter
        3. Build summary from key content

        Args:
            chapter: Chapter to summarize

        Returns:
            Abstract text (3-12 lines)
        """
        text = re.sub(r"⟪IMG:\d+⟫", "", chapter.raw_text)

        # Split into paragraphs
        paragraphs = self._split_paragraphs(text)

        if not paragraphs:
            return "*No content available for this chapter.*"

        abstract_parts = []

        # Add opening summary from first substantial paragraph
        first_para = self._get_first_substantial_paragraph(paragraphs)
        if first_para:
            # Truncate if too long
            sentences = self._split_sentences(first_para)
            abstract_parts.append(" ".join(sentences[:3]))

        # Extract section headings to identify key topics
        headings = self._extract_headings(text)
        if headings:
            topics = ", ".join(headings[:5])  # Limit to 5 topics
            abstract_parts.append(f"**Key topics:** {topics}")

        # Try to identify key concepts mentioned multiple times
        key_concepts = self._extract_key_concepts(text)
        if key_concepts:
            concepts = ", ".join(key_concepts[:6])
            abstract_parts.append(f"**Key concepts:** {concepts}")

        # Combine and ensure within line limits
        abstract = "\n\n".join(abstract_parts)

        # Ensure we meet minimum length
        if len(abstract.split("\n")) < self.MIN_LINES:
            # Add more content from opening paragraphs
            for para in paragraphs[1:4]:
                if para and len(para) > 50:
                    sentences = self._split_sentences(para)
                    abstract += "\n\n" + sentences[0]
                    if len(abstract.split("\n")) >= self.MIN_LINES:
                        break

        # Ensure we don't exceed maximum length
        lines = abstract.split("\n")
        if len(lines) > self.MAX_LINES:
            abstract = "\n".join(lines[:self.MAX_LINES])

        return abstract

    def _split_paragraphs(self, text: str) -> list[str]:
        """Split text into paragraphs."""
        # Split on double newlines
        paragraphs = re.split(r"\n\s*\n", text)
        # Filter empty and very short paragraphs
        return [p.strip() for p in paragraphs if p.strip() and len(p.strip()) > 20]

    def _get_first_substantial_paragraph(self, paragraphs: list[str]) -> Optional[str]:
        """Get first paragraph with substantial content."""
        for para in paragraphs:
            # Skip very short or header-like paragraphs
            if len(para) > 100 and not para.isupper():
                return para
        return paragraphs[0] if paragraphs else None

    def _split_sentences(self, text: str) -> list[str]:
        """Split text into sentences."""
        # Simple sentence splitting on . ! ?
        sentences = re.split(r"(?<=[.!?])\s+", text)
        return [s.strip() for s in sentences if s.strip()]

    def _extract_headings(self, text: str) -> list[str]:
        """Extract section headings from chapter text.

        Looks for patterns that indicate headings:
        - Lines that are all caps
        - Lines followed by all-cap markers
        - Short lines with title case
        """
        headings = []
        lines = text.split("\n")

        for i, line in enumerate(lines):
            line = line.strip()

            if not line or len(line) < 3:
                continue

            # Skip very long lines (not headings)
            if len(line) > 80:
                continue

            # Check for all-caps (section headers)
            if line.isupper() and len(line) > 5:
                headings.append(line.title())
                continue

            # Check for title case short lines (potential subheadings)
            words = line.split()
            if len(words) <= 8 and line[0].isupper():
                # Check if followed by paragraph (indicates heading)
                if i + 1 < len(lines):
                    next_line = lines[i + 1].strip()
                    if next_line and len(next_line) > 50:
                        # Looks like a heading
                        headings.append(line)

        return headings[:10]  # Limit results

    def _extract_key_concepts(self, text: str) -> list[str]:
        """Extract frequently mentioned technical terms.

        Looks for capitalized multi-word terms that appear multiple times.
        """
        # Find capitalized terms (potential concepts)
        pattern = r"\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\b"
        matches = re.findall(pattern, text)

        # Count frequencies
        freq = {}
        for match in matches:
            if len(match) > 3:  # Skip short words
                freq[match] = freq.get(match, 0) + 1

        # Filter to terms appearing multiple times
        concepts = [term for term, count in freq.items() if count >= 3]

        # Sort by frequency
        concepts.sort(key=lambda t: freq[t], reverse=True)

        return concepts[:10]

    def generate_all(self) -> str:
        """Generate abstracts for all chapters.

        Returns:
            Complete ChapterAbstracts.md content
        """
        lines = [
            "# Chapter Abstracts",
            "",
            f"*Summaries of chapters from \"{self.structure.title}\"*",
            "",
        ]

        # Front matter
        if self.structure.front_matter:
            lines.append(f"## {self.structure.front_matter.title}")
            lines.append("")
            lines.append(self.generate_abstract(self.structure.front_matter))
            lines.append("")
            lines.append("---")
            lines.append("")

        # Main chapters
        for chapter in self.structure.chapters:
            lines.append(f"## Chapter {chapter.number}: {chapter.title}")
            lines.append("")
            lines.append(self.generate_abstract(chapter))
            lines.append("")
            lines.append("---")
            lines.append("")

        # Remove trailing separator
        if lines[-2] == "---":
            lines = lines[:-2]

        return "\n".join(lines)

    def write(self, output_path: Path) -> None:
        """Write all abstracts to file.

        Args:
            output_path: Full path to output file
        """
        content = self.generate_all()
        output_path.write_text(content, encoding="utf-8")
