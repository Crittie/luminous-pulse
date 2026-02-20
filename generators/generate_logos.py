#!/usr/bin/env python3
"""
Luminous Pulse — Logo Options
3 distinct concepts, each interpreting human-AI connection.

Reference: Two hands reaching toward each other (Sistine Chapel meets AI),
burst of warm amber light at the point of contact, deep navy field.

Brand: Luminous Pulse | luminouspulse.co
Palette: Navy #1a2744, Blue #6CB4EE, Amber #F4C430, Lavender #B4A7D6
Font: Helvetica Neue Bold (using available alternatives)
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
DEEP_NAVY = Color(0.06, 0.08, 0.14, 1)
BLUE = Color(0.42, 0.71, 0.93, 1)
AMBER = Color(0.96, 0.77, 0.19, 1)
WARM_AMBER = Color(0.98, 0.88, 0.50, 1)
LAVENDER = Color(0.71, 0.65, 0.84, 1)
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
        "BigShoulders-Bold": "BigShoulders-Bold.ttf",
        "BigShoulders": "BigShoulders-Regular.ttf",
        "PoiretOne": "PoiretOne-Regular.ttf",
        "BricolageGrotesque-Bold": "BricolageGrotesque-Bold.ttf",
        "SmoochSans": "SmoochSans-Medium.ttf",
    }
    for name, filename in fonts.items():
        path = os.path.join(FONT_DIR, filename)
        if os.path.exists(path):
            pdfmetrics.registerFont(TTFont(name, path))


def draw_glow(c, x, y, r, color, layers=20, spread=5):
    """Atmospheric glow — warm luminous point."""
    for i in range(layers):
        t = i / layers
        gr = r * (1 + t * spread)
        opacity = 0.10 * (1 - t) ** 2.0
        c.setFillColor(Color(color.red, color.green, color.blue, opacity))
        c.circle(x, y, gr, fill=1, stroke=0)
    c.setFillColor(Color(color.red, color.green, color.blue, 0.9))
    c.circle(x, y, r, fill=1, stroke=0)
    c.setFillColor(Color(1, 1, 1, 0.5))
    c.circle(x, y, r * 0.3, fill=1, stroke=0)


def draw_particles(c, cx, cy, radius, count, color, seed=0):
    """Scattered particle field."""
    for i in range(count):
        angle = (2 * math.pi * i) / count + seed
        dist = radius * (0.3 + 0.7 * abs(math.sin(i * 1.7 + seed)))
        x = cx + dist * math.cos(angle)
        y = cy + dist * math.sin(angle)
        size = 0.4 + 0.8 * abs(math.cos(i * 2.3 + seed))
        opacity = 0.08 + 0.25 * abs(math.sin(i * 1.1 + seed))
        c.setFillColor(Color(color.red, color.green, color.blue, opacity))
        c.circle(x, y, size, fill=1, stroke=0)


# ============================================================
# LOGO 1: "The Spark" — Two reaching arcs meet at a point of light
# Minimalist, geometric. Two curved lines (one structured/digital,
# one organic/human) converging toward a single amber spark.
# ============================================================
def logo_1():
    W, H = 800, 800
    path = os.path.join(OUT_DIR, "logo-option-1-the-spark.pdf")
    c = canvas.Canvas(path, pagesize=(W, H))
    register_fonts()

    CX, CY = W / 2, H / 2

    # Background
    c.setFillColor(DEEP_NAVY)
    c.rect(0, 0, W, H, fill=1, stroke=0)

    # Subtle radial atmosphere
    for i in range(20):
        t = i / 20
        r = 350 * (1 - t)
        c.setFillColor(Color(0.12, 0.16, 0.28, 0.02 * (1 - t)))
        c.circle(CX, CY + 30, r, fill=1, stroke=0)

    # === THE MARK ===
    mark_cy = CY + 60  # Logo mark sits above center
    spark_x, spark_y = CX, mark_cy

    # Left arc — the "digital" reach (structured, geometric segments)
    c.saveState()
    num_segs = 8
    for i in range(num_segs):
        t = i / num_segs
        r = 45 + t * 95
        start = 30 + t * 15
        extent = 55 - t * 15
        opacity = 0.15 + 0.25 * (1 - t)
        c.setStrokeColor(Color(BLUE.red, BLUE.green, BLUE.blue, opacity))
        c.setLineWidth(1.8 - t * 0.8)
        # Arcs approaching from left
        arc_cx = spark_x - 15
        arc_cy = spark_y + 5
        c.arc(arc_cx - r, arc_cy - r, arc_cx + r, arc_cy + r,
              140 + i * 5, extent)
    c.restoreState()

    # Right arc — the "human" reach (organic, flowing curve)
    c.saveState()
    for i in range(num_segs):
        t = i / num_segs
        r = 40 + t * 100
        opacity = 0.12 + 0.22 * (1 - t)
        c.setStrokeColor(Color(LAVENDER.red, LAVENDER.green, LAVENDER.blue, opacity))
        c.setLineWidth(1.6 - t * 0.6)
        arc_cx = spark_x + 15
        arc_cy = spark_y - 5
        c.arc(arc_cx - r, arc_cy - r, arc_cx + r, arc_cy + r,
              320 + i * 4, 50 - t * 10)
    c.restoreState()

    # Concentric pulse rings around the spark — very faint
    c.saveState()
    for i in range(6):
        t = i / 6
        r = 12 + t * 55
        opacity = 0.08 * (1 - t)
        c.setStrokeColor(Color(AMBER.red, AMBER.green, AMBER.blue, opacity))
        c.setLineWidth(0.4)
        c.circle(spark_x, spark_y, r, fill=0, stroke=1)
    c.restoreState()

    # Fine particle scatter around spark
    draw_particles(c, spark_x, spark_y, 80, 40, BLUE, seed=0.3)
    draw_particles(c, spark_x, spark_y, 60, 25, LAVENDER, seed=1.5)

    # THE SPARK — amber point of connection
    draw_glow(c, spark_x, spark_y, 5, AMBER, layers=25, spread=7)

    # Small secondary sparks
    secondaries = [
        (spark_x - 22, spark_y + 14, 1.5),
        (spark_x + 18, spark_y - 12, 1.2),
        (spark_x - 8, spark_y - 20, 1.0),
        (spark_x + 25, spark_y + 8, 0.8),
    ]
    for sx, sy, sr in secondaries:
        draw_glow(c, sx, sy, sr, AMBER, layers=10, spread=4)

    # === WORDMARK ===
    # "LUMINOUS" — bold
    c.setFillColor(Color(WHITE.red, WHITE.green, WHITE.blue, 0.92))
    c.setFont("InstrumentSans-Bold", 38)
    w1 = c.stringWidth("LUMINOUS", "InstrumentSans-Bold", 38)
    # "PULSE" — lighter weight
    c.setFont("InstrumentSans", 38)
    w2 = c.stringWidth("PULSE", "InstrumentSans", 38)
    gap = 12
    total = w1 + gap + w2
    x_start = CX - total / 2
    text_y = CY - 95

    c.setFillColor(Color(WHITE.red, WHITE.green, WHITE.blue, 0.92))
    c.setFont("InstrumentSans-Bold", 38)
    c.drawString(x_start, text_y, "LUMINOUS")
    c.setFillColor(Color(AMBER.red, AMBER.green, AMBER.blue, 0.85))
    c.setFont("InstrumentSans", 38)
    c.drawString(x_start + w1 + gap, text_y, "PULSE")

    # Tagline
    c.setFillColor(Color(FAINT.red, FAINT.green, FAINT.blue, 0.35))
    c.setFont("Jura-Light", 11)
    tag = "your humanity is your superpower"
    tw = c.stringWidth(tag, "Jura-Light", 11)
    c.drawString(CX - tw / 2, text_y - 30, tag)

    # Label
    c.setFillColor(Color(FAINT.red, FAINT.green, FAINT.blue, 0.15))
    c.setFont("DMMono", 7)
    c.drawString(CX - 40, 35, "OPTION 1 — THE SPARK")

    c.showPage()
    c.save()
    print(f"Logo 1 saved: {path}")


# ============================================================
# LOGO 2: "The Pulse" — Concentric emanation from a warm center
# The amber core radiates outward through blue/lavender rings.
# Abstract, icon-forward. The "LP" monogram hidden in negative space.
# ============================================================
def logo_2():
    W, H = 800, 800
    path = os.path.join(OUT_DIR, "logo-option-2-the-pulse.pdf")
    c = canvas.Canvas(path, pagesize=(W, H))
    register_fonts()

    CX, CY = W / 2, H / 2

    # Background
    c.setFillColor(DEEP_NAVY)
    c.rect(0, 0, W, H, fill=1, stroke=0)

    # Atmosphere
    for i in range(15):
        t = i / 15
        r = 320 * (1 - t)
        c.setFillColor(Color(0.12, 0.16, 0.28, 0.02 * (1 - t)))
        c.circle(CX, CY + 50, r, fill=1, stroke=0)

    # === THE MARK ===
    mark_cy = CY + 55

    # Concentric arcs — blue outer system
    c.saveState()
    for i in range(12):
        t = i / 12
        r = 35 + t * 115
        opacity = 0.35 * (1 - t) ** 0.8
        c.setStrokeColor(Color(BLUE.red, BLUE.green, BLUE.blue, opacity))
        c.setLineWidth(2.2 * (1 - t * 0.5))

        # Each arc has a gap — creating a "pulse" effect
        start = (i * 31) % 360
        extent = 220 + 80 * math.sin(i * 0.6)
        c.arc(CX - r, mark_cy - r, CX + r, mark_cy + r, start, extent)
    c.restoreState()

    # Inner lavender arcs — secondary pulse
    c.saveState()
    for i in range(7):
        t = i / 7
        r = 25 + t * 65
        opacity = 0.22 * (1 - t) ** 0.7
        c.setStrokeColor(Color(LAVENDER.red, LAVENDER.green, LAVENDER.blue, opacity))
        c.setLineWidth(1.5 * (1 - t * 0.4))
        start = (i * 47 + 90) % 360
        extent = 160 + 60 * math.cos(i * 0.8)
        c.arc(CX - r, mark_cy - r, CX + r, mark_cy + r, start, extent)
    c.restoreState()

    # Orbital dots at key radii
    for radius, count, dot_r, col in [
        (100, 50, 1.0, BLUE),
        (65, 30, 0.7, LAVENDER),
        (140, 70, 0.6, FAINT),
    ]:
        for i in range(count):
            angle = (2 * math.pi * i) / count
            x = CX + radius * math.cos(angle)
            y = mark_cy + radius * math.sin(angle)
            opacity = 0.10 + 0.30 * abs(math.sin(angle * 2.5))
            c.setFillColor(Color(col.red, col.green, col.blue, opacity))
            size = dot_r * (0.5 + 0.5 * abs(math.cos(angle * 3.1)))
            c.circle(x, y, size, fill=1, stroke=0)

    # Center glow — the warm human core
    draw_glow(c, CX, mark_cy, 7, AMBER, layers=30, spread=5)

    # Four cardinal micro-sparks
    for angle in [0, math.pi / 2, math.pi, 3 * math.pi / 2]:
        sx = CX + 18 * math.cos(angle + 0.3)
        sy = mark_cy + 18 * math.sin(angle + 0.3)
        draw_glow(c, sx, sy, 1.5, AMBER, layers=8, spread=3)

    # === WORDMARK ===
    text_y = CY - 100

    # Stacked layout
    c.setFillColor(Color(WHITE.red, WHITE.green, WHITE.blue, 0.92))
    c.setFont("WorkSans-Bold", 44)
    w_l = c.stringWidth("LUMINOUS", "WorkSans-Bold", 44)
    c.drawString(CX - w_l / 2, text_y, "LUMINOUS")

    c.setFillColor(Color(AMBER.red, AMBER.green, AMBER.blue, 0.80))
    c.setFont("WorkSans", 44)
    w_p = c.stringWidth("PULSE", "WorkSans", 44)
    c.drawString(CX - w_p / 2, text_y - 48, "PULSE")

    # Tagline
    c.setFillColor(Color(FAINT.red, FAINT.green, FAINT.blue, 0.30))
    c.setFont("Jura-Light", 10.5)
    tag = "your humanity is your superpower"
    tw = c.stringWidth(tag, "Jura-Light", 10.5)
    c.drawString(CX - tw / 2, text_y - 85, tag)

    # Thin rule separating mark from text
    c.setStrokeColor(Color(AMBER.red, AMBER.green, AMBER.blue, 0.10))
    c.setLineWidth(0.3)
    c.line(CX - 60, text_y + 25, CX + 60, text_y + 25)

    # Label
    c.setFillColor(Color(FAINT.red, FAINT.green, FAINT.blue, 0.15))
    c.setFont("DMMono", 7)
    c.drawString(CX - 40, 35, "OPTION 2 — THE PULSE")

    c.showPage()
    c.save()
    print(f"Logo 2 saved: {path}")


# ============================================================
# LOGO 3: "The Touch" — Direct reference to the hands concept.
# Two abstract fingertip forms (one geometric/blue, one organic/lavender)
# nearly touching, with amber light blooming at the gap.
# Rendered as elegant line art, not literal illustration.
# ============================================================
def logo_3():
    W, H = 800, 800
    path = os.path.join(OUT_DIR, "logo-option-3-the-touch.pdf")
    c = canvas.Canvas(path, pagesize=(W, H))
    register_fonts()

    CX, CY = W / 2, H / 2

    # Background
    c.setFillColor(DEEP_NAVY)
    c.rect(0, 0, W, H, fill=1, stroke=0)

    # Atmosphere
    for i in range(15):
        t = i / 15
        r = 300 * (1 - t)
        c.setFillColor(Color(0.12, 0.16, 0.28, 0.015 * (1 - t)))
        c.circle(CX, CY + 50, r, fill=1, stroke=0)

    # === THE MARK ===
    mark_cy = CY + 55
    gap_x = CX  # Where the fingers almost meet
    gap_y = mark_cy

    # LEFT FORM — "digital" fingertip approaching from left
    # Constructed from geometric segments and data-point dots
    c.saveState()

    # Main finger form — three tapered lines converging to a point
    tip_x = gap_x - 8
    tip_y = gap_y

    lines_left = [
        # (start_x_offset, start_y_offset, curvature)
        (-120, 35, 0.4),
        (-130, 0, 0.2),
        (-115, -30, 0.5),
    ]

    for dx, dy, curve in lines_left:
        sx = tip_x + dx
        sy = tip_y + dy
        path_obj = c.beginPath()
        steps = 40
        for i in range(steps + 1):
            t = i / steps
            # Ease-in curve toward the tip
            ease_t = t ** 1.5
            x = sx + (tip_x - sx) * ease_t
            y = sy + (tip_y - sy) * ease_t
            # Add slight curve
            y += curve * 20 * math.sin(t * math.pi)

            if i == 0:
                path_obj.moveTo(x, y)
            else:
                path_obj.lineTo(x, y)

        # Opacity tapers: stronger near tip
        c.setStrokeColor(Color(BLUE.red, BLUE.green, BLUE.blue, 0.40))
        c.setLineWidth(1.2)
        c.drawPath(path_obj, fill=0, stroke=1)

    # Digital particles along the left form
    for i in range(25):
        t = i / 25
        px = tip_x - 120 * (1 - t ** 1.3)
        py = tip_y + 40 * math.sin(t * 3 + i * 0.5) * (1 - t)
        size = 0.5 + 1.0 * (1 - t)
        opacity = 0.08 + 0.18 * t
        c.setFillColor(Color(BLUE.red, BLUE.green, BLUE.blue, opacity))
        c.circle(px, py, size, fill=1, stroke=0)

    # Small geometric marks (data/circuit feel)
    for i in range(6):
        t = i / 6
        mx = tip_x - 100 * (1 - t) - 10
        my = tip_y + 15 * math.sin(i * 1.2)
        c.setStrokeColor(Color(BLUE.red, BLUE.green, BLUE.blue, 0.12))
        c.setLineWidth(0.4)
        size = 3 + 2 * t
        c.rect(mx - size / 2, my - size / 2, size, size, fill=0, stroke=1)

    c.restoreState()

    # RIGHT FORM — "human" fingertip approaching from right
    # Organic, flowing curves
    c.saveState()

    tip_rx = gap_x + 8
    tip_ry = gap_y

    lines_right = [
        (125, 30, -0.5),
        (135, -2, -0.15),
        (120, -28, -0.6),
    ]

    for dx, dy, curve in lines_right:
        sx = tip_rx + dx
        sy = tip_ry + dy
        path_obj = c.beginPath()
        steps = 40
        for i in range(steps + 1):
            t = i / steps
            ease_t = t ** 1.5
            x = sx + (tip_rx - sx) * ease_t
            y = sy + (tip_ry - sy) * ease_t
            y += curve * 22 * math.sin(t * math.pi)

            if i == 0:
                path_obj.moveTo(x, y)
            else:
                path_obj.lineTo(x, y)

        c.setStrokeColor(Color(LAVENDER.red, LAVENDER.green, LAVENDER.blue, 0.35))
        c.setLineWidth(1.2)
        c.drawPath(path_obj, fill=0, stroke=1)

    # Organic particles along the right form
    for i in range(20):
        t = i / 20
        px = tip_rx + 120 * (1 - t ** 1.3)
        py = tip_ry + 35 * math.sin(t * 2.5 + i * 0.7) * (1 - t)
        size = 0.6 + 0.9 * (1 - t)
        opacity = 0.06 + 0.15 * t
        c.setFillColor(Color(LAVENDER.red, LAVENDER.green, LAVENDER.blue, opacity))
        c.circle(px, py, size, fill=1, stroke=0)

    # Organic marks (small circles, not squares)
    for i in range(5):
        t = i / 5
        mx = tip_rx + 95 * (1 - t) + 10
        my = tip_ry + 12 * math.sin(i * 1.5)
        c.setStrokeColor(Color(LAVENDER.red, LAVENDER.green, LAVENDER.blue, 0.10))
        c.setLineWidth(0.4)
        c.circle(mx, my, 2.5 + 1.5 * t, fill=0, stroke=1)

    c.restoreState()

    # THE GAP — amber light blooming between the two forms
    # This is the heart of the logo
    draw_glow(c, gap_x, gap_y, 4.5, AMBER, layers=28, spread=8)

    # Tiny amber sparks radiating from the gap
    for i in range(12):
        angle = (2 * math.pi * i) / 12 + 0.2
        dist = 12 + 10 * abs(math.sin(i * 1.7))
        sx = gap_x + dist * math.cos(angle)
        sy = gap_y + dist * math.sin(angle)
        sr = 0.6 + 0.5 * abs(math.cos(i * 2.3))
        draw_glow(c, sx, sy, sr, AMBER, layers=6, spread=3)

    # Faint concentric rings around the gap
    for i in range(4):
        t = i / 4
        r = 20 + t * 40
        c.setStrokeColor(Color(AMBER.red, AMBER.green, AMBER.blue, 0.06 * (1 - t)))
        c.setLineWidth(0.3)
        c.circle(gap_x, gap_y, r, fill=0, stroke=1)

    # === WORDMARK ===
    text_y = CY - 100

    # Side by side — "LUMINOUS PULSE"
    c.setFont("BricolageGrotesque-Bold", 40)
    w_l = c.stringWidth("LUMINOUS", "BricolageGrotesque-Bold", 40)
    c.setFont("Jura-Medium", 40)
    w_p = c.stringWidth("PULSE", "Jura-Medium", 40)
    gap_w = 14
    total = w_l + gap_w + w_p
    x_start = CX - total / 2

    c.setFillColor(Color(WHITE.red, WHITE.green, WHITE.blue, 0.92))
    c.setFont("BricolageGrotesque-Bold", 40)
    c.drawString(x_start, text_y, "LUMINOUS")

    c.setFillColor(Color(AMBER.red, AMBER.green, AMBER.blue, 0.80))
    c.setFont("Jura-Medium", 40)
    c.drawString(x_start + w_l + gap_w, text_y, "PULSE")

    # Tagline
    c.setFillColor(Color(FAINT.red, FAINT.green, FAINT.blue, 0.30))
    c.setFont("Jura-Light", 10.5)
    tag = "your humanity is your superpower"
    tw = c.stringWidth(tag, "Jura-Light", 10.5)
    c.drawString(CX - tw / 2, text_y - 32, tag)

    # Label
    c.setFillColor(Color(FAINT.red, FAINT.green, FAINT.blue, 0.15))
    c.setFont("DMMono", 7)
    c.drawString(CX - 40, 35, "OPTION 3 — THE TOUCH")

    c.showPage()
    c.save()
    print(f"Logo 3 saved: {path}")


if __name__ == "__main__":
    register_fonts()
    logo_1()
    logo_2()
    logo_3()
