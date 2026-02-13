# 2-Email Welcome Sequence — Kit (ConvertKit)

> **Trigger**: New subscriber downloads the free "5-Day Grounding Practice"
> **Goal**: Build trust, deliver value, introduce paid product by email 2
> **Tone**: Personal letter energy. Warm, grounded, tender. Like writing to one person who needs to be seen.
> **From name**: Christie at Luminous Pulse
>
> **Note**: The PDF is delivered instantly via Kit's incentive email on the form (separate from this sequence). This sequence starts after that delivery.

---

## Email 1: The Practice (Day 2)

**Subject line options** (A/B test):
- A: The 2-minute practice that actually works
- B: Why reading affirmations doesn't work (and what does)

**Preview text**: Most people read affirmations wrong. Here's the fix.

---

Hey,

Here's something no one tells you about affirmations:

Reading them doesn't do much.

I know — that feels like a weird thing to say from someone who just gave you a grounding practice. But hear me out.

When you *read* an affirmation, your brain treats it like information. It files it away and moves on.

When you *speak* an affirmation out loud, something different happens. Your brain hears your own voice making a declaration. It starts to take it more seriously. It's the difference between reading "I am held" and hearing yourself say it in your kitchen at 7am.

**The 2-minute practice:**

1. Pick one affirmation from the practice
2. Stand up (seriously — posture matters)
3. Take one deep breath
4. Say the affirmation out loud, three times, slowly
5. Sit with the feeling for 30 seconds

That's it. Two minutes.

Try it tomorrow morning with this one:

> *"There is something in me that change cannot touch. Today, I remember it."*

Say it like you mean it — even if you don't yet. Especially if you don't yet.

The feeling follows the words. Not the other way around.

More soon,
Christie

P.S. — In my next email, I'll tell you about the extended practice — 30 days of grounding for uncertain times. It's the thing I'm most proud of building.

---

## Email 2: The Story + Soft Pitch (Day 5)

**Subject line options** (A/B test):
- A: The night I almost didn't build this
- B: What happened after the meeting that changed everything

**Preview text**: The honest story behind this project — and what's next.

---

Hey,

I want to tell you a quick story.

Last year, I was in a meeting where someone casually said, "We'll just have AI do that part." They were talking about the part of the project I was most proud of.

I didn't say anything in the moment. But that night, I sat with this heavy, unnamed feeling — like my skills had an expiration date no one told me about.

And here's what I figured out over the next few weeks: the spiral wasn't about AI. It was about identity. I had tied my worth to my output — and when a machine matched my output, I didn't know who I was without it.

That's the real crisis nobody talks about. It's not a skills gap. It's an identity gap.

The grounding words I write aren't about ignoring AI or pretending it doesn't matter. They're about **coming home to what's true about you underneath what you produce.** Your ability to love, to care, to sit with someone in silence and make them feel less alone. The stuff that no update, no model, no algorithm will ever touch.

That's what this is about. Not fighting technology. Not pretending everything is fine. Just... remembering.

If the 5-day practice helped you find even a moment of stillness, I built something deeper:

**The Luminous Pulse Practice: 30 Days of Grounding for Uncertain Times**

> **[Link to Kit Commerce product page]**

It's $37 — 30 days of grounding affirmations, reflection prompts, breathwork, and journaling questions designed to move you from anxiety to agency. From fear to grounded hope.

But honestly? If the free practice is enough for you, I'm happy. This project started because I needed these words. If even one of them landed for you, that's the whole point.

Either way, I'll keep showing up in your inbox with more grounding words, more real talk about navigating this moment, and the occasional reminder that your humanity is not the problem — it is the answer.

Thanks for being here.

You are held,
Christie

P.S. — If the free practice helped, I'd love to hear which grounding word stuck. Just reply to this email. I read every response.

---

## Sequence Settings

| Setting | Value |
|---------|-------|
| Delay after signup | Email 1: 2 days |
| Delay after Email 1 | Email 2: 3 days |
| Tag on complete | `welcome-sequence-complete` |
| Tag if clicks paid link | `interested-paid-product` |
| Next sequence | Weekly newsletter (starts Day 22 of launch) |

## Subscriber Flow

```
Subscribe → Instant incentive email (PDF delivery, handled by Kit form)
    ↓ 2 days
Email 1: "The 2-minute practice that actually works"
    ↓ 3 days
Email 2: "The night I almost didn't build this" (soft pitch)
    ↓
Tag: welcome-sequence-complete → enters weekly newsletter
```

## Metrics to Track

- **Incentive email**: Delivery rate, PDF download clicks
- **Email 1**: Open rate (target: 45%+), reply rate
- **Email 2**: Open rate (target: 40%+), click rate on product link, conversion rate (target: 3-5%)
