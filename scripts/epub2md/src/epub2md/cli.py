"""Command-line interface for EPUB to Markdown conversion."""

import argparse
import sys
from pathlib import Path

from .extractor import EPUBExtractor
from .converter import HTMLToMarkdownConverter, ConvertedChapter
from .toc_generator import TOCGenerator
from .index_generator import IndexGenerator
from .abstract_writer import AbstractWriter


def main(args: list[str] | None = None) -> int:
    """Main entry point for epub2md CLI."""
    parser = argparse.ArgumentParser(
        prog="epub2md",
        description="Convert EPUB books to structured Markdown for Claude Code subagents.",
    )

    parser.add_argument(
        "input",
        type=Path,
        help="Path to input EPUB file",
    )

    parser.add_argument(
        "-o", "--output",
        type=Path,
        default=Path("md_out"),
        help="Output directory (default: md_out)",
    )

    parser.add_argument(
        "--abstracts/--no-abstracts",
        dest="abstracts",
        default=True,
        action=argparse.BooleanOptionalAction,
        help="Generate chapter abstracts (default: True)",
    )

    parser.add_argument(
        "--index/--no-index",
        dest="index",
        default=True,
        action=argparse.BooleanOptionalAction,
        help="Generate index file if available (default: True)",
    )

    parser.add_argument(
        "--max-level",
        type=int,
        default=None,
        help="Maximum TOC depth to include (default: all levels)",
    )

    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Show detailed progress",
    )

    parsed = parser.parse_args(args)

    # Validate input
    if not parsed.input.exists():
        print(f"Error: Input file not found: {parsed.input}", file=sys.stderr)
        return 1

    if not parsed.input.suffix.lower() == ".epub":
        print(f"Error: Input file must be an EPUB file: {parsed.input}", file=sys.stderr)
        return 1

    # Run conversion
    try:
        convert_epub(
            input_path=parsed.input,
            output_dir=parsed.output,
            generate_abstracts=parsed.abstracts,
            generate_index=parsed.index,
            max_level=parsed.max_level,
            verbose=parsed.verbose,
        )
        return 0
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        if parsed.verbose:
            import traceback
            traceback.print_exc()
        return 1


def convert_epub(
    input_path: Path,
    output_dir: Path,
    generate_abstracts: bool = True,
    generate_index: bool = True,
    max_level: int | None = None,
    verbose: bool = False,
) -> None:
    """Convert EPUB to Markdown files."""

    def log(msg: str) -> None:
        if verbose:
            print(msg)

    log(f"Opening EPUB: {input_path}")

    # Extract EPUB structure
    extractor = EPUBExtractor(input_path)
    log(f"Book: {extractor.title} by {extractor.author}")

    # Get TOC
    toc = extractor.get_toc()
    log(f"Found {len(extractor.get_flat_toc())} TOC entries")

    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)
    log(f"Output directory: {output_dir}")

    # Extract images
    log("Extracting images...")
    image_count = extractor.extract_images(output_dir)
    log(f"  Extracted {image_count} images to {output_dir / 'images'}")

    # Convert chapters
    converter = HTMLToMarkdownConverter(verbose=verbose)
    chapters: list[ConvertedChapter] = []
    html_contents: dict[str, bytes] = {}

    log("Converting chapters...")
    for chapter_content in extractor.get_chapters():
        log(f"  Converting: {chapter_content.title}")

        converted = converter.convert(
            html_content=chapter_content.content,
            title=chapter_content.title,
            source_href=chapter_content.href,
            order=chapter_content.order,
        )
        chapters.append(converted)
        html_contents[chapter_content.href] = chapter_content.content

        # Write chapter file
        chapter_path = output_dir / converted.filename
        chapter_path.write_text(converted.content, encoding="utf-8")

    log(f"Converted {len(chapters)} chapters")

    # Generate Table of Contents
    log("Generating Table of Contents...")
    toc_generator = TOCGenerator(extractor.title, extractor.author)
    toc_path = toc_generator.write(toc, chapters, output_dir, max_level)
    log(f"  Created: {toc_path.name}")

    # Generate Index if available and requested
    if generate_index:
        log("Checking for index...")
        if extractor.has_index():
            index_content = extractor.get_index_content()
            index_generator = IndexGenerator()
            index_path = index_generator.write(index_content, chapters, output_dir)
            if index_path:
                log(f"  Created: {index_path.name}")
            else:
                log("  No index entries found")
        else:
            log("  No index found in EPUB")

    # Generate Chapter Abstracts if requested
    if generate_abstracts:
        log("Generating chapter abstracts...")
        abstract_writer = AbstractWriter()
        abstracts_path = abstract_writer.write(chapters, html_contents, output_dir)
        log(f"  Created: {abstracts_path.name}")

    # Summary
    print(f"\nConversion complete!")
    print(f"  Chapters: {len(chapters)}")
    print(f"  Images:   {image_count}")
    print(f"  Output:   {output_dir.absolute()}")


if __name__ == "__main__":
    sys.exit(main())
