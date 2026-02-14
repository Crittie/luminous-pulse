#!/usr/bin/env python3
"""Generate the 5-Day Grounding Practice lead magnet PDF for Luminous Pulse."""

from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import HexColor, Color
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, Image
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.platypus.flowables import Flowable
import os

# Brand colors
NAVY = HexColor("#1a1a2e")
DEEP_NAVY = HexColor("#16213e")
BLUE = HexColor("#6CB4EE")
AMBER = HexColor("#F4C430")
LAVENDER = HexColor("#B4A7D6")
WHITE = HexColor("#FFFFFF")
SOFT_WHITE = HexColor("#e8e8e8")
DIM_WHITE = HexColor("#999999")
SOFT_NAVY = HexColor("#2a3a5c")

PAGE_W, PAGE_H = letter


class NavyBackground(Flowable):
    """Draw navy background on every page."""
    def __init__(self, width, height):
        Flowable.__init__(self)
        self.width = width
        self.height = height

    def draw(self):
        self.canv.setFillColor(NAVY)
        self.canv.rect(0, 0, self.width, self.height, fill=1, stroke=0)


def draw_bg(canvas, doc):
    """Page background callback — navy fill + subtle accent line."""
    canvas.saveState()
    canvas.setFillColor(NAVY)
    canvas.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    # Subtle amber accent line at top
    canvas.setStrokeColor(AMBER)
    canvas.setLineWidth(0.5)
    canvas.line(72, PAGE_H - 50, PAGE_W - 72, PAGE_H - 50)
    # Footer
    canvas.setFont("Helvetica", 7)
    canvas.setFillColor(DIM_WHITE)
    canvas.drawCentredString(PAGE_W / 2, 36, "luminouspulse.co  |  @luminouspulse.co")
    canvas.restoreState()


def draw_bg_cover(canvas, doc):
    """Cover page background — navy fill, no header line."""
    canvas.saveState()
    canvas.setFillColor(NAVY)
    canvas.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    canvas.restoreState()


def create_styles():
    styles = getSampleStyleSheet()

    styles.add(ParagraphStyle(
        name="CoverTitle",
        fontName="Helvetica-Bold",
        fontSize=30,
        textColor=WHITE,
        alignment=TA_CENTER,
        spaceAfter=12,
        leading=36,
    ))
    styles.add(ParagraphStyle(
        name="CoverSub",
        fontName="Helvetica",
        fontSize=13,
        textColor=LAVENDER,
        alignment=TA_CENTER,
        spaceAfter=8,
        leading=18,
    ))
    styles.add(ParagraphStyle(
        name="CoverFooter",
        fontName="Helvetica",
        fontSize=10,
        textColor=DIM_WHITE,
        alignment=TA_CENTER,
        spaceAfter=4,
        leading=14,
    ))
    styles.add(ParagraphStyle(
        name="DayLabel",
        fontName="Helvetica",
        fontSize=11,
        textColor=AMBER,
        alignment=TA_LEFT,
        spaceAfter=4,
        leading=14,
        letterSpacing=2,
    ))
    styles.add(ParagraphStyle(
        name="DayTitle",
        fontName="Helvetica-Bold",
        fontSize=14,
        textColor=BLUE,
        alignment=TA_LEFT,
        spaceAfter=16,
        leading=18,
    ))
    styles.add(ParagraphStyle(
        name="Affirmation",
        fontName="Helvetica-Bold",
        fontSize=20,
        textColor=WHITE,
        alignment=TA_CENTER,
        spaceAfter=28,
        leading=28,
        leftIndent=20,
        rightIndent=20,
    ))
    styles.add(ParagraphStyle(
        name="SectionLabel",
        fontName="Helvetica-Bold",
        fontSize=10,
        textColor=AMBER,
        alignment=TA_LEFT,
        spaceAfter=6,
        leading=14,
    ))
    styles.add(ParagraphStyle(
        name="Body",
        fontName="Helvetica",
        fontSize=11,
        textColor=SOFT_WHITE,
        alignment=TA_LEFT,
        spaceAfter=16,
        leading=17,
    ))
    styles.add(ParagraphStyle(
        name="BodyCenter",
        fontName="Helvetica",
        fontSize=11,
        textColor=SOFT_WHITE,
        alignment=TA_CENTER,
        spaceAfter=12,
        leading=17,
    ))
    styles.add(ParagraphStyle(
        name="Heading",
        fontName="Helvetica-Bold",
        fontSize=22,
        textColor=WHITE,
        alignment=TA_CENTER,
        spaceAfter=20,
        leading=28,
    ))
    styles.add(ParagraphStyle(
        name="SubHeading",
        fontName="Helvetica-Bold",
        fontSize=14,
        textColor=BLUE,
        alignment=TA_LEFT,
        spaceAfter=10,
        leading=18,
    ))
    styles.add(ParagraphStyle(
        name="BulletItem",
        fontName="Helvetica",
        fontSize=11,
        textColor=SOFT_WHITE,
        alignment=TA_LEFT,
        spaceAfter=8,
        leading=17,
        leftIndent=20,
        bulletIndent=6,
    ))
    styles.add(ParagraphStyle(
        name="PermissionItem",
        fontName="Helvetica",
        fontSize=12,
        textColor=SOFT_WHITE,
        alignment=TA_LEFT,
        spaceAfter=10,
        leading=18,
        leftIndent=24,
        bulletIndent=8,
    ))
    styles.add(ParagraphStyle(
        name="ItalicText",
        fontName="Helvetica-Oblique",
        fontSize=11,
        textColor=LAVENDER,
        alignment=TA_LEFT,
        spaceAfter=12,
        leading=17,
    ))
    styles.add(ParagraphStyle(
        name="ItalicCenter",
        fontName="Helvetica-Oblique",
        fontSize=11,
        textColor=LAVENDER,
        alignment=TA_CENTER,
        spaceAfter=12,
        leading=17,
    ))
    styles.add(ParagraphStyle(
        name="CTA",
        fontName="Helvetica-Bold",
        fontSize=14,
        textColor=AMBER,
        alignment=TA_CENTER,
        spaceAfter=12,
        leading=20,
    ))
    styles.add(ParagraphStyle(
        name="Closing",
        fontName="Helvetica-Oblique",
        fontSize=13,
        textColor=LAVENDER,
        alignment=TA_CENTER,
        spaceAfter=8,
        leading=18,
    ))
    return styles


