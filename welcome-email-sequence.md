# 2-Email Welcome Sequence — Kit (ConvertKit)

> **Trigger**: New subscriber downloads the free "5-Day Grounding Practice"
> **Goal**: Build trust, deliver value, introduce the Emergency Grounding Kit ($9 tripwire) by email 2
> **Tone**: Personal letter energy. Warm, grounded, tender. Like writing to one person who needs to be seen.
> **From name**: Christie at Luminous Pulse
> **Lowercase rule**: All copy is lowercase per brand voice guide (except "I" and proper nouns)
>
> **Note**: The PDF is delivered instantly via Kit's incentive email on the form (separate from this sequence). The $9 Emergency Grounding Kit is also offered on the Kit thank-you page. This sequence starts after that delivery.
>
> **Important**: The meeting story (the origin story) is NOT told here — it lives in Nurture Email 1 (Day 7). This keeps the welcome sequence focused on value and relationship, and saves the emotional anchor for the nurture sequence where it drives conversion.

---

## Email 1: the practice (Day 2)

**Subject line options** (A/B test):
- A: the 2-minute practice that actually works
- B: why reading affirmations doesn't work (and what does)

**Preview text**: most people read affirmations wrong. here's the fix.

---

hey,

here's something no one tells you about affirmations:

reading them doesn't do much.

I know — that feels like a weird thing to say from someone who just gave you a grounding practice. but hear me out.

when you *read* an affirmation, your brain treats it like information. it files it away and moves on.

when you *speak* an affirmation out loud, something different happens. your brain hears your own voice making a declaration. it starts to take it more seriously. it's the difference between reading "I am held" and hearing yourself say it in your kitchen at 7am.

**the 2-minute practice:**

1. pick one affirmation from the practice
2. stand up (seriously — posture matters)
3. take one deep breath
4. say the affirmation out loud, three times, slowly
5. sit with the feeling for 30 seconds

that's it. two minutes.

try it tomorrow morning with this one:

> *"there is something in me that change cannot touch. today, I remember it."*

say it like you mean it — even if you don't yet. especially if you don't yet.

the feeling follows the words. not the other way around.

more soon,
Christie

P.S. — you're on Day 2 of the practice now. by Day 5, you'll start to notice something shift. stay with it.

---

## Email 2: the check-in + Emergency Kit (Day 5)

**Subject line options** (A/B test):
- A: how's the practice going?
- B: which grounding word stuck?

**Preview text**: a quick check-in — and something for the harder days.

---

hey,

today is Day 5 of your grounding practice. the last one.

I hope at least one of those words has found a permanent spot — your desk, your mirror, your phone wallpaper. the practice works best when the words keep finding you throughout the day, not just during the morning 2 minutes.

so — which one stuck?

for most people, it's one of these:

> *"I am whole before I open my laptop."*

> *"I am not broken for feeling anxious. I am awake in a world that is changing fast."*

> *"there is something in me that change cannot touch."*

whatever yours is — keep it close. say it when the noise gets loud. it's yours now.

**one more thing.**

the 5-day practice is a daily rhythm. but some days don't follow a rhythm. some days the news hits, or the meeting happens, or the 2am spiral starts — and you need something *right now*.

I made something for those days.

**the Emergency Grounding Kit** — 10 emergency grounding cards written for the specific moments that knock you sideways. the Slack notification. the "what are you doing next?" question. the LinkedIn scroll at midnight. plus a breathwork script and a permission slip for the hardest days.

it's $9. think of it as a first-aid kit for your nervous system.

> **[get the Emergency Grounding Kit — $9 →]** *(link to Kit Commerce product)*

if you already grabbed it from the thank-you page — you're all set. and if now's not the right time, that's completely fine. the free practice is yours forever.

either way, I'll keep showing up with more grounding words, more honest reflections, and the occasional reminder that you are not carrying this alone.

you are held,
Christie

P.S. — reply and tell me which grounding word stuck. I read every response, and it genuinely helps me know what resonates.

---

## Sequence Settings

| Setting | Value |
|---------|-------|
| Delay after signup | Email 1: 2 days |
| Delay after Email 1 | Email 2: 3 days |
| Tag on complete | `welcome-sequence-complete` |
| Tag if clicks tripwire link | `interested-tripwire` |
| Tag if purchases tripwire | `tripwire-buyer` |
| Next sequence | Nurture sequence (triggers 2 days after welcome-sequence-complete, if NOT `paid-customer`) |

## Subscriber Flow

```
Subscribe → Instant incentive email (PDF delivery via Kit form)
         → Thank-you page: $9 Emergency Grounding Kit offer (tripwire)
    ↓ 2 days
Email 1: "the 2-minute practice that actually works" (pure value)
    ↓ 3 days
Email 2: "how's the practice going?" (check-in + $9 tripwire soft pitch)
    ↓
Tag: welcome-sequence-complete
    ↓ 2 days
Nurture sequence begins (5 emails: story → value → $37 pitch → proof → urgency)
```

## Metrics to Track

- **Incentive email**: Delivery rate, PDF download clicks
- **Thank-you page tripwire**: Conversion rate (target: 5-10% of new subscribers)
- **Email 1**: Open rate (target: 45%+), reply rate
- **Email 2**: Open rate (target: 40%+), click rate on tripwire link, reply rate ("which word stuck?")
