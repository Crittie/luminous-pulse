#!/usr/bin/env python3
"""
Luminous Pulse — Canvas Expression (Refined)
AI-Optimism Affirmation Brand Art Object

A single-page composition expressing the tension between
signal and stillness, human presence and algorithmic fields.
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib.colors import Color
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import math
import os

# --- Configuration ---
OUTPUT_PATH = os.path.expanduser("~/luminous-pulse/business/luminous-pulse-canvas.pdf")
FONT_DIR = os.path.expanduser("~/.claude/skills/canvas-design/canvas-fonts")

# Palette — refined for depth and atmosphere
DEEP_GROUND = Color(0.055, 0.065, 0.115, 1)     # Richer, deeper twilight
MID_GROUND = Color(0.075, 0.09, 0.15, 1)        # Subtle vignette layer
FIELD_BLUE = Color(0.42, 0.71, 0.93, 1)         # #6CB4EE
SOFT_BLUE = Color(0.30, 0.52, 0.72, 1)          # Muted blue for secondary rings
AMBER_GLOW = Color(0.96, 0.77, 0.19, 1)         # #F4C430
WARM_AMBER = Color(0.98, 0.85, 0.45, 1)         # Lighter amber for inner glow
SPECTRAL_LAVENDER = Color(0.71, 0.65, 0.84, 1)  # #B4A7D6
FAINT_WHITE = Color(0.88, 0.90, 0.94, 1)        # Cooler near-white
GRID_COLOR = Color(0.14, 0.17, 0.26, 1)         # Grid line base

# Page
W, H = letter  # 612 x 792
# Pulse center — slightly above page center for visual balance
PCX, PCY = W / 2, H * 0.545


def register_fonts():
    fonts = {
        "Italiana": "Italiana-Regular.ttf",
        "DMMono": "DMMono-Regular.ttf",
        "Jura-Light": "Jura-Light.ttf",
        "InstrumentSerif": "InstrumentSerif-Regular.ttf",
        "InstrumentSerif-Italic": "InstrumentSerif-Italic.ttf",
        "PoiretOne": "PoiretOne-Regular.ttf",
        "GeistMono": "GeistMono-Regular.ttf",
    }
    for name, filename in fonts.items():
        path = os.path.join(FONT_DIR, filename)
        if os.path.exists(path):
            pdfmetrics.registerFont(TTFont(name, path))


def draw_ground(c):
    """Deep twilight with subtle radial vignette."""
    # Base
    c.setFillColor(DEEP_GROUND)
    c.rect(0, 0, W, H, fill=1, stroke=0)

    # Radial atmosphere — lighter glow near center
    for i in range(25):
        t = i / 25
        r = 320 * (1 - t)
        opacity = 0.025 * (1 - t) ** 1.5
        c.setFillColor(Color(0.15, 0.20, 0.35, opacity))
        c.circle(PCX, PCY, r, fill=1, stroke=0)


def draw_measurement_grid(c):
    """Sparse ruled lines — fainter, more deliberate."""
    c.saveState()

    # Horizontal — only every 48pt, very faint
    for y in range(0, int(H), 48):
        dist = abs(y - PCY) / (H / 2)
        opacity = 0.04 + 0.02 * (1 - dist)
        c.setStrokeColor(Color(0.18, 0.22, 0.34, opacity))
        c.setLineWidth(0.2)
        c.line(0, y, W, y)

    # Vertical — only every 96pt, extremely faint
    for x in range(0, int(W), 96):
        c.setStrokeColor(Color(0.18, 0.22, 0.34, 0.03))
        c.setLineWidth(0.15)
        c.line(x, 0, x, H)

    c.restoreState()


def draw_concentric_pulse(c, cx, cy, max_r, color, num_rings, line_w=0.4,
                          gap_seed=0, arc_min=200, arc_max=320,
                          min_r_threshold=18):
    """Radiating concentric arcs with organic breathing gaps.
    Cleared inner core for signal point luminance."""
    c.saveState()
    for i in range(num_rings):
        t = i / num_rings
        r = max_r * (t ** 0.65)
        # Larger inner clearance — lets the origin signal breathe
        if r < min_r_threshold:
            continue

        # Smooth opacity: peaks in mid-range, fades at edges
        mid_t = abs(t - 0.35) / 0.65  # Distance from sweet spot
        opacity = 0.38 * (1 - mid_t * 0.6) * (1 - t) ** 0.7

        ring_color = Color(color.red, color.green, color.blue, opacity)
        c.setStrokeColor(ring_color)
        c.setLineWidth(line_w * (1 - t * 0.55))

        # Varied arc segments — organic gaps
        start_angle = (i * 23 + gap_seed) % 360
        extent = arc_min + (arc_max - arc_min) * abs(math.sin(i * 0.4 + gap_seed * 0.1))
        c.arc(cx - r, cy - r, cx + r, cy + r, start_angle, extent)

        # Some rings get a second smaller arc — sparser than before
        if i % 4 == 0 and t > 0.35:
            opp_start = (start_angle + 180 + i * 7) % 360
            opp_extent = 25 + 35 * abs(math.cos(i * 0.7))
            c.setStrokeColor(Color(color.red, color.green, color.blue, opacity * 0.3))
            c.arc(cx - r, cy - r, cx + r, cy + r, opp_start, opp_extent)

    c.restoreState()


def draw_orbital_dots(c, cx, cy, radius, num_dots, color, dot_r=1.5,
                      phase_offset=0.0):
    """Dotted orbital path — constellation of presence."""
    c.saveState()
    for i in range(num_dots):
        angle = (2 * math.pi * i) / num_dots + phase_offset

        # Slight elliptical distortion — more organic
        ellipse_factor = 1.0 + 0.06 * math.sin(angle * 2 + 0.8)
        x = cx + radius * ellipse_factor * math.cos(angle)
        y = cy + radius * math.sin(angle)

        opacity = 0.12 + 0.40 * abs(math.sin(angle * 2.5 + phase_offset))
        c.setFillColor(Color(color.red, color.green, color.blue, opacity))

        size = dot_r * (0.6 + 0.5 * abs(math.cos(angle * 3.7 + phase_offset)))
        c.circle(x, y, size, fill=1, stroke=0)

    c.restoreState()


def draw_signal_point(c, x, y, r, color, glow_layers=18):
    """Luminous signal point — deeper atmospheric glow, pristine core."""
    c.saveState()
    # Wide atmospheric haze — more layers, wider spread
    for i in range(glow_layers):
        t = i / glow_layers
        glow_r = r * (1 + t * 8)
        opacity = 0.06 * (1 - t) ** 1.8
        c.setFillColor(Color(color.red, color.green, color.blue, opacity))
        c.circle(x, y, glow_r, fill=1, stroke=0)

    # Warm mid-glow ring
    c.setFillColor(Color(color.red, color.green, color.blue, 0.20))
    c.circle(x, y, r * 2.2, fill=1, stroke=0)

    # Core disc
    c.setFillColor(Color(color.red, color.green, color.blue, 0.90))
    c.circle(x, y, r, fill=1, stroke=0)

    # Hot center — warmer white
    c.setFillColor(Color(1, 0.97, 0.85, 0.75))
    c.circle(x, y, r * 0.45, fill=1, stroke=0)

    # White pinpoint
    c.setFillColor(Color(1, 1, 1, 0.60))
    c.circle(x, y, r * 0.15, fill=1, stroke=0)

    c.restoreState()


def draw_waveform_trace(c, x_start, y_center, length, amplitude, color,
                        freq=0.04, opacity=0.30, lw=0.45):
    """Fine waveform — frequency signature of presence."""
    c.saveState()
    c.setStrokeColor(Color(color.red, color.green, color.blue, opacity))
    c.setLineWidth(lw)

    path = c.beginPath()
    first = True
    steps = int(length / 1.2)
    for i in range(steps):
        t = i / steps
        x = x_start + t * length
        y = y_center + amplitude * (
            0.55 * math.sin(x * freq) +
            0.28 * math.sin(x * freq * 2.1 + 1.4) +
            0.12 * math.sin(x * freq * 4.7 + 0.5) +
            0.05 * math.sin(x * freq * 8.3 + 2.1)
        )
        envelope = math.sin(t * math.pi) ** 0.6
        y = y_center + (y - y_center) * envelope

        if first:
            path.moveTo(x, y)
            first = False
        else:
            path.lineTo(x, y)

    c.drawPath(path, fill=0, stroke=1)
    c.restoreState()


def draw_radial_lines(c, cx, cy, inner_r, outer_r, num_lines, color):
    """Selective radial rules — atmospheric, non-uniform, large breathing gaps."""
    c.saveState()
    for i in range(num_lines):
        angle = (2 * math.pi * i) / num_lines

        # Skip ~50% of lines for large breathing gaps
        skip1 = math.sin(angle * 3.2 + 0.7)
        skip2 = math.cos(angle * 1.9 + 2.1)
        if skip1 < -0.15 or skip2 < -0.4:
            continue

        # Variable length — some reach far, some are stubs
        variation = 0.35 + 0.65 * abs(math.sin(angle * 2.5 + 0.3))
        r_out = inner_r + (outer_r - inner_r) * variation

        x1 = cx + inner_r * math.cos(angle)
        y1 = cy + inner_r * math.sin(angle)
        x2 = cx + r_out * math.cos(angle)
        y2 = cy + r_out * math.sin(angle)

        opacity = 0.025 + 0.04 * abs(math.sin(angle * 1.8))
        c.setStrokeColor(Color(color.red, color.green, color.blue, opacity))
        c.setLineWidth(0.18)
        c.line(x1, y1, x2, y2)

    c.restoreState()


def draw_fine_tick_marks(c, cx, cy, radius, num_ticks, color):
    """Tick marks along a circle — barely perceptible calibration marks.
    Sparser, with intentional gaps so they don't form a visible circle."""
    c.saveState()
    for i in range(num_ticks):
        angle = (2 * math.pi * i) / num_ticks

        # Skip ~40% of ticks for organic distribution
        if math.sin(angle * 2.7 + 1.3) < 0.1:
            continue

        inner = radius - 1.5
        outer = radius + 1.5

        # Every 7th surviving tick is slightly longer
        if i % 7 == 0:
            inner = radius - 3
            outer = radius + 3

        x1 = cx + inner * math.cos(angle)
        y1 = cy + inner * math.sin(angle)
        x2 = cx + outer * math.cos(angle)
        y2 = cy + outer * math.sin(angle)

        opacity = 0.03 + 0.03 * abs(math.sin(angle * 3))
        c.setStrokeColor(Color(color.red, color.green, color.blue, opacity))
        c.setLineWidth(0.15)
        c.line(x1, y1, x2, y2)

    c.restoreState()


