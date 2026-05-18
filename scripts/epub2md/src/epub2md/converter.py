"""HTML to Markdown conversion for EPUB content."""

import re
import shutil
import subprocess
import warnings
from dataclasses import dataclass
from functools import lru_cache

from bs4 import BeautifulSoup, NavigableString, Tag, XMLParsedAsHTMLWarning

# Suppress XML parsing warning - EPUB content is XHTML but we parse as HTML
warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)
from markdownify import markdownify as md, MarkdownConverter


# ---------------------------------------------------------------------------
# Module-level helpers
# ---------------------------------------------------------------------------

def _parse_css_roles(css_text: str) -> dict[str, str]:
    """Parse CSS text to find classes that set sub/superscript or bold/italic.

    Returns a mapping of class name → HTML tag name, e.g.
    {"sup": "sup", "italic": "em", "bold-cls": "strong"}.
    """
    roles: dict[str, str] = {}
    # Match rule blocks:  .className { ... }
    for m in re.finditer(
        r"\.([\w-]+)\s*\{([^}]*)\}", css_text
    ):
        cls_name = m.group(1)
        body = m.group(2)
        # Normalise whitespace for matching
        body_norm = re.sub(r"\s+", "", body.lower())
        if "vertical-align:super" in body_norm:
            roles[cls_name] = "sup"
        elif "vertical-align:sub" in body_norm:
            roles[cls_name] = "sub"
        elif "font-style:italic" in body_norm:
            roles[cls_name] = "em"
        elif "font-weight:bold" in body_norm or "font-weight:700" in body_norm:
            roles[cls_name] = "strong"
    return roles


@lru_cache(maxsize=1)
def _check_pandoc() -> str | None:
    """Return the path to pandoc if available, else None (cached)."""
    return shutil.which("pandoc")


def _convert_mathml_to_latex(math_html: str) -> str | None:
    """Convert a MathML fragment to LaTeX via Pandoc.

    Returns the LaTeX string (without delimiters) on success, or None on
    failure / timeout.
    """
    pandoc = _check_pandoc()
    if pandoc is None:
        return None
    try:
        result = subprocess.run(
            [pandoc, "-f", "html", "-t", "markdown"],
            input=math_html.encode("utf-8"),
            capture_output=True,
            timeout=10,
        )
        if result.returncode == 0:
            latex = result.stdout.decode("utf-8", errors="replace").strip()
            # Pandoc wraps inline math in $…$ — strip the delimiters so the
            # caller can re-wrap consistently.
            if latex.startswith("$") and latex.endswith("$"):
                latex = latex[1:-1].strip()
            elif latex.startswith("$$") and latex.endswith("$$"):
                latex = latex[2:-2].strip()
            return latex
    except (subprocess.TimeoutExpired, OSError):
        pass
    return None


# ---------------------------------------------------------------------------
# Custom markdownify converter
# ---------------------------------------------------------------------------

class EPUBMarkdownConverter(MarkdownConverter):
    """Custom Markdown converter for EPUB content."""

    class Options(MarkdownConverter.DefaultOptions):
        sub_symbol = "<sub>"
        sup_symbol = "<sup>"

    def convert_pre(self, el: Tag, text: str, parent_tags: set) -> str:
        """Convert <pre> blocks, preserving code formatting."""
        if not text:
            return ""

        # Try to detect language from class
        lang = ""
        classes = el.get("class", [])
        if isinstance(classes, list):
            for cls in classes:
                if cls.startswith("language-") or cls.startswith("lang-"):
                    lang = cls.split("-", 1)[1]
                    break

        code = text.strip()
        return f"\n```{lang}\n{code}\n```\n"

    def convert_aside(self, el: Tag, text: str, parent_tags: set) -> str:
        """Convert <aside> elements as blockquotes."""
        if not text:
            return ""
        lines = text.strip().split("\n")
        quoted = "\n".join(f"> {line}" for line in lines)
        return f"\n{quoted}\n"

    def convert_figure(self, el: Tag, text: str, parent_tags: set) -> str:
        """Convert <figure> elements with image placeholders."""
        img = el.find("img")
        figcaption = el.find("figcaption")

        caption = ""
        if figcaption:
            caption = figcaption.get_text(strip=True)

        if img:
            alt = img.get("alt", caption or "Figure")
            src = img.get("src", "")
            return f"\n![{alt}]({src})\n"

        return f"\n[Figure: {caption}]\n" if caption else "\n[Figure]\n"

    def convert_code(self, el: Tag, text: str, parent_tags: set) -> str:
        """Convert <code> elements — pass through math-tex content as-is."""
        classes = el.get("class", [])
        if isinstance(classes, str):
            classes = classes.split()
        if "math-tex" in classes:
            # Return the LaTeX content without backtick wrapping
            return text
        # Default: wrap in backticks
        return super().convert_code(el, text, parent_tags)