class HLine(Flowable):
    """Horizontal line divider."""
    def __init__(self, width, color=SOFT_NAVY, thickness=0.5):
        Flowable.__init__(self)
        self.width = width
        self.color = color
        self.thickness = thickness

    def draw(self):
        self.canv.setStrokeColor(self.color)
        self.canv.setLineWidth(self.thickness)
        self.canv.line(0, 0, self.width, 0)

    def wrap(self, availWidth, availHeight):
        return (self.width, self.thickness + 4)


def build_cover(story, s):
    """Page 1: Cover."""
    story.append(Spacer(1, 140))

    # Logo image if available
    logo_path = os.path.join(os.path.dirname(__file__), "logo-abstract-sanctuary-transparent.png")
    if os.path.exists(logo_path):
        img = Image(logo_path, width=180, height=95)
        img.hAlign = "CENTER"
        story.append(img)
        story.append(Spacer(1, 30))

    story.append(Paragraph("The 5-Day<br/>Grounding Practice", s["CoverTitle"]))
    story.append(Spacer(1, 16))
    story.append(Paragraph(
        "For when the future feels heavier than you can carry.",
        s["CoverSub"]
    ))
    story.append(Spacer(1, 60))
    story.append(Paragraph("Luminous Pulse", s["CoverFooter"]))
    story.append(Paragraph("luminouspulse.co", s["CoverFooter"]))
    story.append(PageBreak())


def build_how_to(story, s):
    """Page 2: How to Use This Practice."""
    story.append(Spacer(1, 30))
    story.append(Paragraph("your morning practice", s["Heading"]))
    story.append(Paragraph("2 minutes. that's all.", s["ItalicCenter"]))
    story.append(Spacer(1, 8))

    steps = [
        "Each morning, read the day's grounding word.",
        "Say it aloud, three times, slowly.",
        "Take 2 minutes with the breathwork exercise.",
        "Sit with the reflection prompt.",
        "Notice how you feel by Day 5.",
    ]
    for i, step in enumerate(steps, 1):
        story.append(Paragraph(
            f'<font color="#{AMBER.hexval()[2:]}">{i}.</font>  {step}',
            s["Body"]
        ))

    story.append(Spacer(1, 12))
    story.append(Paragraph(
        "The feeling follows the words. Not the other way around.",
        s["ItalicCenter"]
    ))

    story.append(Spacer(1, 20))
    story.append(HLine(PAGE_W - 144, SOFT_NAVY))
    story.append(Spacer(1, 16))

    story.append(Paragraph("who this is for", s["SubHeading"]))
    story.append(Paragraph(
        "Anyone carrying the weight of a world that's changing fast. "
        "If you've been laid off, fear you're next, or just feel the ground "
        "shifting beneath you — this is your practice.",
        s["Body"]
    ))
    story.append(Spacer(1, 12))
    story.append(Paragraph(
        "Pin your favorite to your desk, mirror, or laptop lid. "
        "Let it find you throughout the day.",
        s["ItalicText"]
    ))
    story.append(PageBreak())


