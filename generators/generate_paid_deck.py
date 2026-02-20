#!/usr/bin/env python3
"""
Luminous Pulse — Paid Product PDF Generator
"50 Affirmations for the AI Age" printable card deck
57 pages: Cover, Instructions, 4 theme dividers, 50 cards, What's Next
"""

from reportlab.lib.colors import Color
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import textwrap
import os

FONT_DIR = os.path.expanduser("~/.claude/skills/canvas-design/canvas-fonts")
OUT_DIR = os.path.expanduser("~/luminous-pulse/products/core")

# Palette
NAVY = Color(0.10, 0.15, 0.27, 1)
DEEP_NAVY = Color(0.055, 0.068, 0.13, 1)
BLUE = Color(0.42, 0.71, 0.93, 1)
SOFT_BLUE = Color(0.55, 0.67, 0.80, 1)
AMBER = Color(0.96, 0.77, 0.19, 1)
WARM_AMBER = Color(0.98, 0.88, 0.50, 1)
LAVENDER = Color(0.71, 0.65, 0.84, 1)
WHITE = Color(0.95, 0.96, 0.98, 1)
DIM = Color(0.55, 0.58, 0.65, 1)

# Theme accent colors
THEME_COLORS = {
    "empowerment": BLUE,
    "career": AMBER,
    "morning": LAVENDER,
    "anxiety": Color(0.85, 0.87, 0.90, 1),
}

W, H = 432, 288  # 6x4 landscape at 72dpi


def register_fonts():
    fonts = {
        "Helvetica": "Helvetica.ttf",
        "InstrumentSans": "InstrumentSans-Regular.ttf",
        "InstrumentSans-Bold": "InstrumentSans-Bold.ttf",
    }
    for name, filename in fonts.items():
        path = os.path.join(FONT_DIR, filename)
        if os.path.exists(path):
            pdfmetrics.registerFont(TTFont(name, path))


def draw_bg(c, focus_x=None, focus_y=None):
    c.setFillColor(DEEP_NAVY)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    fx = focus_x or W / 2
    fy = focus_y or H / 2
    for i in range(15):
        t = i / 15
        r = 250 * (1 - t)
        c.setFillColor(Color(0.10, 0.14, 0.26, 0.015 * (1 - t)))
        c.circle(fx, fy, r, fill=1, stroke=0)


def draw_amber_dot(c, x, y, r=3):
    for i in range(10):
        t = i / 10
        gr = r * (1 + t * 3)
        c.setFillColor(Color(AMBER.red, AMBER.green, AMBER.blue, 0.06 * (1 - t)))
        c.circle(x, y, gr, fill=1, stroke=0)
    c.setFillColor(Color(AMBER.red, AMBER.green, AMBER.blue, 0.8))
    c.circle(x, y, r, fill=1, stroke=0)
    c.setFillColor(Color(1, 0.97, 0.85, 0.6))
    c.circle(x, y, r * 0.35, fill=1, stroke=0)


def draw_card_number(c, num):
    c.setFont("Helvetica", 9)
    c.setFillColor(Color(DIM.red, DIM.green, DIM.blue, 0.4))
    c.drawRightString(W - 24, 18, f"{num}")


def centered_text(c, text, y, font, size, color):
    c.setFont(font, size)
    c.setFillColor(color)
    tw = c.stringWidth(text, font, size)
    c.drawString(W / 2 - tw / 2, y, text)


# ============================================================
# Cover
# ============================================================
def page_cover(c):
    draw_bg(c, W / 2, H * 0.45)

    centered_text(c, "50 Affirmations for the AI Age", H * 0.65,
                  "Helvetica", 28, Color(WHITE.red, WHITE.green, WHITE.blue, 0.92))
    centered_text(c, "the complete collection.", H * 0.55,
                  "Helvetica", 13, Color(SOFT_BLUE.red, SOFT_BLUE.green, SOFT_BLUE.blue, 0.7))
    centered_text(c, "for humans navigating a world that's changing fast.", H * 0.48,
                  "Helvetica", 11, Color(SOFT_BLUE.red, SOFT_BLUE.green, SOFT_BLUE.blue, 0.5))

    draw_amber_dot(c, W / 2, H * 0.38, r=5)

    # Brand
    c.setFont("Helvetica", 18)
    lw = c.stringWidth("luminous", "Helvetica", 18)
    pw = c.stringWidth("pulse", "Helvetica", 18)
    gap = 6
    total = lw + gap + pw
    sx = W / 2 - total / 2
    c.setFillColor(Color(SOFT_BLUE.red, SOFT_BLUE.green, SOFT_BLUE.blue, 0.7))
    c.drawString(sx, H * 0.20, "luminous")
    c.setFillColor(Color(AMBER.red, AMBER.green, AMBER.blue, 0.7))
    c.drawString(sx + lw + gap, H * 0.20, "pulse")

    centered_text(c, "luminouspulse.co", H * 0.12,
                  "Helvetica", 9, Color(DIM.red, DIM.green, DIM.blue, 0.5))
    c.showPage()


