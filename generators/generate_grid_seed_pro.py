#!/usr/bin/env python3
"""Generate 9 professional grid-seed posts for Luminous Pulse IG launch.

AI-generated backgrounds (Gemini) + programmatic text overlays.
Output: instagram/grid-seed/  — 9 PNGs at 1080x1350 (4:5 portrait)
"""

import base64
import json
import os
import sys
import time

import requests
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
from io import BytesIO


# ── Config ────────────────────────────────────────────────────
WIDTH, HEIGHT = 1080, 1350
HELV = "/System/Library/Fonts/HelveticaNeue.ttc"

OFF_WHITE = (245, 240, 235)
AMBER = (244, 196, 48)
BLUE = (108, 180, 238)
LAVENDER = (180, 167, 214)
DIM = (160, 155, 150)


def fnt(size, bold=False, light=False):
    idx = 1 if bold else (3 if light else 0)
    return ImageFont.truetype(HELV, size, index=idx)


# ── API ───────────────────────────────────────────────────────
def load_api_key():
    for d in [os.getcwd()] + list(
        p for p in [os.path.expanduser("~")] if os.path.isdir(p)
    ):
        env = os.path.join(d, ".env")
        if os.path.isfile(env):
            with open(env) as f:
                for line in f:
                    if line.startswith("OPENROUTER_API_KEY="):
                        return line.split("=", 1)[1].strip().strip("'\"")
    return None


def generate_background(prompt, api_key):
    """Generate an image via OpenRouter and return as PIL Image."""
    resp = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": "google/gemini-3-pro-image-preview",
            "messages": [{"role": "user", "content": prompt}],
            "modalities": ["image", "text"],
        },
    )
    if resp.status_code != 200:
        print(f"  API error {resp.status_code}: {resp.text[:200]}")
        return None

    result = resp.json()
    choices = result.get("choices", [])
    if not choices:
        return None

    msg = choices[0]["message"]
    images = msg.get("images", [])
    if not images and isinstance(msg.get("content"), list):
        images = [p for p in msg["content"] if isinstance(p, dict) and p.get("type") == "image"]

    if not images:
        return None

    img_data = images[0]
    b64 = img_data.get("image_url", {}).get("url") or img_data.get("url", "")
    if "," in b64:
        b64 = b64.split(",", 1)[1]

    return Image.open(BytesIO(base64.b64decode(b64)))


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


def lh(draw, f, spacing=1.5):
    bbox = draw.textbbox((0, 0), "Ay", font=f)
    return int((bbox[3] - bbox[1]) * spacing)


def bh(draw, lines, f, spacing=1.5):
    return lh(draw, f, spacing) * len(lines) if lines else 0


def draw_centered(draw, lines, f, cx, y, color, spacing=1.5):
    step = lh(draw, f, spacing)
    for line in lines:
        lw = draw.textlength(line, font=f)
        draw.text((cx - lw / 2, y), line, font=f, fill=color)
        y += step
    return y


def draw_left(draw, lines, f, x, y, color, spacing=1.5):
    step = lh(draw, f, spacing)
    for line in lines:
        draw.text((x, y), line, font=f, fill=color)
        y += step
    return y


def draw_footer(draw):
    f = fnt(24)
    t = "@luminouspulse.co"
    tw = draw.textlength(t, font=f)
    draw.text(((WIDTH - tw) / 2, HEIGHT - 65), t, font=f, fill=DIM)


# ── Layout functions ──────────────────────────────────────────
def layout_anchor(img, text, accent):
    draw = ImageDraw.Draw(img)
    pad = 90
    # Accent element upper area
    cx, cy = pad + 40, 220
    draw.ellipse([cx - 24, cy - 24, cx + 24, cy + 24], outline=accent, width=3)
    draw.line([(cx + 38, cy), (cx + 200, cy)], fill=accent, width=3)
    # Text lower portion
    f = fnt(58)
    lines = wrap(draw, text, f, WIDTH - pad * 2)
    h = bh(draw, lines, f)
    y = HEIGHT - 120 - h - 80
    draw_left(draw, lines, f, pad, y, OFF_WHITE)
    draw_footer(draw)
    return img


