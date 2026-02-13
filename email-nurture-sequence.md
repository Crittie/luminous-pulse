# 5-Email Nurture Sequence — Free → Paid Conversion

> **Trigger**: Subscriber completes welcome sequence AND does NOT have `paid-customer` tag
> **Goal**: Convert free lead magnet subscribers into paid customers ($12-17 deck)
> **Tone**: Same as welcome sequence — personal, warm, story-driven. Never pushy.
> **From name**: Christie at Luminous Pulse
> **Timing**: Day 7, Day 10, Day 14, Day 17, Day 21 (after initial signup)

---

## Email 1: The Story (Day 7)

**Subject**: what I wish someone told me about AI anxiety

**Preview text**: It wasn't a tool that scared me. It was a meeting.

---

Hey,

I want to tell you something I haven't shared publicly.

Last year I was in a meeting where my manager pulled up a demo of a tool that could do — in 45 seconds — something that took me two days to produce.

Nobody in the room looked at me. But I felt it.

That night I went home and spiraled. Not about the tool. About what I was worth without the thing I thought made me valuable.

And here's what I figured out over the next few weeks: the spiral wasn't about AI. It was about identity. I had tied my worth to my output — and when a machine matched my output, I didn't know who I was without it.

That's the real crisis nobody talks about. It's not a skills gap. It's an identity gap.

The affirmations I write aren't about ignoring AI or pretending it doesn't matter. They're about remembering who you are underneath what you produce.

If you've ever felt that unnamed heaviness after reading an AI headline — you're not broken. You're human. And that's the whole point.

More soon,
Christie

P.S. — If you haven't tried saying one of the free affirmations out loud yet, today's a good day. Start with: *"My intuition is trained on a lifetime of being human. No dataset compares."*

---

## Email 2: Value-First (Day 10)

**Subject**: 3 affirmations for your work week

**Preview text**: Pin one to your desk. Say it before your first meeting.

---

Hey,

Monday energy incoming. Here are three affirmations to carry into your week — one for each vibe:

**If you're feeling uncertain:**
> *"I will not panic about a future I am actively building."*

**If you're in meetings all day:**
> *"I read rooms, build trust, and make calls that no dashboard can make. That is my job."*

**If imposter syndrome is loud:**
> *"I can learn any tool. No tool can learn to be me."*

Pick one. Write it on a sticky note. Put it where you'll see it before your first meeting.

The practice is simple: read it, say it out loud once, and move on with your day. Two seconds. That's all it takes to shift the energy.

These three are from the full collection — 50 affirmations across four themes, each with a reflection prompt to help you go deeper. If the free 7 cards have been working for you, the full deck is the next step.

But for now — just pick one of these three and try it tomorrow morning.

Talk soon,
Christie

P.S. — Which one did you pick? Reply and tell me. I'm genuinely curious which one lands for you.

---

## Email 3: The Full Collection (Day 14)

**Subject**: the full collection is here

**Preview text**: 50 affirmations. 4 themes. Every card has a reflection prompt.

---

Hey,

Two weeks ago you downloaded 7 affirmations. I hope at least one of them has found a permanent spot on your desk or your mirror.

Today I want to share what's behind those 7.

I spent months writing, testing, and refining a complete collection: **50 Affirmations for the AI Age.**

It's organized into four themes:

**AI-Age Empowerment** — for the moments when you wonder where you fit
**Career Confidence** — for the days when imposter syndrome meets automation anxiety
**Morning Motivation** — for starting your day grounded, not scrolling
**Anxiety Relief** — for the nights when the "what ifs" are loud

Every card has a reflection prompt on the back — not just the affirmation, but a question to help you sit with it. That's the part that makes this more than a card deck. It's a practice.

