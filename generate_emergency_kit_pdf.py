#!/usr/bin/env python3
"""Generate the Emergency Grounding Kit PDF ($9 tripwire) for Luminous Pulse."""

from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import HexColor
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


def draw_bg(canvas, doc):
    """Page background — navy fill + amber accent line at top."""
    canvas.saveState()
    canvas.setFillColor(NAVY)
    canvas.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    # Amber accent line at top
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
        name="CardAffirmation",
        fontName="Helvetica-Bold",
        fontSize=18,
        textColor=WHITE,
        alignment=TA_CENTER,
        spaceAfter=24,
        leading=26,
        leftIndent=16,
        rightIndent=16,
    ))
    styles.add(ParagraphStyle(
        name="CardContext",
        fontName="Helvetica-Oblique",
        fontSize=11,
        textColor=AMBER,
        alignment=TA_LEFT,
        spaceAfter=12,
        leading=16,
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
        name="SectionLabel",
        fontName="Helvetica-Bold",
        fontSize=10,
        textColor=AMBER,
        alignment=TA_LEFT,
        spaceAfter=6,
        leading=14,
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
    styles.add(ParagraphStyle(
        name="CardNumber",
        fontName="Helvetica",
        fontSize=10,
        textColor=AMBER,
        alignment=TA_LEFT,
        spaceAfter=4,
        leading=14,
    ))
    styles.add(ParagraphStyle(
        name="BreathStep",
        fontName="Helvetica",
        fontSize=12,
        textColor=SOFT_WHITE,
        alignment=TA_LEFT,
        spaceAfter=12,
        leading=18,
        leftIndent=20,
    ))
    styles.add(ParagraphStyle(
        name="BreathNote",
        fontName="Helvetica-Oblique",
        fontSize=10,
        textColor=LAVENDER,
        alignment=TA_LEFT,
        spaceAfter=6,
        leading=14,
        leftIndent=32,
    ))
    return styles


def build_cover(story, s):
    """Page 1: Cover."""
    story.append(Spacer(1, 120))

    logo_path = os.path.join(os.path.dirname(__file__), "logo-abstract-sanctuary-transparent.png")
    if os.path.exists(logo_path):
        img = Image(logo_path, width=160, height=84)
        img.hAlign = "CENTER"
        story.append(img)
        story.append(Spacer(1, 30))

    story.append(Paragraph("The Emergency<br/>Grounding Kit", s["CoverTitle"]))
    story.append(Spacer(1, 16))
    story.append(Paragraph(
        "For the moment everything shifts.",
        s["CoverSub"]
    ))
    story.append(Spacer(1, 60))
    story.append(Paragraph("Luminous Pulse", s["CoverFooter"]))
    story.append(Paragraph("luminouspulse.co", s["CoverFooter"]))
    story.append(PageBreak())


def build_when_to_use(story, s):
    """Page 2: When to Use This Kit."""
    story.append(Spacer(1, 30))
    story.append(Paragraph("This kit is for right now.", s["Heading"]))
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "Not tomorrow. Not when you \"have time.\"",
        s["BodyCenter"]
    ))
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "Right now \u2014 when the Slack message just landed. When the news broke. "
        "When you're lying awake at 2am refreshing LinkedIn. When the pit in your "
        "stomach won't go away.",
        s["Body"]
    ))
    story.append(Paragraph(
        "This isn't a 30-day journey. It's a 30-second lifeline.",
        s["ItalicCenter"]
    ))
    story.append(Spacer(1, 16))
    story.append(HLine(PAGE_W - 144, SOFT_NAVY))
    story.append(Spacer(1, 16))

    story.append(Paragraph("how to use", s["SubHeading"]))
    steps = [
        "Open this when you feel the spiral starting",
        "Pick the card that speaks to where you are",
        "Read it aloud \u2014 your voice anchors you",
        "Use the breathwork on the next page",
        "Come back as many times as you need",
    ]
    for i, step in enumerate(steps, 1):
        story.append(Paragraph(
            f'<font color="#{AMBER.hexval()[2:]}">{i}.</font>  {step}',
            s["Body"]
        ))

    story.append(Spacer(1, 16))
    story.append(Paragraph(
        "You don't need to be okay right now. You just need "
        "one steady thing to hold onto.",
        s["ItalicCenter"]
    ))
    story.append(PageBreak())


