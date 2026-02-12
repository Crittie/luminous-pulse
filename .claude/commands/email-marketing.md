# Email Marketing Automation — Luminous Pulse

Handle all email marketing tasks for the Luminous Pulse brand using Kit (ConvertKit). This includes setting up sequences, writing emails, configuring automations, managing subscribers, and optimizing the funnel from lead magnet to paid product.

## Brand Context

- **Brand**: Luminous Pulse — AI-age affirmation brand
- **Creator**: Christie Parrow
- **Voice**: Direct, warm, grounded. Like a smart friend who gets it.
- **Lead Magnet**: "7 Affirmations for the AI Age" free PDF card deck
- **Paid Product (Phase 4)**: 50 Affirmations for the AI Age ($9-17)
- **Signature Product (Phase 5)**: Premium guide/course ($27-47)
- **Instagram**: @luminouspulse.co
- **Website**: luminouspulse.co

## Kit (ConvertKit) Setup

### Account Configuration
- **Plan**: Free tier (up to 10,000 subscribers)
- **From name**: Christie at Luminous Pulse
- **From email**: Use the brand email set up in Phase 0
- **Reply-to**: Same as from email (personal replies encouraged)

### Required Forms
1. **Lead Magnet Opt-in** — embedded on Gumroad ($0 product) and link-in-bio
   - Trigger: Delivers "7 Affirmations for the AI Age" PDF
   - Tag: `lead-magnet-downloaded`
   - Automation: Starts welcome sequence

2. **Newsletter Signup** — for website/Instagram bio
   - Tag: `newsletter-subscriber`
   - Automation: Starts welcome sequence (skip if already in it)

3. **Paid Customer** — triggered by Gumroad webhook
   - Tag: `paid-customer`
   - Automation: Removes from nurture sequence, adds to customer sequence

### Required Tags
```
lead-magnet-downloaded
newsletter-subscriber
paid-customer
engaged-subscriber (opened 3+ emails)
unengaged (no opens in 30 days)
theme-career (clicked career content)
theme-anxiety (clicked anxiety content)
theme-morning (clicked morning content)
theme-empowerment (clicked empowerment content)
```

### Required Segments
- **All subscribers** — everyone
- **Warm leads** — `lead-magnet-downloaded` AND `engaged-subscriber` AND NOT `paid-customer`
- **Cold leads** — `lead-magnet-downloaded` AND `unengaged`
- **Customers** — `paid-customer`

## Email Sequences

### Sequence 1: Welcome (3 emails, Days 0-4)
**File**: `/Users/christieparrow/affirmations-project/email-welcome-sequence.md`
**Trigger**: `lead-magnet-downloaded` tag applied
**Timing**: Day 0, Day 2, Day 4

| Email | Subject | Goal |
|-------|---------|------|
| 1 (Day 0) | Your 7 affirmations are here | Deliver PDF, set expectations, introduce brand |
| 2 (Day 2) | The one affirmation that changes everything | Build connection, share personal story |
| 3 (Day 4) | You're not behind (read this today) | Deepen trust, tease paid product |

### Sequence 2: Nurture / Conversion (5 emails, Days 7-21)
**File**: To be created in Phase 4
**Trigger**: Completed welcome sequence AND NOT `paid-customer`
**Timing**: Day 7, Day 10, Day 14, Day 17, Day 21

| Email | Subject | Goal |
|-------|---------|------|
| 1 (Day 7) | What I wish someone told me about AI anxiety | Story-driven, build authority |
| 2 (Day 10) | 3 affirmations for your work week | Value-first, themed content |
| 3 (Day 14) | The full collection is here | Soft pitch for paid product |
| 4 (Day 17) | "I didn't think affirmations were for me" | Social proof / testimonial |
| 5 (Day 21) | Last chance: your affirmation deck | Direct pitch, urgency |

### Sequence 3: Weekly Newsletter (ongoing, Phase 3+)
**Trigger**: Manual send every Monday 7am EST
**Format**:
```
Subject: [Affirmation] + [1-line hook]

1. Affirmation of the Week (from affirmations-150.md)
2. 2-3 sentence reflection / story
3. Quick tip or prompt
4. CTA: Save this / Share / Reply with yours
5. PS: Link to lead magnet or paid product
```