# ============================================================
# Instructions
# ============================================================
def page_instructions(c):
    draw_bg(c, W * 0.3, H * 0.6)

    centered_text(c, "how to use this deck", H * 0.85,
                  "Helvetica", 20, Color(AMBER.red, AMBER.green, AMBER.blue, 0.85))

    # Three ways
    ways = [
        ("the daily draw", "pull one card each morning for 50 days."),
        ("the theme week", "pick one theme and go deep for a week."),
        ("the emergency card", "pin your top 3 where you'll see them daily."),
    ]

    c.setFont("Helvetica", 12)
    start_y = H * 0.68
    for i, (title, desc) in enumerate(ways):
        y = start_y - i * 40
        c.setFillColor(Color(AMBER.red, AMBER.green, AMBER.blue, 0.7))
        c.setFont("Helvetica", 12)
        tw = c.stringWidth(title, "Helvetica", 12)
        c.drawString(W / 2 - tw / 2, y, title)
        c.setFillColor(Color(WHITE.red, WHITE.green, WHITE.blue, 0.65))
        c.setFont("Helvetica", 10)
        dw = c.stringWidth(desc, "Helvetica", 10)
        c.drawString(W / 2 - dw / 2, y - 16, desc)

    # The practice
    centered_text(c, "say it aloud, three times, slowly. the feeling follows the words.", H * 0.14,
                  "Helvetica", 10, Color(LAVENDER.red, LAVENDER.green, LAVENDER.blue, 0.5))
    c.showPage()


# ============================================================
# Theme divider
# ============================================================
def page_theme_divider(c, theme_key, title, subtitle, desc):
    accent = THEME_COLORS[theme_key]
    draw_bg(c, W / 2, H * 0.5)

    # Theme title
    centered_text(c, title, H * 0.65,
                  "Helvetica", 24, Color(accent.red, accent.green, accent.blue, 0.85))

    # Subtitle
    centered_text(c, subtitle, H * 0.52,
                  "Helvetica", 12, Color(WHITE.red, WHITE.green, WHITE.blue, 0.7))

    # Description
    centered_text(c, desc, H * 0.42,
                  "Helvetica", 11, Color(SOFT_BLUE.red, SOFT_BLUE.green, SOFT_BLUE.blue, 0.55))

    # Decorative line
    cx = W / 2
    c.setStrokeColor(Color(accent.red, accent.green, accent.blue, 0.25))
    c.setLineWidth(0.5)
    c.line(cx - 60, H * 0.35, cx + 60, H * 0.35)
    draw_amber_dot(c, cx, H * 0.35, r=2)

    c.showPage()


# ============================================================
# Affirmation card
# ============================================================
def page_affirmation(c, affirmation, reflect, num, theme_key):
    accent = THEME_COLORS[theme_key]
    draw_bg(c, W / 2, H * 0.65)

    cx = W / 2

    # Auto-size affirmation text
    text_len = len(affirmation)
    if text_len < 60:
        font_size = 18
    elif text_len < 90:
        font_size = 16
    elif text_len < 120:
        font_size = 14
    else:
        font_size = 13

    # Wrap affirmation
    avg_char = font_size * 0.48
    chars = int(340 / avg_char)
    lines = textwrap.wrap(affirmation, width=chars)

    lh = font_size * 1.45
    block_h = len(lines) * lh
    start_y = H * 0.72 + block_h / 2

    # Opening quote mark
    c.setFont("Helvetica", 36)
    c.setFillColor(Color(accent.red, accent.green, accent.blue, 0.30))
    c.drawString(cx - 175, start_y + 12, "\u201c")

    # Affirmation lines
    c.setFont("Helvetica", font_size)
    c.setFillColor(Color(WHITE.red, WHITE.green, WHITE.blue, 0.93))
    for i, line in enumerate(lines):
        y = start_y - i * lh
        tw = c.stringWidth(line, "Helvetica", font_size)
        c.drawString(cx - tw / 2, y, line)

    # Divider
    div_y = start_y - len(lines) * lh - 14
    c.setStrokeColor(Color(accent.red, accent.green, accent.blue, 0.2))
    c.setLineWidth(0.4)
    c.line(cx - 60, div_y, cx + 60, div_y)
    draw_amber_dot(c, cx, div_y, r=1.5)

    # Reflect label
    reflect_y = div_y - 20
    c.setFont("Helvetica", 10)
    c.setFillColor(Color(LAVENDER.red, LAVENDER.green, LAVENDER.blue, 0.6))
    label = "reflect"
    lw = c.stringWidth(label, "Helvetica", 10)
    c.drawString(cx - lw / 2, reflect_y, label)

    # Reflect text — auto-size
    r_len = len(reflect)
    r_size = 10 if r_len < 140 else 9
    c.setFont("Helvetica", r_size)
    c.setFillColor(Color(SOFT_BLUE.red, SOFT_BLUE.green, SOFT_BLUE.blue, 0.6))
    r_chars = int(360 / (r_size * 0.45))
    r_lines = textwrap.wrap(reflect, width=r_chars)
    r_start = reflect_y - 16
    for i, line in enumerate(r_lines):
        y = r_start - i * (r_size * 1.4)
        tw = c.stringWidth(line, "Helvetica", r_size)
        c.drawString(cx - tw / 2, y, line)

    draw_card_number(c, num)
    c.showPage()


