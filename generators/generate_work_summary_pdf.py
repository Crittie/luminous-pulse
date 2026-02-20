#!/usr/bin/env python3
"""Generate work summary + pre-launch checklist PDF for Luminous Pulse."""

from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import HexColor
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER

# Brand colors
NAVY = HexColor("#1a2744")
BLUE = HexColor("#6CB4EE")
AMBER = HexColor("#F4C430")
LAVENDER = HexColor("#B4A7D6")
WHITE = HexColor("#FFFFFF")
LIGHT_GRAY = HexColor("#f5f6fa")
DARK_GRAY = HexColor("#333333")
MED_GRAY = HexColor("#666666")
SOFT_NAVY = HexColor("#2a3a5c")
GREEN = HexColor("#4CAF50")
RED_SOFT = HexColor("#e57373")


def create_styles():
    styles = getSampleStyleSheet()

    styles.add(ParagraphStyle(
        name="CoverTitle",
        fontName="Helvetica-Bold",
        fontSize=28,
        textColor=NAVY,
        alignment=TA_LEFT,
        spaceAfter=6,
        leading=34,
    ))
    styles.add(ParagraphStyle(
        name="CoverSubtitle",
        fontName="Helvetica",
        fontSize=13,
        textColor=SOFT_NAVY,
        alignment=TA_LEFT,
        spaceAfter=4,
        leading=18,
    ))
    styles.add(ParagraphStyle(
        name="SectionHeader",
        fontName="Helvetica-Bold",
        fontSize=18,
        textColor=NAVY,
        spaceBefore=20,
        spaceAfter=10,
        leading=22,
    ))
    styles.add(ParagraphStyle(
        name="SubHeader",
        fontName="Helvetica-Bold",
        fontSize=12,
        textColor=SOFT_NAVY,
        spaceBefore=14,
        spaceAfter=6,
        leading=15,
    ))
    styles.add(ParagraphStyle(
        name="DayHeader",
        fontName="Helvetica-Bold",
        fontSize=12,
        textColor=BLUE,
        spaceBefore=14,
        spaceAfter=4,
        leading=15,
    ))
    styles.add(ParagraphStyle(
        name="Body",
        fontName="Helvetica",
        fontSize=10,
        textColor=DARK_GRAY,
        spaceAfter=5,
        leading=14,
    ))
    styles.add(ParagraphStyle(
        name="BodyBold",
        fontName="Helvetica-Bold",
        fontSize=10,
        textColor=DARK_GRAY,
        spaceAfter=5,
        leading=14,
    ))
    styles.add(ParagraphStyle(
        name="CheckItem",
        fontName="Helvetica",
        fontSize=10,
        textColor=DARK_GRAY,
        leftIndent=20,
        spaceAfter=4,
        leading=14,
    ))
    styles.add(ParagraphStyle(
        name="CheckItemDone",
        fontName="Helvetica",
        fontSize=10,
        textColor=MED_GRAY,
        leftIndent=20,
        spaceAfter=4,
        leading=14,
    ))
    styles.add(ParagraphStyle(
        name="Quote",
        fontName="Helvetica-Oblique",
        fontSize=11,
        textColor=SOFT_NAVY,
        leftIndent=20,
        rightIndent=20,
        spaceBefore=8,
        spaceAfter=8,
        leading=15,
    ))
    styles.add(ParagraphStyle(
        name="SmallText",
        fontName="Helvetica",
        fontSize=8,
        textColor=MED_GRAY,
        alignment=TA_CENTER,
        spaceAfter=4,
        leading=10,
    ))
    styles.add(ParagraphStyle(
        name="TableHeader",
        fontName="Helvetica-Bold",
        fontSize=9,
        textColor=WHITE,
        alignment=TA_LEFT,
        leading=12,
    ))
    styles.add(ParagraphStyle(
        name="TableCell",
        fontName="Helvetica",
        fontSize=9,
        textColor=DARK_GRAY,
        alignment=TA_LEFT,
        leading=12,
    ))
    styles.add(ParagraphStyle(
        name="Callout",
        fontName="Helvetica-Bold",
        fontSize=11,
        textColor=NAVY,
        spaceBefore=10,
        spaceAfter=6,
        leading=14,
    ))
    return styles


