#!/usr/bin/env python3
"""Generate "tender landings" workbook PDF — Luminous Pulse ($12).

A career grief journal — for the version of you that's still in the thick of it.

6 sections: naming the loss, the non-linear grief cycle, anger is welcome here,
the body keeps the score, letters you'll never send, what remains.

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


# ── Page Backgrounds ──

def draw_bg(canvas, doc):
    """Standard page background — cream with subtle footer."""
    canvas.saveState()
    canvas.setFillColor(CREAM)
    canvas.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    canvas.setFont("Helvetica", 7)
    canvas.setFillColor(SOFT_GRAY)
    canvas.drawCentredString(PAGE_W / 2, 30,
                             "tender landings  ·  luminouspulse.co")
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
    styles.add(ParagraphStyle(
        name="GriefStage", fontName="Helvetica-Bold", fontSize=11,
        textColor=NAVY, alignment=TA_LEFT, leading=16, spaceAfter=4,
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
    story.append(Paragraph("tender landings", s["CoverTitle"]))
    story.append(Spacer(1, 14))
    story.append(Paragraph(
        "a career grief journal<br/>"
        "for the version of you that's still in the thick of it.",
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
        "this is not a workbook about moving on.",
        s["PromptCenter"]
    ))
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "this is a journal for the space you're in right now. the messy, "
        "heavy, confusing part. the part where people keep telling you "
        "to see this as an opportunity, and you want to scream.",
        s["Body"]
    ))
    story.append(Paragraph(
        "losing a job — or watching your industry change so fast you can't "
        "recognize it — is a kind of grief. real grief. and like all grief, "
        "it doesn't move in a straight line. it circles. it surprises you "
        "at 2am. it hides inside productivity and then collapses into the "
        "couch at 4pm.",
        s["Body"]
    ))
    story.append(Paragraph(
        "this journal gives that grief a place to land.",
        s["BodyCenter"]
    ))
    story.append(Spacer(1, 16))
    story.append(AccentDot(AMBER))
    story.append(Spacer(1, 12))

    story.append(Paragraph("how to use this journal", s["SubHeading"]))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "<b>print it.</b> the physical act of writing activates emotional "
        "processing centers that typing cannot reach. grief especially "
        "needs your hands.",
        s["Body"]
    ))
    story.append(Paragraph(
        "<b>go at any pace.</b> one section per day, one per week, or all "
        "at once at midnight with a cup of tea. there is no schedule. "
        "there is no deadline. you have had enough of those.",
        s["Body"]
    ))
    story.append(Paragraph(
        "<b>skip what you're not ready for.</b> if a section feels too heavy, "
        "turn the page. come back when you're ready. or don't. this journal "
        "belongs to you, not to a curriculum.",
        s["Body"]
    ))
    story.append(Paragraph(
        "<b>be as messy as you need to be.</b> scribble. cross things out. "
        "tear pages out if you want to. rage is welcome. tears are welcome. "
        "numbness is welcome. whatever you're carrying, bring it here.",
        s["Body"]
    ))

    story.append(Spacer(1, 20))
    story.append(Paragraph(
        '"you are not broken for feeling this. you are awake<br/>'
        'in a world that is changing fast."',
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
        ("section 1", "naming the loss",
         "what you actually lost — beyond the job title"),
        ("section 2", "the non-linear grief cycle",
         "where you are right now — and why it keeps moving"),
        (None, "a grounding practice",
         "the 5-4-3-2-1 senses technique"),
        ("section 3", "anger is welcome here",
         "a space for the feelings nobody wants you to have"),
        ("section 4", "the body keeps the score",
         "where grief lives in your body"),
        (None, "permission slip",
         "what you're allowed to feel right now"),
        ("section 5", "letters you'll never send",
         "write to the people, the company, and yourself"),
        ("section 6", "what remains",
         "finding what survives the grief"),
    ]

    for num, title, desc in sections:
        if num:
            story.append(Paragraph(f"{num}: {title}", s["TOCSection"]))
        else:
            story.append(Paragraph(title, s["TOCItem"]))
        story.append(Paragraph(desc, s["TOCItem"]))
        story.append(Spacer(1, 3))

    story.append(Spacer(1, 8))
    story.append(HLine(CONTENT_W * 0.3, LIGHT_GRAY, 0.3))
    story.append(Spacer(1, 6))
    story.append(Paragraph("closing + notes", s["TOCSection"]))

    story.append(PageBreak())


def build_section_opener(story, s, number, title, epigraph):
    """Full-page navy section opener."""
    story.append(NavyPageBg())
    story.append(Spacer(1, 200))
    story.append(Paragraph(f"SECTION {number}", s["SectionNum"]))
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


# ── SECTION 1: Naming the Loss ──

def build_section_1(story, s):
    build_section_opener(story, s, "1", "naming the loss",
        "grief cannot begin to move<br/>until you name what was taken.")

    # Page 1: What you actually lost
    story.append(Spacer(1, 16))
    story.append(Paragraph("what you actually lost", s["SubHeading"]))
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "when you lose a job, people say \"you lost your job.\" but that's "
        "not the whole truth. you lost a dozen things at once, and most of "
        "them don't show up on a severance agreement.",
        s["Body"]
    ))
    story.append(Paragraph(
        "naming the losses — all of them — is the first step toward "
        "understanding why this hurts the way it does.",
        s["Body"]
    ))
    story.append(Spacer(1, 10))

    story.append(Paragraph("THE VISIBLE LOSSES", s["ExerciseLabel"]))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "the things other people can see that you lost:",
        s["ItalicNote"]
    ))
    story.append(Spacer(1, 6))
    story.append(WritingLines(CONTENT_W, num_lines=6))
    story.append(Spacer(1, 14))

    story.append(Paragraph("THE INVISIBLE LOSSES", s["ExerciseLabel"]))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "the things only you know you lost — the routine, the belonging, "
        "the version of yourself that existed inside that role:",
        s["ItalicNote"]
    ))
    story.append(Spacer(1, 6))
    story.append(WritingLines(CONTENT_W, num_lines=6))
    story.append(PageBreak())

    # Page 2: The surprise losses
    story.append(Spacer(1, 16))
    story.append(Paragraph("THE SURPRISE LOSSES", s["ExerciseLabel"]))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "what loss caught you off guard? the thing you didn't expect to miss "
        "— the commute, the coffee order, the sound of your team's Slack channel, "
        "the feeling of being needed at 9am:",
        s["ItalicNote"]
    ))
    story.append(Spacer(1, 8))
    story.append(WritingLines(CONTENT_W, num_lines=8))
    story.append(Spacer(1, 16))

    build_prompt_page(story, s, "NAME IT",
        "if you could give your grief a name — like naming a storm — "
        "what would you call it? why?",
        lines=7)
    story.append(PageBreak())

    # Page 3: The loss nobody asks about
    build_prompt_with_break(story, s, "DEEPER",
        "what is the loss underneath the loss? the thing you're grieving "
        "that has nothing to do with the paycheck — the thing that makes "
        "you cry in the shower or stare at the ceiling at 3am?",
        lines=12,
        note="(you don't have to share this with anyone. it's just for you.)")


# ── SECTION 2: The Non-Linear Grief Cycle ──

def build_section_2(story, s):
    build_section_opener(story, s, "2", "the non-linear<br/>grief cycle",
        "grief does not move in stages. it moves in spirals.<br/>"
        "you will visit the same feelings many times.")

    # Page 1: Mapping where you are
    story.append(Spacer(1, 16))
    story.append(Paragraph("where you are right now", s["SubHeading"]))
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "the Kübler-Ross stages — denial, anger, bargaining, depression, "
        "acceptance — were never meant to be a straight line. grief "
        "researchers now describe it as a spiral. you can feel acceptance "
        "in the morning and rage by noon. you can bargain on Monday "
        "and feel numb by Wednesday.",
        s["Body"]
    ))
    story.append(Paragraph(
        "there is nothing wrong with you. you are not going backward. "
        "you are moving through.",
        s["Body"]
    ))
    story.append(Spacer(1, 12))

    story.append(Paragraph("CHECK IN", s["ExerciseLabel"]))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "for each feeling, note when you last felt it. "
        "yesterday? this morning? right now?",
        s["ItalicNote"]
    ))
    story.append(Spacer(1, 8))

    stages = [
        ("DENIAL / NUMBNESS",
         '"this isn\'t really happening." "I\'m fine." "it\'ll work out."'),
        ("ANGER",
         '"this isn\'t fair." "they had no right." "I gave them everything."'),
        ("BARGAINING",
         '"if I had just..." "maybe if I upskill fast enough..."'),
        ("SADNESS",
         '"what\'s the point?" "I don\'t recognize my own life."'),
        ("ACCEPTANCE",
         '"this happened. I\'m still here. I don\'t know what\'s next, and that\'s okay."'),
    ]

    for stage, description in stages:
        story.append(Paragraph(stage, s["GriefStage"]))
        story.append(Paragraph(description, s["ItalicNote"]))
        story.append(WritingLines(CONTENT_W, num_lines=2, spacing=24))
        story.append(Spacer(1, 4))

    story.append(PageBreak())

    # Page 2: The spiral
    story.append(Spacer(1, 16))
    story.append(Paragraph("THE SPIRAL", s["ExerciseLabel"]))
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "grief spirals. you'll feel better on Tuesday and shattered on "
        "Friday. that doesn't mean you're failing. it means you're human. "
        "each pass through the spiral, you carry a little more "
        "understanding with you.",
        s["Body"]
    ))
    story.append(Spacer(1, 10))

    build_prompt_page(story, s, "NOTICE",
        "which stage do you visit most often? what usually triggers it — "
        "a time of day, a place, a notification, a conversation?",
        lines=7)

    build_prompt_page(story, s, "NOTICE",
        "when was the last time you felt a moment of genuine okay-ness "
        "— even brief? what were you doing? who were you with?",
        lines=7)
    story.append(PageBreak())

    # Page 3: What grief looks like for you
    build_prompt_with_break(story, s, "MAP IT",
        "describe what your grief cycle looks like across a typical week. "
        "what does Monday morning feel like? Wednesday afternoon? "
        "Sunday night? trace the shape of it.",
        lines=14)


# ── Grounding Practice (between sections 2 and 3) ──

def build_grounding_practice(story, s):
    """5-4-3-2-1 senses grounding technique."""
    story.append(Spacer(1, 20))
    story.append(Paragraph("a grounding practice", s["Heading"]))
    story.append(Spacer(1, 10))
    story.append(HLine(CONTENT_W, AMBER, 0.5))
    story.append(Spacer(1, 12))

    story.append(Paragraph(
        "before you move into the next section, come back to your body. "
        "grief lives in the mind. grounding brings you back to now.",
        s["Body"]
    ))
    story.append(Spacer(1, 12))

    story.append(Paragraph("THE 5-4-3-2-1 TECHNIQUE", s["ExerciseLabel"]))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "name what your senses are telling you right now. "
        "say each one out loud if you can.",
        s["ItalicNote"]
    ))
    story.append(Spacer(1, 8))

    senses = [
        ("5", "things you can SEE"),
        ("4", "things you can TOUCH"),
        ("3", "things you can HEAR"),
        ("2", "things you can SMELL"),
        ("1", "thing you can TASTE"),
    ]

    for num, sense in senses:
        story.append(NumberedCircle(int(num)))
        story.append(Spacer(1, 2))
        story.append(Paragraph(sense, s["Body"]))
        story.append(WritingLines(CONTENT_W, num_lines=1, spacing=24))
        story.append(Spacer(1, 4))

    story.append(Spacer(1, 12))
    story.append(Paragraph("AFTER THE PRACTICE", s["ExerciseLabel"]))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "what shifted? even slightly?",
        s["Prompt"]
    ))
    story.append(WritingLines(CONTENT_W, num_lines=4))
    story.append(PageBreak())


# ── SECTION 3: Anger Is Welcome Here ──

def build_section_3(story, s):
    build_section_opener(story, s, "3", "anger is<br/>welcome here",
        "you have every right to be furious.<br/>"
        "this is the page where you don't have to be polite.")

    # Page 1: Permission to rage
    story.append(Spacer(1, 16))
    story.append(Paragraph(
        "most people in your life right now are uncomfortable with your anger. "
        "they want you to be positive. they want you to see the bright side. "
        "they want you to pivot, to upskill, to rebrand yourself.",
        s["Body"]
    ))
    story.append(Paragraph(
        "this section is not for them. this section is for you. "
        "the version of you that wants to throw something. "
        "the version that wants to scream into a pillow. "
        "the version that is tired of being told to be grateful.",
        s["Body"]
    ))
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "anger is not the opposite of healing. it is part of it.",
        s["BodyCenter"]
    ))
    story.append(Spacer(1, 12))

    build_prompt_page(story, s, "THE RAGE LIST",
        "write everything you're angry about. no filter. no qualifications. "
        "no \"but I know I should be grateful.\" just the raw, unedited truth. "
        "let the pen move fast.",
        lines=14)
    story.append(PageBreak())

    # Page 2: Who are you angry at
    story.append(Spacer(1, 16))
    story.append(Paragraph("WHO", s["ExerciseLabel"]))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "who are you angry at? your manager? the company? the industry? "
        "yourself? the economy? name them. you don't have to forgive "
        "anyone on this page.",
        s["Prompt"]
    ))
    story.append(Spacer(1, 8))
    story.append(WritingLines(CONTENT_W, num_lines=8))
    story.append(Spacer(1, 14))

    build_prompt_page(story, s, "THE UNFAIR THING",
        "what is the single most unfair thing about what happened to you? "
        "say it plainly. don't soften it.",
        lines=7)
    story.append(PageBreak())

    # Page 3: What anger is protecting
    story.append(Spacer(1, 16))
    story.append(Paragraph("UNDERNEATH THE ANGER", s["ExerciseLabel"]))
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "anger is almost always a bodyguard for a softer feeling. "
        "underneath rage, there is usually hurt. or fear. or grief. "
        "or love for something that was taken.",
        s["Body"]
    ))
    story.append(Spacer(1, 10))

    build_prompt_page(story, s, "LOOK UNDERNEATH",
        "if you peeled back the anger, what feeling is hiding behind it? "
        "what is the anger protecting you from feeling?",
        lines=8)

    story.append(Spacer(1, 6))
    story.append(HLine(CONTENT_W * 0.3, AMBER, 0.4))
    story.append(Spacer(1, 10))
    story.append(Paragraph(
        "you are allowed to be angry. you are allowed to be angry "
        "for as long as you need to be. the anger will move when it's ready. "
        "you do not need to rush it.",
        s["ItalicCenter"]
    ))
    story.append(PageBreak())


# ── SECTION 4: The Body Keeps the Score ──

def build_section_4(story, s):
    build_section_opener(story, s, "4", "the body keeps<br/>the score",
        "your body has been carrying this loss<br/>"
        "even when your mind was pretending to be fine.")

    # Page 1: Body mapping
    story.append(Spacer(1, 16))
    story.append(Paragraph("where grief lives in your body", s["SubHeading"]))
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "grief is not just an emotion. it is a physical experience. "
        "your body registered the loss before your mind fully processed it. "
        "it is still carrying it — in your jaw, your chest, your stomach, "
        "your shoulders, your sleep.",
        s["Body"]
    ))
    story.append(Spacer(1, 8))

    areas = [
        ("HEAD + JAW",
         "headaches? clenching? grinding teeth at night?"),
        ("THROAT + VOICE",
         "a lump? words you can't say? the feeling of being silenced?"),
        ("CHEST + HEART",
         "tightness? a hollow feeling? racing heart? difficulty breathing?"),
        ("STOMACH + GUT",
         "nausea? loss of appetite? stress eating? the knot that won't untie?"),
        ("SHOULDERS + BACK",
         "tension? pain? the posture of someone bracing for impact?"),
        ("SLEEP",
         "insomnia? oversleeping? waking at 3am with your mind racing?"),
    ]

    for area, prompt in areas:
        story.append(Paragraph(area, s["ExerciseLabel"]))
        story.append(Paragraph(prompt, s["ItalicNote"]))
        story.append(WritingLines(CONTENT_W, num_lines=2, spacing=22))
        story.append(Spacer(1, 2))

    story.append(PageBreak())

    # Page 2: The body's message
    build_prompt_page(story, s, "LISTEN",
        "if your body could speak right now — if the tension in your "
        "shoulders or the knot in your stomach could form words — "
        "what would it say?",
        lines=8)

    build_prompt_page(story, s, "TEND",
        "what is one small, kind thing you could do for your body today? "
        "not exercise. not optimization. just tenderness. a bath. a walk. "
        "lying on the floor. stretching. resting.",
        lines=6)
    story.append(PageBreak())

    # Page 3: What your body remembers
    build_prompt_with_break(story, s, "REMEMBER",
        "your body remembers what safety feels like. describe a time "
        "when your body felt completely safe and at ease. where were you? "
        "what did the air feel like? what could you hear?",
        lines=12,
        note="(hold that memory in your body for a moment. breathe into it.)")


# ── Permission Slip (between sections 4 and 5) ──

def build_permission_slip(story, s):
    """Permission slip — grief-specific permissions."""
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
        "I have permission to grieve a job like I'd grieve any loss.",
        "I have permission to not be okay right now.",
        "I have permission to cry about this, even if other people have it worse.",
        "I have permission to be angry at people I used to admire.",
        "I have permission to take a day where I do absolutely nothing.",
        "I have permission to not have a plan yet.",
        "I have permission to stop pretending I'm \"exploring new opportunities.\"",
        "I have permission to say no to networking events.",
        "I have permission to miss my old life without wanting it back.",
        "I have permission to feel relieved and guilty about the relief.",
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


# ── SECTION 5: Letters You'll Never Send ──

def build_section_5(story, s):
    build_section_opener(story, s, "5", "letters you'll<br/>never send",
        "write to the people, the company, and yourself.<br/>"
        "you do not need to send these. you just need to write them.")

    # Page 1: Letter to the person
    story.append(Spacer(1, 16))
    story.append(Paragraph(
        "unsent letters are one of the most powerful grief tools there is. "
        "writing what you cannot say out loud moves it from your chest "
        "to the page. the page can hold it. your chest was never meant to.",
        s["Body"]
    ))
    story.append(Spacer(1, 8))

    story.append(Paragraph("LETTER 1: TO THE PERSON", s["ExerciseLabel"]))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "write to the person most connected to your loss — a manager, "
        "a CEO, a colleague who stayed, or yourself. say what you "
        "couldn't say in the exit interview.",
        s["ItalicNote"]
    ))
    story.append(Spacer(1, 8))
    story.append(Paragraph("dear _______________,", s["Prompt"]))
    story.append(Spacer(1, 4))
    story.append(WritingLines(CONTENT_W, num_lines=16))
    story.append(PageBreak())

    # Page 2: Letter to the company/industry
    story.append(Spacer(1, 16))
    story.append(Paragraph("LETTER 2: TO THE COMPANY (OR THE INDUSTRY)",
                            s["ExerciseLabel"]))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "write to the organization, the industry, or the system. "
        "tell it what it took from you. tell it what it can never take.",
        s["ItalicNote"]
    ))
    story.append(Spacer(1, 8))
    story.append(Paragraph("dear _______________,", s["Prompt"]))
    story.append(Spacer(1, 4))
    story.append(WritingLines(CONTENT_W, num_lines=18))
    story.append(PageBreak())

    # Page 3: Letter to yourself
    story.append(Spacer(1, 16))
    story.append(Paragraph("LETTER 3: TO YOURSELF", s["ExerciseLabel"]))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "write to the version of you that is hurting right now. "
        "write to them the way you would write to a friend. "
        "with tenderness, not advice.",
        s["ItalicNote"]
    ))
    story.append(Spacer(1, 8))
    story.append(Paragraph("dear me,", s["Prompt"]))
    story.append(Spacer(1, 4))
    story.append(WritingLines(CONTENT_W, num_lines=18))
    story.append(PageBreak())

    # Page 4: After the letters
    story.append(Spacer(1, 20))
    story.append(Paragraph("AFTER THE LETTERS", s["ExerciseLabel"]))
    story.append(Spacer(1, 10))
    story.append(Paragraph(
        "sit with what you wrote. you don't need to do anything with it. "
        "you can keep these letters. you can burn them. you can fold them "
        "into paper airplanes and throw them off a bridge. the point was "
        "never the destination. the point was getting it out of your chest.",
        s["Body"]
    ))
    story.append(Spacer(1, 12))

    build_prompt_page(story, s, "NOTICE",
        "what do you feel in your body right now, after writing those letters? "
        "lighter? heavier? emptier? more full? name it.",
        lines=6)

    build_prompt_page(story, s, "RELEASE",
        "what is the one thing you said in those letters that you most "
        "needed someone to hear? write it here, one more time, "
        "as clearly as you can.",
        lines=6)
    story.append(PageBreak())


# ── SECTION 6: What Remains ──

def build_section_6(story, s):
    build_section_opener(story, s, "6", "what remains",
        "after the loss, after the grief, after the anger —<br/>"
        "there is still something here. there is still you.")

    # Page 1: What survived
    story.append(Spacer(1, 16))
    story.append(Paragraph("what survived", s["SubHeading"]))
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "grief has a way of stripping everything down to what's essential. "
        "underneath all the titles and routines and Slack channels and "
        "performance reviews, there is a person. and that person is still "
        "here. bruised, maybe. tired, certainly. but here.",
        s["Body"]
    ))
    story.append(Spacer(1, 10))

    build_prompt_page(story, s, "NAME IT",
        "what parts of you survived this loss completely intact? "
        "what did the grief not touch?",
        lines=8)

    build_prompt_page(story, s, "NAME IT",
        "what surprised you about your own resilience? "
        "what did you not expect to be able to handle — but you did?",
        lines=6)
    story.append(PageBreak())

    # Page 2: What you're learning
    story.append(Spacer(1, 16))
    story.append(Paragraph("WHAT YOU'RE LEARNING", s["ExerciseLabel"]))
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "this is not \"what doesn't kill you makes you stronger.\" "
        "you do not have to be stronger. but you may be learning "
        "something — about yourself, about what matters, about what "
        "you refuse to go back to.",
        s["Body"]
    ))
    story.append(Spacer(1, 10))

    build_prompt_page(story, s, "NOTICE",
        "what are you learning about yourself that you could only "
        "have learned through this experience?",
        lines=8)

    build_prompt_page(story, s, "NOTICE",
        "what do you refuse to go back to? what boundary, what truth, "
        "what standard for how you're treated — what line in the sand "
        "did this experience draw for you?",
        lines=6)
    story.append(PageBreak())

    # Page 3: What you still want
    story.append(Spacer(1, 16))
    story.append(Paragraph("WHAT YOU STILL WANT", s["ExerciseLabel"]))
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "this is not career planning. this is not goal-setting. "
        "this is a softer question: in the middle of the grief, "
        "what quiet desires are still alive in you?",
        s["Body"]
    ))
    story.append(Spacer(1, 10))

    build_prompt_page(story, s, "WANT",
        "what do you still want — not from a job, but from your life? "
        "what kind of days do you want to have? what kind of mornings? "
        "what kind of relationships?",
        lines=8)

    build_prompt_page(story, s, "WANT",
        "if you could whisper one thing to the version of you from "
        "six months ago — the version that didn't know this was coming — "
        "what would you say?",
        lines=6)
    story.append(PageBreak())

    # Page 4: One true sentence
    story.append(Spacer(1, 30))
    story.append(Paragraph("ONE TRUE SENTENCE", s["ExerciseLabel"]))
    story.append(Spacer(1, 12))
    story.append(Paragraph(
        "Ernest Hemingway, when he was stuck, would tell himself: "
        "\"write one true sentence. write the truest sentence you know.\"",
        s["Body"]
    ))
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "write one true sentence about where you are right now. "
        "not where you should be. not where you're going. just the truth "
        "of this exact moment.",
        s["Body"]
    ))
    story.append(Spacer(1, 20))
    story.append(WritingLines(CONTENT_W, num_lines=3, spacing=32))
    story.append(Spacer(1, 30))
    story.append(HLine(CONTENT_W * 0.3, AMBER, 0.4))
    story.append(Spacer(1, 16))
    story.append(Paragraph(
        "that sentence is the ground you're standing on. it's enough.",
        s["ItalicCenter"]
    ))
    story.append(PageBreak())


# ── Closing Page ──

def build_closing(story, s):
    story.append(Spacer(1, 80))
    story.append(Paragraph("you made it here.", s["Heading"]))
    story.append(Spacer(1, 16))
    story.append(HLine(CONTENT_W * 0.3, AMBER, 0.6))
    story.append(Spacer(1, 20))
    story.append(Paragraph(
        "not to the other side. not to the end. grief doesn't work "
        "like that. but you made it to a place where you could look "
        "at what happened and write about it. that is not nothing. "
        "that is enormous.",
        s["BodyCenter"]
    ))
    story.append(Spacer(1, 12))
    story.append(Paragraph(
        "you named what was lost. you let yourself feel the anger. "
        "you listened to your body. you wrote the letters. "
        "you found what remains.",
        s["BodyCenter"]
    ))
    story.append(Spacer(1, 12))
    story.append(Paragraph(
        "come back to these pages whenever you need to. grief circles. "
        "you might need to reread your own words in three weeks, "
        "or three months. they'll still be here.",
        s["BodyCenter"]
    ))
    story.append(Spacer(1, 24))
    story.append(Paragraph(
        '"I survived every worst day I ever had.<br/>'
        'my track record is 100%."',
        s["Affirmation"]
    ))
    story.append(Spacer(1, 30))
    story.append(AccentDot(AMBER))
    story.append(Spacer(1, 20))
    story.append(Paragraph(
        "when you're ready for what comes after the grief —",
        s["BodyCenter"]
    ))
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        '"who am I without the title?" — 8 exercises for reclaiming<br/>'
        "who you are beyond your job.",
        s["ItalicCenter"]
    ))
    story.append(Spacer(1, 4))
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


# ── Main ──

def build_workbook():
    out_path = os.path.join(os.path.dirname(__file__),
                            "Tender-Landings-Workbook.pdf")

    doc = SimpleDocTemplate(
        out_path,
        pagesize=letter,
        leftMargin=MARGIN, rightMargin=MARGIN,
        topMargin=MARGIN, bottomMargin=MARGIN,
        title="tender landings",
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

    # Sections 1-6 with interludes
    build_section_1(story, s)    # naming the loss
    build_section_2(story, s)    # the non-linear grief cycle
    build_grounding_practice(story, s)  # interlude
    build_section_3(story, s)    # anger is welcome here
    build_section_4(story, s)    # the body keeps the score
    build_permission_slip(story, s)     # interlude
    build_section_5(story, s)    # letters you'll never send
    build_section_6(story, s)    # what remains

    # Closing
    build_closing(story, s)

    # Notes
    build_notes(story, s, num_pages=2)

    # Build with page templates
    doc.build(story, onFirstPage=draw_bg_cover, onLaterPages=draw_bg)

    # Report
    file_size = os.path.getsize(out_path) / (1024 * 1024)
    print(f"\n{'='*50}")
    print(f"  tender landings — workbook generated")
    print(f"  {out_path}")
    print(f"  {file_size:.1f} MB")
    print(f"{'='*50}\n")

    # Count pages (approximate from story)
    page_breaks = sum(1 for item in story if isinstance(item, PageBreak))
    print(f"  approximate pages: {page_breaks + 1}")


if __name__ == "__main__":
    build_workbook()
