#!/usr/bin/env python3
"""Generate all Instagram content for Luminous Pulse.

Outputs:
  instagram/quote-cards/   — 30 quote card PNGs (1080x1080)
  instagram/carousels/     — 8 carousel sets (1080x1080 per slide)
  instagram/highlights/    — 4 Story Highlight cover PNGs (1080x1080)
"""

from PIL import Image, ImageDraw, ImageFont
import os

# ── Brand palette ──────────────────────────────────────────────
NAVY = (26, 39, 68)
NAVY_LIGHT = (35, 50, 82)
BLUE = (108, 180, 238)
AMBER = (244, 196, 48)
LAVENDER = (180, 167, 214)
WHITE = (255, 255, 255)
WHITE_DIM = (210, 215, 225)
DARK_TEXT = (140, 150, 170)

SIZE = (1080, 1080)
PAD = 120  # side padding

# ── Fonts ──────────────────────────────────────────────────────
HELV = "/System/Library/Fonts/Helvetica.ttc"
HELV_NEUE = "/System/Library/Fonts/HelveticaNeue.ttc"


def font(size, bold=False, neue=True):
    path = HELV_NEUE if neue else HELV
    idx = 1 if bold else 0
    return ImageFont.truetype(path, size, index=idx)


# ── Text helpers ───────────────────────────────────────────────
def wrap_text(draw, text, fnt, max_width):
    words = text.split()
    lines, current = [], ""
    for word in words:
        test = f"{current} {word}".strip()
        w = draw.textlength(test, font=fnt)
        if w <= max_width:
            current = test
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def text_block_height(draw, lines, fnt, spacing=1.45):
    if not lines:
        return 0
    bbox = draw.textbbox((0, 0), "Ay", font=fnt)
    lh = bbox[3] - bbox[1]
    return int(lh * spacing * len(lines) - lh * (spacing - 1))


def draw_centered_lines(draw, lines, fnt, y, color=WHITE, spacing=1.45):
    bbox = draw.textbbox((0, 0), "Ay", font=fnt)
    lh = bbox[3] - bbox[1]
    step = int(lh * spacing)
    for line in lines:
        lw = draw.textlength(line, font=fnt)
        x = (SIZE[0] - lw) / 2
        draw.text((x, y), line, font=fnt, fill=color)
        y += step
    return y


def auto_font_size(text):
    length = len(text)
    if length < 45:
        return 54
    elif length < 70:
        return 48
    elif length < 100:
        return 42
    elif length < 140:
        return 36
    else:
        return 32


# ── Decorative elements ───────────────────────────────────────
def draw_quote_mark(draw):
    """Large amber opening quote mark."""
    fnt = font(200, bold=True, neue=False)
    draw.text((PAD - 20, 100), "\u201C", font=fnt, fill=(*AMBER, 60))


def draw_accent_line(draw, y):
    """Thin amber horizontal line."""
    cx = SIZE[0] // 2
    draw.line([(cx - 60, y), (cx + 60, y)], fill=AMBER, width=2)


def draw_brand_footer(draw):
    """Brand handle at bottom."""
    fnt_brand = font(22)
    text = "@luminouspulse.co"
    w = draw.textlength(text, font=fnt_brand)
    draw.text(((SIZE[0] - w) / 2, SIZE[1] - 70), text, font=fnt_brand, fill=DARK_TEXT)


def draw_brand_footer_with_name(draw):
    """Brand name + handle at bottom."""
    fnt_name = font(20, bold=True)
    fnt_handle = font(18)
    name = "luminous pulse"
    handle = "@luminouspulse.co"
    nw = draw.textlength(name, font=fnt_name)
    hw = draw.textlength(handle, font=fnt_handle)
    draw.text(((SIZE[0] - nw) / 2, SIZE[1] - 90), name, font=fnt_name, fill=BLUE)
    draw.text(((SIZE[0] - hw) / 2, SIZE[1] - 62), handle, font=fnt_handle, fill=DARK_TEXT)