def build_day_page(story, s, day_num, theme, affirmation, breathwork, reflection):
    """Build a single day page."""
    story.append(Spacer(1, 30))
    story.append(Paragraph(f"DAY {day_num}", s["DayLabel"]))
    story.append(Paragraph(theme, s["DayTitle"]))
    story.append(Spacer(1, 20))

    story.append(Paragraph(f'"{affirmation}"', s["Affirmation"]))

    story.append(HLine(PAGE_W - 144, SOFT_NAVY))
    story.append(Spacer(1, 16))

    story.append(Paragraph("breathe", s["SectionLabel"]))
    story.append(Paragraph(breathwork, s["Body"]))

    story.append(Spacer(1, 8))
    story.append(Paragraph("reflect", s["SectionLabel"]))
    story.append(Paragraph(reflection, s["Body"]))

    story.append(PageBreak())


def build_days(story, s):
    """Pages 3-7: Day 1-5."""
    days = [
        {
            "num": 1,
            "theme": "Come Home",
            "affirmation": "I am whole before I open my laptop.",
            "breathwork": (
                "Place both feet flat on the floor. Inhale through your nose for 4 counts. "
                "Hold for 4 counts. Exhale through your mouth for 6 counts. Repeat 3 times."
            ),
            "reflection": (
                "When was the last time you felt like yourself — not your job title, "
                "not your output, just you? What were you doing? That person is still here."
            ),
        },
        {
            "num": 2,
            "theme": "Remember",
            "affirmation": "My intuition was trained by a lifetime of being alive. Nothing compares.",
            "breathwork": (
                "Close your eyes. Inhale and silently say \"I am.\" "
                "Exhale and silently say \"here.\" Repeat for 2 minutes."
            ),
            "reflection": (
                "Think of a time your gut feeling was right — when the data said one thing "
                "but you knew better. That instinct didn't get laid off. It's still running."
            ),
        },
        {
            "num": 3,
            "theme": "Name the Feeling",
            "affirmation": "I am not broken for feeling anxious. I am awake in a world that is changing fast.",
            "breathwork": (
                "The 4-7-8 breath. Inhale through your nose for 4 counts. Hold for 7 counts. "
                "Exhale slowly through your mouth for 8 counts. Repeat 4 times."
            ),
            "reflection": (
                "Name three feelings you're carrying right now. Don't judge them. Don't fix them. "
                "Just name them. (Example: fear, anger, relief.) Naming them takes their power."
            ),
        },
        {
            "num": 4,
            "theme": "Permission",
            "affirmation": "I give myself permission to navigate this moment with curiosity, not panic.",
            "breathwork": (
                "Place one hand on your chest and one on your belly. Breathe so that only the belly hand moves. "
                "This activates your parasympathetic nervous system — the part that says \"you are safe.\" 10 breaths."
            ),
            "reflection": (
                "What would change if you replaced \"I should know what's next\" with "
                "\"I'm allowed to not know yet\"? Write down what you'd stop doing. "
                "Write down what you'd start."
            ),
        },
        {
            "num": 5,
            "theme": "What Cannot Be Touched",
            "affirmation": "There is something in me that change cannot touch. Today, I remember it.",
            "breathwork": (
                "Stand up. Feet on the floor. Shoulders down. Three deep breaths — in through the nose, "
                "out through the mouth. On the last exhale, let go of everything you're carrying that isn't yours."
            ),
            "reflection": (
                "Underneath the job title, the industry shift, the anxiety — what is the truest thing about you? "
                "The thing that existed before all of this and will exist after? Write it down. Keep it close."
            ),
        },
    ]

    for day in days:
        build_day_page(
            story, s,
            day["num"], day["theme"], day["affirmation"],
            day["breathwork"], day["reflection"]
        )


