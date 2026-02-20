#!/usr/bin/env python3
"""
Luminous Pulse — Final Logo: "The Touch" (Refined)
Three formats: Square (IG profile), Horizontal (website), Icon-only (favicon/watermark)
"""

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.colors import Color
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import math
import os

FONT_DIR = os.path.expanduser("~/.claude/skills/canvas-design/canvas-fonts")
OUT_DIR = os.path.expanduser("~/luminous-pulse/assets/logos")

# Palette
NAVY = Color(0.10, 0.15, 0.27, 1)
DEEP_NAVY = Color(0.055, 0.068, 0.13, 1)
BLUE = Color(0.42, 0.71, 0.93, 1)
BRIGHT_BLUE = Color(0.50, 0.78, 0.98, 1)
AMBER = Color(0.96, 0.77, 0.19, 1)
WARM_AMBER = Color(0.98, 0.88, 0.50, 1)
LAVENDER = Color(0.71, 0.65, 0.84, 1)
BRIGHT_LAV = Color(0.78, 0.72, 0.90, 1)
WHITE = Color(0.95, 0.96, 0.98, 1)
FAINT = Color(0.80, 0.83, 0.90, 1)


def register_fonts():
    fonts = {
        "Outfit-Bold": "Outfit-Bold.ttf",
        "Outfit": "Outfit-Regular.ttf",
        "WorkSans-Bold": "WorkSans-Bold.ttf",
        "WorkSans": "WorkSans-Regular.ttf",
        "Jura-Light": "Jura-Light.ttf",
        "Jura-Medium": "Jura-Medium.ttf",
        "DMMono": "DMMono-Regular.ttf",
        "InstrumentSans-Bold": "InstrumentSans-Bold.ttf",
        "InstrumentSans": "InstrumentSans-Regular.ttf",
        "BricolageGrotesque-Bold": "BricolageGrotesque-Bold.ttf",
        "BricolageGrotesque": "BricolageGrotesque-Regular.ttf",
    }
    for name, filename in fonts.items():
        path = os.path.join(FONT_DIR, filename)
        if os.path.exists(path):
            pdfmetrics.registerFont(TTFont(name, path))


def draw_glow(c, x, y, r, color, layers=20, spread=5):
    """Atmospheric glow point."""
    for i in range(layers):
        t = i / layers
        gr = r * (1 + t * spread)
        opacity = 0.09 * (1 - t) ** 1.8
        c.setFillColor(Color(color.red, color.green, color.blue, opacity))
        c.circle(x, y, gr, fill=1, stroke=0)
    # Warm mid-ring
    c.setFillColor(Color(color.red, color.green, color.blue, 0.25))
    c.circle(x, y, r * 2.0, fill=1, stroke=0)
    # Core
    c.setFillColor(Color(color.red, color.green, color.blue, 0.92))
    c.circle(x, y, r, fill=1, stroke=0)
    # Hot center
    c.setFillColor(Color(1, 0.97, 0.85, 0.75))
    c.circle(x, y, r * 0.4, fill=1, stroke=0)
    # White pinpoint
    c.setFillColor(Color(1, 1, 1, 0.55))
    c.circle(x, y, r * 0.15, fill=1, stroke=0)