def draw_slide_number(draw, current, total):
    """Small slide indicator dots at bottom."""
    dot_r = 4
    gap = 16
    total_w = total * (dot_r * 2) + (total - 1) * gap
    start_x = (SIZE[0] - total_w) / 2
    y = SIZE[1] - 50
    for i in range(total):
        cx = start_x + i * (dot_r * 2 + gap) + dot_r
        color = WHITE if i == current else (*WHITE_DIM, 80)
        draw.ellipse([cx - dot_r, y - dot_r, cx + dot_r, y + dot_r], fill=color)


# ── Quote card generator ──────────────────────────────────────
def generate_quote_card(affirmation, num, output_dir):
    img = Image.new("RGB", SIZE, NAVY)
    draw = ImageDraw.Draw(img, "RGBA")

    # Decorative quote mark (faded)
    draw_quote_mark(draw)

    # Affirmation text
    fsize = auto_font_size(affirmation)
    fnt = font(fsize)
    max_w = SIZE[0] - PAD * 2
    lines = wrap_text(draw, affirmation, fnt, max_w)

    # Center vertically (offset up slightly)
    block_h = text_block_height(draw, lines, fnt)
    y_start = (SIZE[1] - block_h) / 2 - 20
    y_end = draw_centered_lines(draw, lines, fnt, y_start, WHITE)

    # Accent line
    draw_accent_line(draw, y_end + 30)

    # Brand footer
    draw_brand_footer_with_name(draw)

    path = os.path.join(output_dir, f"qc-{num:02d}.png")
    img.save(path, "PNG")
    return path


# ── Carousel generator ────────────────────────────────────────
def generate_carousel_slide(slide_type, text, subtitle, carousel_num,
                            slide_num, total_slides, output_dir):
    img = Image.new("RGB", SIZE, NAVY)
    draw = ImageDraw.Draw(img, "RGBA")

    if slide_type == "hook":
        # Bold title slide
        fnt_main = font(52, bold=True)
        fnt_sub = font(24)
        max_w = SIZE[0] - PAD * 2
        lines = wrap_text(draw, text, fnt_main, max_w)
        block_h = text_block_height(draw, lines, fnt_main)
        y = (SIZE[1] - block_h) / 2 - 40
        if subtitle:
            y -= 20
        draw_centered_lines(draw, lines, fnt_main, y, AMBER)
        if subtitle:
            sub_lines = wrap_text(draw, subtitle, fnt_sub, max_w)
            sub_y = y + block_h + 30
            draw_centered_lines(draw, sub_lines, fnt_sub, sub_y, WHITE_DIM)

    elif slide_type == "content":
        # Content slide — one idea, centered
        fsize = auto_font_size(text)
        fnt = font(fsize)
        max_w = SIZE[0] - PAD * 2
        lines = wrap_text(draw, text, fnt, max_w)
        block_h = text_block_height(draw, lines, fnt)
        y = (SIZE[1] - block_h) / 2 - 10
        draw_centered_lines(draw, lines, fnt, y, WHITE)

    elif slide_type == "affirmation":
        # Quote-style affirmation slide
        draw_quote_mark(draw)
        fnt_label = font(20, bold=True)
        label = "Say it with me:" if "Say it" in text else "Affirmation:"
        if text.startswith('"') or text.startswith('\u201c'):
            label = ""
        fsize = auto_font_size(text)
        fnt = font(fsize)
        max_w = SIZE[0] - PAD * 2
        lines = wrap_text(draw, text, fnt, max_w)
        block_h = text_block_height(draw, lines, fnt)
        y = (SIZE[1] - block_h) / 2 - 10
        if label:
            lw = draw.textlength(label, font=fnt_label)
            draw.text(((SIZE[0] - lw) / 2, y - 50), label,
                      font=fnt_label, fill=AMBER)
        draw_centered_lines(draw, lines, fnt, y, WHITE)

    elif slide_type == "cta":
        # CTA slide
        fnt_main = font(38, bold=True)
        fnt_sub = font(26)
        max_w = SIZE[0] - PAD * 2

        parts = text.split("\n") if "\n" in text else [text]
        # First part bold/amber
        lines1 = wrap_text(draw, parts[0], fnt_main, max_w)
        block_h1 = text_block_height(draw, lines1, fnt_main)

        # Second part regular/white
        lines2 = []
        if len(parts) > 1:
            lines2 = wrap_text(draw, parts[1].strip(), fnt_sub, max_w)
        block_h2 = text_block_height(draw, lines2, fnt_sub) if lines2 else 0

        total_h = block_h1 + block_h2 + (30 if lines2 else 0)
        y = (SIZE[1] - total_h) / 2 - 20
        y = draw_centered_lines(draw, lines1, fnt_main, y, AMBER)
        if lines2:
            draw_centered_lines(draw, lines2, fnt_sub, y + 20, WHITE_DIM)

    elif slide_type == "practice":
        # Practice/recap slide
        fnt_title = font(36, bold=True)
        fnt_body = font(30)
        max_w = SIZE[0] - PAD * 2

        parts = text.split("\n") if "\n" in text else [text]
        lines1 = wrap_text(draw, parts[0], fnt_title, max_w)
        block_h1 = text_block_height(draw, lines1, fnt_title)

        lines2 = []
        if len(parts) > 1:
            lines2 = wrap_text(draw, parts[1].strip(), fnt_body, max_w)
        block_h2 = text_block_height(draw, lines2, fnt_body) if lines2 else 0

        total_h = block_h1 + block_h2 + (25 if lines2 else 0)
        y = (SIZE[1] - total_h) / 2 - 10
        y = draw_centered_lines(draw, lines1, fnt_title, y, LAVENDER)
        if lines2:
            draw_centered_lines(draw, lines2, fnt_body, y + 25, WHITE)

    # Slide dots
    draw_slide_number(draw, slide_num, total_slides)
    # Brand
    draw_brand_footer(draw)

    path = os.path.join(output_dir, f"slide-{slide_num + 1:02d}.png")
    img.save(path, "PNG")
    return path


