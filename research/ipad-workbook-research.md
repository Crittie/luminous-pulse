# Digital Workbooks & Journals for iPad + Apple Pencil (and Print)
## Comprehensive Product Development Research Guide

**Research Date:** February 18, 2026

---

## 1. iPad/Tablet-Compatible Formats

### What File Format Works Best for Apple Pencil Writing?

**PDF is the universal winner.** Here is why:

- **PDF** is the gold standard for cross-app, cross-platform compatibility. Both GoodNotes and Notability (the two dominant iPad journaling apps) use PDF as their primary import format. PDFs support hyperlinks, form fields, and freehand annotation with Apple Pencil.
- **GoodNotes native format (.goodnotes)** is proprietary and only works within GoodNotes. You cannot sell .goodnotes files for use in other apps.
- **Notability native format (.note)** is also proprietary (it is actually a zip file containing assets, plists, and recordings). Same limitation -- only works in Notability.
- **PNG/JPG** can be imported as page backgrounds but do NOT support hyperlinks or clickable navigation. Avoid these as your primary format.

**Recommendation:** Always create and sell PDFs. They work in GoodNotes, Notability, Noteful, PDF Expert, Xodo, Noteshelf, and even Apple's native Files/Markup app.

### How Do You Make a PDF "Writable" with Apple Pencil?

The good news: **any standard PDF is already writable with Apple Pencil.** There is no special "writable" encoding needed. Here is how it works technically:

1. **Freehand Annotation (Drawing Layer):** When you open any PDF in GoodNotes, Notability, or PDF Expert, the app creates a transparent annotation layer on top of each page. Apple Pencil writes on this layer. The original PDF content remains untouched underneath.

2. **Fillable Form Fields (AcroForms):** You can optionally add interactive text fields to your PDF using Adobe Acrobat, InDesign, or similar tools. When a user taps a form field on iPad, iPadOS activates "Scribble" -- which converts Apple Pencil handwriting into typed text automatically. This is great for structured responses (name fields, short answers) but not ideal for free journaling.

3. **The key distinction:**
   - **"Flat" PDF** = No form fields. User writes freehand with Apple Pencil on an annotation layer. Best for journals, open-ended prompts, gratitude pages.
   - **"Interactive" PDF** = Contains AcroForm fields for typed input. Best for structured workbooks with specific answer fields. Note: form field support varies by app. GoodNotes has limited form field support; PDF Expert and Adobe Acrobat Reader handle them well.

### What Apps Do People Use?

| App | Price | Best For | Form Fields? | Hyperlinks? |
|-----|-------|----------|-------------|-------------|
| **GoodNotes 6** | Free (limited) / $9.99/yr | Digital planning, journaling | Limited | Yes (in read mode) |
| **Notability** | Free (limited) / $14.99/yr | Handwriting, note-taking | Limited | Yes |
| **PDF Expert** | $79.99/yr | PDF annotation, form filling | Full AcroForm | Yes |
| **Noteful** | Free / $9.99 one-time | Budget-friendly alternative | Basic | Yes |
| **Noteshelf** | $14.99 one-time | Aesthetic journaling | Basic | Yes |
| **Xodo** | Free / Premium | Cross-platform PDF | Full | Yes |
| **Apple Markup** | Free (built-in) | Quick annotations | Basic | No |
| **Zinnia** | Free / Premium | Wellness journaling | No | No |

**GoodNotes dominates the market** for digital planner/journal use. Design for GoodNotes first, then verify compatibility with Notability and PDF Expert.

### Flat PDF vs Interactive PDF

| Feature | Flat PDF | Interactive PDF |
|---------|----------|----------------|
| Apple Pencil freehand writing | Yes (via annotation layer) | Yes |
| Typed text in form fields | No | Yes (Scribble converts handwriting) |
| Hyperlinked navigation | Yes | Yes |
| File size | Smaller | Slightly larger |
| App compatibility | Universal | Varies (some apps ignore form fields) |
| Best for | Journals, creative prompts | Workbooks, structured exercises |

