#!/usr/bin/env python3
"""Generate the 30-Day Luminous Pulse Practice PDF ($37 paid product)."""

from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, Image
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.platypus.flowables import Flowable
import os

# Brand colors
NAVY = HexColor("#1a1a2e")
BLUE = HexColor("#6CB4EE")
AMBER = HexColor("#F4C430")
LAVENDER = HexColor("#B4A7D6")
WHITE = HexColor("#FFFFFF")
SOFT_WHITE = HexColor("#e8e8e8")
DIM_WHITE = HexColor("#999999")
SOFT_NAVY = HexColor("#2a3a5c")

PAGE_W, PAGE_H = letter


def draw_bg(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(NAVY)
    canvas.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    canvas.setStrokeColor(AMBER)
    canvas.setLineWidth(0.5)
    canvas.line(72, PAGE_H - 50, PAGE_W - 72, PAGE_H - 50)
    canvas.setFont("Helvetica", 7)
    canvas.setFillColor(DIM_WHITE)
    canvas.drawCentredString(PAGE_W / 2, 36, "luminouspulse.co  |  @luminouspulse.co")
    canvas.restoreState()


def draw_bg_cover(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(NAVY)
    canvas.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    canvas.restoreState()


class HLine(Flowable):
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
    amber_hex = AMBER.hexval()[2:]

    styles.add(ParagraphStyle(
        name="CoverTitle", fontName="Helvetica-Bold", fontSize=28,
        textColor=WHITE, alignment=TA_CENTER, spaceAfter=12, leading=34,
    ))
    styles.add(ParagraphStyle(
        name="CoverSub", fontName="Helvetica", fontSize=13,
        textColor=LAVENDER, alignment=TA_CENTER, spaceAfter=8, leading=18,
    ))
    styles.add(ParagraphStyle(
        name="CoverFooter", fontName="Helvetica", fontSize=10,
        textColor=DIM_WHITE, alignment=TA_CENTER, spaceAfter=4, leading=14,
    ))
    styles.add(ParagraphStyle(
        name="Heading", fontName="Helvetica-Bold", fontSize=22,
        textColor=WHITE, alignment=TA_CENTER, spaceAfter=16, leading=28,
    ))
    styles.add(ParagraphStyle(
        name="ThemeTitle", fontName="Helvetica-Bold", fontSize=26,
        textColor=WHITE, alignment=TA_CENTER, spaceAfter=12, leading=32,
    ))
    styles.add(ParagraphStyle(
        name="ThemeSub", fontName="Helvetica-Oblique", fontSize=12,
        textColor=LAVENDER, alignment=TA_CENTER, spaceAfter=8, leading=17,
    ))
    styles.add(ParagraphStyle(
        name="ThemeDesc", fontName="Helvetica", fontSize=11,
        textColor=SOFT_WHITE, alignment=TA_CENTER, spaceAfter=12, leading=17,
        leftIndent=40, rightIndent=40,
    ))
    styles.add(ParagraphStyle(
        name="SubHeading", fontName="Helvetica-Bold", fontSize=14,
        textColor=BLUE, alignment=TA_LEFT, spaceAfter=10, leading=18,
    ))
    styles.add(ParagraphStyle(
        name="DayLabel", fontName="Helvetica", fontSize=10,
        textColor=AMBER, alignment=TA_LEFT, spaceAfter=4, leading=14,
    ))
    styles.add(ParagraphStyle(
        name="DayTheme", fontName="Helvetica-Bold", fontSize=12,
        textColor=BLUE, alignment=TA_LEFT, spaceAfter=12, leading=16,
    ))
    styles.add(ParagraphStyle(
        name="Affirmation", fontName="Helvetica-Bold", fontSize=17,
        textColor=WHITE, alignment=TA_CENTER, spaceAfter=20, leading=24,
        leftIndent=16, rightIndent=16,
    ))
    styles.add(ParagraphStyle(
        name="SectionLabel", fontName="Helvetica-Bold", fontSize=9,
        textColor=AMBER, alignment=TA_LEFT, spaceAfter=4, leading=12,
    ))
    styles.add(ParagraphStyle(
        name="Body", fontName="Helvetica", fontSize=10,
        textColor=SOFT_WHITE, alignment=TA_LEFT, spaceAfter=10, leading=15,
    ))
    styles.add(ParagraphStyle(
        name="BodyCenter", fontName="Helvetica", fontSize=11,
        textColor=SOFT_WHITE, alignment=TA_CENTER, spaceAfter=12, leading=17,
    ))
    styles.add(ParagraphStyle(
        name="BulletItem", fontName="Helvetica", fontSize=11,
        textColor=SOFT_WHITE, alignment=TA_LEFT, spaceAfter=8, leading=17,
        leftIndent=20, bulletIndent=6,
    ))
    styles.add(ParagraphStyle(
        name="ItalicCenter", fontName="Helvetica-Oblique", fontSize=11,
        textColor=LAVENDER, alignment=TA_CENTER, spaceAfter=12, leading=17,
    ))
    styles.add(ParagraphStyle(
        name="CTA", fontName="Helvetica-Bold", fontSize=14,
        textColor=AMBER, alignment=TA_CENTER, spaceAfter=12, leading=20,
    ))
    styles.add(ParagraphStyle(
        name="Closing", fontName="Helvetica-Oblique", fontSize=13,
        textColor=LAVENDER, alignment=TA_CENTER, spaceAfter=8, leading=18,
    ))
    styles.add(ParagraphStyle(
        name="JournalLabel", fontName="Helvetica-Bold", fontSize=9,
        textColor=LAVENDER, alignment=TA_LEFT, spaceAfter=4, leading=12,
    ))
    return styles


# ---------- Content data ----------

THEMES = [
    {
        "name": "Remember Who You Are",
        "days_label": "Days 1\u20136",
        "description": (
            "For the moments when you wonder where you fit in a world "
            "that\u2019s changing fast. These six days are about returning to "
            "what\u2019s true about you underneath what you produce."
        ),
        "quote": "There are things inside you that disruption cannot touch.",
        "days": [
            {
                "affirmation": "My intuition was trained by a lifetime of being alive. Nothing compares.",
                "breathe": "Place both feet flat on the floor. Inhale for 4 counts. Hold for 4. Exhale for 6. Repeat 3 times. With each exhale, let go of one comparison you\u2019ve been carrying.",
                "reflect": "Think of a time your gut feeling was right \u2014 when the data said one thing but you knew better. That instinct didn\u2019t get laid off. It\u2019s still running.",
                "journal": "What is one thing you know to be true about yourself that no tool, title, or trend can change?",
            },
            {
                "affirmation": "I am irreplaceable \u2014 not because of what I produce, but because of who I am.",
                "breathe": "Close your eyes. Inhale and silently say \u201cI am.\u201d Exhale and silently say \u201cenough.\u201d Repeat for 2 minutes.",
                "reflect": "When was the last time someone thanked you for something that had nothing to do with your work output? What did they thank you for?",
                "journal": "List three things about you that have nothing to do with your job title. Read them aloud.",
            },
            {
                "affirmation": "My humanity is not a limitation. It is the entire point.",
                "breathe": "The physiological sigh: two short inhales through the nose, then one long exhale through the mouth. Repeat 5 times. This is the fastest way to calm your nervous system.",
                "reflect": "What part of your work involves something only a human can do \u2014 caring, reading a room, knowing when someone needs to be heard?",
                "journal": "If your humanity were a strength on your resume, what would the bullet point say?",
            },
            {
                "affirmation": "I am more than my output. I am the meaning behind it.",
                "breathe": "Box breathing: inhale 4 counts, hold 4, exhale 4, hold 4. Repeat 4 rounds. Notice the stillness in the holds.",
                "reflect": "Think about a piece of work you\u2019re proud of. What mattered more \u2014 the deliverable, or why you made it?",
                "journal": "What meaning do you bring to your work that wouldn\u2019t exist without you?",
            },
            {
                "affirmation": "My story cannot be generated. It can only be lived.",
                "breathe": "Place one hand on your heart. Breathe slowly \u2014 in for 5, out for 5. Feel your heartbeat. That rhythm is yours alone.",
                "reflect": "What\u2019s a chapter of your life that made you who you are today \u2014 one that no algorithm could have predicted or produced?",
                "journal": "Write the first line of your story. Not your career story. Your real one.",
            },
            {
                "affirmation": "I was not designed. I emerged. That is a kind of miracle no code can replicate.",
                "breathe": "Stand up. Feet on the floor. Shoulders back. Three deep breaths \u2014 in through the nose, out through the mouth. On the last exhale, let your shoulders drop completely.",
                "reflect": "You were not trained on a dataset. You were shaped by every conversation, heartbreak, sunrise, and hard day you\u2019ve ever had. What shaped you most?",
                "journal": "What is the most human thing about you \u2014 the thing that makes people feel something when they\u2019re around you?",
            },
        ],
    },
    {
        "name": "Name the Feeling",
        "days_label": "Days 7\u201312",
        "description": (
            "For the days when the anxiety is loud and you need someone "
            "to say \u201cI see you.\u201d These six days are about validating what "
            "you\u2019re feeling without rushing to fix it."
        ),
        "quote": "Your worry is valid. You are not broken for feeling this. You are awake.",
        "days": [
            {
                "affirmation": "I give myself permission to navigate this moment with curiosity, not panic.",
                "breathe": "The 4-7-8 breath: inhale for 4, hold for 7, exhale for 8. Repeat 4 times. This activates your parasympathetic nervous system.",
                "reflect": "What are you most curious about right now \u2014 not worried about, genuinely curious? What would you explore if fear weren\u2019t in the room?",
                "journal": "Rewrite one of your current worries as a question that starts with \u201cWhat if...\u201d (e.g., \u201cWhat if I\u2019m not behind \u2014 what if I\u2019m just in between?\u201d)",
            },
            {
                "affirmation": "I am not broken for feeling anxious. I am awake in a world that is changing fast.",
                "breathe": "Belly breathing: place both hands on your belly. Breathe so your hands rise and fall. 10 slow breaths. Your belly expanding means your diaphragm is engaged \u2014 that\u2019s the calm signal.",
                "reflect": "Name three feelings you\u2019re carrying right now. Don\u2019t judge them. Don\u2019t fix them. Just name them.",
                "journal": "If your anxiety could talk, what would it say it\u2019s trying to protect you from?",
            },
            {
                "affirmation": "I am not the only one who feels this way. I am just honest enough to admit it.",
                "breathe": "Alternate nostril breathing: close your right nostril, inhale left. Close left, exhale right. Inhale right, close right, exhale left. 5 full cycles.",
                "reflect": "Who in your life is probably feeling the same way but hasn\u2019t said it out loud? What would it mean to them if you did?",
                "journal": "Write a sentence that starts with \u201cI haven\u2019t told anyone, but...\u201d You don\u2019t have to share it. Just write it.",
            },
            {
                "affirmation": "I am allowed to step away from the noise. Silence is not falling behind.",
                "breathe": "Silent breathing: breathe normally but count each exhale. When you reach 10, start over. If your mind wanders, start over. 2 minutes.",
                "reflect": "When was the last time you gave yourself permission to stop scrolling, stop researching, stop consuming \u2014 and just be still?",
                "journal": "What is one source of noise you could step away from today? What would you do with that time instead?",
            },
            {
                "affirmation": "I will not catastrophize a future that has not happened yet.",
                "breathe": "Grounding breath: inhale for 4 counts while pressing your feet firmly into the floor. Exhale for 6 while relaxing your feet. Repeat 5 times.",
                "reflect": "What\u2019s the worst thing your brain has predicted in the last year that didn\u2019t actually happen?",
                "journal": "Write down your biggest fear about the future. Now write the most realistic version of what will probably happen. Notice the gap.",
            },
            {
                "affirmation": "The headlines are designed to scare me. My life is designed to be lived.",
                "breathe": "Humming exhale: inhale deeply, then hum as you exhale. Feel the vibration in your chest. Repeat 6 times. The vibration stimulates your vagus nerve.",
                "reflect": "How much of your anxiety comes from your actual life vs. from things you\u2019ve read? Be honest.",
                "journal": "If you didn\u2019t read a single headline for a week, what would you actually feel? What would you do with that mental space?",
            },
        ],
    },
    {
        "name": "Ground Yourself",
        "days_label": "Days 13\u201318",
        "description": (
            "Morning practices for starting your day anchored, not rattled. "
            "These six days are about building a daily rhythm that keeps you "
            "connected to who you are before the world tells you who to be."
        ),
        "quote": "Start the day grounded in who you are, not rattled by what\u2019s changing.",
        "days": [
            {
                "affirmation": "I am whole before I open my laptop.",
                "breathe": "Before you touch your phone: sit up in bed, feet on the floor. 5 breaths. In through the nose, out through the mouth. You are a person before you are a professional.",
                "reflect": "What\u2019s the first thing you usually do when you wake up? What would change if the first thing was a breath and a grounding word instead?",
                "journal": "Complete this sentence: \u201cBefore I open my laptop, I am...\u201d",
            },
            {
                "affirmation": "I do not need to optimize my morning. I need to feel it.",
                "breathe": "Slow your exhale: inhale for 3, exhale for 6. The longer exhale tells your body it\u2019s safe. 8 rounds.",
                "reflect": "When did \u201cmorning routine\u201d become another thing to optimize? What would a morning look like if efficiency wasn\u2019t the point?",
                "journal": "Describe your ideal morning in 3 sentences. Not productive \u2014 peaceful.",
            },
            {
                "affirmation": "I choose presence over productivity this morning.",
                "breathe": "Mindful coffee/tea: hold your cup with both hands. Feel the warmth. Inhale the steam. Take the first sip like it\u2019s the only thing in the world. That\u2019s presence.",
                "reflect": "What\u2019s one moment today where you could choose to be present instead of productive? A conversation? A walk? A meal?",
                "journal": "What would today look like if you measured it by how present you were, not how much you got done?",
            },
            {
                "affirmation": "This day is not a problem to be solved. It is a life to be lived.",
                "breathe": "Body scan breath: as you inhale, notice your head and shoulders. As you exhale, notice your chest and belly. Next breath: notice your hips and legs. Next: your feet on the ground. 4 breaths, top to bottom.",
                "reflect": "Are you approaching today as something to survive, or something to experience? What would shift if you chose the second?",
                "journal": "Write one thing you want to experience today \u2014 not accomplish, experience.",
            },
            {
                "affirmation": "I do not need to earn my worth today. I woke up with it.",
                "breathe": "Self-compassion touch: place your hand over your heart. Breathe slowly. Silently say \u201cI am worthy of a good day.\u201d Feel the warmth of your own hand. 5 breaths.",
                "reflect": "Where did you first learn that your worth was tied to your output? Is that still true?",
                "journal": "If your worth was already settled \u2014 fully, permanently \u2014 what would you stop doing today?",
            },
            {
                "affirmation": "I feel the ground beneath my feet. I begin here.",
                "breathe": "Walking breath: step outside (or stand by a window). Walk slowly for 1 minute. Inhale for 2 steps, exhale for 3 steps. Feel each footfall. You are here.",
                "reflect": "What does \u201cgrounded\u201d actually feel like in your body? Where do you feel it \u2014 your feet, your chest, your hands?",
                "journal": "What is one thing that is true and real and good about your life right now \u2014 not your career, your life?",
            },
        ],
    },
    {
        "name": "You Are Not Alone",
        "days_label": "Days 19\u201324",
        "description": (
            "Reminders that you are held, even when it doesn\u2019t feel like it. "
            "These six days are about connection \u2014 to yourself, to the people "
            "around you, and to the quiet truth that none of us are carrying this alone."
        ),
        "quote": "You are held. We carry this together.",
        "days": [
            {
                "affirmation": "The part of you that loves cannot be automated.",
                "breathe": "Heart coherence: breathe in for 5, out for 5. As you breathe, think of someone you love. Picture their face. Let the feeling spread through your chest. 2 minutes.",
                "reflect": "Who in your life makes you feel seen \u2014 not for your title or your output, but for who you actually are?",
                "journal": "Write a short message to someone you love. You can send it or keep it. The act of writing it is the practice.",
            },
            {
                "affirmation": "You are held. Even here. Even now. Even in the uncertainty.",
                "breathe": "Self-hug breath: cross your arms and place your hands on opposite shoulders. Squeeze gently. Breathe slowly. This is the butterfly hug \u2014 used in trauma therapy to activate bilateral calming.",
                "reflect": "When was the last time you let yourself be held \u2014 physically, emotionally, or by a moment of stillness?",
                "journal": "What would it feel like to believe you are held, even right now? Write what comes up.",
            },
            {
                "affirmation": "I am not the only one trembling. And we are stronger for admitting it.",
                "breathe": "Connected breathing: if someone is near you, try breathing in sync with them for 1 minute. If you\u2019re alone, imagine breathing alongside everyone reading this right now.",
                "reflect": "What would change if you told one person the truth about how you\u2019re feeling right now?",
                "journal": "Write the words: \u201cI am scared about ___.\u201d Then write: \u201cAnd I am not the only one.\u201d Read both aloud.",
            },
            {
                "affirmation": "I do not need to think my way out of this. I need to breathe my way through it.",
                "breathe": "Extended exhale: inhale for 4, exhale for 8. If 8 is too long, try 6. The long exhale is the reset button. 6 rounds.",
                "reflect": "When you\u2019re spiraling, do you try to think your way out or feel your way through? What would happen if you chose the body instead of the mind?",
                "journal": "Write down the thing your mind keeps trying to solve. Then close the journal. You don\u2019t have to solve it today.",
            },
            {
                "affirmation": "Stillness is not the absence of doing. It is the presence of being.",
                "breathe": "2 minutes of nothing: set a timer. Sit. Don\u2019t breathe intentionally. Don\u2019t think intentionally. Just be here. When the timer goes off, notice what you feel.",
                "reflect": "When was the last time you were truly still \u2014 not resting, not recovering, just still?",
                "journal": "What are you afraid will happen if you stop moving? Write it down. Is it true?",
            },
            {
                "affirmation": "Every act of presence is a small revolution against the noise.",
                "breathe": "Sensory grounding: name 5 things you can see, 4 you can touch, 3 you can hear, 2 you can smell, 1 you can taste. Then take 3 breaths.",
                "reflect": "What\u2019s one small act of presence you can commit to today \u2014 a conversation without your phone, a meal without a screen, a walk without a podcast?",
                "journal": "What does revolution look like for you right now? Not the loud kind \u2014 the quiet kind.",
            },
        ],
    },
    {
        "name": "The World We\u2019re Building",
        "days_label": "Days 25\u201330",
        "description": (
            "Grounded hope for the future you\u2019re helping create. "
            "These final six days are about looking forward \u2014 not with "
            "anxiety, but with earned optimism that comes from having "
            "sat in the hard stuff first."
        ),
        "quote": "The future worth showing up for is one where our humanity leads.",
        "days": [
            {
                "affirmation": "What if the most human era is just beginning?",
                "breathe": "Expansive breath: stand up, arms at your sides. Inhale and slowly raise your arms overhead. Exhale and lower them. 5 times. Take up space.",
                "reflect": "What if the skills that matter most in the next decade are empathy, creativity, and presence? How does that change how you feel about your future?",
                "journal": "Write a headline from 5 years in the future that makes you feel hopeful. Make it specific.",
            },
            {
                "affirmation": "The future needs people who know who they are. I am becoming that person.",
                "breathe": "Intentional inhale: as you breathe in, silently say \u201cI am becoming.\u201d As you exhale: \u201cwho I\u2019m meant to be.\u201d 2 minutes.",
                "reflect": "Who are you becoming through this uncertainty? Not who you\u2019re losing \u2014 who you\u2019re becoming.",
                "journal": "Write a letter to yourself one year from now. What do you want that person to know about this moment?",
            },
            {
                "affirmation": "I will not panic about a future I am actively building.",
                "breathe": "Action breath: inhale for 4 (gathering energy), hold for 2 (focusing), exhale for 4 (releasing into action). 6 rounds.",
                "reflect": "What is one small thing you\u2019re building right now \u2014 a skill, a relationship, a project, a version of yourself? Name it.",
                "journal": "What is one step you can take today that your future self will thank you for?",
            },
            {
                "affirmation": "The future needs me whole, not optimized.",
                "breathe": "Wholeness breath: breathe into the parts of yourself you\u2019ve been neglecting. Your creativity. Your playfulness. Your rest. 5 breaths, one for each part of you that needs attention.",
                "reflect": "What part of yourself have you abandoned in the name of keeping up? Is it time to bring it back?",
                "journal": "If you didn\u2019t need to be optimized, productive, or impressive \u2014 who would you be? Write that person\u2019s morning.",
            },
            {
                "affirmation": "I am planting seeds in uncertain soil. That is an act of faith.",
                "breathe": "Rooting breath: press your feet into the ground. Inhale and imagine roots growing from your feet into the earth. Exhale and imagine them deepening. 5 breaths.",
                "reflect": "What seeds are you planting right now that you may not see bloom for months or years?",
                "journal": "Name one thing you believe in even though you can\u2019t prove it yet. That\u2019s faith. That\u2019s enough.",
            },
            {
                "affirmation": "We will look back on this time and say: that was when we remembered what mattered.",
                "breathe": "Gratitude breath: with each inhale, think of one thing you\u2019re grateful for. With each exhale, let go of one thing that no longer serves you. 5 rounds.",
                "reflect": "30 days ago you started this practice. What has shifted? What do you know now that you didn\u2019t then?",
                "journal": "Complete this sentence: \u201cWhat matters most to me is ___.\u201d Write it somewhere you\u2019ll see it. That\u2019s your compass.",
            },
        ],
    },
]


def build_cover(story, s):
    story.append(Spacer(1, 110))
    logo_path = os.path.join(os.path.dirname(__file__), "logo-abstract-sanctuary-transparent.png")
    if os.path.exists(logo_path):
        img = Image(logo_path, width=160, height=84)
        img.hAlign = "CENTER"
        story.append(img)
        story.append(Spacer(1, 30))
    story.append(Paragraph("The Luminous Pulse Practice", s["CoverTitle"]))
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "30 Days of Grounding for Uncertain Times",
        s["CoverSub"]
    ))
    story.append(Spacer(1, 60))
    story.append(Paragraph("luminouspulse.co", s["CoverFooter"]))
    story.append(PageBreak())


