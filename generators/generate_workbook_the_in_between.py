#!/usr/bin/env python3
"""Generate "the in-between" workbook PDF — Luminous Pulse flagship product ($27).

a guided journal for the space between who you were and who you're becoming.

Design: Printable on cream/off-white background. Navy + amber accents.
Generous margins for comfortable handwriting. Writing lines where needed.
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import HexColor, Color
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
MARGIN = 0.85 * inch  # generous margins for printing + binding
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
    """A line with a small checkbox at the start — for permission slips."""
    def __init__(self, width, color=LINE_COLOR):
        Flowable.__init__(self)
        self.line_width = width
        self.color = color

    def draw(self):
        self.canv.setStrokeColor(NAVY_LIGHT)
        self.canv.setLineWidth(0.6)
        # Checkbox
        self.canv.rect(0, 2, 10, 10, fill=0, stroke=1)
        # Line
        self.canv.setStrokeColor(self.color)
        self.canv.setLineWidth(0.4)
        self.canv.line(18, 0, self.line_width, 0)

    def wrap(self, availWidth, availHeight):
        return (self.line_width, 16)


class NavyPageBg(Flowable):
    """Paints the current page navy (for section openers).

    Must be placed right after a PageBreak so it's at the top of a fresh page.
    The draw origin after PageBreak is at (MARGIN, PAGE_H - MARGIN) in page coords.
    """
    def __init__(self):
        Flowable.__init__(self)

    def draw(self):
        self.canv.saveState()
        self.canv.setFillColor(NAVY)
        # Overshoot by 20pt to ensure full coverage at all edges
        overshoot = 20
        self.canv.rect(
            -MARGIN - overshoot,
            -(PAGE_H - MARGIN) - overshoot,
            PAGE_W + 2 * overshoot,
            PAGE_H + 2 * overshoot,
            fill=1, stroke=0
        )
        # Thin amber line near page bottom
        y_line = -(PAGE_H - MARGIN) + 60
        self.canv.setStrokeColor(AMBER)
        self.canv.setLineWidth(0.8)
        self.canv.line(0, y_line, CONTENT_W, y_line)
        self.canv.restoreState()

    def wrap(self, availWidth, availHeight):
        return (0, 0)  # takes no space in the flow


# ── Page Backgrounds ──

def draw_bg(canvas, doc):
    """Standard page background — cream with subtle footer."""
    canvas.saveState()
    canvas.setFillColor(CREAM)
    canvas.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    # Footer
    canvas.setFont("Helvetica", 7)
    canvas.setFillColor(SOFT_GRAY)
    canvas.drawCentredString(PAGE_W / 2, 30, "the in-between  ·  luminouspulse.co")
    # Page number
    page_num = canvas.getPageNumber()
    if page_num > 2:  # skip cover + inside cover
        canvas.drawRightString(PAGE_W - MARGIN, 30, str(page_num))
    canvas.restoreState()


def draw_bg_cover(canvas, doc):
    """Cover page — navy background."""
    canvas.saveState()
    canvas.setFillColor(NAVY)
    canvas.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    canvas.restoreState()


def draw_bg_section(canvas, doc):
    """Section opener — navy background with amber accent."""
    canvas.saveState()
    canvas.setFillColor(NAVY)
    canvas.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    # Thin amber line at bottom
    canvas.setStrokeColor(AMBER)
    canvas.setLineWidth(0.8)
    canvas.line(MARGIN, 60, PAGE_W - MARGIN, 60)
    canvas.restoreState()


# ── Styles ──

def create_styles():
    styles = getSampleStyleSheet()

    # Cover styles (on navy)
    styles.add(ParagraphStyle(
        name="CoverTitle", fontName="Helvetica-Bold", fontSize=36,
        textColor=WHITE, alignment=TA_CENTER, leading=44, spaceAfter=16,
    ))
    styles.add(ParagraphStyle(
        name="CoverSub", fontName="Helvetica-Oblique", fontSize=14,
        textColor=LAVENDER, alignment=TA_CENTER, leading=20, spaceAfter=8,
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
        name="SectionTitle", fontName="Helvetica-Bold", fontSize=28,
        textColor=WHITE, alignment=TA_CENTER, leading=36, spaceAfter=20,
    ))
    styles.add(ParagraphStyle(
        name="SectionEpigraph", fontName="Helvetica-Oblique", fontSize=12,
        textColor=LAVENDER, alignment=TA_CENTER, leading=18, spaceAfter=8,
        leftIndent=40, rightIndent=40,
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
        name="PromptLabel", fontName="Helvetica-Bold", fontSize=10,
        textColor=AMBER_SOFT, alignment=TA_LEFT, leading=14, spaceAfter=4,
        letterSpacing=2,
    ))
    styles.add(ParagraphStyle(
        name="Prompt", fontName="Helvetica-Oblique", fontSize=12,
        textColor=NAVY, alignment=TA_LEFT, leading=18, spaceAfter=12,
        leftIndent=4,
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
        name="Affirmation", fontName="Helvetica-Bold", fontSize=16,
        textColor=NAVY, alignment=TA_CENTER, leading=22, spaceAfter=16,
        leftIndent=20, rightIndent=20,
    ))
    styles.add(ParagraphStyle(
        name="AffirmationLight", fontName="Helvetica-Oblique", fontSize=14,
        textColor=NAVY_LIGHT, alignment=TA_CENTER, leading=20, spaceAfter=12,
        leftIndent=20, rightIndent=20,
    ))
    styles.add(ParagraphStyle(
        name="SmallLabel", fontName="Helvetica", fontSize=8,
        textColor=SOFT_GRAY, alignment=TA_LEFT, leading=12, spaceAfter=4,
        letterSpacing=1,
    ))
    styles.add(ParagraphStyle(
        name="PermissionText", fontName="Helvetica", fontSize=11,
        textColor=NAVY, alignment=TA_LEFT, leading=16, spaceAfter=6,
        leftIndent=22,
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
        name="MicroPractice", fontName="Helvetica", fontSize=10,
        textColor=HexColor("#444444"), alignment=TA_LEFT, leading=15, spaceAfter=6,
        leftIndent=12, bulletIndent=4,
    ))

    return styles


# ── Page Builders ──

def build_cover(story, s):
    """Cover page — navy background."""
    story.append(Spacer(1, 180))

    # Logo if available
    logo_path = os.path.join(os.path.dirname(__file__), "logo-abstract-sanctuary-transparent.png")
    if os.path.exists(logo_path):
        img = Image(logo_path, width=140, height=74)
        img.hAlign = "CENTER"
        story.append(img)
        story.append(Spacer(1, 40))

    story.append(Paragraph("the in-between", s["CoverTitle"]))
    story.append(Spacer(1, 12))
    story.append(Paragraph(
        "a guided journal for the space between<br/>"
        "who you were and who you're becoming.",
        s["CoverSub"]
    ))
    story.append(Spacer(1, 80))
    story.append(Paragraph("Luminous Pulse", s["CoverFooter"]))
    story.append(Paragraph("luminouspulse.co", s["CoverFooter"]))
    story.append(PageBreak())


def build_design_philosophy(story, s):
    """Why this is a printable workbook."""
    story.append(Spacer(1, 60))
    story.append(Paragraph("before you begin", s["Heading"]))
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "this workbook was designed to be printed and written in by hand.",
        s["Body"]
    ))
    story.append(Paragraph(
        "not because we're against technology — but because neuroscience shows "
        "that the physical act of writing activates emotional processing centers "
        "in your brain that typing simply cannot reach.",
        s["Body"]
    ))
    story.append(Paragraph(
        "when you're processing grief, uncertainty, or identity shifts, "
        "your hands need to be part of the conversation.",
        s["Body"]
    ))
    story.append(Spacer(1, 16))
    story.append(HLine(CONTENT_W, LIGHT_GRAY))
    story.append(Spacer(1, 16))

    story.append(Paragraph("how to use this workbook", s["SubHeading"]))
    story.append(Spacer(1, 4))

    instructions = [
        "print it. the whole thing, or one section at a time.",
        "find a pen you like. not a fancy one. just one that feels good.",
        "there is no right pace. one page a day. one page a week. whatever you have.",
        "the prompts are invitations, not assignments. skip what doesn't resonate.",
        "the body check-ins matter. your body is holding things your mind hasn't processed yet.",
        "the writing lines are suggestions. write in the margins. draw. scratch things out.",
        "you do not need to finish this to benefit from it.",
    ]
    for inst in instructions:
        story.append(Paragraph(
            f'<font color="{AMBER_SOFT.hexval()}">—</font>  {inst}',
            s["Body"]
        ))

    story.append(Spacer(1, 20))
    story.append(Paragraph(
        "the feeling follows the writing. not the other way around.",
        s["AffirmationLight"]
    ))
    story.append(PageBreak())


def build_table_of_contents(story, s):
    """Table of contents."""
    story.append(Spacer(1, 40))
    story.append(Paragraph("contents", s["Heading"]))
    story.append(Spacer(1, 14))

    sections = [
        ("one", "letting go", "acknowledging what was lost"),
        ("two", "sitting with", "being present with discomfort"),
        ("three", "uncovering", "discovering what remains"),
        ("four", "planting", "experimenting with new possibilities"),
        ("five", "tending", "nurturing what's growing"),
        ("six", "emerging", "stepping into who you're becoming"),
    ]

    for num, title, sub in sections:
        story.append(Paragraph(
            f'<font color="{AMBER_SOFT.hexval()}" size="9">{num.upper()}</font>',
            s["SmallLabel"]
        ))
        story.append(Paragraph(title, s["SubHeading"]))
        story.append(Paragraph(sub, s["ItalicNote"]))
        story.append(Spacer(1, 4))

    story.append(Spacer(1, 10))
    story.append(HLine(CONTENT_W, LIGHT_GRAY))
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        f'<font color="{AMBER_SOFT.hexval()}" size="9">CLOSING</font>',
        s["SmallLabel"]
    ))
    story.append(Paragraph("a letter to your future self", s["SubHeading"]))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        f'<font color="{AMBER_SOFT.hexval()}" size="9">APPENDIX</font>',
        s["SmallLabel"]
    ))
    story.append(Paragraph("printable affirmation cards", s["SubHeading"]))
    story.append(PageBreak())


def build_section_opener(story, s, num, title, epigraph):
    """Full-page section opener on navy background."""
    story.append(NavyPageBg())
    story.append(Spacer(1, 200))
    story.append(Paragraph(num.upper(), s["SectionNum"]))
    story.append(Paragraph(title, s["SectionTitle"]))
    story.append(Spacer(1, 24))
    story.append(Paragraph(epigraph, s["SectionEpigraph"]))
    story.append(PageBreak())


def build_prompt_page(story, s, label, prompt, instruction=None, lines=9):
    """A journaling prompt page with writing lines."""
    story.append(Spacer(1, 30))
    story.append(Paragraph(label.upper(), s["PromptLabel"]))
    story.append(Spacer(1, 4))
    story.append(Paragraph(prompt, s["Prompt"]))

    if instruction:
        story.append(Paragraph(instruction, s["ItalicNote"]))

    story.append(Spacer(1, 12))
    story.append(WritingLines(CONTENT_W, num_lines=lines, spacing=26))
    story.append(PageBreak())


def build_body_checkin(story, s, intro=None):
    """Body check-in page — where do you feel it?"""
    story.append(Spacer(1, 30))
    story.append(Paragraph("BODY CHECK-IN", s["PromptLabel"]))
    story.append(Spacer(1, 8))

    if intro:
        story.append(Paragraph(intro, s["Body"]))
        story.append(Spacer(1, 8))

    story.append(Paragraph(
        "close your eyes for 30 seconds. scan from head to toe. "
        "where do you notice tension, heaviness, or holding?",
        s["Prompt"]
    ))
    story.append(Spacer(1, 8))

    body_areas = [
        ("head / jaw", "what are you clenching?"),
        ("throat / chest", "what are you holding back?"),
        ("stomach", "what are you carrying?"),
        ("shoulders / back", "what are you bracing for?"),
        ("hands / feet", "where are you gripping?"),
    ]

    for area, question in body_areas:
        story.append(Paragraph(
            f'<font color="{AMBER_SOFT.hexval()}"><b>{area}</b></font>  '
            f'<font color="{SOFT_GRAY.hexval()}">{question}</font>',
            s["Body"]
        ))
        story.append(WritingLines(CONTENT_W, num_lines=2, spacing=24))
        story.append(Spacer(1, 4))

    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "what does your body need right now? (movement, stillness, warmth, cold, touch, space?)",
        s["ItalicNote"]
    ))
    story.append(WritingLines(CONTENT_W, num_lines=2, spacing=24))
    story.append(PageBreak())


def build_permission_slip(story, s, permissions, closing=None):
    """Permission slip page with checkboxes."""
    story.append(Spacer(1, 30))
    story.append(Paragraph("PERMISSION SLIP", s["PromptLabel"]))
    story.append(Spacer(1, 8))
    story.append(Paragraph("you are allowed to:", s["Prompt"]))
    story.append(Spacer(1, 12))

    for p in permissions:
        story.append(CheckboxLine(CONTENT_W))
        story.append(Paragraph(p, s["PermissionText"]))
        story.append(Spacer(1, 6))

    # Blank ones for them to write their own
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "write your own:",
        s["ItalicNote"]
    ))
    for _ in range(3):
        story.append(CheckboxLine(CONTENT_W))
        story.append(Spacer(1, 16))

    if closing:
        story.append(Spacer(1, 12))
        story.append(Paragraph(closing, s["AffirmationLight"]))

    story.append(PageBreak())


def build_micro_experiment(story, s, title, experiments):
    """Micro-experiment page — small offline actions."""
    story.append(Spacer(1, 30))
    story.append(Paragraph("MICRO-EXPERIMENT", s["PromptLabel"]))
    story.append(Spacer(1, 8))
    story.append(Paragraph(title, s["SubHeading"]))
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "choose one. do it before you open this workbook again. "
        "then write what happened.",
        s["ItalicNote"]
    ))
    story.append(Spacer(1, 12))

    for exp in experiments:
        story.append(Paragraph(
            f'<font color="{AMBER_SOFT.hexval()}">◻</font>  {exp}',
            s["Body"]
        ))

    story.append(Spacer(1, 16))
    story.append(Paragraph("what happened:", s["PromptLabel"]))
    story.append(Spacer(1, 4))
    story.append(WritingLines(CONTENT_W, num_lines=8, spacing=26))
    story.append(PageBreak())


def build_affirmation_page(story, s, affirmation, sub=None):
    """Full-page affirmation — centered, breathing room."""
    story.append(Spacer(1, 220))
    story.append(Paragraph(f'"{affirmation}"', s["Affirmation"]))
    if sub:
        story.append(Spacer(1, 8))
        story.append(Paragraph(sub, s["ItalicCenter"]))
    story.append(PageBreak())


def build_breathwork_page(story, s, title, instructions, when_to_use=None):
    """A guided breathwork practice page."""
    story.append(Spacer(1, 30))
    story.append(Paragraph("BREATHWORK PRACTICE", s["PromptLabel"]))
    story.append(Spacer(1, 8))
    story.append(Paragraph(title, s["SubHeading"]))
    story.append(Spacer(1, 8))

    for step in instructions:
        story.append(Paragraph(
            f'<font color="{AMBER_SOFT.hexval()}">—</font>  {step}',
            s["Body"]
        ))

    if when_to_use:
        story.append(Spacer(1, 12))
        story.append(Paragraph(
            f'<font color="{AMBER_SOFT.hexval()}"><b>when to use this:</b></font> {when_to_use}',
            s["Body"]
        ))

    story.append(Spacer(1, 16))
    story.append(Paragraph("how did it feel?", s["PromptLabel"]))
    story.append(Spacer(1, 4))
    story.append(WritingLines(CONTENT_W, num_lines=5, spacing=26))
    story.append(PageBreak())


def build_gratitude_page(story, s, intro):
    """A gratitude / noticing page."""
    story.append(Spacer(1, 30))
    story.append(Paragraph("WHAT I NOTICE", s["PromptLabel"]))
    story.append(Spacer(1, 8))
    story.append(Paragraph(intro, s["Prompt"]))
    story.append(Spacer(1, 12))

    prompts = [
        "one thing I'm grateful for today (it can be small):",
        "one thing I did well this week (not at work — in life):",
        "one thing I noticed about myself that surprised me:",
        "one thing I want to carry forward:",
    ]
    for p in prompts:
        story.append(Paragraph(
            f'<font color="{AMBER_SOFT.hexval()}"><b>{p}</b></font>',
            s["Body"]
        ))
        story.append(WritingLines(CONTENT_W, num_lines=3, spacing=24))
        story.append(Spacer(1, 4))

    story.append(PageBreak())


# ── Section Content ──

def build_section_one(story, s):
    """Section 1: Letting Go — acknowledging what was lost."""
    build_section_opener(story, s, "one", "letting go",
        "you cannot grieve what you refuse to name.")

    # Prompt 1
    build_prompt_page(story, s,
        "PROMPT",
        "what did you lose — beyond the job title? name every piece. "
        "the routine. the people. the identity. the plan.",
        "don't rush. let each one land before moving to the next.",
        lines=10
    )

    # Prompt 2
    build_prompt_page(story, s,
        "PROMPT",
        "what were you in the middle of when it ended? "
        "what project, relationship, or growth trajectory got interrupted?",
        lines=9
    )

    # Body check-in
    build_body_checkin(story, s,
        "grief lives in the body before the mind can name it. "
        "let's find where yours is sitting."
    )

    # Prompt 3
    build_prompt_page(story, s,
        "PROMPT",
        "write a letter to the version of you who still had the job. "
        "what would you say to them? what do you wish they knew?",
        "you don't have to send it. you just have to write it.",
        lines=10
    )

    # Prompt 4
    build_prompt_page(story, s,
        "PROMPT",
        "what are you pretending is fine that isn't? what truth have you been "
        "smiling through?",
        lines=9
    )

    # Breathwork
    build_breathwork_page(story, s,
        "the physiological sigh",
        [
            "inhale deeply through your nose.",
            "at the top, take one more short inhale (a double inhale).",
            "exhale long and slow through your mouth.",
            "repeat 3 times.",
            "this is the fastest way to calm your nervous system — "
            "one cycle takes 10 seconds.",
        ],
        "when grief hits suddenly. when the news is bad. when your chest tightens."
    )

    # Deeper prompt
    build_prompt_page(story, s,
        "PROMPT",
        "what parts of your identity were tangled up in the job? "
        "the title, the team, the routine, the recognition? "
        "name them separately. they are not all the same loss.",
        lines=9
    )

    # Permission slip
    build_permission_slip(story, s, [
        "grieve a job, even if you weren't happy there.",
        "feel angry about how it happened.",
        "not be 'over it' yet.",
        "stop performing recovery for other people.",
        "let the loss be as big as it actually is.",
    ], "this permission does not expire.")

    # Affirmation
    build_affirmation_page(story, s,
        "I do not need to be over this. I need to be honest about it.",
        "say it out loud. say it again. let it settle."
    )

    # Micro-experiment
    build_micro_experiment(story, s,
        "one small act of letting go", [
            "unfollow one LinkedIn account that makes you feel behind.",
            "delete one draft job application that felt forced.",
            "say out loud: 'I am not where I was. that's allowed.'",
            "put your work lanyard / badge in a drawer. not the trash. just a drawer.",
            "tell one person the truth when they ask how you're doing.",
        ]
    )

    # Closing prompt
    build_prompt_page(story, s,
        "BEFORE YOU MOVE ON",
        "what did you learn about yourself in this section? "
        "what surprised you? what felt hard to write?",
        lines=8
    )


def build_section_two(story, s):
    """Section 2: Sitting With — being present with discomfort."""
    build_section_opener(story, s, "two", "sitting with",
        "the antidote to this feeling is not more information. it is presence.")

    # Prompt 1
    build_prompt_page(story, s,
        "PROMPT",
        "what does uncertainty feel like in your body? describe it like you're "
        "describing weather. is it a storm? a fog? a held breath?",
        lines=9
    )

    # Prompt 2
    build_prompt_page(story, s,
        "PROMPT",
        "what are you most afraid of? not the reasonable fear. the 3am fear. "
        "the one you don't say out loud.",
        "naming the fear is not the same as making it real. naming it is how you make it smaller.",
        lines=9
    )

    # Body check-in
    build_body_checkin(story, s,
        "anxiety is not just a thought. it's a physical event. "
        "let's notice what it's doing right now."
    )

    # Grounding practice
    story.append(Spacer(1, 30))
    story.append(Paragraph("GROUNDING PRACTICE", s["PromptLabel"]))
    story.append(Spacer(1, 8))
    story.append(Paragraph("the 5-4-3-2-1 method", s["SubHeading"]))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "when the spiral hits, anchor yourself here. name:",
        s["Body"]
    ))

    senses = [
        ("5 things you can see", 2),
        ("4 things you can touch", 2),
        ("3 things you can hear", 2),
        ("2 things you can smell", 1),
        ("1 thing you can taste", 1),
    ]
    for sense, lines in senses:
        story.append(Paragraph(
            f'<font color="{AMBER_SOFT.hexval()}"><b>{sense}</b></font>',
            s["Body"]
        ))
        story.append(WritingLines(CONTENT_W, num_lines=lines, spacing=24))
        story.append(Spacer(1, 4))

    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "return to this page whenever you need it. it doesn't expire.",
        s["ItalicNote"]
    ))
    story.append(PageBreak())

    # Prompt 3
    build_prompt_page(story, s,
        "PROMPT",
        "what would you do today if you weren't waiting for the anxiety to go away first?",
        lines=9
    )

    # Prompt 4
    build_prompt_page(story, s,
        "PROMPT",
        "write about a time you sat with something difficult and came through it. "
        "not because you fixed it — because you stayed.",
        lines=9
    )

    # Breathwork
    build_breathwork_page(story, s,
        "box breathing (4-4-4-4)",
        [
            "inhale through your nose for 4 counts.",
            "hold for 4 counts.",
            "exhale through your mouth for 4 counts.",
            "hold (lungs empty) for 4 counts.",
            "repeat for 4-5 rounds.",
            "Navy SEALs use this before high-stakes situations. "
            "you can use it before anything that scares you.",
        ],
        "before interviews. before hard conversations. when the 3am spiral hits."
    )

    # Deeper prompt
    build_prompt_page(story, s,
        "PROMPT",
        "what would you say to a friend who was going through exactly "
        "what you're going through? write it down. then read it back to yourself.",
        "we are always kinder to others than to ourselves. practice receiving that kindness.",
        lines=9
    )

    # Permission slip
    build_permission_slip(story, s, [
        "not have a plan yet.",
        "say 'I don't know' when people ask what's next.",
        "close LinkedIn and go outside.",
        "feel the full weight of this without rushing to 'move on.'",
        "take longer than you thought you would.",
    ], "you are not behind. you are in the middle.")

    # Affirmation
    build_affirmation_page(story, s,
        "I do not need to solve the future today. I just need to be here now.")

    # Micro-experiment
    build_micro_experiment(story, s,
        "one small act of presence", [
            "sit somewhere for 10 minutes without your phone.",
            "eat one meal without a screen.",
            "take a walk with no destination and no podcast.",
            "write a list of 5 things that are true right now (not projections about the future).",
            "put your hand on your chest and say: 'I am here. this is enough.'",
        ]
    )

    # Closing prompt
    build_prompt_page(story, s,
        "BEFORE YOU MOVE ON",
        "what is it like to stop running from this feeling? "
        "what happens when you let it be here without fixing it?",
        lines=8
    )


def build_section_three(story, s):
    """Section 3: Uncovering — discovering what remains."""
    build_section_opener(story, s, "three", "uncovering",
        "underneath the job title, the anxiety, the grief — something remains. "
        "something that was here before all of this.")

    # Prompt 1
    build_prompt_page(story, s,
        "PROMPT",
        "make a list of 20 things that make you who you are — "
        "and none of them can be job-related.",
        "this is harder than it sounds. stay with it.",
        lines=12
    )

    # Prompt 2
    build_prompt_page(story, s,
        "PROMPT",
        "who were you at 8 years old? what did you love? what made you forget time? "
        "what made you feel alive?",
        lines=9
    )

    # Values excavation
    story.append(Spacer(1, 30))
    story.append(Paragraph("VALUES EXCAVATION", s["PromptLabel"]))
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "circle the 10 values that feel most true to you right now. "
        "then narrow to 5. then to 3.",
        s["Body"]
    ))
    story.append(Spacer(1, 8))

    values_list = [
        "autonomy · belonging · creativity · curiosity · depth",
        "fairness · family · freedom · generosity · growth",
        "honesty · humor · independence · integrity · justice",
        "kindness · knowledge · leadership · love · loyalty",
        "meaning · nature · order · patience · peace",
        "play · presence · purpose · reliability · resilience",
        "rest · security · service · simplicity · solitude",
        "spirituality · stability · strength · tenderness · trust",
        "truth · warmth · wholeness · wisdom · wonder",
    ]
    for row in values_list:
        story.append(Paragraph(row, s["BodyCenter"]))

    story.append(Spacer(1, 16))
    story.append(Paragraph("my 3 core values right now:", s["SubHeading"]))
    story.append(WritingLines(CONTENT_W, num_lines=3, spacing=28))
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "how would your days look different if these 3 values led your decisions?",
        s["Prompt"]
    ))
    story.append(WritingLines(CONTENT_W, num_lines=4, spacing=26))
    story.append(PageBreak())

    # Body check-in
    build_body_checkin(story, s,
        "you've been excavating. that stirs things up. "
        "let's check what your body is doing."
    )

    # Prompt 3
    build_prompt_page(story, s,
        "PROMPT",
        "what are 3 things you do well that have nothing to do with "
        "your industry, your tools, or your resume?",
        "think about what people come to you for outside of work.",
        lines=9
    )

    # Prompt 4
    build_prompt_page(story, s,
        "PROMPT",
        "if no one would ever see it and no one could judge it — "
        "what would you make? write? build? try?",
        lines=9
    )

    # Breathwork
    build_breathwork_page(story, s,
        "butterfly hug (bilateral stimulation)",
        [
            "cross your arms over your chest, fingertips resting below your collarbones.",
            "interlock your thumbs — your hands form butterfly wings.",
            "close or soften your eyes.",
            "alternately tap your hands against your chest, like a butterfly flapping.",
            "breathe slowly. focus on a safe memory or simply notice what comes up.",
            "continue for 1-3 minutes.",
            "developed for hurricane survivors. now used for processing loss of any kind.",
        ],
        "when identity feels shaky. when the 'who am I now?' question feels too big."
    )

    # Noticing page
    build_gratitude_page(story, s,
        "you've been digging. let's surface for a moment and notice what's here."
    )

    # Permission slip
    build_permission_slip(story, s, [
        "be someone beyond your job title.",
        "not know what you want to do next.",
        "want something different from what you had.",
        "admit that you were more than your output.",
        "rediscover parts of yourself you buried for the career.",
    ], "who you are is not what you do. it never was.")

    # Affirmation
    build_affirmation_page(story, s,
        "I carry things no technology will ever replicate: "
        "lived experience, empathy, and purpose.")

    # Micro-experiment
    build_micro_experiment(story, s,
        "one small act of uncovering", [
            "do something you loved at age 12. for 20 minutes. no judgment.",
            "ask someone who knows you well: 'what's the thing about me that has nothing to do with work?'",
            "write a bio for yourself that doesn't mention your career.",
            "cook something from scratch without a recipe.",
            "spend an hour on something that has no productive value. just for the joy of it.",
        ]
    )

    # Closing prompt
    build_prompt_page(story, s,
        "BEFORE YOU MOVE ON",
        "what did you find that surprised you? what was already here "
        "that you had forgotten about?",
        lines=8
    )


def build_section_four(story, s):
    """Section 4: Planting — experimenting with new possibilities."""
    build_section_opener(story, s, "four", "planting",
        "you don't need to know what grows. you just need to put something in the soil.")

    # Prompt 1
    build_prompt_page(story, s,
        "PROMPT",
        "if money and judgment weren't factors, name 5 things you'd be curious "
        "to try. not commit to. just try.",
        "write fast. don't filter. the weird answers are the interesting ones.",
        lines=9
    )

    # Prompt 2
    build_prompt_page(story, s,
        "PROMPT",
        "what's the smallest possible version of one of those ideas? "
        "not the business plan. the afternoon experiment.",
        "a seed is not a tree. it doesn't need to be.",
        lines=9
    )

    # Body check-in
    build_body_checkin(story, s,
        "possibility can feel exciting and terrifying at the same time. "
        "both responses are valid."
    )

    # Prompt 3
    build_prompt_page(story, s,
        "PROMPT",
        "what would you attempt if you gave yourself permission to be "
        "a beginner again?",
        lines=9
    )

    # Prompt 4
    build_prompt_page(story, s,
        "PROMPT",
        "write about a time you started something without knowing "
        "how it would end. what happened?",
        lines=9
    )

    # Reframing exercise
    story.append(Spacer(1, 30))
    story.append(Paragraph("REFRAMING EXERCISE", s["PromptLabel"]))
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "take 3 things from your career that feel like losses. "
        "rewrite each one as a seed — something that could grow into "
        "something new.",
        s["Body"]
    ))
    story.append(Spacer(1, 12))

    for i in range(1, 4):
        story.append(Paragraph(
            f'<font color="{AMBER_SOFT.hexval()}"><b>the loss:</b></font>',
            s["Body"]
        ))
        story.append(WritingLines(CONTENT_W, num_lines=2, spacing=24))
        story.append(Spacer(1, 4))
        story.append(Paragraph(
            f'<font color="{BLUE.hexval()}"><b>the seed:</b></font>',
            s["Body"]
        ))
        story.append(WritingLines(CONTENT_W, num_lines=2, spacing=24))
        story.append(Spacer(1, 8))

    story.append(PageBreak())

    # Breathwork
    build_breathwork_page(story, s,
        "coherent breathing (5.5 breaths per minute)",
        [
            "inhale slowly through your nose for 5.5 seconds.",
            "exhale slowly through your nose for 5.5 seconds.",
            "no holding. just a smooth wave.",
            "continue for 3-5 minutes.",
            "this rhythm synchronizes your heart rate, blood pressure, and "
            "nervous system into a state researchers call 'coherence.'",
        ],
        "when you need clarity. when decisions feel impossible. when you want to think clearly."
    )

    # Extra prompt
    build_prompt_page(story, s,
        "PROMPT",
        "imagine you meet yourself one year from now. they look rested. "
        "they look like themselves. what did they do in the months between? "
        "not the big moves — the small ones.",
        lines=10
    )

    # Permission slip
    build_permission_slip(story, s, [
        "try something without knowing if it will work.",
        "be a beginner.",
        "change your mind.",
        "let it be small.",
        "not monetize it.",
    ], "not everything has to become a career. some things just get to be yours.")

    # Affirmation
    build_affirmation_page(story, s,
        "I am planting seeds in uncertain soil. that is an act of faith.")

    # Micro-experiment
    build_micro_experiment(story, s,
        "one small act of planting", [
            "sign up for one class, workshop, or meetup in something you've never tried.",
            "write 500 words about anything. don't edit them.",
            "make something with your hands (bread, art, a playlist, a shelf).",
            "have one conversation with someone in a field you know nothing about.",
            "say yes to one thing you'd normally say no to.",
        ]
    )

    # Closing prompt
    build_prompt_page(story, s,
        "BEFORE YOU MOVE ON",
        "what felt like possibility in this section? what felt scary? "
        "what's the one seed you want to water?",
        lines=8
    )


def build_section_five(story, s):
    """Section 5: Tending — nurturing what's growing."""
    build_section_opener(story, s, "five", "tending",
        "growth looks slow from the inside. trust the root system.")

    # Prompt 1
    build_prompt_page(story, s,
        "PROMPT",
        "what's one thing that has shifted in you since you started this workbook? "
        "even something small. especially something small.",
        lines=9
    )

    # Prompt 2
    build_prompt_page(story, s,
        "PROMPT",
        "what does your ideal tuesday look like? not a fantasy. "
        "a real tuesday. describe the morning, the afternoon, the evening.",
        "be specific. specificity is where meaning lives.",
        lines=10
    )

    # Body check-in
    build_body_checkin(story, s,
        "you've been doing hard work. "
        "let's check if your body is holding it differently now."
    )

    # Prompt 3
    build_prompt_page(story, s,
        "PROMPT",
        "who do you want to be around? not for networking. "
        "for nourishment. name 3 people or types of people.",
        lines=9
    )

    # Daily rhythms
    story.append(Spacer(1, 30))
    story.append(Paragraph("DAILY RHYTHMS", s["PromptLabel"]))
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "design a daily rhythm that reflects your values — not your "
        "old job schedule, not what LinkedIn says a 'productive morning' looks like.",
        s["Body"]
    ))
    story.append(Spacer(1, 8))

    rhythms = [
        "morning anchor (the first thing that grounds you):",
        "midday pause (how you check in with yourself):",
        "evening close (how you end the day with intention):",
        "one offline thing (something your hands do):",
    ]
    for r in rhythms:
        story.append(Paragraph(
            f'<font color="{AMBER_SOFT.hexval()}"><b>{r}</b></font>',
            s["Body"]
        ))
        story.append(WritingLines(CONTENT_W, num_lines=2, spacing=24))
        story.append(Spacer(1, 6))

    story.append(PageBreak())

    # Breathwork
    build_breathwork_page(story, s,
        "4-7-8 breathing (the natural tranquilizer)",
        [
            "place the tip of your tongue behind your upper front teeth.",
            "exhale completely through your mouth with a whoosh.",
            "inhale through your nose for 4 counts.",
            "hold your breath for 7 counts.",
            "exhale through your mouth for 8 counts.",
            "repeat 4 cycles.",
            "Dr. Andrew Weil calls this 'a natural tranquilizer for the nervous system.'",
        ],
        "at night when the worries come. when sleep won't. when you need to rest."
    )

    # Noticing page
    build_gratitude_page(story, s,
        "you're past the halfway point. let's pause and notice what's changing."
    )

    # Permission slip
    build_permission_slip(story, s, [
        "move slowly.",
        "celebrate small progress.",
        "change the plan when it stops fitting.",
        "not compare your timeline to anyone else's.",
        "rest as part of the work, not a reward for finishing it.",
    ], "tending is a practice, not a performance.")

    # Affirmation
    build_affirmation_page(story, s,
        "I am doing better than I think I am. "
        "the evidence is that I am still here, still trying.")

    # Micro-experiment
    build_micro_experiment(story, s,
        "one small act of tending", [
            "do the same grounding practice 3 days in a row. notice what changes.",
            "write a thank-you note to yourself for something specific.",
            "water a plant. literally. then sit with it for a minute.",
            "go to bed 30 minutes earlier than usual. no screen. just rest.",
            "tell someone about one thing you're tending (a skill, a hope, a habit).",
        ]
    )

    # Closing prompt
    build_prompt_page(story, s,
        "BEFORE YOU MOVE ON",
        "what is growing in you that you didn't expect? "
        "what needs more attention? what needs less?",
        lines=8
    )


