#!/usr/bin/env python3
"""Sanctuary Reels — Generate professional branded videos for Luminous Pulse.

Usage:
    python generate.py grounding-word --text "steady" --mood ember
    python generate.py quote --text "the part of you that loves cannot be automated." --mood moonlight
    python generate.py breathe --type physiological-sigh --mood twilight
    python generate.py permission --text "you have permission to not apply to a single job today." --mood lavender
"""

import argparse
import base64
import json
import os
import subprocess
import sys
import hashlib

# ── Config ──────────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BG_DIR = os.path.join(SCRIPT_DIR, "backgrounds")
OUT_DIR = os.path.join(SCRIPT_DIR, "out")
INSTAGRAM_DIR = os.path.join(os.path.dirname(SCRIPT_DIR), "instagram", "videos")

ACCENT_COLORS = {
    "amber": "#F4C430",
    "blue": "#6CB4EE",
    "lavender": "#B4A7D6",
}

# Background mood prompts for AI generation
MOOD_PROMPTS = {
    "ember": (
        "Abstract atmospheric background for meditation app. "
        "Deep navy blue darkness with warm amber and golden bokeh lights scattered softly. "
        "Glowing embers floating upward. Warm firelight feeling. Very dark, moody, cinematic. "
        "No text, no people, no objects. Pure abstract atmosphere. 9:16 vertical."
    ),
    "moonlight": (
        "Abstract atmospheric background. Deep navy darkness with silver-blue moonlight "
        "filtering through soft clouds. Ethereal, dreamy, gentle glow. Cool tones with "
        "subtle blue luminescence. Very dark overall. No text, no people. Pure atmosphere. 9:16 vertical."
    ),
    "twilight": (
        "Abstract atmospheric background. Deep blue-purple twilight gradient. "
        "Soft indigo and violet tones blending into deep navy. Stars barely visible. "
        "Peaceful, expansive, calming evening sky. Very dark. No text, no people. "
        "Pure abstract atmosphere. 9:16 vertical."
    ),
    "starfield": (
        "Abstract atmospheric background. Deep dark navy black with scattered distant stars. "
        "Subtle nebula wisps in deep blue and faint purple. Vast, quiet, infinite feeling. "
        "Like looking up at the night sky from a dark field. No text, no people. 9:16 vertical."
    ),
    "lavender": (
        "Abstract atmospheric background. Deep navy darkness with soft lavender and purple mist. "
        "Dreamlike, floating quality. Gentle purple luminescence in the center. "
        "Very dark edges. Soothing, restful. No text, no people. Pure atmosphere. 9:16 vertical."
    ),
    "sunrise": (
        "Abstract atmospheric background. Deep navy blue transitioning to warm golden amber at horizon. "
        "First light of dawn. Soft warm glow breaking through darkness. Hopeful, gentle, quiet morning. "
        "Very dark upper portion. No text, no people. Pure abstract atmosphere. 9:16 vertical."
    ),
    "ocean": (
        "Abstract atmospheric background. Deep dark ocean blue with light filtering through water surface. "
        "Subtle caustic light patterns. Deep, calming, immersive blue. Like being underwater looking up. "
        "Very dark. No text, no people. Pure atmosphere. 9:16 vertical."
    ),
}


def load_api_key():
    """Load OpenRouter API key from .env file."""
    env_path = os.path.join(os.path.dirname(SCRIPT_DIR), ".env")
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                if line.startswith("OPENROUTER_API_KEY="):
                    return line.strip().split("=", 1)[1].strip().strip('"').strip("'")
    key = os.environ.get("OPENROUTER_API_KEY")
    if key:
        return key
    print("error: OPENROUTER_API_KEY not found in .env or environment")
    sys.exit(1)


