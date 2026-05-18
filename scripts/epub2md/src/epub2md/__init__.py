"""EPUB2MD - Convert EPUB books to structured Markdown for Claude Code subagents."""

__version__ = "0.1.0"

from .extractor import EPUBExtractor
from .converter import HTMLToMarkdownConverter
from .toc_generator import TOCGenerator
from .index_generator import IndexGenerator
from .abstract_writer import AbstractWriter
from .summarizer import ChapterSummarizer

__all__ = [
    "EPUBExtractor",
    "HTMLToMarkdownConverter",
    "TOCGenerator",
    "IndexGenerator",
    "AbstractWriter",
    "ChapterSummarizer",
]