def build_section_six(story, s):
    """Section 6: Emerging — stepping into who you're becoming."""
    build_section_opener(story, s, "six", "emerging",
        "you were not designed. you emerged. "
        "that is a kind of miracle no code can replicate.")

    # Prompt 1
    build_prompt_page(story, s,
        "PROMPT",
        "who are you now? not who you were. not who you think you should be. "
        "who are you right now, in this in-between?",
        "write in the present tense. 'I am...'",
        lines=10
    )

    # Prompt 2
    build_prompt_page(story, s,
        "PROMPT",
        "what do you know now that you didn't know when you started "
        "this workbook? about yourself, about what matters, about what you need.",
        lines=9
    )

    # Body check-in
    build_body_checkin(story, s,
        "one last scan. notice what's different from the first time you did this."
    )

    # Prompt 3 — composting
    build_prompt_page(story, s,
        "COMPOSTING",
        "what beliefs, habits, or stories do you want to leave behind? "
        "not destroy — compost. let them feed what comes next.",
        "write them down. then cross them out gently. they served you once.",
        lines=9
    )

    # Prompt 4
    build_prompt_page(story, s,
        "PROMPT",
        "write an intention for the next season of your life. "
        "not a goal. not a SMART objective. an intention. "
        "something that begins with 'I will...' or 'I choose...'",
        lines=9
    )

    # Breathwork
    build_breathwork_page(story, s,
        "vagal toning — the 'voo' breath",
        [
            "inhale deeply through your nose.",
            "exhale while making a long, low 'voo' sound — like a foghorn.",
            "feel the vibration in your chest and throat.",
            "repeat 5-8 times.",
            "the vibration stimulates the vagus nerve, the longest nerve in your body, "
            "which runs from your brainstem to your gut.",
            "it signals safety to your entire nervous system.",
        ],
        "when you need to feel grounded in your body. when the world feels too big."
    )

    # Extra prompt
    build_prompt_page(story, s,
        "PROMPT",
        "what do you want to be known for — not on a resume, "
        "but by the people who love you? write it like an intention.",
        lines=9
    )

    # Permission slip
    build_permission_slip(story, s, [
        "become someone new.",
        "keep some of who you were.",
        "not have it figured out even after doing all this work.",
        "be proud of yourself for getting here.",
        "begin again, as many times as you need to.",
    ], "you have always been becoming. this was just one chapter.")

    # Affirmation
    build_affirmation_page(story, s,
        "the future needs me whole, not optimized.")

    # Micro-experiment
    build_micro_experiment(story, s,
        "one small act of emerging", [
            "introduce yourself to someone new — without mentioning your old job title.",
            "do something that scares you slightly. slightly is enough.",
            "write '3 things I'm proud of this month' on a sticky note. put it where you'll see it.",
            "take yourself somewhere you've never been. alone. on purpose.",
            "tell one person: 'I'm in a transition and I'm doing okay.'",
        ]
    )

    # Closing prompt
    build_prompt_page(story, s,
        "BEFORE YOU CLOSE THIS WORKBOOK",
        "what do you want to remember about this time? "
        "not the pain — the becoming. the small moments of ground beneath your feet.",
        lines=9
    )


