#!/usr/bin/env python3
"""
Luminous Pulse Logo v2 - Enhanced Luminescence
Circular format, 1000x1000px
Emphasis on glowing, luminescent LP monogram
"""

from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math

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
pulse_rings = [
    (480, lavender, 1, 30),
    (460, lavender, 2, 40),
    (440, lavender, 1, 25),
    (380, blue, 2, 50),
    (350, blue, 1, 35),
    (320, blue, 3, 45),
    (290, blue, 1, 30),
    (240, amber, 2, 55),
    (210, amber, 1, 40),
    (180, amber, 2, 50),
    (140, blue, 1, 30),
    (110, blue, 2, 40),
    (80, blue, 1, 25),
]

# Draw all pulse rings
for radius, color, width, opacity in pulse_rings:
    r = int(color[1:3], 16)
    g = int(color[3:5], 16)
    b = int(color[5:7], 16)
    bbox = [center - radius, center - radius, center + radius, center + radius]
    draw.ellipse(bbox, outline=(r, g, b, opacity), width=width)

# Add dotted orbital paths
def draw_dotted_circle(draw, center_x, center_y, radius, color, dot_count=60, dot_size=2):
    r = int(color[1:3], 16)
    g = int(color[3:5], 16)
    b = int(color[5:7], 16)
    for i in range(dot_count):
        angle = (2 * math.pi * i) / dot_count
        x = center_x + radius * math.cos(angle)
        y = center_y + radius * math.sin(angle)
        draw.ellipse([x - dot_size, y - dot_size, x + dot_size, y + dot_size],
                     fill=(r, g, b, 70))

draw_dotted_circle(draw, center, center, 410, lavender, 80, 1.5)
draw_dotted_circle(draw, center, center, 260, amber, 60, 1.5)
draw_dotted_circle(draw, center, center, 155, blue, 50, 1.5)

# Add radial lines
def draw_radial_lines(draw, center_x, center_y, inner_r, outer_r, line_count=12):
    for i in range(line_count):
        angle = (2 * math.pi * i) / line_count
        x1 = center_x + inner_r * math.cos(angle)
        y1 = center_y + inner_r * math.sin(angle)
        x2 = center_x + outer_r * math.cos(angle)
        y2 = center_y + outer_r * math.sin(angle)
        draw.line([(x1, y1), (x2, y2)], fill=(108, 180, 238, 20), width=1)

draw_radial_lines(draw, center, center, 50, 480, 24)

# ENHANCED LUMINESCENT "LP" MONOGRAM
# Create a separate layer for the glowing text effect
glow_layer = Image.new('RGBA', (size, size), (0, 0, 0, 0))
glow_draw = ImageDraw.Draw(glow_layer, 'RGBA')

font_path = "/sessions/stoic-epic-cerf/mnt/.skills/skills/canvas-design/canvas-fonts/"

try:
    # Use Jura Light for elegant letterforms
    font_size = 140
    font = ImageFont.truetype(f'{font_path}Jura-Light.ttf', font_size)

    text = "LP"
    bbox = glow_draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    x = center - text_width // 2
    y = center - text_height // 2 - 15

    # Multiple glow layers for luminescence
    # Outer glow - blue
    for offset in range(20, 0, -2):
        opacity = int(80 * (offset / 20))
        glow_draw.text((x, y), text, font=font, fill=(108, 180, 238, opacity))

    # Middle glow - amber
    for offset in range(12, 0, -1):
        opacity = int(120 * (offset / 12))
        glow_draw.text((x, y), text, font=font, fill=(244, 196, 48, opacity))

    # Inner bright core - white-amber
    glow_draw.text((x, y), text, font=font, fill=(255, 255, 200, 255))

    # Apply gaussian blur for soft glow
    glow_layer = glow_layer.filter(ImageFilter.GaussianBlur(radius=3))

    # Composite the glow layer onto main image
    img.paste(glow_layer, (0, 0), glow_layer)

    # Draw the sharp text on top for definition
    main_draw = ImageDraw.Draw(img, 'RGBA')
    main_draw.text((x, y), text, font=font, fill=(255, 246, 210, 255))

except Exception as e:
    print(f"Font loading issue: {e}")

# Add subtle central energy field
energy_layer = Image.new('RGBA', (size, size), (0, 0, 0, 0))
energy_draw = ImageDraw.Draw(energy_layer, 'RGBA')

for i in range(70, 0, -3):
    opacity = int(60 * (i / 70))
    energy_draw.ellipse([center - i, center - i, center + i, center + i],
                        fill=(108, 180, 238, opacity))

energy_layer = energy_layer.filter(ImageFilter.GaussianBlur(radius=5))
img.paste(energy_layer, (0, 0), energy_layer)

# Save PNG logo
img.save('/sessions/stoic-epic-cerf/mnt/affirmations-project/luminous-pulse-logo.png', 'PNG', quality=100)

print("✓ Luminescent logo created: luminous-pulse-logo.png (1000x1000px)")