def hr():
    return HRFlowable(
        width="100%", thickness=1, color=LAVENDER,
        spaceBefore=6, spaceAfter=6
    )


def make_table(headers, rows, col_widths=None):
    s = create_styles()
    header_row = [Paragraph(h, s["TableHeader"]) for h in headers]
    data = [header_row]
    for row in rows:
        data.append([Paragraph(str(c), s["TableCell"]) for c in row])

    t = Table(data, colWidths=col_widths, repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
        ("TOPPADDING", (0, 0), (-1, 0), 8),
        ("BACKGROUND", (0, 1), (-1, -1), WHITE),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, LIGHT_GRAY]),
        ("TOPPADDING", (0, 1), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 1), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("GRID", (0, 0), (-1, -1), 0.5, HexColor("#dddddd")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    return t


def add_footer(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(MED_GRAY)
    canvas.setFont("Helvetica", 7)
    canvas.drawString(72, 36, "Luminous Pulse  |  Work Summary  |  February 13, 2026")
    canvas.drawRightString(letter[0] - 72, 36, f"Page {doc.page}")
    canvas.setStrokeColor(AMBER)
    canvas.setLineWidth(2)
    canvas.line(72, letter[1] - 36, letter[0] - 72, letter[1] - 36)
    canvas.restoreState()


def build_pdf():
    filename = "/Users/christieparrow/luminous-pulse/_archive/Luminous-Pulse-Work-Summary-Feb13.pdf"
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        topMargin=0.75 * inch,
        bottomMargin=0.75 * inch,
        leftMargin=0.85 * inch,
        rightMargin=0.85 * inch,
    )
    s = create_styles()
    story = []

    # Check mark and box symbols
    CHECK = "\u2705"
    BOX = "\u2610"

    # ── COVER PAGE ──
    story.append(Spacer(1, 1.2 * inch))
    story.append(Paragraph("Luminous Pulse", s["CoverTitle"]))
    story.append(Spacer(1, 4))
    story.append(Paragraph("Work Completed + Pre-Launch Checklist", s["CoverSubtitle"]))
    story.append(Paragraph("February 13, 2026", s["CoverSubtitle"]))
    story.append(Spacer(1, 12))
    story.append(hr())
    story.append(Spacer(1, 12))
    story.append(Paragraph(
        "Launch Target: February 17, 2026 (Lunar New Year / New Moon)",
        s["BodyBold"]
    ))
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "This document covers: (1) everything completed by Claude Code today, "
        "(2) the complete asset inventory, and (3) what Christie needs to complete "
        "before the February 17 launch.",
        s["Body"]
    ))
    story.append(Spacer(1, 36))
    story.append(Paragraph(
        '<i>"The feeling follows the words. Not the other way around."</i>',
        s["Quote"]
    ))
    story.append(PageBreak())

    # ── SECTION 1: WORK COMPLETED TODAY ──
    story.append(Paragraph("1. Work Completed Today (Feb 13)", s["SectionHeader"]))
    story.append(hr())

    story.append(Paragraph("New Content Files Created (7 files)", s["SubHeader"]))
    today_files = [
        ["File", "Description", "Purpose"],
        ["influencer-outreach-templates.md", "6 DM templates + 3 follow-ups + outreach cadence", "Phase 4: Micro-influencer partnerships"],
        ["blog-post-1-identity-crisis.md", '"Who Am I Without My Job?" (~2,400 words)', "SEO: identity crisis after job loss"],
        ["blog-post-2-affirmations-after-layoff.md", '"25 Grounding Affirmations" (~2,300 words)', "SEO: affirmations after getting laid off"],
        ["blog-post-3-ai-replacing-job-anxiety.md", '"AI Is Replacing Your Job?" (~2,500 words)', "SEO: AI replacing my job anxiety"],
        ["seo-content-strategy.md", "Full SEO roadmap, keyword research, content clusters", "SEO planning for luminouspulse.co"],
        ["instagram-reels-audio-strategy-2026.md", "Trending audio by content type + algorithm tips", "Reels audio selection guide"],
    ]
    t = make_table(today_files[0], today_files[1:], col_widths=[2.2*inch, 2.5*inch, 1.6*inch])
    story.append(t)

    story.append(Paragraph("Research Completed (3 deep-dive research agents)", s["SubHeader"]))
    research = [
        "\u2022  <b>Trending Reels Audio 2026</b> \u2014 Specific song recommendations by content type, algorithm insights, audio length sweet spots",
        "\u2022  <b>Micro-Influencer Outreach Strategy</b> \u2014 Best practices for DMs, collaboration formats, zero-budget partnerships, follow-up cadence",
        "\u2022  <b>SEO Keyword Research</b> \u2014 Long-tail keyword opportunities, 8 blog topic recommendations, on-page SEO checklist, schema markup, traffic timeline",
    ]
    for r in research:
        story.append(Paragraph(r, s["CheckItem"]))

    story.append(Paragraph("Launch Plan Tasks Checked Off", s["SubHeader"]))
    checked = [
        "\u2022  [Phase 1] Identify trending Reels audio for displaced tech worker audience",
        "\u2022  [Phase 4] Draft influencer outreach DM templates",
        "\u2022  [Phase 4] Write SEO blog posts (3 of 8 written, 5 planned)",
    ]
    for c in checked:
        story.append(Paragraph(c, s["CheckItem"]))
    story.append(PageBreak())

    # ── SECTION 2: COMPLETE WORK FROM PRIOR SESSIONS ──
    story.append(Paragraph("2. All Claude Code Work (Complete)", s["SectionHeader"]))
    story.append(hr())
    story.append(Paragraph(
        "The following content has been created across all sessions. Every piece of "
        "copywriting, research, and strategy needed for launch is complete.",
        s["Body"]
    ))

    all_work = [
        ("Brand Foundation", [
            "Brand positioning, taglines, elevator pitch",
            "Brand voice guide (warm, grounded, defiant, tender)",
            "Instagram bio copy (keyword-optimized)",
            "Complete brand reframe documentation",
            "All 14 content pipeline files rewritten",
        ]),
        ("Visual Assets", [
            "Sanctuary logo (4 options + IG profile version)",
            "Kit product covers (free, paid, tripwire)",
            "3 content background images (sanctuary aesthetic)",
        ]),
        ("Content Pipeline (46+ pieces)", [
            "170+ grounding affirmations across 5 themes",
            "Affirmation ratings for resonance/shareability",
            "Captions for all 46+ posts with CTAs",
            "6 hashtag sets (3\u20135 tags each)",
            "30-day content calendar",
            "8 carousel slide scripts",
            "Reel scripts + Instagram Live script",
            "Trending Reels audio strategy guide",
        ]),
        ("Products (3 products)", [
            "5-Day Grounding Practice content (free lead magnet, 10 pages)",
            "Emergency Grounding Kit content ($9 tripwire, 15 pages)",
            "30-Day Luminous Pulse Practice content ($37\u2013$47, 30 days x 5 themes)",
        ]),
        ("Email Marketing", [
            "2-email welcome sequence",
            "5-email nurture/conversion sequence",
            "Kit product descriptions (free, tripwire, paid)",
            "Tripwire thank-you page copy + post-purchase email",
            "Lead magnet landing page copy",
            "Social proof / credibility snippets",
        ]),
        ("Marketing & Growth", [
            "10 LinkedIn posts (4 formats) + bio update",
            "Podcast guest one-sheet (bio, 3 pitches, outreach DM)",
            "6 influencer outreach DM templates + follow-up cadence",
            "3 SEO blog posts (~7,200 words total)",
            "Full SEO content strategy + keyword research",
        ]),
        ("Strategic Planning", [
            "Launch plan (5 phases, 111 days)",
            "Deepened launch plan (research-enhanced)",
            "Notion task tracker",
            "Revenue model + projections",
        ]),
    ]

    for category, items in all_work:
        story.append(Paragraph(f"<b>{category}</b>", s["SubHeader"]))
        for item in items:
            story.append(Paragraph(f"\u2713  {item}", s["CheckItemDone"]))
    story.append(PageBreak())

    # ── SECTION 3: WHAT CHRISTIE NEEDS TO DO BEFORE FEB 17 ──
    story.append(Paragraph("3. Your Pre-Launch Checklist (Feb 13\u201317)", s["SectionHeader"]))
    story.append(hr())
    story.append(Paragraph(
        "Everything below needs to be completed before the February 17 Lunar New Year launch. "
        "Tasks are organized by day with estimated time. All copy and content files are written \u2014 "
        "these are implementation tasks.",
        s["Body"]
    ))

    # Day-by-day breakdown
    story.append(Paragraph("Thursday, February 13 (Today)", s["DayHeader"]))
    story.append(Paragraph("<i>Estimated time: 1\u20132 hours</i>", s["Body"]))
    today_tasks = [
        f"{BOX}  Upload Sanctuary logo as IG profile photo (logo-ig-profile.png)",
        f"{BOX}  Update Instagram bio (use instagram-bio-copy.md Option 1)",
        f"{BOX}  Update website (luminouspulse.co) with new hero copy from brand-positioning.md",
        f"{BOX}  Set up Beacons link-in-bio (connect to: website, Kit form placeholder, IG)",
    ]
    for t_item in today_tasks:
        story.append(Paragraph(t_item, s["CheckItem"]))

    story.append(Paragraph("Friday, February 14", s["DayHeader"]))
    story.append(Paragraph("<i>Estimated time: 2\u20133 hours</i>", s["Body"]))
    fri_tasks = [
        f"{BOX}  Create Kit form for lead magnet (email capture + PDF delivery via incentive email)",
        f"{BOX}  Set up DKIM/SPF/DMARC email authentication in Kit (critical for deliverability)",
        f"{BOX}  Create the 5-Day Grounding Practice PDF in Canva (use lead-magnet-pdf-content.md)",
        f"{BOX}  Upload PDF to Kit form as incentive email attachment",
        f"{BOX}  Load welcome email sequence into Kit (from welcome-email-sequence.md)",
        f"{BOX}  Update Beacons link-in-bio with Kit form link",
    ]
    for t_item in fri_tasks:
        story.append(Paragraph(t_item, s["CheckItem"]))

    story.append(Paragraph("Saturday, February 15", s["DayHeader"]))
    story.append(Paragraph("<i>Estimated time: 4\u20136 hours</i>", s["Body"]))
    sat_tasks = [
        f"{BOX}  Design 5\u20138 master Canva templates (sanctuary aesthetic: navy bg, amber/blue accents)",
        f"{BOX}  Create first 9 static quote posts from templates (best content for grid seeding)",
        f"{BOX}  Create 2\u20133 carousels (using carousel-slide-copy.md)",
        f"{BOX}  Design Story Highlight covers (About, Practice, Free Guide, Community)",
        f"{BOX}  Test full funnel: Beacons \u2192 Kit form \u2192 PDF delivery \u2192 welcome email",
    ]
    for t_item in sat_tasks:
        story.append(Paragraph(t_item, s["CheckItem"]))

    story.append(Paragraph("Sunday, February 16", s["DayHeader"]))
    story.append(Paragraph("<i>Estimated time: 3\u20134 hours</i>", s["Body"]))
    sun_tasks = [
        f"{BOX}  Film first 2\u20133 Reels (using scripts from reel-and-live-scripts.md)",
        f"{BOX}  Record 1\u20132 grounding meditation clips (60\u201390 sec) for Stories",
        f"{BOX}  Seed Instagram grid with first 6\u20139 posts (best content first \u2014 DO NOT post yet)",
        f"{BOX}  Set up Metricool and schedule first week of content",
        f"{BOX}  Set up ManyChat DM automation (trigger word: GROUNDED \u2192 Kit form link)",
        f"{BOX}  Final review: check all links, email delivery, bio, profile photo",
    ]
    for t_item in sun_tasks:
        story.append(Paragraph(t_item, s["CheckItem"]))

    story.append(Paragraph("Monday, February 17 \u2014 LAUNCH DAY (Lunar New Year)", s["DayHeader"]))
    story.append(Paragraph("<i>Estimated time: 2\u20133 hours</i>", s["Body"]))
    launch_tasks = [
        f"{BOX}  Publish first 6\u20139 grid posts (or schedule to publish throughout the day)",
        f"{BOX}  Post first Instagram Story (grounding word + poll: \u201cHow are you actually doing?\u201d)",
        f"{BOX}  Post first LinkedIn post (use Post 1 from linkedin-posts.md: \u201cThe Meeting\u201d)",
        f"{BOX}  Begin engagement: follow 20 niche accounts, leave 10 thoughtful comments",
        f"{BOX}  Share launch on personal social media",
        f"{BOX}  Send first email to any existing contacts (personal announcement)",
    ]
    for t_item in launch_tasks:
        story.append(Paragraph(t_item, s["CheckItem"]))
    story.append(PageBreak())

    # ── SECTION 4: LAUNCH DAY CONTENT PLAN ──
    story.append(Paragraph("4. Launch Day Content Plan (Feb 17)", s["SectionHeader"]))
    story.append(hr())
    story.append(Paragraph(
        "Lunar New Year / New Moon \u2014 a symbolic day for new beginnings. "
        "Use this energy in your copy and Stories.",
        s["Body"]
    ))

    story.append(Paragraph("Grid Posts (publish 6\u20139)", s["SubHeader"]))
    story.append(Paragraph(
        "Choose the strongest content for first impressions. When someone visits your profile, "
        "they see the grid first. Every post should feel intentional and cohesive.",
        s["Body"]
    ))
    grid_recs = [
        "\u2022  2\u20133 affirmation quote cards (strongest from affirmations-150.md)",
        "\u2022  1\u20132 \u201cName the Feeling\u201d posts (highest engagement potential)",
        "\u2022  1 carousel (educational, high save rate)",
        "\u2022  1\u20132 permission/resilience posts",
        "\u2022  1 Reel (if filmed \u2014 personal story or grounding practice)",
    ]
    for g in grid_recs:
        story.append(Paragraph(g, s["CheckItem"]))

    story.append(Paragraph("Stories (3\u20135 throughout the day)", s["SubHeader"]))
    stories = [
        '\u2022  Morning: Grounding word + "Happy Lunar New Year. Today we begin."',
        '\u2022  Mid-day: Poll \u2014 "How are you actually doing today?" (Great / Surviving / Struggling / Don\'t ask)',
        '\u2022  Afternoon: Share a quote card post to Stories with "This is what we\'re about"',
        '\u2022  Evening: "Comment GROUNDED on our latest post for a free grounding practice in your DMs"',
    ]
    for st in stories:
        story.append(Paragraph(st, s["CheckItem"]))

    story.append(Paragraph("LinkedIn (Post 1: The Meeting)", s["SubHeader"]))
    story.append(Paragraph(
        "Post the vulnerability story (\u201cI was in a meeting where someone casually said, "
        "\u2018We\u2019ll just have AI do that part.\u2019\u201d) from linkedin-posts.md. This is your "
        "highest-reach content format. Post between 7\u20138 AM or 12\u20131 PM.",
        s["Body"]
    ))
    story.append(PageBreak())

    # ── SECTION 5: FIRST WEEK SCHEDULE ──
    story.append(Paragraph("5. First Week Schedule (Feb 17\u201323)", s["SectionHeader"]))
    story.append(hr())

    week_data = [
        ["Day", "Instagram", "LinkedIn", "Other"],
        ["Mon 2/17\nLAUNCH", "Seed grid (6\u20139 posts)\n3\u20135 Stories", "Post 1:\nThe Meeting", "Engage 30 min"],
        ["Tue 2/18", "Quote card\n1\u20132 Stories", "\u2014", "Engage 30 min\nReply to all DMs"],
        ["Wed 2/19", "Carousel\n1\u20132 Stories", "Post 2:\nThe 2am Scroll", "Engage 30 min"],
        ["Thu 2/20", "Quote card\n1\u20132 Stories", "\u2014", "Engage 30 min\nReply to all DMs"],
        ["Fri 2/21", "Reel\n1\u20132 Stories", "Post 3:\n873 Per Day", "Engage 30 min"],
        ["Sat 2/22", "Rest day\n1 Story", "\u2014", "Batch content\nfor next week"],
        ["Sun 2/23", "Rest day\n1 Story", "\u2014", "Film Reels\nfor next week"],
    ]
    t = make_table(week_data[0], week_data[1:], col_widths=[1*inch, 2*inch, 1.5*inch, 1.8*inch])
    story.append(t)

    story.append(Paragraph("Daily Time Investment", s["SubHeader"]))
    time_data = [
        ["Activity", "Time", "When"],
        ["Post scheduled content", "10 min", "Morning"],
        ["Post 1\u20132 Stories", "15 min", "Throughout day"],
        ["Engage (comments on niche accounts)", "30 min", "Afternoon"],
        ["Reply to comments and DMs", "15 min", "Evening"],
        ["Total", "~70 min/day", ""],
    ]
    t = make_table(time_data[0], time_data[1:], col_widths=[2.5*inch, 1.5*inch, 2.3*inch])
    story.append(t)
    story.append(PageBreak())

    # ── SECTION 6: KEY FILES REFERENCE ──
    story.append(Paragraph("6. Key Files Quick Reference", s["SectionHeader"]))
    story.append(hr())
    story.append(Paragraph(
        "All files are in: /Users/christieparrow/luminous-pulse/",
        s["Body"]
    ))

    ref_data = [
        ["Task", "File to Use"],
        ["Update Instagram bio", "instagram-bio-copy.md (Option 1)"],
        ["Update website copy", "brand-positioning.md"],
        ["Create lead magnet PDF", "lead-magnet-pdf-content.md"],
        ["Set up Kit form", "kit-product-description.md"],
        ["Write welcome emails in Kit", "welcome-email-sequence.md"],
        ["Write carousel slides", "carousel-slide-copy.md"],
        ["Choose affirmations for posts", "affirmations-150.md"],
        ["Write post captions", "post-captions.md"],
        ["Pick hashtags", "hashtag-sets.md"],
        ["Film Reels", "reel-and-live-scripts.md"],
        ["Choose Reels audio", "instagram-reels-audio-strategy-2026.md"],
        ["Post on LinkedIn", "linkedin-posts.md"],
        ["Follow content schedule", "content-calendar.md"],
        ["Set up tripwire ($9)", "kit-tripwire-product-description.md"],
        ["IG profile photo", "logo-ig-profile.png"],
        ["Kit cover images", "kit-cover-free-practice.png, kit-cover-paid-practice.png"],
        ["Post backgrounds", "instagram/bg-quote-navy-amber.png, etc."],
    ]
    t = make_table(ref_data[0], ref_data[1:], col_widths=[2.5*inch, 3.8*inch])
    story.append(t)
    story.append(PageBreak())

    # ── SECTION 7: FUNNEL TESTING CHECKLIST ──
    story.append(Paragraph("7. Funnel Testing Checklist (Before Launch)", s["SectionHeader"]))
    story.append(hr())
    story.append(Paragraph(
        "Test every step of the funnel on Sunday, February 16. Use your personal email.",
        s["Body"]
    ))

    funnel_tests = [
        f"{BOX}  Click Beacons link-in-bio \u2192 does it load? Are all links correct?",
        f"{BOX}  Click \u201cFree Grounding Practice\u201d link \u2192 does Kit form load?",
        f"{BOX}  Submit Kit form with test email \u2192 does confirmation page show?",
        f"{BOX}  Check email \u2192 did incentive email arrive? Is PDF attached?",
        f"{BOX}  Open PDF \u2192 does it look correct? Are all 10 pages present?",
        f"{BOX}  Does thank-you page show $9 tripwire offer?",
        f"{BOX}  Wait 1 day \u2192 does welcome email #1 arrive?",
        f"{BOX}  Comment \u201cGROUNDED\u201d on a test post \u2192 does ManyChat DM fire?",
        f"{BOX}  Does DM contain correct Kit form link?",
        f"{BOX}  Check that website (luminouspulse.co) loads and looks correct",
        f"{BOX}  Check that all IG highlights have covers and correct content",
    ]
    for ft in funnel_tests:
        story.append(Paragraph(ft, s["CheckItem"]))

    story.append(Paragraph("If Something Breaks", s["SubHeader"]))
    breaks = [
        "\u2022  <b>Email not arriving:</b> Check Kit form settings \u2192 Incentive email must be enabled. Check spam folder. Verify DKIM/SPF.",
        "\u2022  <b>PDF not attached:</b> Re-upload to Kit form incentive email settings. Max file size: 5MB.",
        "\u2022  <b>ManyChat not responding:</b> Check keyword trigger is exactly \u201cGROUNDED\u201d (case-sensitive). Verify automation is active.",
        "\u2022  <b>Beacons links broken:</b> Re-check each link URL. Test in incognito browser.",
    ]
    for b in breaks:
        story.append(Paragraph(b, s["CheckItem"]))
    story.append(PageBreak())

    # ── SECTION 8: LAUNCH DAY REMINDERS ──
    story.append(Paragraph("8. Launch Day Reminders", s["SectionHeader"]))
    story.append(hr())

    story.append(Paragraph("Posting Best Practices", s["SubHeader"]))
    reminders = [
        "\u2022  Best Instagram posting times: 6\u20139 AM and 12\u20133 PM (your timezone)",
        "\u2022  Best LinkedIn posting times: 7\u20138 AM or 12\u20131 PM (Tuesday\u2013Thursday best)",
        "\u2022  Reply to every comment within 24 hours (boosts algorithm)",
        "\u2022  Reply to every DM (even if just \u201cThank you, this means a lot\u201d)",
        "\u2022  Engage with 5\u201310 accounts in your niche daily (thoughtful comments, not generic)",
        "\u2022  Use 3\u20135 hashtags per post (in caption, not comments)",
        "\u2022  Post Stories daily (algorithm rewards consistency)",
        "\u2022  Save trending audio when scrolling (look for upward arrow \u2191)",
    ]
    for rem in reminders:
        story.append(Paragraph(rem, s["CheckItem"]))

    story.append(Paragraph("Mindset for Launch Week", s["SubHeader"]))
    story.append(Paragraph(
        '<i>"The practice is not about feeling better. It\u2019s about feeling grounded. '
        'The difference matters."</i>',
        s["Quote"]
    ))
    mindset = [
        "\u2022  Growth will be slow at first \u2014 that\u2019s normal and expected",
        "\u2022  Focus on engagement quality over follower count",
        "\u2022  Saves and shares matter 3\u20135x more than likes",
        "\u2022  Your first 50 followers are the hardest. After that, momentum builds",
        "\u2022  Document everything \u2014 your own experience is your best content",
        "\u2022  This is a new moon. A beginning. Let it be a beginning.",
    ]
    for m in mindset:
        story.append(Paragraph(m, s["CheckItem"]))

    # Final page
    story.append(Spacer(1, 36))
    story.append(hr())
    story.append(Spacer(1, 12))
    story.append(Paragraph(
        "Everything is written. Everything is ready. The only thing left is you.",
        s["Callout"]
    ))
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "luminouspulse.co  |  @luminouspulse  |  Christie Parrow",
        s["SmallText"]
    ))
    story.append(Paragraph(
        "You are held.",
        s["Quote"]
    ))

    doc.build(story, onFirstPage=add_footer, onLaterPages=add_footer)
    print(f"Work summary PDF created: {filename}")


if __name__ == "__main__":
    build_pdf()