def build_permission_slip(story, s):
    """Page 8: Permission Slip."""
    story.append(Spacer(1, 40))
    story.append(Paragraph("Your Permission Slip", s["Heading"]))
    story.append(Spacer(1, 8))
    story.append(Paragraph("You are allowed to:", s["ItalicCenter"]))
    story.append(Spacer(1, 16))

    permissions = [
        "Feel the full weight of what's happening without rushing to \"move on\"",
        "Not have a plan yet",
        "Say \"I don't know\" when people ask what's next",
        "Step away from the noise without calling it \"falling behind\"",
        "Grieve a job, even if you weren't happy there",
        "Take longer than you thought you would",
        "Ask for help",
        "Rest",
    ]
    for p in permissions:
        story.append(Paragraph(
            f'<font color="#{AMBER.hexval()[2:]}">—</font>  {p}',
            s["PermissionItem"]
        ))

    story.append(Spacer(1, 24))
    story.append(Paragraph(
        "This permission does not expire.",
        s["CTA"]
    ))
    story.append(PageBreak())


def build_daily_habit(story, s):
    """Page 9: The Morning Practice (Keep This)."""
    story.append(Spacer(1, 40))
    story.append(Paragraph("The Morning Practice", s["Heading"]))
    story.append(Paragraph("keep this page", s["ItalicCenter"]))
    story.append(Spacer(1, 16))

    steps = [
        "Pick one grounding word each morning (start with your favorite from this practice)",
        "Say it aloud three times before you open your phone",
        "Take 5 breaths with your feet on the floor",
        "Set the grounding word as your phone wallpaper for the day",
        "When the anxiety comes — and it will — return to the word",
    ]
    for i, step in enumerate(steps, 1):
        story.append(Paragraph(
            f'<font color="#{AMBER.hexval()[2:]}">{i}.</font>  {step}',
            s["Body"]
        ))

    story.append(Spacer(1, 20))
    story.append(HLine(PAGE_W - 144, SOFT_NAVY))
    story.append(Spacer(1, 16))
    story.append(Paragraph(
        "The practice is not about feeling better.<br/>"
        "It's about feeling grounded. The difference matters.",
        s["ItalicCenter"]
    ))
    story.append(PageBreak())


def build_whats_next(story, s):
    """Page 10: What's Next."""
    story.append(Spacer(1, 40))
    story.append(Paragraph("These 5 days are just the beginning.", s["Heading"]))
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "If this practice helped you — there's more.",
        s["BodyCenter"]
    ))
    story.append(Spacer(1, 20))
    story.append(Paragraph(
        "The 30-Day Luminous Pulse Practice",
        s["SubHeading"]
    ))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "takes you deeper across five themes:",
        s["BodyCenter"]
    ))
    story.append(Spacer(1, 12))

    themes = [
        "Remember Who You Are",
        "Name the Feeling",
        "Ground Yourself",
        "You Are Not Alone",
        "The World We're Building",
    ]
    for t in themes:
        story.append(Paragraph(
            f'<font color="#{AMBER.hexval()[2:]}">—</font>  {t}',
            s["PermissionItem"]
        ))

    story.append(Spacer(1, 16))
    story.append(Paragraph(
        "30 grounding affirmations. 30 reflection prompts.<br/>"
        "Daily breathwork. A morning practice framework<br/>"
        "you can carry for life.",
        s["BodyCenter"]
    ))

    story.append(Spacer(1, 30))
    story.append(HLine(PAGE_W - 144, SOFT_NAVY))
    story.append(Spacer(1, 20))

    story.append(Paragraph(
        "Follow @luminouspulse.co for daily grounding words<br/>"
        "that meet you where you actually are.",
        s["BodyCenter"]
    ))
    story.append(Spacer(1, 8))
    story.append(Paragraph("luminouspulse.co", s["CoverFooter"]))
    story.append(Spacer(1, 24))
    story.append(Paragraph("You are held.", s["Closing"]))


def main():
    output_path = os.path.join(os.path.dirname(__file__), "5-Day-Grounding-Practice.pdf")

    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        topMargin=60,
        bottomMargin=60,
        leftMargin=72,
        rightMargin=72,
    )

    s = create_styles()
    story = []

    build_cover(story, s)
    build_how_to(story, s)
    build_days(story, s)
    build_permission_slip(story, s)
    build_daily_habit(story, s)
    build_whats_next(story, s)

    # Use cover bg for first page, regular bg for rest
    doc.build(story, onFirstPage=draw_bg_cover, onLaterPages=draw_bg)

    print(f"Generated: {output_path}")
    print(f"Pages: 10")


if __name__ == "__main__":
    main()
