#!/usr/bin/env python3
"""
Luminous Pulse - 7 AI-Age Affirmations Card Deck
Printable PDF with 4x6 inch cards
"""

from reportlab.lib.pagesizes import letter, landscape
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor
import textwrap

# Register fonts
font_path = "/sessions/stoic-epic-cerf/mnt/.skills/skills/canvas-design/canvas-fonts/"
pdfmetrics.registerFont(TTFont('Jura-Light', f'{font_path}Jura-Light.ttf'))
pdfmetrics.registerFont(TTFont('Jura-Medium', f'{font_path}Jura-Medium.ttf'))
pdfmetrics.registerFont(TTFont('GeistMono', f'{font_path}GeistMono-Regular.ttf'))
pdfmetrics.registerFont(TTFont('InstrumentSans', f'{font_path}InstrumentSans-Regular.ttf'))

# Color palette
twilight = HexColor('#16213e')
blue = HexColor('#6CB4EE')
amber = HexColor('#F4C430')
lavender = HexColor('#B4A7D6')
dark_navy = HexColor('#1a2744')
white = HexColor('#e8e8e8')

# Page setup - Letter landscape for 2 cards per page (4x6 each)
page_width, page_height = landscape(letter)
card_width = 4 * 72  # 4 inches
card_height = 6 * 72  # 6 inches

# Create PDF
pdf_file = '/sessions/stoic-epic-cerf/mnt/affirmations-project/luminous-pulse-affirmation-deck.pdf'
c = canvas.Canvas(pdf_file, pagesize=landscape(letter))

def draw_pulse_background(c, x, y, width, height, intensity='medium'):
    """Draw subtle concentric pulses background"""
    c.saveState()

    center_x = x + width / 2
    center_y = y + height / 2

    # Draw subtle concentric circles
    if intensity == 'high':
        radii = [20, 40, 60, 80, 100, 120, 140, 160, 180, 200, 220, 240]
        opacity = 0.15
    elif intensity == 'low':
        radii = [30, 70, 110, 150, 190, 230]
        opacity = 0.08
    else:  # medium
        radii = [25, 55, 85, 115, 145, 175, 205]
        opacity = 0.12

    for radius in radii:
        c.setStrokeColor(blue)
        c.setStrokeAlpha(opacity)
        c.setLineWidth(0.5)
        c.circle(center_x, center_y, radius, stroke=1, fill=0)

    # Add some dotted rings
    c.setDash([2, 4])
    c.setStrokeColor(lavender)
    c.setStrokeAlpha(opacity * 0.7)
    for r in [45, 95, 165]:
        c.circle(center_x, center_y, r, stroke=1, fill=0)

    c.setDash([])  # Reset dash
    c.restoreState()

def draw_card_front(c, x, y, affirmation_text, card_number):
    """Draw affirmation card front"""
    # Background
    c.setFillColor(dark_navy)
    c.rect(x, y, card_width, card_height, fill=1, stroke=0)

    # Pulse background
    draw_pulse_background(c, x, y, card_width, card_height, 'medium')

    # Border
    c.setStrokeColor(blue)
    c.setStrokeAlpha(0.3)
    c.setLineWidth(1)
    c.rect(x + 10, y + 10, card_width - 20, card_height - 20, fill=0, stroke=1)

    # Card number (top right, small)
    c.setFont('GeistMono', 8)
    c.setFillColor(lavender)
    c.setFillAlpha(0.5)
    c.drawRightString(x + card_width - 20, y + card_height - 25, f"{card_number}/7")
    c.setFillAlpha(1.0)

    # Affirmation text - centered, wrapped if needed
    c.setFont('Jura-Light', 20)  # Reduced from 24
    c.setFillColor(white)

    # Wrap text
    max_width = card_width - 70  # Leave margins
    words = affirmation_text.split()
    lines = []
    current_line = []

    for word in words:
        test_line = ' '.join(current_line + [word])
        if c.stringWidth(test_line, 'Jura-Light', 20) <= max_width:
            current_line.append(word)
        else:
            if current_line:
                lines.append(' '.join(current_line))
            current_line = [word]
    if current_line:
        lines.append(' '.join(current_line))

    # Center the text block vertically
    line_height = 28  # Reduced from 32
    total_height = len(lines) * line_height
    start_y = y + (card_height / 2) + (total_height / 2)

    for i, line in enumerate(lines):
        text_width = c.stringWidth(line, 'Jura-Light', 20)
        c.drawString(x + (card_width - text_width) / 2, start_y - i * line_height, line)

    # Subtle accent marks (corner details)
    c.setStrokeColor(amber)
    c.setStrokeAlpha(0.4)
    c.setLineWidth(1.5)
    # Top left corner accent
    c.line(x + 15, y + card_height - 15, x + 30, y + card_height - 15)
    c.line(x + 15, y + card_height - 15, x + 15, y + card_height - 30)
    # Bottom right corner accent
    c.line(x + card_width - 15, y + 15, x + card_width - 30, y + 15)
    c.line(x + card_width - 15, y + 15, x + card_width - 15, y + 30)
    c.setStrokeAlpha(1.0)

