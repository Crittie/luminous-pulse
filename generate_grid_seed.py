#!/usr/bin/env python3
"""Generate 9 grid-seed quote cards for Luminous Pulse IG launch.

Uses 6 layout styles from the IG visual research:
  The Anchor, The Spotlight Word, The Breath,
  The Frame, The Split, The Diagonal

Output: instagram/grid-seed/  — 9 PNGs at 1080x1350 (4:5 portrait)
"""

import math
import os
import random

from PIL import Image, ImageDraw, ImageFont, ImageFilter

# ── Brand palette ─────────────────────────────────────────────
NAVY = (26, 26, 46)           # #1a1a2e
NAVY_LIGHT = (34, 40, 62)     # slightly lighter for gradients
OFF_WHITE = (245, 240, 235)   # #F5F0EB — warm, not stark
AMBER = (244, 196, 48)        # #F4C430
BLUE = (108, 180, 238)        # #6CB4EE
LAVENDER = (180, 167, 214)    # #B4A7D6
DIM = (120, 125, 140)         # footer / muted text

# 4:5 portrait — max IG feed real estate
WIDTH, HEIGHT = 1080, 1350

# ── Fonts ─────────────────────────────────────────────────────
HELV_NEUE = "/System/Library/Fonts/HelveticaNeue.ttc"


def fnt(size, bold=False, light=False):
    # index: 0=Regular, 1=Bold, 3=Light, 4=UltraLight
    if bold:
        idx = 1
    elif light:
        idx = 3
    else:
        idx = 0
    return ImageFont.truetype(HELV_NEUE, size, index=idx)


# ── Background helpers ────────────────────────────────────────
def navy_gradient(w, h):
    """Subtle radial gradient — lighter center, darker edges."""
    img = Image.new("RGB", (w, h), NAVY)
    draw = ImageDraw.Draw(img)
    cx, cy = w // 2, h // 2
    max_r = math.sqrt(cx**2 + cy**2)
    # Draw rings from outside in
    for r in range(int(max_r), 0, -4):
        t = r / max_r
        c = tuple(int(NAVY_LIGHT[i] + (NAVY[i] - NAVY_LIGHT[i]) * t) for i in range(3))
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=c)
    return img


def add_grain(img, amount=12):
    """Add subtle film grain texture."""
    grain = Image.new("RGB", img.size)
    pixels = grain.load()
    for y in range(img.size[1]):
        for x in range(img.size[0]):
            v = random.randint(-amount, amount)
            pixels[x, y] = (128 + v, 128 + v, 128 + v)
    grain = grain.convert("L")
    # Blend very lightly
    img_arr = img.load()
    g_arr = grain.load()
    for y in range(img.size[1]):
        for x in range(img.size[0]):
            r, g, b = img_arr[x, y]
            offset = (g_arr[x, y] - 128) * 0.3
            img_arr[x, y] = (
                max(0, min(255, int(r + offset))),
                max(0, min(255, int(g + offset))),
                max(0, min(255, int(b + offset))),
            )
    return img


def make_bg():
    """Navy background with gradient + grain."""
    img = navy_gradient(WIDTH, HEIGHT)
    img = add_grain(img, amount=10)
    return img


# ── Text helpers ──────────────────────────────────────────────
def wrap(draw, text, f, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        test = f"{cur} {w}".strip()
        if draw.textlength(test, font=f) <= max_w:
            cur = test
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def line_height(draw, f, spacing=1.5):
    bbox = draw.textbbox((0, 0), "Ay", font=f)
    return int((bbox[3] - bbox[1]) * spacing)


def block_height(draw, lines, f, spacing=1.5):
    if not lines:
        return 0
    lh = line_height(draw, f, spacing)
    return lh * len(lines)


def draw_lines_centered(draw, lines, f, x_center, y, color, spacing=1.5):
    lh = line_height(draw, f, spacing)
    for line in lines:
        lw = draw.textlength(line, font=f)
        draw.text((x_center - lw / 2, y), line, font=f, fill=color)
        y += lh
    return y


def draw_lines_left(draw, lines, f, x, y, color, spacing=1.5):
    lh = line_height(draw, f, spacing)
    for line in lines:
        draw.text((x, y), line, font=f, fill=color)
        y += lh
    return y


def draw_footer(draw):
    f = fnt(24)
    text = "@luminouspulse.co"
    tw = draw.textlength(text, font=f)
    draw.text(((WIDTH - tw) / 2, HEIGHT - 65), text, font=f, fill=DIM)


# ── Layout: The Anchor ────────────────────────────────────────
# Text left-aligned in lower 2/3. Accent element in upper third.
def layout_anchor(text, accent_color):
    img = make_bg()
    draw = ImageDraw.Draw(img)
    pad = 90

    # Accent element — circle + line in upper area
    cx = pad + 40
    cy = 220
    r = 24
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=accent_color, width=3)
    draw.line([(cx + r + 14, cy), (cx + r + 180, cy)], fill=accent_color, width=3)

    # Text — left-aligned, lower portion, large
    f = fnt(58)
    max_w = WIDTH - pad * 2
    lines = wrap(draw, text, f, max_w)
    bh = block_height(draw, lines, f)
    y = HEIGHT - 120 - bh - 80
    draw_lines_left(draw, lines, f, pad, y, OFF_WHITE)

    draw_footer(draw)
    return img