# ============================================================
# What's Next
# ============================================================
def page_whats_next(c):
    draw_bg(c, W / 2, H * 0.5)

    centered_text(c, "you just did something most people won't.", H * 0.80,
                  "Helvetica", 18, Color(WHITE.red, WHITE.green, WHITE.blue, 0.9))

    centered_text(c, "you invested in yourself.", H * 0.70,
                  "Helvetica", 14, Color(SOFT_BLUE.red, SOFT_BLUE.green, SOFT_BLUE.blue, 0.7))

    lines = [
        "pin your top 3 where you'll see them daily.",
        "share your favorite with someone who needs it.",
        "come back in 30 days and see which ones hit differently.",
    ]
    start_y = H * 0.54
    for i, line in enumerate(lines):
        y = start_y - i * 20
        c.setFont("Helvetica", 11)
        c.setFillColor(Color(AMBER.red, AMBER.green, AMBER.blue, 0.5))
        c.drawString(W * 0.15, y, "\u2192")
        c.setFillColor(Color(WHITE.red, WHITE.green, WHITE.blue, 0.7))
        c.drawString(W * 0.20, y, line)

    centered_text(c, "follow @luminouspulse.co for daily affirmations", H * 0.22,
                  "Helvetica", 12, Color(LAVENDER.red, LAVENDER.green, LAVENDER.blue, 0.6))

    # Brand
    c.setFont("Helvetica", 15)
    lw = c.stringWidth("luminous", "Helvetica", 15)
    pw = c.stringWidth("pulse", "Helvetica", 15)
    gap = 5
    total = lw + gap + pw
    sx = W / 2 - total / 2
    c.setFillColor(Color(SOFT_BLUE.red, SOFT_BLUE.green, SOFT_BLUE.blue, 0.6))
    c.drawString(sx, H * 0.12, "luminous")
    c.setFillColor(Color(AMBER.red, AMBER.green, AMBER.blue, 0.6))
    c.drawString(sx + lw + gap, H * 0.12, "pulse")

    c.showPage()


