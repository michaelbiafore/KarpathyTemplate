"""Command-line interface for PDF to Markdown conversion."""

import argparse
import sys
from pathlib import Path

from .extractor import PDFExtractor
from .chapter_splitter import ChapterSplitter
from .converter import MarkdownConverter
from .toc_generator import TOCGenerator
from .index_generator import IndexGenerator
from .abstract_writer import AbstractWriter
from .image_extractor import ImageExtractor


def main():
    """Main entry point for CLI."""
    parser = argparse.ArgumentParser(
        description="Convert PDF books to structured Markdown chapters",
        prog="pdf2md"
    )

    parser.add_argument(
        "pdf_path",
        type=str,
        help="Path to input PDF file"
    )

    parser.add_argument(
        "-o", "--output",
        type=str,
        default="md_out",
        help="Output directory (default: md_out)"
    )

    parser.add_argument(
        "--no-abstracts",
        action="store_true",
        help="Skip generating chapter abstracts"
    )

    parser.add_argument(
        "--no-index",
        action="store_true",
        help="Skip generating index file"
    )

    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Show detailed progress"
    )

    parser.add_argument(
        "--extract-images",
        dest="extract_images",
        action="store_true",
        default=True,
        help="Extract embedded images to <output>/images/ (default: on)"
    )

    parser.add_argument(
        "--no-extract-images",
        dest="extract_images",
        action="store_false",
        help="Disable image extraction"
    )

    parser.add_argument(
        "--min-image-size",
        type=int,
        default=80,
        help="Skip images smaller than NxN pixels (default: 80)"
    )

    parser.add_argument(
        "--image-recurrence-threshold",
        type=float,
        default=0.30,
        help="Skip images that appear on more than this fraction of pages "
             "(default: 0.30, i.e. 30%%)"
    )

    args = parser.parse_args()

    # Validate input
    pdf_path = Path(args.pdf_path)
    if not pdf_path.exists():
        print(f"Error: PDF file not found: {pdf_path}", file=sys.stderr)
        sys.exit(1)

    output_dir = Path(args.output)

    # Run conversion
    try:
        convert_pdf(
            pdf_path=pdf_path,
            output_dir=output_dir,
            generate_abstracts=not args.no_abstracts,
            generate_index=not args.no_index,
            verbose=args.verbose,
            extract_images=args.extract_images,
            min_image_size=args.min_image_size,
            image_recurrence_threshold=args.image_recurrence_threshold,
        )
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def convert_pdf(
    pdf_path: Path,
    output_dir: Path,
    generate_abstracts: bool = True,
    generate_index: bool = True,
    verbose: bool = False,
    extract_images: bool = True,
    min_image_size: int = 80,
    image_recurrence_threshold: float = 0.30,
) -> None:
    """Convert PDF to Markdown files.

    Args:
        pdf_path: Path to input PDF
        output_dir: Directory for output files
        generate_abstracts: Whether to create ChapterAbstracts.md
        generate_index: Whether to create Index.md
        verbose: Show progress details
    """
    def log(msg: str):
        if verbose:
            print(msg)

    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)
    log(f"Output directory: {output_dir}")

    # Open PDF and extract structure
    log(f"Opening PDF: {pdf_path}")

    with PDFExtractor(pdf_path) as extractor:
        log(f"PDF has {extractor.page_count} pages")

        # Extract images first — they're referenced when text is extracted with markers
        image_extractor = None
        if extract_images:
            log("Extracting embedded images...")
            image_extractor = ImageExtractor(
                doc=extractor.doc,
                out_dir=output_dir,
                min_width=min_image_size,
                min_height=min_image_size,
                recurrence_threshold=image_recurrence_threshold,
                verbose=verbose,
            )
            images = image_extractor.extract_all()
            log(f"Saved {len(images)} images to {output_dir / 'images'}")

        # Get TOC and split into chapters
        log("Analyzing document structure...")
        splitter = ChapterSplitter(extractor, image_extractor=image_extractor)
        structure = splitter.split()

        log(f"Found {len(structure.chapters)} chapters")

        # Create converter (image-aware if we extracted images)
        converter = MarkdownConverter(image_extractor=image_extractor)

        # Write individual chapter files
        log("Converting chapters to Markdown...")
        for chapter in structure.chapters:
            filename = splitter.get_chapter_filename(chapter)
            filepath = output_dir / filename

            content = converter.convert(chapter)
            filepath.write_text(content, encoding="utf-8")
            log(f"  Written: {filename}")

        # Write front matter if present
        if structure.front_matter:
            filename = f"00_{splitter._sanitize_filename(structure.front_matter.title)}.md"
            filepath = output_dir / filename
            content = converter.convert(structure.front_matter)
            filepath.write_text(content, encoding="utf-8")
            log(f"  Written: {filename}")

        # Generate Table of Contents
        log("Generating Table of Contents...")
        toc_gen = TOCGenerator(structure, splitter)
        toc_path = output_dir / "Table_of_Contents.md"
        toc_gen.write(toc_path)
        log(f"  Written: Table_of_Contents.md")

        # Generate Index if requested and found
        if generate_index and structure.index_start_page >= 0:
            log("Generating Index...")
            index_gen = IndexGenerator(pdf_path, extractor)
            index_path = output_dir / "Index.md"
            index_gen.write(
                index_path,
                structure.index_start_page,
                structure.index_end_page
            )
            log(f"  Written: Index.md")
        elif generate_index:
            log("No index section found in PDF")

        # Generate Chapter Abstracts if requested
        if generate_abstracts:
            log("Generating Chapter Abstracts...")
            abstract_writer = AbstractWriter(structure)
            abstracts_path = output_dir / "ChapterAbstracts.md"
            abstract_writer.write(abstracts_path)
            log(f"  Written: ChapterAbstracts.md")

    print(f"Conversion complete! Output written to: {output_dir}")
    print(f"  - {len(structure.chapters)} chapter files")
    print(f"  - Table_of_Contents.md")
    if generate_index and structure.index_start_page >= 0:
        print(f"  - Index.md")
    if generate_abstracts:
        print(f"  - ChapterAbstracts.md")


if __name__ == "__main__":
    main()