def build_how_to(story, s):
    story.append(Spacer(1, 30))
    story.append(Paragraph("how to use this practice", s["Heading"]))
    story.append(Spacer(1, 8))

    story.append(Paragraph(
        "This is a 30-day grounding practice organized into five themes. "
        "Each day gives you four things:",
        s["BodyCenter"]
    ))
    story.append(Spacer(1, 12))

    items = [
        "A grounding affirmation \u2014 say it aloud, three times, slowly",
        "A breathwork exercise \u2014 2 minutes to reset your nervous system",
        "A reflection prompt \u2014 sit with it, no need to write",
        "A journaling question \u2014 write when you\u2019re ready, skip when you\u2019re not",
    ]
    amber_hex = AMBER.hexval()[2:]
    for i, item in enumerate(items, 1):
        story.append(Paragraph(
            f'<font color="#{amber_hex}">{i}.</font>  {item}',
            s["BulletItem"]
        ))

    story.append(Spacer(1, 16))
    story.append(HLine(PAGE_W - 144, SOFT_NAVY))
    story.append(Spacer(1, 16))

    story.append(Paragraph("the daily rhythm", s["SubHeading"]))
    story.append(Paragraph(
        "Each morning, before you open your phone or your laptop, "
        "give yourself 5 minutes with the day\u2019s practice. Read the affirmation. "
        "Do the breathwork. Sit with the reflection. Journal if it calls to you.",
        s["Body"]
    ))
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "The feeling follows the words. Not the other way around.",
        s["ItalicCenter"]
    ))

    story.append(Spacer(1, 16))
    story.append(HLine(PAGE_W - 144, SOFT_NAVY))
    story.append(Spacer(1, 16))

    story.append(Paragraph("the five themes", s["SubHeading"]))
    themes_list = [
        "Remember Who You Are (Days 1\u20136)",
        "Name the Feeling (Days 7\u201312)",
        "Ground Yourself (Days 13\u201318)",
        "You Are Not Alone (Days 19\u201324)",
        "The World We\u2019re Building (Days 25\u201330)",
    ]
    for t in themes_list:
        story.append(Paragraph(
            f'<font color="#{amber_hex}">\u2014</font>  {t}',
            s["BulletItem"]
        ))

    story.append(Spacer(1, 16))
    story.append(Paragraph(
        "By Day 30, come back to Day 1 and notice which affirmations "
        "hit differently. That\u2019s when you\u2019ll know it\u2019s working.",
        s["ItalicCenter"]
    ))
    story.append(PageBreak())