def build_breathwork(story, s):
    """Page 3: Emergency Breathwork — The 4-7-8 Reset."""
    story.append(Spacer(1, 30))
    story.append(Paragraph("Emergency Breathwork", s["Heading"]))
    story.append(Paragraph("The 4-7-8 Reset", s["ItalicCenter"]))
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "When your chest tightens and your mind races, start here.",
        s["BodyCenter"]
    ))
    story.append(Paragraph(
        "This is not meditation. This is a nervous system reset.",
        s["ItalicCenter"]
    ))
    story.append(Spacer(1, 16))
    story.append(HLine(PAGE_W - 144, SOFT_NAVY))
    story.append(Spacer(1, 16))

    # Step 1
    story.append(Paragraph(
        f'<font color="#{AMBER.hexval()[2:]}"><b>1.</b></font>  '
        f'<b>Inhale</b> through your nose for <b>4 counts</b>',
        s["BreathStep"]
    ))
    story.append(Paragraph(
        "Breathe into your belly, not your chest",
        s["BreathNote"]
    ))

    # Step 2
    story.append(Paragraph(
        f'<font color="#{AMBER.hexval()[2:]}"><b>2.</b></font>  '
        f'<b>Hold</b> for <b>7 counts</b>',
        s["BreathStep"]
    ))
    story.append(Paragraph(
        "This is where the reset happens \u2014 stay with it",
        s["BreathNote"]
    ))

    # Step 3
    story.append(Paragraph(
        f'<font color="#{AMBER.hexval()[2:]}"><b>3.</b></font>  '
        f'<b>Exhale</b> slowly through your mouth for <b>8 counts</b>',
        s["BreathStep"]
    ))
    story.append(Paragraph(
        "Let everything out \u2014 the fear, the tightness, the what-ifs",
        s["BreathNote"]
    ))

    # Step 4
    story.append(Paragraph(
        f'<font color="#{AMBER.hexval()[2:]}"><b>4.</b></font>  '
        f'<b>Repeat 4 times</b>',
        s["BreathStep"]
    ))
    story.append(Spacer(1, 16))

    story.append(Paragraph(
        "After 4 rounds, notice what shifted. Your hands. Your jaw. Your shoulders.",
        s["Body"]
    ))
    story.append(Paragraph(
        "You were just somewhere else. Now you're here.",
        s["ItalicCenter"]
    ))

    story.append(Spacer(1, 16))
    story.append(HLine(PAGE_W - 144, SOFT_NAVY))
    story.append(Spacer(1, 12))
    story.append(Paragraph("when to use this", s["SectionLabel"]))

    when_items = [
        "Before opening your email after a layoff announcement",
        "When you can't sleep because the future feels too heavy",
        "Before any conversation about \"what's next\"",
        "Anytime the tightness starts",
    ]
    for item in when_items:
        story.append(Paragraph(
            f'<font color="#{AMBER.hexval()[2:]}">\u2014</font>  {item}',
            s["BulletItem"]
        ))
    story.append(PageBreak())


def build_card(story, s, card_num, affirmation, context_line, body_text):
    """Build a single emergency card page."""
    story.append(Spacer(1, 40))
    story.append(Paragraph(f"EMERGENCY CARD {card_num}", s["CardNumber"]))
    story.append(Spacer(1, 16))
    story.append(Paragraph(f'"{affirmation}"', s["CardAffirmation"]))
    story.append(HLine(PAGE_W - 144, SOFT_NAVY))
    story.append(Spacer(1, 16))
    story.append(Paragraph(context_line, s["CardContext"]))
    story.append(Paragraph(body_text, s["Body"]))
    story.append(PageBreak())


