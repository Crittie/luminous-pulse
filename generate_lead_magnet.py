#!/usr/bin/env python3
"""
Luminous Pulse — Lead Magnet PDF Generator
"7 Affirmations for the AI Age" printable card deck
10 pages: Cover, Instructions, 7 Cards, What's Next
"""

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.colors import Color
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import math
import os
import textwrap

FONT_DIR = os.path.expanduser("~/.claude/skills/canvas-design/canvas-fonts")
OUT_DIR = os.path.expanduser("~/affirmations-project")

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

# Page size — 4x6 card
W, H = 432, 288  # 6" x 4" at 72dpi, landscape


def register_fonts():
    fonts = {
        "Helvetica": "Helvetica.ttf",
        "Helvetica": "Helvetica.ttf",
        "InstrumentSans": "InstrumentSans-Regular.ttf",
        "InstrumentSans-Bold": "InstrumentSans-Bold.ttf",
    }
    for name, filename in fonts.items():
        path = os.path.join(FONT_DIR, filename)
        if os.path.exists(path):
            pdfmetrics.registerFont(TTFont(name, path))


def draw_bg(c, focus_x=None, focus_y=None):
    """Dark navy background with subtle radial glow."""
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
    """Small amber glow dot."""
    for i in range(10):
        t = i / 10
        gr = r * (1 + t * 3)
        c.setFillColor(Color(AMBER.red, AMBER.green, AMBER.blue, 0.06 * (1 - t)))
        c.circle(x, y, gr, fill=1, stroke=0)
    c.setFillColor(Color(AMBER.red, AMBER.green, AMBER.blue, 0.8))
    c.circle(x, y, r, fill=1, stroke=0)
    c.setFillColor(Color(1, 0.97, 0.85, 0.6))
    c.circle(x, y, r * 0.35, fill=1, stroke=0)


def draw_decorative_line(c):
    """Subtle horizontal divider line."""
    cx = W / 2
    line_w = 80
    c.setStrokeColor(Color(AMBER.red, AMBER.green, AMBER.blue, 0.25))
    c.setLineWidth(0.5)
    c.line(cx - line_w, H * 0.5, cx + line_w, H * 0.5)
    draw_amber_dot(c, cx, H * 0.5, r=2)


def draw_text_block(c, text, x, y, font, size, color, max_width=360,
                    line_height=None, align="center"):
    """Draw wrapped text block."""
    c.setFont(font, size)
    c.setFillColor(color)
    lh = line_height or size * 1.5

    # Estimate chars per line
    avg_char = size * 0.5
    chars = int(max_width / avg_char)
    lines = textwrap.wrap(text, width=chars)

    for i, line in enumerate(lines):
        ly = y - i * lh
        if align == "center":
            tw = c.stringWidth(line, font, size)
            c.drawString(x - tw / 2, ly, line)
        else:
            c.drawString(x, ly, line)

    return len(lines)


def draw_card_number(c, num):
    """Small card number in bottom-right corner."""
    c.setFont("Helvetica", 9)
    c.setFillColor(Color(DIM.red, DIM.green, DIM.blue, 0.4))
    c.drawRightString(W - 24, 18, f"{num}")


# ============================================================
# PAGE 1: Cover
# ============================================================
def page_cover(c):
    draw_bg(c, W / 2, H * 0.45)

    # Title
    c.setFont("Helvetica", 32)
    c.setFillColor(Color(WHITE.red, WHITE.green, WHITE.blue, 0.92))
    title = "7 Affirmations for the AI Age"
    tw = c.stringWidth(title, "Helvetica", 32)
    c.drawString(W / 2 - tw / 2, H * 0.62, title)

    # Subtitle
    c.setFont("Helvetica", 13)
    c.setFillColor(Color(SOFT_BLUE.red, SOFT_BLUE.green, SOFT_BLUE.blue, 0.7))
    sub = "daily reminders that your humanity is your superpower."
    sw = c.stringWidth(sub, "Helvetica", 13)
    c.drawString(W / 2 - sw / 2, H * 0.52, sub)

    # Amber spark in center
    draw_amber_dot(c, W / 2, H * 0.42, r=5)

    # Brand
    c.setFont("Helvetica", 18)
    c.setFillColor(Color(SOFT_BLUE.red, SOFT_BLUE.green, SOFT_BLUE.blue, 0.7))
    lw = c.stringWidth("luminous", "Helvetica", 18)
    pw = c.stringWidth("pulse", "Helvetica", 18)
    gap = 6
    total = lw + gap + pw
    sx = W / 2 - total / 2

    c.drawString(sx, H * 0.22, "luminous")
    c.setFillColor(Color(AMBER.red, AMBER.green, AMBER.blue, 0.7))
    c.drawString(sx + lw + gap, H * 0.22, "pulse")

    # URL
    c.setFont("Helvetica", 9)
    c.setFillColor(Color(DIM.red, DIM.green, DIM.blue, 0.5))
    url = "luminouspulse.co"
    uw = c.stringWidth(url, "Helvetica", 9)
    c.drawString(W / 2 - uw / 2, H * 0.14, url)

    c.showPage()


