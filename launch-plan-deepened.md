# Launch Plan: Luminous Pulse — Grounding for Displaced Tech Workers (DEEPENED)

## Enhancement Summary

**Deepened on:** February 13, 2026
**Research agents used:** 7 (Instagram growth, displaced tech worker audience, email funnel optimization, content marketing, Metricool/ManyChat/Beacons, pricing & launch strategy, Kit best practices)

### Critical Discoveries

1. **Instagram Live requires 1,000+ followers** (as of August 2025). Removed from Phase 3. Replaced with Story-based alternatives.
2. **ManyChat free plan does NOT include Kit integration.** Workaround: send DM users to Kit form directly instead of collecting email in ManyChat.
3. **No established brand serves this niche.** Zero direct competitors combining grounding/affirmation practices with tech-worker specificity. Wide-open positioning.
4. **$9 tripwire product recommended.** Insert between free lead magnet and $37 product to increase conversion 3-5x.
5. **Launch paid product at Day 40-45** (not Day 52). Nurture sequence already warms subscribers — don't let them cool off.
6. **Posting cadence revised.** Reels (primary growth) + Carousels (primary engagement) > static quote cards. Algorithm heavily rewards shares/saves over likes.
7. **LinkedIn should be a secondary platform.** 220M "Open to Work" users. Vulnerability posts routinely get 10K-100K+ impressions. Your exact audience self-identifies there.
8. **Email deliverability risk.** Kit free tier has 19.83% spam rate. Must set up DKIM/SPF/DMARC before sending any emails.
9. **430,000+ tech workers displaced since 2024** — audience is massive and growing. 873 per day in early 2026.
10. **Metricool free tier: 50 posts/month.** Adequate but requires planning. Best-time heat map is a strong free feature.

---

## Context

Luminous Pulse is a sanctuary brand for tech professionals navigating layoffs, role elimination, and career disruption. Instagram is the primary platform. Budget is under $50/month. Strong video/content creation skills. Claude Code handles copywriting, research, asset generation, and planning support.

**Target audience**: Displaced tech workers — PMs, engineers, designers, marketers (25-45) who've been laid off, fear they're next, or are watching their industry reshape itself.

> **Audience scale**: ~430,000-440,000 tech workers displaced since 2024. In early 2026, layoffs are running at ~873/day. 28.5% of 2025 layoffs were tied to AI adoption. This is a population the size of a mid-sized American city, refreshed weekly.

**Brand positioning**: Where displaced humans come to rest. Not "just upskill" advice. Not doom. Honest hope and grounding for the identity crisis underneath the career crisis.

> **Competitive advantage**: There is NO established brand specifically serving the emotional/spiritual wellness needs of displaced tech workers. Adjacent competitors (career coaches, meditation apps, outplacement firms) are either too tactical, too generic, or too corporate. Nobody is doing "grounding practices for engineers who just lost their jobs."