# ============================================================
# Card data — 50 top-rated affirmations with reflection prompts
# ============================================================
THEMES = {
    "empowerment": {
        "title": "ai-age empowerment",
        "subtitle": "for the moments when you wonder where you fit.",
        "desc": "these affirmations are your anchor.",
        "cards": [
            ("My intuition is trained on a lifetime of being human. No dataset compares.",
             "Think of a time your gut feeling was right \u2014 when the data said one thing but you knew better. That instinct isn\u2019t going anywhere."),
            ("I carry things no technology will ever replicate: lived experience, empathy, and purpose.",
             "Write down one moment where your empathy changed an outcome. That\u2019s your evidence. Keep it close."),
            ("I am irreplaceable \u2014 not because of what I produce, but because of who I am.",
             "If you couldn\u2019t list a single job title or skill, how would people describe your value? That description is the truest one."),
            ("I am not in competition with technology. I am in partnership with it.",
             "Where in your work could AI handle the repetitive parts so you can spend more time on what only you can do?"),
            ("Technology amplifies my creativity. It does not replace it.",
             "Name one creative idea you\u2019ve had recently that no tool prompted. Where did it come from? That source is yours alone."),
            ("My humanity is not a limitation. It is the entire point.",
             "When was the last time something deeply human \u2014 a laugh, a tear, a pause \u2014 changed the direction of a conversation?"),
            ("No algorithm will ever understand what it feels like to be me. That is my edge.",
             "Describe a feeling you\u2019ve had this week that you couldn\u2019t fully explain in words. That complexity is what makes you irreducible."),
            ("The things that make me human \u2014 doubt, courage, love \u2014 are features, not bugs.",
             "Pick one: doubt, courage, or love. When did that quality lead you to a better decision than pure logic would have?"),
            ("My story cannot be generated. It can only be lived.",
             "What\u2019s one chapter of your story that only you could have written? Not because it was easy \u2014 because it was yours."),
            ("I am not a prompt. I am the person behind it.",
             "The next time you use AI, pause before you type. You\u2019re the one deciding what matters. That\u2019s the job."),
            ("I don\u2019t need to outperform a machine. I need to be fully human.",
             "What does \u201cfully human\u201d look like for you today? Not the ideal version \u2014 the real one."),
            ("I am more than my output. I am the meaning behind it.",
             "Think about the last thing you created. What was the intention behind it? That intention is the part no tool can generate."),
            ("The most powerful technology in any room is still a human being who knows their worth.",
             "Recall a room where your presence \u2014 not your slides \u2014 shifted the energy. You were the technology that mattered most."),
            ("The question is not whether AI can do what I do. The question is whether it can be who I am.",
             "Make a list of what you do versus who you are. The second column is what actually defines your value."),
        ],
    },
    "career": {
        "title": "career confidence",
        "subtitle": "for the days when imposter syndrome meets automation anxiety.",
        "desc": "you\u2019re not falling behind. these cards are your proof.",
        "cards": [
            ("My value at work is not measured in output speed. It is measured in judgment.",
             "Think of your best contribution this year. Was it fast? Or was it thoughtful? The things that matter most rarely come from moving faster."),
            ("My human skills are not soft skills. They are survival skills.",
             "Name three \u201csoft\u201d skills you used this week. Now rename them: reading the room, building trust, making the call. These are essential."),
            ("I adapt, I learn, and I bring something to every room that no tool ever will.",
             "List three skills you\u2019ve learned in the past five years that you never planned to learn. You adapt. You always have."),
            ("I can learn any tool. No tool can learn to be me.",
             "How many tools have you learned and outgrown in your career? Each one was a chapter, not the whole story."),
            ("I read rooms, build trust, and make calls that no dashboard can make. That is my job.",
             "When was the last time you made a decision that couldn\u2019t be justified by data alone \u2014 and it turned out right?"),
            ("I have reinvented myself before. I will do it again. This is what I do.",
             "Write down every major career pivot you\u2019ve made. Count them. That number is your evidence."),
            ("My instinct to ask \u2018should we?\u2019 when everyone else asks \u2018can we?\u2019 \u2014 that is leadership.",
             "Think of a time you slowed a room down by asking the uncomfortable question. That moment probably saved something."),
            ("I do not need to know everything about AI to be valuable.",
             "What do you know deeply \u2014 not about AI, but about your craft? That depth is what makes you irreplaceable."),
            ("I am allowed to learn slowly. Mastery and speed are not the same thing.",
             "What\u2019s one thing you\u2019ve mastered that took years, not days? Real skill is built slowly. That hasn\u2019t changed."),
            ("Today, I bring something to my work that no prompt could ever generate: me.",
             "Before your next meeting, take one breath and remind yourself: you are the irreplaceable variable in every room you enter."),
            ("My experience is not a liability. It is an unfair advantage.",
             "What pattern have you seen repeat that a new hire or new tool wouldn\u2019t recognize? That pattern recognition is your edge."),
            ("I am not behind. I am building something that takes time: expertise.",
             "Compare where you were 5 years ago to today. You\u2019re not behind. You\u2019re compounding."),
            ("I will not panic about a future I am actively building.",
             "Name one thing you\u2019re doing today that builds toward your future. You\u2019re not frozen. You\u2019re in motion."),
            ("I have survived every industry shift so far. My track record speaks for itself.",
             "List every major change in your field you\u2019ve navigated. You survived all of them. This one is no different."),
        ],
    },
    "morning": {
        "title": "morning motivation",
        "subtitle": "for starting your day grounded, not scrolling.",
        "desc": "read one of these before you open your laptop.",
        "cards": [
            ("I wake up with something no machine ever will: a reason to care about today.",
             "Before you reach for your phone: what is one thing you genuinely care about doing today? Start there."),
            ("I am the author of this day. Not the algorithm, not the feed, not the forecast.",
             "Write your one-sentence intention for today. Not a to-do \u2014 an intention. That\u2019s your opening line."),
            ("I am whole before I open my laptop.",
             "Sit with this for 30 seconds before you start working. Your worth doesn\u2019t boot up with your computer."),
            ("Today, I lead with curiosity. Not fear.",
             "Name one thing you\u2019re curious about this morning \u2014 genuinely curious, not anxiously monitoring. Let it guide your first hour."),
            ("I am allowed to take my time. Not everything needs to move at machine speed.",
             "What is one thing you\u2019ll do slowly and intentionally today? Slowness is not weakness \u2014 it\u2019s a choice."),
            ("This morning, I choose to focus on what I can create, not what I might lose.",
             "Write down three things you want to create or contribute today. Not protect \u2014 create. That shift changes your energy."),
            ("I am ready for today. Not because I know what\u2019s coming, but because I know who I am.",
             "Complete this sentence: \u201cI am someone who ___.\u201d Don\u2019t list skills \u2014 list character."),
            ("I will not let a headline decide how I feel about my future.",
             "If something spiked your anxiety this morning, ask: is this about my life, or is this about clicks?"),
            ("Today I will do one thing that only a human can do. That is enough.",
             "What\u2019s your one human thing today? A real conversation, a creative idea, a moment of kindness."),
            ("I do not need to optimize my morning. I need to feel it.",
             "Skip the productivity hack. What do you actually feel right now? Name it. That awareness is the most productive thing you can do."),
            ("Today I choose to see change as an invitation, not a threat.",
             "What changed recently that you initially resisted but now appreciate? That pattern is your proof."),
        ],
    },
    "anxiety": {
        "title": "anxiety relief",
        "subtitle": "for the nights when the \u201cwhat ifs\u201d are loud.",
        "desc": "these words are your permission slip to breathe.",
        "cards": [
            ("I give myself permission to navigate this moment with curiosity, not panic.",
             "What\u2019s one thing about AI that excites you \u2014 separate from what scares you? Hold both feelings at once."),
            ("I have adapted before. I will adapt again. My resilience is not a theory \u2014 it is my lived history.",
             "Write down your three hardest transitions. You\u2019re still here. Adaptation is something you already are."),
            ("I survived every \u2018worst day\u2019 I ever had. My track record is 100%.",
             "Name the day you were most sure you wouldn\u2019t make it through. You\u2019re reading this, which means you did."),
            ("I replace \u2018what if it all goes wrong\u2019 with \u2018what if I handle it.\u2019",
             "The next time a worst-case scenario enters your mind, complete this: \u201cAnd if that happens, I will ___.\u201d"),
            ("I am not broken for feeling anxious. I am awake in a world that is changing fast.",
             "Your anxiety is proof you\u2019re paying attention. Acknowledge it, thank it, then decide what you actually want to do."),
            ("The headlines are designed to scare me. My life is designed to be lived.",
             "How much of your anxiety this week came from headlines versus your actual lived experience? Notice the gap."),
            ("I am allowed to feel overwhelmed by how fast things are changing.",
             "Say it out loud: \u201cI am overwhelmed.\u201d Take one breath. You don\u2019t need to fix the feeling. Just name it."),
            ("I can hold two truths: AI is powerful, and so am I.",
             "Where else do you hold two truths at once? Hard and beautiful. Scary and exciting. You\u2019re already good at this."),
            ("I am not fragile. I am paying attention. There is a difference.",
             "What did you notice this week that others missed? Your sensitivity is not fragility \u2014 it\u2019s intelligence."),
            ("My value does not decrease because a tool got faster.",
             "Did your favorite teacher lose value when calculators arrived? Speed was never the point."),
            ("I do not need certainty to feel safe. I have something better: adaptability.",
             "List everything uncertain right now. Then list every uncertain thing you\u2019ve navigated. The second list is always longer."),
        ],
    },
}


# ============================================================
# Main
# ============================================================
if __name__ == "__main__":
    register_fonts()
    path = os.path.join(OUT_DIR, "50-affirmations-paid-deck.pdf")
    c = canvas.Canvas(path, pagesize=(W, H))

    page_cover(c)
    page_instructions(c)

    card_num = 1
    for theme_key in ["empowerment", "career", "morning", "anxiety"]:
        theme = THEMES[theme_key]
        page_theme_divider(c, theme_key, theme["title"], theme["subtitle"], theme["desc"])
        for affirmation, reflect in theme["cards"]:
            page_affirmation(c, affirmation, reflect, card_num, theme_key)
            card_num += 1

    page_whats_next(c)

    c.save()
    print(f"Paid deck PDF saved: {path}")
    print(f"Total cards: {card_num - 1}")
    print(f"Total pages: {card_num - 1 + 6}")  # cards + cover + instructions + 4 dividers + whats next