def draw_connecting_lines(c, signals, color):
    """Faint lines connecting signal points — constellation pattern."""
    c.saveState()
    connections = [(0, 1), (0, 2), (0, 5), (1, 3), (2, 4), (3, 5)]
    for a, b in connections:
        if a < len(signals) and b < len(signals):
            x1, y1, _ = signals[a]
            x2, y2, _ = signals[b]
            c.setStrokeColor(Color(color.red, color.green, color.blue, 0.04))
            c.setLineWidth(0.3)
            c.setDash([4, 8], 0)
            c.line(x1, y1, x2, y2)
    c.setDash([], 0)
    c.restoreState()


def draw_cross_hairs(c, cx, cy, size, color, opacity=0.10):
    """Fine crosshair — instrument reference marker."""
    c.saveState()
    c.setStrokeColor(Color(color.red, color.green, color.blue, opacity))
    c.setLineWidth(0.25)
    # Gapped crosshair — more refined
    gap = size * 0.3
    c.line(cx - size, cy, cx - gap, cy)
    c.line(cx + gap, cy, cx + size, cy)
    c.line(cx, cy - size, cx, cy - gap)
    c.line(cx, cy + gap, cx, cy + size)
    c.restoreState()


def draw_specimen_labels(c):
    """Clinical notation — fewer, more precisely placed."""
    c.saveState()
    c.setFont("DMMono", 5)

    # Left column — aligned to a single x position
    lx = 32
    labels_left = [
        (lx, H - 44, "FIELD 01", 0.14),
        (lx, H - 100, "f = 0.618", 0.10),
        (lx, PCY + 8, "ORIGIN", 0.12),
        (lx, 108, "SIGNAL", 0.10),
        (lx, 52, "OBS. 2026.02.10", 0.08),
    ]
    for x, y, text, opacity in labels_left:
        c.setFillColor(Color(FAINT_WHITE.red, FAINT_WHITE.green, FAINT_WHITE.blue, opacity))
        c.drawString(x, y, text)

    # Right column — right-aligned
    rx = W - 32
    labels_right = [
        (rx, H - 44, "PULSE 01", 0.14),
        (rx, H - 100, "λ = 440nm", 0.10),
        (rx, PCY + 8, "AMPLITUDE", 0.12),
        (rx, 108, "SPECTRUM", 0.10),
        (rx, 52, "DATUM", 0.08),
    ]
    for x, y, text, opacity in labels_right:
        c.setFillColor(Color(FAINT_WHITE.red, FAINT_WHITE.green, FAINT_WHITE.blue, opacity))
        tw = c.stringWidth(text, "DMMono", 5)
        c.drawString(x - tw, y, text)

    c.restoreState()