# ── Layout: The Spotlight Word ────────────────────────────────
# One word fills ~40% of the card. Rest sits above/below.
def layout_spotlight(text, accent_color, spotlight_word):
    img = make_bg()
    draw = ImageDraw.Draw(img)

    # Find the spotlight word in text
    lower = text.lower()
    sw_lower = spotlight_word.lower()
    idx = lower.find(sw_lower)

    if idx >= 0:
        before = text[:idx].strip()
        after = text[idx + len(spotlight_word):].strip()
        display_word = spotlight_word.upper().rstrip(".,;:!?")
    else:
        before = ""
        display_word = spotlight_word.upper()
        after = text

    # Giant spotlight word — try large, scale down if needed
    for sz in [180, 160, 140, 120]:
        f_big = fnt(sz, bold=True)
        tw = draw.textlength(display_word, font=f_big)
        if tw <= WIDTH - 80:
            break

    big_bbox = draw.textbbox((0, 0), display_word, font=f_big)
    big_h = big_bbox[3] - big_bbox[1]

    # Center the spotlight word vertically
    cy = HEIGHT // 2 - big_h // 2 - 20
    draw.text(((WIDTH - tw) / 2, cy), display_word, font=f_big, fill=accent_color)

    # Text above — readable size
    f_sm = fnt(36, light=True)
    if before:
        bw = draw.textlength(before, font=f_sm)
        draw.text(((WIDTH - bw) / 2, cy - 70), before, font=f_sm, fill=OFF_WHITE)

    # Text below
    if after:
        after = after.lstrip(" .,;:!?")
        if after:
            aw = draw.textlength(after, font=f_sm)
            draw.text(((WIDTH - aw) / 2, cy + big_h + 35), after, font=f_sm,
                      fill=OFF_WHITE)

    draw_footer(draw)
    return img