# ============================================================
# PAGE 2: Instructions
# ============================================================
def page_instructions(c):
    draw_bg(c, W * 0.3, H * 0.6)

    # Title
    c.setFont("Helvetica", 20)
    c.setFillColor(Color(AMBER.red, AMBER.green, AMBER.blue, 0.85))
    title = "the practice"
    tw = c.stringWidth(title, "Helvetica", 20)
    c.drawString(W / 2 - tw / 2, H * 0.82, title)

    c.setFont("Helvetica", 10)
    c.setFillColor(Color(DIM.red, DIM.green, DIM.blue, 0.6))
    sub = "2 minutes each morning"
    sw = c.stringWidth(sub, "Helvetica", 10)
    c.drawString(W / 2 - sw / 2, H * 0.74, sub)

    # Steps
    steps = [
        "pick one card each morning.",
        "stand up. posture matters.",
        "take one deep breath.",
        "say the affirmation aloud, three times, slowly.",
        "sit with the feeling for 30 seconds.",
        "reflect using the prompt below the affirmation.",
    ]

    c.setFont("Helvetica", 12)
    start_y = H * 0.62
    for i, step in enumerate(steps):
        y = start_y - i * 22

        # Number
        c.setFillColor(Color(AMBER.red, AMBER.green, AMBER.blue, 0.6))
        c.drawString(W * 0.18, y, f"{i + 1}.")

        # Text
        c.setFillColor(Color(WHITE.red, WHITE.green, WHITE.blue, 0.8))
        c.drawString(W * 0.23, y, step)

    # Bottom note
    c.setFont("Helvetica", 10)
    c.setFillColor(Color(LAVENDER.red, LAVENDER.green, LAVENDER.blue, 0.5))
    note = "the feeling follows the words. not the other way around."
    nw = c.stringWidth(note, "Helvetica", 10)
    c.drawString(W / 2 - nw / 2, H * 0.12, note)

    c.showPage()


# ============================================================
# PAGES 3-9: Affirmation Cards
# ============================================================
CARDS = [
    {
        "affirmation": "My intuition is trained on a lifetime of being human. No dataset compares.",
        "reflect": "Think of a time your gut feeling was right \u2014 when the data said one thing but you knew better. That instinct isn\u2019t going anywhere.",
    },
    {
        "affirmation": "Technology amplifies my creativity. It does not replace it.",
        "reflect": "Name one creative idea you\u2019ve had recently that no tool prompted. Where did it come from? That source is yours alone.",
    },
    {
        "affirmation": "I adapt, I learn, and I bring something to every room that no tool ever will.",
        "reflect": "List three skills you\u2019ve learned in the past five years that you never planned to learn. You adapt. You always have.",
    },
    {
        "affirmation": "I am not in competition with technology. I am in partnership with it.",
        "reflect": "Where in your work could AI handle the repetitive parts so you can spend more time on the parts only you can do?",
    },
    {
        "affirmation": "I give myself permission to navigate this moment with curiosity, not panic.",
        "reflect": "What\u2019s one thing about AI that genuinely excites you \u2014 separate from what scares you? Hold both feelings at once.",
    },
    {
        "affirmation": "My value is not measured in output speed. It is measured in judgment.",
        "reflect": "Think of your best contribution this year. Was it fast? Or was it thoughtful? The things that matter most rarely come from moving faster.",
    },
    {
        "affirmation": "I carry things no technology will ever replicate: lived experience, empathy, and purpose.",
        "reflect": "Write down one moment where your empathy changed an outcome. That\u2019s your evidence. Keep it close.",
    },
]