**Products**:
- Free: "The 5-Day Grounding Practice" (PDF, email capture via Kit form)
- **NEW — Tripwire ($9)**: "The Emergency Grounding Kit" (offered on Kit thank-you page)
- Paid: "The Luminous Pulse Practice: 30 Days of Grounding" ($27 founder's price → $37 → $47 regular)

> **Research insight**: A $9 tripwire between free and paid increases conversion 3-5x. Buyers of the $9 product are 3-5x more likely to purchase the $37 product later. At $9, it's a true impulse buy. Contents: 10 "emergency" affirmation cards, a guided breathwork script, a "Grounding Toolkit" one-pager, and a printable permission slip.

The plan maps every task to one of two owners:
- **You** — tasks requiring your creative eye, voice, decisions, and platform actions
- **Claude Code** — copywriting, research, asset generation, and planning support

---

## Tech Stack

| Tool | Cost | Purpose |
|------|------|---------|
| Kit (ConvertKit) Free | $0 | Email capture, PDF delivery (form incentive email), welcome/nurture sequences, paid product sales (Kit Commerce — 3.5% + $0.30 per sale) |
| Metricool Free | $0 | Content scheduling (50 posts/month, best-time heat map, 30-day analytics) |
| ManyChat Free | $0 | DM automation (trigger: GROUNDED). 1,000 contacts, 3 keyword triggers. **No Kit integration on free — route users to Kit form instead.** |
| Beacons Free | $0 | Link-in-bio (unlimited links, analytics. 9% fee on any product sales through Beacons — use Kit Commerce for sales instead) |
| Canva Free (or Pro $12.99) | $0-13 | Design templates |
| Vercel | $0 | Website hosting (luminouspulse.co) |
| Domain | ~$1/mo | luminouspulse.co |
| CapCut Free | $0 | Video editing |
| **Total** | **$1-14/month** | |

Reserve remaining budget for paid ads starting Day 82 ($5-10/day).

> **Platform research notes**:
> - **Metricool** is the strongest free scheduling tool in 2026 (5x more posts than Buffer free, 10x more than Later free). Includes competitor tracking and AI scheduling. Auto-publish works for feed posts, Reels, and carousels. Stories with interactive stickers require manual publish via notification.
> - **ManyChat free** does NOT include third-party integrations (Kit, Zapier, etc.). Those require Pro at $15/month. **Workaround**: Skip email collection inside ManyChat entirely. Your DM flow sends users to a Kit landing page/form link. Kit handles email capture. This costs $0.
> - **Beacons** beats Linktree (too limited) and Stan Store ($29/month). Free tier includes unlimited links, digital product sales, 50 emails/month, and real-time analytics. The 9% transaction fee means you lose $3.33 per $37 sale — so sell through Kit Commerce instead and use Beacons only as a link hub.
> - **Kit Commerce** has the lowest fees at your volume: 3.5% + $0.30 per sale ($1.60 on a $37 sale) vs. Gumroad at 10% + $0.50 ($4.20). That saves $2.60 per sale.

---

## Phase 0: Brand Foundation (Days 1-7) — MOSTLY DONE

### You Do
- [x] Brainstorm and finalize brand name (Luminous Pulse)
- [x] Claim Instagram handle (@luminouspulse) + TikTok handle
- [x] Register domain (luminouspulse.co)
- [x] Set up brand email
- [x] Choose Canva tier
- [x] Lock color palette: blue #6CB4EE, amber #F4C430, lavender #B4A7D6
- [x] Select fonts: Helvetica Neue
- [x] Set up Instagram Business account
- [x] Set up landing page (Vercel — luminouspulse.co)
- [ ] Upload Sanctuary logo as IG profile photo (`logo-ig-profile.png`)
- [ ] Update Instagram bio (use `instagram-bio-copy.md` Option 1)
- [ ] Update website with new positioning (use `brand-positioning.md`)
- [ ] Set up Beacons link-in-bio (3-5 links max: Free Practice, Paid Product, Website, About)
- [ ] **NEW**: Set up DKIM, SPF, and DMARC email authentication for luminouspulse.co domain

> **Why email authentication matters**: Kit's free tier has a 19.83% spam rate. Without DKIM/SPF/DMARC, nearly 1 in 5 of your emails may land in spam. Google, Yahoo, and Microsoft now enforce bulk sender rules — unauthenticated emails will be rejected or junked. Set this up BEFORE sending your first email. Kit provides setup instructions in their help docs.

### Claude Code Does
- [x] Write brand positioning and tagline options
- [x] Draft Instagram bio copy (keyword-optimized for displaced tech workers)
- [x] Create brand voice guide
- [x] Complete brand reframe (AI affirmations → sanctuary for displaced tech workers)
- [x] Rewrite all content pipeline files (14 files)
- [x] Generate brand logo identity ("The Sanctuary" — 4 options + IG profile version)
- [x] Generate Kit product cover images (free + paid + tripwire)
- [x] Generate content background images (sanctuary aesthetic)

---

## Phase 1: Content Stockpile (Days 8-18)

**Goal: 30+ pieces of content ready before first public post**

> **Research insight**: Quality over quantity. 3 high-quality posts per week you can sustain beats 7 mediocre ones. Accounts that show up reliably get better algorithmic distribution. The algorithm rewards consistency, not volume.

### You Do
- [ ] Film 6-8 Reels (using scripts from `reel-and-live-scripts.md`)
- [ ] Design 5-8 master Canva templates (sanctuary aesthetic — navy backgrounds, amber/blue accents)
- [ ] Create 8 carousel posts (using `carousel-slide-copy.md`) — **these are your #1 engagement driver**
- [ ] Create 15-20 static quote posts from templates
- [ ] Design Story Highlight covers (About, Practice, Free Guide, Community)
- [ ] Record 2-3 grounding meditation clips (60-90 sec)
- [ ] **NEW**: Create 10 Pinterest pin templates in Canva using brand palette (for Phase 4 launch)

### Claude Code Does
- [x] Generate 155 grounding affirmations across 5 themes
- [x] Rate affirmations for resonance/shareability
- [x] Generate captions for all 30+ posts (with CTAs)
- [x] Compile hashtag sets (6 sets of 3-5 tags each, in caption)
- [x] Build content calendar for Days 1-30
- [x] Write all carousel slide copy
- [x] Write landing page copy for lead magnet
- [x] Draft 2-email welcome sequence for Kit
- [x] Write grounding practice content (free PDF)
- [x] Identify trending Reels audio for displaced tech worker audience
- [x] **NEW**: Write $9 tripwire product content ("The Emergency Grounding Kit")

---

## Phase 2: Pre-Launch Setup (Days 19-21)

### You Do
- [ ] Seed Instagram grid with first 6-9 posts (best content first — lead with Reels and carousels)
- [x] Set up Kit (ConvertKit) free tier
- [ ] Create Kit form for lead magnet (email capture + PDF delivery via incentive email)
- [ ] **NEW**: Set up $9 tripwire on Kit Commerce (offered on thank-you page after free download)
- [ ] Create free lead magnet PDF: "The 5-Day Grounding Practice"
- [ ] Load welcome email sequence into Kit (from `welcome-email-sequence.md`)
- [ ] Connect Beacons to: Kit form (free practice), Kit Commerce (paid product), website
- [ ] Test entire funnel: Beacons → Kit form → PDF delivery → thank-you page ($9 offer) → welcome sequence
- [ ] **NEW**: Warm up sender reputation — send first emails to 5-10 engaged contacts, increase gradually over 2-4 weeks

> **Deliverability checklist**: Before sending your first email: (1) Custom domain configured (hello@luminouspulse.co, not @kit.com), (2) DKIM/SPF/DMARC authentication verified, (3) Double opt-in enabled, (4) Start with 5-10 emails/day, increase gradually. Keep spam complaints under 0.3% and bounces under 2%.

### Claude Code Does
- [x] Write Kit product description (free lead magnet)
- [x] Write lead magnet PDF content
- [x] Write social proof / credibility snippets
- [ ] Set up content scheduling in Metricool (connect Instagram Business account for auto-publish)
- [ ] Configure ManyChat DM automation (trigger: GROUNDED → sends Kit form link, NOT email collection inside ManyChat)
- [ ] Pre-schedule first 2 weeks of content (within 50 posts/month Metricool limit)
- [x] **NEW**: Write $9 tripwire product description and thank-you page copy

> **ManyChat DM flow (free tier)**:
> 1. User comments "GROUNDED" on post/reel
> 2. Public comment reply (3 variants rotated to avoid flagging)
> 3. Opening DM with button (REQUIRED by Meta — "Comment Reply" type)
> 4. User taps button → receives link to Kit form (NOT email collection in ManyChat)
> 5. Kit handles email capture + PDF delivery + welcome sequence
> 6. Smart Delay follow-up (2 hours later if link not clicked)
>
> **Why skip ManyChat email collection**: Kit integration requires ManyChat Pro ($15/month). By routing to Kit form, the entire flow stays free AND Kit handles the full funnel natively.
>
> **ManyChat free tier limits**: 1,000 contacts total (includes unsubscribed + deleted — they all count, and you can't delete on free). 3 keyword triggers. Plan strategically:
> 1. "GROUNDED" — lead magnet delivery
> 2. "PRACTICE" — paid product info
> 3. Reserve 1 for future campaigns

---

## Phase 3: Launch & Build (Days 22-51) — First 30 Active Days

**Posting cadence: 4x/week + daily Stories**

> **Research-optimized schedule** (prioritizes Reels for growth + Carousels for engagement):

| Day | Format | Content Type | Why |
|-----|--------|-------------|-----|
| Monday | Carousel (8-10 slides) | Name the Feeling / Ground Yourself | Carousels get 2.14x more interactions than single images, 22% more saves |
| Wednesday | Reel (30-60 sec) | Remember Who You Are | Reels reach 36% more users than carousels, 125% more than photos. 55% of views come from non-followers |
| Thursday | Carousel (8-10 slides) | You Are Not Alone / educational | Second carousel for deep engagement |
| Friday | Reel (15-30 sec) | The World We're Building / personal story | End week with hope |
| Daily | 1-3 Stories | Polls, grounding words, BTS, Q&As | Always include an interactive sticker (poll, quiz, slider) |

> **Posting time**: Tuesday-Thursday at 11AM-12PM local time (catches tech worker lunch break scroll). Reels at 12PM or 7PM. Sunday evening 6-8PM for reflective content.

### You Do (Daily, ~90 min)
- [ ] Post daily Story with interactive elements (poll, quiz, slider sticker — at least 1 per Story)
- [ ] Engage 20 min/day: follow niche accounts, leave thoughtful 2-3 sentence comments on tech career and healing content
- [ ] Reply to every comment and DM within 24 hours
- [ ] Review weekly analytics (Metricool dashboard)

> **Engagement priority**: The algorithm tracks conversation depth. A 3-comment back-and-forth signals more than 20 "nice!" comments. When engaging with other accounts, write substantive comments that start conversations. DM conversations are algorithmic gold.

### You Do (Weekly, ~3 hours)
- [ ] Batch create next week's posts in Canva (2 carousels + design elements for Reels)
- [ ] Film next week's 2 Reels (batch on weekends — one setup, multiple clips)
- [ ] Engage with 5-10 accounts in adjacent niches (tech career coaches, burnout therapists, mindfulness teachers)
- [ ] **NEW**: Post 1-2x/week on LinkedIn from personal account (vulnerability/validation posts about tech displacement)

> **LinkedIn research insight**: 220M people have "Open to Work" enabled — your exact audience self-identifies. Vulnerability posts ("I was in a meeting where someone said 'We'll just have AI do that part'") routinely get 50K-500K impressions. Personal profiles get 10x more reach than company pages. Start with 2-3 posts/week.

### Claude Code Does (Weekly)
- [ ] Auto-post scheduled content via Metricool
- [ ] Run comment-to-DM automation (ManyChat — "Comment GROUNDED" → Kit form link)
- [ ] Track engagement metrics weekly (Metricool 30-day analytics: reach, engagement rate, best-performing posts, saves)
- [ ] Monitor competitor activity (use Metricool's competitor tracking — free feature)
- [ ] Draft next week's captions
- [ ] Identify trending hashtags and audio weekly
- [ ] Write new batches of grounding content
- [ ] Draft weekly email newsletter content

### Day 30 Targets
| Metric | Target | How to Track |
|--------|--------|-------------|
| Followers | 100-300 | Instagram profile |
| Email subscribers | 30-75 | Kit dashboard |
| Engagement rate | 5%+ | Instagram Insights / Metricool |
| Lead magnet downloads | 20-40 | Kit analytics |
| Top post saves | 15+ saves | Instagram Insights |
| DM automation responses | Active | ManyChat dashboard |
| Tripwire sales ($9) | 3-8 | Kit Commerce |

> **Revised targets**: Research shows 100-300 followers in 30 days is realistic for a solo brand starting from zero with consistent 4x/week posting. The original 200-500 target was optimistic for organic-only growth. Focus on engagement rate (5%+) over follower count — that's the signal that matters.

> **Instagram Live removed**: As of August 2025, Instagram requires 1,000+ followers for Live. Plan Live sessions for after you hit that milestone (likely Phase 4-5). Until then, use Story videos with interactive stickers and Reels that feel Live-style (face-to-camera, conversational).

---

## Validation Checkpoint (Day 14)

Before going deeper, validate demand:
- [ ] 10+ grounding posts live with 5%+ engagement rate
- [ ] At least 30 followers from organic content
- [ ] DM automation (GROUNDED keyword) getting responses
- [ ] At least 5 email subscribers from Kit form
- [ ] If failing: adjust hooks, test different content pillars, lean into "Name the Feeling" (highest engagement potential for displaced tech workers)

> **Research-backed pivot signals**: If engagement is below 3% after 14 days, test these adjustments:
> 1. Lead with Reels over static posts (Reels get 30.81% average reach rate)
> 2. Use more specific tech language in hooks ("Another round of layoffs" > "Times are changing")
> 3. Shift from aspirational to validating content ("Your anger is valid" > "You're going to be great")
> 4. Check posting times — are you hitting the 11AM-12PM window?

---

## Phase 4: Accelerate & First Revenue (Days 40-81)

> **Moved from Day 52 to Day 40**: Research shows that waiting until Day 52 lets warm subscribers cool off. Your nurture sequence already warms people over 14 days — if someone downloads the free practice on Day 22, they're ready to buy by Day 36. Launch the paid product when you hit 50+ email subscribers and 5%+ engagement, even if that's Day 35.

### You Do
- [ ] Create paid "30-Day Luminous Pulse Practice" PDF
- [ ] Set up Kit Commerce product page (from `kit-paid-product-description.md`)
- [ ] **REVISED**: Launch at **$27 founder's price** (move to $37 after 30 sales or 60 days, then $47)
- [ ] **NEW**: Recruit 5-10 beta testers before launch (give free access, collect testimonials)
- [ ] Film talking-head Reels (personal story, founder journey, the meeting story)
- [ ] Launch 7-day grounding challenge (IG Stories — #GroundedIn7)
- [ ] DM outreach to 20 micro-influencers (healing/wellness/anxiety/tech layoff niche)
- [ ] Review and double down on top 3 content formats
- [ ] **NEW**: Start podcast guesting outreach (5-10 pitches/week to tech career, wellness, and creator podcasts)

> **Pricing research**: $37 for a PDF from an unknown brand with no social proof is a friction point. $27 is the "no-brainer threshold" for digital wellness products from new creators. Three price-anchor opportunities: $27 founder's → $37 after 30 sales → $47 regular. The $10 gap between tiers is meaningful (27% increase) without feeling manipulative.
>
> Do NOT use charm pricing ($26.99). In the wellness/healing space, round or specific whole numbers signal authenticity. "$27" feels intentional; "$26.99" feels like a sales gimmick.

> **Beta tester strategy**: Give the 30-day practice to 5-10 engaged followers before launch. Ask specific questions: "What did Day 7's affirmation make you feel?" Even 3 genuine testimonials transform your conversion rate. Send this DM: "I'm creating something and wanted to share it with you first. Would you be open to trying the full 30-day practice and telling me what you think?"

> **Authentic urgency that works for a healing brand**:
> - "Founder's pricing ends [specific date]" (real deadline, real reason)
> - "The first 25 people get a bonus guided meditation" (limited bonus, unlimited product)
> - "I'm launching at $27. After [date], it goes to $37 — as I add guided audio and community features, the price reflects that."
> - NEVER: fake countdown timers, "Only 3 spots left!" for a digital download, guilt-based framing

### Claude Code Does
- [x] Write 30-Day Practice content (paid product)
- [x] Write Kit Commerce product page copy ($37)
- [x] Draft 5-email nurture sequence (conversion)
- [ ] **NEW**: Write $9 tripwire content ("The Emergency Grounding Kit")
- [ ] Create 3 variations of top-performing posts
- [ ] Expand to Pinterest (5-8 pins/day via Tailwind or manual scheduling)
- [ ] Generate weekly analytics reports
- [x] Draft influencer outreach DM templates
- [x] Write SEO blog posts (Tier 3 long-tail keywords first — see SEO section below)
- [x] **NEW**: Draft LinkedIn posts (10 posts — vulnerability + validation + data-insight formats)
- [x] **NEW**: Write podcast guest one-sheet (bio, 3 topic pitches, talking points, outreach DM template)

> **SEO blog priority (Tier 3 long-tail keywords — lowest competition, your niche sweet spot)**:
> - "affirmations after getting laid off" (100-500 monthly searches, very low competition)
> - "tech layoff mental health" (500-2,000 monthly searches, low competition)
> - "identity crisis after job loss" (200-800 monthly searches, very low competition)
> - "grounding exercises for career anxiety" (100-500 monthly searches, very low competition)
> - Target 1 blog post/week, 1,500-2,500 words, each with lead magnet CTA

### Day 60 Targets
| Metric | Target |
|--------|--------|
| Followers | 500-1,500 |
| Email subscribers | 100-300 |
| Revenue (paid product) | $100-500 |
| Tripwire revenue ($9) | $50-200 |
| Beta tester testimonials | 3-5 collected |
| Influencer collab | 1 completed |
| Podcast appearances | 1-2 recorded |

> **Realistic funnel math at Day 60**:
> | Stage | Number | Rate |
> |-------|--------|------|
> | Landing page visitors | 500-1,000 | — |
> | Email subscribers | 100-250 | 20-25% opt-in |
> | Tripwire buyers ($9) | 10-25 | 10% of subscribers |
> | Complete 5-day practice | 40-100 | 40% engagement |
> | Purchase 30-Day Practice ($27-37) | 5-15 | 5-8% of subscribers |
> | Revenue | $225-$780 | Tripwire + paid product |

---

## Phase 5: Scale & Expand (Days 82-111)

### You Do
- [ ] Move paid product to $37 (if still at founder's $27 price)
- [ ] Start paid ads ($5-10/day on top-performing Reels)
- [ ] Launch weekly email newsletter
- [ ] Plan TikTok launch (repurpose existing Reels — same format, re-export with TikTok captions)
- [ ] **NEW**: Host first Instagram Live (now that you should be near or past 1,000 followers)
- [ ] Scope YouTube channel (longer grounding meditations)
- [ ] Evaluate community options (Discord or Circle)

> **Paid ads research (start only after you have a converting funnel)**:
> - Objective: Lead generation (email sign-ups for free grounding guide)
> - Use your best-performing organic Reel as your first ad creative (proven engagement)
> - Target: Interest-based (mindfulness, meditation, career development, anxiety management) + demographics (28-45, US/Canada/UK, tech careers)
> - Expected: $0.60-$2.50 cost per lead, 30-180 email sign-ups per month at $150-300/month spend
> - Kill any ad with CPL above $5 after 3 days of data
> - Hook in first 2 seconds: "If you were laid off from tech, hear this..."

### Claude Code Does
- [ ] Optimize ad targeting and budget
- [ ] Full content repurposing pipeline (IG → TikTok → Pinterest → Blog → Email)
- [ ] Automate email newsletter scheduling
- [ ] SEO monitoring and keyword tracking (move to Tier 2 keywords)
- [ ] Competitor pricing and product analysis
- [ ] Write ad copy variations (5-10 versions)
- [ ] Write TikTok captions
- [ ] **NEW**: Build "The Complete Sanctuary" bundle ($67 — 30-Day Practice + affirmation card deck + guided audio + journaling template)

> **Content repurposing pipeline ("One-to-Seven" system)**:
> ```
> ANCHOR: 5-min talking-head video on weekly topic
>     ├── Instagram Reel (60-90 sec highlight)
>     ├── TikTok (same clip, re-exported)
>     ├── Instagram Carousel (key points as slides)
>     ├── Pinterest Pin (infographic, links to blog)
>     ├── Blog Post (1,500-word SEO article)
>     ├── Email Newsletter (personal angle + blog link + product CTA)
>     ├── Instagram Stories (3-5 Stories breaking down each point)
>     └── Quote Graphics x3 (pull best one-liners)
> ```

### Day 90 Targets
| Metric | Target |
|--------|--------|
| Followers | 1,500-3,500 |
| Email subscribers | 300-750 |
| Revenue (cumulative 90 days) | $1,000-$2,600 |
| Paid product | Live on Kit Commerce at $37 |
| TikTok | Active (repurposing Reels) |
| Pinterest | 50+ pins live |
| Blog posts | 8-12 published |

> **Realistic 90-day revenue breakdown**:
> | Source | Conservative | Optimistic |
> |--------|-------------|------------|
> | Tripwire ($9) | $450 (50 sales) | $1,000 (112 sales) |
> | Paid product ($27-37) | $540 (20 sales) | $1,480 (40 sales) |
> | **Total** | **$990** | **$2,480** |
>
> The real value of the first 90 days is not revenue — it is validation, email list building, and social proof that compounds in months 4-6.

---

## Revenue Model

```
Free Lead Magnet (5-Day Practice) → Kit form email capture
    ↓
Thank-you page: $9 Tripwire ("Emergency Grounding Kit") — expect 10-15% conversion
    ↓
Welcome sequence (2 emails over 5 days)
    ↓
Nurture sequence (5 emails over 14 days)
    ↓
~5-8% convert to Paid ($27 founder's → $37 → $47 regular)
```

**Revenue projections at scale:**

| Subscribers | Tripwire Revenue (10-15%) | Paid Revenue (5-8%) | Total |
|-------------|--------------------------|---------------------|-------|
| 100 | $90-$135 | $135-$296 | $225-$431 |
| 500 | $450-$675 | $675-$1,480 | $1,125-$2,155 |
| 1,000 | $900-$1,350 | $1,350-$2,960 | $2,250-$4,310 |

> **Email subject line patterns that work for this niche**:
> - Curiosity + benefit: "The 2-minute practice that changed everything"
> - Direct self-interest: "Your body is holding stress from your last job"
> - Specificity: "Day 1 of 5: The ground beneath your feet"
> - Personal/intimate: "When I lost my tech job, this saved me"
> - Keep under 50 characters. Wellness audiences reward authenticity over polish.

> **A/B test priorities** (once you have 200+ subscribers):
> 1. Subject lines on Nurture Email 3 (the soft pitch) — this determines how many people see the offer
> 2. CTA button text on Nurture Email 5 ("Start My 30-Day Practice" vs "Get the Full Practice for $27")
> 3. Send timing on pitch emails (morning 9AM vs late afternoon 5PM)

---

## Audience Emotional Journey (Content Mapping)

> Research mapped the post-layoff experience to 7 stages. Map your content to where your audience IS emotionally:

| Stage | Timeframe | Experience | Best Content |
|-------|-----------|-----------|-------------|
| **Shock** | Days 0-3 | Numbness, "did this really happen?" | Gentle grounding. "You don't need a plan today." Breathing exercises. |
| **Denial & Anger** | Week 1-2 | Rage at employer. Checking Blind obsessively. | Validation. "Your anger is valid." Honor the emotion. |
| **Bargaining** | Weeks 2-4 | "Could I have done more?" Imposter syndrome. | Counter-narrative. "Your layoff is not a performance review." |
| **Identity Crisis** | Months 1-3 | "Who am I without my title?" Deepest valley. | **Your sweet spot.** Daily affirmation sequences, grounding meditations, community. |
| **Acceptance** | Months 3-6 | Separating worth from employer. Exploring. | Forward-looking. "I am becoming." Vision-setting. |
| **Reconstruction** | Months 6+ | New identity forming. | Integration. Premium products, workshops. |

---

## Their Language (Use This in All Copy)

> **Exact words displaced tech workers use** (from Reddit, Blind, LinkedIn, Hacker News):

**About the experience:**
- "I got the tap on the shoulder" / "I was impacted"
- "I found out through a Slack message"
- "I gave them everything" / "After everything I did for this company"

**About identity:**
- "Who am I without my job?"
- "I don't know what I'm doing with my life"
- "I feel like a failure"
- "My whole identity was wrapped up in that role"

**About imposter syndrome:**
- "Maybe I wasn't good enough"
- "I keep downgrading what I apply for"
- "I'm starting to question everything"

**About the search:**
- "I've sent 200 applications" / "Radio silence"
- "The market is brutal" / "I feel invisible"
- "Is tech even a good career anymore?"

**Language rules:**
- Use their words, not wellness jargon. "If you feel invisible right now" > "align your chakras"
- Mirror the rawness. "Your layoff was not a performance review" > "release what no longer serves you"
- Name specific tech experiences: Slack notifications, badge access revoked, "Open to Work" badge, LeetCode, TC culture
- Avoid toxic positivity. "Everything happens for a reason" will alienate. "This is hard and you are allowed to feel that" will connect.

| Use This | Not This |
|----------|----------|
| "The Slack message came on a Tuesday" | "Life throws curveballs" |
| "Your worth is not your TC" | "You are worthy" (generic) |
| "If you're refreshing LinkedIn at 2am" | "If you're struggling" (vague) |
| "Your layoff was not a performance review" | "Everything happens for a reason" |
| "Breathe first. Plan later." | "Just upskill" / "Pivot" |

---

## Key Timing Opportunities

> Layoffs cluster predictably. Plan content launches and campaigns around these waves:
> - **January**: New fiscal year layoffs (major wave)
> - **Q2 earnings season**: Post-earnings restructuring
> - **October**: Historically worst month for tech layoffs (153,074 cuts in Oct 2025)
> - **Within 48 hours of any major layoff announcement**: Post validating content. "If you were affected by [Company]'s layoff this week — breathe first."

---

## What to Do First (This Week)

1. **Today**: Upload Sanctuary logo as IG profile photo
2. **Today**: Update Instagram bio with displaced tech worker positioning
3. **Today**: Update website (luminouspulse.co) with new hero copy
4. **Today**: Set up DKIM/SPF/DMARC email authentication for luminouspulse.co
5. **Day 2**: Set up Kit form for lead magnet with incentive email PDF delivery
6. **Day 2**: Set up $9 tripwire on Kit Commerce thank-you page
7. **Day 3**: Create the 5-Day Grounding Practice PDF
8. **Day 4-5**: Design Canva templates and start creating grid posts
9. **Day 6-7**: Film first batch of Reels

---

## Monthly Budget Allocation ($50)

| Item | Cost | When |
|------|------|------|
| Domain (luminouspulse.co) | ~$1 | Ongoing |
| Canva Pro (optional) | $0-13 | Phase 1+ |
| Everything else | $0 | Phases 0-4 |
| Paid ads (reserve) | $36-49 | Phase 5 (Day 82+) |
| **ManyChat Pro upgrade** | **$15** | **Only when approaching 800+ contacts or when Kit integration becomes necessary** |
