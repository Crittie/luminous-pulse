#!/usr/bin/env python3
"""Generate Luminous Pulse workbook bundles.

Bundle 1: "the complete grounding collection" — $47
  All 6 workbooks + emergency grounding kit + 30-day practice = 8 products

Bundle 2: "the recovery starter" — $27
  Emergency grounding kit + "tender landings" + "who am I without the title?"

Each bundle gets: branded cover page, table of contents, then merged PDFs.
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import HexColor
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.platypus.flowables import Flowable
from PyPDF2 import PdfReader, PdfWriter
import os
import tempfile

# ── Brand Colors ──
CREAM = HexColor("#FAF6F1")
NAVY = HexColor("#1a1a2e")
DEEP_NAVY = HexColor("#16213e")
NAVY_LIGHT = HexColor("#2a3a5c")
BLUE = HexColor("#6CB4EE")
AMBER = HexColor("#F4C430")
AMBER_SOFT = HexColor("#D4A82A")
LAVENDER = HexColor("#B4A7D6")
SOFT_GRAY = HexColor("#8a8a8a")
LIGHT_GRAY = HexColor("#d0cdc8")
LINE_COLOR = HexColor("#d8d3cc")
WHITE = HexColor("#FFFFFF")

PAGE_W, PAGE_H = letter
MARGIN = 0.85 * inch
CONTENT_W = PAGE_W - 2 * MARGIN

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


# ── Custom Flowables ──

class NavyPageBg(Flowable):
    def __init__(self):
        Flowable.__init__(self)

    def draw(self):
        self.canv.saveState()
        self.canv.setFillColor(NAVY)
        overshoot = 20
        self.canv.rect(
            -MARGIN - overshoot,
            -PAGE_H + MARGIN - overshoot,
            PAGE_W + 2 * overshoot,
            PAGE_H + 2 * overshoot,
            fill=1, stroke=0,
        )
        self.canv.restoreState()

    def wrap(self, availWidth, availHeight):
        return (0, 0)


class HLine(Flowable):
    def __init__(self, width, color=LIGHT_GRAY, thickness=0.5):
        Flowable.__init__(self)
        self.width = width
        self.color = color
        self.thickness = thickness

    def draw(self):
        self.canv.setStrokeColor(self.color)
        self.canv.setLineWidth(self.thickness)
        self.canv.line(0, 0, self.width, 0)

    def wrap(self, availWidth, availHeight):
        return (self.width, self.thickness + 6)


class AccentDot(Flowable):
    def __init__(self, color=AMBER, size=6):
        Flowable.__init__(self)
        self.color = color
        self.dot_size = size

    def draw(self):
        self.canv.setFillColor(self.color)
        self.canv.circle(self.dot_size / 2, self.dot_size / 2,
                         self.dot_size / 2, fill=1, stroke=0)

    def wrap(self, availWidth, availHeight):
        return (self.dot_size, self.dot_size + 4)


# ── Styles ──

def make_styles():
    base = getSampleStyleSheet()
    s = {}

    s["CoverTitle"] = ParagraphStyle(
        "CoverTitle", parent=base["Normal"],
        fontName="Helvetica", fontSize=34, leading=42,
        textColor=WHITE, alignment=TA_CENTER,
        spaceAfter=8,
    )
    s["CoverSubtitle"] = ParagraphStyle(
        "CoverSubtitle", parent=base["Normal"],
        fontName="Helvetica", fontSize=14, leading=20,
        textColor=AMBER, alignment=TA_CENTER,
        spaceAfter=4,
    )
    s["CoverBody"] = ParagraphStyle(
        "CoverBody", parent=base["Normal"],
        fontName="Helvetica", fontSize=11, leading=17,
        textColor=LIGHT_GRAY, alignment=TA_CENTER,
    )
    s["CoverBrand"] = ParagraphStyle(
        "CoverBrand", parent=base["Normal"],
        fontName="Helvetica", fontSize=10, leading=14,
        textColor=AMBER_SOFT, alignment=TA_CENTER,
    )
    s["TocHeading"] = ParagraphStyle(
        "TocHeading", parent=base["Normal"],
        fontName="Helvetica-Bold", fontSize=22, leading=28,
        textColor=NAVY, alignment=TA_LEFT,
        spaceAfter=16,
    )
    s["TocItem"] = ParagraphStyle(
        "TocItem", parent=base["Normal"],
        fontName="Helvetica", fontSize=12, leading=18,
        textColor=NAVY, alignment=TA_LEFT,
        spaceAfter=4, leftIndent=12,
    )
    s["TocDetail"] = ParagraphStyle(
        "TocDetail", parent=base["Normal"],
        fontName="Helvetica", fontSize=9.5, leading=14,
        textColor=SOFT_GRAY, alignment=TA_LEFT,
        spaceAfter=12, leftIndent=12,
    )
    s["TocNote"] = ParagraphStyle(
        "TocNote", parent=base["Normal"],
        fontName="Helvetica", fontSize=10, leading=16,
        textColor=SOFT_GRAY, alignment=TA_LEFT,
        spaceBefore=16,
    )
    s["SectionDivTitle"] = ParagraphStyle(
        "SectionDivTitle", parent=base["Normal"],
        fontName="Helvetica", fontSize=20, leading=26,
        textColor=WHITE, alignment=TA_CENTER,
        spaceAfter=6,
    )
    s["SectionDivSub"] = ParagraphStyle(
        "SectionDivSub", parent=base["Normal"],
        fontName="Helvetica", fontSize=11, leading=16,
        textColor=AMBER, alignment=TA_CENTER,
    )
    return s


# ── Page Builders ──

def build_cover(story, s, title, subtitle, description, value_line):
    """Navy cover page with title, subtitle, and description."""
    story.append(NavyPageBg())
    story.append(Spacer(1, 140))
    story.append(AccentDot(AMBER, 8))
    story.append(Spacer(1, 20))
    story.append(Paragraph(title, s["CoverTitle"]))
    story.append(Spacer(1, 12))
    story.append(HLine(CONTENT_W * 0.4, AMBER_SOFT, 0.6))
    story.append(Spacer(1, 12))
    story.append(Paragraph(subtitle, s["CoverSubtitle"]))
    story.append(Spacer(1, 24))
    story.append(Paragraph(description, s["CoverBody"]))
    story.append(Spacer(1, 16))
    story.append(Paragraph(value_line, s["CoverBody"]))
    story.append(Spacer(1, 60))
    story.append(Paragraph("luminous pulse", s["CoverBrand"]))
    story.append(Paragraph("where anxious humans come to rest", s["CoverBody"]))
    story.append(PageBreak())


def build_toc(story, s, items):
    """Cream-background table of contents page."""
    story.append(Spacer(1, 40))
    story.append(AccentDot(AMBER, 6))
    story.append(Spacer(1, 12))
    story.append(Paragraph("what's inside", s["TocHeading"]))
    story.append(HLine(CONTENT_W, LINE_COLOR, 0.4))
    story.append(Spacer(1, 12))

    for item in items:
        story.append(Paragraph(
            f'<b>{item["title"]}</b>  ·  {item["pages"]} pages  ·  ${item["price"]} value',
            s["TocItem"],
        ))
        story.append(Paragraph(item["desc"], s["TocDetail"]))

    story.append(Spacer(1, 12))
    story.append(HLine(CONTENT_W, LINE_COLOR, 0.4))
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "each workbook is designed to stand alone or be used together.<br/>"
        "start wherever feels right. there is no wrong order.",
        s["TocNote"],
    ))
    story.append(PageBreak())


def build_section_divider(story, s, title, tagline):
    """Navy divider page before each included workbook."""
    story.append(NavyPageBg())
    story.append(Spacer(1, 220))
    story.append(AccentDot(AMBER, 8))
    story.append(Spacer(1, 16))
    story.append(Paragraph(title, s["SectionDivTitle"]))
    story.append(Spacer(1, 8))
    story.append(Paragraph(tagline, s["SectionDivSub"]))
    story.append(PageBreak())


def generate_front_matter_pdf(path, build_fn):
    """Generate a small front-matter PDF, return its path."""
    doc = SimpleDocTemplate(
        path, pagesize=letter,
        leftMargin=MARGIN, rightMargin=MARGIN,
        topMargin=MARGIN, bottomMargin=MARGIN,
    )
    story = []
    build_fn(story)
    doc.build(story)
    return path


def merge_pdfs(output_path, pdf_paths):
    """Merge multiple PDFs into one."""
    writer = PdfWriter()
    for pdf_path in pdf_paths:
        reader = PdfReader(pdf_path)
        for page in reader.pages:
            writer.add_page(page)
    with open(output_path, "wb") as f:
        writer.write(f)
    total = len(writer.pages)
    size_mb = os.path.getsize(output_path) / (1024 * 1024)
    return total, size_mb


# ── Bundle Definitions ──

COMPLETE_COLLECTION = {
    "title": "the complete<br/>grounding collection",
    "subtitle": "every workbook. every practice. one sanctuary.",
    "description": (
        "8 workbooks spanning 340+ pages of grounding practices,<br/>"
        "reflection prompts, breathwork techniques, and identity work.<br/>"
        "from emergency grounding to 12-week sustained practice."
    ),
    "value_line": "$141+ individual value  ·  yours for $47",
    "items": [
        {
            "file": "Emergency-Grounding-Kit.pdf",
            "title": "the emergency grounding kit",
            "desc": "crisis-moment techniques when everything feels like too much",
            "tagline": "for the moments that won't wait",
            "pages": 15, "price": 9,
        },
        {
            "file": "Before-The-Room-Workbook.pdf",
            "title": "before the room",
            "desc": "pre-interview grounding ritual, gap story reframes, nervous system toolkit",
            "tagline": "grounding for the room you're about to walk into",
            "pages": 28, "price": 9,
        },
        {
            "file": "Tender-Landings-Workbook.pdf",
            "title": "tender landings",
            "desc": "a grief journal for career loss — naming what hurts, unsent letters, what remains",
            "tagline": "a grief journal for career loss",
            "pages": 44, "price": 12,
        },
        {
            "file": "Who-Am-I-Without-The-Title-Workbook.pdf",
            "title": "who am I without the title?",
            "desc": "identity mapping, values archaeology, and rebuilding who you are beyond work",
            "tagline": "identity work for when the title is gone",
            "pages": 49, "price": 15,
        },
        {
            "file": "Steady-Workbook.pdf",
            "title": "steady",
            "desc": "12 weeks of weekly intention, mid-week check-in, Friday reflection, and analog rest",
            "tagline": "12 weeks of checking in with yourself",
            "pages": 63, "price": 15,
        },
        {
            "file": "30-Days-Of-Ground-Workbook.pdf",
            "title": "30 days of ground",
            "desc": "daily grounding practice with breathwork, prompts, offline rituals, and affirmation cards",
            "tagline": "one day at a time, for thirty days",
            "pages": 66, "price": 17,
        },
        {
            "file": "The-In-Between-Workbook.pdf",
            "title": "the in-between",
            "desc": "the flagship — 8 deep chapters from freefall to first steps, with interludes and practices",
            "tagline": "the flagship practice for the space between who you were and who you're becoming",
            "pages": 90, "price": 27,
        },
        {
            "file": "30-Day-Luminous-Pulse-Practice.pdf",
            "title": "the 30-day luminous pulse practice",
            "desc": "the original: 30 affirmations, breathwork, reflection prompts, and journaling",
            "tagline": "the original 30-day practice",
            "pages": 39, "price": 37,
        },
    ],
}

RECOVERY_STARTER = {
    "title": "the recovery starter",
    "subtitle": "three workbooks to begin finding ground.",
    "description": (
        "the essential trio for the early days:<br/>"
        "crisis grounding, grief processing, and identity rebuilding.<br/>"
        "92 pages of guided practice."
    ),
    "value_line": "$36 individual value  ·  yours for $27",
    "items": [
        {
            "file": "Emergency-Grounding-Kit.pdf",
            "title": "the emergency grounding kit",
            "desc": "crisis-moment techniques when everything feels like too much",
            "tagline": "for the moments that won't wait",
            "pages": 15, "price": 9,
        },
        {
            "file": "Tender-Landings-Workbook.pdf",
            "title": "tender landings",
            "desc": "a grief journal for career loss — naming what hurts, unsent letters, what remains",
            "tagline": "a grief journal for career loss",
            "pages": 44, "price": 12,
        },
        {
            "file": "Who-Am-I-Without-The-Title-Workbook.pdf",
            "title": "who am I without the title?",
            "desc": "identity mapping, values archaeology, and rebuilding who you are beyond work",
            "tagline": "identity work for when the title is gone",
            "pages": 49, "price": 15,
        },
    ],
}


def build_bundle(bundle_def, output_filename):
    """Build a complete bundle PDF with cover, TOC, dividers, and merged workbooks."""
    s = make_styles()
    tmp_parts = []

    # 1. Front matter (cover + TOC)
    front_path = os.path.join(BASE_DIR, f"_tmp_front_{output_filename}")

    def build_front(story):
        build_cover(
            story, s,
            bundle_def["title"],
            bundle_def["subtitle"],
            bundle_def["description"],
            bundle_def["value_line"],
        )
        build_toc(story, s, bundle_def["items"])

    generate_front_matter_pdf(front_path, build_front)
    tmp_parts.append(front_path)

    # 2. For each workbook: section divider + actual PDF
    for item in bundle_def["items"]:
        # Section divider page
        div_path = os.path.join(BASE_DIR, f"_tmp_div_{item['file']}")

        def build_div(story, _item=item):
            build_section_divider(story, s, _item["title"], _item["tagline"])

        generate_front_matter_pdf(div_path, build_div)
        tmp_parts.append(div_path)

        # Actual workbook PDF
        wb_path = os.path.join(BASE_DIR, item["file"])
        if not os.path.exists(wb_path):
            print(f"  WARNING: {item['file']} not found, skipping")
            continue
        tmp_parts.append(wb_path)

    # 3. Merge everything
    output_path = os.path.join(BASE_DIR, output_filename)
    total_pages, size_mb = merge_pdfs(output_path, tmp_parts)

    # 4. Clean up temp files
    for p in tmp_parts:
        if p.startswith(os.path.join(BASE_DIR, "_tmp_")):
            os.remove(p)

    return output_path, total_pages, size_mb


if __name__ == "__main__":
    print()
    print("=" * 50)
    print("  building: the complete grounding collection")
    print("=" * 50)
    path1, pages1, mb1 = build_bundle(
        COMPLETE_COLLECTION, "The-Complete-Grounding-Collection.pdf"
    )
    print(f"  {path1}")
    print(f"  {pages1} pages  ·  {mb1:.1f} MB")

    print()
    print("=" * 50)
    print("  building: the recovery starter")
    print("=" * 50)
    path2, pages2, mb2 = build_bundle(
        RECOVERY_STARTER, "The-Recovery-Starter.pdf"
    )
    print(f"  {path2}")
    print(f"  {pages2} pages  ·  {mb2:.1f} MB")

    print()
    print("  done. both bundles generated.")
    print()