def build_future_self_letter(story, s):
    """Closing: letter to your future self."""
    story.append(Spacer(1, 40))
    story.append(Paragraph("a letter to your future self", s["Heading"]))
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "write a letter to yourself, 6 months from now. "
        "tell them what this time was like. what you learned. what you hope for them. "
        "what you want them to remember about who you were in the in-between.",
        s["Body"]
    ))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "seal it. set a calendar reminder. open it when the time comes.",
        s["ItalicNote"]
    ))
    story.append(Spacer(1, 12))
    story.append(Paragraph(
        "dear future me,",
        s["Prompt"]
    ))
    story.append(WritingLines(CONTENT_W, num_lines=18, spacing=26))
    story.append(PageBreak())

    # Second page of the letter
    story.append(Spacer(1, 30))
    story.append(WritingLines(CONTENT_W, num_lines=20, spacing=26))
    story.append(Spacer(1, 16))
    story.append(Paragraph(
        "with steadiness and tenderness,",
        s["ItalicNote"]
    ))
    story.append(WritingLines(CONTENT_W, num_lines=2, spacing=28))
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        f'<font color="{AMBER_SOFT.hexval()}">date:</font> _______________',
        s["Body"]
    ))
    story.append(PageBreak())


def build_affirmation_cards(story, s):
    """Appendix: Printable affirmation cards (cut along dotted lines)."""
    story.append(Spacer(1, 40))
    story.append(Paragraph("printable affirmation cards", s["Heading"]))
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "cut along the dotted lines. keep one in your wallet, "
        "one on your mirror, one by your bed.",
        s["ItalicCenter"]
    ))
    story.append(Spacer(1, 16))

    cards = [
        "I am whole before I open my laptop.",
        "I do not need to solve the future today.",
        "my intuition was trained by a lifetime of being alive.",
        "I am not broken for feeling anxious. I am awake.",
        "I am planting seeds in uncertain soil. that is an act of faith.",
        "the future needs me whole, not optimized.",
        "I am doing better than I think I am.",
        "I was not designed. I emerged. that is a kind of miracle.",
        "the antidote to this feeling is not more information. it is presence.",
        "I am here. I am whole. I am enough.",
        "there is something in me that change cannot touch.",
        "I am not behind. I am in the middle.",
    ]

    for i, card in enumerate(cards):
        story.append(Paragraph(
            f'<font color="{NAVY.hexval()}" size="13"><b>"{card}"</b></font>',
            ParagraphStyle(
                name=f"Card{i}", fontName="Helvetica-Bold", fontSize=13,
                textColor=NAVY, alignment=TA_CENTER, leading=18,
                spaceAfter=4, leftIndent=16, rightIndent=16,
            )
        ))
        story.append(Paragraph(
            "— luminous pulse",
            ParagraphStyle(
                name=f"CardSig{i}", fontName="Helvetica-Oblique", fontSize=8,
                textColor=SOFT_GRAY, alignment=TA_CENTER, leading=12,
                spaceAfter=8,
            )
        ))
        story.append(HLine(CONTENT_W, HexColor("#c0bbb5"), 0.3))
        story.append(Spacer(1, 8))

        # Page break after every 4 cards
        if (i + 1) % 4 == 0 and i < len(cards) - 1:
            story.append(PageBreak())
            story.append(Spacer(1, 30))