def draw_touch_mark(c, cx, cy, scale=1.0):
    """
    The Touch mark — two sets of converging lines with amber spark.
    scale=1.0 for full logo, smaller for icon.
    """
    s = scale
    gap_x, gap_y = cx, cy

    # ─── LEFT SIDE: DIGITAL (Blue) ───
    # 5 lines for richer visual weight, each with gradient opacity
    tip_x = gap_x - 10 * s
    tip_y = gap_y

    lines_left = [
        # (x_offset, y_offset, curvature, base_opacity, line_width)
        (-180 * s, 55 * s,   0.30,  0.55, 2.0 * s),   # outermost
        (-190 * s, 28 * s,   0.18,  0.50, 1.8 * s),
        (-195 * s, 0,        0.08,  0.60, 2.2 * s),   # center — strongest
        (-190 * s, -25 * s, -0.15,  0.50, 1.8 * s),
        (-175 * s, -50 * s, -0.28,  0.45, 1.6 * s),   # outermost
    ]

    c.saveState()
    for dx, dy, curve, base_op, lw in lines_left:
        sx = tip_x + dx
        sy = tip_y + dy
        path_obj = c.beginPath()
        steps = 60
        for i in range(steps + 1):
            t = i / steps
            ease_t = t ** 1.6
            x = sx + (tip_x - sx) * ease_t
            y = sy + (tip_y - sy) * ease_t
            y += curve * 30 * s * math.sin(t * math.pi)

            if i == 0:
                path_obj.moveTo(x, y)
            else:
                path_obj.lineTo(x, y)

        # Opacity gradient: faint at origin, strong near tip
        c.setStrokeColor(Color(BLUE.red, BLUE.green, BLUE.blue, base_op))
        c.setLineWidth(lw)
        c.drawPath(path_obj, fill=0, stroke=1)

    # Digital particles — structured, grid-like scatter
    for i in range(35):
        t = i / 35
        px = tip_x - 180 * s * (1 - t ** 1.2)
        py = tip_y + 55 * s * math.sin(t * 3.5 + i * 0.4) * (1 - t)
        size = (0.6 + 1.2 * (1 - t)) * s
        opacity = 0.06 + 0.20 * t
        c.setFillColor(Color(BLUE.red, BLUE.green, BLUE.blue, opacity))
        c.circle(px, py, size, fill=1, stroke=0)

    # Geometric accent marks — small squares near the lines' origins
    for i in range(8):
        t = i / 8
        mx = tip_x - 170 * s * (1 - t * 0.3) + (i % 3) * 8 * s
        my = tip_y + 45 * s * math.sin(i * 0.9) * (1 - t * 0.5)
        c.setStrokeColor(Color(BLUE.red, BLUE.green, BLUE.blue, 0.10 + 0.05 * t))
        c.setLineWidth(0.35 * s)
        sz = (2.5 + 2 * t) * s
        c.rect(mx - sz / 2, my - sz / 2, sz, sz, fill=0, stroke=1)
    c.restoreState()

    # ─── RIGHT SIDE: HUMAN (Lavender) ───
    tip_rx = gap_x + 10 * s
    tip_ry = gap_y

    lines_right = [
        (185 * s, 50 * s,  -0.35,  0.48, 1.8 * s),
        (195 * s, 24 * s,  -0.14,  0.45, 1.7 * s),
        (200 * s, -2,      -0.05,  0.52, 2.0 * s),  # center — strongest
        (195 * s, -22 * s,  0.12,  0.45, 1.7 * s),
        (180 * s, -48 * s,  0.32,  0.42, 1.5 * s),
    ]

    c.saveState()
    for dx, dy, curve, base_op, lw in lines_right:
        sx = tip_rx + dx
        sy = tip_ry + dy
        path_obj = c.beginPath()
        steps = 60
        for i in range(steps + 1):
            t = i / steps
            ease_t = t ** 1.6
            x = sx + (tip_rx - sx) * ease_t
            y = sy + (tip_ry - sy) * ease_t
            y += curve * 30 * s * math.sin(t * math.pi)

            if i == 0:
                path_obj.moveTo(x, y)
            else:
                path_obj.lineTo(x, y)

        c.setStrokeColor(Color(LAVENDER.red, LAVENDER.green, LAVENDER.blue, base_op))
        c.setLineWidth(lw)
        c.drawPath(path_obj, fill=0, stroke=1)

    # Organic particles — softer, more scattered
    for i in range(28):
        t = i / 28
        px = tip_rx + 180 * s * (1 - t ** 1.2)
        py = tip_ry + 50 * s * math.sin(t * 2.8 + i * 0.6) * (1 - t)
        size = (0.5 + 1.0 * (1 - t)) * s
        opacity = 0.05 + 0.16 * t
        c.setFillColor(Color(LAVENDER.red, LAVENDER.green, LAVENDER.blue, opacity))
        c.circle(px, py, size, fill=1, stroke=0)

    # Organic accent marks — small circles (vs squares on digital side)
    for i in range(7):
        t = i / 7
        mx = tip_rx + 165 * s * (1 - t * 0.3) - (i % 3) * 7 * s
        my = tip_ry + 40 * s * math.sin(i * 1.1) * (1 - t * 0.5)
        c.setStrokeColor(Color(LAVENDER.red, LAVENDER.green, LAVENDER.blue, 0.08 + 0.04 * t))
        c.setLineWidth(0.35 * s)
        c.circle(mx, my, (2 + 2 * t) * s, fill=0, stroke=1)
    c.restoreState()

    # ─── THE SPARK — Amber bloom at the point of contact ───
    draw_glow(c, gap_x, gap_y, 6 * s, AMBER, layers=30, spread=7)

    # Radiating micro-sparks
    for i in range(16):
        angle = (2 * math.pi * i) / 16 + 0.15
        dist = (14 + 12 * abs(math.sin(i * 1.7))) * s
        sx = gap_x + dist * math.cos(angle)
        sy = gap_y + dist * math.sin(angle)
        sr = (0.5 + 0.6 * abs(math.cos(i * 2.3))) * s
        draw_glow(c, sx, sy, sr, AMBER, layers=8, spread=3)

    # Faint pulse rings from the spark
    for i in range(5):
        t = i / 5
        r = (22 + t * 50) * s
        c.setStrokeColor(Color(AMBER.red, AMBER.green, AMBER.blue, 0.07 * (1 - t)))
        c.setLineWidth(0.3 * s)
        start = (i * 40) % 360
        extent = 200 + 100 * math.sin(i * 1.2)
        c.arc(gap_x - r, gap_y - r, gap_x + r, gap_y + r, start, extent)


