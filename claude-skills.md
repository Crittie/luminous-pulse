# Claude Skills — Luminous Pulse Project

> What Claude Code currently does for this project, and skills available to accelerate growth.
>
> **Last updated:** February 13, 2026

---

## Currently Active Skills

These are things Claude Code does right now for Luminous Pulse.

### 1. Copywriting & Content Generation
**What it does**: Writes all brand copy — affirmations, captions, email sequences, product descriptions, blog posts, carousel scripts, Reel scripts, LinkedIn posts, podcast pitches, influencer outreach DMs.
**Files produced**: `post-captions.md`, `carousel-slide-copy.md`, `reel-and-live-scripts.md`, `welcome-email-sequence.md`, `email-nurture-sequence.md`, `linkedin-posts.md`, `influencer-outreach-templates.md`, `blog-post-1/2/3-*.md`, all Kit product descriptions.
**Invoke**: Just ask — "write captions for next week" or "draft a new blog post about [topic]"

### 2. Brand Strategy & Positioning
**What it does**: Brand voice, positioning statements, taglines, bio copy, content pillars, audience research, competitor monitoring. Managed the full brand reframe from AI affirmations to displaced workers sanctuary.
**Files produced**: `brand-positioning.md`, `brand-voice-guide.md`, `instagram-bio-copy.md`, `brand-reframe.md`
**Invoke**: "update brand positioning for [new direction]" or "write bio options for [platform]"

### 3. Content Strategy & Calendar
**What it does**: Builds content calendars with posting schedules, format mix, hashtag rotation, technique integration, and monthly content previews. Maps healing techniques to content formats.
**Files produced**: `content-calendar.md`, `hashtag-sets.md`, `seo-content-strategy.md`, `instagram-reels-audio-strategy-2026.md`
**Invoke**: "update content calendar for month 2" or "plan next week's posts"

### 4. PDF Product Generation
**What it does**: Generates brand-styled PDFs using Python/reportlab — lead magnets, business plans, work summaries. Navy background, brand colors, Helvetica Neue, logo embedded.
**Files produced**: `generate_lead_magnet_pdf.py`, `generate_business_plan_pdf.py`, `generate_work_summary_pdf.py`
**Invoke**: "generate the lead magnet PDF" or "create a PDF for [new product]"
**Note**: Requires `.venv` activation. Avoid reportlab style names "BodyText" and "Italic" (already defined).

### 5. Image Generation
**What it does**: Generates logos, Kit product covers, Instagram backgrounds, quote cards, carousel slides using Python scripts and the `generate-image` skill (OpenRouter API — FLUX.2 Pro / Gemini 3 Pro).
**Files produced**: All `logo-*.png`, `kit-cover-*.png`, `instagram/` directory (quote cards, carousels, highlights, backgrounds)
**Invoke**: "generate a new logo option" or "create Kit cover for [product]" or "generate quote cards"

### 6. SEO & Blog Writing
**What it does**: Keyword research, content cluster planning, blog post writing (2,000-2,500 words, SEO-optimized with schema markup templates), publishing schedule, traffic projections.
**Files produced**: `seo-content-strategy.md`, 3 blog posts, schema markup templates
**Invoke**: "write a blog post targeting [keyword]" or "plan the next SEO content cluster"

### 7. Research
**What it does**: Deep research using parallel agents — audience analysis, competitor monitoring, platform trends, healing practices, pricing strategy, funnel optimization, Instagram algorithm insights.
**Files produced**: `healing-practices-reference-guide.md`, `competitor-monitoring.md`, and research embedded in `launch-plan-deepened.md`
**Invoke**: "research [topic] for our content strategy" or "what are the trends in [area]"

### 8. Website Development & Deployment
**What it does**: Writes and updates `index.html` — responsive design, mobile optimization, Kit form integration, OG meta tags, favicon. Commits and pushes to GitHub for auto-deploy via Vercel.
**Files produced**: `index.html`
**Invoke**: "update the website with [change]" or "push to git"