def generate_carousel(name, slides, carousel_num, base_dir):
    out = os.path.join(base_dir, f"carousel-{carousel_num:02d}-{name}")
    os.makedirs(out, exist_ok=True)
    total = len(slides)
    paths = []
    for i, (stype, text, subtitle) in enumerate(slides):
        p = generate_carousel_slide(stype, text, subtitle,
                                    carousel_num, i, total, out)
        paths.append(p)
    return paths


# ── Highlight icon shapes ─────────────────────────────────────
def draw_highlight_icon(draw, icon_type):
    """Draw a simple geometric icon for highlight covers."""
    cx, cy = SIZE[0] // 2, SIZE[1] // 2 - 50

    if icon_type == "about":
        # Circle with "i" inside
        r = 70
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=AMBER, width=5)
        fnt = font(80, bold=True)
        draw.text((cx - 14, cy - 48), "i", font=fnt, fill=AMBER)

    elif icon_type == "affirmations":
        # Glowing star / radial burst
        import math
        r_outer, r_inner = 75, 30
        points = 8
        star = []
        for i in range(points * 2):
            angle = math.pi / 2 + (math.pi * i / points)
            r = r_outer if i % 2 == 0 else r_inner
            star.append((cx + r * math.cos(angle), cy + r * math.sin(angle)))
        draw.polygon(star, fill=AMBER)

    elif icon_type == "free guide":
        # Down arrow into tray (download icon)
        # Arrow shaft
        draw.rectangle([cx - 8, cy - 60, cx + 8, cy + 10], fill=AMBER)
        # Arrow head
        draw.polygon([(cx - 40, cy + 10), (cx + 40, cy + 10), (cx, cy + 55)],
                     fill=AMBER)
        # Tray
        draw.line([(cx - 55, cy + 65), (cx - 55, cy + 80),
                   (cx + 55, cy + 80), (cx + 55, cy + 65)],
                  fill=AMBER, width=5, joint="curve")

    elif icon_type == "shop":
        # Shopping bag outline
        w, h = 70, 80
        # Bag body
        draw.rectangle([cx - w, cy - h // 2, cx + w, cy + h],
                       outline=AMBER, width=5)
        # Handle
        draw.arc([cx - 30, cy - h // 2 - 40, cx + 30, cy - h // 2 + 10],
                 start=180, end=0, fill=AMBER, width=5)


# ── Highlight cover generator ─────────────────────────────────
def generate_highlight_cover(title, icon_type, output_dir):
    img = Image.new("RGB", SIZE, NAVY)
    draw = ImageDraw.Draw(img)

    # Draw geometric icon
    draw_highlight_icon(draw, icon_type)

    # Title below icon
    fnt_title = font(36, bold=True)
    tw = draw.textlength(title, font=fnt_title)
    draw.text(((SIZE[0] - tw) / 2, SIZE[1] // 2 + 100),
              title, font=fnt_title, fill=WHITE)

    path = os.path.join(output_dir, f"highlight-{title.lower().replace(' ', '-')}.png")
    img.save(path, "PNG")
    return path


# ══════════════════════════════════════════════════════════════
# DATA
# ══════════════════════════════════════════════════════════════

QUOTE_CARDS = [
    "My humanity is not a limitation. It is the entire point.",
    "Technology amplifies my creativity. It does not replace it.",
    "I give myself permission to navigate this moment with curiosity, not panic.",
    "My value is not measured in output speed. It is measured in judgment.",
    "I carry things no technology will ever replicate: lived experience, empathy, and purpose.",
    "I am not behind. I am building something that takes time: expertise.",
    "No algorithm will ever understand what it feels like to be me. That is my edge.",
    "I wake up with something no machine ever will: a reason to care about today.",
    "I read rooms, build trust, and make calls that no dashboard can make. That is my job.",
    "The things that make me human \u2014 doubt, courage, love \u2014 are features, not bugs.",
    "I am the original intelligence. Everything else is built in my image.",
    "I am whole before I open my laptop.",
    "Every problem I have ever solved has made me harder to replace.",
    "I am not broken for feeling anxious. I am awake in a world that is changing fast.",
    "Today I choose to see change as an invitation, not a threat.",
    "I am not a prompt. I am the person behind it.",
    "The headlines are designed to scare me. My life is designed to be lived.",
    "I am the author of this day. Not the algorithm, not the feed, not the forecast.",
    "My story cannot be generated. It can only be lived.",
    "I can learn any tool. No tool can learn to be me.",
    "I do not need to optimize my morning. I need to feel it.",
    "I trust my instincts more than any output. They have kept me alive this long.",
    "I have reinvented myself before. I will do it again. This is what I do.",
    "My ability to feel is not a flaw in the system. It is the system.",
    "I replace \u2018what if it all goes wrong\u2019 with \u2018what if I handle it.\u2019",
    "I give the world something it cannot download: presence.",
    "I will not panic about a future I am actively building.",
    "I am allowed to step away from the noise. Silence is not falling behind.",
    "Today, I bring the one thing no tool can: genuine intention.",
    "The future belongs to people who know who they are. I am becoming that person.",
]

CAROUSELS = [
    {
        "name": "5-things-ai-will-never-have",
        "slides": [
            ("hook", "5 Things AI Will Never Have", None),
            ("content", "The instinct to pause before saying something that could hurt someone.", None),
            ("content", "The courage to start over after everything falls apart.", None),
            ("content", "The warmth of sitting next to someone in silence and making them feel less alone.", None),
            ("content", "The ability to look at a sunset and feel something it can\u2019t name.", None),
            ("content", "The stubbornness to keep going when every logical reason says quit.", None),
            ("affirmation", "\u201CI carry things no technology will ever replicate.\u201D", None),
            ("cta", "Save this for the days you need a reminder.\nShare with someone who needs to hear this today.", None),
        ],
    },
    {
        "name": "5-affirmations-for-the-ai-age",
        "slides": [
            ("hook", "5 Affirmations for the AI Age", "(screenshot this)"),
            ("affirmation", "\u201CI am irreplaceable \u2014 not because of what I produce, but because of who I am.\u201D", None),
            ("affirmation", "\u201CTechnology amplifies my creativity. It does not replace it.\u201D", None),
            ("affirmation", "\u201CI adapt, I learn, and I bring something to every room that no tool ever will.\u201D", None),
            ("affirmation", "\u201CMy intuition is trained on a lifetime of being human. No dataset compares.\u201D", None),
            ("affirmation", "\u201CI choose to grow alongside AI, not in competition with it.\u201D", None),
            ("practice", "Your morning practice:\nRead these aloud. Every single day.", None),
            ("cta", "Want 7 more?\nGrab our free affirmation guide. Link in bio.", None),
        ],
    },
    {
        "name": "how-to-reframe-ai-anxiety",
        "slides": [
            ("hook", "Feeling anxious about AI?", "Read this before your next spiral."),
            ("content", "The anxiety is normal. You\u2019re watching the world change in real time. That\u2019s disorienting.", None),
            ("content", "But here\u2019s what anxiety skips: You\u2019ve adapted before. New tools. New industries. New ways of working. You\u2019re still here.", None),
            ("content", "AI is a tool. A powerful one. But a tool doesn\u2019t have your judgment, your taste, your instincts.", None),
            ("content", "The people who thrive won\u2019t be the ones who fight AI. They\u2019ll be the ones who use it without losing themselves.", None),
            ("affirmation", "\u201CI navigate change with steadiness and curiosity. I have done this before.\u201D", None),
            ("affirmation", "\u201CI am not in competition with technology. I am in partnership with it.\u201D", None),
            ("cta", "Save this carousel.\nCome back to it the next time a headline tries to scare you.", None),
        ],
    },
    {
        "name": "what-your-boss-cant-automate",
        "slides": [
            ("hook", "What your boss can\u2019t automate:", "(this might surprise you)"),
            ("content", "Reading the room in a tense meeting and knowing when to speak \u2014 and when to listen.", None),
            ("content", "Building trust with a difficult client over months of small, consistent gestures.", None),
            ("content", "Making the call when the data says one thing and your gut says another.", None),
            ("content", "Mentoring someone through a career crisis with honesty and care.", None),
            ("content", "Noticing what\u2019s NOT being said in a meeting \u2014 and gently surfacing it.", None),
            ("affirmation", "\u201CI bring emotional intelligence, ethical judgment, and lived experience to every role I hold.\u201D", None),
            ("cta", "Know someone worried about their job in the AI age?\nSend them this.", None),
        ],
    },
    {
        "name": "morning-affirmations-for-tech-workers",
        "slides": [
            ("hook", "Morning affirmations for anyone who works alongside AI tools", None),
            ("affirmation", "\u201CI use AI as a collaborator, not a replacement for my own thinking.\u201D", None),
            ("affirmation", "\u201CMy value at work is not measured in output speed. It\u2019s measured in judgment.\u201D", None),
            ("affirmation", "\u201CI am allowed to learn slowly. Mastery and speed are not the same thing.\u201D", None),
            ("affirmation", "\u201CToday, I bring something to my work that no prompt could ever generate: me.\u201D", None),
            ("affirmation", "\u201CI do not need to know everything about AI to be valuable.\u201D", None),
            ("practice", "Try this:\nPick ONE of these. Set it as your phone wallpaper. Read it every morning this week.", None),
            ("cta", "Follow for daily affirmations that actually match the world you live in.", None),
        ],
    },
    {
        "name": "signs-youre-more-resilient",
        "slides": [
            ("hook", "6 signs you\u2019re more resilient than you think", "(even if it doesn\u2019t feel like it)"),
            ("content", "You\u2019ve already survived every \u201Cworst day\u201D you\u2019ve had. Your track record is 100%.", None),
            ("content", "You learned new tools when your industry changed \u2014 even when it felt impossible.", None),
            ("content", "You ask hard questions about the future instead of burying your head. (You\u2019re doing that right now.)", None),
            ("content", "You\u2019re here \u2014 seeking growth, not avoidance. That\u2019s not anxiety. That\u2019s wisdom in motion.", None),
            ("content", "You hold complexity. You can be excited about AI AND unsettled by it. Both are valid. Both are human.", None),
            ("affirmation", "\u201CI have adapted before. I will adapt again. My resilience is not a theory \u2014 it\u2019s my lived history.\u201D", None),
            ("cta", "Needed this?\nSave it. Send it to someone who\u2019s been in their head lately.", None),
        ],
    },
    {
        "name": "human-skills-that-matter-most",
        "slides": [
            ("hook", "In the age of AI, these human skills matter more than ever:", None),
            ("content", "Creative problem-solving. AI optimizes within rules. You break them when they stop working.", None),
            ("content", "Emotional regulation. Staying calm in chaos. Leading through uncertainty. No model can do this.", None),
            ("content", "Cross-cultural communication. Understanding context, nuance, and the things people mean but don\u2019t say.", None),
            ("content", "Ethical judgment. Deciding what should be done \u2014 not just what can be done.", None),
            ("content", "Deep listening. Hearing what someone needs before they\u2019ve found the words.", None),
            ("affirmation", "\u201CMy human skills are not soft skills. They are survival skills. And they are mine.\u201D", None),
            ("cta", "Which skill resonates most?\nTell us in the comments. Follow for more.", None),
        ],
    },
    {
        "name": "a-permission-slip",
        "slides": [
            ("hook", "Consider this your permission slip:", None),
            ("content", "You are allowed to feel overwhelmed by how fast things are changing.", None),
            ("content", "You are allowed to not have an opinion on every new AI tool.", None),
            ("content", "You are allowed to say \u201CI don\u2019t know yet\u201D when someone asks if AI will take your job.", None),
            ("content", "You are allowed to use AI without feeling like a fraud \u2014 and to not use it without feeling left behind.", None),
            ("content", "You are allowed to move at your own pace. Adoption is not a race.", None),
            ("affirmation", "\u201CI give myself permission to navigate this moment with curiosity, not panic.\u201D", None),
            ("cta", "Save your permission slip. It doesn\u2019t expire.\nFree affirmation guide in our bio.", None),
        ],
    },
]

HIGHLIGHTS = [
    ("About", "about"),
    ("Affirmations", "affirmations"),
    ("Free Guide", "free guide"),
    ("Shop", "shop"),
]


# ══════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════

def main():
    base = os.path.dirname(os.path.abspath(__file__))
    ig = os.path.join(base, "instagram")

    # ── Quote cards ──
    qc_dir = os.path.join(ig, "quote-cards")
    os.makedirs(qc_dir, exist_ok=True)
    print(f"Generating {len(QUOTE_CARDS)} quote cards...")
    for i, aff in enumerate(QUOTE_CARDS, 1):
        generate_quote_card(aff, i, qc_dir)
        print(f"  qc-{i:02d}.png")

    # ── Carousels ──
    car_dir = os.path.join(ig, "carousels")
    os.makedirs(car_dir, exist_ok=True)
    print(f"\nGenerating {len(CAROUSELS)} carousels...")
    for i, c in enumerate(CAROUSELS, 1):
        slides = c["slides"]
        print(f"  Carousel {i}: {c['name']} ({len(slides)} slides)")
        generate_carousel(c["name"], slides, i, car_dir)

    # ── Highlight covers ──
    hl_dir = os.path.join(ig, "highlights")
    os.makedirs(hl_dir, exist_ok=True)
    print(f"\nGenerating {len(HIGHLIGHTS)} highlight covers...")
    for title, icon in HIGHLIGHTS:
        generate_highlight_cover(title, icon, hl_dir)
        print(f"  {title}")

    # ── Summary ──
    total_qc = len(QUOTE_CARDS)
    total_slides = sum(len(c["slides"]) for c in CAROUSELS)
    total_hl = len(HIGHLIGHTS)
    total = total_qc + total_slides + total_hl
    print(f"\nDone! {total} images generated:")
    print(f"  {total_qc} quote cards")
    print(f"  {total_slides} carousel slides ({len(CAROUSELS)} carousels)")
    print(f"  {total_hl} highlight covers")


if __name__ == "__main__":
    main()