**The full collection is $12 right now** (it'll go up to $17 soon).

> **[Get the 50-Card Deck → Link to Gumroad]**

Print them. Cut them. Pin your favorites everywhere. Come back to the deck in 30 days and notice which affirmations hit differently than they did on day one.

That's when you'll know it's working.

Your humanity is your superpower,
Christie

P.S. — If $12 is tough right now, no pressure at all. The free 7 are yours forever and the weekly affirmations I share are always free. This is here when you're ready.

---

## Email 4: Social Proof (Day 17)

**Subject**: "I didn't think affirmations were for me"

**Preview text**: What I keep hearing from people who tried the deck.

---

Hey,

I want to share something I've been hearing a lot:

*"I didn't think affirmations were for me. I thought they were too woo-woo. But these actually make sense because they're about the real world."*

That response keeps coming up — from engineers, PMs, designers, marketers. People who would never describe themselves as "affirmation people."

And I get it. Most affirmation content feels like it was written in a different decade. "I am abundant." "I attract success." Those don't land when you're worried about whether your job exists in two years.

That's exactly why I made these different.

Every affirmation in this deck was written for a specific feeling:
- The feeling after reading a scary AI headline
- The feeling before a meeting where you're not sure you're needed
- The feeling at 11pm when you're wondering if you should be learning something new

These are affirmations for real life. Your life. Right now.

> **[Get the 50-Card Deck → $12 → Link to Gumroad]**

If one of the free 7 has already stuck with you, imagine what 50 could do.

More soon,
Christie

P.S. — If you've been using the free cards and have a favorite, I'd love to hear which one. Just reply — every response makes my day.

---

## Email 5: Last Chance (Day 21)

**Subject**: last day at this price

**Preview text**: The launch price goes away tomorrow.

---

Hey,

Quick note — the launch price for the 50-card affirmation deck ends tomorrow.

After that, it goes from $12 to $17.

I'm not going to write a long email about this. You already know if these affirmations work for you. You've had the free 7 for three weeks.

If they've helped, the full collection is the obvious next step. 50 cards. 4 themes. Reflection prompts on every one.

> **[Get the deck at $12 before the price goes up → Link to Gumroad]**

If now's not the right time, that's completely fine. I'll keep showing up in your inbox with free affirmations and real talk about navigating this moment.

Either way — your humanity is your superpower. Don't forget it.

Christie

P.S. — After this, I won't pitch the deck again for a while. We'll go back to our regular programming: affirmations, reflections, and the occasional honest story about what it's like to be human in the age of AI.

---

## Sequence Settings

| Setting | Value |
|---------|-------|
| Trigger | Completed welcome sequence AND NOT `paid-customer` |
| Email 1 | Day 7 after signup |
| Email 2 | Day 10 after signup |
| Email 3 | Day 14 after signup |
| Email 4 | Day 17 after signup |
| Email 5 | Day 21 after signup |
| Exit condition | `paid-customer` tag applied → remove from sequence |
| Tag on complete | `nurture-sequence-complete` |
| Tag if clicks product link | `interested-paid-product` |

## Automation Rules

```
WHEN subscriber completes welcome sequence (Day 5)
AND tag != paid-customer
THEN wait 2 days
THEN add to nurture sequence

WHEN tag paid-customer is added at any point
THEN remove from nurture sequence immediately
THEN add to post-purchase sequence
```

## Metrics to Track

- **Email 1 (Story)**: Open rate target 35%+, reply rate
- **Email 2 (Value)**: Open rate target 30%+, reply rate ("which one did you pick?")
- **Email 3 (Pitch)**: Open rate target 30%+, click rate on product link, conversion rate target 3-5%
- **Email 4 (Proof)**: Open rate target 28%+, click rate on product link
- **Email 5 (Urgency)**: Open rate target 35%+ (urgency boosts opens), conversion rate target 5-8%

## Expected Conversion

- 3-5% of nurture subscribers convert to paid
- At $12, every 100 subscribers = $36-60 revenue
- At $17, every 100 subscribers = $51-85 revenue
