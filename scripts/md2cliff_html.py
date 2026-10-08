# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "markdown>=3.5",
#     "pillow>=10.0",
# ]
# ///
"""Render a 'cliff notes' Markdown summary into a single portable HTML file.

Portable means: one self-contained `.html` with no external dependency of any
kind. Every image is embedded as a `data:` URI, every CSS declaration that can
be inlined is inlined onto the element as a `style=` attribute, CSS custom
properties are resolved to literal values, and no web fonts or scripts are
referenced. The file can be attached to an email, moved to a machine with
unknown paths, or opened straight off a USB stick and still render.

Why the inlining matters: the design in `Refs/formatted_transcript_style.html`
is expressed with CSS custom properties inside a `<style>` block. Gmail and
Outlook strip `<head><style>` and do not support `var()`, so a naive copy of
that stylesheet renders as unstyled text in exactly the place this file is
meant to be read. The original stylesheet stays the single source of truth --
it is parsed at runtime, not duplicated here -- and is emitted *both* inlined
per element and as a `<style>` block for the rules that cannot be inlined
(hover, nth-child, media queries).

Image sizing: a figure is never upscaled past its intrinsic pixel width, so
lettering inside a diagram cannot be blown up and go soft, and tall figures are
capped so a single graphic cannot eat a whole page. See `display_width`.

Usage:
    uv run scripts/md2cliff_html.py \
        --md      /abs/path/cliff.md \
        --images-dir /abs/path/images \
        --style   /abs/path/Refs/formatted_transcript_style.html \
        --out     /abs/path/out.html \
        --title   "Document title" \
        --target-pages 4
"""

import argparse
import base64
import io
import json
import re
import sys
from pathlib import Path

import markdown
from PIL import Image

# --- page-estimate model -----------------------------------------------------
# At the stylesheet's 17px / 1.65 line-height, a US-Letter page of body copy
# holds roughly 450 words, and its content box is roughly 1000 CSS px tall.
# Both numbers are used only to *report* an estimated page count so the caller
# can tighten or loosen the summary; nothing depends on them being exact.
WORDS_PER_PAGE = 450
PAGE_CONTENT_PX = 1000
CAPTION_PX = 34  # vertical cost of a figure caption line

# --- image sizing ------------------------------------------------------------
# The stylesheet gives body a max-width of 880px with 1.5rem (24px) side
# padding, so the real content box is 832px. Figures are sized against that.
DEFAULT_CONTENT_PX = 832
MIN_DISPLAY_PX = 240
TALL_FRACTION = 0.45       # portrait figures stay narrow or they run off-page
SQUARE_FRACTION = 0.68     # near-square figures get most of the column
WIDE_ASPECT = 1.4          # at or above this, a figure takes the full column
PAGE_SCALE_PX = 1500       # a source this wide is a whole-page extraction
MAX_FIGURE_PX = 820        # a figure may not be taller than this
# PDF-embedded rasters are often only ~420px wide. Shown at native size they
# are crisp but look lost in an 832px column, and their lettering reads small.
# A mild upscale trades a little sharpness for legibility; past ~1.3x the text
# visibly softens, which is the "too large" failure we are avoiding.
MAX_UPSCALE = 1.25

RASTER_MIME = {"PNG": "image/png", "JPEG": "image/jpeg", "GIF": "image/gif",
               "WEBP": "image/webp", "BMP": "image/png", "TIFF": "image/png"}


def display_width(w: int, h: int, content_px: int,
                  max_upscale: float = MAX_UPSCALE) -> int:
    """Pick the on-page width for a figure of intrinsic size w x h.

    Three rules, in order:
      1. Aspect ratio sets the ambition -- portrait figures stay narrow so they
         do not run off the page, landscape figures may use the full column.
      2. Never exceed the intrinsic width. Upscaling a diagram past 100% makes
         its lettering both soft and oversized, which is the failure mode this
         function exists to prevent.
      3. Never go below MIN_DISPLAY_PX unless the image itself is smaller,
         which keeps small figures from becoming unreadably tiny.
    """
    if w <= 0 or h <= 0:
        return content_px
    aspect = w / h
    if aspect < 0.8:
        target = TALL_FRACTION * content_px
    elif aspect < WIDE_ASPECT:
        target = SQUARE_FRACTION * content_px
    else:
        target = float(content_px)

    # A source this wide is a whole-page or full-spread extraction: its own
    # lettering is proportionally large, so the full column is the right call
    # even when the aspect ratio reads as near-square. Squeezing one of these
    # into a two-thirds column is what makes diagram text unreadable.
    if w >= PAGE_SCALE_PX and aspect >= 0.8:
        target = max(target, float(content_px))

    # rule 2: never blow a figure up past MAX_UPSCALE of its real pixels
    target = min(target, float(w) * max_upscale)
    target = max(target, float(min(MIN_DISPLAY_PX, w)))  # rule 3: a floor

    # A figure taller than MAX_FIGURE_PX gets narrowed until it fits.
    if target / aspect > MAX_FIGURE_PX:
        target = min(MAX_FIGURE_PX * aspect, float(w) * max_upscale)
    return max(1, round(target))