### 9. Email Marketing Planning
**What it does**: Writes email sequences (welcome, nurture, conversion), plans funnel architecture, drafts incentive emails, sets up tagging strategy.
**Files produced**: `welcome-email-sequence.md`, `email-nurture-sequence.md`
**Existing command**: `.claude/commands/email-marketing.md` (needs update to new brand)
**Invoke**: "write a new email sequence for [purpose]" or "draft the incentive email"

### 10. Launch Planning & Project Management
**What it does**: Master launch plan with phased milestones, task assignment (You Do / Claude Code Does), day-by-day checklists, revenue projections, metric targets.
**Files produced**: `launch-plan.md`, `launch-plan-deepened.md`, `notion-task-tracker.md`
**Invoke**: "update the launch plan" or "what's left before launch"

---

## Available Skills to Add

These are skills installed globally that we haven't used yet but could accelerate the project.

### High Priority — Use Now

| Skill | What it does | How it helps Luminous Pulse |
|-------|-------------|----------------------------|
| `copywriting` | Professional marketing copy with conversion frameworks | Sharpen landing pages, product descriptions, ad copy |
| `social-content` | Platform-specific social content optimization | Optimize captions for IG algorithm, plan cross-platform repurposing |
| `email-sequence` | Advanced email sequence architecture | Build sophisticated nurture flows, re-engagement campaigns, segmentation |
| `seo-optimizer` | On-page SEO, meta tags, Core Web Vitals | Optimize blog posts and website for search rankings |
| `schema-markup` | Structured data for rich search results | Add Article, FAQ, HowTo schema to blog posts for featured snippets |
| `form-cro` | Lead capture form optimization | Optimize the Kit email form for higher conversion |
| `analytics-tracking` | GA4, GTM, event tracking, UTM parameters | Set up Google Analytics + Search Console on luminouspulse.co |
| `launch-strategy` | Go-to-market planning, phased launches | Refine the Feb 17 launch and plan paid product launches |
| `marketing-psychology` | 70+ mental models for persuasion | Apply scarcity, social proof, anchoring to product pages and emails |

### Medium Priority — Use in Month 2-3

| Skill | What it does | How it helps Luminous Pulse |
|-------|-------------|----------------------------|
| `content-strategy` | Topic clusters, content planning frameworks | Plan Months 3-6 content with data-driven topic selection |
| `pricing-strategy` | Pricing psychology, tier optimization | Optimize $9 / $37 / $47 price points, plan new product tiers |
| `paid-ads` | Ad creative, targeting, budget optimization | When paid ads start (Day 82+, $5-10/day on top Reels) |
| `ab-test-setup` | A/B test architecture and measurement | Test email subject lines, landing page variants, CTA copy |
| `page-cro` | Landing page conversion optimization | Optimize luminouspulse.co for higher email capture rate |
| `signup-flow-cro` | Signup funnel optimization | Improve the Beacons → Kit → PDF → email flow |
| `programmatic-seo` | SEO pages at scale with templates | Generate location/keyword variant pages (e.g., "grounding for [role]") |
| `competitor-alternatives` | Competitor analysis and positioning | Map competitive landscape as wellness/grounding niche grows |
| `video-creator` | Programmatic video creation with Remotion | Auto-generate quote card videos, breathing timer Reels, affirmation animations |

### Future — Use for App & Scale

| Skill | What it does | How it helps Luminous Pulse |
|-------|-------------|----------------------------|
| `app-builder` | Full-stack app from natural language | Build the grounding practice app (technique pairing, guided sequences) |
| `mobile-design` | Mobile-first UI/UX design | Design the app experience |
| `workflow-automation` | Zapier/Make automation flows | Automate Kit → Metricool → ManyChat workflows |
| `zapier-workflows` | Zapier-specific automation | Connect tools in the tech stack |
| `stripe-integration` | Payment processing | When moving beyond Kit Commerce to custom checkout |
| `firebase` | Backend services | User accounts, progress tracking for the app |
| `google-analytics` | GA4 deep configuration | Advanced analytics, conversion funnels, audience insights |
| `vercel-deployment` | Advanced Vercel configuration | Custom domains, serverless functions, edge config |
| `web-performance-optimization` | Core Web Vitals, speed optimization | Optimize luminouspulse.co load times as content grows |
| `prd` | Product requirements documents | Write specs for the app, new features, guided audio products |

