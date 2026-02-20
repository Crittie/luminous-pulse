#!/usr/bin/env python3
"""Generate "before the room" workbook PDF — Luminous Pulse ($9).

An interview grounding guide — for the 30 minutes before the thing that scares you.

5 parts: the pre-interview ground, reframing your gap story, nervous system
regulation toolkit, post-interview decompression, win or lose I'm still me.

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
        self.canv.circle(self.dot_size / 2, self.dot_size / 2,
                         self.dot_size / 2, fill=1, stroke=0)

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
    """A dashed cutting line."""
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


# ── Page Backgrounds ──

def draw_bg(canvas, doc):
    """Standard page background — cream with subtle footer."""
    canvas.saveState()
    canvas.setFillColor(CREAM)
    canvas.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    canvas.setFont("Helvetica", 7)
    canvas.setFillColor(SOFT_GRAY)
    canvas.drawCentredString(PAGE_W / 2, 30,
                             "before the room  ·  luminouspulse.co")
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
        name="TOCSection", fontName="Helvetica-Bold", fontSize=11,
        textColor=NAVY, alignment=TA_LEFT, leading=16, spaceAfter=3,
    ))
    styles.add(ParagraphStyle(
        name="TOCItem", fontName="Helvetica", fontSize=10,
        textColor=HexColor("#555555"), alignment=TA_LEFT, leading=14, spaceAfter=2,
        leftIndent=16,
    ))
    styles.add(ParagraphStyle(
        name="StepLabel", fontName="Helvetica-Bold", fontSize=11,
        textColor=NAVY, alignment=TA_LEFT, leading=16, spaceAfter=4,
    ))
    styles.add(ParagraphStyle(
        name="TimeLabel", fontName="Helvetica-Bold", fontSize=9,
        textColor=AMBER_SOFT, alignment=TA_LEFT, leading=13, spaceAfter=2,
        letterSpacing=1,
    ))
    styles.add(ParagraphStyle(
        name="QuickRefTitle", fontName="Helvetica-Bold", fontSize=11,
        textColor=NAVY, alignment=TA_CENTER, leading=15, spaceAfter=6,
    ))
    styles.add(ParagraphStyle(
        name="QuickRefBody", fontName="Helvetica", fontSize=9.5,
        textColor=HexColor("#333333"), alignment=TA_LEFT, leading=14, spaceAfter=6,
    ))

    return styles


# ── Page Builders ──

def build_cover(story, s):
    story.append(Spacer(1, 180))
    logo_path = os.path.join(os.path.dirname(__file__),
                             "logo-abstract-sanctuary-transparent.png")
    if os.path.exists(logo_path):
        img = Image(logo_path, width=120, height=63)
        img.hAlign = "CENTER"
        story.append(img)
        story.append(Spacer(1, 40))
    story.append(Paragraph("before the room", s["CoverTitle"]))
    story.append(Spacer(1, 14))
    story.append(Paragraph(
        "an interview grounding guide<br/>"
        "for the 30 minutes before the thing that scares you.",
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
        "your hands are shaking. your stomach is doing the thing. "
        "you've rehearsed your answers seventeen times but your brain "
        "just went blank.",
        s["PromptCenter"]
    ))
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "this guide was designed for exactly this moment — the 30 minutes "
        "before you walk into the room (or click the link, or dial the "
        "number). it's not about performance tips or power poses. "
        "it's about helping your nervous system remember that you are safe, "
        "you are capable, and you are more than any single conversation "
        "can define.",
        s["Body"]
    ))
    story.append(Paragraph(
        "you can use this guide once, or you can use it before every "
        "interview. keep it in your bag. keep it on your desk. "
        "the pages don't expire.",
        s["Body"]
    ))
    story.append(Spacer(1, 16))
    story.append(AccentDot(AMBER))
    story.append(Spacer(1, 12))

    story.append(Paragraph("how to use this guide", s["SubHeading"]))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "<b>before the interview:</b> work through parts 1-3. "
        "these are the grounding ritual, the gap story reframe, and the "
        "nervous system toolkit. together they take about 20-25 minutes.",
        s["Body"]
    ))
    story.append(Paragraph(
        "<b>after the interview:</b> turn to part 4. this is the "
        "decompression practice — what to do with all that adrenaline "
        "once the call is over.",
        s["Body"]
    ))
    story.append(Paragraph(
        "<b>anytime:</b> part 5 is a set of affirmations and a writing "
        "exercise you can return to whenever the identity wobble hits.",
        s["Body"]
    ))

    story.append(Spacer(1, 20))
    story.append(Paragraph(
        '"I am ready for today. not because I know what\'s coming,<br/>'
        'but because I know who I am."',
        s["AffirmationLight"]
    ))
    story.append(PageBreak())


def build_toc(story, s):
    story.append(Spacer(1, 40))
    story.append(Paragraph("contents", s["Heading"]))
    story.append(Spacer(1, 14))
    story.append(HLine(CONTENT_W, AMBER, 0.6))
    story.append(Spacer(1, 14))

    sections = [
        ("part 1", "the pre-interview ground",
         "a grounding ritual for the 30 minutes before"),
        ("part 2", "reframing your gap story",
         "how to talk about what happened — without shame"),
        ("part 3", "the nervous system toolkit",
         "three techniques to regulate your body before you walk in"),
        ("part 4", "post-interview decompression",
         "what to do with all that adrenaline"),
        ("part 5", "win or lose, I'm still me",
         "affirmations for the identity wobble"),
    ]

    for num, title, desc in sections:
        story.append(Paragraph(f"{num}: {title}", s["TOCSection"]))
        story.append(Paragraph(desc, s["TOCItem"]))
        story.append(Spacer(1, 3))

    story.append(Spacer(1, 8))
    story.append(HLine(CONTENT_W * 0.3, LIGHT_GRAY, 0.3))
    story.append(Spacer(1, 6))
    story.append(Paragraph("closing + quick reference card", s["TOCSection"]))

    story.append(PageBreak())


def build_section_opener(story, s, number, title, epigraph):
    """Full-page navy section opener."""
    story.append(NavyPageBg())
    story.append(Spacer(1, 200))
    story.append(Paragraph(f"PART {number}", s["SectionNum"]))
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


# ── PART 1: The Pre-Interview Ground ──

def build_part_1(story, s):
    build_section_opener(story, s, "1", "the pre-interview<br/>ground",
        "you don't need to be perfect.<br/>"
        "you need to be present.")

    # The 30-Minute Ritual
    story.append(Spacer(1, 16))
    story.append(Paragraph("the 30-minute ritual", s["SubHeading"]))
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "this is your pre-interview grounding sequence. "
        "do it in order. each step builds on the last. "
        "you can do it at home, in a parking lot, in a coffee shop "
        "bathroom. you just need 30 minutes and yourself.",
        s["Body"]
    ))
    story.append(Spacer(1, 12))

    # Step 1: Arrive (5 min)
    story.append(Paragraph("T-30 MINUTES", s["TimeLabel"]))
    story.append(Paragraph("step 1: arrive in your body", s["StepLabel"]))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "put your phone on do not disturb. close your eyes. "
        "place both feet flat on the floor. feel the ground.",
        s["Body"]
    ))
    story.append(Paragraph(
        "take 5 slow breaths. in through the nose, out through the mouth. "
        "don't count. just breathe until your shoulders drop.",
        s["Body"]
    ))
    story.append(Spacer(1, 6))
    story.append(Paragraph("NOTICE", s["ExerciseLabel"]))
    story.append(Paragraph(
        "where is the anxiety right now? chest? stomach? throat? hands? "
        "name it without trying to fix it.",
        s["ItalicNote"]
    ))
    story.append(WritingLines(CONTENT_W, num_lines=2, spacing=24))
    story.append(Spacer(1, 10))

    # Step 2: Ground (5 min)
    story.append(Paragraph("T-25 MINUTES", s["TimeLabel"]))
    story.append(Paragraph("step 2: the 5-4-3-2-1 ground", s["StepLabel"]))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "name what your senses are telling you right now. "
        "say each one out loud if you can.",
        s["ItalicNote"]
    ))
    story.append(Spacer(1, 6))

    senses = [
        ("5", "things I can see:"),
        ("4", "things I can touch:"),
        ("3", "things I can hear:"),
        ("2", "things I can smell:"),
        ("1", "thing I can taste:"),
    ]
    for num, sense in senses:
        story.append(Paragraph(f"<b>{num}</b> {sense}", s["Body"]))
    story.append(PageBreak())

    # Step 3: Breathe (5 min)
    story.append(Spacer(1, 16))
    story.append(Paragraph("T-20 MINUTES", s["TimeLabel"]))
    story.append(Paragraph("step 3: box breathing", s["StepLabel"]))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "this is the technique Navy SEALs use before high-stakes operations. "
        "it creates \"alert calm\" — focused and present, not drowsy.",
        s["Body"]
    ))
    story.append(Spacer(1, 8))

    steps = [
        "inhale through your nose for 4 seconds.",
        "hold for 4 seconds.",
        "exhale through your mouth for 4 seconds.",
        "hold (lungs empty) for 4 seconds.",
        "repeat for 5 minutes (or until you feel steady).",
    ]
    for i, step in enumerate(steps, 1):
        story.append(NumberedCircle(i))
        story.append(Spacer(1, 2))
        story.append(Paragraph(step, s["Body"]))
        story.append(Spacer(1, 2))

    story.append(Spacer(1, 12))

    # Step 4: Set intention (5 min)
    story.append(Paragraph("T-15 MINUTES", s["TimeLabel"]))
    story.append(Paragraph("step 4: set your intention", s["StepLabel"]))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "this is not about \"nailing the interview.\" this is about "
        "showing up as yourself. complete the sentences below.",
        s["Body"]
    ))
    story.append(Spacer(1, 8))
    story.append(Paragraph("today, I want them to see that I am...", s["Prompt"]))
    story.append(WritingLines(CONTENT_W, num_lines=2, spacing=26))
    story.append(Spacer(1, 8))
    story.append(Paragraph("the one thing I want to communicate is...", s["Prompt"]))
    story.append(WritingLines(CONTENT_W, num_lines=2, spacing=26))
    story.append(PageBreak())

    # Step 5: Anchor phrase (5 min)
    story.append(Spacer(1, 16))
    story.append(Paragraph("T-10 MINUTES", s["TimeLabel"]))
    story.append(Paragraph("step 5: choose your anchor phrase", s["StepLabel"]))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "an anchor phrase is a single sentence you can silently repeat "
        "when the anxiety spikes during the conversation. choose one "
        "from the list or write your own.",
        s["Body"]
    ))
    story.append(Spacer(1, 8))

    phrases = [
        "I belong in this room.",
        "I am interviewing them too.",
        "I've survived harder things than a conversation.",
        "I don't need this job to be whole.",
        "my worth is not on the table today.",
    ]
    for p in phrases:
        story.append(AccentDot(AMBER, size=5))
        story.append(Spacer(1, 2))
        story.append(Paragraph(f'"{p}"', s["AffirmationLight"]))
        story.append(Spacer(1, 4))

    story.append(Spacer(1, 10))
    story.append(Paragraph("my anchor phrase:", s["SubHeading"]))
    story.append(WritingLines(CONTENT_W, num_lines=2, spacing=28))
    story.append(Spacer(1, 12))

    # Step 6: Walk in
    story.append(Paragraph("T-5 MINUTES", s["TimeLabel"]))
    story.append(Paragraph("step 6: walk in", s["StepLabel"]))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "stand up. shake your hands out. roll your shoulders. "
        "take one long exhale. say your anchor phrase out loud, once. "
        "then go.",
        s["Body"]
    ))
    story.append(Spacer(1, 10))
    story.append(HLine(CONTENT_W * 0.3, AMBER, 0.4))
    story.append(Spacer(1, 10))
    story.append(Paragraph(
        "you are not performing. you are showing up. there is a difference.",
        s["ItalicCenter"]
    ))
    story.append(PageBreak())


# ── PART 2: Reframing Your Gap Story ──

def build_part_2(story, s):
    build_section_opener(story, s, "2", "reframing your<br/>gap story",
        "they're going to ask. here's how to answer<br/>"
        "without shrinking.")

    # Page 1: The question you're dreading
    story.append(Spacer(1, 16))
    story.append(Paragraph("the question you're dreading", s["SubHeading"]))
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        '"so, tell me about your gap." "what have you been doing since your '
        'last role?" "why did you leave?"',
        s["Body"]
    ))
    story.append(Paragraph(
        "this question feels like a trap because our culture treats "
        "employment gaps like character flaws. they are not. you were "
        "navigating one of the most disruptive periods in modern work "
        "history. that is not a gap. it is a chapter.",
        s["Body"]
    ))
    story.append(Spacer(1, 10))

    story.append(Paragraph("THE REFRAME", s["ExerciseLabel"]))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "you do not need to apologize for the gap. you do not need "
        "to fill it with fake projects or exaggerated freelance work. "
        "you need one honest, grounded sentence that tells the truth "
        "without performing shame.",
        s["Body"]
    ))
    story.append(Spacer(1, 8))

    story.append(Paragraph("TEMPLATES", s["ExerciseLabel"]))
    story.append(Spacer(1, 6))

    templates = [
        '"my role was eliminated during a restructuring. I used the time to '
        '[one true thing: rest, take care of family, clarify what I want next]."',
        '"the team was impacted by AI-driven changes. since then, I\'ve been '
        'focused on [one genuine activity]."',
        '"I took time to recalibrate after a major transition. I\'m clearer now '
        'about what I\'m looking for."',
    ]
    for i, t in enumerate(templates, 1):
        story.append(NumberedCircle(i))
        story.append(Spacer(1, 2))
        story.append(Paragraph(t, s["Body"]))
        story.append(Spacer(1, 6))

    story.append(PageBreak())

    # Page 2: Write your version
    story.append(Spacer(1, 16))
    story.append(Paragraph("WRITE YOUR VERSION", s["ExerciseLabel"]))
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "using the templates above as a starting point, write "
        "your own gap story in 2-3 sentences. the rules: "
        "no apologizing. no over-explaining. no performing.",
        s["Body"]
    ))
    story.append(Spacer(1, 8))

    story.append(Paragraph("my gap story (draft 1):", s["SubHeading"]))
    story.append(WritingLines(CONTENT_W, num_lines=5, spacing=28))
    story.append(Spacer(1, 16))

    story.append(Paragraph("REFINE IT", s["ExerciseLabel"]))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "now say it out loud. does it feel true? does it feel "
        "like you? if something feels off, rewrite it below.",
        s["ItalicNote"]
    ))
    story.append(Spacer(1, 8))

    story.append(Paragraph("my gap story (final):", s["SubHeading"]))
    story.append(WritingLines(CONTENT_W, num_lines=5, spacing=28))
    story.append(Spacer(1, 14))
    story.append(Paragraph(
        "practice saying this once, out loud, before the interview. "
        "the first time you say it should not be to a stranger.",
        s["ItalicCenter"]
    ))
    story.append(PageBreak())

    # Page 3: What you bring
    story.append(Spacer(1, 16))
    story.append(Paragraph("WHAT YOU BRING TO THE ROOM", s["ExerciseLabel"]))
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "before the interview, remind yourself what you actually bring. "
        "not your résumé. the human things.",
        s["Body"]
    ))
    story.append(Spacer(1, 8))

    story.append(Paragraph("3 skills I'm genuinely proud of:", s["Prompt"]))
    story.append(WritingLines(CONTENT_W, num_lines=4, spacing=26))
    story.append(Spacer(1, 10))

    story.append(Paragraph(
        "something I've learned about myself during this transition:", s["Prompt"]
    ))
    story.append(WritingLines(CONTENT_W, num_lines=4, spacing=26))
    story.append(Spacer(1, 10))

    story.append(Paragraph(
        "the one quality I want every team I work with to experience:", s["Prompt"]
    ))
    story.append(WritingLines(CONTENT_W, num_lines=3, spacing=26))
    story.append(PageBreak())


# ── PART 3: The Nervous System Toolkit ──

def build_part_3(story, s):
    build_section_opener(story, s, "3", "the nervous system<br/>toolkit",
        "your brain may forget your talking points.<br/>"
        "your body won't forget how to breathe.")

    # Page 1: Physiological sigh
    story.append(Spacer(1, 16))
    story.append(Paragraph(
        "these are three evidence-based techniques for calming your "
        "nervous system. each one takes under 2 minutes. learn all three "
        "and use whichever one your body responds to most.",
        s["Body"]
    ))
    story.append(Spacer(1, 12))

    story.append(Paragraph("TECHNIQUE 1: THE PHYSIOLOGICAL SIGH", s["ExerciseLabel"]))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "neuroscientist Andrew Huberman calls this the single fastest "
        "way to calm your nervous system in real time. you can do it "
        "on camera without anyone noticing.",
        s["ItalicNote"]
    ))
    story.append(Spacer(1, 8))

    sigh_steps = [
        "take a deep breath in through your nose.",
        "at the top, take a second short inhale (a quick sip of air).",
        "exhale slowly through your mouth — as long as you can.",
        "repeat 2-3 times.",
    ]
    for i, step in enumerate(sigh_steps, 1):
        story.append(NumberedCircle(i))
        story.append(Spacer(1, 2))
        story.append(Paragraph(step, s["Body"]))
        story.append(Spacer(1, 2))

    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "best for: mid-interview panic, racing heart, brain fog. "
        "you can do this with your camera on.",
        s["ItalicNote"]
    ))
    story.append(Spacer(1, 16))

    # Technique 2: Butterfly hug
    story.append(Paragraph("TECHNIQUE 2: THE BUTTERFLY HUG", s["ExerciseLabel"]))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "a self-administered bilateral stimulation technique developed "
        "for trauma processing. it sounds simple. it works.",
        s["ItalicNote"]
    ))
    story.append(Spacer(1, 8))

    hug_steps = [
        "cross your arms over your chest, fingertips just below collarbones.",
        "interlock your thumbs (your hands form butterfly wings).",
        "alternately tap your hands gently against your chest.",
        "close your eyes. breathe slowly. continue for 1-2 minutes.",
    ]
    for i, step in enumerate(hug_steps, 1):
        story.append(NumberedCircle(i))
        story.append(Spacer(1, 2))
        story.append(Paragraph(step, s["Body"]))
        story.append(Spacer(1, 2))

    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "best for: pre-interview anxiety, the waiting room, "
        "the 5 minutes before you click the video call link.",
        s["ItalicNote"]
    ))
    story.append(PageBreak())

    # Page 2: TIPP + Cold water
    story.append(Spacer(1, 16))
    story.append(Paragraph("TECHNIQUE 3: THE COLD RESET", s["ExerciseLabel"]))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "from Dialectical Behavior Therapy. the mammalian dive reflex "
        "slows your heart rate within seconds. this is the emergency brake.",
        s["ItalicNote"]
    ))
    story.append(Spacer(1, 8))

    cold_steps = [
        "splash cold water on your face (especially around your eyes and temples).",
        "or: hold ice cubes in your palms for 30 seconds.",
        "or: press a cold, wet paper towel against the back of your neck.",
        "follow with 3 slow breaths.",
    ]
    for i, step in enumerate(cold_steps, 1):
        story.append(NumberedCircle(i))
        story.append(Spacer(1, 2))
        story.append(Paragraph(step, s["Body"]))
        story.append(Spacer(1, 2))

    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "best for: when anxiety is at an 8/10 or higher. when your "
        "hands are shaking and you can't think. when box breathing "
        "isn't enough.",
        s["ItalicNote"]
    ))

    story.append(Spacer(1, 20))
    story.append(Paragraph("WHICH ONE IS FOR ME?", s["ExerciseLabel"]))
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "try all three right now — not before an interview, just now. "
        "notice which one your body responds to most. that's your go-to.",
        s["Body"]
    ))
    story.append(Spacer(1, 8))
    story.append(Paragraph("my go-to technique:", s["SubHeading"]))
    story.append(WritingLines(CONTENT_W, num_lines=1, spacing=28))
    story.append(Spacer(1, 10))
    story.append(Paragraph("what I noticed when I tried it:", s["Prompt"]))
    story.append(WritingLines(CONTENT_W, num_lines=4, spacing=26))
    story.append(PageBreak())


# ── PART 4: Post-Interview Decompression ──

def build_part_4(story, s):
    build_section_opener(story, s, "4", "post-interview<br/>decompression",
        "the interview is over. your nervous system isn't.<br/>"
        "here's what to do with all that adrenaline.")

    # Page 1: The immediate after
    story.append(Spacer(1, 16))
    story.append(Paragraph("the first 10 minutes after", s["SubHeading"]))
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "your body just went through a stress response. whether the "
        "interview went well or badly, your nervous system needs to "
        "come down. do these in order.",
        s["Body"]
    ))
    story.append(Spacer(1, 12))

    story.append(Paragraph("THE DECOMPRESSION SEQUENCE", s["ExerciseLabel"]))
    story.append(Spacer(1, 8))

    decomp = [
        ("SHAKE IT OFF (1 MINUTE)",
         "stand up. shake your hands vigorously for 30 seconds. "
         "then shake your whole body — shoulders, hips, legs. "
         "animals do this after a threat passes. it discharges "
         "the adrenaline your body just produced."),
        ("LONG EXHALES (2 MINUTES)",
         "breathe in for 4 counts. breathe out for 8. "
         "the extended exhale activates your parasympathetic nervous "
         "system. repeat 5-6 times."),
        ("COLD WATER (30 SECONDS)",
         "splash cold water on your face and wrists. "
         "this resets your autonomic nervous system."),
        ("NAME IT (2 MINUTES)",
         "say out loud how you feel. not how it went. how you FEEL. "
         "\"I feel relieved.\" \"I feel shaky.\" \"I feel numb.\" "
         "naming the emotion reduces its intensity by up to 50%."),
    ]

    for title, desc in decomp:
        story.append(Paragraph(title, s["ExerciseLabel"]))
        story.append(Spacer(1, 2))
        story.append(Paragraph(desc, s["Body"]))
        story.append(Spacer(1, 8))

    story.append(PageBreak())

    # Page 2: The debrief
    story.append(Spacer(1, 16))
    story.append(Paragraph("the debrief", s["SubHeading"]))
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "not a post-mortem. not a list of things you should have said. "
        "just a gentle check-in with yourself.",
        s["ItalicNote"]
    ))
    story.append(Spacer(1, 10))

    story.append(Paragraph("BEFORE I REPLAY IT IN MY HEAD", s["ExerciseLabel"]))
    story.append(Spacer(1, 6))

    story.append(Paragraph("one thing I'm proud of from that conversation:", s["Prompt"]))
    story.append(WritingLines(CONTENT_W, num_lines=3, spacing=26))
    story.append(Spacer(1, 10))

    story.append(Paragraph("one thing I'd do differently (no judgment):", s["Prompt"]))
    story.append(WritingLines(CONTENT_W, num_lines=3, spacing=26))
    story.append(Spacer(1, 10))

    story.append(Paragraph(
        "something I noticed about the company or the interviewer:", s["Prompt"]
    ))
    story.append(WritingLines(CONTENT_W, num_lines=3, spacing=26))
    story.append(Spacer(1, 10))

    story.append(Paragraph("how my body feels right now:", s["Prompt"]))
    story.append(WritingLines(CONTENT_W, num_lines=2, spacing=26))
    story.append(PageBreak())

    # Page 3: The non-negotiable
    story.append(Spacer(1, 20))
    story.append(Paragraph("THE NON-NEGOTIABLE", s["ExerciseLabel"]))
    story.append(Spacer(1, 10))
    story.append(Paragraph(
        "regardless of how it went, you need to do one kind thing "
        "for yourself in the next hour. not productive. not optimizing. "
        "just kind.",
        s["Body"]
    ))
    story.append(Spacer(1, 8))

    story.append(Paragraph(
        "check one (or write your own):",
        s["ItalicNote"]
    ))
    story.append(Spacer(1, 8))

    kind_things = [
        "walk outside for 10 minutes with no phone.",
        "eat something warm.",
        "call someone who loves me (not to debrief — just to hear their voice).",
        "lie on the floor for 5 minutes and do nothing.",
        "take a shower or bath.",
    ]
    for k in kind_things:
        story.append(CheckboxLine(CONTENT_W))
        story.append(Spacer(1, 2))
        story.append(Paragraph(k, s["Body"]))
        story.append(Spacer(1, 4))

    story.append(Spacer(1, 8))
    story.append(Paragraph("my own:", s["Prompt"]))
    story.append(WritingLines(CONTENT_W, num_lines=1, spacing=28))
    story.append(Spacer(1, 16))
    story.append(Paragraph(
        "you showed up. that was the hard part. the rest is not up to you.",
        s["ItalicCenter"]
    ))
    story.append(PageBreak())


# ── PART 5: Win or Lose, I'm Still Me ──

def build_part_5(story, s):
    build_section_opener(story, s, "5", "win or lose,<br/>I'm still me",
        "no single conversation gets to define you.<br/>"
        "not this one. not the last one. not the next one.")

    # Page 1: Affirmations
    story.append(Spacer(1, 16))
    story.append(Paragraph("affirmations for the interview process",
                            s["SubHeading"]))
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "read these slowly. underline the ones that feel true. "
        "return to them before every interview.",
        s["ItalicNote"]
    ))
    story.append(Spacer(1, 12))

    affirmations = [
        "I am not auditioning for my own worth.",
        "I bring something to every room I enter that cannot be found on a résumé.",
        "a rejection is information, not a verdict.",
        "I am interviewing them too.",
        "my value does not decrease because one person couldn't see it.",
        "I have survived every worst day I ever had. my track record is 100%.",
        "I am not behind. I am arriving exactly when I am ready.",
        "the right room will recognize me. I don't need to convince the wrong one.",
        "I can feel nervous and be capable at the same time.",
        "this process does not get to take my peace.",
    ]

    for aff in affirmations:
        story.append(AccentDot(AMBER, size=5))
        story.append(Spacer(1, 2))
        story.append(Paragraph(f'"{aff}"', s["Affirmation"]))
        story.append(Spacer(1, 6))

    story.append(PageBreak())

    # Page 2: The identity anchor
    story.append(Spacer(1, 16))
    story.append(Paragraph("THE IDENTITY ANCHOR", s["ExerciseLabel"]))
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "the interview process has a way of making you forget who you are. "
        "every rejection chips away at the story. every ghosted application "
        "makes you wonder. so let's anchor it now, before the noise starts.",
        s["Body"]
    ))
    story.append(Spacer(1, 10))

    story.append(Paragraph(
        "regardless of what happens in any interview, these things are true about me:",
        s["Prompt"]
    ))
    story.append(WritingLines(CONTENT_W, num_lines=6, spacing=28))
    story.append(Spacer(1, 16))

    story.append(Paragraph(
        "the kind of work environment where I do my best:", s["Prompt"]
    ))
    story.append(WritingLines(CONTENT_W, num_lines=4, spacing=28))
    story.append(Spacer(1, 16))

    story.append(Paragraph(
        "what I refuse to compromise on in my next role:", s["Prompt"]
    ))
    story.append(WritingLines(CONTENT_W, num_lines=4, spacing=28))
    story.append(PageBreak())

    # Page 3: A note for the bad days
    story.append(Spacer(1, 30))
    story.append(Paragraph("A NOTE FOR THE BAD DAYS", s["ExerciseLabel"]))
    story.append(Spacer(1, 12))
    story.append(Paragraph(
        "write a short message to yourself — the version of you "
        "that just got a rejection, or never heard back, or stumbled "
        "through an answer. what do they need to hear from you right now?",
        s["Body"]
    ))
    story.append(Spacer(1, 12))
    story.append(Paragraph("dear me on a bad day,", s["Prompt"]))
    story.append(Spacer(1, 4))
    story.append(WritingLines(CONTENT_W, num_lines=12))
    story.append(Spacer(1, 16))
    story.append(Paragraph(
        "fold this page over so you can find it fast.",
        s["ItalicCenter"]
    ))
    story.append(PageBreak())


# ── Closing Page ──

def build_closing(story, s):
    story.append(Spacer(1, 80))
    story.append(Paragraph("you've got this.", s["Heading"]))
    story.append(Spacer(1, 16))
    story.append(HLine(CONTENT_W * 0.3, AMBER, 0.6))
    story.append(Spacer(1, 20))
    story.append(Paragraph(
        "not because you're going to ace every interview. "
        "not because you'll always say the right thing. "
        "but because you showed up for yourself before you showed up for them. "
        "and that changes everything.",
        s["BodyCenter"]
    ))
    story.append(Spacer(1, 12))
    story.append(Paragraph(
        "keep this guide close. use it every time. "
        "the ritual gets faster as it becomes familiar. "
        "eventually your body will remember the steps on its own.",
        s["BodyCenter"]
    ))
    story.append(Spacer(1, 24))
    story.append(Paragraph(
        '"I am ready for today. not because I know what\'s coming,<br/>'
        'but because I know who I am."',
        s["Affirmation"]
    ))
    story.append(Spacer(1, 30))
    story.append(AccentDot(AMBER))
    story.append(Spacer(1, 20))
    story.append(Paragraph(
        "when you're ready for more —",
        s["BodyCenter"]
    ))
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        '"who am I without the title?" — 8 exercises for reclaiming '
        "who you are beyond your job.",
        s["ItalicCenter"]
    ))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        '"the in-between" — a 90-page guided journal for the full journey.',
        s["ItalicCenter"]
    ))
    story.append(Spacer(1, 8))
    story.append(Paragraph("luminouspulse.co", s["CTA"]))
    story.append(PageBreak())


# ── Quick Reference Card ──

def build_quick_reference(story, s):
    """Tear-out quick reference card with all techniques."""
    story.append(Spacer(1, 16))
    story.append(Paragraph("quick reference card", s["Heading"]))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "tear this page out and keep it with you.",
        s["ItalicCenter"]
    ))
    story.append(Spacer(1, 8))
    story.append(DashedLine(CONTENT_W))
    story.append(Spacer(1, 12))

    # Box Breathing
    story.append(Paragraph("BOX BREATHING", s["QuickRefTitle"]))
    story.append(Paragraph(
        "inhale 4 sec → hold 4 sec → exhale 4 sec → hold 4 sec. "
        "repeat 5 min. creates alert calm.",
        s["QuickRefBody"]
    ))
    story.append(Spacer(1, 6))

    # Physiological Sigh
    story.append(Paragraph("PHYSIOLOGICAL SIGH", s["QuickRefTitle"]))
    story.append(Paragraph(
        "deep inhale → second short inhale at the top → long slow exhale. "
        "repeat 2-3x. fastest nervous system reset.",
        s["QuickRefBody"]
    ))
    story.append(Spacer(1, 6))

    # Butterfly Hug
    story.append(Paragraph("BUTTERFLY HUG", s["QuickRefTitle"]))
    story.append(Paragraph(
        "cross arms over chest, interlock thumbs. alternate tapping "
        "gently for 1-2 min. eyes closed. bilateral stimulation.",
        s["QuickRefBody"]
    ))
    story.append(Spacer(1, 6))

    # Cold Reset
    story.append(Paragraph("COLD RESET", s["QuickRefTitle"]))
    story.append(Paragraph(
        "cold water on face/wrists, or ice cubes in palms for 30 sec. "
        "triggers dive reflex. emergency brake for panic.",
        s["QuickRefBody"]
    ))
    story.append(Spacer(1, 6))

    # 5-4-3-2-1
    story.append(Paragraph("5-4-3-2-1 GROUNDING", s["QuickRefTitle"]))
    story.append(Paragraph(
        "5 see · 4 touch · 3 hear · 2 smell · 1 taste. "
        "brings you back to the present moment.",
        s["QuickRefBody"]
    ))
    story.append(Spacer(1, 8))
    story.append(DashedLine(CONTENT_W))
    story.append(Spacer(1, 12))

    # The 30-min protocol summary
    story.append(Paragraph("THE 30-MINUTE PROTOCOL", s["QuickRefTitle"]))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "T-30: arrive in your body (feet on floor, 5 breaths)  ·  "
        "T-25: 5-4-3-2-1 ground  ·  "
        "T-20: box breathing (5 min)  ·  "
        "T-15: set your intention  ·  "
        "T-10: choose anchor phrase  ·  "
        "T-5: shake it off, walk in",
        s["QuickRefBody"]
    ))
    story.append(Spacer(1, 12))

    # Anchor phrases
    story.append(Paragraph("ANCHOR PHRASES", s["QuickRefTitle"]))
    story.append(Spacer(1, 4))
    phrases = [
        "I belong in this room.",
        "I am interviewing them too.",
        "my worth is not on the table today.",
    ]
    for p in phrases:
        story.append(Paragraph(f'  ·  "{p}"', s["QuickRefBody"]))
    story.append(Spacer(1, 8))
    story.append(DashedLine(CONTENT_W))
    story.append(Spacer(1, 12))
    story.append(Paragraph(
        "luminouspulse.co",
        s["ItalicCenter"]
    ))
    story.append(PageBreak())


# ── Notes Pages ──

def build_notes(story, s, num_pages=1):
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


# ── Main ──

def build_workbook():
    out_path = os.path.join(os.path.dirname(__file__),
                            "Before-The-Room-Workbook.pdf")

    doc = SimpleDocTemplate(
        out_path,
        pagesize=letter,
        leftMargin=MARGIN, rightMargin=MARGIN,
        topMargin=MARGIN, bottomMargin=MARGIN,
        title="before the room",
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

    # Parts 1-5
    build_part_1(story, s)     # pre-interview ground (30-min ritual)
    build_part_2(story, s)     # reframing your gap story
    build_part_3(story, s)     # nervous system toolkit
    build_part_4(story, s)     # post-interview decompression
    build_part_5(story, s)     # win or lose, I'm still me

    # Closing
    build_closing(story, s)

    # Quick reference card (tear-out)
    build_quick_reference(story, s)

    # Notes
    build_notes(story, s, num_pages=1)

    # Build with page templates
    doc.build(story, onFirstPage=draw_bg_cover, onLaterPages=draw_bg)

    # Report
    file_size = os.path.getsize(out_path) / (1024 * 1024)
    print(f"\n{'='*50}")
    print(f"  before the room — workbook generated")
    print(f"  {out_path}")
    print(f"  {file_size:.1f} MB")
    print(f"{'='*50}\n")


if __name__ == "__main__":
    build_workbook()