def build_theme_intro(story, s, theme):
    story.append(Spacer(1, 120))
    story.append(Paragraph(theme["name"], s["ThemeTitle"]))
    story.append(Spacer(1, 4))
    story.append(Paragraph(theme["days_label"], s["ThemeSub"]))
    story.append(Spacer(1, 24))
    story.append(HLine(PAGE_W - 200, AMBER, 1))
    story.append(Spacer(1, 24))
    story.append(Paragraph(
        f'<i>{theme["quote"]}</i>',
        s["ThemeDesc"]
    ))
    story.append(Spacer(1, 16))
    story.append(Paragraph(theme["description"], s["ThemeDesc"]))
    story.append(PageBreak())


def build_day_page(story, s, day_num, theme_name, day_data):
    story.append(Spacer(1, 20))
    story.append(Paragraph(f"DAY {day_num}", s["DayLabel"]))
    story.append(Paragraph(theme_name, s["DayTheme"]))
    story.append(Spacer(1, 12))

    story.append(Paragraph(f'"{day_data["affirmation"]}"', s["Affirmation"]))

    story.append(HLine(PAGE_W - 144, SOFT_NAVY))
    story.append(Spacer(1, 12))

    story.append(Paragraph("BREATHE", s["SectionLabel"]))
    story.append(Paragraph(day_data["breathe"], s["Body"]))

    story.append(Spacer(1, 4))
    story.append(Paragraph("REFLECT", s["SectionLabel"]))
    story.append(Paragraph(day_data["reflect"], s["Body"]))

    story.append(Spacer(1, 4))
    story.append(Paragraph("JOURNAL", s["JournalLabel"]))
    story.append(Paragraph(day_data["journal"], s["Body"]))

    story.append(PageBreak())