**For your use case (wellness/affirmation journals):** Use flat PDFs with generous writing space. Add hyperlinked navigation tabs. Skip form fields unless you specifically need typed responses -- they add complexity and reduce app compatibility.

---

## 2. Dual-Format Best Practices (Print + Digital)

### How Successful Creators Handle Both Formats

**Strategy A -- Single PDF, Dual Use (Most Common):**
- Design one PDF that works for both printing AND iPad annotation
- Use standard paper sizes (US Letter or A4) so it prints correctly
- Sell as one product with instructions: "Print it OR use it on your iPad with GoodNotes/Notability"
- This is the simplest approach and what most Etsy sellers do

**Strategy B -- Two Separate Files (Premium Approach):**
- Create a "Print Version" (no hyperlinks, crop marks, bleed area, 300 DPI)
- Create a "Digital Version" (hyperlinked tabs, optimized for screen, 150 DPI, landscape orientation)
- Sell as a bundle at a higher price point
- This is more work but justifies premium pricing ($15-25 vs $5-10)

**Strategy C -- Tiered SKUs:**
- Basic: Printable PDF only ($7-10)
- Standard: Digital iPad version only ($10-15)
- Premium Bundle: Both + bonus stickers/covers ($20-30)

### Page Size for Both Print and iPad

| Size | Dimensions | Print? | iPad Fit? | Notes |
|------|-----------|--------|-----------|-------|
| **US Letter** | 8.5" x 11" (2550 x 3300 px @300dpi) | Perfect | Good (portrait) | Best for US market, prints on standard paper |
| **A4** | 8.27" x 11.69" (2480 x 3508 px @300dpi) | Perfect | Good (portrait) | Best for international market |
| **GoodNotes Standard** | 834 x 1112 px (portrait) | No | Perfect | iPad-native, but won't print well |
| **A5** | 5.83" x 8.27" | Half-sheet printing | Very good | Popular compromise |
| **US Half Letter** | 5.5" x 8.5" | Half-sheet printing | Very good | US equivalent of A5 |

**Recommended approach for dual-format:**
- **Portrait orientation, US Letter (8.5" x 11")** for US audience
- **Portrait orientation, A4** for international audience
- Design at **300 DPI** (print-ready), then export a screen-optimized version at **150 DPI** for the digital file
- The 4:3 aspect ratio of Letter/A4 works reasonably well on iPad screens

### Margins, Line Spacing, and Writing Space

**For Apple Pencil handwriting:**
- **Line spacing: 7-8mm minimum** (most popular range is 5-7mm, but Apple Pencil handwriting tends to be larger than physical pen writing -- err toward 8mm)
- **Left/right margins: 0.75" - 1" minimum** (for both print binding and iPad palm rejection zones)
- **Top margin: 0.5" - 0.75"** (leave room for navigation tabs in digital version)
- **Bottom margin: 0.5"**
- **Writing area per page:** Aim for 15-20 lines per page for lined journals; for open-ended prompts, give a full half-page or more of blank/dotted space

**Print-specific considerations:**
- Add 0.125" bleed on all sides for professional printing
- Inner margin (gutter) should be 0.5" wider for spiral/coil binding