def encode_image(path: Path, disp_w: int, retina: int) -> tuple[str, int, int, int]:
    """Return (data-URI, intrinsic_w, intrinsic_h, encoded_bytes).

    The stored pixels are capped at ``retina * disp_w`` so a 3000px source does
    not carry 2 MB of base64 for a 720px slot. Format is preserved (a diagram
    re-encoded as JPEG picks up ringing around text), with palette/alpha PNGs
    left alone.
    """
    with Image.open(path) as im:
        im.load()
        fmt = (im.format or "PNG").upper()
        w, h = im.size
        max_px = max(1, disp_w * max(1, retina))
        out = im
        if w > max_px:
            new_h = max(1, round(h * max_px / w))
            out = im.resize((max_px, new_h), Image.LANCZOS)

        buf = io.BytesIO()
        save_fmt = "JPEG" if fmt in ("JPEG", "JPG") else "PNG"
        if save_fmt == "JPEG":
            out.convert("RGB").save(buf, "JPEG", quality=85, optimize=True)
        else:
            out.save(buf, "PNG", optimize=True)
        raw = buf.getvalue()

    # If a PNG turned out enormous and has no transparency, JPEG is far smaller.
    if save_fmt == "PNG" and len(raw) > 900_000:
        with Image.open(path) as im2:
            im2.load()
            if im2.mode not in ("RGBA", "LA", "P"):
                buf2 = io.BytesIO()
                scaled = im2
                if im2.size[0] > max_px:
                    nh = max(1, round(im2.size[1] * max_px / im2.size[0]))
                    scaled = im2.resize((max_px, nh), Image.LANCZOS)
                scaled.convert("RGB").save(buf2, "JPEG", quality=85, optimize=True)
                if len(buf2.getvalue()) < len(raw):
                    raw, save_fmt = buf2.getvalue(), "JPEG"

    mime = RASTER_MIME.get(save_fmt, "image/png")
    uri = f"data:{mime};base64," + base64.b64encode(raw).decode("ascii")
    return uri, w, h, len(raw)


# --- stylesheet handling -----------------------------------------------------
#: Selectors simple enough to inline onto every matching element.
INLINABLE = {
    "body", "h1", "h2", "h3", "h4", "p", "a", "ul", "ol", "li", "img",
    "blockquote", "code", "pre", "table", "th", "td", "tr", "hr", "strong",
    "em", "figure", "figcaption",
}


def parse_style(style_html: str) -> tuple[dict[str, str], str]:
    """Parse the reference stylesheet.

    Returns (tag -> inline declaration string, full CSS with vars resolved).
    Rules whose selector is not a bare tag -- `a:hover`, `tr:nth-child(even)`,
    `h2#table-of-contents + ul` -- cannot become a style attribute and survive
    only in the emitted <style> block.
    """
    css = re.sub(r"</?style[^>]*>", "", style_html, flags=re.I)
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)

    variables: dict[str, str] = {}
    for block in re.findall(r":root\s*\{(.*?)\}", css, flags=re.S):
        for name, value in re.findall(r"(--[\w-]+)\s*:\s*([^;]+);", block):
            variables[name.strip()] = value.strip()

    def resolve(text: str) -> str:
        # Repeat so a variable defined in terms of another still resolves.
        for _ in range(5):
            new = re.sub(
                r"var\(\s*(--[\w-]+)\s*(?:,\s*([^)]+))?\)",
                lambda m: variables.get(m.group(1), (m.group(2) or "").strip()),
                text,
            )
            if new == text:
                break
            text = new
        return text

    css = resolve(css)

    inline: dict[str, str] = {}
    for selector, body in re.findall(r"([^{}]+)\{([^{}]*)\}", css):
        decls = " ".join(body.split()).strip().rstrip(";")
        if not decls:
            continue
        # A declaration destined for a style="..." attribute must not contain a
        # double quote. The reference font stack has several ("Segoe UI",
        # "SF Mono"), and left as-is they close the attribute early and break
        # every styled element on the page. CSS accepts single-quoted family
        # names, so swapping is lossless.
        decls = decls.replace('"', "'")
        for sel in (s.strip() for s in selector.split(",")):
            if sel in INLINABLE:
                merged = inline.get(sel, "")
                inline[sel] = (merged + "; " + decls).strip("; ") if merged else decls

    # `p > em:only-child` is the caption style and cannot be expressed as a tag
    # selector, but captions are load-bearing in a figure-heavy document and
    # mail clients drop the <style> block. Keep it for targeted inlining.
    caption = ""
    for selector, body in re.findall(r"([^{}]+)\{([^{}]*)\}", css):
        if "em:only-child" in selector:
            caption = " ".join(body.split()).strip().rstrip(";").replace('"', "'")
    if caption:
        inline["__caption__"] = caption
    return inline, css.strip()


