# Email Marketing Automation — Luminous Pulse

Handle all email marketing tasks for the Luminous Pulse brand using Kit (ConvertKit). This includes setting up sequences, writing emails, configuring automations, managing subscribers, and optimizing the funnel from lead magnet to paid product.

## Brand Context

- **Brand**: Luminous Pulse — sanctuary for displaced workers
- **Creator**: Christie Parrow
- **Voice**: Direct, warm, grounded. Like a smart friend who gets it.
- **Positioning**: Where anxious humans come to rest. Grounding for displaced workers in uncertain times.
- **Lead Magnet**: "The 5-Day Grounding Practice" free PDF (email capture via Kit form)
- **Tripwire Product**: "The Emergency Grounding Kit" ($9)
- **Paid Product**: "The 30-Day Luminous Pulse Practice" ($37 launch / $47 regular)
- **Instagram**: @luminouspulse.co
- **Website**: luminouspulse.co

## Kit (ConvertKit) Setup

### Account Configuration
- **Plan**: Free tier (up to 10,000 subscribers)
- **From name**: Christie at Luminous Pulse
- **From email**: Use the brand email
- **Reply-to**: Same as from email (personal replies encouraged)

### Required Forms
1. **Lead Magnet Opt-in** — embedded on website and link-in-bio (Beacons)
   - Kit Form ID: `7f9bdedb95`
   - Form action: `https://app.kit.com/forms/9081984/subscriptions`
   - Trigger: Delivers "The 5-Day Grounding Practice" PDF
   - Tag: `lead-magnet-downloaded`
   - Automation: Starts welcome sequence

2. **Newsletter Signup** — for website/Instagram bio
   - Tag: `newsletter-subscriber`
   - Automation: Starts welcome sequence (skip if already in it)

3. **Paid Customer** — triggered by Kit Commerce
   - Tag: `paid-customer`
   - Automation: Removes from nurture sequence, adds to customer sequence

### Required Tags
```
lead-magnet-downloaded
newsletter-subscriber
paid-customer
tripwire-customer
engaged-subscriber (opened 3+ emails)
unengaged (no opens in 30 days)
theme-grounding (clicked grounding content)
theme-breathwork (clicked breathwork content)
theme-identity (clicked identity/career content)
theme-somatic (clicked body-based content)
```

### Required Segments
- **All subscribers** — everyone
- **Warm leads** — `lead-magnet-downloaded` AND `engaged-subscriber` AND NOT `paid-customer`
- **Cold leads** — `lead-magnet-downloaded` AND `unengaged`
- **Customers** — `paid-customer` OR `tripwire-customer`

## Email Sequences

### Incentive Email (Instant — PDF Delivery)
**Trigger**: Kit form submission confirmed
**Timing**: Immediately after double opt-in

Subject: `your grounding practice is here`

Body:
```
Hey — welcome to Luminous Pulse.

Your free 5-Day Grounding Practice is ready. Download it below and start with Day 1 whenever you're ready — it takes less than 5 minutes.

[Download button — auto-inserted by Kit]

This practice was built for the moment you're in right now — the uncertainty, the displacement, the constant recalibration. It's not about fixing you. It's about landing you.

Over the next few days, I'll send you a couple of things that have helped me and hundreds of others navigate this same terrain. Nothing spammy — just real talk.

You're not behind. You're becoming.
— Christie

PS: If one of the daily practices hits different, reply and tell me which one. I read every reply.
```

### Sequence 1: Welcome (2 emails, Days 2-5)
**File**: `/Users/christieparrow/affirmations-project/welcome-email-sequence.md`
**Trigger**: `lead-magnet-downloaded` tag applied
**Timing**: Day 2, Day 5

| Email | Subject | Goal |
|-------|---------|------|
| 1 (Day 2) | the 2-minute practice that actually works | Build connection, share a grounding technique |
| 2 (Day 5) | the night I almost didn't build this | Deepen trust, soft pitch to $37 product |

### Sequence 2: Nurture / Conversion (5 emails, Days 7-21)
**File**: `/Users/christieparrow/affirmations-project/email-nurture-sequence.md`
**Trigger**: Completed welcome sequence AND NOT `paid-customer`
**Timing**: Day 7, Day 10, Day 14, Day 17, Day 21

| Email | Subject | Goal |
|-------|---------|------|
| 1 (Day 7) | the identity crisis no one warns you about | Story-driven, build authority |
| 2 (Day 10) | 3 grounding practices for your hardest days | Value-first, technique content |
| 3 (Day 14) | what if the pause is the point? | Reframe displacement as transformation |
| 4 (Day 17) | "I didn't think breathing could change anything" | Social proof / testimonial |
| 5 (Day 21) | your 30-day practice is ready | Direct pitch for $37 product |

### Sequence 3: Weekly Newsletter (ongoing)
**Trigger**: Manual send every Monday 7am EST
**Format**:
```
Subject: [affirmation] + [1-line hook]

1. Affirmation of the Week (from affirmations-150.md)
2. 2-3 sentence reflection / grounding insight
3. Technique of the week (from healing-practices-reference-guide.md)
4. CTA: Save this / Share / Reply with yours
5. PS: Link to lead magnet or paid product
```