def layout_spotlight(img, text, accent, word):
    draw = ImageDraw.Draw(img)
    lo = text.lower()
    wl = word.lower()
    idx = lo.find(wl)
    before = text[:idx].strip() if idx >= 0 else ""
    after = text[idx + len(word):].strip().lstrip(" .,;:!?") if idx >= 0 else text
    display = word.upper().rstrip(".,;:!?")

    for sz in [180, 160, 140, 120]:
        fb = fnt(sz, bold=True)
        tw = draw.textlength(display, font=fb)
        if tw <= WIDTH - 80:
            break

    bb = draw.textbbox((0, 0), display, font=fb)
    big_h = bb[3] - bb[1]
    cy = HEIGHT // 2 - big_h // 2 - 20
    draw.text(((WIDTH - tw) / 2, cy), display, font=fb, fill=accent)

    fs = fnt(36, light=True)
    if before:
        bw = draw.textlength(before, font=fs)
        draw.text(((WIDTH - bw) / 2, cy - 70), before, font=fs, fill=OFF_WHITE)
    if after:
        aw = draw.textlength(after, font=fs)
        draw.text(((WIDTH - aw) / 2, cy + big_h + 35), after, font=fs, fill=OFF_WHITE)

    draw_footer(draw)
    return img


def layout_breath(img, text, accent):
    draw = ImageDraw.Draw(img)
    f = fnt(42, light=True)
    max_w = WIDTH * 0.55
    lines = wrap(draw, text, f, max_w)
    h = bh(draw, lines, f, spacing=2.0)
    y = (HEIGHT - h) / 2
    draw_centered(draw, lines, f, WIDTH // 2, y, OFF_WHITE, spacing=2.0)
    draw.ellipse([WIDTH // 2 - 6, y - 50, WIDTH // 2 + 6, y - 38], fill=accent)
    draw_footer(draw)
    return img


def layout_frame(img, text, accent):
    draw = ImageDraw.Draw(img, "RGBA")
    inset = 55
    draw.rectangle([inset, inset, WIDTH - inset, HEIGHT - inset],
                   outline=accent, width=3)
    for cx, cy in [(inset, inset), (WIDTH - inset, inset),
                   (inset, HEIGHT - inset), (WIDTH - inset, HEIGHT - inset)]:
        draw.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=accent)

    f = fnt(52)
    pad = 130
    lines = wrap(draw, text, f, WIDTH - pad * 2)
    h = bh(draw, lines, f)
    y = (HEIGHT - h) / 2
    draw_centered(draw, lines, f, WIDTH // 2, y, OFF_WHITE)
    draw_footer(draw)
    return img


def layout_split(img, text, accent):
    draw = ImageDraw.Draw(img, "RGBA")
    block_w = int(WIDTH * 0.20)
    overlay = (*accent, 60)
    draw.rectangle([0, 0, block_w, HEIGHT], fill=overlay)
    draw.line([(block_w, 0), (block_w, HEIGHT)], fill=accent, width=3)

    tx = block_w + 70
    f = fnt(50)
    lines = wrap(draw, text, f, WIDTH - tx - 80)
    h = bh(draw, lines, f)
    y = (HEIGHT - h) / 2
    draw_left(draw, lines, f, tx, y, OFF_WHITE)
    draw_footer(draw)
    return img


def layout_diagonal(img, text, accent):
    draw = ImageDraw.Draw(img)
    txt = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    td = ImageDraw.Draw(txt)

    f = fnt(56)
    pad = 110
    lines = wrap(td, text, f, WIDTH - pad * 2)
    h = bh(td, lines, f)
    y = (HEIGHT - h) / 2

    if lines:
        last = lines[-1]
        llw = td.textlength(last, font=f)
        step = lh(td, f)
        by = y + step * (len(lines) - 1) - 8
        td.rectangle([WIDTH // 2 - llw / 2 - 15, by,
                       WIDTH // 2 + llw / 2 + 15, by + step + 8],
                      fill=(*accent, 65))

    draw_centered(td, lines, f, WIDTH // 2, y, OFF_WHITE)
    txt = txt.rotate(3, resample=Image.BICUBIC, expand=False,
                     center=(WIDTH // 2, HEIGHT // 2))
    img.paste(txt, (0, 0), txt)
    draw = ImageDraw.Draw(img)
    draw_footer(draw)
    return img


# ── Post data ─────────────────────────────────────────────────
POSTS = [
    {
        "num": 1,
        "text": "The headlines are designed to scare me. My life is designed to be lived.",
        "layout": "anchor",
        "accent": AMBER,
        "bg_prompt": (
            "Abstract dark navy blue background, deep navy tones (#1a1a2e). "
            "Warm amber ember glow in the lower portion, like dying campfire embers "
            "in darkness. Subtle smoke wisps. Film grain texture. "
            "No text, no objects, no people. Portrait 4:5. "
            "Moody, defiant, warm. Premium quality."
        ),
    },
    {
        "num": 2,
        "text": "I am not broken for feeling anxious. I am awake in a world that is changing fast.",
        "layout": "breath",
        "accent": LAVENDER,
        "bg_prompt": (
            "Abstract dark navy background with soft lavender and purple mist "
            "drifting gently across the center. Ethereal, dreamlike, gentle. "
            "Very subtle bokeh. Film grain. Deep navy (#1a1a2e) dominant. "
            "No text, no objects, no people. Portrait 4:5. "
            "Soothing, validating, soft. Premium quality."
        ),
    },
    {
        "num": 3,
        "text": "I do not need to have an answer when someone asks what I'm doing next.",
        "layout": "frame",
        "accent": BLUE,
        "bg_prompt": (
            "Abstract dark navy background with cool blue light filtering "
            "softly from one side, like moonlight through a window. "
            "Still, quiet, contained. Subtle dust particles in the light beam. "
            "Navy (#1a1a2e) dominant. No text, no objects, no people. Portrait 4:5. "
            "Calm, permission, peaceful. Premium quality."
        ),
    },
    {
        "num": 4,
        "text": "The part of you that loves cannot be automated.",
        "layout": "spotlight",
        "accent": AMBER,
        "spotlight_word": "loves",
        "bg_prompt": (
            "Abstract dark navy background with warm golden amber bokeh light "
            "particles floating like fireflies. Soft warm glow emanating from "
            "the center. Atmospheric, intimate. Film grain. Navy (#1a1a2e) dominant. "
            "No text, no objects, no people. Portrait 4:5. "
            "Warm, heartfelt, sanctuary. Premium quality."
        ),
    },
    {
        "num": 5,
        "text": "I am allowed to feel the full weight of this before I figure out what's next.",
        "layout": "split",
        "accent": BLUE,
        "bg_prompt": (
            "Abstract dark navy background with a single soft blue-white light "
            "source on the left side, fading into deep darkness on the right. "
            "Like a doorway of light in a dark room. Minimal, weighted. "
            "Navy (#1a1a2e) dominant. No text, no objects, no people. Portrait 4:5. "
            "Heavy, honest, grounding. Premium quality."
        ),
    },
    {
        "num": 6,
        "text": "I am not behind. I am building something that takes time.",
        "layout": "diagonal",
        "accent": LAVENDER,
        "bg_prompt": (
            "Abstract dark navy background with soft purple twilight gradient "
            "in the upper portion, fading to deep navy below. Subtle star-like "
            "points of light. Quiet, forward-looking. Film grain. "
            "Navy (#1a1a2e) dominant. No text, no objects, no people. Portrait 4:5. "
            "Patient, hopeful, twilight. Premium quality."
        ),
    },
    {
        "num": 7,
        "text": "You were never meant to scroll through your own obsolescence at 11pm. Put the phone down. Breathe. You are still here.",
        "layout": "breath",
        "accent": LAVENDER,
        "bg_prompt": (
            "Abstract dark navy background with a cool blue-white phone-screen-like "
            "glow in the center that fades to soft lavender at the edges, "
            "surrounded by deep darkness. Like a phone screen illuminating a dark room. "
            "Atmospheric, haunting, tender. Navy (#1a1a2e) dominant. "
            "No text, no objects, no people. Portrait 4:5. Premium quality."
        ),
    },
    {
        "num": 8,
        "text": "Breathe first. Plan later. Survive the feeling before you solve the problem.",
        "layout": "anchor",
        "accent": AMBER,
        "bg_prompt": (
            "Abstract dark navy background with warm amber light breaking "
            "through from below, like sunrise on the horizon or light under a door. "
            "Atmospheric, grounding, hopeful. Soft gradient from dark to warm. "
            "Film grain. Navy (#1a1a2e) dominant. "
            "No text, no objects, no people. Portrait 4:5. Premium quality."
        ),
    },
    {
        "num": 9,
        "text": "I do not owe anyone a hot take on the future. I owe myself peace.",
        "layout": "frame",
        "accent": BLUE,
        "bg_prompt": (
            "Abstract dark navy background with scattered tiny blue-white stars "
            "or light points across a vast dark space. Cosmic, spacious, peaceful. "
            "Like looking up at a clear night sky. Minimal, expansive. "
            "Navy (#1a1a2e) dominant. No text, no objects, no people. Portrait 4:5. "
            "Vast, free, restful. Premium quality."
        ),
    },
]


# ── Main ──────────────────────────────────────────────────────
def main():
    api_key = load_api_key()
    if not api_key:
        print("error: OPENROUTER_API_KEY not found in .env")
        sys.exit(1)

    base = os.path.dirname(os.path.abspath(__file__))
    out_dir = os.path.join(base, "instagram", "grid-seed")
    os.makedirs(out_dir, exist_ok=True)

    print("generating 9 professional grid-seed posts...\n")

    for post in POSTS:
        num = post["num"]
        print(f"  {num}/9: generating background...")

        bg = generate_background(post["bg_prompt"], api_key)
        if bg is None:
            print(f"  {num}/9: background generation failed, using gradient fallback")
            bg = Image.new("RGB", (WIDTH, HEIGHT), (26, 26, 46))

        # Resize to 1080x1350
        bg = bg.resize((WIDTH, HEIGHT), Image.LANCZOS)

        # Darken slightly for text readability
        bg = ImageEnhance.Brightness(bg).enhance(0.65)
        bg = bg.convert("RGBA")

        # Apply layout
        layout = post["layout"]
        accent = post["accent"]

        if layout == "anchor":
            img = layout_anchor(bg, post["text"], accent)
        elif layout == "spotlight":
            img = layout_spotlight(bg, post["text"], accent, post["spotlight_word"])
        elif layout == "breath":
            img = layout_breath(bg, post["text"], accent)
        elif layout == "frame":
            img = layout_frame(bg, post["text"], accent)
        elif layout == "split":
            img = layout_split(bg, post["text"], accent)
        elif layout == "diagonal":
            img = layout_diagonal(bg, post["text"], accent)

        # Save as RGB
        img = img.convert("RGB")
        path = os.path.join(out_dir, f"grid-{num:02d}-{layout}.png")
        img.save(path, "PNG", quality=95)
        print(f"  {num}/9: saved {os.path.basename(path)}")
        print(f"         \"{post['text'][:50]}...\"\n")

        # Small delay to avoid rate limiting
        if num < 9:
            time.sleep(1)

    print("done! 9 professional posts saved to instagram/grid-seed/")
    print("\npost order 1→9 to build the grid.")


if __name__ == "__main__":
    main()