def generate_background(mood: str, api_key: str) -> str:
    """Generate an AI background image. Returns path to saved PNG.

    Caches by mood name so we don't regenerate the same background twice.
    """
    import requests

    os.makedirs(BG_DIR, exist_ok=True)

    # Check cache
    cache_path = os.path.join(BG_DIR, f"{mood}.png")
    if os.path.exists(cache_path):
        print(f"  using cached background: {mood}")
        return f"backgrounds/{mood}.png"

    prompt = MOOD_PROMPTS.get(mood)
    if not prompt:
        print(f"  unknown mood '{mood}', using navy gradient (no API call)")
        return ""

    print(f"  generating {mood} background via AI...")

    response = requests.post(
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
        timeout=60,
    )

    if response.status_code != 200:
        print(f"  API error {response.status_code}: {response.text[:200]}")
        return ""

    data = response.json()

    # Extract image from response — handle multiple response formats
    b64_data = None
    choices = data.get("choices", [])
    if choices:
        msg = choices[0].get("message", {})

        # Format 1: msg.images[]
        images = msg.get("images", [])

        # Format 2: msg.content[] with type "image" or "image_url"
        if not images and isinstance(msg.get("content"), list):
            images = [
                p for p in msg["content"]
                if isinstance(p, dict) and p.get("type") in ("image", "image_url")
            ]

        if images:
            img_obj = images[0]
            raw = (
                img_obj.get("image_url", {}).get("url", "")
                or img_obj.get("url", "")
                or img_obj.get("data", "")
            )
            if "," in raw:
                b64_data = raw.split(",", 1)[1]
            elif raw:
                b64_data = raw

    if not b64_data:
        print("  could not extract image from API response")
        # Debug: show response structure
        if choices:
            msg = choices[0].get("message", {})
            print(f"  response keys: {list(msg.keys())}")
            content = msg.get("content", "")
            if isinstance(content, list):
                print(f"  content types: {[p.get('type') for p in content if isinstance(p, dict)]}")
        return ""

    # Save
    with open(cache_path, "wb") as f:
        f.write(base64.b64decode(b64_data))

    print(f"  saved: {cache_path}")
    # Return relative path for Remotion's staticFile (relative to public/)
    return f"backgrounds/{mood}.png"


def render_video(composition_id: str, props: dict, output_name: str, duration_frames: int = None):
    """Render a Remotion composition to MP4."""
    os.makedirs(OUT_DIR, exist_ok=True)
    os.makedirs(INSTAGRAM_DIR, exist_ok=True)

    output_path = os.path.join(OUT_DIR, f"{output_name}.mp4")
    instagram_path = os.path.join(INSTAGRAM_DIR, f"{output_name}.mp4")

    # Write props to temp file
    props_path = os.path.join(SCRIPT_DIR, ".render-props.json")
    with open(props_path, "w") as f:
        json.dump(props, f)

    cmd = [
        "npx", "remotion", "render",
        "src/index.ts", composition_id, output_path,
        "--codec", "h264",
        "--props", props_path,
    ]

    # Only add --frames if within composition limits
    # Composition defaults: GroundingWord=300, QuoteCard=450, BreathExercise=660, PermissionSlip=360
    COMP_LIMITS = {
        "GroundingWord": 300, "QuoteCardStory": 450, "QuoteCardFeed": 450,
        "BreathExercise": 900, "PermissionSlip": 360,
    }
    max_frames = COMP_LIMITS.get(composition_id, 9999)
    if duration_frames and duration_frames <= max_frames:
        cmd.extend(["--frames", f"0-{duration_frames - 1}"])

    print(f"\n  rendering {composition_id} → {output_name}.mp4 ...")

    result = subprocess.run(cmd, cwd=SCRIPT_DIR, capture_output=True, text=True, timeout=300)

    # Clean up
    if os.path.exists(props_path):
        os.remove(props_path)

    if result.returncode != 0:
        print(f"  render error (stderr):\n{result.stderr[-1000:]}")
        print(f"  render error (stdout tail):\n{result.stdout[-500:]}")
        return None

    # Copy to instagram/videos/
    import shutil
    shutil.copy2(output_path, instagram_path)

    size_mb = os.path.getsize(output_path) / (1024 * 1024)
    print(f"  done! {size_mb:.1f} MB")
    print(f"  → {output_path}")
    print(f"  → {instagram_path}")
    return output_path


def cmd_grounding_word(args):
    """Generate a grounding word video."""
    api_key = load_api_key()
    bg_path = ""
    if not args.no_background:
        bg_path = generate_background(args.mood, api_key)

    accent = ACCENT_COLORS.get(args.accent, args.accent)

    props = {
        "word": args.text,
        "backgroundSrc": bg_path,
        "accentColor": accent,
        "subtext": args.subtext or "say it out loud. say it again. let it settle.",
    }

    name = args.output or f"grounding-word-{args.text.lower().replace(' ', '-')}"
    render_video("GroundingWord", props, name, duration_frames=300)


def cmd_quote(args):
    """Generate an animated quote card video."""
    api_key = load_api_key()
    bg_path = ""
    if not args.no_background:
        bg_path = generate_background(args.mood, api_key)

    accent = ACCENT_COLORS.get(args.accent, args.accent)
    accent_words = args.accent_words.split(",") if args.accent_words else []

    props = {
        "text": args.text,
        "backgroundSrc": bg_path,
        "accentColor": accent,
        "accentWords": accent_words,
        "cta": args.cta or "save this for when you need it.",
    }

    # Calculate duration based on word count
    word_count = len(args.text.split())
    duration = max(12, min(20, 3 + word_count * 0.5)) * 30  # frames at 30fps

    slug = hashlib.md5(args.text.encode()).hexdigest()[:8]
    name = args.output or f"quote-{slug}"

    fmt = args.format
    if fmt == "story":
        render_video("QuoteCardStory", props, name, duration_frames=int(duration))
    elif fmt == "feed":
        render_video("QuoteCardFeed", props, name, duration_frames=int(duration))
    else:
        render_video("QuoteCardStory", props, f"{name}-story", duration_frames=int(duration))
        render_video("QuoteCardFeed", props, f"{name}-feed", duration_frames=int(duration))