def draw_card_back(c, x, y, reflection_text):
    """Draw card back with reflection prompt"""
    # Background
    c.setFillColor(twilight)
    c.rect(x, y, card_width, card_height, fill=1, stroke=0)

    # Subtle pulse background
    draw_pulse_background(c, x, y, card_width, card_height, 'low')

    # Border
    c.setStrokeColor(lavender)
    c.setStrokeAlpha(0.3)
    c.setLineWidth(1)
    c.rect(x + 10, y + 10, card_width - 20, card_height - 20, fill=0, stroke=1)

    # "reflect" label at top
    c.setFont('GeistMono', 9)
    c.setFillColor(amber)
    c.setFillAlpha(0.7)
    text_width = c.stringWidth('reflect', 'GeistMono', 9)
    c.drawString(x + (card_width - text_width) / 2, y + card_height - 40, 'reflect')
    c.setFillAlpha(1.0)

    # Reflection text
    c.setFont('InstrumentSans', 10)  # Reduced from 11
    c.setFillColor(white)

    # Wrap reflection text
    max_width = card_width - 60
    wrapped = textwrap.wrap(reflection_text, width=70)  # Increased from 65

    line_height = 16  # Reduced from 18
    start_y = y + card_height - 75

    for i, line in enumerate(wrapped):
        c.drawString(x + 30, start_y - i * line_height, line)

    # Bottom logo mark
    c.setFont('Jura-Light', 10)
    c.setFillColor(lavender)
    c.setFillAlpha(0.5)
    logo_text = "luminous pulse"
    text_width = c.stringWidth(logo_text, 'Jura-Light', 10)
    c.drawString(x + (card_width - text_width) / 2, y + 25, logo_text)
    c.setFillAlpha(1.0)

def draw_cover_page(c):
    """Draw the cover page with title and intro"""
    c.setFillColor(dark_navy)
    c.rect(0, 0, page_width, page_height, fill=1, stroke=0)

    # Large pulse background centered
    draw_pulse_background(c, 0, 0, page_width, page_height, 'high')

    # Title
    c.setFont('Jura-Light', 48)
    c.setFillColor(white)
    title = "7 affirmations"
    title_width = c.stringWidth(title, 'Jura-Light', 48)
    c.drawString((page_width - title_width) / 2, page_height - 150, title)

    c.setFont('Jura-Light', 28)
    subtitle = "for the age of ai"
    subtitle_width = c.stringWidth(subtitle, 'Jura-Light', 28)
    c.drawString((page_width - subtitle_width) / 2, page_height - 190, subtitle)

    # Tagline
    c.setFont('InstrumentSans', 14)
    c.setFillColor(lavender)
    tagline = "your humanity is your superpower"
    tagline_width = c.stringWidth(tagline, 'InstrumentSans', 14)
    c.drawString((page_width - tagline_width) / 2, page_height - 240, tagline)

    # Logo watermark
    try:
        logo_img = ImageReader('/sessions/stoic-epic-cerf/mnt/affirmations-project/luminous-pulse-logo.png')
        logo_size = 200
        c.drawImage(logo_img, (page_width - logo_size) / 2, (page_height / 2) - 100,
                   width=logo_size, height=logo_size, mask='auto', preserveAspectRatio=True)
    except:
        pass

    # Bottom info
    c.setFont('GeistMono', 10)
    c.setFillColor(white)
    c.setFillAlpha(0.7)
    info_lines = [
        "daily reminders designed for humans",
        "navigating a world of ai",
        "",
        "@luminouspulse.co",
        "luminouspulse.co"
    ]
    y_pos = 120
    for line in info_lines:
        line_width = c.stringWidth(line, 'GeistMono', 10)
        c.drawString((page_width - line_width) / 2, y_pos, line)
        y_pos -= 18
    c.setFillAlpha(1.0)

    c.showPage()