def draw_spaced_string(c, x_center, y, text, font, size, spacing):
    """Draw a string with custom letter spacing, centered at x_center."""
    c.setFont(font, size)
    # Calculate total width with spacing
    total_w = 0
    for ch in text:
        total_w += c.stringWidth(ch, font, size) + spacing
    total_w -= spacing  # No spacing after last char

    x = x_center - total_w / 2
    for ch in text:
        c.drawString(x, y, ch)
        x += c.stringWidth(ch, font, size) + spacing


def draw_anchor_phrase(c):
    """The singular anchoring text — inscribed with deliberate letter spacing."""
    c.saveState()

    phrase = "your humanity is your superpower"
    phrase_y = PCY - 230

    # Calculate approximate width for framing rules
    c.setFont("InstrumentSerif-Italic", 11)
    base_tw = c.stringWidth(phrase, "InstrumentSerif-Italic", 11)
    spaced_tw = base_tw + len(phrase) * 0.6  # Account for extra spacing
    rule_w = spaced_tw + 60

    # Framing rules — wider spacing, more delicate
    c.setStrokeColor(Color(FAINT_WHITE.red, FAINT_WHITE.green, FAINT_WHITE.blue, 0.05))
    c.setLineWidth(0.2)
    c.line(W / 2 - rule_w / 2, phrase_y + 20, W / 2 + rule_w / 2, phrase_y + 20)
    c.line(W / 2 - rule_w / 2, phrase_y - 10, W / 2 + rule_w / 2, phrase_y - 10)

    # Phrase — letter-spaced for inscribed quality
    c.setFillColor(Color(FAINT_WHITE.red, FAINT_WHITE.green, FAINT_WHITE.blue, 0.26))
    draw_spaced_string(c, W / 2, phrase_y, phrase,
                       "InstrumentSerif-Italic", 11, 0.6)

    # Classifier — more space below
    c.setFont("DMMono", 4.5)
    sub = "LUMINOUS PULSE  —  FIELD STUDY NO. 1"
    tw2 = c.stringWidth(sub, "DMMono", 4.5)
    c.setFillColor(Color(FAINT_WHITE.red, FAINT_WHITE.green, FAINT_WHITE.blue, 0.08))
    c.drawString(W / 2 - tw2 / 2, phrase_y - 24, sub)

    c.restoreState()


