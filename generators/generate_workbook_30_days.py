#!/usr/bin/env python3
"""Generate "30 days of ground" workbook PDF — Luminous Pulse ($17).

A daily practice workbook — one page per day. one prompt. one breath. one offline thing.

30 daily spreads across 4 weekly themes + weekly pauses + affirmation cards.

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


class DashedLine(Flowable):
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


class AffirmationCard(Flowable):
    """A single affirmation card with dashed border for cutting."""
    def __init__(self, text, width, height=72):
        Flowable.__init__(self)
        self.text = text
        self.card_width = width
        self.card_height = height

    def draw(self):
        w = self.card_width
        h = self.card_height
        c = self.canv
        # Dashed border
        c.setStrokeColor(LIGHT_GRAY)
        c.setLineWidth(0.4)
        c.setDash(3, 3)
        c.rect(0, 0, w, h, fill=0, stroke=1)
        c.setDash()
        # Small dot
        c.setFillColor(AMBER_SOFT)
        c.circle(12, h / 2, 2, fill=1, stroke=0)
        # Text
        c.setFillColor(NAVY)
        c.setFont("Helvetica-Bold", 9)
        # Word wrap manually for card
        words = self.text.split()
        lines = []
        current = ""
        for word in words:
            test = f"{current} {word}".strip()
            if c.stringWidth(test, "Helvetica-Bold", 9) < w - 36:
                current = test
            else:
                lines.append(current)
                current = word
        if current:
            lines.append(current)
        y_start = h / 2 + (len(lines) - 1) * 6
        for i, line in enumerate(lines):
            c.drawString(22, y_start - i * 12, line)
        # Brand footer
        c.setFont("Helvetica", 6)
        c.setFillColor(SOFT_GRAY)
        c.drawRightString(w - 8, 6, "luminouspulse.co")

    def wrap(self, availWidth, availHeight):
        return (self.card_width, self.card_height + 6)


# ── Page Backgrounds ──

def draw_bg(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(CREAM)
    canvas.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    canvas.setFont("Helvetica", 7)
    canvas.setFillColor(SOFT_GRAY)
    canvas.drawCentredString(PAGE_W / 2, 30,
                             "30 days of ground  ·  luminouspulse.co")
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
        name="DayNum", fontName="Helvetica", fontSize=9,
        textColor=AMBER_SOFT, alignment=TA_LEFT, leading=13, spaceAfter=2,
        letterSpacing=2,
    ))
    styles.add(ParagraphStyle(
        name="DayTitle", fontName="Helvetica-Bold", fontSize=16,
        textColor=NAVY, alignment=TA_LEFT, leading=22, spaceAfter=8,
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
        name="BodySmall", fontName="Helvetica", fontSize=9.5,
        textColor=HexColor("#444444"), alignment=TA_LEFT, leading=14, spaceAfter=6,
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
        name="OfflineBox", fontName="Helvetica", fontSize=9.5,
        textColor=HexColor("#555555"), alignment=TA_LEFT, leading=14, spaceAfter=4,
    ))
    styles.add(ParagraphStyle(
        name="PracticeTitle", fontName="Helvetica-Bold", fontSize=9.5,
        textColor=BLUE, alignment=TA_LEFT, leading=14, spaceAfter=2,
    ))

    return styles


# ── 30 Days Content ──

DAYS = [
    # Week 1: Arriving (Days 1-7)
    {
        "title": "the ground beneath you",
        "prompt": "place your feet flat on the floor. what does the ground feel like today?",
        "practice": ("5-4-3-2-1 GROUNDING",
                     "name 5 things you see, 4 you can touch, 3 you hear, "
                     "2 you smell, 1 you taste."),
        "offline": "walk outside for 10 minutes. leave your phone.",
        "affirmation": "I feel the ground beneath my feet. I begin here.",
    },
    {
        "title": "what morning feels like",
        "prompt": "describe this morning in sensory detail. not what you did. what it felt like.",
        "practice": ("PHYSIOLOGICAL SIGH",
                     "deep inhale through nose → second short inhale → "
                     "long slow exhale through mouth. repeat 3x."),
        "offline": "make a hot drink and hold it with both hands for one full minute.",
        "affirmation": "my morning belongs to me. no notification changes that.",
    },
    {
        "title": "one true sentence",
        "prompt": "write the truest sentence you know about where you are right now.",
        "practice": ("BODY SCAN (2 MIN)",
                     "close your eyes. start at the top of your head. "
                     "move slowly down. notice without fixing."),
        "offline": "handwrite a note to someone. a real one, on paper.",
        "affirmation": "I do not need to have it all figured out this morning.",
    },
    {
        "title": "what are you carrying?",
        "prompt": "what are you carrying today that isn't yours to hold?",
        "practice": ("SHOULDER DROP",
                     "inhale and lift your shoulders to your ears. "
                     "hold 5 seconds. exhale and let them drop completely. 3x."),
        "offline": "sit somewhere without a screen for 15 minutes.",
        "affirmation": "I am allowed to put this down for a moment.",
    },
    {
        "title": "the small good thing",
        "prompt": "what is one small, genuinely good thing about today? it can be tiny.",
        "practice": ("COHERENT BREATHING",
                     "inhale for 5.5 seconds. exhale for 5.5 seconds. "
                     "no holds. just a slow, even rhythm for 2 minutes."),
        "offline": "cook something from scratch. nothing fancy.",
        "affirmation": "today I will do one thing that only a human can do.",
    },
    {
        "title": "who called today?",
        "prompt": "who did you think about today? who do you wish had called?",
        "practice": ("BUTTERFLY HUG",
                     "cross arms over chest, interlock thumbs. "
                     "alternately tap gently for 1-2 minutes. eyes closed."),
        "offline": "call someone. not to vent. just to hear their voice.",
        "affirmation": "connection is not a soft skill. it is the infrastructure of everything.",
    },
    {
        "title": "the week in one word",
        "prompt": "if you had to describe this week in one word, what would it be? why that word?",
        "practice": ("JAW RELEASE",
                     "open your mouth wide. hold 5 seconds. "
                     "close slowly. let your tongue rest on the roof of your mouth. "
                     "notice the release."),
        "offline": "take something off your to-do list without doing it.",
        "affirmation": "I am not behind. I woke up. I showed up. that is the practice.",
    },
    # Week 2: Feeling (Days 8-14)
    {
        "title": "name the feeling",
        "prompt": "right now, without thinking too hard: what are you feeling? name it as specifically as you can.",
        "practice": ("BOX BREATHING",
                     "inhale 4 sec → hold 4 → exhale 4 → hold 4. "
                     "repeat for 3 minutes. creates alert calm."),
        "offline": "go to a library or bookstore. browse with no agenda.",
        "affirmation": "the anxiety is information, not a verdict.",
    },
    {
        "title": "the feeling underneath",
        "prompt": "beneath the first feeling you named, what's hiding? what's the feeling underneath the feeling?",
        "practice": ("HAND ON HEART",
                     "place your right hand on your chest. "
                     "feel your heartbeat. breathe into the warmth of your palm. 1 minute."),
        "offline": "listen to an entire album from start to finish. no skipping.",
        "affirmation": "I am allowed to feel overwhelmed by how fast things are changing.",
    },
    {
        "title": "what anger is saying",
        "prompt": "what is making you angry right now? don't censor it. let the pen be fast.",
        "practice": ("COLD WATER RESET",
                     "splash cold water on your face and wrists. "
                     "the mammalian dive reflex calms your nervous system in seconds."),
        "offline": "walk somewhere you've never walked before. explore.",
        "affirmation": "I am not fragile. I am paying attention. there is a difference.",
    },
    {
        "title": "permission to feel",
        "prompt": "what feeling have you been trying not to feel? what if you let it arrive?",
        "practice": ("EXHALE EMPHASIS",
                     "inhale for 4 counts. exhale for 8. "
                     "the extended exhale activates your parasympathetic system. 5x."),
        "offline": "watch the sky change for 10 minutes. don't photograph it.",
        "affirmation": "I release the need to understand everything happening right now.",
    },
    {
        "title": "the body's truth",
        "prompt": "where do you feel today's emotions in your body? describe the sensation.",
        "practice": ("PROGRESSIVE RELAXATION",
                     "tense your feet for 5 seconds, release. "
                     "move up: calves, thighs, stomach, fists, shoulders, face. "
                     "release each one completely."),
        "offline": "stretch for 10 minutes. no app. no video. just your body and the floor.",
        "affirmation": "my body knows things my mind has forgotten. I listen.",
    },
    {
        "title": "what grief looks like today",
        "prompt": "grief changes shape every day. what shape is yours in today?",
        "practice": ("HUMMING",
                     "take a deep breath. hum on the exhale — one long note. "
                     "the vibration stimulates your vagus nerve. 5 breaths."),
        "offline": "find a body of water — a lake, a river, a fountain. sit near it.",
        "affirmation": "this feeling will pass. my ability to grow through it will not.",
    },
    {
        "title": "two truths",
        "prompt": "name two feelings you're holding at the same time. how do they coexist?",
        "practice": ("BILATERAL TAPPING",
                     "cross arms and alternately tap your knees — "
                     "left, right, left, right. slow and steady for 1 minute."),
        "offline": "eat a meal without any screen in sight.",
        "affirmation": "I can hold two truths: the world is changing, and so is my capacity to meet it.",
    },
    # Week 3: Remembering (Days 15-21)
    {
        "title": "before all the titles",
        "prompt": "what did you love doing before anyone gave you a job title?",
        "practice": ("FEET ON GROUND",
                     "press your feet into the floor. push down. "
                     "feel the resistance. you are here. you are solid. 30 seconds."),
        "offline": "dig up a childhood photo. look at it for a while.",
        "affirmation": "I was built for uncertainty. I have navigated it my entire life.",
    },
    {
        "title": "the thing nobody pays you for",
        "prompt": "what do you do that nobody pays you for — but that makes you feel most alive?",
        "practice": ("4-7-8 BREATHING",
                     "inhale 4 counts. hold 7. exhale 8. "
                     "Dr. Andrew Weil calls this a \"natural tranquilizer.\" 4 cycles."),
        "offline": "do the thing from your answer above. even for 10 minutes.",
        "affirmation": "my creativity doesn't run on electricity. it runs on living.",
    },
    {
        "title": "someone who sees you",
        "prompt": "who in your life sees you — the real you, not the professional version?",
        "practice": ("WARM HANDS",
                     "rub your palms together vigorously for 15 seconds. "
                     "cup them over your closed eyes. breathe into the warmth."),
        "offline": "spend time with one of the people you named above.",
        "affirmation": "I give the world something it cannot download: presence.",
    },
    {
        "title": "what you're good at (not your job)",
        "prompt": "list 5 things you're good at that have nothing to do with your profession.",
        "practice": ("PHYSIOLOGICAL SIGH",
                     "double inhale through nose → long slow exhale. "
                     "fastest nervous system reset. 3x."),
        "offline": "make something with your hands. draw, bake, fix, build, plant.",
        "affirmation": "I am more than my output. I am the meaning behind it.",
    },
    {
        "title": "the quiet things",
        "prompt": "what are the quiet things about you that never make it onto a résumé?",
        "practice": ("NECK RELEASE",
                     "drop your right ear toward your right shoulder. "
                     "hold 20 seconds. switch sides. "
                     "roll your head forward gently in a half-circle."),
        "offline": "write a list of 10 things you're grateful for. the smaller, the better.",
        "affirmation": "my story cannot be generated. it can only be lived.",
    },
    {
        "title": "what your hands remember",
        "prompt": "your hands know how to do things your mind has forgotten. what do they remember?",
        "practice": ("FINGER BREATHING",
                     "spread one hand. with the other, trace up each finger (inhale) "
                     "and down (exhale). 5 fingers = 5 breaths."),
        "offline": "use your hands: knead dough, pull weeds, sketch, play an instrument.",
        "affirmation": "I can learn any tool. no tool can learn to be me.",
    },
    {
        "title": "the week you remembered",
        "prompt": "this week asked you to remember who you are beyond work. what surprised you?",
        "practice": ("FULL BODY SHAKE",
                     "stand up. shake your hands for 30 seconds. "
                     "then your whole body — arms, legs, shoulders. "
                     "animals do this to discharge stress."),
        "offline": "do something you did as a kid, for no reason.",
        "affirmation": "I was here before this. I will be here after. I am the constant.",
    },
    # Week 4: Planting (Days 22-28)
    {
        "title": "what's pulling you",
        "prompt": "what are you curious about right now — even slightly? what makes you lean in?",
        "practice": ("COHERENT BREATHING",
                     "5.5 seconds in, 5.5 seconds out. "
                     "this rhythm balances your nervous system. 3 minutes."),
        "offline": "follow a curiosity from today's answer for 30 minutes. no phone.",
        "affirmation": "I am planting seeds in uncertain soil. that is an act of faith.",
    },
    {
        "title": "one small thing",
        "prompt": "what is one small action you could take today that would feel like care for your future self?",
        "practice": ("HAND ON BELLY",
                     "place your hand on your belly. breathe so your hand rises. "
                     "3 breaths. diaphragmatic breathing signals safety."),
        "offline": "take yourself somewhere — coffee shop, park, museum. alone. with intention.",
        "affirmation": "I do not need a perfect plan. I need a willing heart and a clear next step.",
    },
    {
        "title": "what you refuse to go back to",
        "prompt": "what did your old life teach you that you refuse to repeat?",
        "practice": ("BUTTERFLY HUG",
                     "cross arms, interlock thumbs, alternate tapping. "
                     "1-2 minutes with slow breathing."),
        "offline": "clean or organize one small space. make it feel like yours.",
        "affirmation": "I am not defined by the tools I use. I am defined by the decisions I make.",
    },
    {
        "title": "a life you'd want",
        "prompt": "describe a day in a life you'd actually want. not a perfect day. a real one.",
        "practice": ("SMILE BREATHING",
                     "inhale normally. on the exhale, let a slight smile form. "
                     "the facial feedback signals calm to your brain. 5 breaths."),
        "offline": "plan one element from today's answer. write it in your calendar.",
        "affirmation": "the future needs me whole, not optimized.",
    },
    {
        "title": "who you want to become",
        "prompt": "not what you want to do. who do you want to BE? what qualities? what energy?",
        "practice": ("VOO BREATHING",
                     "inhale deeply. exhale while making a long, low 'voo' sound. "
                     "the vibration stimulates your vagus nerve. 5x."),
        "offline": "spend 20 minutes with someone who embodies something you admire.",
        "affirmation": "the future belongs to people who know who they are. I am becoming that person.",
    },
    {
        "title": "a letter to next week",
        "prompt": "write a short note to yourself for next Monday. what do you want to remember?",
        "practice": ("GROUNDING FEET",
                     "press your feet into the ground. shift your weight left, right, "
                     "forward, back. find center. you are here."),
        "offline": "prepare something for tomorrow — food, clothes, a note to yourself.",
        "affirmation": "I choose to build the future I want to live in, one day at a time.",
    },
    {
        "title": "what four weeks taught you",
        "prompt": "you've been showing up for 28 days. what do you know now that you didn't know on day 1?",
        "practice": ("BOX BREATHING",
                     "4 in, 4 hold, 4 out, 4 hold. "
                     "the practice you started with. notice how it feels different now."),
        "offline": "reread your answers from days 1-7. notice what changed.",
        "affirmation": "I am not just surviving change. I am becoming someone who can hold it.",
    },
    # Days 29-30: Emerging
    {
        "title": "what remains",
        "prompt": "after 29 days of showing up, what is the thing that stays constant? what is the ground?",
        "practice": ("YOUR FAVORITE",
                     "by now you have a go-to practice. do it. "
                     "the one your body responds to most. you know which one."),
        "offline": "go somewhere beautiful. bring nothing but your attention.",
        "affirmation": "I am grounded. I am clear. I am ready.",
    },
    {
        "title": "the declaration",
        "prompt": "write one sentence about who you are — not who you were, not who you should be. who you are. right now.",
        "practice": ("PHYSIOLOGICAL SIGH + SMILE",
                     "double inhale → long exhale → let a smile arrive. "
                     "you showed up for 30 days. that's real."),
        "offline": "say your sentence from today out loud. then go live your day.",
        "affirmation": "I am the original intelligence. everything else is built in my image.",
    },
]

WEEKLY_THEMES = [
    ("WEEK 1", "arriving",
     "this week is about landing in the present moment. "
     "you've been living in the future (anxiety) or the past (grief). "
     "these 7 days are about right here, right now."),
    ("WEEK 2", "feeling",
     "this week asks you to name what you're carrying. "
     "not fix it. not reframe it. just name it. naming is the first act of tending."),
    ("WEEK 3", "remembering",
     "this week reconnects you with who you are beyond your job. "
     "the things you love, the people who see you, the skills that are yours."),
    ("WEEK 4", "planting",
     "this week looks forward — gently. not with goals or timelines. "
     "with curiosity and small brave actions."),
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
    story.append(Paragraph("30 days of ground", s["CoverTitle"]))
    story.append(Spacer(1, 14))
    story.append(Paragraph(
        "one page per day. one prompt. one breath.<br/>one offline thing.",
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
        "this is not a big workbook. it's a small one. on purpose.",
        s["PromptCenter"]
    ))
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "when everything feels like too much — when the idea of a 90-page "
        "journal makes you want to lie down — this is where you start. "
        "one page per day. that's it.",
        s["Body"]
    ))
    story.append(Paragraph(
        "each day gives you four things: a grounding prompt to write about, "
        "a body practice that takes under 5 minutes, one offline thing "
        "to do, and a micro-affirmation to close with. some days will "
        "feel easy. some will feel heavy. both are fine.",
        s["Body"]
    ))
    story.append(Spacer(1, 16))
    story.append(AccentDot(AMBER))
    story.append(Spacer(1, 12))

    story.append(Paragraph("the rules", s["SubHeading"]))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "<b>print it.</b> handwriting activates emotional processing "
        "centers that typing cannot reach.",
        s["Body"]
    ))
    story.append(Paragraph(
        "<b>one day at a time.</b> don't read ahead. each day is designed "
        "for that day. trust the sequence.",
        s["Body"]
    ))
    story.append(Paragraph(
        "<b>if you miss a day, keep going.</b> this is not a streak. "
        "there is no scoreboard. pick up where you left off.",
        s["Body"]
    ))
    story.append(Paragraph(
        "<b>do the offline thing.</b> it's not optional. the offline "
        "thing is the point. the writing is the preparation. "
        "the offline thing is the practice.",
        s["Body"]
    ))

    story.append(Spacer(1, 20))
    story.append(Paragraph(
        '"I do not need to optimize my morning. I need to feel it."',
        s["AffirmationLight"]
    ))
    story.append(PageBreak())


def build_week_opener(story, s, week_num, theme, description):
    """Navy page to mark the start of a week."""
    story.append(NavyPageBg())
    story.append(Spacer(1, 200))
    story.append(Paragraph(f"WEEK {week_num}", s["SectionNum"]))
    story.append(Spacer(1, 12))
    story.append(Paragraph(theme, s["SectionTitle"]))
    story.append(Spacer(1, 20))
    story.append(Paragraph(description, s["SectionEpigraph"]))
    story.append(PageBreak())


def build_day_page(story, s, day_num, day, deep=False):
    """Build a single day's page: prompt + practice + offline + affirmation + writing lines.

    If deep=True, adds an extra page of writing space after the main page.
    """
    # Day header
    story.append(Spacer(1, 12))
    story.append(Paragraph(f"DAY {day_num}", s["DayNum"]))
    story.append(Paragraph(day["title"], s["DayTitle"]))
    story.append(HLine(CONTENT_W, AMBER, 0.4))
    story.append(Spacer(1, 8))

    # Prompt
    story.append(Paragraph("TODAY'S GROUND", s["ExerciseLabel"]))
    story.append(Spacer(1, 4))
    story.append(Paragraph(day["prompt"], s["Prompt"]))
    story.append(Spacer(1, 4))
    story.append(WritingLines(CONTENT_W, num_lines=6, spacing=26))
    story.append(Spacer(1, 8))

    # Body practice
    pname, pdesc = day["practice"]
    story.append(Paragraph(pname, s["PracticeTitle"]))
    story.append(Paragraph(pdesc, s["BodySmall"]))
    story.append(Spacer(1, 6))

    # Offline thing
    story.append(HLine(CONTENT_W * 0.15, AMBER_SOFT, 0.3))
    story.append(Spacer(1, 4))
    story.append(Paragraph("ONE OFFLINE THING", s["ExerciseLabel"]))
    story.append(Paragraph(day["offline"], s["OfflineBox"]))
    story.append(Spacer(1, 8))

    # Micro-affirmation
    story.append(Paragraph(
        f'"{day["affirmation"]}"',
        s["MicroAffirmation"]
    ))
    story.append(PageBreak())

    # Extra writing page for deeper days
    if deep:
        story.append(Spacer(1, 16))
        story.append(Paragraph(f"DAY {day_num} — KEEP WRITING", s["DayNum"]))
        story.append(Spacer(1, 8))
        story.append(WritingLines(CONTENT_W, num_lines=22))
        story.append(PageBreak())


def build_weekly_pause(story, s, week_num):
    """A 2-page reflection at the end of each week."""
    story.append(Spacer(1, 20))
    story.append(Paragraph(f"week {week_num} pause", s["Heading"]))
    story.append(Spacer(1, 8))
    story.append(HLine(CONTENT_W, LAVENDER, 0.5))
    story.append(Spacer(1, 12))

    story.append(Paragraph(
        "before you move to the next week, take a moment to look back.",
        s["ItalicNote"]
    ))
    story.append(Spacer(1, 8))

    story.append(Paragraph("LOOK BACK", s["ExerciseLabel"]))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "which day this week felt the most true?", s["Prompt"]
    ))
    story.append(WritingLines(CONTENT_W, num_lines=3, spacing=26))
    story.append(Spacer(1, 8))

    story.append(Paragraph(
        "which offline thing did you actually do? how did it feel?", s["Prompt"]
    ))
    story.append(WritingLines(CONTENT_W, num_lines=3, spacing=26))
    story.append(Spacer(1, 8))

    story.append(Paragraph(
        "one word for this week:", s["Prompt"]
    ))
    story.append(WritingLines(CONTENT_W, num_lines=1, spacing=28))
    story.append(PageBreak())

    # Page 2: Deeper weekly reflection
    story.append(Spacer(1, 20))
    story.append(Paragraph(f"WEEK {week_num} — BODY CHECK", s["ExerciseLabel"]))
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "how does your body feel compared to last week? "
        "where are you holding less tension? where are you still tight?",
        s["Prompt"]
    ))
    story.append(WritingLines(CONTENT_W, num_lines=5, spacing=26))
    story.append(Spacer(1, 10))

    story.append(Paragraph(f"WEEK {week_num} — LOOK AHEAD", s["ExerciseLabel"]))
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "what do you want to bring into next week? "
        "what do you want to leave behind?",
        s["Prompt"]
    ))
    story.append(WritingLines(CONTENT_W, num_lines=5, spacing=26))
    story.append(Spacer(1, 12))

    # Week-specific closing affirmation
    week_affirmations = {
        1: "I am here. that is the starting point.",
        2: "naming the feeling is the first act of tending it.",
        3: "I was always more than what I did for a living.",
        4: "I do not need certainty to take one small step.",
    }
    aff = week_affirmations.get(week_num, "I am grounded.")
    story.append(HLine(CONTENT_W * 0.3, AMBER, 0.4))
    story.append(Spacer(1, 10))
    story.append(Paragraph(f'"{aff}"', s["MicroAffirmation"]))
    story.append(PageBreak())


def build_closing(story, s):
    story.append(Spacer(1, 80))
    story.append(Paragraph("you showed up.", s["Heading"]))
    story.append(Spacer(1, 16))
    story.append(HLine(CONTENT_W * 0.3, AMBER, 0.6))
    story.append(Spacer(1, 20))
    story.append(Paragraph(
        "30 days. 30 prompts. 30 breaths. 30 offline things. "
        "not because someone made you. because some part of you "
        "knew that the ground was there if you just slowed down "
        "enough to feel it.",
        s["BodyCenter"]
    ))
    story.append(Spacer(1, 12))
    story.append(Paragraph(
        "the practice doesn't end here. you can start over at day 1. "
        "you can keep a blank journal and write your own prompts. "
        "you can simply carry the habit: one prompt, one breath, "
        "one offline thing. every day. that's enough.",
        s["BodyCenter"]
    ))
    story.append(Spacer(1, 24))
    story.append(Paragraph(
        '"I am the author of this day. not the algorithm,<br/>'
        'not the feed, not the forecast."',
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
        '"before the room" · "the in-between"',
        s["ItalicCenter"]
    ))
    story.append(Spacer(1, 8))
    story.append(Paragraph("luminouspulse.co", s["CTA"]))
    story.append(PageBreak())


def build_affirmation_cards(story, s):
    """30 printable affirmation cards, cut along dotted lines."""
    story.append(Spacer(1, 16))
    story.append(Paragraph("affirmation cards", s["Heading"]))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "cut along the dashed lines. keep them in a jar, a pocket, "
        "on your mirror, in your wallet. pull one when you need it.",
        s["ItalicCenter"]
    ))
    story.append(Spacer(1, 12))

    # Use the affirmations from each day
    card_width = CONTENT_W
    for i, day in enumerate(DAYS):
        story.append(AffirmationCard(day["affirmation"], card_width, height=60))
        story.append(Spacer(1, 2))
        # Page break every 9 cards
        if (i + 1) % 9 == 0 and i < len(DAYS) - 1:
            story.append(PageBreak())
            story.append(Spacer(1, 12))

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

def build_workbook():
    out_path = os.path.join(os.path.dirname(__file__),
                            "30-Days-Of-Ground-Workbook.pdf")

    doc = SimpleDocTemplate(
        out_path,
        pagesize=letter,
        leftMargin=MARGIN, rightMargin=MARGIN,
        topMargin=MARGIN, bottomMargin=MARGIN,
        title="30 days of ground",
        author="Luminous Pulse · luminouspulse.co",
    )

    s = create_styles()
    story = []

    build_cover(story, s)
    build_intro(story, s)

    # Deep days get an extra writing page (every 5th day + days 1, 7, 14, 21, 28, 30)
    deep_days = {1, 5, 7, 10, 14, 15, 20, 21, 25, 28, 30}

    # Build 30 days across 4 weeks + days 29-30
    for week_idx in range(4):
        label, theme, desc = WEEKLY_THEMES[week_idx]
        build_week_opener(story, s, week_idx + 1, theme, desc)
        start = week_idx * 7
        end = start + 7
        for i in range(start, end):
            day_num = i + 1
            build_day_page(story, s, day_num, DAYS[i], deep=(day_num in deep_days))
        build_weekly_pause(story, s, week_idx + 1)

    # Days 29-30 (emerging)
    story.append(NavyPageBg())
    story.append(Spacer(1, 200))
    story.append(Paragraph("DAYS 29-30", s["SectionNum"]))
    story.append(Spacer(1, 12))
    story.append(Paragraph("emerging", s["SectionTitle"]))
    story.append(Spacer(1, 20))
    story.append(Paragraph(
        "you have been grounding for a month.<br/>"
        "now see what's growing.",
        s["SectionEpigraph"]
    ))
    story.append(PageBreak())

    build_day_page(story, s, 29, DAYS[28], deep=True)
    build_day_page(story, s, 30, DAYS[29], deep=True)

    build_closing(story, s)
    build_affirmation_cards(story, s)
    build_notes(story, s, num_pages=2)

    doc.build(story, onFirstPage=draw_bg_cover, onLaterPages=draw_bg)

    file_size = os.path.getsize(out_path) / (1024 * 1024)
    print(f"\n{'='*50}")
    print(f"  30 days of ground — workbook generated")
    print(f"  {out_path}")
    print(f"  {file_size:.1f} MB")
    print(f"{'='*50}\n")


if __name__ == "__main__":
    build_workbook()