def inject_inline_styles(html: str, inline: dict[str, str]) -> str:
    """Add a style= attribute to every element we have declarations for.

    The HTML here is generated by python-markdown from our own Markdown, so it
    is small, well-formed and predictable -- a targeted regex is safe and keeps
    this script dependency-light. An existing style= attribute wins, since it
    carries the per-figure sizing computed above.
    """
    for tag, decls in inline.items():
        # body lands on the wrapper element; img is already styled per figure
        # with its computed width, so re-adding the generic rules is redundant.
        if tag in ("body", "img") or tag.startswith("__"):
            continue
        pattern = re.compile(rf"<{tag}(?=[\s>/])([^>]*)>", flags=re.I)

        def add(m: re.Match, tag=tag, decls=decls) -> str:
            attrs = m.group(1)
            if re.search(r"\bstyle\s*=", attrs, flags=re.I):
                return f"<{tag}{attrs}>"  # an explicit style= already won
            return f'<{tag}{attrs} style="{decls}">'

        html = pattern.sub(add, html)
    return html


def build(md_path: Path, images_dir: Path, style_path: Path, title: str,
          subtitle: str | None, content_px: int, retina: int,
          max_bytes: int, max_upscale: float = MAX_UPSCALE) -> tuple[str, dict]:
    text = md_path.read_text(encoding="utf-8")
    text = re.sub(r"^---\s*\n.*?\n---\s*\n", "", text, count=1, flags=re.S)

    words = len(re.sub(r"!\[[^\]]*\]\([^)]*\)", "", text).split())

    html_body = markdown.markdown(
        text, extensions=["tables", "fenced_code", "toc", "sane_lists", "attr_list"]
    )

    inline, full_css = parse_style(style_path.read_text(encoding="utf-8"))

    figures: list[dict] = []
    total_img_bytes = 0
    total_fig_px = 0
    missing: list[str] = []

    def replace_img(m: re.Match) -> str:
        nonlocal total_img_bytes, total_fig_px
        attrs = m.group(1)
        src_m = re.search(r'src\s*=\s*"([^"]+)"', attrs)
        alt_m = re.search(r'alt\s*=\s*"([^"]*)"', attrs)
        if not src_m:
            return m.group(0)
        src = src_m.group(1)
        alt = alt_m.group(1) if alt_m else ""
        if src.startswith(("http://", "https://", "data:")):
            # An external URL is exactly what portability forbids.
            missing.append(f"{src} (external URL, dropped)")
            return ""
        candidate = (images_dir / Path(src).name)
        if not candidate.exists():
            missing.append(src)
            return ""
        try:
            with Image.open(candidate) as probe:
                iw, ih = probe.size
            disp = display_width(iw, ih, content_px, max_upscale)
            uri, iw, ih, nbytes = encode_image(candidate, disp, retina)
        except Exception as exc:  # unreadable or unsupported image
            missing.append(f"{src} ({exc})")
            return ""
        total_img_bytes += nbytes
        disp_h = round(disp / (iw / ih)) if ih else disp
        total_fig_px += disp_h + CAPTION_PX
        figures.append({"file": Path(src).name, "intrinsic": [iw, ih],
                        "display_px": disp, "scale": round(disp / iw, 2),
                        "display_h_px": disp_h, "bytes": nbytes, "alt": alt})
        img_style = (f"{inline.get('img', '')}; width:{disp}px; max-width:100%; "
                     f"height:auto; display:block; margin:1.4rem auto 0.6rem")
        img_style = img_style.strip("; ")
        return (f'<img src="{uri}" alt="{alt}" width="{disp}" '
                f'style="{img_style}">')

    html_body = re.sub(r"<img([^>]*)>", replace_img, html_body)

    # Style the figure captions -- a paragraph whose entire content is one <em>.
    caption_css = inline.get("__caption__", "")
    if caption_css:
        html_body = re.sub(
            r"<p>(\s*<em>.*?</em>\s*)</p>",
            lambda m: f'<p style="{caption_css}">{m.group(1)}</p>',
            html_body, flags=re.S)

    html_body = inject_inline_styles(html_body, inline)

    body_decls = inline.get("body", "")
    header = f"<h1 style=\"{inline.get('h1', '')}\">{title}</h1>"
    if subtitle:
        header += (f'<p style="{inline.get("p", "")}; color:#52606d; '
                   f'margin-top:-0.4rem">{subtitle}</p>')

    est_pages = round(words / WORDS_PER_PAGE + total_fig_px / PAGE_CONTENT_PX, 2)

    doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<style>
{full_css}
@media (max-width: 760px) {{
  body, div.cliff-root {{ padding: 1.5rem 1rem 3rem !important; font-size: 16px !important; }}
  img {{ width: 100% !important; }}
}}
</style>
</head>
<body style="{body_decls}">
<div class="cliff-root" style="{body_decls}">
{header}
{html_body}
</div>
</body>
</html>
"""
    report = {
        "title": title,
        "words": words,
        "figures": len(figures),
        "figure_detail": figures,
        "estimated_pages": est_pages,
        "image_bytes": total_img_bytes,
        "html_bytes": len(doc.encode("utf-8")),
        "missing_images": missing,
        "over_max_bytes": len(doc.encode("utf-8")) > max_bytes,
        "max_bytes": max_bytes,
    }
    return doc, report


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Render a cliff-notes Markdown summary into one portable, "
                    "fully self-contained HTML file.")
    ap.add_argument("--md", required=True, type=Path, help="Cliff Markdown file")
    ap.add_argument("--images-dir", required=True, type=Path,
                    help="Directory holding the referenced images")
    ap.add_argument("--style", required=True, type=Path,
                    help="Reference stylesheet (Refs/formatted_transcript_style.html)")
    ap.add_argument("--out", required=True, type=Path, help="Output .html path")
    ap.add_argument("--title", required=True)
    ap.add_argument("--subtitle", default=None)
    ap.add_argument("--target-pages", type=float, default=None,
                    help="Reported alongside the estimate so the caller can retune")
    ap.add_argument("--content-px", type=int, default=DEFAULT_CONTENT_PX)
    ap.add_argument("--max-upscale", type=float, default=MAX_UPSCALE,
                    help="Largest allowed enlargement past a figure's real pixel "
                         "width (1.0 = never upscale)")
    ap.add_argument("--retina", type=int, default=2,
                    help="Store images at this multiple of display width (1 to halve size)")
    ap.add_argument("--max-bytes", type=int, default=20_000_000,
                    help="Warn when the finished file exceeds this (email limit)")
    args = ap.parse_args()

    for p in (args.md, args.images_dir, args.style):
        if not p.exists():
            print(f"Error: not found: {p.resolve()}", file=sys.stderr)
            return 1

    doc, report = build(
        args.md.resolve(), args.images_dir.resolve(), args.style.resolve(),
        args.title, args.subtitle, args.content_px, args.retina, args.max_bytes,
        args.max_upscale,
    )
    out = args.out.resolve()
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(doc, encoding="utf-8")

    report["out"] = str(out)
    if args.target_pages:
        report["target_pages"] = args.target_pages
        report["pages_delta"] = round(report["estimated_pages"] - args.target_pages, 2)
    print(json.dumps(report, indent=2))

    if report["missing_images"]:
        print(f"Warning: {len(report['missing_images'])} image reference(s) could "
              f"not be embedded and were dropped.", file=sys.stderr)
    if report["over_max_bytes"]:
        print(f"Warning: {report['html_bytes']} bytes exceeds --max-bytes "
              f"{args.max_bytes}; lower --retina or cut figures.", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
