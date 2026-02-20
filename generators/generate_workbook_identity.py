#!/usr/bin/env python3
"""Generate "who am I without the title?" workbook PDF — Luminous Pulse ($15).

8 exercises for reclaiming who you are beyond your job.

Design: Printable on cream/off-white background. Navy + amber accents.
Generous margins for comfortable handwriting. Writing lines where needed.
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import HexColor
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, Image
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.platypus.flowables import Flowable
import os

# ── Brand Colors (workbook palette — light background for printing) ──
CREAM = HexColor("#FAF6F1")
WARM_WHITE = HexColor("#F5F0EB")
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


# ── Custom Flowables ──

class WritingLines(Flowable):
    """Draw horizontal writing lines for journaling space."""
    def __init__(self, width, num_lines=8, spacing=28, color=LINE_COLOR):
        Flowable.__init__(self)
        self.line_width = width
        self.num_lines = num_lines
        self.spacing = spacing
        self.color = color

    def draw(self):
        self.canv.setStrokeColor(self.color)
        self.canv.setLineWidth(0.4)
        for i in range(self.num_lines):
            y = self.num_lines * self.spacing - (i + 1) * self.spacing
            self.canv.line(0, y, self.line_width, y)

    def wrap(self, availWidth, availHeight):
        return (self.line_width, self.num_lines * self.spacing)


class HLine(Flowable):
    """Thin horizontal divider."""
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
    """Small decorative dot (section marker)."""
    def __init__(self, color=AMBER, size=6):
        Flowable.__init__(self)
        self.color = color
        self.dot_size = size

    def draw(self):
        self.canv.setFillColor(self.color)
        self.canv.circle(self.dot_size / 2, self.dot_size / 2, self.dot_size / 2, fill=1, stroke=0)

    def wrap(self, availWidth, availHeight):
        return (self.dot_size, self.dot_size + 4)


class CheckboxLine(Flowable):
    """A line with a small checkbox at the start."""
    def __init__(self, width, color=LINE_COLOR):
        Flowable.__init__(self)
        self.line_width = width
        self.color = color

    def draw(self):
        self.canv.setStrokeColor(NAVY_LIGHT)
        self.canv.setLineWidth(0.6)
        self.canv.rect(0, 2, 10, 10, fill=0, stroke=1)
        self.canv.setStrokeColor(self.color)
        self.canv.setLineWidth(0.4)
        self.canv.line(18, 0, self.line_width, 0)

    def wrap(self, availWidth, availHeight):
        return (self.line_width, 16)


class NavyPageBg(Flowable):
    """Paints the current page navy (for section openers)."""
    def __init__(self):
        Flowable.__init__(self)

    def draw(self):
        self.canv.saveState()
        self.canv.setFillColor(NAVY)
        overshoot = 20
        self.canv.rect(
            -MARGIN - overshoot,
            -(PAGE_H - MARGIN) - overshoot,
            PAGE_W + 2 * overshoot,
            PAGE_H + 2 * overshoot,
            fill=1, stroke=0
        )
        y_line = -(PAGE_H - MARGIN) + 60
        self.canv.setStrokeColor(AMBER)
        self.canv.setLineWidth(0.8)
        self.canv.line(0, y_line, CONTENT_W, y_line)
        self.canv.restoreState()

    def wrap(self, availWidth, availHeight):
        return (0, 0)


class NumberedCircle(Flowable):
    """A small numbered circle for list items."""
    def __init__(self, number, color=AMBER_SOFT, size=20):
        Flowable.__init__(self)
        self.number = str(number)
        self.color = color
        self.size = size

    def draw(self):
        r = self.size / 2
        self.canv.setFillColor(self.color)
        self.canv.circle(r, r, r, fill=1, stroke=0)
        self.canv.setFillColor(WHITE)
        self.canv.setFont("Helvetica-Bold", 10)
        self.canv.drawCentredString(r, r - 3.5, self.number)

    def wrap(self, availWidth, availHeight):
        return (self.size, self.size + 4)


class DashedLine(Flowable):
    """A dashed cutting line for the envelope template."""
    def __init__(self, width, color=SOFT_GRAY):
        Flowable.__init__(self)
        self.line_width = width
        self.color = color

    def draw(self):
        self.canv.setStrokeColor(self.color)
        self.canv.setLineWidth(0.5)
        self.canv.setDash(4, 3)
        self.canv.line(0, 0, self.line_width, 0)
        self.canv.setDash()

    def wrap(self, availWidth, availHeight):
        return (self.line_width, 6)


class EnvelopeTemplate(Flowable):
    """Draw a simple envelope outline for the 'letter to future self' exercise."""
    def __init__(self, width, height=180):
        Flowable.__init__(self)
        self.env_width = width
        self.env_height = height

    def draw(self):
        w = self.env_width
        h = self.env_height
        c = self.canv
        # Outer rectangle (dashed)
        c.setStrokeColor(NAVY_LIGHT)
        c.setLineWidth(0.8)
        c.setDash(6, 4)
        c.rect(0, 0, w, h, fill=0, stroke=1)
        c.setDash()
        # Scissors icon hint
        c.setFont("Helvetica", 8)
        c.setFillColor(SOFT_GRAY)
        c.drawString(8, h + 6, "cut along dashed line  ·  fold  ·  seal  ·  open in 90 days")
        # Flap triangle
        c.setStrokeColor(LIGHT_GRAY)
        c.setLineWidth(0.5)
        c.line(0, h, w / 2, h * 0.55)
        c.line(w, h, w / 2, h * 0.55)
        # "To:" line
        c.setFont("Helvetica-Oblique", 10)
        c.setFillColor(NAVY_LIGHT)
        c.drawString(30, h * 0.35, "to: future me")
        # Date line
        c.setStrokeColor(LINE_COLOR)
        c.setLineWidth(0.4)
        c.drawString(30, h * 0.2, "open on: _______________")
        # "From:" line
        c.drawString(w - 160, h * 0.12, "from: today's me")

    def wrap(self, availWidth, availHeight):
        return (self.env_width, self.env_height + 20)


# ── Page Backgrounds ──

def draw_bg(canvas, doc):
    """Standard page background — cream with subtle footer."""
    canvas.saveState()
    canvas.setFillColor(CREAM)
    canvas.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    canvas.setFont("Helvetica", 7)
    canvas.setFillColor(SOFT_GRAY)
    canvas.drawCentredString(PAGE_W / 2, 30, "who am I without the title?  ·  luminouspulse.co")
    page_num = canvas.getPageNumber()
    if page_num > 2:
        canvas.drawRightString(PAGE_W - MARGIN, 30, str(page_num))
    canvas.restoreState()


def draw_bg_cover(canvas, doc):
    """Cover page — navy background."""
    canvas.saveState()
    canvas.setFillColor(NAVY)
    canvas.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    canvas.restoreState()


# ── Styles ──

def create_styles():
    styles = getSampleStyleSheet()

    styles.add(ParagraphStyle(
        name="CoverTitle", fontName="Helvetica-Bold", fontSize=32,
        textColor=WHITE, alignment=TA_CENTER, leading=40, spaceAfter=16,
    ))
    styles.add(ParagraphStyle(
        name="CoverSub", fontName="Helvetica-Oblique", fontSize=13,
        textColor=LAVENDER, alignment=TA_CENTER, leading=19, spaceAfter=8,
    ))
    styles.add(ParagraphStyle(
        name="CoverFooter", fontName="Helvetica", fontSize=10,
        textColor=HexColor("#888888"), alignment=TA_CENTER, leading=14,
    ))

    # Section opener styles (on navy)
    styles.add(ParagraphStyle(
        name="SectionNum", fontName="Helvetica", fontSize=12,
        textColor=AMBER, alignment=TA_CENTER, leading=16, spaceAfter=8,
        letterSpacing=3,
    ))
    styles.add(ParagraphStyle(
        name="SectionTitle", fontName="Helvetica-Bold", fontSize=26,
        textColor=WHITE, alignment=TA_CENTER, leading=34, spaceAfter=18,
    ))
    styles.add(ParagraphStyle(
        name="SectionEpigraph", fontName="Helvetica-Oblique", fontSize=11.5,
        textColor=LAVENDER, alignment=TA_CENTER, leading=17, spaceAfter=8,
        leftIndent=30, rightIndent=30,
    ))

    # Content page styles (on cream)
    styles.add(ParagraphStyle(
        name="Heading", fontName="Helvetica-Bold", fontSize=20,
        textColor=NAVY, alignment=TA_CENTER, leading=26, spaceAfter=16,
    ))
    styles.add(ParagraphStyle(
        name="SubHeading", fontName="Helvetica-Bold", fontSize=13,
        textColor=NAVY, alignment=TA_LEFT, leading=18, spaceAfter=8,
    ))
    styles.add(ParagraphStyle(
        name="ExerciseLabel", fontName="Helvetica-Bold", fontSize=10,
        textColor=AMBER_SOFT, alignment=TA_LEFT, leading=14, spaceAfter=4,
        letterSpacing=2,
    ))
    styles.add(ParagraphStyle(
        name="Prompt", fontName="Helvetica-Oblique", fontSize=12,
        textColor=NAVY, alignment=TA_LEFT, leading=18, spaceAfter=12,
        leftIndent=4,
    ))
    styles.add(ParagraphStyle(
        name="PromptCenter", fontName="Helvetica-Oblique", fontSize=12,
        textColor=NAVY, alignment=TA_CENTER, leading=18, spaceAfter=12,
    ))
    styles.add(ParagraphStyle(
        name="Body", fontName="Helvetica", fontSize=10.5,
        textColor=HexColor("#333333"), alignment=TA_LEFT, leading=16, spaceAfter=10,
    ))
    styles.add(ParagraphStyle(
        name="BodyCenter", fontName="Helvetica", fontSize=10.5,
        textColor=HexColor("#333333"), alignment=TA_CENTER, leading=16, spaceAfter=10,
    ))
    styles.add(ParagraphStyle(
        name="Affirmation", fontName="Helvetica-Bold", fontSize=15,
        textColor=NAVY, alignment=TA_CENTER, leading=21, spaceAfter=14,
        leftIndent=16, rightIndent=16,
    ))
    styles.add(ParagraphStyle(
        name="AffirmationLight", fontName="Helvetica-Oblique", fontSize=13,
        textColor=NAVY_LIGHT, alignment=TA_CENTER, leading=19, spaceAfter=12,
        leftIndent=16, rightIndent=16,
    ))
    styles.add(ParagraphStyle(
        name="SmallLabel", fontName="Helvetica", fontSize=8,
        textColor=SOFT_GRAY, alignment=TA_LEFT, leading=12, spaceAfter=4,
        letterSpacing=1,
    ))
    styles.add(ParagraphStyle(
        name="ItalicNote", fontName="Helvetica-Oblique", fontSize=10,
        textColor=SOFT_GRAY, alignment=TA_LEFT, leading=15, spaceAfter=8,
    ))
    styles.add(ParagraphStyle(
        name="ItalicCenter", fontName="Helvetica-Oblique", fontSize=10.5,
        textColor=SOFT_GRAY, alignment=TA_CENTER, leading=15, spaceAfter=10,
    ))
    styles.add(ParagraphStyle(
        name="CTA", fontName="Helvetica-Bold", fontSize=12,
        textColor=AMBER_SOFT, alignment=TA_CENTER, leading=18, spaceAfter=8,
    ))
    styles.add(ParagraphStyle(
        name="ListItem", fontName="Helvetica", fontSize=10.5,
        textColor=HexColor("#333333"), alignment=TA_LEFT, leading=16, spaceAfter=6,
        leftIndent=28, bulletIndent=12,
    ))
    styles.add(ParagraphStyle(
        name="TOCSection", fontName="Helvetica-Bold", fontSize=11,
        textColor=NAVY, alignment=TA_LEFT, leading=16, spaceAfter=3,
    ))
    styles.add(ParagraphStyle(
        name="TOCItem", fontName="Helvetica", fontSize=10,
        textColor=HexColor("#555555"), alignment=TA_LEFT, leading=14, spaceAfter=2,
        leftIndent=16,
    ))

    return styles


# ── Page Builders ──

def build_cover(story, s):
    story.append(Spacer(1, 180))
    logo_path = os.path.join(os.path.dirname(__file__), "logo-abstract-sanctuary-transparent.png")
    if os.path.exists(logo_path):
        img = Image(logo_path, width=120, height=63)
        img.hAlign = "CENTER"
        story.append(img)
        story.append(Spacer(1, 40))
    story.append(Paragraph("who am I<br/>without the title?", s["CoverTitle"]))
    story.append(Spacer(1, 14))
    story.append(Paragraph(
        "8 exercises for reclaiming who you are<br/>beyond your job.",
        s["CoverSub"]
    ))
    story.append(Spacer(1, 80))
    story.append(Paragraph("Luminous Pulse", s["CoverFooter"]))
    story.append(Paragraph("luminouspulse.co", s["CoverFooter"]))
    story.append(PageBreak())


def build_intro(story, s):
    story.append(Spacer(1, 50))
    story.append(Paragraph("before you begin", s["Heading"]))
    story.append(Spacer(1, 16))
    story.append(HLine(CONTENT_W, AMBER, 0.6))
    story.append(Spacer(1, 16))

    story.append(Paragraph(
        "when someone asks you who you are, what do you say?",
        s["PromptCenter"]
    ))
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "for most of us, the answer starts with a job title. "
        "I'm a product manager. I'm an engineer. I'm a designer. "
        "we don't even notice how completely we've fused our identity "
        "with our role — until the role is taken away.",
        s["Body"]
    ))
    story.append(Paragraph(
        "and then the question becomes something different. "
        "something heavier. something that wakes you up at 3am: "
        "if I'm not that anymore... who am I?",
        s["Body"]
    ))
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "this workbook is for that question.",
        s["BodyCenter"]
    ))
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "it won't give you a new title. it won't tell you what to do next. "
        "instead, it will walk you through 8 exercises designed to help you "
        "remember — or maybe discover for the first time — the parts of you "
        "that existed before the title, that exist alongside the title, and "
        "that will outlast any title.",
        s["Body"]
    ))

    story.append(Spacer(1, 16))
    story.append(AccentDot(AMBER))
    story.append(Spacer(1, 12))

    story.append(Paragraph("how to use this workbook", s["SubHeading"]))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "<b>print it.</b> neuroscience shows that handwriting activates emotional "
        "processing centers that typing cannot reach. when you're untangling "
        "identity, your hands need to be part of the conversation.",
        s["Body"]
    ))
    story.append(Paragraph(
        "<b>go in order.</b> the 8 exercises build on each other. they move from "
        "looking backward (who you were) through the present (who you are right now) "
        "to looking forward (who you might become).",
        s["Body"]
    ))
    story.append(Paragraph(
        "<b>take your time.</b> one exercise per sitting, or one per day, or one per "
        "week. there is no pace you should be at. if an exercise feels heavy, "
        "put the workbook down and come back tomorrow.",
        s["Body"]
    ))
    story.append(Paragraph(
        "<b>be honest.</b> nobody will read this but you. the messier, the better. "
        "cross things out. write in the margins. argue with the prompts. "
        "this is your space.",
        s["Body"]
    ))

    story.append(Spacer(1, 20))
    story.append(Paragraph(
        '"you are more than your output. you are the meaning behind it."',
        s["AffirmationLight"]
    ))
    story.append(PageBreak())


def build_toc(story, s):
    story.append(Spacer(1, 40))
    story.append(Paragraph("contents", s["Heading"]))
    story.append(Spacer(1, 14))
    story.append(HLine(CONTENT_W, AMBER, 0.6))
    story.append(Spacer(1, 14))

    exercises = [
        ("exercise 1", "the roles I've worn", "mapping the identities you carry"),
        ("exercise 2", "what I valued before the title", "excavating your core values"),
        ("exercise 3", "20 things that make me, me", "identity beyond the job"),
        (None, "body check-in", "where you hold your identity"),
        ("exercise 4", "the origin story", "where you began — before any title found you"),
        (None, "a grounding practice", "the physiological sigh"),
        ("exercise 5", "composting the old identity", "what to keep, what to release, what to transform"),
        ("exercise 6", "seeds of who I'm becoming", "planting without forcing"),
        (None, "permission slip", "what you're allowed to feel"),
        ("exercise 7", "letter to your future self", "seal it. open it in 90 days."),
        ("exercise 8", "the declaration", "affirmations for identity reclamation"),
    ]

    for num, title, desc in exercises:
        if num:
            story.append(Paragraph(f"{num}: {title}", s["TOCSection"]))
        else:
            story.append(Paragraph(title, s["TOCItem"]))
        story.append(Paragraph(desc, s["TOCItem"]))
        story.append(Spacer(1, 3))

    story.append(Spacer(1, 8))
    story.append(HLine(CONTENT_W * 0.3, LIGHT_GRAY, 0.3))
    story.append(Spacer(1, 6))
    story.append(Paragraph("closing + notes + envelope", s["TOCSection"]))

    story.append(PageBreak())


def build_exercise_opener(story, s, number, title, epigraph):
    """Full-page navy section opener for an exercise."""
    story.append(NavyPageBg())
    story.append(Spacer(1, 200))
    story.append(Paragraph(f"EXERCISE {number}", s["SectionNum"]))
    story.append(Spacer(1, 12))
    story.append(Paragraph(title, s["SectionTitle"]))
    story.append(Spacer(1, 20))
    story.append(Paragraph(epigraph, s["SectionEpigraph"]))
    story.append(PageBreak())


def build_prompt_page(story, s, label, prompt_text, lines=10, note=None):
    """A journaling prompt with writing lines."""
    story.append(Spacer(1, 20))
    story.append(Paragraph(label.upper(), s["ExerciseLabel"]))
    story.append(Spacer(1, 6))
    story.append(Paragraph(prompt_text, s["Prompt"]))
    if note:
        story.append(Paragraph(note, s["ItalicNote"]))
    story.append(Spacer(1, 12))
    story.append(WritingLines(CONTENT_W, num_lines=lines))
    story.append(Spacer(1, 16))


def build_prompt_with_break(story, s, label, prompt_text, lines=10, note=None):
    """Prompt page that fills the page then breaks."""
    build_prompt_page(story, s, label, prompt_text, lines, note)
    story.append(PageBreak())


# ── EXERCISE 1: The Roles I've Worn ──

def build_exercise_1(story, s):
    build_exercise_opener(story, s, "1", "the roles I've worn",
        "you have always been more than one thing.<br/>"
        "let's remember them all.")

    # Page 1: Introduction + first mapping
    story.append(Spacer(1, 16))
    story.append(Paragraph("mapping the identities you carry", s["SubHeading"]))
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "you are not just your job title. you never were. but when the title "
        "was the loudest identity, it's easy to forget the others.",
        s["Body"]
    ))
    story.append(Paragraph(
        "this exercise asks you to map every role you've ever played. "
        "not just professional roles — all of them. the ones you chose, "
        "the ones that chose you, and the ones you haven't thought about in years.",
        s["Body"]
    ))
    story.append(Spacer(1, 10))

    story.append(Paragraph("PART A: THE ROLES", s["ExerciseLabel"]))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "list every role you play or have played. include professional titles, "
        "family roles, creative identities, community roles, forgotten hobbies. "
        "nothing is too small.",
        s["ItalicNote"]
    ))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "examples: project manager, daughter, gardener, neighbor who waters "
        "the plants, the friend who remembers birthdays, weekend baker, "
        "the person animals trust...",
        s["ItalicNote"]
    ))
    story.append(Spacer(1, 10))
    story.append(WritingLines(CONTENT_W, num_lines=14))
    story.append(PageBreak())

    # Page 2: Reflection on the roles
    story.append(Spacer(1, 16))
    story.append(Paragraph("PART B: THE PATTERNS", s["ExerciseLabel"]))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "look at your list. circle the 5 roles that feel most like you — "
        "the ones that would survive any job change.",
        s["ItalicNote"]
    ))
    story.append(Spacer(1, 10))

    build_prompt_page(story, s, "REFLECT",
        "which roles on your list existed before you ever had a job title?",
        lines=6)

    build_prompt_page(story, s, "REFLECT",
        "which role do you play that nobody pays you for — "
        "but that makes you feel most like yourself?",
        lines=6)
    story.append(PageBreak())

    # Page 3: The role that's grieving
    build_prompt_with_break(story, s, "DEEPER",
        "if your job title could speak, what would it say to you right now? "
        "and what would you say back?",
        lines=12,
        note="(this one might surprise you. let it.)")


# ── EXERCISE 2: Values Excavation ──

def build_exercise_2(story, s):
    build_exercise_opener(story, s, "2", "what I valued<br/>before the title",
        "your values don't come from your job description.<br/>"
        "they come from you.")

    # Values word bank
    story.append(Spacer(1, 16))
    story.append(Paragraph("excavating your core values", s["SubHeading"]))
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "when we lose a job, we sometimes lose touch with what we actually "
        "value — because the job told us what to value. deadlines. KPIs. "
        "velocity. those were the job's values. what are yours?",
        s["Body"]
    ))
    story.append(Spacer(1, 10))

    story.append(Paragraph("PART A: THE WORD BANK", s["ExerciseLabel"]))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "read this list slowly. circle every value that makes something "
        "in your chest respond. don't think. feel.",
        s["ItalicNote"]
    ))
    story.append(Spacer(1, 8))

    values = [
        "creativity · honesty · freedom · loyalty · adventure · kindness",
        "security · humor · connection · courage · beauty · justice",
        "simplicity · family · growth · integrity · play · wisdom",
        "independence · generosity · curiosity · faith · health · service",
        "belonging · patience · authenticity · peace · love · craft",
        "resilience · nature · community · purpose · solitude · warmth",
    ]
    for row in values:
        story.append(Paragraph(row, s["BodyCenter"]))

    story.append(Spacer(1, 16))
    story.append(Paragraph("PART B: YOUR TOP 5", s["ExerciseLabel"]))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "from your circled words, choose the 5 that feel most essential. "
        "the ones you'd fight for.",
        s["ItalicNote"]
    ))
    story.append(Spacer(1, 8))

    for i in range(1, 6):
        story.append(NumberedCircle(i))
        story.append(WritingLines(CONTENT_W, num_lines=1, spacing=26))
        story.append(Spacer(1, 4))

    story.append(PageBreak())

    # Page 2: Values reflection
    story.append(Spacer(1, 16))
    story.append(Paragraph("PART C: LIVING YOUR VALUES", s["ExerciseLabel"]))
    story.append(Spacer(1, 10))

    build_prompt_page(story, s, "REFLECT",
        "when was the last time you lived one of your top 5 values — "
        "outside of work?",
        lines=7)

    build_prompt_page(story, s, "REFLECT",
        "which of your values did your last job honor? "
        "which did it quietly violate?",
        lines=7)
    story.append(PageBreak())

    # Page 3: Values + identity
    build_prompt_with_break(story, s, "DEEPER",
        "if you built your next chapter entirely around your top 5 values "
        "— not around a job title or salary — what might that look like? "
        "don't plan. just dream on paper.",
        lines=12)


# ── EXERCISE 3: 20 Things That Make Me, Me ──

def build_exercise_3(story, s):
    build_exercise_opener(story, s, "3", "20 things that<br/>make me, me",
        "the small, strange, specific things that no résumé<br/>"
        "would ever capture — but that make you, you.")

    story.append(Spacer(1, 16))
    story.append(Paragraph(
        "this exercise is deceptively simple. list 20 things about yourself that "
        "have nothing to do with your career. the weirder, the better. the more "
        "specific, the more true.",
        s["Body"]
    ))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "examples: I can identify birds by their calls. I always cry at the same "
        "part of the same movie. I make the best scrambled eggs anyone has ever tasted. "
        "I remember the exact shade of blue of the lake where I learned to swim.",
        s["ItalicNote"]
    ))
    story.append(Spacer(1, 12))

    for i in range(1, 11):
        story.append(Paragraph(f"<b>{i}.</b>", s["SmallLabel"]))
        story.append(WritingLines(CONTENT_W, num_lines=1, spacing=26))
        story.append(Spacer(1, 4))

    story.append(PageBreak())

    # Page 2: 11-20
    story.append(Spacer(1, 16))
    story.append(Paragraph("20 THINGS (CONTINUED)", s["ExerciseLabel"]))
    story.append(Spacer(1, 10))

    for i in range(11, 21):
        story.append(Paragraph(f"<b>{i}.</b>", s["SmallLabel"]))
        story.append(WritingLines(CONTENT_W, num_lines=1, spacing=26))
        story.append(Spacer(1, 4))

    story.append(Spacer(1, 16))
    story.append(HLine(CONTENT_W * 0.3, AMBER, 0.4))
    story.append(Spacer(1, 10))
    story.append(Paragraph(
        "read your list out loud. slowly. these are things no layoff, "
        "no restructuring, no algorithm can take from you.",
        s["ItalicCenter"]
    ))
    story.append(PageBreak())

    # Page 3: Reflection
    build_prompt_with_break(story, s, "REFLECT",
        "which item on your list surprised you? which one made you smile? "
        "which one do you wish more people knew about you?",
        lines=10)


# ── Body Check-In (between exercises 3 and 4) ──

def build_body_checkin(story, s):
    """Body check-in page — where do you hold your identity?"""
    story.append(Spacer(1, 16))
    story.append(Paragraph("body check-in", s["Heading"]))
    story.append(Spacer(1, 8))
    story.append(HLine(CONTENT_W, AMBER, 0.5))
    story.append(Spacer(1, 8))

    story.append(Paragraph(
        "your body has been carrying your identity crisis even if your "
        "mind hasn't named it yet. take a moment to check in.",
        s["Body"]
    ))
    story.append(Spacer(1, 6))

    areas = [
        ("JAW + TEETH", "are you clenching? when did that start?"),
        ("SHOULDERS + NECK", "are they up near your ears? what are they bracing for?"),
        ("CHEST + HEART", "tight? hollow? heavy? what is the feeling there?"),
        ("STOMACH + GUT", "knotted? empty? fluttering? what is it telling you?"),
        ("HANDS", "are they tense? open? what do they want to do?"),
    ]

    for area, prompt in areas:
        story.append(Paragraph(area, s["ExerciseLabel"]))
        story.append(Paragraph(prompt, s["ItalicNote"]))
        story.append(WritingLines(CONTENT_W, num_lines=2, spacing=24))
        story.append(Spacer(1, 4))

    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "take three slow breaths. in through the nose, out through the mouth. "
        "let your shoulders drop. you are safe right now.",
        s["ItalicCenter"]
    ))
    story.append(PageBreak())


# ── EXERCISE 4: The Origin Story ──

def build_exercise_4(story, s):
    build_exercise_opener(story, s, "4", "the origin story",
        "before any title found you,<br/>there was a person with a story.")

    story.append(Spacer(1, 16))
    story.append(Paragraph(
        "this exercise invites you to go back. not to your first job, "
        "but before that. to the version of you that existed before "
        "anyone gave you a title, a performance review, or a LinkedIn profile.",
        s["Body"]
    ))
    story.append(Spacer(1, 12))

    build_prompt_page(story, s, "REMEMBER",
        "what did you love doing as a child — the thing you did "
        "just because it made you feel alive? not for a grade, "
        "not for praise. just because.",
        lines=8)

    build_prompt_page(story, s, "REMEMBER",
        "what did people come to you for — even before you had "
        "any formal expertise? what did friends, family, or "
        "classmates naturally seek you out for?",
        lines=6)
    story.append(PageBreak())

    # Page 2
    build_prompt_page(story, s, "REMEMBER",
        "describe a moment when you felt fully yourself — a specific memory, "
        "as detailed as you can make it. where were you? what were you doing? "
        "who was there?",
        lines=10)

    build_prompt_page(story, s, "CONNECT",
        "what thread connects that childhood love, that natural gift, "
        "and that moment of feeling fully yourself? what does it tell "
        "you about who you are underneath all the titles?",
        lines=6)
    story.append(PageBreak())


# ── Grounding Practice (between exercises 4 and 5) ──

def build_grounding_practice(story, s):
    """A breathwork + grounding practice page."""
    story.append(Spacer(1, 20))
    story.append(Paragraph("a grounding practice", s["Heading"]))
    story.append(Spacer(1, 10))
    story.append(HLine(CONTENT_W, AMBER, 0.5))
    story.append(Spacer(1, 12))

    story.append(Paragraph(
        "before you move into the next exercise, take a moment to "
        "ground yourself. this practice takes about 2 minutes.",
        s["Body"]
    ))
    story.append(Spacer(1, 12))

    story.append(Paragraph("THE PHYSIOLOGICAL SIGH", s["ExerciseLabel"]))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "neuroscientist Andrew Huberman calls this the fastest "
        "way to calm your nervous system in real time:",
        s["ItalicNote"]
    ))
    story.append(Spacer(1, 8))

    steps = [
        "take a deep breath in through your nose.",
        "at the top, take a second short inhale (a quick sip of air).",
        "exhale slowly through your mouth — as long as you can.",
        "repeat 2-3 times.",
    ]
    for i, step in enumerate(steps, 1):
        story.append(NumberedCircle(i))
        story.append(Spacer(1, 2))
        story.append(Paragraph(step, s["Body"]))
        story.append(Spacer(1, 4))

    story.append(Spacer(1, 12))
    story.append(Paragraph("WHEN TO USE THIS", s["ExerciseLabel"]))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "before opening LinkedIn. before an interview. before an exercise "
        "in this workbook that feels heavy. anytime you notice your chest "
        "tightening or your jaw clenching.",
        s["Body"]
    ))

    story.append(Spacer(1, 16))
    story.append(Paragraph("AFTER THE PRACTICE", s["ExerciseLabel"]))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "what do you notice right now? where did the breath go in your body?",
        s["Prompt"]
    ))
    story.append(WritingLines(CONTENT_W, num_lines=5))
    story.append(PageBreak())


# ── EXERCISE 5: Composting the Old Identity ──

def build_exercise_5(story, s):
    build_exercise_opener(story, s, "5", "composting the<br/>old identity",
        "not everything from your old life needs to be thrown away.<br/>"
        "some of it can become soil for what grows next.")

    story.append(Spacer(1, 16))
    story.append(Paragraph(
        "composting is the act of taking what's finished and transforming it "
        "into something that nourishes new growth. your old professional "
        "identity isn't garbage. it's material.",
        s["Body"]
    ))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "this exercise asks you to sort through what you carried in your "
        "professional life and decide what stays, what goes, and what transforms.",
        s["Body"]
    ))
    story.append(Spacer(1, 16))

    # Three columns concept (stacked for simplicity)
    story.append(Paragraph("KEEP", s["ExerciseLabel"]))
    story.append(Paragraph(
        "skills, relationships, habits, or parts of your professional "
        "identity that are genuinely yours — that you want to carry forward.",
        s["ItalicNote"]
    ))
    story.append(Spacer(1, 6))
    story.append(WritingLines(CONTENT_W, num_lines=6))
    story.append(Spacer(1, 14))

    story.append(Paragraph("RELEASE", s["ExerciseLabel"]))
    story.append(Paragraph(
        "beliefs, habits, or expectations that belonged to the role, "
        "not to you. things you performed but never chose.",
        s["ItalicNote"]
    ))
    story.append(Spacer(1, 6))
    story.append(WritingLines(CONTENT_W, num_lines=6))
    story.append(PageBreak())

    # Page 2: Transform + reflection
    story.append(Spacer(1, 16))
    story.append(Paragraph("TRANSFORM", s["ExerciseLabel"]))
    story.append(Paragraph(
        "things that were part of your old identity that could become "
        "something new. the skill that served a company could serve "
        "a community. the discipline could become a creative practice.",
        s["ItalicNote"]
    ))
    story.append(Spacer(1, 6))
    story.append(WritingLines(CONTENT_W, num_lines=7))
    story.append(Spacer(1, 16))

    story.append(HLine(CONTENT_W * 0.3, AMBER, 0.4))
    story.append(Spacer(1, 12))

    build_prompt_page(story, s, "REFLECT",
        "what's the one thing in your 'release' list that you're still "
        "holding onto? why is it hard to let go?",
        lines=8)
    story.append(PageBreak())

    # Page 3: Goodbye letter
    story.append(Spacer(1, 16))
    story.append(Paragraph("A SHORT GOODBYE", s["ExerciseLabel"]))
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "write a short letter to your old professional identity. "
        "thank it for what it gave you. tell it what you're keeping. "
        "tell it what you're letting go.",
        s["Body"]
    ))
    story.append(Spacer(1, 10))
    story.append(Paragraph("dear [old title],", s["Prompt"]))
    story.append(Spacer(1, 4))
    story.append(WritingLines(CONTENT_W, num_lines=16))
    story.append(PageBreak())


# ── EXERCISE 6: Seeds of Who I'm Becoming ──

def build_exercise_6(story, s):
    build_exercise_opener(story, s, "6", "seeds of who<br/>I'm becoming",
        "you don't need to know where you're going.<br/>"
        "you just need to notice what's pulling you.")

    story.append(Spacer(1, 16))
    story.append(Paragraph(
        "this is not a career planning exercise. this is not about 'what's next.' "
        "this is about paying attention to the quiet signals your body and heart "
        "are already sending about who you might be becoming.",
        s["Body"]
    ))
    story.append(Spacer(1, 12))

    build_prompt_page(story, s, "NOTICE",
        "what are you curious about right now — even slightly? "
        "what articles do you save? what conversations make you lean in? "
        "what would you learn if nobody was watching?",
        lines=8)

    build_prompt_page(story, s, "NOTICE",
        "what kind of day makes you feel most like yourself? "
        "describe it: what time do you wake up? what do you do? "
        "who's around? what's the texture of the day?",
        lines=7)
    story.append(PageBreak())

    # Page 2
    build_prompt_page(story, s, "IMAGINE",
        "if money and job titles didn't exist — if everyone's basic needs "
        "were met — what would you spend your days doing?",
        lines=8)

    build_prompt_page(story, s, "IMAGINE",
        "write a tiny, imperfect vision of who you might be in one year. "
        "not a goal. not a plan. a feeling. what does the future version "
        "of you feel like from the inside?",
        lines=7)
    story.append(PageBreak())

    # Page 3: Planting
    story.append(Spacer(1, 16))
    story.append(Paragraph("PLANTING WITHOUT FORCING", s["ExerciseLabel"]))
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "choose one small seed from what you've written — one curiosity, "
        "one pull, one whisper of who you might become. write it below. "
        "then write one tiny action you could take this week to water it.",
        s["Body"]
    ))
    story.append(Spacer(1, 10))

    story.append(Paragraph("the seed:", s["SubHeading"]))
    story.append(WritingLines(CONTENT_W, num_lines=2, spacing=28))
    story.append(Spacer(1, 16))

    story.append(Paragraph("one small action to water it:", s["SubHeading"]))
    story.append(WritingLines(CONTENT_W, num_lines=2, spacing=28))
    story.append(Spacer(1, 20))

    story.append(Paragraph(
        '"I am planting seeds in uncertain soil. that is an act of faith."',
        s["AffirmationLight"]
    ))
    story.append(PageBreak())


# ── Permission Slip (between exercises 6 and 7) ──

def build_permission_slip(story, s):
    """Permission slip page — give yourself permission."""
    story.append(Spacer(1, 20))
    story.append(Paragraph("permission slip", s["Heading"]))
    story.append(Spacer(1, 10))
    story.append(HLine(CONTENT_W, LAVENDER, 0.6))
    story.append(Spacer(1, 12))

    story.append(Paragraph(
        "check the ones you need today. add your own at the bottom.",
        s["ItalicNote"]
    ))
    story.append(Spacer(1, 12))

    permissions = [
        "I have permission to not know what I want to be.",
        "I have permission to grieve a career that isn't dead yet.",
        "I have permission to introduce myself without a job title.",
        "I have permission to take a break from figuring it all out.",
        "I have permission to be proud of who I am right now.",
        "I have permission to change my mind about everything.",
        "I have permission to not apply to a single job today.",
        "I have permission to miss my old life without wanting it back.",
        "I have permission to feel afraid and still be brave.",
        "I have permission to take up space without a title to justify it.",
    ]

    for p in permissions:
        story.append(CheckboxLine(CONTENT_W))
        story.append(Spacer(1, 2))
        story.append(Paragraph(p, s["Body"]))
        story.append(Spacer(1, 6))

    story.append(Spacer(1, 10))
    story.append(Paragraph("WRITE YOUR OWN", s["ExerciseLabel"]))
    story.append(Spacer(1, 6))
    story.append(Paragraph("I have permission to...", s["Prompt"]))
    story.append(WritingLines(CONTENT_W, num_lines=3, spacing=28))
    story.append(PageBreak())


# ── EXERCISE 7: Letter to Your Future Self ──

def build_exercise_7(story, s):
    build_exercise_opener(story, s, "7", "letter to your<br/>future self",
        "write to the person you'll be in 90 days.<br/>"
        "they need to hear from you.")

    story.append(Spacer(1, 16))
    story.append(Paragraph(
        "you are going to write a letter to yourself — to the version "
        "of you that will exist 90 days from now. they will be someone "
        "slightly different from who you are today. they will have new "
        "experiences, new fears, new small victories.",
        s["Body"]
    ))
    story.append(Paragraph(
        "write to them with honesty and tenderness. tell them where you "
        "are right now. what you're afraid of. what you hope for. what "
        "you want them to remember about this moment.",
        s["Body"]
    ))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "when you're done, cut out the envelope on the last page of this "
        "workbook, fold your letter, seal it, and write the date to open it. "
        "put it somewhere you'll find it.",
        s["ItalicNote"]
    ))
    story.append(Spacer(1, 12))

    story.append(Paragraph("dear future me,", s["Prompt"]))
    story.append(Spacer(1, 4))
    story.append(WritingLines(CONTENT_W, num_lines=18))
    story.append(PageBreak())

    # Page 2: continuation
    story.append(Spacer(1, 16))
    story.append(Paragraph("LETTER (CONTINUED)", s["ExerciseLabel"]))
    story.append(Spacer(1, 10))
    story.append(WritingLines(CONTENT_W, num_lines=20))
    story.append(Spacer(1, 16))

    story.append(Paragraph("with love,", s["Prompt"]))
    story.append(Spacer(1, 4))
    story.append(WritingLines(CONTENT_W, num_lines=1, spacing=28))
    story.append(Spacer(1, 8))
    story.append(Paragraph("date: _______________", s["Body"]))
    story.append(PageBreak())


# ── EXERCISE 8: The Declaration ──

def build_exercise_8(story, s):
    build_exercise_opener(story, s, "8", "the declaration",
        "read these slowly. underline the ones that feel true.<br/>"
        "then write your own.")

    story.append(Spacer(1, 16))
    story.append(Paragraph("affirmations for identity reclamation", s["SubHeading"]))
    story.append(Spacer(1, 12))

    affirmations = [
        "I am more than my output. I am the meaning behind it.",
        "my worth was never measured in speed. it is measured in depth.",
        "I am not obsolete. I am evolving.",
        "no algorithm will ever understand what it feels like to be me.",
        "I refuse to shrink myself to fit inside a comparison with technology.",
        "my story cannot be generated. it can only be lived.",
        "I am not defined by the tools I use. I am defined by the decisions I make.",
        "the future needs me whole, not optimized.",
        "I was built for uncertainty. I have navigated it my entire life.",
        "my humanity is not a limitation. it is the entire point.",
    ]

    for aff in affirmations:
        story.append(AccentDot(AMBER, size=5))
        story.append(Spacer(1, 2))
        story.append(Paragraph(f'"{aff}"', s["Affirmation"]))
        story.append(Spacer(1, 6))

    story.append(PageBreak())

    # Page 2: Write your own
    story.append(Spacer(1, 16))
    story.append(Paragraph("NOW WRITE YOUR OWN", s["ExerciseLabel"]))
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "using what you've uncovered in this workbook — your roles, your values, "
        "your 20 things, your origin story, your seeds — write 3 declarations "
        "about who you are. not who you were. not who you should be. who you are.",
        s["Body"]
    ))
    story.append(Spacer(1, 12))

    for i in range(1, 4):
        story.append(Paragraph(f"DECLARATION {i}", s["ExerciseLabel"]))
        story.append(Spacer(1, 6))
        story.append(WritingLines(CONTENT_W, num_lines=3, spacing=28))
        story.append(Spacer(1, 16))

    story.append(Spacer(1, 10))
    story.append(Paragraph(
        "say them out loud. say them again. these are yours.",
        s["ItalicCenter"]
    ))
    story.append(PageBreak())


# ── Closing Page ──

def build_closing(story, s):
    story.append(Spacer(1, 80))
    story.append(Paragraph(
        "you finished.",
        s["Heading"]
    ))
    story.append(Spacer(1, 16))
    story.append(HLine(CONTENT_W * 0.3, AMBER, 0.6))
    story.append(Spacer(1, 20))
    story.append(Paragraph(
        "not because someone told you to. not for a grade or a metric "
        "or a performance review. you did this because some part of you "
        "needed to remember who you are.",
        s["BodyCenter"]
    ))
    story.append(Spacer(1, 12))
    story.append(Paragraph(
        "that part of you — the part that seeks, that questions, "
        "that refuses to be reduced to a title — that part is the answer "
        "to the question this workbook asks.",
        s["BodyCenter"]
    ))
    story.append(Spacer(1, 20))
    story.append(Paragraph(
        '"the question is not whether AI can do what I do.<br/>'
        'the question is whether it can be who I am."',
        s["Affirmation"]
    ))
    story.append(Spacer(1, 30))
    story.append(AccentDot(AMBER))
    story.append(Spacer(1, 20))
    story.append(Paragraph(
        "if this workbook helped you, there's more.",
        s["BodyCenter"]
    ))
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        '"the in-between" — a 90-page guided journal for navigating<br/>'
        "the full journey of identity, grief, and rebuilding.",
        s["ItalicCenter"]
    ))
    story.append(Spacer(1, 8))
    story.append(Paragraph("luminouspulse.co", s["CTA"]))
    story.append(PageBreak())


# ── Notes Pages ──

def build_notes(story, s, num_pages=2):
    """Blank journaling pages."""
    for i in range(num_pages):
        story.append(Spacer(1, 20))
        if i == 0:
            story.append(Paragraph("notes", s["Heading"]))
            story.append(Spacer(1, 10))
            story.append(HLine(CONTENT_W * 0.3, LIGHT_GRAY, 0.3))
            story.append(Spacer(1, 12))
        else:
            story.append(Spacer(1, 16))
        story.append(WritingLines(CONTENT_W, num_lines=22))
        story.append(PageBreak())


# ── Envelope Template ──

def build_envelope(story, s):
    story.append(Spacer(1, 30))
    story.append(Paragraph("the envelope", s["Heading"]))
    story.append(Spacer(1, 10))
    story.append(Paragraph(
        "cut along the dashed line. fold your letter from exercise 7. "
        "place it inside. seal with tape or wax. write the date you'll open it. "
        "put it somewhere safe — a drawer, a book, taped to your mirror.",
        s["Body"]
    ))
    story.append(Spacer(1, 20))
    story.append(EnvelopeTemplate(CONTENT_W, height=220))
    story.append(Spacer(1, 30))

    # Second envelope (in case they want a spare)
    story.append(Paragraph(
        "spare envelope (or write a second letter to someone you trust):",
        s["ItalicNote"]
    ))
    story.append(Spacer(1, 14))
    story.append(EnvelopeTemplate(CONTENT_W, height=220))
    story.append(PageBreak())


# ── Main ──

def build_workbook():
    out_path = os.path.join(os.path.dirname(__file__),
                            "Who-Am-I-Without-The-Title-Workbook.pdf")

    doc = SimpleDocTemplate(
        out_path,
        pagesize=letter,
        leftMargin=MARGIN, rightMargin=MARGIN,
        topMargin=MARGIN, bottomMargin=MARGIN,
        title="who am I without the title?",
        author="Luminous Pulse · luminouspulse.co",
    )

    s = create_styles()
    story = []

    # Cover (navy background)
    build_cover(story, s)

    # Intro page
    build_intro(story, s)

    # Table of contents
    build_toc(story, s)

    # Exercises 1-8 with interludes
    build_exercise_1(story, s)
    build_exercise_2(story, s)
    build_exercise_3(story, s)
    build_body_checkin(story, s)
    build_exercise_4(story, s)
    build_grounding_practice(story, s)
    build_exercise_5(story, s)
    build_exercise_6(story, s)
    build_permission_slip(story, s)
    build_exercise_7(story, s)
    build_exercise_8(story, s)

    # Closing
    build_closing(story, s)

    # Notes
    build_notes(story, s, num_pages=2)

    # Envelope template
    build_envelope(story, s)

    # Build with page templates
    doc.build(story, onFirstPage=draw_bg_cover, onLaterPages=draw_bg)

    # Report
    file_size = os.path.getsize(out_path) / (1024 * 1024)
    print(f"\n{'='*50}")
    print(f"  who am I without the title? — workbook generated")
    print(f"  {out_path}")
    print(f"  {file_size:.1f} MB")
    print(f"{'='*50}\n")

    # Count pages (approximate from story)
    page_breaks = sum(1 for item in story if isinstance(item, PageBreak))
    print(f"  approximate pages: {page_breaks + 1}")


if __name__ == "__main__":
    build_workbook()
