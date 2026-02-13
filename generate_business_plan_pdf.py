#!/usr/bin/env python3
"""Generate comprehensive business plan PDF for Luminous Pulse."""

from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import HexColor
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.platypus.flowables import KeepTogether

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


def create_styles():
    styles = getSampleStyleSheet()

    styles.add(ParagraphStyle(
        name="CoverTitle",
        fontName="Helvetica-Bold",
        fontSize=32,
        textColor=NAVY,
        alignment=TA_LEFT,
        spaceAfter=8,
        leading=38,
    ))
    styles.add(ParagraphStyle(
        name="CoverSubtitle",
        fontName="Helvetica",
        fontSize=14,
        textColor=SOFT_NAVY,
        alignment=TA_LEFT,
        spaceAfter=6,
        leading=20,
    ))
    styles.add(ParagraphStyle(
        name="CoverTagline",
        fontName="Helvetica-Oblique",
        fontSize=11,
        textColor=MED_GRAY,
        alignment=TA_LEFT,
        spaceAfter=4,
        leading=16,
    ))
    styles.add(ParagraphStyle(
        name="SectionHeader",
        fontName="Helvetica-Bold",
        fontSize=20,
        textColor=NAVY,
        spaceBefore=24,
        spaceAfter=12,
        leading=24,
    ))
    styles.add(ParagraphStyle(
        name="SubHeader",
        fontName="Helvetica-Bold",
        fontSize=13,
        textColor=SOFT_NAVY,
        spaceBefore=16,
        spaceAfter=6,
        leading=16,
    ))
    styles.add(ParagraphStyle(
        name="Body",
        fontName="Helvetica",
        fontSize=10,
        textColor=DARK_GRAY,
        spaceAfter=6,
        leading=14,
    ))
    styles.add(ParagraphStyle(
        name="BodyBold",
        fontName="Helvetica-Bold",
        fontSize=10,
        textColor=DARK_GRAY,
        spaceAfter=6,
        leading=14,
    ))
    styles.add(ParagraphStyle(
        name="BulletItem",
        fontName="Helvetica",
        fontSize=10,
        textColor=DARK_GRAY,
        leftIndent=20,
        spaceAfter=3,
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
        leading=16,
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
        name="Metric",
        fontName="Helvetica-Bold",
        fontSize=22,
        textColor=BLUE,
        alignment=TA_CENTER,
        spaceAfter=2,
        leading=26,
    ))
    styles.add(ParagraphStyle(
        name="MetricLabel",
        fontName="Helvetica",
        fontSize=9,
        textColor=MED_GRAY,
        alignment=TA_CENTER,
        spaceAfter=8,
        leading=12,
    ))
    return styles


def hr():
    return HRFlowable(
        width="100%", thickness=1, color=LAVENDER,
        spaceBefore=8, spaceAfter=8
    )


def thin_hr():
    return HRFlowable(
        width="100%", thickness=0.5, color=HexColor("#e0e0e0"),
        spaceBefore=4, spaceAfter=4
    )


def make_table(headers, rows, col_widths=None):
    """Create a styled table."""
    s = create_styles()
    header_row = [Paragraph(h, s["TableHeader"]) for h in headers]
    data = [header_row]
    for row in rows:
        data.append([Paragraph(str(c), s["TableCell"]) for c in row])

    if col_widths is None:
        col_widths = [None] * len(headers)

    t = Table(data, colWidths=col_widths, repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, 0), 9),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
        ("TOPPADDING", (0, 0), (-1, 0), 8),
        ("BACKGROUND", (0, 1), (-1, -1), WHITE),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, LIGHT_GRAY]),
        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 1), (-1, -1), 9),
        ("TOPPADDING", (0, 1), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 1), (-1, -1), 6),
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
    canvas.drawString(
        72, 36,
        "Luminous Pulse  |  luminouspulse.co  |  @luminouspulse"
    )
    canvas.drawRightString(
        letter[0] - 72, 36,
        f"Page {doc.page}"
    )
    # Top accent line
    canvas.setStrokeColor(BLUE)
    canvas.setLineWidth(2)
    canvas.line(72, letter[1] - 36, letter[0] - 72, letter[1] - 36)
    canvas.restoreState()