### Sequence 4: Post-Purchase (Phase 4+)
**Trigger**: `paid-customer` tag applied
**Timing**: Immediately, Day 3, Day 7

| Email | Subject | Goal |
|-------|---------|------|
| 1 (Immediate) | Your 50 affirmations are ready | Deliver product, usage tips |
| 2 (Day 3) | How to get the most from your deck | Retention, reduce refunds |
| 3 (Day 7) | You're part of something bigger | Community invite, review ask |

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
AND send re-engagement email ("Still there?")
WAIT 7 days
IF no open THEN unsubscribe (keep list clean)
```

### Rule 5: Interest Tagging
```
WHEN subscriber clicks link containing "career"
THEN add tag theme-career

WHEN subscriber clicks link containing "anxiety"
THEN add tag theme-anxiety
```

## Gumroad → Kit Integration

### Free Lead Magnet ($0 product)
1. Create Gumroad product with $0 price, require email
2. In Gumroad → Settings → Integrations → connect Kit
3. Map purchase to `lead-magnet-downloaded` tag
4. Kit automation triggers welcome sequence

### Paid Product ($9-17)
1. Create Gumroad product with price
2. Map purchase to `paid-customer` tag
3. Kit automation removes from nurture, starts post-purchase

## Writing Guidelines

### Subject Lines
- Keep under 50 characters
- Use lowercase (matches brand voice)
- Lead with the affirmation or a question
- No clickbait, no ALL CAPS, no excessive punctuation
- Examples:
  - "your monday affirmation"
  - "the skill no one talks about"
  - "you're not behind"
  - "I needed to hear this today"

### Email Body
- **Tone**: Like a letter from a friend, not a newsletter
- **Length**: 150-300 words max
- **Structure**: Hook → Story/Value → CTA
- **Formatting**: Short paragraphs (1-2 sentences), plenty of whitespace
- **Signoff**: "Your humanity is your superpower. — Christie"
- **PS line**: Always include — highest-read part of any email

### CTAs
- Soft: "Reply and tell me..." / "Save this for later"
- Medium: "Grab your free guide" / "Read more on Instagram"
- Direct: "Get the full collection" / "Start your practice today"

## File References

| Asset | Location |
|-------|----------|
| Welcome sequence copy | `/Users/christieparrow/affirmations-project/email-welcome-sequence.md` |
| Lead magnet PDF | `/Users/christieparrow/affirmations-project/7-affirmations-lead-magnet.pdf` |
| Gumroad product copy | `/Users/christieparrow/affirmations-project/gumroad-product-description.md` |
| 162 affirmations | `/Users/christieparrow/affirmations-project/affirmations-150.md` |
| Nurture sequence (Phase 4) | To be created |
| Newsletter templates (Phase 3) | To be created |

## Task Checklist

When this skill is invoked, check which phase the user is in and suggest the relevant next steps:

### Phase 2 (Pre-Launch)
- [ ] Create Kit free account
- [ ] Set up lead magnet opt-in form
- [ ] Load 3-email welcome sequence
- [ ] Connect Gumroad → Kit for lead magnet
- [ ] Test: download lead magnet → receive email 1 → receive email 2 → receive email 3

### Phase 3 (Launch)
- [ ] Start weekly newsletter (Mondays 7am EST)
- [ ] Set up engagement tagging automation
- [ ] Monitor open rates (target: 40%+ for welcome, 25%+ for newsletter)
- [ ] Write 4 weeks of newsletter content

### Phase 4 (Revenue)
- [ ] Write 5-email nurture/conversion sequence
- [ ] Connect Gumroad paid product → Kit
- [ ] Set up purchase → exit nurture automation
- [ ] Write 3-email post-purchase sequence
- [ ] Set up re-engagement automation for cold subscribers

### Phase 5 (Scale)
- [ ] Segment by interest tags for targeted sends
- [ ] A/B test subject lines (Kit supports this on paid plan)
- [ ] Evaluate upgrade to Kit paid plan if approaching 10K subscribers
- [ ] Set up automated newsletter scheduling

## Quick Commands

```bash
# Check existing email assets
ls ~/affirmations-project/email-*

# Read welcome sequence
cat ~/affirmations-project/email-welcome-sequence.md

# Read affirmations for newsletter content
cat ~/affirmations-project/affirmations-150.md
```