def build_cards(story, s):
    """Pages 4-13: Emergency Cards 1-10."""
    cards = [
        {
            "affirmation": "I do not have to solve the future in this moment. I just have to breathe through it.",
            "context": "This card is for the first wave \u2014 when the news hits and everything in you wants to fix it immediately.",
            "body": (
                "You don't have to fix it yet. You don't have to know what comes next. "
                "Right now, the only job you have is to be here. Breathe. The plan can wait "
                "until your hands stop shaking."
            ),
        },
        {
            "affirmation": "My layoff is not a performance review. It is a business decision that happened to me.",
            "context": "This card is for the voice that says \"Maybe I wasn't good enough.\"",
            "body": (
                "You were. The spreadsheet didn't know your name. The decision was made in a room "
                "you weren't invited to, about numbers you never saw. This is not a reflection of "
                "your value. It never was."
            ),
        },
        {
            "affirmation": "I am allowed to feel the full weight of this before I figure out what's next.",
            "context": "This card is for the people already telling you to \"look on the bright side.\"",
            "body": (
                "You don't owe anyone optimism right now. Grief is not a failure of mindset. "
                "The weight is real. Feel it. Carry it for as long as you need to. The bright side "
                "will still be there when you're ready."
            ),
        },
        {
            "affirmation": "I have survived every hard day I have ever had. My track record is 100%.",
            "context": "This card is for the 2am spiral.",
            "body": (
                "Pull up your evidence file. The reorg you survived. The pivot you made. The time "
                "you started over and built something better. You have done harder things than this. "
                "You just can't see it from where you're standing right now."
            ),
        },
        {
            "affirmation": "My worth was set long before my badge access was revoked.",
            "context": "This card is for the identity crisis.",
            "body": (
                "You were someone before that title. Before that team. Before that Slack handle. "
                "The person who made people laugh in meetings. Who stayed late because they cared, "
                "not because they had to. Who noticed when someone was struggling and showed up. "
                "That person didn't get laid off. That person is still right here."
            ),
        },
        {
            "affirmation": "I do not need to have an answer when someone asks what I'm doing next.",
            "context": "This card is for the small-talk dread.",
            "body": (
                "\"So, what are you up to now?\" is the most loaded question in the English language "
                "when you don't know the answer. Here's your permission: \"I'm taking some time to "
                "figure that out.\" That's a complete answer. It's honest. It's enough."
            ),
        },
        {
            "affirmation": "The job market is brutal right now. That is not a reflection of my talent.",
            "context": "This card is for the silence after 200 applications.",
            "body": (
                "If you've sent hundreds of applications and heard nothing back \u2014 the market is "
                "broken, not you. Hiring freezes, AI screening, ghost postings. This is the landscape. "
                "Your talent didn't change. The terrain did."
            ),
        },
        {
            "affirmation": "I am not falling behind. I am finding my footing.",
            "context": "This card is for when LinkedIn makes you feel like everyone else has it figured out.",
            "body": (
                "They don't. The \"Excited to announce\" posts are the highlight reel. Behind every "
                "polished update is someone who also cried in their car, questioned everything, and ate "
                "cereal for dinner. You are exactly where millions of other people are right now. "
                "You're just honest about it."
            ),
        },
        {
            "affirmation": "Breathe first. Plan later. Survive the feeling before you solve the problem.",
            "context": "This card is for the person making a plan while panicking.",
            "body": (
                "Your nervous system cannot process grief and strategy at the same time. When the fear "
                "is loud, your brain cannot think clearly. So stop trying to solve it right now. Breathe. "
                "Drink water. Go outside. The plan will be better when you're not making it from a "
                "place of terror."
            ),
        },
        {
            "affirmation": "There is something in me that change cannot touch. Today, I remember it.",
            "context": "This card is for any day at all.",
            "body": (
                "Underneath the job title, the industry shift, the anxiety, the uncertainty \u2014 "
                "there is a part of you that remains. Your capacity to love. Your ability to show up "
                "for the people who need you. Your stubbornness to keep going. That part doesn't care "
                "about the job market. It was there before this. It will be there after."
            ),
        },
    ]

    for i, card in enumerate(cards, 1):
        build_card(story, s, i, card["affirmation"], card["context"], card["body"])