def build_pdf():
    filename = "/Users/christieparrow/affirmations-project/Luminous-Pulse-Business-Plan.pdf"
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

    # ── COVER PAGE ──
    story.append(Spacer(1, 1.5 * inch))
    story.append(Paragraph("Luminous Pulse", s["CoverTitle"]))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "Comprehensive Business Plan",
        s["CoverSubtitle"]
    ))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "Grounding Practices for Displaced Tech Workers",
        s["CoverSubtitle"]
    ))
    story.append(Spacer(1, 16))
    story.append(hr())
    story.append(Spacer(1, 12))
    story.append(Paragraph(
        '"Where displaced humans come to rest."',
        s["Quote"]
    ))
    story.append(Spacer(1, 24))
    story.append(Paragraph(
        "Founder: Christie Parrow  |  PMP-Certified Project Manager  |  7+ Years in Tech",
        s["Body"]
    ))
    story.append(Paragraph(
        "luminouspulse.co  |  @luminouspulse  |  February 2026",
        s["Body"]
    ))
    story.append(Spacer(1, 48))
    story.append(Paragraph(
        "Budget: Under $50/month  |  Primary Platform: Instagram  |  Launch: February 17, 2026 (Lunar New Year)",
        s["BodyBold"]
    ))
    story.append(PageBreak())

    # ── TABLE OF CONTENTS ──
    story.append(Paragraph("Contents", s["SectionHeader"]))
    story.append(hr())
    toc_items = [
        "1. Executive Summary",
        "2. The Opportunity",
        "3. Brand Positioning",
        "4. Target Audience",
        "5. Product Ladder",
        "6. Revenue Model & Projections",
        "7. Tech Stack",
        "8. Content Strategy",
        "9. Launch Phases",
        "10. Growth Milestones",
        "11. Competitive Landscape",
        "12. SEO & Blog Strategy",
        "13. Asset Inventory",
    ]
    for item in toc_items:
        story.append(Paragraph(item, s["Body"]))
    story.append(PageBreak())

    # ── 1. EXECUTIVE SUMMARY ──
    story.append(Paragraph("1. Executive Summary", s["SectionHeader"]))
    story.append(hr())
    story.append(Paragraph(
        "Luminous Pulse is a digital wellness brand creating grounding practices specifically for "
        "displaced tech workers. In a market where 430,000+ tech professionals have been displaced "
        "since 2024 \u2014 with ~873 more every day \u2014 there is no brand addressing the emotional "
        "and identity crisis underneath the career crisis.",
        s["Body"]
    ))
    story.append(Paragraph(
        "Everyone tells displaced workers to upskill. Nobody asks how they\u2019re actually doing. "
        "Luminous Pulse fills that gap with grounding affirmations, breathwork practices, and "
        "daily rituals that help people remember who they are beyond their job title.",
        s["Body"]
    ))
    story.append(Paragraph(
        "The business model is content-first: Instagram drives awareness, a free lead magnet "
        "captures emails, and an automated email funnel converts subscribers into customers for "
        "digital products ($9\u2013$47). Total operating cost is under $14/month.",
        s["Body"]
    ))

    story.append(Paragraph("Key Numbers", s["SubHeader"]))
    metrics_data = [
        ["430,000+", "Tech workers displaced\nsince 2024"],
        ["$1\u201314/mo", "Total operating\ncost"],
        ["$9\u2013$47", "Product price\nrange"],
        ["3\u20135%", "Expected email-to-\npurchase conversion"],
    ]
    metric_cells = []
    for val, label in metrics_data:
        cell = [
            Paragraph(val, s["Metric"]),
            Paragraph(label, s["MetricLabel"]),
        ]
        metric_cells.append(cell)

    # Simple approach - just list them
    for val, label in metrics_data:
        story.append(Paragraph(f"<b>{val}</b> \u2014 {label.replace(chr(10), ' ')}", s["Body"]))

    story.append(PageBreak())

    # ── 2. THE OPPORTUNITY ──
    story.append(Paragraph("2. The Opportunity", s["SectionHeader"]))
    story.append(hr())
    story.append(Paragraph(
        "The tech industry is experiencing its most significant workforce disruption in decades. "
        "This creates a large, underserved audience with acute emotional needs:",
        s["Body"]
    ))
    bullets = [
        "\u2022  430,000+ tech workers displaced since 2024; ~873 per day in early 2026",
        "\u2022  28.5% of 2025 layoffs directly tied to AI adoption",
        "\u2022  75% of employees are concerned AI will make their job obsolete",
        "\u2022  54% of U.S. workers experience stress spikes due to job insecurity",
        "\u2022  220 million LinkedIn users have \u201cOpen to Work\u201d enabled",
    ]
    for b in bullets:
        story.append(Paragraph(b, s["BulletItem"]))

    story.append(Paragraph("The White Space", s["SubHeader"]))
    story.append(Paragraph(
        "The career coaching market tells people to upskill. The wellness market offers generic "
        "affirmations. Nobody occupies the intersection: specific, grounded emotional support "
        "for tech workers navigating displacement. Luminous Pulse is the first mover in this space.",
        s["Body"]
    ))

    story.append(Paragraph("Post-Layoff Emotional Journey", s["SubHeader"]))
    journey = [
        ["Stage", "Timeline", "What They Need"],
        ["Shock & Relief", "Week 1\u20132", "Permission to feel, grounding"],
        ["Anger & Grief", "Week 3\u20134", "Validation, naming the feeling"],
        ["Identity Crisis", "Month 2\u20133", "Who am I without my title?"],
        ["Bargaining", "Month 3\u20134", "Should I just learn AI?"],
        ["Reconstruction", "Month 4\u20136", "Rebuilding identity, grounded hope"],
    ]
    t = make_table(journey[0], journey[1:], col_widths=[1.6*inch, 1.2*inch, 3.5*inch])
    story.append(t)
    story.append(PageBreak())

    # ── 3. BRAND POSITIONING ──
    story.append(Paragraph("3. Brand Positioning", s["SectionHeader"]))
    story.append(hr())
    story.append(Paragraph(
        "For tech professionals who\u2019ve been laid off, displaced, or are watching their industry "
        "reshape beneath their feet, Luminous Pulse is the place where you come to feel less alone "
        "and more in possession of your own power.",
        s["Body"]
    ))
    story.append(Paragraph(
        "Unlike generic affirmation accounts that ignore what\u2019s happening, and unlike AI hype "
        "accounts that treat disruption as entertainment, we sit in the real fear with you \u2014 "
        "and help you transform it into clarity, strength, and grounded hope.",
        s["Body"]
    ))

    story.append(Paragraph("Brand Voice", s["SubHeader"]))
    voice_items = [
        "\u2022  <b>Warm</b> \u2014 Like a friend who brings you coffee and doesn\u2019t ask what\u2019s next",
        "\u2022  <b>Grounded</b> \u2014 Rooted in reality, not toxic positivity or doom",
        "\u2022  <b>Defiant</b> \u2014 Quietly refuses the narrative that you\u2019re disposable",
        "\u2022  <b>Tender</b> \u2014 Meets people in vulnerability, never shame",
    ]
    for v in voice_items:
        story.append(Paragraph(v, s["BulletItem"]))

    story.append(Paragraph("Tagline", s["SubHeader"]))
    story.append(Paragraph(
        '<i>"Your humanity is not the problem. It is the answer."</i>',
        s["Quote"]
    ))

    story.append(Paragraph("Content Pillars", s["SubHeader"]))
    pillars = [
        "\u2022  <b>Name the Feeling</b> \u2014 Naming the specific grief of displacement",
        "\u2022  <b>Remember Who You Are</b> \u2014 Identity beyond job titles",
        "\u2022  <b>Ground Yourself</b> \u2014 Breathwork, affirmations, daily rituals",
        "\u2022  <b>You Are Not Alone</b> \u2014 Community, shared stories, vulnerability",
        "\u2022  <b>The World We\u2019re Building</b> \u2014 Grounded hope for the future",
    ]
    for p in pillars:
        story.append(Paragraph(p, s["BulletItem"]))

    story.append(Paragraph("Design System", s["SubHeader"]))
    design_data = [
        ["Element", "Specification"],
        ["Primary Blue", "#6CB4EE"],
        ["Amber Accent", "#F4C430"],
        ["Lavender", "#B4A7D6"],
        ["Navy Background", "#1a2744"],
        ["Font", "Helvetica Neue"],
        ["Aesthetic", "Sanctuary \u2014 warm light, gentle glow, calm navy"],
    ]
    t = make_table(design_data[0], design_data[1:], col_widths=[2.5*inch, 3.8*inch])
    story.append(t)
    story.append(PageBreak())

    # ── 4. TARGET AUDIENCE ──
    story.append(Paragraph("4. Target Audience", s["SectionHeader"]))
    story.append(hr())
    story.append(Paragraph(
        "<b>Primary:</b> Displaced tech workers (25\u201345) \u2014 PMs, engineers, designers, marketers "
        "who\u2019ve been laid off, fear they\u2019re next, or are watching their industry reshape itself.",
        s["Body"]
    ))
    story.append(Paragraph(
        "<b>Secondary:</b> Early-career tech workers (22\u201330) entering a job market that looks "
        "nothing like what they were promised.",
        s["Body"]
    ))
    story.append(Paragraph("Psychographic Profile", s["SubHeader"]))
    story.append(Paragraph(
        "They got the Slack message on a Tuesday. Or they\u2019re watching rounds of layoffs hit "
        "their team. They scroll LinkedIn at midnight and see people celebrating AI tools while "
        "quietly wondering if they\u2019re being replaced. They wish someone would sit with them in "
        "that feeling \u2014 not dismiss it, not exploit it, but hold it.",
        s["Body"]
    ))
    story.append(Paragraph("Where They Gather", s["SubHeader"]))
    where = [
        "\u2022  LinkedIn (220M+ \u201cOpen to Work\u201d users)",
        "\u2022  Instagram (wellness, mental health, career content)",
        "\u2022  Reddit: r/layoffs, r/careerguidance, r/cscareerquestions",
        "\u2022  Blind (anonymous tech worker forum)",
        "\u2022  Discord communities for tech career support",
    ]
    for w in where:
        story.append(Paragraph(w, s["BulletItem"]))
    story.append(PageBreak())

    # ── 5. PRODUCT LADDER ──
    story.append(Paragraph("5. Product Ladder", s["SectionHeader"]))
    story.append(hr())
    products = [
        ["Product", "Price", "Format", "Purpose"],
        ["The 5-Day Grounding Practice", "Free", "PDF (10 pages)", "Lead magnet \u2014 email capture"],
        ["The Emergency Grounding Kit", "$9", "PDF (15 pages)", "Tripwire \u2014 immediate conversion"],
        ["The 30-Day Luminous Pulse Practice", "$27\u2013$47", "PDF (40+ pages)", "Core product \u2014 main revenue"],
    ]
    t = make_table(products[0], products[1:], col_widths=[2.2*inch, 0.7*inch, 1.3*inch, 2.1*inch])
    story.append(t)

    story.append(Spacer(1, 12))
    story.append(Paragraph("Product Details", s["SubHeader"]))

    story.append(Paragraph("<b>Free: The 5-Day Grounding Practice</b>", s["BodyBold"]))
    story.append(Paragraph(
        "5 day cards, each with one affirmation + breathwork exercise + reflection prompt. "
        "Delivered via Kit form incentive email. Primary purpose: email capture and trust building.",
        s["Body"]
    ))

    story.append(Paragraph("<b>$9 Tripwire: The Emergency Grounding Kit</b>", s["BodyBold"]))
    story.append(Paragraph(
        "10 emergency grounding cards for specific displaced-worker moments (the Slack message, "
        "the 2am spiral, the identity crisis, the 200th application). Shown on Kit thank-you page "
        "after free download. Expected 10\u201315% conversion. Buyers are 3\u20135x more likely to "
        "purchase the $37 product.",
        s["Body"]
    ))

    story.append(Paragraph("<b>$27\u2013$47: The 30-Day Luminous Pulse Practice</b>", s["BodyBold"]))
    story.append(Paragraph(
        "30 grounding affirmations across 5 themes with daily breathwork, reflection prompts, and "
        "a morning practice framework. $27 founder\u2019s price \u2192 $37 launch \u2192 $47 regular. "
        "Sold on Kit Commerce (3.5% + $0.30 per transaction).",
        s["Body"]
    ))
    story.append(PageBreak())

    # ── 6. REVENUE MODEL ──
    story.append(Paragraph("6. Revenue Model & Projections", s["SectionHeader"]))
    story.append(hr())
    story.append(Paragraph("Funnel Architecture", s["SubHeader"]))
    funnel_steps = [
        "1.  Instagram content \u2192 Bio link \u2192 Lead magnet download (email capture)",
        "2.  Kit form delivers free 5-Day Practice PDF via incentive email",
        "3.  Thank-you page shows $9 Emergency Kit tripwire (10\u201315% convert)",
        "4.  Welcome sequence (2 emails over 5 days) builds trust",
        "5.  Nurture sequence (5 emails over 14 days) converts to $37 product",
        "6.  Expected 3\u20135% of subscribers convert to paid product",
    ]
    for step in funnel_steps:
        story.append(Paragraph(step, s["BulletItem"]))

    story.append(Paragraph("Revenue Projections", s["SubHeader"]))
    rev_data = [
        ["Subscribers", "Tripwire Rev ($9)", "Main Product Rev ($37)", "Total Est. Revenue"],
        ["100", "$90\u2013135", "$111\u2013185", "$201\u2013320"],
        ["500", "$450\u2013675", "$555\u2013925", "$1,005\u20131,600"],
        ["1,000", "$900\u20131,350", "$1,110\u20131,850", "$2,010\u20133,200"],
        ["2,500", "$2,250\u20133,375", "$2,775\u20134,625", "$5,025\u20138,000"],
    ]
    t = make_table(rev_data[0], rev_data[1:], col_widths=[1.2*inch, 1.5*inch, 1.8*inch, 1.8*inch])
    story.append(t)

    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "<i>Assumes 10% tripwire conversion and 3\u20135% main product conversion.</i>",
        s["SmallText"]
    ))

    story.append(Paragraph("Monthly Operating Costs", s["SubHeader"]))
    cost_data = [
        ["Item", "Cost"],
        ["Kit (ConvertKit) Free Tier", "$0"],
        ["Metricool Free Tier", "$0"],
        ["ManyChat Free Tier", "$0"],
        ["Beacons Free Tier", "$0"],
        ["Canva (Free or Pro)", "$0\u201313"],
        ["Vercel Hosting", "$0"],
        ["Domain (luminouspulse.co)", "~$1"],
        ["CapCut Free", "$0"],
        ["Total", "$1\u201314/month"],
    ]
    t = make_table(cost_data[0], cost_data[1:], col_widths=[3.5*inch, 2.8*inch])
    story.append(t)
    story.append(PageBreak())

    # ── 7. TECH STACK ──
    story.append(Paragraph("7. Tech Stack", s["SectionHeader"]))
    story.append(hr())
    stack_data = [
        ["Tool", "Purpose", "Key Constraints"],
        ["Kit Free", "Email capture, PDF delivery, sequences, commerce", "1 sequence, 1 automation, 10K subscribers"],
        ["Metricool Free", "Content scheduling", "50 posts/month, 1 brand, 30-day analytics"],
        ["ManyChat Free", "DM automation (keyword: GROUNDED)", "1,000 contacts, 3 triggers, no Kit integration"],
        ["Beacons Free", "Link-in-bio hub", "Kit form link, website, IG highlights"],
        ["Canva Free/Pro", "Design templates and assets", "Pro ($13) for brand kit and resize"],
        ["Vercel", "Website hosting (luminouspulse.co)", "Free tier, automatic deploys"],
        ["CapCut Free", "Video editing for Reels", "Full-featured free tier"],
    ]
    t = make_table(stack_data[0], stack_data[1:], col_widths=[1.2*inch, 2.3*inch, 2.8*inch])
    story.append(t)

    story.append(Paragraph("Key Technical Notes", s["SubHeader"]))
    tech_notes = [
        "\u2022  Kit free tier uses form incentive emails (not automations) for PDF delivery",
        "\u2022  ManyChat free tier cannot integrate with Kit \u2014 route DM users to Kit form link",
        "\u2022  Set up DKIM/SPF/DMARC for Kit email authentication (19.83% spam rate without it)",
        "\u2022  Kit Commerce takes 3.5% + $0.30 per transaction",
        "\u2022  Metricool AI scheduling picks optimal post times from heat map data",
    ]
    for n in tech_notes:
        story.append(Paragraph(n, s["BulletItem"]))
    story.append(PageBreak())

    # ── 8. CONTENT STRATEGY ──
    story.append(Paragraph("8. Content Strategy", s["SectionHeader"]))
    story.append(hr())
    story.append(Paragraph("Instagram (Primary Platform)", s["SubHeader"]))
    story.append(Paragraph(
        "<b>Posting cadence:</b> 5x/week + daily Stories",
        s["Body"]
    ))
    cadence = [
        ["Day", "Content Type", "Purpose"],
        ["Monday", "Quote Card (affirmation)", "Grounding + saves"],
        ["Tuesday", "Quote Card (Name the Feeling)", "Emotional resonance + shares"],
        ["Wednesday", "Carousel (educational)", "Authority + saves + follows"],
        ["Thursday", "Quote Card (permission/resilience)", "Community + shares"],
        ["Friday", "Reel (storytelling or practice)", "Reach + new followers"],
        ["Daily", "1\u20132 Stories (polls, Q&A, grounding)", "Engagement + algorithm boost"],
    ]
    t = make_table(cadence[0], cadence[1:], col_widths=[1.2*inch, 2.3*inch, 2.8*inch])
    story.append(t)

    story.append(Paragraph("Instagram Algorithm (2026)", s["SubHeader"]))
    algo = [
        "\u2022  Views are the primary metric; shares/saves weighted 3\u20135x over likes",
        "\u2022  Reels reach: 30.81% (highest); Carousels engagement: 10.15% (highest)",
        "\u2022  Voiceovers + original audio get algorithmic preference",
        "\u2022  Instagram penalizes recycled TikTok content with watermarks",
        "\u2022  Retention and replays matter more than likes",
    ]
    for a in algo:
        story.append(Paragraph(a, s["BulletItem"]))

    story.append(Paragraph("LinkedIn (Secondary Platform)", s["SubHeader"]))
    story.append(Paragraph(
        "2\u20133 posts/week from Christie\u2019s personal profile. Vulnerability posts get 50K\u2013500K "
        "impressions. Personal profiles get 10x more reach than company pages. 10 posts written "
        "across vulnerability story, validation, data + insight, and grounding practice formats.",
        s["Body"]
    ))

    story.append(Paragraph("SEO Blog Strategy", s["SubHeader"]))
    story.append(Paragraph(
        "8 blog posts planned targeting low-competition, high-intent keywords. First 3 written: "
        "identity crisis after job loss, affirmations after layoff, AI job anxiety. Expected "
        "timeline: 3\u20136 months for initial rankings, 6\u201312 months for meaningful traffic.",
        s["Body"]
    ))
    story.append(PageBreak())

    # ── 9. LAUNCH PHASES ──
    story.append(Paragraph("9. Launch Phases", s["SectionHeader"]))
    story.append(hr())

    phases = [
        ("Phase 0: Brand Foundation (Days 1\u20137)", "MOSTLY COMPLETE",
         "Brand name, domain, Instagram, color palette, fonts, logo, brand voice, positioning."),
        ("Phase 1: Content Stockpile (Days 8\u201318)", "IN PROGRESS",
         "46+ pieces of content ready before first post. 170+ affirmations written, all captions "
         "and copy complete. Remaining: film Reels, design Canva templates, create static posts."),
        ("Phase 2: Pre-Launch Setup (Days 19\u201321)", "NEXT",
         "Seed Instagram grid (6\u20139 posts), create Kit form, build lead magnet PDF in Canva, "
         "load email sequences, connect Beacons, test full funnel."),
        ("Phase 3: Launch & Build (Days 22\u201351)", "PLANNED",
         "First 30 active posting days. 5x/week + daily Stories. Daily engagement (30 min). "
         "Weekly batch content creation. First Instagram Live on Day 21."),
        ("Phase 4: Accelerate (Days 52\u201381)", "PLANNED",
         "Launch paid product on Kit Commerce. 7-day grounding challenge. Micro-influencer "
         "outreach (20 creators). DM templates and outreach cadence ready."),
        ("Phase 5: Scale (Days 82\u2013111)", "PLANNED",
         "Paid ads ($5\u201310/day). TikTok launch. Weekly email newsletter. Content repurposing "
         "pipeline. Pinterest expansion."),
    ]
    for title, status, desc in phases:
        story.append(Paragraph(f"<b>{title}</b> \u2014 {status}", s["SubHeader"]))
        story.append(Paragraph(desc, s["Body"]))
    story.append(PageBreak())

    # ── 10. GROWTH MILESTONES ──
    story.append(Paragraph("10. Growth Milestones", s["SectionHeader"]))
    story.append(hr())
    milestones = [
        ["Milestone", "Day 30", "Day 60", "Day 90"],
        ["Followers", "200\u2013500", "1,000\u20132,500", "2,500\u20135,000"],
        ["Email Subscribers", "50\u2013100", "200\u2013500", "500\u20131,000"],
        ["Engagement Rate", "5%+", "5%+", "5%+"],
        ["Lead Magnet Downloads", "30\u201350", "100\u2013250", "300\u2013500"],
        ["Revenue", "\u2014", "$100\u2013500", "$500\u20132,000"],
        ["Influencer Collabs", "\u2014", "1 completed", "3\u20135 completed"],
        ["Paid Ads", "\u2014", "\u2014", "$5\u201310/day active"],
    ]
    t = make_table(milestones[0], milestones[1:], col_widths=[1.8*inch, 1.4*inch, 1.4*inch, 1.7*inch])
    story.append(t)

    story.append(Paragraph("Validation Checkpoint (Day 14)", s["SubHeader"]))
    story.append(Paragraph(
        "Before going deeper, validate demand: 10+ grounding posts live with 5%+ engagement rate, "
        "at least 50 followers from organic content, DM automation getting responses. If failing: "
        "adjust hooks, test different content pillars, lean into \u201cName the Feeling\u201d content.",
        s["Body"]
    ))
    story.append(PageBreak())

    # ── 11. COMPETITIVE LANDSCAPE ──
    story.append(Paragraph("11. Competitive Landscape", s["SectionHeader"]))
    story.append(hr())
    comp_data = [
        ["Competitor", "Their Angle", "Our Differentiation"],
        ["@iam.affirmations", "Generic positivity", "We name the specific grief of displacement"],
        ["@thegoodquote", "Literary quotes", "Original words for a feeling no one else names"],
        ["@mindsetofgreatness", "Hustle culture", "Tenderness and healing, not \u201cpivot harder\u201d"],
        ["@theholisticpsychologist", "Nervous system theory", "Same depth, specific to tech displacement"],
        ["LinkedIn career coaches", "Upskill / Network / Pivot", "Address the identity crisis first"],
    ]
    t = make_table(comp_data[0], comp_data[1:], col_widths=[1.8*inch, 1.8*inch, 2.7*inch])
    story.append(t)

    story.append(Spacer(1, 12))
    story.append(Paragraph(
        "<b>Our moat:</b> The intersection of grounded healing + tech displacement + human connection "
        "is wide open. Zero brands specifically serve the emotional wellness needs of displaced tech "
        "workers. We are first movers.",
        s["Body"]
    ))
    story.append(PageBreak())

    # ── 12. SEO & BLOG STRATEGY ──
    story.append(Paragraph("12. SEO & Blog Strategy", s["SectionHeader"]))
    story.append(hr())
    story.append(Paragraph(
        "Target low-competition, high-intent keywords where luminouspulse.co can rank within "
        "3\u20136 months. The niche \u201ctech workers + layoffs + mental health\u201d has minimal competition.",
        s["Body"]
    ))
    seo_data = [
        ["Target Keyword", "Est. Monthly Searches", "Competition", "Blog Post Status"],
        ["identity crisis after job loss", "200\u2013800", "Medium", "Written"],
        ["affirmations after getting laid off", "100\u2013500", "Low", "Written"],
        ["AI replacing my job anxiety", "100\u2013300", "Low", "Written"],
        ["tech layoff mental health", "500\u20131,000", "Medium", "Planned (Month 2)"],
        ["grounding exercises for career anxiety", "50\u2013150", "Very Low", "Planned (Month 2)"],
        ["job loss depression", "1,000\u20132,000", "Medium", "Planned (Month 3)"],
        ["mindfulness for career transition", "50\u2013200", "Low", "Planned (Month 3)"],
    ]
    t = make_table(seo_data[0], seo_data[1:], col_widths=[2.2*inch, 1.2*inch, 1*inch, 1.8*inch])
    story.append(t)

    story.append(Paragraph("Traffic Expectations", s["SubHeader"]))
    traffic = [
        "\u2022  Months 1\u20132: 0\u201350 visitors (pages indexed, no rankings)",
        "\u2022  Months 3\u20134: 50\u2013200 visitors (long-tail keywords ranking)",
        "\u2022  Months 5\u20136: 200\u2013500 visitors (page 1 for specific queries)",
        "\u2022  Months 7\u20139: 500\u20131,500 visitors (medium keywords ranking)",
        "\u2022  Months 10\u201312: 1,500\u20133,000 visitors (established authority)",
    ]
    for tr in traffic:
        story.append(Paragraph(tr, s["BulletItem"]))
    story.append(PageBreak())

    # ── 13. ASSET INVENTORY ──
    story.append(Paragraph("13. Complete Asset Inventory", s["SectionHeader"]))
    story.append(hr())
    story.append(Paragraph(
        "All copywriting and content assets have been created by Claude Code. "
        "Below is the full inventory of ready-to-use files.",
        s["Body"]
    ))

    asset_categories = [
        ("Brand Foundation", [
            "brand-positioning.md \u2014 Positioning statement, taglines, content pillars",
            "brand-voice-guide.md \u2014 Voice guide (warm, grounded, defiant, tender)",
            "instagram-bio-copy.md \u2014 Keyword-optimized bio options",
            "brand-reframe.md \u2014 Complete pivot documentation",
        ]),
        ("Content Pipeline", [
            "affirmations-150.md \u2014 170+ grounding affirmations across 5 themes",
            "post-captions.md \u2014 Captions for 46+ posts with CTAs",
            "carousel-slide-copy.md \u2014 8 carousel scripts",
            "reel-and-live-scripts.md \u2014 Reel scripts + Instagram Live script",
            "hashtag-sets.md \u2014 6 sets of 3\u20135 tags each",
            "content-calendar.md \u2014 30-day calendar",
            "instagram-reels-audio-strategy-2026.md \u2014 Trending audio guide",
        ]),
        ("Products", [
            "lead-magnet-pdf-content.md \u2014 5-Day Grounding Practice (free)",
            "tripwire-product-content.md \u2014 Emergency Grounding Kit ($9)",
            "paid-affirmation-card-deck-50.md \u2014 30-Day Practice ($37\u2013$47)",
        ]),
        ("Email Marketing", [
            "welcome-email-sequence.md \u2014 2-email welcome sequence",
            "email-nurture-sequence.md \u2014 5-email conversion sequence",
        ]),
        ("Kit Commerce", [
            "kit-product-description.md \u2014 Free lead magnet listing",
            "kit-tripwire-product-description.md \u2014 $9 tripwire listing + thank-you page",
            "kit-paid-product-description.md \u2014 $37 paid product listing",
        ]),
        ("Marketing & Growth", [
            "linkedin-posts.md \u2014 10 LinkedIn posts + bio update",
            "podcast-guest-one-sheet.md \u2014 Bio, 3 pitches, outreach template",
            "influencer-outreach-templates.md \u2014 6 DM templates + follow-ups",
            "lead-magnet-landing-page-copy.md \u2014 Kit form landing page",
            "social-proof-snippets.md \u2014 Credibility copy",
        ]),
        ("SEO", [
            "seo-content-strategy.md \u2014 Full SEO roadmap + keyword research",
            "blog-post-1-identity-crisis.md \u2014 ~2,400 words",
            "blog-post-2-affirmations-after-layoff.md \u2014 ~2,300 words",
            "blog-post-3-ai-replacing-job-anxiety.md \u2014 ~2,500 words",
        ]),
        ("Visual Assets", [
            "logo-ig-profile.png \u2014 Instagram profile photo",
            "kit-cover-free-practice.png \u2014 Free product cover",
            "kit-cover-paid-practice.png \u2014 Paid product cover",
            "kit-cover-tripwire.png \u2014 Tripwire product cover",
            "instagram/bg-quote-navy-amber.png \u2014 Quote card background",
            "instagram/bg-quote-glow.png \u2014 Quote card background (warm)",
            "instagram/bg-carousel-lavender.png \u2014 Carousel background",
        ]),
    ]

    for category, items in asset_categories:
        story.append(Paragraph(f"<b>{category}</b>", s["SubHeader"]))
        for item in items:
            story.append(Paragraph(f"\u2022  {item}", s["BulletItem"]))

    # Final page
    story.append(PageBreak())
    story.append(Spacer(1, 2 * inch))
    story.append(Paragraph("Luminous Pulse", s["CoverTitle"]))
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        '"Your humanity is not the problem. It is the answer."',
        s["Quote"]
    ))
    story.append(Spacer(1, 24))
    story.append(Paragraph(
        "Christie Parrow  |  luminouspulse.co  |  @luminouspulse",
        s["Body"]
    ))
    story.append(Paragraph(
        "PMP-Certified Project Manager  |  7+ Years in Tech",
        s["Body"]
    ))
    story.append(Spacer(1, 24))
    story.append(Paragraph(
        "Prepared February 2026",
        s["SmallText"]
    ))

    doc.build(story, onFirstPage=add_footer, onLaterPages=add_footer)
    print(f"Business plan PDF created: {filename}")


if __name__ == "__main__":
    build_pdf()