def cmd_breathe(args):
    """Generate a breathing exercise video."""
    api_key = load_api_key()
    bg_path = ""
    if not args.no_background:
        bg_path = generate_background(args.mood, api_key)

    accent = ACCENT_COLORS.get(args.accent, args.accent)

    # Calculate duration based on pattern + cycles
    CYCLE_DURATIONS = {
        "physiological-sigh": 7.7,
        "coherent": 11.5,
        "box": 16.5,
        "4-7-8": 20,
    }
    cycle_dur = CYCLE_DURATIONS.get(args.type, 10)
    total_seconds = 3.5 + cycle_dur * args.cycles + 4  # intro + cycles + outro
    duration_frames = int(total_seconds * 30)

    props = {
        "patternName": args.type,
        "title": args.title or "",
        "subtitle": args.subtitle or "",
        "backgroundSrc": bg_path,
        "accentColor": accent,
        "cycles": args.cycles,
        "outro": args.outro or "your nervous system just got a reset.",
    }

    name = args.output or f"breathe-{args.type}"
    render_video("BreathExercise", props, name, duration_frames=duration_frames)


def cmd_permission(args):
    """Generate a permission slip video."""
    api_key = load_api_key()
    bg_path = ""
    if not args.no_background:
        bg_path = generate_background(args.mood, api_key)

    accent = ACCENT_COLORS.get(args.accent, args.accent)

    # Duration based on text length
    char_count = len(args.text)
    total_seconds = max(10, 3 + char_count * 0.07 + 3)
    duration_frames = int(total_seconds * 30)

    props = {
        "text": args.text,
        "backgroundSrc": bg_path,
        "accentColor": accent,
    }

    slug = hashlib.md5(args.text.encode()).hexdigest()[:8]
    name = args.output or f"permission-{slug}"
    render_video("PermissionSlip", props, name, duration_frames=duration_frames)


def main():
    parser = argparse.ArgumentParser(description="Sanctuary Reels — Luminous Pulse video generator")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Common args
    def add_common(sub):
        sub.add_argument("--mood", default="ember", choices=list(MOOD_PROMPTS.keys()),
                         help="Background mood")
        sub.add_argument("--accent", default="amber", help="Accent color (amber/blue/lavender or hex)")
        sub.add_argument("--output", default="", help="Custom output filename (no extension)")
        sub.add_argument("--no-background", action="store_true", help="Use plain navy gradient")

    # grounding-word
    gw = subparsers.add_parser("grounding-word", help="Grounding word of the day")
    gw.add_argument("--text", required=True, help="The grounding word")
    gw.add_argument("--subtext", default="", help="Override subtext below word")
    add_common(gw)
    gw.set_defaults(func=cmd_grounding_word)

    # quote
    qt = subparsers.add_parser("quote", help="Animated quote card")
    qt.add_argument("--text", required=True, help="The quote text")
    qt.add_argument("--accent-words", default="", help="Comma-separated words to highlight")
    qt.add_argument("--cta", default="", help="Override CTA text")
    qt.add_argument("--format", default="both", choices=["story", "feed", "both"],
                     help="Output format")
    add_common(qt)
    qt.set_defaults(func=cmd_quote)

    # breathe
    br = subparsers.add_parser("breathe", help="Breathing exercise follow-along")
    br.add_argument("--type", default="physiological-sigh",
                     choices=["physiological-sigh", "coherent", "box", "4-7-8"],
                     help="Breathing pattern")
    br.add_argument("--cycles", type=int, default=2, help="Number of breath cycles")
    br.add_argument("--title", default="", help="Override title")
    br.add_argument("--subtitle", default="", help="Override subtitle")
    br.add_argument("--outro", default="", help="Override outro text")
    add_common(br)
    br.set_defaults(func=cmd_breathe)

    # permission
    pm = subparsers.add_parser("permission", help="Permission slip")
    pm.add_argument("--text", required=True, help="The permission text")
    add_common(pm)
    pm.set_defaults(func=cmd_permission)

    args = parser.parse_args()

    print(f"\n{'='*50}")
    print(f"sanctuary reels — luminous pulse")
    print(f"{'='*50}\n")

    args.func(args)

    print(f"\n{'='*50}")
    print(f"done!")
    print(f"{'='*50}\n")


if __name__ == "__main__":
    main()
