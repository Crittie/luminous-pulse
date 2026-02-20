# luminous pulse — content-ready batch 1
**march 10, 2026 launch · instagram**

---

## what's in here

| folder | contents | upload to |
|--------|----------|-----------|
| `01-quote-cards/` | 20 quote card PNGs · 1080×1350 | IG feed post (image) |
| `02-carousels/` | 4 carousels · 8 slides each · 1080×1350 | IG feed post (multi-image, slides in order) |
| `03-reels/` | 6 reel MP4s · 1080×1920 · silent | IG Reels (add audio in app) |
| `04-story-templates/` | 6 reusable story PNGs · 1080×1920 | IG Stories (add stickers in app) |
| `05-highlights/` | 4 highlight cover PNGs · 1080×1080 | IG Story Highlights |

---

## carousels — which is which

| folder | topic | caption file |
|--------|-------|-------------|
| `c1-nobody-tells-you/` | what nobody fucking tells you about losing your job | `scroll-stopping-copy.md` carousel 1 |
| `c2-body-after-layoff/` | 5 things your body does after a layoff | `scroll-stopping-copy.md` carousel 2 |
| `c3-everything-happens-for-a-reason/` | if one more person says everything happens for a reason | `scroll-stopping-copy.md` carousel 3 |
| `c4-where-are-you-right-now/` | where are you right now? (be honest.) | `scroll-stopping-copy.md` carousel 4 |

---

## reels — which is which

| file | concept | duration |
|------|---------|---------|
| `reel-1-youre-awake.mp4` | "you're awake at 2am again" — naming the 2am spiral | ~20s |
| `reel-2-honest-timeline.mp4` | honest timeline of job loss — raw beat-by-beat | ~18s |
| `reel-3-they-say-you-need.mp4` | "they say… you need…" call-and-response | ~15s |
| `reel-4-real-stages.mp4` | the real stages of job loss (not what they told you) | ~20s |
| `reel-5-54321-reset.mp4` | 5-4-3-2-1 grounding reset — guided practice | ~22s |
| `reel-6-still-here.mp4` | "still here" — affirmation close | ~15s |

**reels are silent.** add trending audio in the instagram app before posting.
see `reel-canva-animation-guide.md` for canva animation tips if you want to add motion to the PNGs instead.

---

## story templates — how to use

each template has `[swap: ...]` placeholder zones. open in canva or edit in IG stories:

| file | type | ig sticker to add |
|------|------|-------------------|
| `story-1-permission-slip.png` | permission text | none — just swap the bracketed text |
| `story-2-poll.png` | poll | add IG **poll sticker** over the two pills |
| `story-3-grounding-word.png` | grounding word | none — swap word + definition |
| `story-4-save-worthy.png` | reshare-worthy quote | none — swap statement |
| `story-5-question-box.png` | question sticker | add IG **question sticker** inside the dashed box |
| `story-6-this-or-that.png` | this or that | add IG **slider sticker** in the lavender zone |

**14-day story calendar** → `scroll-stopping-copy.md` (story calendar section)

---

## reusability — yes, all scripts regenerate

all assets were built with python scripts in the project root. to generate a new batch:

```
source .venv/bin/activate

# new quote cards → edit content in generate_quote_cards_v2.py → python generate_quote_cards_v2.py
# new carousels → edit SLIDES[] data in generate_carousel_1.py / generate_carousels_2_3_4.py
# new reels → edit REELS[] data in generate_reels.py + generate_reel_mp4s.py
# new story templates → edit placeholder text in generate_story_templates.py
```

the design system (colors, fonts, glow layers, pulse rings) is shared across all scripts — any regeneration will be visually consistent with this batch.

---

## posting order (content calendar)

follow `content-calendar.md` for day-by-day posting sequence.
cross-platform schedule → `cross-platform-calendar.md`

**launch week quick-start:**
- day 1-2: seed grid with 6-9 quote cards from `01-quote-cards/`
- day 3: first carousel (`c1-nobody-tells-you/`)
- day 4: first reel (`reel-1-youre-awake.mp4`)
- day 5: story series using templates from `04-story-templates/`

---

*@luminouspulse.co · luminouspulse.co*