def build_notes_pages(story, s, count=3):
    """Blank notes pages for free journaling."""
    story.append(PageBreak())
    story.append(Spacer(1, 30))
    story.append(Paragraph("notes", s["Heading"]))
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "for the things that don't fit anywhere else. "
        "the stray thoughts, the half-formed ideas, the things "
        "you need to get out of your head and onto paper.",
        s["ItalicCenter"]
    ))
    story.append(Spacer(1, 16))
    story.append(WritingLines(CONTENT_W, num_lines=18, spacing=26))

    for _ in range(count - 1):
        story.append(PageBreak())
        story.append(Spacer(1, 30))
        story.append(WritingLines(CONTENT_W, num_lines=22, spacing=26))


def build_closing(story, s):
    """Final page — about Luminous Pulse."""
    story.append(PageBreak())
    story.append(Spacer(1, 140))

    logo_path = os.path.join(os.path.dirname(__file__), "logo-abstract-sanctuary-transparent.png")
    if os.path.exists(logo_path):
        img = Image(logo_path, width=100, height=53)
        img.hAlign = "CENTER"
        story.append(img)
        story.append(Spacer(1, 24))

    story.append(Paragraph(
        "luminous pulse",
        ParagraphStyle(
            name="ClosingBrand", fontName="Helvetica-Bold", fontSize=16,
            textColor=NAVY, alignment=TA_CENTER, leading=20, spaceAfter=8,
        )
    ))
    story.append(Paragraph(
        "where anxious humans come to rest.",
        s["ItalicCenter"]
    ))
    story.append(Spacer(1, 24))
    story.append(Paragraph(
        "this workbook was created by Christie Parrow — "
        "a PMP-certified project manager, AI industry professional, "
        "and a human who understands what it feels like when the ground shifts.",
        s["BodyCenter"]
    ))
    story.append(Spacer(1, 16))
    story.append(HLine(200, LIGHT_GRAY))
    story.append(Spacer(1, 16))
    story.append(Paragraph("luminouspulse.co", s["BodyCenter"]))
    story.append(Paragraph("@luminouspulse.co", s["BodyCenter"]))
    story.append(Spacer(1, 24))
    story.append(Paragraph(
        "if this workbook helped you, share it with someone who needs it.",
        s["ItalicCenter"]
    ))
    story.append(Paragraph(
        "we are all in the in-between together.",
        s["AffirmationLight"]
    ))