# ── Layout: The Breath ────────────────────────────────────────
# Enormous space. Narrow column. Light font. Spaciousness is the design.
def layout_breath(text, accent_color):
    img = make_bg()
    draw = ImageDraw.Draw(img)

    f = fnt(42, light=True)
    max_w = WIDTH * 0.55
    lines = wrap(draw, text, f, max_w)
    bh = block_height(draw, lines, f, spacing=2.0)

    y = (HEIGHT - bh) / 2
    draw_lines_centered(draw, lines, f, WIDTH // 2, y, OFF_WHITE, spacing=2.0)

    # Accent dot above text
    draw.ellipse([WIDTH // 2 - 6, y - 50, WIDTH // 2 + 6, y - 38],
                 fill=accent_color)

    draw_footer(draw)
    return img


# ── Layout: The Frame ─────────────────────────────────────────
# Visible border inset from edge. "Window into the sanctuary."
def layout_frame(text, accent_color):
    img = make_bg()
    draw = ImageDraw.Draw(img)

    # Frame border — visible but elegant
    inset = 55
    draw.rectangle(
        [inset, inset, WIDTH - inset, HEIGHT - inset],
        outline=accent_color, width=3
    )

    # Small corner accents (brighter dots at corners)
    for cx, cy in [(inset, inset), (WIDTH - inset, inset),
                   (inset, HEIGHT - inset), (WIDTH - inset, HEIGHT - inset)]:
        draw.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=accent_color)

    # Quote centered inside frame
    pad = 130
    f = fnt(54)
    max_w = WIDTH - pad * 2
    lines = wrap(draw, text, f, max_w)
    bh = block_height(draw, lines, f)
    y = (HEIGHT - bh) / 2
    draw_lines_centered(draw, lines, f, WIDTH // 2, y, OFF_WHITE)

    draw_footer(draw)
    return img


# ── Layout: The Split ─────────────────────────────────────────
# Color block on left (~20%), navy on right. Instantly recognizable.
def layout_split(text, accent_color):
    img = make_bg()
    draw = ImageDraw.Draw(img)

    # Left color block — more visible blend
    block_w = int(WIDTH * 0.20)
    block_color = tuple(int(accent_color[i] * 0.5 + NAVY[i] * 0.5) for i in range(3))
    draw.rectangle([0, 0, block_w, HEIGHT], fill=block_color)

    # Bright accent line at block edge
    draw.line([(block_w, 0), (block_w, HEIGHT)], fill=accent_color, width=3)

    # Text on the right side — large
    text_x = block_w + 70
    text_max_w = WIDTH - text_x - 80
    f = fnt(50)
    lines = wrap(draw, text, f, text_max_w)
    bh = block_height(draw, lines, f)
    y = (HEIGHT - bh) / 2
    draw_lines_left(draw, lines, f, text_x, y, OFF_WHITE)

    draw_footer(draw)
    return img


# ── Layout: The Diagonal ─────────────────────────────────────
# Subtle angle with accent bar behind key phrase.
def layout_diagonal(text, accent_color):
    img = make_bg()
    draw = ImageDraw.Draw(img)

    # Create text on a separate layer, then rotate
    txt_layer = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    txt_draw = ImageDraw.Draw(txt_layer)

    pad = 110
    f = fnt(56)
    max_w = WIDTH - pad * 2
    lines = wrap(txt_draw, text, f, max_w)
    bh = block_height(txt_draw, lines, f)
    y = (HEIGHT - bh) / 2

    # Accent bar behind the last line
    if lines:
        last_line = lines[-1]
        ll_w = txt_draw.textlength(last_line, font=f)
        lh = line_height(txt_draw, f)
        bar_y = y + lh * (len(lines) - 1) - 8
        bar_color = (*accent_color, 65)
        txt_draw.rectangle(
            [WIDTH // 2 - ll_w / 2 - 15, bar_y,
             WIDTH // 2 + ll_w / 2 + 15, bar_y + lh + 8],
            fill=bar_color
        )

    draw_lines_centered(txt_draw, lines, f, WIDTH // 2, y, OFF_WHITE)

    # Rotate ~3 degrees
    txt_layer = txt_layer.rotate(3, resample=Image.BICUBIC, expand=False,
                                  center=(WIDTH // 2, HEIGHT // 2))
    img.paste(txt_layer, (0, 0), txt_layer)

    draw = ImageDraw.Draw(img)
    draw_footer(draw)
    return img


# ══════════════════════════════════════════════════════════════
# GRID SEED DATA
# ══════════════════════════════════════════════════════════════

# 9 posts: 6 from content calendar + 3 strongest from QA audit
# Layout and accent color assigned for grid visual rhythm
#
# Grid reads bottom-to-top on IG (first posted = bottom-right):
#   Row 3 (top):    7  8  9   ← posted last
#   Row 2 (mid):    4  5  6
#   Row 1 (bottom): 1  2  3   ← posted first
#
# Color rhythm: each row gets amber, lavender, blue (one each)
# Layout rhythm: no two adjacent posts share a layout

POSTS = [
    # --- Row 1 (bottom, posted first) ---
    {
        "num": 1,
        "text": "My humanity is not a limitation. It is the entire point.",
        "layout": "anchor",
        "accent": AMBER,
    },
    {
        "num": 2,
        "text": "My creativity runs on living. It always has.",
        "layout": "spotlight",
        "accent": LAVENDER,
        "spotlight_word": "living",
    },
    {
        "num": 3,
        "text": "I give myself permission to navigate this moment with curiosity, not panic.",
        "layout": "breath",
        "accent": BLUE,
    },
    # --- Row 2 (middle) ---
    {
        "num": 4,
        "text": "My worth was never measured in speed. It is measured in depth.",
        "layout": "frame",
        "accent": BLUE,
    },
    {
        "num": 5,
        "text": "I carry things no technology will ever replicate: lived experience, empathy, and purpose.",
        "layout": "split",
        "accent": AMBER,
    },
    {
        "num": 6,
        "text": "I am not behind. I am building something that takes time.",
        "layout": "diagonal",
        "accent": LAVENDER,
    },
    # --- Row 3 (top, posted last) ---
    {
        "num": 7,
        "text": "The part of you that loves cannot be automated.",
        "layout": "spotlight",
        "accent": AMBER,
        "spotlight_word": "loves",
    },
    {
        "num": 8,
        "text": "I am not broken for feeling anxious. I am awake in a world that is changing fast.",
        "layout": "breath",
        "accent": LAVENDER,
    },
    {
        "num": 9,
        "text": "My story cannot be generated. It can only be lived.",
        "layout": "anchor",
        "accent": BLUE,
    },
]


# ══════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════

LAYOUTS = {
    "anchor": layout_anchor,
    "spotlight": layout_spotlight,
    "breath": layout_breath,
    "frame": layout_frame,
    "split": layout_split,
    "diagonal": layout_diagonal,
}


def main():
    base = os.path.dirname(os.path.abspath(__file__))
    out_dir = os.path.join(base, "instagram", "grid-seed")
    os.makedirs(out_dir, exist_ok=True)

    random.seed(42)  # reproducible grain

    print("generating 9 grid-seed posts (1080x1350)...\n")

    for post in POSTS:
        num = post["num"]
        layout_name = post["layout"]
        layout_fn = LAYOUTS[layout_name]
        accent = post["accent"]

        if layout_name == "spotlight":
            img = layout_fn(post["text"], accent, post["spotlight_word"])
        else:
            img = layout_fn(post["text"], accent)

        path = os.path.join(out_dir, f"grid-{num:02d}-{layout_name}.png")
        img.save(path, "PNG", quality=95)
        print(f"  {num}. [{layout_name:10s}] {post['text'][:50]}...")

    print(f"\ndone! 9 posts saved to instagram/grid-seed/")
    print("\npost in order 1→9 to build the grid bottom-up.")
    print("row 1 (bottom): posts 1, 2, 3")
    print("row 2 (middle):  posts 4, 5, 6")
    print("row 3 (top):     posts 7, 8, 9")


if __name__ == "__main__":
    main()
