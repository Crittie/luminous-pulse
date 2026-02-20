#!/usr/bin/env python3
"""Generate "steady" workbook PDF — Luminous Pulse ($15).

12 weeks of checking in with yourself.

Each week: Monday intention, mid-week check-in, Friday reflection,
weekend analog activity. Plus 3 monthly reviews.

Design: Printable on cream/off-white background. Navy + amber accents.
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


# ── Custom Flowables ──

class WritingLines(Flowable):
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


class CheckboxLine(Flowable):
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


# ── Page Backgrounds ──

def draw_bg(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(CREAM)
    canvas.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    canvas.setFont("Helvetica", 7)
    canvas.setFillColor(SOFT_GRAY)
    canvas.drawCentredString(PAGE_W / 2, 30,
                             "steady  ·  luminouspulse.co")
    page_num = canvas.getPageNumber()
    if page_num > 2:
        canvas.drawRightString(PAGE_W - MARGIN, 30, str(page_num))
    canvas.restoreState()


def draw_bg_cover(canvas, doc):
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
    styles.add(ParagraphStyle(
        name="Heading", fontName="Helvetica-Bold", fontSize=20,
        textColor=NAVY, alignment=TA_CENTER, leading=26, spaceAfter=16,
    ))
    styles.add(ParagraphStyle(
        name="SubHeading", fontName="Helvetica-Bold", fontSize=13,
        textColor=NAVY, alignment=TA_LEFT, leading=18, spaceAfter=8,
    ))
    styles.add(ParagraphStyle(
        name="WeekLabel", fontName="Helvetica", fontSize=9,
        textColor=AMBER_SOFT, alignment=TA_LEFT, leading=13, spaceAfter=2,
        letterSpacing=2,
    ))
    styles.add(ParagraphStyle(
        name="DayLabel", fontName="Helvetica-Bold", fontSize=11,
        textColor=NAVY, alignment=TA_LEFT, leading=16, spaceAfter=6,
    ))
    styles.add(ParagraphStyle(
        name="ExerciseLabel", fontName="Helvetica-Bold", fontSize=10,
        textColor=AMBER_SOFT, alignment=TA_LEFT, leading=14, spaceAfter=4,
        letterSpacing=2,
    ))
    styles.add(ParagraphStyle(
        name="Prompt", fontName="Helvetica-Oblique", fontSize=12,
        textColor=NAVY, alignment=TA_LEFT, leading=18, spaceAfter=10,
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
        name="MicroAffirmation", fontName="Helvetica-Oblique", fontSize=10,
        textColor=NAVY_LIGHT, alignment=TA_CENTER, leading=15, spaceAfter=4,
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
        name="AnalogBox", fontName="Helvetica", fontSize=10,
        textColor=HexColor("#555555"), alignment=TA_LEFT, leading=15, spaceAfter=6,
    ))

    return styles


# ── 12 Weeks Content ──

WEEKS = [
    # Month 1: Grounding
    {
        "theme": "the ground beneath you",
        "monday": "what is one thing you want to feel this week? not accomplish. feel.",
        "midweek": "it's Wednesday. check in: are you closer to that feeling or further away? what shifted?",
        "friday": "what surprised you about this week? what do you know now that you didn't know on Monday?",
        "analog": "walk for 20 minutes without your phone. notice 5 things you wouldn't normally see.",
        "affirmation": "I begin where I am. that is always enough.",
    },
    {
        "theme": "what you're carrying",
        "monday": "what are you carrying into this week that isn't yours to hold?",
        "midweek": "where in your body do you feel the weight of what you're carrying? name the spot.",
        "friday": "what did you put down this week — even briefly? how did it feel to set it down?",
        "analog": "clean one small space in your home — a drawer, a shelf, a corner. make it feel like yours.",
        "affirmation": "I am allowed to set things down.",
    },
    {
        "theme": "permission",
        "monday": "what do you need permission to do this week? give it to yourself in writing.",
        "midweek": "did you take the permission you gave yourself on Monday? if not, what got in the way?",
        "friday": "what would your week have looked like if you'd given yourself more permission?",
        "analog": "say no to one thing this weekend. protect your time like it's sacred. because it is.",
        "affirmation": "I do not need anyone's approval to take care of myself.",
    },
    {
        "theme": "the pace you need",
        "monday": "how fast are you moving right now? is it your pace or someone else's?",
        "midweek": "what would slow enough feel like? describe it in sensory detail.",
        "friday": "when this week did you feel most like yourself? what was the pace of that moment?",
        "analog": "cook a meal from scratch. slowly. taste everything. let it take as long as it takes.",
        "affirmation": "I move at my own pace. that pace is enough.",
    },
    # Month 2: Reconnecting
    {
        "theme": "who sees you",
        "monday": "who in your life sees the real you — not the résumé version? set an intention to reach out to one of them.",
        "midweek": "have you reached out yet? if not, this is your nudge. if yes, how did it feel?",
        "friday": "what kind of connection did you most need this week? did you get it?",
        "analog": "call someone you love. not to vent or update. just to hear their voice.",
        "affirmation": "connection is not a soft skill. it is the infrastructure of everything.",
    },
    {
        "theme": "what you still love",
        "monday": "what are you still curious about — even in the middle of the uncertainty?",
        "midweek": "did you follow any curiosity this week? even for 10 minutes?",
        "friday": "what brought you the most genuine pleasure this week? how small was it?",
        "analog": "spend 30 minutes doing something purely for enjoyment. not for productivity. not for growth. for fun.",
        "affirmation": "my creativity doesn't run on electricity. it runs on living.",
    },
    {
        "theme": "the body's truth",
        "monday": "what is your body trying to tell you this Monday morning? listen before you plan.",
        "midweek": "how did your body feel after the best moment of this week so far?",
        "friday": "where is your body holding this week? jaw? shoulders? stomach? breathe into that place.",
        "analog": "stretch, walk, swim, dance, or lie on the floor. let your body move without an app telling it how.",
        "affirmation": "my body knows things my mind has forgotten. I listen.",
    },
    {
        "theme": "anger and tenderness",
        "monday": "what are you angry about this week? name it without softening it.",
        "midweek": "underneath the anger, what's the softer feeling? fear? grief? love for something lost?",
        "friday": "where did tenderness show up this week? toward yourself or from someone else?",
        "analog": "write an unsent letter. to a person, a company, a version of yourself. then put it away.",
        "affirmation": "I can hold anger and tenderness at the same time. that is not confusion. that is depth.",
    },
    # Month 3: Building
    {
        "theme": "what you're learning",
        "monday": "what are you learning about yourself right now — something you could only learn through this experience?",
        "midweek": "how are you different from the person who started this workbook? be specific.",
        "friday": "what did you handle this week that the version of you from 2 months ago would be proud of?",
        "analog": "go somewhere you've never been. a new café, a different park, a part of town you don't know.",
        "affirmation": "I am not the same person I was at the start. that's the point.",
    },
    {
        "theme": "one small brave thing",
        "monday": "what is one small brave thing you could do this week? not big. not heroic. just slightly outside your comfort zone.",
        "midweek": "have you done the brave thing yet? if yes, what happened? if not, what's the smallest version of it you could do today?",
        "friday": "looking back at the week: when were you brave without even realizing it?",
        "analog": "start a conversation with someone new — a neighbor, a barista, a stranger at the park.",
        "affirmation": "courage is not the absence of fear. it is one small step while afraid.",
    },
    {
        "theme": "what you refuse",
        "monday": "what do you refuse to go back to? what line in the sand has this experience drawn?",
        "midweek": "are you living in accordance with that refusal? where are the gaps?",
        "friday": "what boundary did you hold this week — even a small one? how did it feel?",
        "analog": "write a list of 5 non-negotiables for your next chapter. keep it somewhere visible.",
        "affirmation": "my standards are not rigid. they are the shape of my self-respect.",
    },
    {
        "theme": "what's next (gently)",
        "monday": "if you could design the next 3 months — not as a plan but as a feeling — what would they feel like?",
        "midweek": "what is one small action you could take today that points in the direction of that feeling?",
        "friday": "12 weeks ago, you started this practice. write one true sentence about who you are now.",
        "analog": "write a letter to yourself, to be opened in 3 months. seal it. date it. put it away.",
        "affirmation": "I am becoming someone who can hold whatever comes next. and that is enough.",
    },
]


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
    story.append(Paragraph("steady", s["CoverTitle"]))
    story.append(Spacer(1, 14))
    story.append(Paragraph(
        "12 weeks of checking in with yourself.",
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
        "this is a practice of returning to yourself.",
        s["PromptCenter"]
    ))
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "not a course. not a challenge. not a transformation program. "
        "just a weekly rhythm of checking in — with your body, your mind, "
        "your feelings, and the version of you that exists when you put "
        "the phone down.",
        s["Body"]
    ))
    story.append(Paragraph(
        "each week has four touchpoints: a Monday intention, a mid-week "
        "check-in, a Friday reflection, and a weekend analog activity. "
        "some weeks you'll do all four. some weeks you'll manage one. "
        "both are fine. the practice is in the returning.",
        s["Body"]
    ))
    story.append(Spacer(1, 16))
    story.append(AccentDot(AMBER))
    story.append(Spacer(1, 12))

    story.append(Paragraph("how to use this workbook", s["SubHeading"]))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "<b>print it.</b> handwriting activates emotional processing "
        "centers that typing cannot reach.",
        s["Body"]
    ))
    story.append(Paragraph(
        "<b>start on a Monday.</b> any Monday. set a recurring reminder "
        "for Monday morning, Wednesday evening, and Friday afternoon.",
        s["Body"]
    ))
    story.append(Paragraph(
        "<b>do the analog activity.</b> it's the most important part. "
        "the writing is the reflection. the analog activity is the practice.",
        s["Body"]
    ))
    story.append(Paragraph(
        "<b>if you miss a week, don't restart.</b> just pick up at the "
        "next week. there is no scoreboard. there is no streak to protect.",
        s["Body"]
    ))

    story.append(Spacer(1, 20))
    story.append(Paragraph(
        '"today I move at my own pace. that pace is enough."',
        s["AffirmationLight"]
    ))
    story.append(PageBreak())


def build_month_opener(story, s, month_num, title, description):
    """Navy page to mark the start of a month."""
    story.append(NavyPageBg())
    story.append(Spacer(1, 200))
    story.append(Paragraph(f"MONTH {month_num}", s["SectionNum"]))
    story.append(Spacer(1, 12))
    story.append(Paragraph(title, s["SectionTitle"]))
    story.append(Spacer(1, 20))
    story.append(Paragraph(description, s["SectionEpigraph"]))
    story.append(PageBreak())


def build_week_spread(story, s, week_num, week):
    """Build a 4-page weekly spread: Monday + Mid-week + Friday + Weekend."""
    # Page 1: Monday Intention
    story.append(Spacer(1, 12))
    story.append(Paragraph(f"WEEK {week_num}", s["WeekLabel"]))
    story.append(Paragraph(week["theme"], s["SubHeading"]))
    story.append(HLine(CONTENT_W, AMBER, 0.4))
    story.append(Spacer(1, 10))

    story.append(Paragraph("MONDAY INTENTION", s["ExerciseLabel"]))
    story.append(Spacer(1, 4))
    story.append(Paragraph("date: _______________", s["ItalicNote"]))
    story.append(Spacer(1, 6))
    story.append(Paragraph(week["monday"], s["Prompt"]))
    story.append(Spacer(1, 6))
    story.append(WritingLines(CONTENT_W, num_lines=10, spacing=26))
    story.append(Spacer(1, 10))
    story.append(Paragraph(
        f'"{week["affirmation"]}"',
        s["MicroAffirmation"]
    ))
    story.append(PageBreak())

    # Page 2: Mid-week Check-in
    story.append(Spacer(1, 12))
    story.append(Paragraph(f"WEEK {week_num}", s["WeekLabel"]))
    story.append(Spacer(1, 4))
    story.append(Paragraph("MID-WEEK CHECK-IN", s["ExerciseLabel"]))
    story.append(Spacer(1, 4))
    story.append(Paragraph("date: _______________", s["ItalicNote"]))
    story.append(HLine(CONTENT_W, LIGHT_GRAY, 0.3))
    story.append(Spacer(1, 8))

    story.append(Paragraph(week["midweek"], s["Prompt"]))
    story.append(Spacer(1, 6))
    story.append(WritingLines(CONTENT_W, num_lines=8, spacing=26))
    story.append(Spacer(1, 10))

    # Quick body check
    story.append(Paragraph("BODY CHECK", s["ExerciseLabel"]))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "right now: jaw (clenching?) · shoulders (up?) · "
        "stomach (knotted?) · breath (shallow?)",
        s["ItalicNote"]
    ))
    story.append(WritingLines(CONTENT_W, num_lines=3, spacing=24))
    story.append(PageBreak())

    # Page 3: Friday Reflection
    story.append(Spacer(1, 12))
    story.append(Paragraph(f"WEEK {week_num}", s["WeekLabel"]))
    story.append(Spacer(1, 4))
    story.append(Paragraph("FRIDAY REFLECTION", s["ExerciseLabel"]))
    story.append(Spacer(1, 4))
    story.append(Paragraph("date: _______________", s["ItalicNote"]))
    story.append(HLine(CONTENT_W, LIGHT_GRAY, 0.3))
    story.append(Spacer(1, 8))

    story.append(Paragraph(week["friday"], s["Prompt"]))
    story.append(Spacer(1, 6))
    story.append(WritingLines(CONTENT_W, num_lines=8, spacing=26))
    story.append(Spacer(1, 10))

    # Gratitude + one word
    story.append(Paragraph("ONE GOOD THING THIS WEEK", s["ExerciseLabel"]))
    story.append(Spacer(1, 4))
    story.append(WritingLines(CONTENT_W, num_lines=2, spacing=26))
    story.append(Spacer(1, 8))
    story.append(Paragraph("ONE WORD FOR THIS WEEK", s["ExerciseLabel"]))
    story.append(Spacer(1, 4))
    story.append(WritingLines(CONTENT_W, num_lines=1, spacing=28))
    story.append(PageBreak())

    # Page 4: Weekend Analog Activity
    story.append(Spacer(1, 12))
    story.append(Paragraph(f"WEEK {week_num}", s["WeekLabel"]))
    story.append(Spacer(1, 4))
    story.append(Paragraph("WEEKEND: ONE OFFLINE THING", s["ExerciseLabel"]))
    story.append(HLine(CONTENT_W, LAVENDER, 0.4))
    story.append(Spacer(1, 10))

    story.append(Paragraph(week["analog"], s["Body"]))
    story.append(Spacer(1, 12))

    story.append(Paragraph("AFTER", s["ExerciseLabel"]))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "how did that feel? what did you notice?",
        s["Prompt"]
    ))
    story.append(WritingLines(CONTENT_W, num_lines=8, spacing=26))
    story.append(Spacer(1, 16))
    story.append(HLine(CONTENT_W * 0.3, AMBER, 0.3))
    story.append(Spacer(1, 10))
    story.append(Paragraph(
        f'"{week["affirmation"]}"',
        s["MicroAffirmation"]
    ))
    story.append(PageBreak())


def build_monthly_review(story, s, month_num):
    """A 2-page monthly review."""
    story.append(Spacer(1, 30))
    story.append(Paragraph(f"month {month_num} review", s["Heading"]))
    story.append(Spacer(1, 10))
    story.append(HLine(CONTENT_W, AMBER, 0.5))
    story.append(Spacer(1, 14))

    story.append(Paragraph("LOOK BACK", s["ExerciseLabel"]))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "what was the theme of this month — not one you planned, "
        "but one that emerged on its own?",
        s["Prompt"]
    ))
    story.append(WritingLines(CONTENT_W, num_lines=4, spacing=26))
    story.append(Spacer(1, 8))

    story.append(Paragraph(
        "which week hit the hardest? what made it hard?",
        s["Prompt"]
    ))
    story.append(WritingLines(CONTENT_W, num_lines=4, spacing=26))
    story.append(Spacer(1, 8))

    story.append(Paragraph(
        "which analog activity did you actually enjoy the most?",
        s["Prompt"]
    ))
    story.append(WritingLines(CONTENT_W, num_lines=3, spacing=26))
    story.append(PageBreak())

    # Page 2
    story.append(Spacer(1, 20))
    story.append(Paragraph("LOOK INWARD", s["ExerciseLabel"]))
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "what shifted in you over these 4 weeks? it can be small.",
        s["Prompt"]
    ))
    story.append(WritingLines(CONTENT_W, num_lines=5, spacing=26))
    story.append(Spacer(1, 10))

    story.append(Paragraph("LOOK AHEAD", s["ExerciseLabel"]))
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "what do you want next month to feel like? "
        "not what you want to accomplish. what you want to feel.",
        s["Prompt"]
    ))
    story.append(WritingLines(CONTENT_W, num_lines=5, spacing=26))
    story.append(Spacer(1, 12))

    month_affirmations = {
        1: "I have spent a month returning to myself. that is not nothing.",
        2: "I am not the same person I was 8 weeks ago. and that's exactly right.",
        3: "12 weeks of steady. I am the kind of person who shows up for themselves.",
    }
    aff = month_affirmations.get(month_num, "I am steady.")
    story.append(HLine(CONTENT_W * 0.3, AMBER, 0.4))
    story.append(Spacer(1, 12))
    story.append(Paragraph(f'"{aff}"', s["AffirmationLight"]))
    story.append(PageBreak())


def build_closing(story, s):
    story.append(Spacer(1, 80))
    story.append(Paragraph("steady.", s["Heading"]))
    story.append(Spacer(1, 16))
    story.append(HLine(CONTENT_W * 0.3, AMBER, 0.6))
    story.append(Spacer(1, 20))
    story.append(Paragraph(
        "twelve weeks. forty-eight check-ins. twelve analog activities. "
        "twelve one-word summaries. not because anyone graded you on it. "
        "because you chose to keep returning to yourself.",
        s["BodyCenter"]
    ))
    story.append(Spacer(1, 12))
    story.append(Paragraph(
        "the practice doesn't end here. start over at week 1. "
        "the same prompts will land differently because you're different. "
        "or keep the rhythm on your own: Monday intention, mid-week check, "
        "Friday reflection, one analog thing. that's the practice. "
        "that's all it's ever been.",
        s["BodyCenter"]
    ))
    story.append(Spacer(1, 24))
    story.append(Paragraph(
        '"I welcome today with steady hands and a clear mind."',
        s["Affirmation"]
    ))
    story.append(Spacer(1, 30))
    story.append(AccentDot(AMBER))
    story.append(Spacer(1, 20))
    story.append(Paragraph(
        "the full luminous pulse collection —",
        s["BodyCenter"]
    ))
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        '"who am I without the title?" · "tender landings" · '
        '"before the room" · "30 days of ground" · "the in-between"',
        s["ItalicCenter"]
    ))
    story.append(Spacer(1, 8))
    story.append(Paragraph("luminouspulse.co", s["CTA"]))
    story.append(PageBreak())


def build_notes(story, s, num_pages=2):
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

MONTH_THEMES = [
    ("grounding", "the first month is about landing.<br/>"
     "feeling the ground. noticing the body. slowing the pace."),
    ("reconnecting", "the second month is about remembering.<br/>"
     "who you are. who sees you. what you still love."),
    ("building", "the third month is about planting.<br/>"
     "not rushing. not planning. just small brave steps."),
]


def build_workbook():
    out_path = os.path.join(os.path.dirname(__file__),
                            "Steady-Workbook.pdf")

    doc = SimpleDocTemplate(
        out_path,
        pagesize=letter,
        leftMargin=MARGIN, rightMargin=MARGIN,
        topMargin=MARGIN, bottomMargin=MARGIN,
        title="steady",
        author="Luminous Pulse · luminouspulse.co",
    )

    s = create_styles()
    story = []

    build_cover(story, s)
    build_intro(story, s)

    # 3 months × 4 weeks
    for month_idx in range(3):
        theme, desc = MONTH_THEMES[month_idx]
        build_month_opener(story, s, month_idx + 1, theme, desc)

        start_week = month_idx * 4
        for w in range(4):
            week_num = start_week + w + 1
            build_week_spread(story, s, week_num, WEEKS[start_week + w])

        build_monthly_review(story, s, month_idx + 1)

    build_closing(story, s)
    build_notes(story, s, num_pages=2)

    doc.build(story, onFirstPage=draw_bg_cover, onLaterPages=draw_bg)

    file_size = os.path.getsize(out_path) / (1024 * 1024)
    print(f"\n{'='*50}")
    print(f"  steady — workbook generated")
    print(f"  {out_path}")
    print(f"  {file_size:.1f} MB")
    print(f"{'='*50}\n")


if __name__ == "__main__":
    build_workbook()