def build_permission_slip(story, s):
    """Page 14: The Permission Slip."""
    story.append(Spacer(1, 30))
    story.append(Paragraph(
        "Cut this out. Pin it to your mirror. Keep it in your wallet.<br/>"
        "Take a photo and set it as your lock screen.",
        s["ItalicCenter"]
    ))
    story.append(Spacer(1, 24))
    story.append(Paragraph("Permission Slip", s["Heading"]))
    story.append(Spacer(1, 8))

    story.append(Paragraph(
        "I, _____________, give myself permission to:",
        s["BodyCenter"]
    ))
    story.append(Spacer(1, 12))

    permissions = [
        "Feel the full weight of what happened without rushing to \"move on\"",
        "Not have a plan yet",
        "Say \"I don't know\" when people ask what's next",
        "Step away from LinkedIn when it makes me feel worse",
        "Grieve a job even if I wasn't happy there",
        "Ask for help without feeling like a failure",
        "Take longer than I thought I would",
        "Be angry, sad, relieved, confused, and hopeful \u2014 all at once",
        "Rest without calling it \"lazy\"",
        "Start over at my own pace",
    ]
    for p in permissions:
        story.append(Paragraph(
            f'<font color="#{AMBER.hexval()[2:]}">\u2014</font>  {p}',
            s["PermissionItem"]
        ))

    story.append(Spacer(1, 20))
    story.append(Paragraph("This permission does not expire.", s["CTA"]))
    story.append(Spacer(1, 20))

    story.append(Paragraph(
        "Signed: _____________&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Date: _____________",
        s["BodyCenter"]
    ))
    story.append(PageBreak())


def build_whats_next(story, s):
    """Page 15: What's Next."""
    story.append(Spacer(1, 40))
    story.append(Paragraph(
        "You don't have to figure it all out today.",
        s["Heading"]
    ))
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "But when you're ready to go deeper \u2014 when you want a daily practice "
        "that meets you where you are and walks with you toward steadier ground:",
        s["Body"]
    ))
    story.append(Spacer(1, 16))

    story.append(Paragraph(
        "The 30-Day Luminous Pulse Practice",
        s["SubHeading"]
    ))
    story.append(Spacer(1, 4))

    features = [
        "30 grounding affirmations (one for each day)",
        "Reflection prompts for each day",
        "Breathwork exercises",
        "5 themed sections that build on each other",
    ]
    for f in features:
        story.append(Paragraph(
            f'<font color="#{AMBER.hexval()[2:]}">\u2014</font>  {f}',
            s["BulletItem"]
        ))

    story.append(Spacer(1, 12))
    story.append(Paragraph(
        "It moves you from emergency mode to grounded strength \u2014 at your own pace.",
        s["ItalicCenter"]
    ))

    story.append(Spacer(1, 24))
    story.append(HLine(PAGE_W - 144, SOFT_NAVY))
    story.append(Spacer(1, 16))

    story.append(Paragraph(
        "Or start with the free 5-Day Grounding Practice if you haven't already:",
        s["BodyCenter"]
    ))
    story.append(Spacer(1, 8))
    story.append(Paragraph("luminouspulse.co", s["CTA"]))

    story.append(Spacer(1, 24))
    story.append(HLine(PAGE_W - 144, SOFT_NAVY))
    story.append(Spacer(1, 16))
    story.append(Paragraph(
        "Follow @luminouspulse.co for daily grounding words<br/>"
        "that meet you where you actually are.",
        s["BodyCenter"]
    ))
    story.append(Spacer(1, 16))
    story.append(Paragraph("You are held.", s["Closing"]))


def main():
    output_path = os.path.join(os.path.dirname(__file__), "Emergency-Grounding-Kit.pdf")

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
    build_when_to_use(story, s)
    build_breathwork(story, s)
    build_cards(story, s)
    build_permission_slip(story, s)
    build_whats_next(story, s)

    doc.build(story, onFirstPage=draw_bg_cover, onLaterPages=draw_bg)

    print(f"Generated: {output_path}")
    print(f"Pages: 15")


if __name__ == "__main__":
    main()
