#!/usr/bin/env python3
"""Generate comprehensive business plan PDF for Luminous Pulse — The Path to $1M."""

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
LIGHT_AMBER = HexColor("#FFF8E1")
LIGHT_BLUE = HexColor("#E8F4FD")


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
        name="SubHeader2",
        fontName="Helvetica-Bold",
        fontSize=11,
        textColor=SOFT_NAVY,
        spaceBefore=12,
        spaceAfter=4,
        leading=14,
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
        "Luminous Pulse  |  luminouspulse.co  |  @luminouspulse.co"
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
    filename = "/Users/christieparrow/luminous-pulse/business/Luminous-Pulse-Business-Plan.pdf"
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
        "Business Plan: The Path to $1M",
        s["CoverSubtitle"]
    ))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "Grounding Practices for Displaced Workers",
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
        "luminouspulse.co  |  @luminouspulse.co  |  February 2026",
        s["Body"]
    ))
    story.append(Spacer(1, 48))
    story.append(Paragraph(
        "Year 1: $95K  |  Year 2: $395K  |  Year 3: $1.025M",
        s["BodyBold"]
    ))
    story.append(Paragraph(
        "Primary Platform: Instagram  |  Multi-Platform: Pinterest, Etsy, LinkedIn, SEO  |  B2B Corporate",
        s["Body"]
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
        "5. The Value Ladder (6 Tiers)",
        "6. Revenue Model & 36-Month Projections",
        "7. The Quiz Funnel",
        "8. B2B Corporate Strategy",
        "9. Multi-Platform Distribution",
        "10. Tech Stack & Investment",
        "11. Content Strategy",
        "12. Launch Phases",
        "13. 36-Month Milestones",
        "14. Competitive Landscape",
        "15. Risk Analysis",
        "16. What Makes This Defensible",
        "17. Asset Inventory",
    ]
    for item in toc_items:
        story.append(Paragraph(item, s["Body"]))
    story.append(PageBreak())

    # ── 1. EXECUTIVE SUMMARY ──
    story.append(Paragraph("1. Executive Summary", s["SectionHeader"]))
    story.append(hr())
    story.append(Paragraph(
        "Luminous Pulse is a digital wellness brand creating grounding practices for "
        "displaced workers. In a market where 20.8 million Americans are laid off annually, "
        "350,000+ federal workers were displaced by DOGE in 2025, and 75% of employees fear "
        "AI will make their job obsolete \u2014 there is no brand addressing the emotional "
        "and identity crisis underneath the career crisis.",
        s["Body"]
    ))
    story.append(Paragraph(
        "The business model transforms from a low-ticket PDF shop into a <b>multi-tier "
        "wellness brand with recurring revenue and B2B corporate sales</b>. The core insight: "
        "printable workbooks are the trust-builder, not the business model. The real revenue "
        "comes from a 6-tier value ladder: free quiz, $9\u2013$47 workbooks, $197 course, "
        "$39/mo membership, $997 coaching, and $1,500\u2013$25,000 B2B corporate.",
        s["Body"]
    ))

    story.append(Paragraph("Key Numbers", s["SubHeader"]))
    key_nums = [
        "\u2022  <b>$95K Year 1</b> \u2014 $395K Year 2 \u2014 $1.025M Year 3",
        "\u2022  <b>$102M combined TAM</b> \u2014 $71M B2C + $31M B2B",
        "\u2022  <b>77% profit margins</b> \u2014 digital products, minimal COGS",
        "\u2022  <b>6-tier value ladder</b> \u2014 free to $25K B2B licensing",
        "\u2022  <b>$677+ LTV</b> \u2014 up from $27\u2013$56 with workbooks alone",
        "\u2022  <b>First mover</b> \u2014 zero competitors in grounding for displaced workers",
    ]
    for n in key_nums:
        story.append(Paragraph(n, s["BulletItem"]))

    story.append(Spacer(1, 8))
    rev_summary = [
        ["Timeline", "Revenue", "Profit", "What Changes"],
        ["Year 1", "$85K\u2013$120K", "$65K\u2013$95K",
         "Add course + membership + Etsy/Pinterest + first B2B"],
        ["Year 2", "$300K\u2013$500K", "$200K\u2013$350K",
         "Scale ads, 10\u201320 corporate clients, 500+ members"],
        ["Year 3", "$800K\u2013$1.2M", "$600K\u2013$900K",
         "Full product ladder, B2B established, small team"],
    ]
    t = make_table(rev_summary[0], rev_summary[1:],
                   col_widths=[1*inch, 1.3*inch, 1.3*inch, 2.7*inch])
    story.append(t)
    story.append(PageBreak())

    # ── 2. THE OPPORTUNITY ──
    story.append(Paragraph("2. The Opportunity", s["SectionHeader"]))
    story.append(hr())
    story.append(Paragraph(
        "The workforce is experiencing structural displacement at unprecedented scale. "
        "This creates a massive, underserved audience with acute emotional needs:",
        s["Body"]
    ))
    bullets = [
        "\u2022  <b>20.8 million</b> U.S. layoffs per year (BLS JOLTS 2025)",
        "\u2022  <b>350,000+</b> federal workers displaced by DOGE in 2025",
        "\u2022  <b>75%</b> of employees fear AI will make their job obsolete",
        "\u2022  <b>54%</b> of U.S. workers experience stress spikes from job insecurity",
        "\u2022  <b>$5.65B</b> outplacement market (growing 7.6%/year) \u2014 zero emotional focus",
        "\u2022  <b>$73.3B</b> U.S. mental wellness market \u2014 generic, not displacement-specific",
    ]
    for b in bullets:
        story.append(Paragraph(b, s["BulletItem"]))

    story.append(Paragraph("The White Space", s["SubHeader"]))
    story.append(Paragraph(
        "Career coaches are tactical (resume, interview prep). Therapists are clinical. "
        "Wellness brands are generic. <b>Nobody addresses the identity crisis</b> \u2014 the "
        "\"who am I now?\" question that 55\u201370% of displaced professionals carry. Luminous "
        "Pulse is the first mover in this space, combining grounding practices with "
        "displacement-specific emotional support.",
        s["Body"]
    ))

    story.append(Paragraph("Market Sizing", s["SubHeader"]))
    tam_data = [
        ["Segment", "Size", "Annual Value"],
        ["Currently displaced workers (US)", "~892,000", "\u2014"],
        ["Recently displaced (past 12 months)", "~1,200,000", "\u2014"],
        ["DOGE federal cuts (2025)", "350,000+", "\u2014"],
        ["Underemployed / identity-in-crisis", "~500,000", "\u2014"],
        ["Partners / family members", "~1,000,000", "\u2014"],
        ["Total B2C TAM", "~3,950,000", "$71.1M"],
        ["Outplacement firms (addressable)", "~500 firms", "$6M"],
        ["Companies conducting layoffs", "~5,000/yr", "$25M"],
        ["Total B2B TAM", "\u2014", "$31M"],
        ["Combined TAM", "\u2014", "$102M"],
    ]
    t = make_table(tam_data[0], tam_data[1:],
                   col_widths=[2.5*inch, 1.3*inch, 1.3*inch])
    story.append(t)

    story.append(Spacer(1, 8))
    som_data = [
        ["Level", "B2C", "B2B", "Total"],
        ["SAM (reachable)", "$4.1M", "$3.1M", "$7.2M"],
        ["SOM Year 1", "$50K\u2013$80K", "$10K\u2013$40K", "$60K\u2013$120K"],
        ["SOM Year 2", "$150K\u2013$250K", "$100K\u2013$200K", "$250K\u2013$450K"],
        ["SOM Year 3", "$350K\u2013$550K", "$300K\u2013$450K", "$650K\u2013$1M"],
    ]
    t = make_table(som_data[0], som_data[1:],
                   col_widths=[1.5*inch, 1.5*inch, 1.5*inch, 1.5*inch])
    story.append(t)
    story.append(PageBreak())

    # ── 3. BRAND POSITIONING ──
    story.append(Paragraph("3. Brand Positioning", s["SectionHeader"]))
    story.append(hr())
    story.append(Paragraph(
        "For workers who\u2019ve been laid off, displaced, or are watching their industry "
        "reshape beneath their feet, Luminous Pulse is the place where you come to feel less alone "
        "and more in possession of your own power.",
        s["Body"]
    ))
    story.append(Paragraph(
        "Unlike generic affirmation accounts that ignore what\u2019s happening, and unlike career "
        "coaches who say \"just upskill,\" we sit in the real fear with you \u2014 "
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
        "\u2022  <b>Name the Feeling</b> \u2014 The specific grief of displacement",
        "\u2022  <b>Remember Who You Are</b> \u2014 Identity beyond job titles",
        "\u2022  <b>Ground Yourself</b> \u2014 Breathwork, affirmations, daily rituals",
        "\u2022  <b>You Are Not Alone</b> \u2014 Community, shared stories",
        "\u2022  <b>The World We\u2019re Building</b> \u2014 Grounded hope for the future",
    ]
    for p in pillars:
        story.append(Paragraph(p, s["BulletItem"]))
    story.append(PageBreak())

    # ── 4. TARGET AUDIENCE ──
    story.append(Paragraph("4. Target Audience", s["SectionHeader"]))
    story.append(hr())
    story.append(Paragraph(
        "<b>Primary:</b> Displaced workers (25\u201345) \u2014 PMs, engineers, designers, "
        "marketers, federal employees who\u2019ve been laid off, fear they\u2019re next, or are "
        "watching their industry reshape itself.",
        s["Body"]
    ))
    story.append(Paragraph(
        "<b>Secondary:</b> Early-career workers (22\u201330) entering a job market that looks "
        "nothing like what they were promised. Partners and family members of displaced workers.",
        s["Body"]
    ))

    story.append(Paragraph("Meet Sam (Primary Persona)", s["SubHeader"]))
    story.append(Paragraph(
        "34-year-old former senior PM. Laid off 3 months ago. Tells everyone \"I\u2019m fine.\" "
        "At 2am, scrolls Instagram looking for anything that makes her feel less alone. Won\u2019t "
        "call it therapy, won\u2019t hire a coach, but will take a quiet self-assessment that "
        "meets her where she is. Ashamed of needing help. Active 6pm\u20132am.",
        s["Body"]
    ))

    story.append(Paragraph("Post-Layoff Emotional Journey", s["SubHeader"]))
    journey = [
        ["Stage", "Timeline", "What They Need", "Product Match"],
        ["Shock & Relief", "Week 1\u20132", "Permission, grounding", "Before the Room ($9)"],
        ["Anger & Grief", "Week 3\u20134", "Naming the feeling", "Tender Landings ($12)"],
        ["Identity Crisis", "Month 2\u20133", "Who am I without my title?", "Identity Workbook ($15)"],
        ["Bargaining", "Month 3\u20134", "Should I just learn AI?", "Course ($197)"],
        ["Reconstruction", "Month 4\u20136+", "Rebuilding identity", "Membership ($39/mo)"],
    ]
    t = make_table(journey[0], journey[1:],
                   col_widths=[1.2*inch, 1*inch, 1.8*inch, 2.3*inch])
    story.append(t)
    story.append(PageBreak())

    # ── 5. THE VALUE LADDER ──
    story.append(Paragraph("5. The Value Ladder (6 Tiers)", s["SectionHeader"]))
    story.append(hr())
    story.append(Paragraph(
        "The workbooks are the trust-builder, not the business model. The real revenue comes "
        "from higher-ticket products, recurring membership, and B2B corporate sales.",
        s["Body"]
    ))

    story.append(Paragraph("Tier 1: Free (Lead Generation)", s["SubHeader2"]))
    story.append(Paragraph(
        "\"Find your grounding practice\" quiz + 5-day grounding practice PDF. "
        "Email capture and segmentation via Interact + Kit.",
        s["Body"]
    ))

    story.append(Paragraph("Tier 2: Entry ($9\u2013$47) \u2014 Current Products", s["SubHeader2"]))
    products = [
        ["Product", "Price", "Pages"],
        ["\"before the room\"", "$9", "28"],
        ["\"tender landings\"", "$12", "44"],
        ["\"who am I without the title?\"", "$15", "49"],
        ["\"steady\"", "$15", "63"],
        ["\"30 days of ground\"", "$17", "66"],
        ["\"the in-between\" (flagship)", "$27", "90"],
        ["\"the recovery starter\" bundle", "$27", "113"],
        ["\"the complete grounding collection\"", "$47", "404"],
    ]
    t = make_table(products[0], products[1:],
                   col_widths=[2.8*inch, 0.8*inch, 0.8*inch])
    story.append(t)

    story.append(Paragraph(
        "Tier 3: Mid-Ticket ($197) \u2014 \"Grounded Through Change\" Course", s["SubHeader2"]))
    story.append(Paragraph(
        "6-week online course (self-paced). 6 video modules, companion workbook, private "
        "community, weekly group Q&A. Includes all Tier 2 workbooks. Launch: $147. Regular: $197.",
        s["Body"]
    ))

    story.append(Paragraph(
        "Tier 4: Recurring ($39/mo) \u2014 \"The Sanctuary\" Membership", s["SubHeader2"]))
    story.append(Paragraph(
        "Monthly grounding workbook, weekly live sessions, private community, archive access, "
        "monthly expert guest. $39/mo ($29/mo annual). 500 members = $234K/year.",
        s["Body"]
    ))

    story.append(Paragraph(
        "Tier 5: High-Ticket ($997\u2013$3,000) \u2014 Coaching", s["SubHeader2"]))
    story.append(Paragraph(
        "\"Rebuild\" 12-week group coaching (8\u201312 per cohort, $997, 4 cohorts/year = $40K/yr). "
        "1:1 coaching (6 sessions, $3,000, cap 20 clients/year = $60K/yr).",
        s["Body"]
    ))

    story.append(Paragraph(
        "Tier 6: B2B Corporate ($1,500\u2013$25,000)", s["SubHeader2"]))
    story.append(Paragraph(
        "Single workshop ($1,500), 4-session package ($5,000), annual license ($12,000/yr). "
        "See Section 8 for full B2B strategy.",
        s["Body"]
    ))
    story.append(PageBreak())

    # ── 6. REVENUE MODEL ──
    story.append(Paragraph("6. Revenue Model & 36-Month Projections", s["SectionHeader"]))
    story.append(hr())

    story.append(Paragraph("$1M Revenue Mix (Year 3 Target)", s["SubHeader"]))
    rev_mix = [
        ["Revenue Stream", "Unit Price", "Units/Year", "Annual Revenue", "% of Total"],
        ["Workbooks ($9\u2013$47)", "$18 avg", "5,000", "$90,000", "9%"],
        ["Digital Course ($197)", "$197", "800", "$157,600", "16%"],
        ["Membership ($39/mo)", "$468/yr avg", "600 active", "$280,800", "28%"],
        ["Group Coaching ($997)", "$997", "40", "$39,880", "4%"],
        ["1:1 Coaching ($3,000)", "$3,000", "20", "$60,000", "6%"],
        ["Corporate Workshops", "$1,500", "80", "$120,000", "12%"],
        ["Corporate Packages", "$5,000", "20", "$100,000", "10%"],
        ["Outplacement Licensing", "$12,000/yr", "8", "$96,000", "10%"],
        ["Speaking + Affiliate", "varies", "\u2014", "$50,000", "5%"],
        ["Total", "", "", "$994,280", "100%"],
    ]
    t = make_table(rev_mix[0], rev_mix[1:],
                   col_widths=[1.5*inch, 0.9*inch, 0.9*inch, 1.2*inch, 0.8*inch])
    story.append(t)

    story.append(Paragraph("B2C / B2B Split", s["SubHeader"]))
    split = [
        ["Segment", "Revenue", "Percentage"],
        ["B2C (individuals)", "$628,280", "63%"],
        ["B2B (corporate + licensing)", "$316,000", "32%"],
        ["Other (speaking, affiliate)", "$50,000", "5%"],
    ]
    t = make_table(split[0], split[1:],
                   col_widths=[2.5*inch, 1.5*inch, 1.5*inch])
    story.append(t)

    story.append(Paragraph("Year 1 Revenue by Stream ($95K)", s["SubHeader"]))
    y1_streams = [
        ["Stream", "Year 1 Revenue", "Notes"],
        ["Workbooks (all channels)", "$18,000", "IG + Etsy + Pinterest + direct"],
        ["Digital Course ($197)", "$23,640", "~120 enrollments, 4 launches"],
        ["Membership ($39/mo)", "$14,040", "Growing from 0 to ~120 members"],
        ["Group Coaching ($997)", "$7,976", "2 cohorts (8 people each)"],
        ["1:1 Coaching ($3,000)", "$9,000", "3 clients"],
        ["Corporate Workshops", "$10,500", "7 paid workshops"],
        ["Licensing", "$12,000", "1 deal (signed month 11)"],
        ["Total", "$95,156", ""],
    ]
    t = make_table(y1_streams[0], y1_streams[1:],
                   col_widths=[2*inch, 1.3*inch, 3*inch])
    story.append(t)

    story.append(Paragraph("Profitability", s["SubHeader"]))
    profit = [
        ["Year", "Revenue", "Expenses", "Profit", "Margin"],
        ["Year 1", "$95K", "$20K", "$75K", "79%"],
        ["Year 2", "$395K", "$102K", "$293K", "74%"],
        ["Year 3", "$1.025M", "$240K", "$785K", "77%"],
    ]
    t = make_table(profit[0], profit[1:],
                   col_widths=[1*inch, 1.2*inch, 1.2*inch, 1.2*inch, 1*inch])
    story.append(t)
    story.append(PageBreak())

    # ── 7. THE QUIZ FUNNEL ──
    story.append(Paragraph("7. The Quiz Funnel", s["SectionHeader"]))
    story.append(hr())
    story.append(Paragraph(
        "The quiz is the primary acquisition mechanism. It feeds the entire value ladder.",
        s["Body"]
    ))
    story.append(Paragraph(
        "<b>\"Find Your Grounding Practice\"</b> \u2014 6 questions, 2 minutes, 4 outcomes. "
        "Built on Interact, connected to Kit via API. Never called a \"quiz\" \u2014 always "
        "\"self-assessment\" or \"grounding inventory\" (Sam associates quizzes with judgment).",
        s["Body"]
    ))

    story.append(Paragraph("Funnel Architecture", s["SubHeader"]))
    funnel_steps = [
        "1.  Instagram / Pinterest / Etsy / SEO / Ads",
        "2.  \"Find your grounding practice\" quiz (Interact)",
        "3.  Email capture with Kit tag (quiz-tender / identity / grounding / rebuild)",
        "4.  Outcome-specific email sequence (5 emails, 17 days)",
        "5.  Workbook purchase ($9\u2013$47) \u2014 first transaction",
        "6.  Post-purchase sequence: course offer ($197, day 14)",
        "7.  Course enrollment \u2014 deeper engagement",
        "8.  Membership conversion ($39/mo) \u2014 recurring revenue",
        "9.  Group coaching application ($997) \u2014 high-touch",
    ]
    for step in funnel_steps:
        story.append(Paragraph(step, s["BulletItem"]))

    story.append(Paragraph("Conversion Targets", s["SubHeader"]))
    conv_data = [
        ["Stage", "Target", "Notes"],
        ["Quiz start (from click)", "70%", "Interact benchmark"],
        ["Quiz completion", "75%", "6 questions, ~2 min"],
        ["Email opt-in (post-quiz)", "40%+", "Industry avg: 18% for PDFs"],
        ["Quiz to workbook (21 days)", "10\u201312%", "Outcome-specific emails"],
        ["Workbook buyer to course", "15\u201320%", "Warm audience, proven trust"],
        ["Course to membership", "25\u201330%", "Natural next step"],
        ["Membership to coaching", "3\u20135%", "Self-selecting high-intent"],
    ]
    t = make_table(conv_data[0], conv_data[1:],
                   col_widths=[2*inch, 1*inch, 3.3*inch])
    story.append(t)

    story.append(Paragraph("Quiz Outcomes", s["SubHeader"]))
    quiz_outcomes = [
        ["Outcome", "Tag", "Recommended Product"],
        ["\"the tender one\"", "quiz-tender", "Tender Landings ($12)"],
        ["\"the unnamed one\"", "quiz-identity", "Who Am I Without the Title? ($15)"],
        ["\"the bracing one\"", "quiz-grounding", "Before the Room ($9)"],
        ["\"the rebuilder\"", "quiz-rebuild", "Steady ($15) or Complete Collection ($47)"],
    ]
    t = make_table(quiz_outcomes[0], quiz_outcomes[1:],
                   col_widths=[1.5*inch, 1.2*inch, 3.6*inch])
    story.append(t)
    story.append(PageBreak())

    # ── 8. B2B CORPORATE STRATEGY ──
    story.append(Paragraph("8. B2B Corporate Strategy", s["SectionHeader"]))
    story.append(hr())
    story.append(Paragraph(
        "The outplacement market is <b>$5.65 billion</b> (2025, growing 7.6%/year). "
        "Traditional outplacement is tactical \u2014 resume writing, job boards, interview prep. "
        "<b>Nobody addresses the emotional/identity crisis.</b> That\u2019s the whitespace.",
        s["Body"]
    ))

    story.append(Paragraph("\"Workforce Transition Resilience Program\"", s["SubHeader"]))
    b2b_products = [
        ["Offering", "Price", "Description"],
        ["Single Workshop", "$1,500",
         "90-min virtual workshop for displaced teams (10\u201350 people). "
         "Facilitator-led grounding + digital workbook bundle."],
        ["Workshop Package", "$5,000",
         "4 sessions over 4\u20136 weeks: regulation, grief, job search grounding, slow rebuild. "
         "Complete collection for each participant."],
        ["Annual License", "$12,000/yr",
         "Unlimited digital workbook access, quarterly workshops, custom-branded resources, "
         "HR dashboard. For outplacement firms + large employers."],
    ]
    t = make_table(b2b_products[0], b2b_products[1:],
                   col_widths=[1.3*inch, 0.8*inch, 4.2*inch])
    story.append(t)

    story.append(Paragraph("Pricing vs Traditional Outplacement", s["SubHeader"]))
    pricing_comp = [
        ["", "Traditional Outplacement", "Luminous Pulse"],
        ["Per-employee cost", "$500\u2013$1,900", "$30\u2013$50"],
        ["What\u2019s included", "Resume, job boards, interview prep",
         "Grounding, identity work, grief processing"],
        ["Delivery", "1:1 coaching (expensive)", "Digital + group (scales infinitely)"],
        ["Emotional component", "Minimal", "Core focus"],
        ["Positioning", "\"Get your next job\"", "\"Get back to yourself first\""],
    ]
    t = make_table(pricing_comp[0], pricing_comp[1:],
                   col_widths=[1.5*inch, 2.2*inch, 2.6*inch])
    story.append(t)

    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "<i>This isn\u2019t a replacement for outplacement \u2014 it\u2019s a complement. "
        "Companies offer career services + Luminous Pulse for the emotional work.</i>",
        s["SmallText"]
    ))

    story.append(Paragraph("B2B Sales Timeline", s["SubHeader"]))
    b2b_timeline = [
        "\u2022  Month 4\u20135: Build B2B one-pager + case study template",
        "\u2022  Month 6: 3 free workshops (for testimonials and case studies)",
        "\u2022  Month 7\u20138: First paid workshops ($1,500)",
        "\u2022  Month 9\u201310: Outplacement firm conversations",
        "\u2022  Month 11\u201312: First licensing deal signed ($12,000)",
    ]
    for item in b2b_timeline:
        story.append(Paragraph(item, s["BulletItem"]))
    story.append(PageBreak())

    # ── 9. MULTI-PLATFORM DISTRIBUTION ──
    story.append(Paragraph("9. Multi-Platform Distribution", s["SectionHeader"]))
    story.append(hr())
    story.append(Paragraph(
        "Instagram alone caps reach at ~227,000 reachable Sams. The plan needs more channels. "
        "Instagram organic reach dropped 28% year-over-year.",
        s["Body"]
    ))
    channels = [
        ["Channel", "Role", "Revenue Impact", "When"],
        ["Instagram", "Community, DMs, paid ads", "Medium \u2014 declining organic", "Now"],
        ["Pinterest", "Evergreen discovery engine", "HIGH \u2014 6.2x ROAS, pins last years", "Month 1"],
        ["Etsy", "Marketplace for printables", "HIGH \u2014 top sellers do $10K+/mo", "Month 1\u20132"],
        ["LinkedIn", "B2B outreach, professionals", "HIGH for B2B", "Month 3"],
        ["SEO/Blog", "Search intent capture", "HIGH long-term \u2014 3 posts written", "Month 1"],
        ["YouTube", "Authority, course promotion", "Medium-high \u2014 compounds", "Month 4\u20136"],
        ["TikTok", "Viral discovery", "Medium \u2014 34% buy from creators", "Month 3\u20134"],
        ["Amazon KDP", "Physical workbook versions", "Medium \u2014 passive income", "Month 6+"],
    ]
    t = make_table(channels[0], channels[1:],
                   col_widths=[1.1*inch, 1.6*inch, 2*inch, 1.1*inch])
    story.append(t)

    story.append(Paragraph("Pinterest Strategy (Highest-Priority New Channel)", s["SubHeader"]))
    story.append(Paragraph(
        "Pinterest is a visual search engine, not a social network. Wellness and printables "
        "are top-performing categories. A single well-optimized pin can drive traffic for years. "
        "Target: 10\u201315 pins/week (most repurposed from Instagram). Expected: 5,000\u201315,000 "
        "monthly visitors by month 6.",
        s["Body"]
    ))

    story.append(Paragraph("Etsy Strategy", s["SubHeader"]))
    story.append(Paragraph(
        "Etsy is the largest marketplace for digital printables. The workbook line is already "
        "built \u2014 it just needs listings. Expected: $500\u2013$2,000/month in first 6 months, "
        "scaling to $5,000\u2013$15,000/month by month 12\u201318.",
        s["Body"]
    ))
    story.append(PageBreak())

    # ── 10. TECH STACK ──
    story.append(Paragraph("10. Tech Stack & Investment", s["SectionHeader"]))
    story.append(hr())
    stack_data = [
        ["Tool", "Purpose", "Cost", "When"],
        ["Kit (ConvertKit)", "Email, PDF delivery, commerce",
         "$0 (free to 5K subs)", "Now"],
        ["Interact", "Quiz funnel", "$27/mo", "Now"],
        ["Canva Pro", "Design templates", "$13/mo", "Now"],
        ["Metricool", "Content scheduling", "$0", "Now"],
        ["ManyChat", "DM automation", "$0", "Now"],
        ["Vercel", "Website hosting", "$0", "Now"],
        ["Etsy", "Marketplace", "$0.20/listing + 6.5%", "Month 1\u20132"],
        ["Pinterest Business", "Discovery engine", "$0", "Month 1"],
        ["Zoom Pro", "Workshops + coaching", "$16/mo", "Month 3"],
        ["Teachable / Circle", "Course + membership", "$49\u2013$100/mo", "Month 4"],
        ["Calendly", "B2B booking", "$12/mo", "Month 5"],
    ]
    t = make_table(stack_data[0], stack_data[1:],
                   col_widths=[1.3*inch, 1.8*inch, 1.6*inch, 1*inch])
    story.append(t)

    story.append(Paragraph("Investment Requirements", s["SubHeader"]))
    invest_data = [
        ["Asset", "Build Time", "Investment", "Revenue Potential"],
        ["Etsy store + listings", "1 week", "$0.20/listing", "$60K\u2013$180K/yr"],
        ["Pinterest + first 50 pins", "1 week", "$0", "Free traffic"],
        ["3 SEO blog posts (written)", "1 day", "$0", "Free traffic"],
        ["Digital course", "6\u20138 weeks", "$500\u2013$5,000", "$157K/yr"],
        ["Membership platform", "2 weeks", "$49\u2013$100/mo", "$280K/yr"],
        ["Corporate workshop deck", "3 weeks", "$300", "$220K/yr"],
        ["Group coaching program", "2 weeks", "$0", "$40K\u2013$60K/yr"],
        ["Licensing package", "2 weeks", "$500", "$96K/yr"],
    ]
    t = make_table(invest_data[0], invest_data[1:],
                   col_widths=[1.7*inch, 1*inch, 1.2*inch, 1.4*inch])
    story.append(t)

    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "<b>Total product development investment: ~$1,500\u2013$6,000 + time.</b> "
        "Year 1 expenses: $20K (ads $10K, tools $3K, VA $1.5K, content $2.4K, misc $3.1K). "
        "Profit margin remains above 74% through year 3.",
        s["Body"]
    ))
    story.append(PageBreak())

    # ── 11. CONTENT STRATEGY ──
    story.append(Paragraph("11. Content Strategy", s["SectionHeader"]))
    story.append(hr())
    story.append(Paragraph("Instagram (Primary Platform)", s["SubHeader"]))
    story.append(Paragraph(
        "<b>Posting cadence:</b> 5x/week + daily Stories. Schedule all ads 6pm\u20132am "
        "(Sam\u2019s active hours). Voice: lowercase, quiet, permission-based.",
        s["Body"]
    ))
    cadence = [
        ["Day", "Content Type", "Purpose"],
        ["Monday", "Quote Card (affirmation)", "Grounding + saves"],
        ["Tuesday", "Quote Card (Name the Feeling)", "Emotional resonance + shares"],
        ["Wednesday", "Carousel (educational)", "Authority + saves + follows"],
        ["Thursday", "Quote Card (permission)", "Community + shares"],
        ["Friday", "Reel (storytelling or practice)", "Reach + new followers"],
        ["Daily", "1\u20132 Stories (polls, Q&A)", "Engagement + algorithm boost"],
    ]
    t = make_table(cadence[0], cadence[1:],
                   col_widths=[1.2*inch, 2.3*inch, 2.8*inch])
    story.append(t)

    story.append(Paragraph("SEO Blog Strategy", s["SubHeader"]))
    story.append(Paragraph(
        "7 keyword clusters targeting low-competition, high-intent terms. 3 posts written "
        "(identity crisis, affirmations after layoff, AI job anxiety). 2 new clusters added "
        "for B2B (workplace transition) and course/membership keywords.",
        s["Body"]
    ))

    story.append(Paragraph("Ad Strategy (Quiz Funnel)", s["SubHeader"]))
    story.append(Paragraph(
        "16 Instagram ads written: 6 cold ads (carousels + reels), 4 story ads, 4 retargeting "
        "ads, 2 upsell ads. A/B testing plan over 8 weeks. Budget: $150/mo (month 1), "
        "scaling to $600/mo (month 4+). Target CPAs: quiz start $0.50\u2013$1.00, "
        "email signup $1.50\u2013$3.00.",
        s["Body"]
    ))
    story.append(PageBreak())

    # ── 12. LAUNCH PHASES ──
    story.append(Paragraph("12. Launch Phases", s["SectionHeader"]))
    story.append(hr())

    phases = [
        ("Phase 0: Brand Foundation (Days 1\u20137)", "COMPLETE",
         "Brand name, domain, IG, colors, fonts, logo, voice, positioning, brand reframe."),
        ("Phase 1: Content Stockpile (Days 8\u201318)", "COMPLETE",
         "155+ affirmations, 46+ captions, 8 carousels, 6 hashtag sets, 30-day calendar, "
         "3 SEO blog posts, email sequences, quiz copy, ad copy. All written."),
        ("Phase 2: Pre-Launch (Days 19\u201321)", "IN PROGRESS",
         "Seed IG grid, Kit form + incentive email, quiz build in Interact, Beacons link-in-bio, "
         "Etsy store, Pinterest account. Test full funnel."),
        ("Phase 3: Launch & Build (Days 22\u201351)", "PLANNED",
         "First 30 posting days. 5x/week + daily Stories. DM automation. Quiz funnel live."),
        ("Phase 4: Accelerate (Days 40\u201381)", "PLANNED",
         "Workbook sales on Kit Commerce + Etsy. Beta testers. Micro-influencer outreach. "
         "Podcast pitches. LinkedIn content begins."),
        ("Phase 5: Scale & Pre-Sell (Days 82\u2013111)", "PLANNED",
         "Paid ads ($5\u201310/day). TikTok launch. Pre-sell course ($147). "
         "Zoom Pro for workshops."),
        ("Phase 6: Course Launch (Month 3\u20134)", "PLANNED",
         "\"Grounded Through Change\" course ($197). 6 modules, private community. "
         "Target: 30+ enrollments first cohort."),
        ("Phase 7: Membership + B2B (Month 5\u20136)", "PLANNED",
         "\"The Sanctuary\" membership ($39/mo). B2B one-pager. 3 free corporate workshops "
         "for case studies. Target: 30+ founding members."),
        ("Phase 8: B2B Revenue (Month 7\u20139)", "PLANNED",
         "First paid workshops ($1,500). \"Rebuild\" group coaching ($997). "
         "Outplacement outreach. Target: $9K\u2013$11.5K/mo."),
        ("Phase 9: Full Engine (Month 10\u201312)", "PLANNED",
         "All streams active. First licensing deal ($12K). VA hired. "
         "Target: $12K\u2013$15K/mo. Year 1 total: $85K\u2013$120K."),
    ]
    for title, status, desc in phases:
        story.append(Paragraph(f"<b>{title}</b> \u2014 {status}", s["SubHeader2"]))
        story.append(Paragraph(desc, s["Body"]))
    story.append(PageBreak())

    # ── 13. MILESTONES ──
    story.append(Paragraph("13. 36-Month Milestones", s["SectionHeader"]))
    story.append(hr())
    milestones = [
        ["Milestone", "Target", "When"],
        ["Quiz live + connected to Kit", "Done", "Month 1"],
        ["Etsy store live", "8+ listings", "Month 1\u20132"],
        ["Pinterest active", "50+ pins", "Month 1\u20132"],
        ["First $1,000 revenue month", "Multi-channel", "Month 3\u20134"],
        ["Digital course launched", "First cohort", "Month 4"],
        ["1,000 email subscribers", "All channels", "Month 4\u20135"],
        ["First corporate workshop (free)", "1 workshop", "Month 6"],
        ["Membership launched", "Founding members", "Month 6"],
        ["First paid workshop", "$1,500", "Month 7\u20138"],
        ["First $5,000 revenue month", "Multi-stream", "Month 7\u20138"],
        ["Group coaching launched", "First cohort", "Month 9"],
        ["First $10,000 revenue month", "All streams", "Month 10\u201311"],
        ["First licensing deal", "$12,000", "Month 11\u201312"],
        ["Year 1 total", "$85K\u2013$120K", "Month 12"],
        ["Membership at 250+ members", "$9,750/mo recurring", "Month 15"],
        ["5,000 email subscribers", "All channels", "Month 14\u201316"],
        ["10+ corporate clients", "$15K+/mo B2B", "Month 16\u201318"],
        ["Year 2 total", "$300K\u2013$500K", "Month 24"],
        ["500+ members", "$19,500/mo recurring", "Month 24"],
        ["5+ licensing deals active", "$60K+/yr recurring", "Month 24\u201328"],
        ["Year 3 total", "$800K\u2013$1.2M", "Month 36"],
    ]
    t = make_table(milestones[0], milestones[1:],
                   col_widths=[2.5*inch, 1.8*inch, 1.5*inch])
    story.append(t)
    story.append(PageBreak())

    # ── 14. COMPETITIVE LANDSCAPE ──
    story.append(Paragraph("14. Competitive Landscape", s["SectionHeader"]))
    story.append(hr())
    comp_data = [
        ["Competitor", "Their Angle", "Our Differentiation"],
        ["@iam.affirmations", "Generic positivity",
         "We name the specific grief of displacement"],
        ["@thegoodquote", "Literary quotes",
         "Original words for a feeling no one else names"],
        ["@mindsetofgreatness", "Hustle culture",
         "Tenderness and healing, not \"pivot harder\""],
        ["@theholisticpsychologist", "Nervous system theory",
         "Same depth, specific to displacement"],
        ["LinkedIn career coaches", "Upskill / Network / Pivot",
         "Address the identity crisis first"],
        ["Outplacement firms", "Career transition ($1,900/employee)",
         "Emotional/identity crisis at 5\u201310x lower cost"],
    ]
    t = make_table(comp_data[0], comp_data[1:],
                   col_widths=[1.6*inch, 1.6*inch, 3.1*inch])
    story.append(t)

    story.append(Spacer(1, 12))
    story.append(Paragraph(
        "<b>Our moat:</b> The intersection of grounded healing + displacement + human "
        "connection is wide open. The business spans B2B corporate (workshops at "
        "$1,500\u2013$25,000) and multi-platform distribution (Pinterest, Etsy, LinkedIn, "
        "YouTube). The value ladder extends from free quiz to $997 group coaching. "
        "Zero brands specifically serve the emotional needs of displaced workers. "
        "We are first movers.",
        s["Body"]
    ))
    story.append(PageBreak())

    # ── 15. RISK ANALYSIS ──
    story.append(Paragraph("15. Risk Analysis", s["SectionHeader"]))
    story.append(hr())

    risks = [
        ("Risk 1: B2B revenue fails to materialize (HIGH impact)",
         "Corporate workshops and licensing represent 32% of the $1M model. "
         "If this segment doesn\u2019t develop, B2C-only ceiling is ~$600K\u2013$700K/year "
         "(still excellent). Mitigation: start B2B outreach by month 4. Offer 3 free workshops "
         "for case studies. Partner with career coaches who have corporate relationships."),
        ("Risk 2: Ad costs exceed returns (MEDIUM impact)",
         "If CAC rises above $20 for B2C with $18 AOV, paid acquisition becomes unprofitable "
         "on first purchase. Mitigation: never let paid acquisition exceed 30% of customer "
         "acquisition. Invest in organic (Pinterest, Etsy, SEO). Safety net: with the value "
         "ladder, a $12 CAC customer who buys the course + membership has $700+ LTV."),
        ("Risk 3: Founder burnout (HIGH impact)",
         "Solo founder running B2C content, B2B sales, product development, community, and "
         "workshops will hit a wall at ~$150K\u2013$200K/year. Mitigation: hire VA by month 10. "
         "Systematize everything. Use membership as leverage (one-to-many)."),
        ("Risk 4: Course or membership doesn\u2019t convert (MEDIUM impact)",
         "Mitigation: pre-sell the course before building it (50+ paid = green light). "
         "For membership, founding-member rate ($19/mo) to seed 50 committed members. "
         "Fallback: multi-platform workbook sales alone can reach $150K\u2013$250K/year."),
    ]
    for title, desc in risks:
        story.append(Paragraph(f"<b>{title}</b>", s["SubHeader2"]))
        story.append(Paragraph(desc, s["Body"]))

    story.append(Paragraph("Plan B: What If $1M Isn\u2019t Reachable?", s["SubHeader"]))
    planb = [
        ["Scenario", "Year 1", "Year 2", "Year 3"],
        ["Conservative (B2C, slow B2B)", "$40,000", "$120,000", "$300,000"],
        ["Moderate (balanced)", "$95,000", "$395,000", "$1,000,000"],
        ["Aggressive (strong B2B)", "$120,000", "$500,000", "$1,200,000+"],
        ["Worst case (high CAC, no B2B)", "$20,000", "$60,000", "$150,000"],
    ]
    t = make_table(planb[0], planb[1:],
                   col_widths=[2.2*inch, 1.2*inch, 1.2*inch, 1.4*inch])
    story.append(t)
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "<i>Even the worst case ($150K by year 3) is a real business with 70%+ margins.</i>",
        s["SmallText"]
    ))
    story.append(PageBreak())

    # ── 16. DEFENSIBILITY ──
    story.append(Paragraph("16. What Makes This Defensible", s["SectionHeader"]))
    story.append(hr())
    defensible = [
        ("<b>The need is accelerating.</b> 20.8M layoffs/year. 350,000+ federal workers "
         "displaced by DOGE. 1.9M long-term unemployed. Structural, not cyclical."),
        ("<b>Nobody occupies the space between.</b> Career coaches are tactical. Therapists "
         "are clinical. Nobody addresses the identity crisis \u2014 the \"who am I now?\" question."),
        ("<b>The pain persists after reemployment.</b> Research shows life satisfaction does "
         "not fully recover after job loss \u2014 even years later."),
        ("<b>The quiz builds a moat.</b> Every response is zero-party data. We learn what "
         "displaced workers actually feel, at scale. That data improves everything."),
        ("<b>The value ladder creates compounding LTV.</b> A Sam who enters at $12 and "
         "ascends to course + membership has $677+ LTV (vs $27\u2013$56 with workbooks alone)."),
        ("<b>B2B is defensible by relationship.</b> Once an outplacement firm licenses the "
         "content, switching costs are high."),
        ("<b>The brand voice is inimitable.</b> Lowercase, quiet, permission-based. Can\u2019t "
         "be replicated by a corporate wellness vendor with a PowerPoint deck."),
    ]
    for item in defensible:
        story.append(Paragraph(f"\u2022  {item}", s["BulletItem"]))
        story.append(Spacer(1, 4))
    story.append(PageBreak())

    # ── 17. ASSET INVENTORY ──
    story.append(Paragraph("17. Complete Asset Inventory", s["SectionHeader"]))
    story.append(hr())
    story.append(Paragraph(
        "All copywriting and content assets have been created. "
        "Below is the inventory of ready-to-use files.",
        s["Body"]
    ))

    asset_categories = [
        ("Brand & Strategy", [
            "brand-positioning.md \u2014 Positioning, taglines, content pillars",
            "brand-voice-guide.md \u2014 Voice guide (warm, grounded, defiant, tender)",
            "business-plan-1m.md \u2014 $1M revenue plan (this document\u2019s source)",
            "business-goals.md \u2014 Quiz funnel, TAM/SAM/SOM, market sizing",
            "content-strategy-2026.md \u2014 Full content strategy & product roadmap",
            "ig-ad-strategy.md \u2014 Instagram ad & growth strategy",
            "seo-content-strategy.md \u2014 7 keyword clusters, publishing schedule",
            "launch-plan.md / launch-plan-deepened.md \u2014 Phased launch plans",
        ]),
        ("Products (Built)", [
            "8 printable workbooks (340+ pages, $9\u2013$27)",
            "2 bundles ($27 starter, $47 complete collection \u2014 404 pages)",
            "5-Day Grounding Practice (free lead magnet, 10 pages)",
            "Emergency Grounding Kit (tripwire, $9, 15 pages)",
            "30-Day Luminous Pulse Practice (core, $37, 39 pages)",
        ]),
        ("Email Marketing (60+ emails written)", [
            "Quiz outcome email sequences (4 outcomes x 5 emails = 20 emails)",
            "Welcome sequence (2 emails)",
            "Nurture sequence (5 emails)",
            "Incentive email (PDF delivery)",
            "Kit configured: 11 tags, 9 automation rules",
        ]),
        ("Content Pipeline", [
            "155+ grounding affirmations across 5 themes",
            "46+ post captions with CTAs",
            "8 carousel scripts, Reel + IG Live scripts",
            "16 Instagram ads (cold + retargeting + upsell)",
            "Quiz landing page + 4 result pages",
            "3 SEO blog posts (published-ready)",
            "10 LinkedIn posts",
        ]),
        ("Visual Assets", [
            "Logo suite (sanctuary, wordmark, IG profile, transparent)",
            "Kit product covers (free + paid + tripwire)",
            "Instagram backgrounds, quote cards, carousel templates",
        ]),
        ("PDFs Generated", [
            "Luminous-Pulse-Pitch-Deck.pdf \u2014 20-slide investor deck",
            "Luminous-Pulse-Business-Plan.pdf \u2014 This document",
            "All workbook PDFs (11 files)",
        ]),
    ]

    for category, items in asset_categories:
        story.append(Paragraph(f"<b>{category}</b>", s["SubHeader2"]))
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
        "Christie Parrow  |  luminouspulse.co  |  @luminouspulse.co",
        s["Body"]
    ))
    story.append(Paragraph(
        "PMP-Certified Project Manager  |  7+ Years in Tech",
        s["Body"]
    ))
    story.append(Spacer(1, 16))
    story.append(Paragraph(
        "Year 1: $95K  |  Year 2: $395K  |  Year 3: $1.025M",
        s["BodyBold"]
    ))
    story.append(Spacer(1, 24))
    story.append(Paragraph(
        "Prepared February 2026",
        s["SmallText"]
    ))

    doc.build(story, onFirstPage=add_footer, onLaterPages=add_footer)
    print(f"\u2713 Business plan PDF created: {filename}")


if __name__ == "__main__":
    build_pdf()