def draw_background(c, W, H, focus_x, focus_y):
    """Deep navy with atmospheric glow."""
    c.setFillColor(DEEP_NAVY)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    for i in range(20):
        t = i / 20
        r = 350 * (1 - t)
        c.setFillColor(Color(0.10, 0.14, 0.26, 0.018 * (1 - t)))
        c.circle(focus_x, focus_y, r, fill=1, stroke=0)


# Gradient colors (matches CSS: #6CB4EE -> #F4C430)
GRAD_BLUE = Color(0.424, 0.706, 0.933, 1)   # #6CB4EE
GRAD_AMBER = Color(0.957, 0.769, 0.188, 1)  # #F4C430


def draw_gradient_text(c, text, x, y, font, size, opacity=0.9):
    """Draw text with per-character blue-to-amber gradient, matching the CSS."""
    c.setFont(font, size)
    total_w = c.stringWidth(text, font, size)
    cx = x
    for i, ch in enumerate(text):
        if ch == " ":
            cx += c.stringWidth(" ", font, size)
            continue
        # t goes 0->1 across the full string
        t = cx / (x + total_w) if total_w > 0 else 0
        # Normalize t to 0-1 range relative to start
        t = (cx - x) / total_w if total_w > 0 else 0
        r = GRAD_BLUE.red + (GRAD_AMBER.red - GRAD_BLUE.red) * t
        g = GRAD_BLUE.green + (GRAD_AMBER.green - GRAD_BLUE.green) * t
        b = GRAD_BLUE.blue + (GRAD_AMBER.blue - GRAD_BLUE.blue) * t
        c.setFillColor(Color(r, g, b, opacity))
        c.drawString(cx, y, ch)
        cx += c.stringWidth(ch, font, size)


# ============================================================
# FORMAT 1: Square (1080x1080 scaled to 800x800 PDF)
# For Instagram profile pic, social media
# ============================================================
def logo_square():
    W, H = 800, 800
    path = os.path.join(OUT_DIR, "logo-final-square.pdf")
    c = canvas.Canvas(path, pagesize=(W, H))
    register_fonts()
    CX, CY = W / 2, H / 2

    draw_background(c, W, H, CX, CY + 40)

    # Mark — centered, upper half
    draw_touch_mark(c, CX, CY + 60, scale=1.15)

    # Wordmark — directly below mark, tight
    text_y = CY - 100
    font = "Helvetica"
    size = 56

    c.setFont(font, size)
    full_text = "luminous pulse"
    total_w = c.stringWidth(full_text, font, size)
    x_start = CX - total_w / 2

    draw_gradient_text(c, full_text, x_start, text_y, font, size, opacity=0.9)

    c.showPage()
    c.save()
    print(f"Square logo saved: {path}")


# ============================================================
# FORMAT 2: Horizontal (1200x400 for website header / banner)
# ============================================================
def logo_horizontal():
    W, H = 1200, 420
    path = os.path.join(OUT_DIR, "logo-final-horizontal.pdf")
    c = canvas.Canvas(path, pagesize=(W, H))
    register_fonts()
    CY = H / 2

    draw_background(c, W, H, 340, CY)

    # Mark — left side
    mark_cx = 340
    draw_touch_mark(c, mark_cx, CY, scale=0.78)

    # Wordmark — right of mark, lowercase, Helvetica with gradient
    font = "Helvetica"
    size = 50
    text_x = 560
    text_y = CY - 16

    draw_gradient_text(c, "luminous pulse", text_x, text_y, font, size, opacity=0.9)

    c.showPage()
    c.save()
    print(f"Horizontal logo saved: {path}")


# ============================================================
# FORMAT 3: Icon only (square, no text — for favicon, watermark, app icon)
# ============================================================
def logo_icon():
    W, H = 500, 500
    path = os.path.join(OUT_DIR, "logo-final-icon.pdf")
    c = canvas.Canvas(path, pagesize=(W, H))
    register_fonts()
    CX, CY = W / 2, H / 2

    draw_background(c, W, H, CX, CY)

    # Mark only — centered, slightly larger for icon presence
    draw_touch_mark(c, CX, CY, scale=0.95)

    c.showPage()
    c.save()
    print(f"Icon logo saved: {path}")


if __name__ == "__main__":
    register_fonts()
    logo_square()
    logo_horizontal()
    logo_icon()