# ── Main ──

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(script_dir, "The-In-Between-Workbook.pdf")

    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=MARGIN,
        rightMargin=MARGIN,
        topMargin=MARGIN,
        bottomMargin=MARGIN,
    )

    s = create_styles()
    story = []

    # Cover (navy bg)
    build_cover(story, s)

    # Design philosophy + how to use (cream bg)
    build_design_philosophy(story, s)

    # Table of contents
    build_table_of_contents(story, s)

    # Section 1: Letting Go
    build_section_one(story, s)

    # Section 2: Sitting With
    build_section_two(story, s)

    # Section 3: Uncovering
    build_section_three(story, s)

    # Section 4: Planting
    build_section_four(story, s)

    # Section 5: Tending
    build_section_five(story, s)

    # Section 6: Emerging
    build_section_six(story, s)

    # Closing: Future Self Letter
    build_future_self_letter(story, s)

    # Appendix: Affirmation Cards
    build_affirmation_cards(story, s)

    # Notes pages
    build_notes_pages(story, s, count=4)

    # Final page
    build_closing(story, s)

    # Build with alternating page templates
    # Cover gets navy, section openers get navy, everything else gets cream
    page_templates = []

    def on_page(canvas, doc):
        """Determine page background based on content."""
        draw_bg(canvas, doc)

    doc.build(story, onFirstPage=draw_bg_cover, onLaterPages=on_page)

    page_count = doc.page
    size_mb = os.path.getsize(output_path) / (1024 * 1024)
    print(f"\n  done! {page_count} pages, {size_mb:.1f} MB")
    print(f"  → {output_path}")


if __name__ == "__main__":
    main()
