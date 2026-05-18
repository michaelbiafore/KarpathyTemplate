"""Extract embedded images from a PDF, save as PNG, and index by xref."""

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import fitz


@dataclass
class ExtractedImage:
    xref: int
    page_num: int
    bbox: tuple
    filename: str
    rel_path: str
    caption: Optional[str]
    caption_id: Optional[str]
    width: int
    height: int


class ImageExtractor:
    """Pull embedded raster images out of a PDF, save as PNG, dedup by xref.

    Filters applied:
      * min pixel size (skip bullet glyphs / icons)
      * recurrence across pages (skip logos / running headers)
      * CMYK / indexed → RGB conversion, then PNG
    """

    CAPTION_RE = re.compile(
        r"^\s*(Figure|Fig\.?|Table)\s+(\d+(?:[.\-]\d+)*)\s*[:.\-–]?\s*(.*)$",
        re.IGNORECASE,
    )
    MARKER_RE = re.compile(r"⟪IMG:(\d+)⟫")

    def __init__(
        self,
        doc: fitz.Document,
        out_dir: Path,
        min_width: int = 80,
        min_height: int = 80,
        recurrence_threshold: float = 0.30,
        verbose: bool = False,
    ):
        self.doc = doc
        self.out_dir = Path(out_dir)
        self.images_dir = self.out_dir / "images"
        self.min_width = min_width
        self.min_height = min_height
        self.recurrence_threshold = recurrence_threshold
        self.verbose = verbose

        self._by_xref: dict[int, ExtractedImage] = {}
        self._occurrences: dict[int, list[tuple[int, Optional[fitz.Rect]]]] = {}
        self._skipped: set[int] = set()

    # ------------------------------------------------------------------ public

    def extract_all(self) -> dict[int, ExtractedImage]:
        self.images_dir.mkdir(parents=True, exist_ok=True)

        self._collect_occurrences()
        self._save_qualifying_images()
        return self._by_xref

    @property
    def by_xref(self) -> dict[int, ExtractedImage]:
        return self._by_xref

    @property
    def caption_ids(self) -> set[str]:
        """Set of caption numeric IDs (e.g. '3.2') we successfully matched to an image."""
        return {img.caption_id for img in self._by_xref.values() if img.caption_id}

    def image_for_page_bbox(
        self, page_num: int, bbox: fitz.Rect, tol: float = 5.0
    ) -> Optional[ExtractedImage]:
        """Look up an extracted image by its position on the given page."""
        best = None
        for xref, img in self._by_xref.items():
            for occ_page, occ_bbox in self._occurrences.get(xref, []):
                if occ_page != page_num or occ_bbox is None:
                    continue
                if (
                    abs(occ_bbox.x0 - bbox.x0) < tol
                    and abs(occ_bbox.y0 - bbox.y0) < tol
                ):
                    return img
                best = best or img  # page-only fallback candidate

        # Fallback: if only one extracted image lives on this page, use it
        page_imgs = [
            img
            for xref, img in self._by_xref.items()
            for occ_page, _ in self._occurrences.get(xref, [])
            if occ_page == page_num
        ]
        if len(page_imgs) == 1:
            return page_imgs[0]
        return None

    # --------------------------------------------------------------- internals

    def _collect_occurrences(self) -> None:
        total = self.doc.page_count
        for page_num in range(total):
            page = self.doc[page_num]
            seen = set()
            for img in page.get_images(full=True):
                xref = img[0]
                if xref in seen:
                    continue
                seen.add(xref)
                try:
                    bbox = page.get_image_bbox(img)
                except Exception:
                    bbox = None
                self._occurrences.setdefault(xref, []).append((page_num, bbox))

    def _save_qualifying_images(self) -> None:
        total_pages = self.doc.page_count
        recurrence_max = max(2, int(total_pages * self.recurrence_threshold))

        used_stems: dict[str, int] = {}

        for xref, occs in self._occurrences.items():
            if len(occs) > recurrence_max:
                self._skipped.add(xref)
                if self.verbose:
                    print(
                        f"  images: skip xref {xref} — appears on {len(occs)} pages"
                    )
                continue

            try:
                info = self.doc.extract_image(xref)
            except Exception as e:
                self._skipped.add(xref)
                if self.verbose:
                    print(f"  images: skip xref {xref} — extract failed: {e}")
                continue

            width = info.get("width", 0)
            height = info.get("height", 0)
            if width < self.min_width or height < self.min_height:
                self._skipped.add(xref)
                continue

            first_page, first_bbox = occs[0]
            caption, caption_id = self._find_caption(first_page, first_bbox)

            stem = self._make_stem(xref, first_page, caption, caption_id)
            # Disambiguate colliding stems (same caption id reused, etc.)
            count = used_stems.get(stem, 0)
            used_stems[stem] = count + 1
            filename = f"{stem}.png" if count == 0 else f"{stem}_{count + 1}.png"
            filepath = self.images_dir / filename

            try:
                self._save_as_png(xref, filepath)
            except Exception as e:
                self._skipped.add(xref)
                if self.verbose:
                    print(f"  images: skip xref {xref} — save failed: {e}")
                continue

            rel_path = f"images/{filename}"
            self._by_xref[xref] = ExtractedImage(
                xref=xref,
                page_num=first_page,
                bbox=tuple(first_bbox) if first_bbox else (0, 0, 0, 0),
                filename=filename,
                rel_path=rel_path,
                caption=caption,
                caption_id=caption_id,
                width=width,
                height=height,
            )

            if self.verbose:
                size_kb = filepath.stat().st_size // 1024
                print(
                    f"  images: wrote {filename} ({width}x{height}, {size_kb}KB)"
                )

    def _save_as_png(self, xref: int, filepath: Path) -> None:
        pix = fitz.Pixmap(self.doc, xref)
        try:
            # Convert away from CMYK / other non-RGB colorspaces
            if pix.colorspace is None or pix.colorspace.n >= 4:
                pix = fitz.Pixmap(fitz.csRGB, pix)
            # Strip alpha if PyMuPDF refuses to PNG-save it directly
            pix.save(str(filepath))
        finally:
            pix = None  # release pixmap

    def _find_caption(
        self, page_num: int, img_bbox: Optional[fitz.Rect]
    ) -> tuple[Optional[str], Optional[str]]:
        if img_bbox is None:
            return None, None

        page = self.doc[page_num]
        blocks = page.get_text("dict")["blocks"]

        def horizontally_overlaps(b):
            return b.x0 < img_bbox.x1 and b.x1 > img_bbox.x0

        below, above = [], []
        for b in blocks:
            if b.get("type") != 0:
                continue
            bbox = fitz.Rect(b["bbox"])
            if not horizontally_overlaps(bbox):
                continue
            if 0 <= (bbox.y0 - img_bbox.y1) <= 120:
                below.append((bbox.y0, self._block_text(b)))
            elif 0 <= (img_bbox.y0 - bbox.y1) <= 120:
                above.append((-bbox.y0, self._block_text(b)))

        for _, text in sorted(below):
            result = self._match_caption(text)
            if result:
                return result

        for _, text in sorted(above):
            result = self._match_caption(text)
            if result:
                return result

        return None, None

    @staticmethod
    def _block_text(block: dict) -> str:
        parts = []
        for line in block.get("lines", []):
            for span in line.get("spans", []):
                parts.append(span.get("text", ""))
            parts.append("\n")
        return "".join(parts).strip()

    def _match_caption(
        self, text: str
    ) -> Optional[tuple[str, str]]:
        first_line = next(
            (ln.strip() for ln in text.split("\n") if ln.strip()), ""
        )
        m = self.CAPTION_RE.match(first_line)
        if not m:
            return None
        kind, number, rest = m.group(1), m.group(2), m.group(3).strip()
        kind_key = kind.strip().lower().rstrip(".")
        kind_norm = {"fig": "Figure", "figure": "Figure", "table": "Table"}.get(
            kind_key, kind.title()
        )
        label = f"{kind_norm} {number}"
        if rest:
            label = f"{label}: {rest[:200]}"
        return label, number

    def _make_stem(
        self,
        xref: int,
        page_num: int,
        caption: Optional[str],
        caption_id: Optional[str],
    ) -> str:
        if caption_id:
            parts = re.split(r"[.\-]", caption_id)
            numeric = [p for p in parts if p.isdigit()]
            if numeric:
                label = "-".join(f"{int(p):02d}" for p in numeric)
                slug = self._slugify(caption)
                stem = f"fig_{label}"
                if slug:
                    stem = f"{stem}_{slug}"
                return stem[:80]
        return f"fig_p{page_num + 1:03d}_x{xref}"

    @staticmethod
    def _slugify(text: Optional[str], max_len: int = 40) -> str:
        if not text:
            return ""
        text = re.sub(
            r"^(Figure|Fig\.?|Table)\s*\d+(?:[.\-]\d+)*\s*[:.\-–]?\s*",
            "",
            text,
            flags=re.IGNORECASE,
        )
        text = re.sub(r"[^\w\s-]", "", text)
        text = re.sub(r"\s+", "_", text.strip())
        return text[:max_len].rstrip("_")