def page_affirmation(c, card, num):
    draw_bg(c, W / 2, H * 0.65)

    cx = W / 2

    # Affirmation text
    c.setFont("Helvetica", 18)
    c.setFillColor(Color(WHITE.red, WHITE.green, WHITE.blue, 0.93))

    # Wrap the affirmation
    avg_char = 18 * 0.48
    chars = int(340 / avg_char)
    lines = textwrap.wrap(card["affirmation"], width=chars)

    # Center the block vertically in upper portion
    lh = 26
    block_h = len(lines) * lh
    start_y = H * 0.72 + block_h / 2

    # Opening quote mark
    c.setFont("Helvetica", 36)
    c.setFillColor(Color(AMBER.red, AMBER.green, AMBER.blue, 0.35))
    c.drawString(cx - 175, start_y + 12, "\u201c")

    c.setFont("Helvetica", 18)
    c.setFillColor(Color(WHITE.red, WHITE.green, WHITE.blue, 0.93))
    for i, line in enumerate(lines):
        y = start_y - i * lh
        tw = c.stringWidth(line, "Helvetica", 18)
        c.drawString(cx - tw / 2, y, line)

    # Divider
    div_y = start_y - len(lines) * lh - 16
    c.setStrokeColor(Color(AMBER.red, AMBER.green, AMBER.blue, 0.2))
    c.setLineWidth(0.4)
    c.line(cx - 60, div_y, cx + 60, div_y)
    draw_amber_dot(c, cx, div_y, r=1.5)

    # Reflect label
    reflect_y = div_y - 22
    c.setFont("Helvetica", 10)
    c.setFillColor(Color(LAVENDER.red, LAVENDER.green, LAVENDER.blue, 0.6))
    label = "reflect"
    lw = c.stringWidth(label, "Helvetica", 10)
    c.drawString(cx - lw / 2, reflect_y, label)

    # Reflect text
    c.setFont("Helvetica", 10.5)
    c.setFillColor(Color(SOFT_BLUE.red, SOFT_BLUE.green, SOFT_BLUE.blue, 0.65))
    r_chars = int(340 / (10.5 * 0.45))
    r_lines = textwrap.wrap(card["reflect"], width=r_chars)
    r_start = reflect_y - 18
    for i, line in enumerate(r_lines):
        y = r_start - i * 15
        tw = c.stringWidth(line, "Helvetica", 10.5)
        c.drawString(cx - tw / 2, y, line)

    draw_card_number(c, num)
    c.showPage()


# ============================================================
# PAGE 10: What's Next
# ============================================================
def page_whats_next(c):
    draw_bg(c, W / 2, H * 0.5)

    cx = W / 2

    # Title
    c.setFont("Helvetica", 22)
    c.setFillColor(Color(WHITE.red, WHITE.green, WHITE.blue, 0.9))
    title = "these 7 are just the beginning."
    tw = c.stringWidth(title, "Helvetica", 22)
    c.drawString(cx - tw / 2, H * 0.78, title)

    # Themes
    themes = [
        "ai-age empowerment",
        "career confidence",
        "morning motivation",
        "anxiety relief",
    ]

    c.setFont("Helvetica", 12)
    start_y = H * 0.60
    for i, theme in enumerate(themes):
        y = start_y - i * 20
        c.setFillColor(Color(AMBER.red, AMBER.green, AMBER.blue, 0.5))
        c.drawString(cx - 80, y, "\u2192")
        c.setFillColor(Color(WHITE.red, WHITE.green, WHITE.blue, 0.75))
        c.drawString(cx - 62, y, theme)

    # Follow CTA
    c.setFont("Helvetica", 13)
    c.setFillColor(Color(LAVENDER.red, LAVENDER.green, LAVENDER.blue, 0.65))
    cta = "follow @luminouspulse.co for daily affirmations"
    cw = c.stringWidth(cta, "Helvetica", 13)
    c.drawString(cx - cw / 2, H * 0.25, cta)

    # Brand
    c.setFont("Helvetica", 15)
    lw = c.stringWidth("luminous", "Helvetica", 15)
    pw = c.stringWidth("pulse", "Helvetica", 15)
    gap = 5
    total = lw + gap + pw
    sx = cx - total / 2

    c.setFillColor(Color(SOFT_BLUE.red, SOFT_BLUE.green, SOFT_BLUE.blue, 0.6))
    c.drawString(sx, H * 0.14, "luminous")
    c.setFillColor(Color(AMBER.red, AMBER.green, AMBER.blue, 0.6))
    c.drawString(sx + lw + gap, H * 0.14, "pulse")

    c.showPage()


# ============================================================
# MAIN
# ============================================================
if __name__ == "__main__":
    register_fonts()
    path = os.path.join(OUT_DIR, "7-affirmations-lead-magnet.pdf")
    c = canvas.Canvas(path, pagesize=(W, H))

    page_cover(c)
    page_instructions(c)
    for i, card in enumerate(CARDS):
        page_affirmation(c, card, i + 1)
    page_whats_next(c)

    c.save()
    print(f"Lead magnet PDF saved: {path}")