def draw_top_title(c):
    """Movement name — whispered at top."""
    c.saveState()
    c.setFont("Jura-Light", 6.5)
    title = "L U M I N O U S   P U L S E"
    tw = c.stringWidth(title, "Jura-Light", 6.5)
    c.setFillColor(Color(FAINT_WHITE.red, FAINT_WHITE.green, FAINT_WHITE.blue, 0.10))
    c.drawString(W / 2 - tw / 2, H - 38, title)
    c.restoreState()


def draw_frame(c):
    """Containment border with refined corner marks."""
    c.saveState()
    margin = 24

    # Main border — barely there
    c.setStrokeColor(Color(0.22, 0.25, 0.36, 0.10))
    c.setLineWidth(0.25)
    c.rect(margin, margin, W - 2 * margin, H - 2 * margin, fill=0, stroke=1)

    # Corner marks — amber accent
    mark_len = 12
    c.setStrokeColor(Color(AMBER_GLOW.red, AMBER_GLOW.green, AMBER_GLOW.blue, 0.22))
    c.setLineWidth(0.35)
    corners = [
        (margin, margin, 1, 1),
        (margin, H - margin, 1, -1),
        (W - margin, margin, -1, 1),
        (W - margin, H - margin, -1, -1),
    ]
    for cx, cy, dx, dy in corners:
        c.line(cx, cy, cx + mark_len * dx, cy)
        c.line(cx, cy, cx, cy + mark_len * dy)

    c.restoreState()