**Digital-specific considerations:**
- Keep important content away from screen edges (iPads have rounded corners)
- Navigation tabs should be large enough to tap easily (minimum 44px tap target per Apple's HIG)

---

## 3. GoodNotes/Notability Template Market

### Market Size and Opportunity

The digital planner market on Etsy alone is substantial:
- **Top sellers earn GBP 10,000-20,000/month** (approximately $12,000-$25,000 USD)
- **Average successful sellers earn $500-$5,000/month**
- Digital planners are consistently among the **top 5 best-selling digital product categories** on Etsy
- The market is **evergreen** -- demand spikes at New Year, back-to-school, and quarterly planning seasons, but exists year-round

### Etsy Pricing Data

| Product Type | Price Range | Sweet Spot |
|-------------|-------------|------------|
| Basic digital planner (undated) | $3 - $8 | $4 - $6 |
| Dated annual planner | $5 - $15 | $8 - $12 |
| All-in-one planner bundle | $10 - $25 | $12 - $18 |
| Wellness/mental health journal | $5 - $15 | $8 - $12 |
| Premium bundles (planners + stickers + covers) | $15 - $50 | $20 - $30 |
| Sticker packs | $2 - $8 | $3 - $5 |

**Key insight:** Generic planners are **oversaturated**. Niched-down products sell better. Examples: "ADHD daily planner for moms," "CBT self-therapy journal," "PM productivity workbook." Your existing PM niche is a strength.

### Selling Platforms

| Platform | Pros | Cons | Fees |
|----------|------|------|------|
| **Etsy** | Massive built-in audience, SEO traffic | High competition, listing fees, 6.5% transaction fee | $0.20/listing + 6.5% + payment processing |
| **Gumroad** | Simple setup, you already use it, good for existing audience | No discovery/SEO, must drive own traffic | 10% flat fee |
| **Kit Commerce** (formerly ConvertKit) | Integrates with email marketing | Small marketplace, limited discovery | 3.5% + $0.30 per transaction |
| **GoodNotes Marketplace** | Direct in-app audience, curated | Requires application approval, quarterly payouts, revenue share | Commission-based (rate in contract) |
| **Shopify** | Full control, branding, no listing limits | Monthly fee, must drive own traffic | $39/mo + payment processing |
| **Creative Market** | Design-focused audience | Application required, 30% commission | 30% commission |

**For your situation:** Continue using **Gumroad** (you already have it set up for your PM ebook). Add **Etsy** as a second channel for discovery. Consider applying to the **GoodNotes Marketplace** for credibility and in-app visibility.

### What Makes a GoodNotes Template "Good"?

Based on analysis of top-selling templates, the key quality differentiators are:

1. **Hyperlinked navigation tabs** -- Clickable side tabs and top tabs that jump between sections (monthly, weekly, daily, etc.). Top templates have 30,000+ hyperlinks across the document.
2. **Clean, modern design** -- Minimalist layouts outperform busy/cluttered designs. Think navy + one accent color (you already have this with your navy + orange system).
3. **Generous writing space** -- Templates with cramped lines get poor reviews. Leave plenty of room for Apple Pencil handwriting.
4. **Multiple page templates** -- Include dot grid, lined, blank, and graph options.
5. **Realistic paper textures** -- Subtle paper texture backgrounds (cream, kraft, white linen) feel more premium than flat white.
6. **Bonus stickers** -- Digital sticker packs (PNG files or a separate GoodNotes sticker book) are expected at the $10+ price point.
7. **Cover designs** -- Multiple cover options (5-10 designs) so users can personalize.
8. **Bookmarks** -- Properly structured PDF bookmarks for the sidebar navigation in GoodNotes.

---

## 4. Technical Production

### Best Tools Comparison

| Tool | Cost | Hyperlinks? | Master Pages? | Export Quality | Learning Curve | Best For |
|------|------|-------------|---------------|---------------|----------------|----------|
| **Affinity Publisher** | $69.99 one-time (iPad: $19.99) | Yes | Yes | Excellent, great compression | Medium | Professional dual-format production |
| **Keynote** | Free (Mac/iPad) | Best-in-class | Yes (Master Slides) | Good, but large files | Low-Medium | Quick hyperlinked planners |
| **Canva Pro** | $12.99/mo | Yes (basic) | No master pages | Good | Very Low | Beginners, simple planners under 30 pages |
| **Adobe InDesign** | $22.99/mo | Yes | Yes | Best | High | Professional publishers |
| **Planify Pro** | $9.99/mo | Auto-generated | Yes | Good | Low | Planner-specific, auto-linking |
| **PowerPoint/Google Slides** | Free-$9.99/mo | Yes | Yes (Master Slides) | Acceptable | Low | Budget option |

**Recommended tool stack:**

- **Best overall:** Affinity Publisher (one-time $69.99 purchase, professional output, works on Mac and iPad, excellent PDF compression, master pages for consistent navigation tabs across all pages)
- **Best for speed/beginners:** Planify Pro ($9.99/mo, automatically generates all hyperlinks between pages -- no manual linking of months/weeks/days)
- **Best free option:** Keynote (excellent hyperlink support, but exports large files that need compression)
- **Avoid for large planners:** Canva (no master pages makes tab management painful on 100+ page documents; licensing restrictions on selling Canva-made PDFs)

### How to Add Hyperlinked Navigation

**The process in Affinity Publisher or Keynote:**

1. **Create your page layout** with section tabs (rectangles along the right side or top of each page)
2. **Design a "master page"** with these tabs so they appear on every page
3. **Add hyperlinks to each tab:**
   - Right-click the tab shape/text > Add Link > Choose destination page
   - Link "January" tab to page 5 (where January starts)
   - Link "Weekly" tab to page 12 (where weekly spreads start)
   - Repeat for every section
4. **Add a Table of Contents page** with hyperlinks to all major sections
5. **Export as PDF** -- ensure "Include Hyperlinks" is checked in export settings

**In Canva:**
- Select a shape/text > Click "Link" icon in top toolbar > Choose page number
- Note: Canva requires you to manually update links on EVERY page (no master page feature)

**In Planify Pro:**
- Links are generated automatically when you define your planner structure (year > months > weeks > days)

### How to Add Fillable Form Fields

**If you want typed-response fields (optional):**

1. Design your layout in Affinity Publisher / InDesign / Canva
2. Export as a standard PDF
3. Open in **Adobe Acrobat Pro** ($22.99/mo) or **PDF Expert** ($79.99/yr)
4. Use the "Prepare Form" tool to draw text field boxes where you want typed responses
5. Set field properties (font, size, multiline, max characters)
6. Save as an interactive PDF

**Caveat:** Form fields have inconsistent support across iPad apps. GoodNotes has limited form field support. If your primary audience uses GoodNotes, skip form fields and design generous blank/lined spaces for freehand writing instead.

### Resolution Requirements

| Use Case | DPI | File Size Impact |
|----------|-----|-----------------|
| **Print only** | 300 DPI | Largest files |
| **Dual format (recommended)** | 300 DPI source, export 150 DPI for digital | Medium files |
| **Screen/iPad only** | 150 DPI | Smallest files |
| **Background textures** | 150 DPI is sufficient | -- |
| **Text and vectors** | Resolution-independent (vector) | Minimal impact |

### File Size Optimization for iPad

iPads struggle with very large PDFs. Here are the targets:

| Planner Size | Target File Size | Max Acceptable |
|-------------|-----------------|----------------|
| Monthly (30-50 pages) | 5-15 MB | 25 MB |
| Quarterly (100-150 pages) | 15-30 MB | 50 MB |
| Annual (300-500 pages) | 30-60 MB | 100 MB |
| 1000+ page mega-planner | Split into volumes | Never exceed 150 MB |

**Optimization techniques:**

1. **Use vector graphics** for lines, shapes, borders, tabs (zero bloat)
2. **Limit raster images** -- Background textures at 150 DPI, not 300
3. **Use the monochrome color model** for black-and-white line art (up to 24x smaller than RGB)
4. **Compress on export** -- Affinity Publisher lets you preview file size before exporting and offers compression controls
5. **Split large planners** into monthly or quarterly volumes rather than one massive annual file
6. **Avoid embedding fonts** you do not actually use
7. **Flatten transparency** where possible
8. **Test on an actual iPad** before selling -- open the file in GoodNotes and flip through all pages to check for lag

### Writing Space Design Guidelines

For Apple Pencil freehand writing:
- **Minimum line height:** 7mm (8mm recommended for comfortable handwriting)
- **Dot grid spacing:** 5mm is standard
- **Lines per page:** 15-20 for a Letter-sized page in portrait
- **Prompt response areas:** Give at least 1.5" - 2" of vertical space for short answers, half-page for reflections
- **Margin for palm rejection:** Keep writing area at least 0.5" from edges
- **Tap target size for tabs:** Minimum 44x44 pixels (Apple Human Interface Guidelines)

---

## 5. Competitor Examples and Analysis

### Well-Made iPad-Compatible Journals and Workbooks

#### 1. Templatables -- Digital Wellness & Fitness Journal
- **Price:** ~$15-20
- **Pages:** 700+ pages across 12 notebooks
- **Features:** 30,000+ hyperlinks, daily pages for meals/fitness/sleep/hydration tracking, 100+ additional planning templates, 500+ digital stickers, 100+ bonus planner covers
- **What they do well:** Massive value proposition, extremely thorough hyperlinking, wellness-specific design
- **Niche:** Wellness, fitness, self-care
- **URL:** templatables.com

#### 2. HappyDownloads -- Rainbow Digital Planner
- **Price:** $2.99 - $12.99
- **Pages:** Extensive (part of 10,000-planner bundle system)
- **Features:** 60+ templates across productivity, wellness, fitness, nutrition, and finance; mood tracker, habits tracker, sleep tracker, gratitude journal; 50,000 stickers
- **What they do well:** Incredible volume of templates, customizable planner builder tool, very competitive pricing
- **Niche:** General planning with wellness sections
- **URL:** happydownloads.net

#### 3. BestSelf Co. -- Self Journal for GoodNotes
- **Price:** ~$15-20 (digital), $32.95 (physical)
- **Features:** 13-week goal-setting system, daily pages with gratitude + targets + schedule, quarterly reflections, monthly planning; based on their bestselling physical journal
- **What they do well:** Proven system (physical product first, then digitized); strong brand; structured methodology, not just blank pages
- **Niche:** Productivity and goal-setting
- **URL:** bestself.co

#### 4. iPad Planner (ipadplanner.com) -- Digital Bullet Journal
- **Price:** ~$10-15
- **Pages:** 1,300+ pages
- **Features:** 128,356 hyperlinks, 24-month calendar, dot-grid layout, customizable index page, clean minimalist design
- **What they do well:** Insane number of hyperlinks for seamless navigation, optimized specifically for iPad, clean design
- **Niche:** Bullet journaling / productivity
- **URL:** ipadplanner.com

#### 5. Self-Therapy Journal Bundle (Etsy)
- **Price:** ~$8-15
- **Pages:** 365+ daily prompts
- **Features:** CBT exercises, guided journal prompts, shadow work worksheets, mindfulness tools, daily digital journal
- **What they do well:** Therapeutic depth -- not just a blank journal but guided mental health exercises; strong niche positioning
- **Niche:** Mental health, CBT, self-therapy
- **Platform:** Etsy

#### 6. Zinnia App (Standalone)
- **Price:** Free / Premium subscription
- **Features:** Ready-to-use journals, planners, trackers; full Apple Pencil integration; wellness-specific templates (gratitude, mood, self-care)
- **What they do well:** Native app experience (smoother than PDF-in-GoodNotes), beautiful templates, easy onboarding
- **Niche:** Wellness journaling
- **URL:** App Store

#### 7. OnPlanners -- GoodNotes Templates
- **Price:** Free - $15
- **Features:** Wide selection of dated/undated planners, journals, and trackers; hyperlinked PDFs; multiple design styles
- **What they do well:** Huge template variety, detailed customization options, clear comparison guides
- **Niche:** General planning
- **URL:** onplanners.com

#### 8. Digital-Planner.com -- Wellness Journal
- **Price:** ~$10-20
- **Features:** Dedicated daily wellness pages, fitness tracking, meal planning, mood tracking, weekly/monthly/yearly reflections, hyperlinked navigation
- **What they do well:** Comprehensive wellness system (not just prompts), professional design, pattern-recognition focus
- **Niche:** Wellness and health
- **URL:** digital-planner.com

#### 9. The Sweet Setup -- GoodNotes Productivity Templates
- **Price:** ~$20-40 (template bundle + video training)
- **Features:** 24+ custom templates for productivity planning, meeting notes, habit trackers, daily/weekly/monthly schedules, goal-setters, video training included
- **What they do well:** Educational component (video tutorials), professional quality, strong brand reputation in Apple productivity space
- **Niche:** Productivity
- **URL:** thesweetsetup.com

#### 10. Guided Wellness Discovery Journal (Etsy)
- **Price:** ~$8-15
- **Pages:** 150+ pages
- **Features:** 120+ unique prompts organized by monthly themes (Understanding Yourself, Health and Wellness, Acceptance, Resilience), daily guided entries
- **What they do well:** Structured monthly progression, therapeutic depth, beautiful design
- **Niche:** Wellness, personal growth

### Competitive Patterns

**What the best competitors do consistently:**
1. Hyperlinked navigation is table stakes -- every serious competitor has it
2. Wellness/mental health is a growing and underserved niche (less saturated than generic planning)
3. Bundles with stickers and covers command premium prices
4. The best products have a structured methodology, not just blank pages
5. Multi-year dating (2025-2027) or undated formats reduce churn
6. Clean, minimalist design with 1-2 accent colors outperforms busy/colorful layouts
7. Etsy + own website (Gumroad/Shopify) dual distribution is standard

---

## 6. Actionable Recommendations for Your Business

### Product Concept: PM Wellness + Productivity Digital Workbook

Given your existing brand (ChatGPT Prompts for PMs), consider a digital journal/workbook that bridges **PM productivity** and **wellness/burnout prevention**. This is a genuinely underserved niche.

### Recommended Technical Stack

1. **Design tool:** Affinity Publisher ($69.99 one-time) -- OR start with Keynote (free) for a first version
2. **Page size:** US Letter portrait (8.5" x 11") at 300 DPI -- export digital version at 150 DPI
3. **Format:** Flat PDF with hyperlinked navigation tabs (no form fields)
4. **File delivery:** PDF for GoodNotes/Notability + same PDF works for printing
5. **Sell on:** Gumroad (primary) + Etsy (discovery)

### Pricing Strategy

- **Digital-only iPad journal:** $9.99 - $14.99
- **Print-ready + Digital bundle:** $14.99 - $19.99
- **Premium bundle (journal + stickers + covers):** $19.99 - $27.00
- **Lead magnet:** Free 5-page sample (email capture, funnels to paid product)

### Minimum Viable Product Checklist

- [ ] 50-100 pages
- [ ] Hyperlinked table of contents
- [ ] Hyperlinked section tabs on every page
- [ ] 7-8mm line spacing for Apple Pencil writing
- [ ] US Letter size (portrait)
- [ ] Under 30 MB file size
- [ ] Tested in GoodNotes, Notability, and PDF Expert
- [ ] 3-5 cover design options
- [ ] Clear usage instructions (1-page "How to Use This Journal on iPad")
- [ ] Both a digital-optimized (150 DPI) and print-ready (300 DPI) export

---

## Sources

### iPad/Tablet Formats
- [Apple Support: Write in your journal on iPad](https://support.apple.com/guide/ipad/write-in-your-journal-ipad376f7c5c/ipados)
- [iMore: Best PDF annotation apps for iPad 2026](https://www.imore.com/best-pdf-apps-ipad)
- [Hello Brio: Digital Journaling on iPad 2025](https://www.hellobrio.com/blog/digital-journaling-on-ipad)
- [Adobe: Mark up PDFs with Apple Pencil](https://www.adobe.com/acrobat/hub/can-you-use-apple-pencil-on-pdf.html)
- [GoodNotes Support: Import files](https://support.goodnotes.com/hc/en-us/articles/7353717816463-Import-files-into-Goodnotes)
- [GoodNotes Support: Hyperlink support in digital planners](https://support.goodnotes.com/hc/en-us/articles/8652018962831-Hyperlink-Support-in-Digital-Planners-and-PDF-Documents)
- [MacRumors: Writing freehand on PDF with iPad](https://forums.macrumors.com/threads/writing-freehand-on-a-pdf-with-ipad.2448561/)

### Template Creation
- [Jena W Designs: How to use hyperlinks in GoodNotes](https://jenawdesigns.com/blogs/digital-planning-tips/how-to-use-hyperlinks-in-goodnotes)
- [GoodNotes Support: Create custom templates with hyperlinks](https://support.goodnotes.com/hc/en-us/articles/333757017176-How-to-create-custom-templates-with-working-hyperlinks-Digital-Planner)
- [Life is Messy and Brilliant: How to make a digital planner with hyperlinks](https://lifeismessyandbrilliant.com/how-to-make-a-digital-planner-with-hyperlinks/)
- [Realistic Planner: How to create digital planner for GoodNotes](https://realisticplanner.com/how-to-create-digital-planner-for-goodnotes/)
- [Make a Digital Planner: Digital planner size for GoodNotes](https://makeadigitalplanner.com/digital-planner-size-for-goodnotes/)
- [GoodNotes Support: Built-in template dimensions](https://support.goodnotes.com/hc/en-us/articles/4403641962383-What-are-the-page-dimensions-of-built-in-GoodNotes-templates-)

### Tools and Software
- [The Pink Ink: Keynote vs Affinity Publisher for digital planners](https://the-pinkink.com/blog/keynote-vs-affinity-publisher-which-one-to-choose-when-making-your-digital-planner)
- [Powerhouse Planners: 6 apps to create digital planners](https://powerhouseplanners.com/programs-to-create-digital-planners/)
- [Make a Digital Planner: Best programs](https://makeadigitalplanner.com/programs-to-make-a-digital-planner/)
- [Planify Pro: Create digital planner with automatic linking](https://blog.planifypro.com/create-digital-planner-automatic-linking/)
- [Moonrise Digital: Keep GoodNotes journal lightweight](https://moonrisedigitalco.com/how-to-keep-your-goodnotes-journal-lightweight-avoid-pdf-bloat-save-space-on-your-ipad/)

### Market and Pricing
- [Etsy: GoodNotes templates marketplace](https://www.etsy.com/market/goodnotes_templates)
- [Digital Biz PLR: Best digital products to sell on Etsy 2026](https://digitalbizplr.com/blogs/learn/best-digital-products-sell-etsy-2026)
- [Alicia Rafie: Digital journal ideas that sell on Etsy](https://aliciarafieiblog.com/digital-journal-ideas-etsy/)
- [Kajabi: Sell GoodNotes templates successfully](https://www.kajabi.com/blog/sell-goodnotes-templates)
- [Amma Rose Designs: Is selling digital planners profitable?](https://ammarosedesigns.com/is-selling-digital-planners-profitable/)
- [GoodNotes: Apply to be a marketplace creator](https://www.goodnotes.com/marketplace/apply-to-be-a-creator)

### Workbook Creation Guides
- [Wobo: How to create digital workbooks](https://wobo.app/blog/how-to-create-a-digital-workbook)
- [Made on Sundays: How to create a digitally fillable workbook](https://madeonsundays.com/fillableworkbook/)
- [Creative Market: How to create a fillable PDF workbook](https://creativemarket.com/blog/how-to-create-a-fillable-pdf-workbook)
- [Blurb: How to create a workbook for your course](https://www.blurb.com/blog/how-to-create-workbook-for-online-course/)
- [PrintablesBuzz: How to size a digital planner in Affinity Publisher](https://printablesbuzz.com/planners/how-to-size-a-digital-planner/)

### Competitor Products
- [Templatables: Digital Wellness Planners](https://www.templatables.com/en-us/collections/digital-wellness-and-self-care-planners)
- [HappyDownloads: Digital Planner Shop](https://www.happydownloads.net/)
- [BestSelf Co: Self Journal GoodNotes Template](https://bestself.co/products/self-journal-goodnote-app-template)
- [iPad Planner: Digital Journal Templates](https://ipadplanner.com/collections/digital-journal)
- [GoodNotes Blog: 11 Best Digital Planners 2026](https://www.goodnotes.com/blog/digital-planners)
- [The Sweet Setup: GoodNotes Templates](https://thesweetsetup.com/goodnotes/)
- [OnPlanners: GoodNotes Templates](https://onplanners.com/templates/goodnotes)
- [Digital-Planner.com: Wellness Journal](https://digital-planner.com/wellness/journal)
- [Gridfiti: 75 Best Aesthetic GoodNotes Templates 2026](https://gridfiti.com/goodnotes-templates-aesthetic/)