@dataclass
class ConvertedChapter:
    """Represents a converted chapter."""
    title: str
    filename: str
    content: str
    source_href: str
    order: int


class HTMLToMarkdownConverter:
    """Convert EPUB HTML content to Markdown."""

    def __init__(self, verbose: bool = False):
        self._verbose = verbose
        self._css_roles: dict[str, str] = {}
        self._converter = EPUBMarkdownConverter(
            heading_style="ATX",
            bullets="-",
        )

    def _log(self, msg: str) -> None:
        if self._verbose:
            print(msg)

    # ------------------------------------------------------------------
    # CSS role extraction
    # ------------------------------------------------------------------

    def _extract_css_roles(self, soup: BeautifulSoup) -> dict[str, str]:
        """Read all <style> tags and return a class→tag mapping."""
        roles: dict[str, str] = {}
        for style_tag in soup.find_all("style"):
            css_text = style_tag.get_text()
            if css_text:
                roles.update(_parse_css_roles(css_text))
        return roles

    def _replace_css_spans(self, soup: Tag) -> None:
        """Replace <span class="X"> with semantic HTML based on CSS roles."""
        if not self._css_roles:
            return
        for span in soup.find_all("span", class_=True):
            classes = span.get("class", [])
            if isinstance(classes, str):
                classes = classes.split()
            for cls in classes:
                if cls in self._css_roles:
                    span.name = self._css_roles[cls]
                    break

    # ------------------------------------------------------------------
    # MathML conversion
    # ------------------------------------------------------------------

    def _convert_mathml(self, soup: Tag) -> None:
        """Convert <math> elements to LaTeX wrapped in <code class="math-tex">."""
        math_elements = soup.find_all("math")
        if not math_elements:
            return

        has_pandoc = _check_pandoc() is not None
        if not has_pandoc:
            self._log("    Warning: Pandoc not found — MathML will be converted to plain text")

        for math_el in math_elements:
            math_html = str(math_el)

            if has_pandoc:
                latex = _convert_mathml_to_latex(math_html)
            else:
                latex = None

            if latex:
                # Wrap in $…$ and use a <code class="math-tex"> element so
                # the custom converter can pass it through unescaped.
                snippet = BeautifulSoup(
                    f'<code class="math-tex">${latex}$</code>',
                    "html.parser",
                )
                math_el.replace_with(snippet.code)
            else:
                # Fallback: extract plain text
                plain = math_el.get_text()
                math_el.replace_with(plain)

    # ------------------------------------------------------------------
    # Main pipeline
    # ------------------------------------------------------------------

    def convert(
        self,
        html_content: bytes,
        title: str,
        source_href: str,
        order: int,
    ) -> ConvertedChapter:
        """Convert HTML content to Markdown."""
        # Parse HTML
        soup = BeautifulSoup(html_content, "lxml")

        # Extract CSS roles BEFORE removing <style> tags
        self._css_roles = self._extract_css_roles(soup)
        if self._css_roles:
            self._log(f"    CSS roles detected: {self._css_roles}")

        # Remove unwanted elements (now safe to remove styles)
        for tag in soup.find_all(["script", "style", "meta", "link", "head"]):
            tag.decompose()

        # Get body content
        body = soup.find("body")
        if body is None:
            body = soup

        # Extract title from content if not provided
        if not title or title == "Untitled":
            title = self._extract_title(body) or f"Chapter {order + 1}"

        # Pre-process content
        self._preprocess(body)

        # Convert to Markdown using custom converter
        markdown_content = self._convert_to_markdown(body)

        # Post-process Markdown
        markdown_content = self._postprocess(markdown_content, title)

        # Generate filename
        filename = self._generate_filename(title, order)

        # Add frontmatter
        content_with_frontmatter = self._add_frontmatter(
            markdown_content, title, source_href
        )

        return ConvertedChapter(
            title=title,
            filename=filename,
            content=content_with_frontmatter,
            source_href=source_href,
            order=order,
        )

    def _extract_title(self, soup: Tag) -> str | None:
        """Extract title from first heading."""
        for tag in ["h1", "h2", "h3"]:
            heading = soup.find(tag)
            if heading:
                return heading.get_text(strip=True)
        return None

    def _preprocess(self, soup: Tag) -> None:
        """Pre-process HTML before conversion."""
        # Replace CSS-styled spans with semantic tags
        self._replace_css_spans(soup)

        # Convert MathML to LaTeX
        self._convert_mathml(soup)

        # Convert epub:type annotations to standard elements
        for el in soup.find_all(attrs={"epub:type": True}):
            epub_type = el.get("epub:type", "")
            if "sidebar" in epub_type or "note" in epub_type:
                el.name = "aside"

        # Handle nested code blocks (skip math-tex code elements)
        for pre in soup.find_all("pre"):
            code = pre.find("code")
            if code:
                classes = code.get("class", [])
                if isinstance(classes, str):
                    classes = classes.split()
                if "math-tex" in classes:
                    continue
                # Move code contents directly to pre
                pre.string = code.get_text()
                code.decompose()

    def _convert_to_markdown(self, soup: Tag) -> str:
        """Convert BeautifulSoup element to Markdown using custom converter."""
        return self._converter.convert_soup(soup)

    def _postprocess(self, content: str, title: str) -> str:
        """Post-process Markdown content."""
        # Remove excessive blank lines (more than 2 consecutive)
        content = re.sub(r"\n{4,}", "\n\n\n", content)

        # Normalize heading levels - ensure single H1
        lines = content.split("\n")
        h1_count = sum(1 for line in lines if line.startswith("# ") and not line.startswith("## "))

        if h1_count == 0:
            # Add title as H1 if none exists
            content = f"# {title}\n\n{content}"
        elif h1_count > 1:
            # Convert extra H1s to H2
            found_first = False
            new_lines = []
            for line in lines:
                if line.startswith("# ") and not line.startswith("## "):
                    if found_first:
                        line = "#" + line  # Convert to H2
                    else:
                        found_first = True
                new_lines.append(line)
            content = "\n".join(new_lines)

        # Clean up image references — strip all directory components
        # since extract_images() flattens to images/<filename>
        content = re.sub(
            r"!\[([^\]]*)\]\([^)]*?([^/)\s]+)\)",
            r"![\1](images/\2)",
            content,
        )

        # Remove leading/trailing whitespace
        content = content.strip()

        return content

    def _generate_filename(self, title: str, order: int) -> str:
        """Generate filesystem-safe filename from title."""
        # Remove special characters
        safe_title = re.sub(r"[^\w\s-]", "", title)
        # Replace whitespace with underscores
        safe_title = re.sub(r"\s+", "_", safe_title.strip())
        # Truncate to max 55 chars (leaving room for prefix and extension)
        safe_title = safe_title[:55]
        # Remove trailing underscores
        safe_title = safe_title.rstrip("_")
        # Add zero-padded order prefix
        return f"{order:03d}_{safe_title}.md"

    def _add_frontmatter(
        self, content: str, title: str, source_href: str
    ) -> str:
        """Add YAML frontmatter to content."""
        # Escape quotes in title for YAML
        safe_title = title.replace('"', '\\"')
        frontmatter = f'''---
title: "{safe_title}"
source_file: "{source_href}"
---

'''
        return frontmatter + content