def build_morning_practice(story, s):
    story.append(Spacer(1, 40))
    story.append(Paragraph("Your Morning Practice", s["Heading"]))
    story.append(Paragraph("keep this page", s["ItalicCenter"]))
    story.append(Spacer(1, 16))

    amber_hex = AMBER.hexval()[2:]
    steps = [
        "Pick one grounding word each morning (start with your favorite from this practice)",
        "Say it aloud three times before you open your phone",
        "Take 5 breaths with your feet on the floor",
        "Set the grounding word as your phone wallpaper for the day",
        "When the anxiety comes \u2014 and it will \u2014 return to the word",
    ]
    for i, step in enumerate(steps, 1):
        story.append(Paragraph(
            f'<font color="#{amber_hex}">{i}.</font>  {step}',
            s["BulletItem"]
        ))

    story.append(Spacer(1, 20))
    story.append(HLine(PAGE_W - 144, SOFT_NAVY))
    story.append(Spacer(1, 16))
    story.append(Paragraph(
        "The practice is not about feeling better.<br/>"
        "It\u2019s about feeling grounded. The difference matters.",
        s["ItalicCenter"]
    ))

    story.append(Spacer(1, 24))
    story.append(HLine(PAGE_W - 144, SOFT_NAVY))
    story.append(Spacer(1, 16))
    story.append(Paragraph(
        "After Day 30, start again from Day 1. The words will land "
        "differently the second time. That\u2019s the practice working.",
        s["BodyCenter"]
    ))
    story.append(PageBreak())