def draw_instructions_page(c):
    """Draw the 'how to use' instructions page"""
    # Background
    c.setFillColor(twilight)
    c.rect(0, 0, page_width, page_height, fill=1, stroke=0)

    draw_pulse_background(c, 0, 0, page_width, page_height, 'medium')

    # Title
    c.setFont('Jura-Light', 36)
    c.setFillColor(amber)
    title = "how to use this deck"
    title_width = c.stringWidth(title, 'Jura-Light', 36)
    c.drawString((page_width - title_width) / 2, page_height - 100, title)

    # Instructions
    c.setFont('InstrumentSans', 13)
    c.setFillColor(white)

    instructions = [
        "the practice (2 minutes)",
        "",
        "1. pick one card each morning",
        "2. stand up — posture matters",
        "3. take one deep breath",
        "4. say the affirmation aloud, three times, slowly",
        "5. sit with the feeling for 30 seconds",
        "6. reflect using the prompt on the back",
        "",
        "the feeling follows the words.",
        "not the other way around.",
    ]

    y_pos = page_height - 180
    for line in instructions:
        if line == "":
            y_pos -= 15
            continue
        if line.startswith("the") or line == "not the other way around.":
            c.setFillColor(lavender)
        else:
            c.setFillColor(white)
        c.drawString(180, y_pos, line)
        y_pos -= 24

    # Tip box
    c.setFont('InstrumentSans', 11)
    c.setFillColor(amber)
    c.setFillAlpha(0.8)
    tip = "tip: pin your favorite to your desk, mirror, or laptop lid."
    c.drawString(180, y_pos - 40, tip)
    tip2 = "let it find you throughout the day."
    c.drawString(180, y_pos - 60, tip2)
    c.setFillAlpha(1.0)

    c.showPage()

# Affirmations data
affirmations = [
    {
        "front": "my intuition is trained on a lifetime of being human. no dataset compares.",
        "back": "think of a time your gut feeling turned out to be right — when the data said one thing but you knew better. what did that feel like? that instinct isn't going anywhere."
    },
    {
        "front": "technology amplifies my creativity. it does not replace it.",
        "back": "name one creative idea you've had recently that no tool prompted you to have. where did it come from? that source is yours alone."
    },
    {
        "front": "i adapt, i learn, and i bring something to every room that no tool ever will.",
        "back": "list three skills you've learned in the past five years that you never planned to learn. notice the pattern: you adapt. you always have."
    },
    {
        "front": "i am not in competition with technology. i am in partnership with it.",
        "back": "where in your work could ai handle the repetitive parts so you can spend more time on the parts only you can do? that reframe changes everything."
    },
    {
        "front": "i give myself permission to navigate this moment with curiosity, not panic.",
        "back": "what's one thing about ai that genuinely excites you — separate from what scares you? hold both feelings at once. that's maturity, not contradiction."
    },
    {
        "front": "my value is not measured in output speed. it is measured in judgment.",
        "back": "think of your best contribution at work this year. was it fast? or was it thoughtful? the things that matter most rarely come from moving faster."
    },
    {
        "front": "i carry things no technology will ever replicate: lived experience, empathy, and purpose.",
        "back": "write down one moment where your empathy changed an outcome — a conversation, a decision, a relationship. that's your evidence. keep it close."
    }
]

# Generate PDF
# Page 1: Cover
draw_cover_page(c)

# Page 2: Instructions
draw_instructions_page(c)

# Pages 3-9: Affirmation cards (front and back, 2 per page)
for i, aff in enumerate(affirmations):
    # Card front (left side)
    draw_card_front(c, 36, (page_height - card_height) / 2, aff['front'], i + 1)

    # Card back (right side)
    draw_card_back(c, page_width - card_width - 36, (page_height - card_height) / 2, aff['back'])

    c.showPage()

# Final page: "What's next"
c.setFillColor(dark_navy)
c.rect(0, 0, page_width, page_height, fill=1, stroke=0)

draw_pulse_background(c, 0, 0, page_width, page_height, 'medium')

c.setFont('Jura-Light', 32)
c.setFillColor(amber)
title = "want more?"
title_width = c.stringWidth(title, 'Jura-Light', 32)
c.drawString((page_width - title_width) / 2, page_height - 120, title)

c.setFont('InstrumentSans', 13)
c.setFillColor(white)
lines = [
    "these 7 affirmations are just the beginning.",
    "",
    "follow @luminouspulse.co for daily affirmations",
    "visit luminouspulse.co for more resources",
    "",
    "built human. staying human."
]

y_pos = page_height - 200
for line in lines:
    if line == "":
        y_pos -= 15
        continue
    line_width = c.stringWidth(line, 'InstrumentSans', 13)
    c.drawString((page_width - line_width) / 2, y_pos, line)
    y_pos -= 24

c.setFont('Jura-Light', 18)
c.setFillColor(lavender)
tagline = "your humanity is your superpower"
tagline_width = c.stringWidth(tagline, 'Jura-Light', 18)
c.drawString((page_width - tagline_width) / 2, 100, tagline)

c.save()

print(f"✓ Affirmation deck created: {pdf_file}")
print(f"  - Cover page")
print(f"  - Instructions page")
print(f"  - 7 affirmation cards (front & back)")
print(f"  - Final 'what's next' page")
print(f"  Total: 10 pages")
