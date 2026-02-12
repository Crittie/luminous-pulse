#!/usr/bin/env python3
"""
Luminous Pulse Logo - Instagram Profile Picture
Circular format, 1000x1000px for high quality
Concentric pulses with minimal typography
"""

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from PIL import Image, ImageDraw, ImageFont
import math

# Register fonts
font_path = "/sessions/stoic-epic-cerf/mnt/.skills/skills/canvas-design/canvas-fonts/"
pdfmetrics.registerFont(TTFont('Jura-Light', f'{font_path}Jura-Light.ttf'))
pdfmetrics.registerFont(TTFont('GeistMono', f'{font_path}GeistMono-Regular.ttf'))

# Create circular logo as PNG (1000x1000 for Instagram quality)
size = 1000
img = Image.new('RGB', (size, size), color='#16213e')
draw = ImageDraw.Draw(img, 'RGBA')

center = size // 2

# Color palette
twilight = '#16213e'
blue = '#6CB4EE'
amber = '#F4C430'
lavender = '#B4A7D6'

# Draw concentric pulse rings - varying opacity and spacing
# Outer rings - lavender
pulse_rings = [
    (480, lavender, 1, 40),
    (460, lavender, 2, 50),
    (440, lavender, 1, 30),

    # Middle rings - blue
    (380, blue, 2, 60),
    (350, blue, 1, 45),
    (320, blue, 3, 55),
    (290, blue, 1, 40),

    # Inner accent - amber
    (240, amber, 2, 70),
    (210, amber, 1, 50),
    (180, amber, 2, 60),

    # Core rings - blue
    (140, blue, 1, 40),
    (110, blue, 2, 50),
    (80, blue, 1, 35),
]

# Draw all pulse rings
for radius, color, width, opacity in pulse_rings:
    # Convert hex to RGB
    r = int(color[1:3], 16)
    g = int(color[3:5], 16)
    b = int(color[5:7], 16)

    bbox = [center - radius, center - radius, center + radius, center + radius]
    draw.ellipse(bbox, outline=(r, g, b, opacity), width=width)

# Add dotted orbital paths
def draw_dotted_circle(draw, center_x, center_y, radius, color, dot_count=60, dot_size=2):
    """Draw a dotted circle"""
    r = int(color[1:3], 16)
    g = int(color[3:5], 16)
    b = int(color[5:7], 16)

    for i in range(dot_count):
        angle = (2 * math.pi * i) / dot_count
        x = center_x + radius * math.cos(angle)
        y = center_y + radius * math.sin(angle)
        draw.ellipse([x - dot_size, y - dot_size, x + dot_size, y + dot_size],
                     fill=(r, g, b, 80))

# Dotted orbital paths
draw_dotted_circle(draw, center, center, 410, lavender, 80, 1.5)
draw_dotted_circle(draw, center, center, 260, amber, 60, 1.5)
draw_dotted_circle(draw, center, center, 155, blue, 50, 1.5)

# Add radiating lines from center (very subtle)
def draw_radial_lines(draw, center_x, center_y, inner_r, outer_r, line_count=12):
    """Draw subtle radial lines"""
    for i in range(line_count):
        angle = (2 * math.pi * i) / line_count
        x1 = center_x + inner_r * math.cos(angle)
        y1 = center_y + inner_r * math.sin(angle)
        x2 = center_x + outer_r * math.cos(angle)
        y2 = center_y + outer_r * math.sin(angle)

        # Blue radial lines, very faint
        draw.line([(x1, y1), (x2, y2)], fill=(108, 180, 238, 25), width=1)

draw_radial_lines(draw, center, center, 50, 480, 24)

# Add central glow effect
for i in range(60, 0, -2):
    opacity = int(100 * (i / 60))
    draw.ellipse([center - i, center - i, center + i, center + i],
                 fill=(108, 180, 238, opacity))

# Add minimal typography - "LP" monogram in center
try:
    # Use Jura Light for elegant, thin letterforms
    font_size = 120
    font = ImageFont.truetype(f'{font_path}Jura-Light.ttf', font_size)

    # Draw "LP" monogram
    text = "LP"
    # Get text bounding box
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    x = center - text_width // 2
    y = center - text_height // 2 - 10  # Slight adjustment

    # Draw text in amber with slight glow
    draw.text((x, y), text, font=font, fill=(244, 196, 48, 255))

except Exception as e:
    print(f"Font loading issue: {e}")

# Save PNG logo
img.save('/sessions/stoic-epic-cerf/mnt/affirmations-project/luminous-pulse-logo.png', 'PNG', quality=100)

print("✓ Logo created: luminous-pulse-logo.png (1000x1000px)")