### Creative & Content Production

| Skill | What it does | How it helps Luminous Pulse |
|-------|-------------|----------------------------|
| `generate-image` | AI image generation (FLUX.2 Pro / Gemini) | Already in use — logos, covers, backgrounds |
| `canvas-design` | Design guidance and templates | Help design Canva templates programmatically |
| `mermaid-diagrams` | Flowcharts and diagrams | Visualize funnels, content flows, user journeys |
| `writing-clearly-and-concisely` | Editing for clarity | Polish blog posts, emails, and product copy |
| `pdf` / `pdf-processing` | Advanced PDF manipulation | Merge, split, annotate PDFs for products |
| `audiocraft-audio-generation` | AI audio generation | Generate ambient sounds for guided meditations |

---

## Custom Commands to Build

These are project-specific commands we should create in `.claude/commands/`:

### 1. `/generate-weekly-content`
Generate next week's captions, Story prompts, and technique tutorials based on the content calendar. Pull affirmations from `affirmations-150.md` and techniques from `healing-practices-reference-guide.md`.

### 2. `/generate-blog-post`
Write a new SEO-optimized blog post targeting a keyword from `seo-content-strategy.md`. Include schema markup, internal/external links, CTAs, and FAQ section.

### 3. `/generate-product-pdf`
Create a new branded PDF product (guided practice, toolkit, workbook) with navy background, brand colors, and logo. Handles all reportlab setup.

### 4. `/analytics-report`
Pull and summarize weekly metrics — followers, engagement rate, email subscribers, lead magnet downloads, top posts by saves. Format as a weekly report.

### 5. `/update-email-marketing`
Updated version of the existing email-marketing command, reflecting the new brand (displaced workers, not AI affirmations). Handles Kit sequence writing, tagging strategy, and funnel optimization.

### 6. `/generate-quiz`
Create interactive quiz content — "What's your nervous system state?", "Where does your body hold stress?", "Which healing modality fits you?" — with scoring logic and email capture integration.

### 7. `/repurpose-content`
Take a single piece of content (blog post, carousel, Reel script) and repurpose it across formats: Instagram caption, LinkedIn post, email newsletter, Pinterest pin, TikTok script.

### 8. `/competitor-scan`
Research competitors in the wellness/grounding/displaced worker niche. Track new entrants, trending content formats, pricing changes, audience overlap.

---

## How to Use Skills

```bash
# Use a global skill by name
# Just reference the skill topic in your request and Claude will activate it

# Example: "Use the copywriting skill to rewrite the landing page"
# Example: "Use seo-optimizer to audit blog post 1"
# Example: "Use marketing-psychology to improve the nurture email sequence"

# Custom commands (once built):
# /generate-weekly-content
# /generate-blog-post "keyword here"
# /generate-product-pdf "product name"
```

---

## Priority Actions

1. **Now**: Set up `analytics-tracking` — get Google Analytics + Search Console on luminouspulse.co before launch
2. **Now**: Use `schema-markup` to add structured data to the website
3. **Week 1**: Use `form-cro` to optimize the Kit email capture form
4. **Week 2**: Use `marketing-psychology` to strengthen the nurture email sequence
5. **Month 2**: Use `video-creator` to auto-generate breathing timer Reels
6. **Month 2**: Build custom commands (`/generate-weekly-content`, `/generate-blog-post`)
7. **Month 3**: Use `paid-ads` when starting ad spend
8. **Month 4+**: Use `app-builder` to scope and build the grounding practice app