def build_closing(story, s):
    story.append(Spacer(1, 100))
    story.append(Paragraph(
        "You made it.",
        s["Heading"]
    ))
    story.append(Spacer(1, 16))
    story.append(Paragraph(
        "30 days of showing up for yourself in a world that "
        "keeps asking you to show up for everything else first.",
        s["BodyCenter"]
    ))
    story.append(Spacer(1, 12))
    story.append(Paragraph(
        "That is not a small thing. That is the whole thing.",
        s["ItalicCenter"]
    ))
    story.append(Spacer(1, 30))
    story.append(HLine(PAGE_W - 200, AMBER, 1))
    story.append(Spacer(1, 30))
    story.append(Paragraph(
        "Follow @luminouspulse.co for daily grounding words<br/>"
        "that meet you where you actually are.",
        s["BodyCenter"]
    ))
    story.append(Spacer(1, 8))
    story.append(Paragraph("luminouspulse.co", s["CTA"]))
    story.append(Spacer(1, 30))
    story.append(Paragraph("You are held.", s["Closing"]))


def main():
    output_path = os.path.join(os.path.dirname(__file__), "30-Day-Luminous-Pulse-Practice.pdf")

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

    day_num = 1
    for theme in THEMES:
        build_theme_intro(story, s, theme)
        for day_data in theme["days"]:
            build_day_page(story, s, day_num, theme["name"], day_data)
            day_num += 1

    build_morning_practice(story, s)
    build_closing(story, s)

    doc.build(story, onFirstPage=draw_bg_cover, onLaterPages=draw_bg)

    page_count = 2 + (len(THEMES) * 7) + 2  # cover+howto + (intro+6days)*5 + practice+closing
    print(f"Generated: {output_path}")
    print(f"Pages: {page_count}")


if __name__ == "__main__":
    main()