### Sequence 4: Post-Purchase
**Trigger**: `paid-customer` tag applied
**Timing**: Immediately, Day 3, Day 7

| Email | Subject | Goal |
|-------|---------|------|
| 1 (Immediate) | your 30-day practice is ready | Deliver product, Day 1 guidance |
| 2 (Day 3) | how to make this practice stick | Retention, reduce refunds |
| 3 (Day 7) | you're part of something bigger | Community building, review ask |

## Automation Rules

### Rule 1: Welcome → Nurture Pipeline
```
WHEN subscriber completes Welcome Sequence
AND tag != paid-customer
THEN add to Nurture Sequence
```

### Rule 2: Purchase Exits Nurture
```
WHEN tag paid-customer is added
THEN remove from Nurture Sequence
AND add to Post-Purchase Sequence
```

### Rule 3: Engagement Tagging
```
WHEN subscriber opens 3+ emails in 14 days
THEN add tag engaged-subscriber
```

### Rule 4: Re-engagement
```
WHEN subscriber has not opened email in 30 days
THEN add tag unengaged
AND send re-engagement email ("still there?")
WAIT 7 days
IF no open THEN unsubscribe (keep list clean)
```

### Rule 5: Interest Tagging
```
WHEN subscriber clicks link containing "grounding"
THEN add tag theme-grounding

WHEN subscriber clicks link containing "breathwork"
THEN add tag theme-breathwork

WHEN subscriber clicks link containing "identity" OR "career"
THEN add tag theme-identity
```

## Automatic Lead Magnet Delivery

### How It Works
When a new subscriber signs up via the Kit form (on website or Beacons link-in-bio), they immediately receive the "5-Day Grounding Practice" PDF via Kit's incentive email feature.

### Setup Steps
1. Go to **Kit → Grow → Landing Pages & Forms**
2. Select the lead magnet opt-in form (ID: `7f9bdedb95`)
3. Click **Settings** (gear icon) on the form
4. Under **Incentive**, toggle **Send incentive email** ON
5. **Upload the PDF**: `5-Day-Grounding-Practice.pdf`
6. Customize the incentive email (see copy above)
7. Click **Save**

### Testing the Delivery Flow
1. Subscribe with a test email → confirm double opt-in → should receive incentive email with PDF link within 60 seconds
2. Verify Welcome Email 1 arrives on Day 2
3. Check Kit dashboard → subscriber should have `lead-magnet-downloaded` tag applied
4. Verify full funnel: Beacons → Kit form → PDF → welcome emails → nurture emails

## Writing Guidelines

### Subject Lines
- Keep under 50 characters
- Use lowercase (matches brand voice)
- Lead with the practice or a feeling
- No clickbait, no ALL CAPS, no excessive punctuation
- Examples:
  - "your monday grounding practice"
  - "the pause that changes everything"
  - "you're not behind"
  - "when the ground disappears"

### Email Body
- **Tone**: Like a letter from a friend, not a newsletter
- **Length**: 150-300 words max
- **Structure**: Hook → Story/Value → CTA
- **Formatting**: Short paragraphs (1-2 sentences), plenty of whitespace
- **Signoff**: "You're not behind. You're becoming. — Christie"
- **PS line**: Always include — highest-read part of any email

### CTAs
- Soft: "Reply and tell me..." / "Save this for later"
- Medium: "Try this 2-minute practice" / "Read more on Instagram"
- Direct: "Start your 30-day practice" / "Get grounded today"

## File References

| Asset | Location |
|-------|----------|
| Welcome sequence copy | `welcome-email-sequence.md` |
| Nurture sequence copy | `email-nurture-sequence.md` |
| Lead magnet PDF | `5-Day-Grounding-Practice.pdf` |
| Lead magnet PDF content | `lead-magnet-pdf-content.md` |
| Kit product descriptions | `kit-product-description.md`, `kit-paid-product-description.md`, `kit-tripwire-product-description.md` |
| 155 affirmations | `affirmations-150.md` |
| Healing practices guide | `healing-practices-reference-guide.md` |

## Task Checklist

### Pre-Launch (Now)
- [ ] Set up Kit lead magnet opt-in form with incentive email
- [ ] Upload 5-Day Grounding Practice PDF to Kit
- [ ] Load 2-email welcome sequence
- [ ] Load 5-email nurture sequence
- [ ] Test full funnel: form → PDF delivery → welcome → nurture
- [ ] Set up ManyChat DM automation (trigger: GROUNDED)

### Launch (Feb 17)
- [ ] Start weekly newsletter (Mondays 7am EST)
- [ ] Set up engagement tagging automation
- [ ] Monitor open rates (target: 40%+ for welcome, 25%+ for newsletter)
- [ ] Write 4 weeks of newsletter content

### Month 2 (Revenue)
- [ ] Set up Kit Commerce for $37 paid product
- [ ] Set up $9 tripwire product
- [ ] Connect purchase → exit nurture automation
- [ ] Write 3-email post-purchase sequence
- [ ] Set up re-engagement automation for cold subscribers

### Month 3+ (Scale)
- [ ] Segment by interest tags for targeted sends
- [ ] A/B test subject lines
- [ ] Evaluate upgrade to Kit paid plan if approaching 10K subscribers