def main():
    c = canvas.Canvas(OUTPUT_PATH, pagesize=letter)
    register_fonts()

    # === LAYER 0: Ground with atmosphere ===
    draw_ground(c)

    # === LAYER 1: Measurement grid (sparser) ===
    draw_measurement_grid(c)

    # === LAYER 2: Radial lines — even sparser ===
    draw_radial_lines(c, PCX, PCY, 55, 275, 60, SOFT_BLUE)

    # === LAYER 3: Tick marks — ghostly calibration ===
    draw_fine_tick_marks(c, PCX, PCY, 210, 100, FAINT_WHITE)
    draw_fine_tick_marks(c, PCX, PCY, 140, 60, FAINT_WHITE)

    # === LAYER 4: Primary pulse — blue, wider inner clearance ===
    draw_concentric_pulse(c, PCX, PCY, 270, FIELD_BLUE, 28, line_w=0.42,
                          gap_seed=0, arc_min=210, arc_max=305,
                          min_r_threshold=28)

    # === LAYER 5: Secondary pulse — lavender, offset more for separation ===
    draw_concentric_pulse(c, PCX - 30, PCY + 25, 175, SPECTRAL_LAVENDER, 16,
                          line_w=0.28, gap_seed=55, arc_min=170, arc_max=260,
                          min_r_threshold=22)

    # === LAYER 6: Tertiary pulse — amber, intimate, clear center ===
    draw_concentric_pulse(c, PCX + 35, PCY - 15, 80, AMBER_GLOW, 10,
                          line_w=0.22, gap_seed=100, arc_min=140, arc_max=240,
                          min_r_threshold=20)

    # === LAYER 7: Orbital constellations ===
    draw_orbital_dots(c, PCX, PCY, 175, 80, FIELD_BLUE, dot_r=1.1, phase_offset=0)
    draw_orbital_dots(c, PCX, PCY, 120, 55, SPECTRAL_LAVENDER, dot_r=0.8, phase_offset=0.5)
    draw_orbital_dots(c, PCX, PCY, 240, 100, FAINT_WHITE, dot_r=0.6, phase_offset=1.0)

    # === LAYER 8: Signal points — warm presence nodes ===
    signals = [
        (PCX, PCY, 3.5),             # Origin
        (PCX - 80, PCY + 85, 2.3),   # Upper left
        (PCX + 105, PCY - 55, 2.0),  # Lower right
        (PCX + 48, PCY + 120, 1.7),  # Upper right
        (PCX - 125, PCY - 45, 1.4),  # Far left
        (PCX + 8, PCY - 115, 1.8),   # Below center
    ]

    # Constellation connections (before points, so they're underneath)
    draw_connecting_lines(c, signals, AMBER_GLOW)

    for sx, sy, sr in signals:
        draw_signal_point(c, sx, sy, sr, AMBER_GLOW)

    # === LAYER 9: Crosshairs at key nodes ===
    draw_cross_hairs(c, PCX, PCY, 14, FAINT_WHITE, 0.10)
    draw_cross_hairs(c, PCX - 80, PCY + 85, 9, FAINT_WHITE, 0.06)
    draw_cross_hairs(c, PCX + 105, PCY - 55, 9, FAINT_WHITE, 0.06)

    # === LAYER 10: Waveform traces — lower field ===
    wave_y = 118

    # Faint horizontal datum line — grounds the waveforms
    c.saveState()
    c.setStrokeColor(Color(FAINT_WHITE.red, FAINT_WHITE.green, FAINT_WHITE.blue, 0.04))
    c.setLineWidth(0.2)
    c.line(45, wave_y, W - 45, wave_y)
    c.restoreState()

    draw_waveform_trace(c, 50, wave_y, W - 100, 15, FIELD_BLUE,
                        freq=0.055, opacity=0.22, lw=0.38)
    draw_waveform_trace(c, 70, wave_y - 4, W - 140, 8, SPECTRAL_LAVENDER,
                        freq=0.085, opacity=0.13, lw=0.28)
    # Amber trace — whisper
    draw_waveform_trace(c, 90, wave_y + 2, W - 180, 4, AMBER_GLOW,
                        freq=0.12, opacity=0.08, lw=0.22)

    # === LAYER 11: Typography ===
    draw_top_title(c)
    draw_specimen_labels(c)
    draw_anchor_phrase(c)

    # === LAYER 12: Frame ===
    draw_frame(c)

    # === Finalize ===
    c.showPage()
    c.save()
    print(f"Canvas saved to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
