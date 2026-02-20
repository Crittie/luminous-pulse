#!/usr/bin/env python3
"""Generate pitch deck PDF with charts for Luminous Pulse — path to $1M."""

import os
import io
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
from reportlab.lib.pagesizes import landscape, letter
from reportlab.lib.colors import HexColor
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, Image, HRFlowable, KeepTogether
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT

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
CREAM = HexColor("#FAF6F1")
GREEN = HexColor("#2ecc71")

# Matplotlib brand colors
C_NAVY = "#1a2744"
C_BLUE = "#6CB4EE"
C_AMBER = "#F4C430"
C_LAVENDER = "#B4A7D6"
C_SOFT_NAVY = "#2a3a5c"
C_MED_GRAY = "#666666"
C_RED = "#e17055"
C_GREEN = "#2ecc71"

PAGE_W, PAGE_H = landscape(letter)


def create_styles():
    styles = getSampleStyleSheet()

    styles.add(ParagraphStyle(
        name="SlideTitle",
        fontName="Helvetica-Bold",
        fontSize=28,
        textColor=NAVY,
        alignment=TA_LEFT,
        spaceAfter=6,
        leading=34,
    ))
    styles.add(ParagraphStyle(
        name="SlideSubtitle",
        fontName="Helvetica",
        fontSize=14,
        textColor=SOFT_NAVY,
        alignment=TA_LEFT,
        spaceAfter=12,
        leading=20,
    ))
    styles.add(ParagraphStyle(
        name="SlideBody",
        fontName="Helvetica",
        fontSize=12,
        textColor=DARK_GRAY,
        spaceAfter=8,
        leading=17,
    ))
    styles.add(ParagraphStyle(
        name="SlideBodyBold",
        fontName="Helvetica-Bold",
        fontSize=12,
        textColor=DARK_GRAY,
        spaceAfter=8,
        leading=17,
    ))
    styles.add(ParagraphStyle(
        name="SlideBullet",
        fontName="Helvetica",
        fontSize=11,
        textColor=DARK_GRAY,
        leftIndent=24,
        spaceAfter=5,
        leading=16,
    ))
    styles.add(ParagraphStyle(
        name="BigNumber",
        fontName="Helvetica-Bold",
        fontSize=42,
        textColor=BLUE,
        alignment=TA_CENTER,
        spaceAfter=2,
        leading=48,
    ))
    styles.add(ParagraphStyle(
        name="BigNumberLabel",
        fontName="Helvetica",
        fontSize=11,
        textColor=MED_GRAY,
        alignment=TA_CENTER,
        spaceAfter=12,
        leading=14,
    ))
    styles.add(ParagraphStyle(
        name="QuoteText",
        fontName="Helvetica-Oblique",
        fontSize=16,
        textColor=SOFT_NAVY,
        alignment=TA_CENTER,
        spaceBefore=20,
        spaceAfter=12,
        leading=24,
        leftIndent=40,
        rightIndent=40,
    ))
    styles.add(ParagraphStyle(
        name="SmallNote",
        fontName="Helvetica",
        fontSize=8,
        textColor=MED_GRAY,
        alignment=TA_LEFT,
        spaceAfter=4,
        leading=10,
    ))
    styles.add(ParagraphStyle(
        name="CoverTitle",
        fontName="Helvetica-Bold",
        fontSize=36,
        textColor=NAVY,
        alignment=TA_LEFT,
        spaceAfter=8,
        leading=42,
    ))
    styles.add(ParagraphStyle(
        name="CoverSubtitle",
        fontName="Helvetica",
        fontSize=16,
        textColor=SOFT_NAVY,
        alignment=TA_LEFT,
        spaceAfter=6,
        leading=22,
    ))
    styles.add(ParagraphStyle(
        name="CoverTagline",
        fontName="Helvetica-Oblique",
        fontSize=12,
        textColor=MED_GRAY,
        alignment=TA_LEFT,
        spaceAfter=4,
        leading=16,
    ))
    styles.add(ParagraphStyle(
        name="TableHeaderStyle",
        fontName="Helvetica-Bold",
        fontSize=10,
        textColor=WHITE,
        alignment=TA_LEFT,
        leading=13,
    ))
    styles.add(ParagraphStyle(
        name="TableCellStyle",
        fontName="Helvetica",
        fontSize=10,
        textColor=DARK_GRAY,
        alignment=TA_LEFT,
        leading=13,
    ))
    styles.add(ParagraphStyle(
        name="TableCellBold",
        fontName="Helvetica-Bold",
        fontSize=10,
        textColor=NAVY,
        alignment=TA_LEFT,
        leading=13,
    ))
    styles.add(ParagraphStyle(
        name="FooterText",
        fontName="Helvetica",
        fontSize=8,
        textColor=LAVENDER,
        alignment=TA_RIGHT,
    ))
    return styles


def hr():
    return HRFlowable(
        width="100%", thickness=1.5, color=LAVENDER,
        spaceBefore=6, spaceAfter=10
    )


def slide_break():
    return PageBreak()


def fig_to_image(fig, width=8.5, height=4.5):
    """Convert matplotlib figure to reportlab Image flowable."""
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=200, bbox_inches="tight",
                facecolor="white", edgecolor="none")
    plt.close(fig)
    buf.seek(0)
    img = Image(buf, width=width * inch, height=height * inch)
    return img


def setup_chart_style():
    """Set matplotlib defaults for brand consistency."""
    plt.rcParams.update({
        "font.family": "Helvetica",
        "font.size": 11,
        "axes.titlesize": 14,
        "axes.titleweight": "bold",
        "axes.labelsize": 11,
        "axes.edgecolor": C_MED_GRAY,
        "axes.linewidth": 0.8,
        "xtick.color": C_MED_GRAY,
        "ytick.color": C_MED_GRAY,
        "grid.alpha": 0.3,
        "grid.color": "#cccccc",
    })


# ── CHART GENERATORS ─────────────────────────────────────────────────

def chart_layoff_trend():
    """Bar chart: annual job cuts 2023-2025."""
    fig, ax = plt.subplots(figsize=(9, 4.2))
    years = ["2023", "2024", "2025"]
    cuts = [265000, 761358, 1206374]
    colors = [C_LAVENDER, C_BLUE, C_AMBER]

    bars = ax.bar(years, cuts, color=colors, width=0.55, edgecolor="white", linewidth=1.5)
    for bar, val in zip(bars, cuts):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 25000,
                f"{val:,.0f}", ha="center", va="bottom", fontsize=13,
                fontweight="bold", color=C_NAVY)

    ax.set_ylabel("job cuts announced", fontsize=11, color=C_MED_GRAY)
    ax.set_title("the layoff cycle is accelerating", fontsize=16,
                 fontweight="bold", color=C_NAVY, pad=12)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x/1e6:.1f}M" if x >= 1e6 else f"{x/1e3:.0f}K"))
    ax.set_ylim(0, 1500000)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    ax.annotate("+58% YoY", xy=(2, 1206374), xytext=(2.35, 1100000),
                fontsize=12, fontweight="bold", color=C_RED,
                arrowprops=dict(arrowstyle="->", color=C_RED, lw=1.5))

    # DOGE annotation
    ax.annotate("includes 350K+\nDOGE federal cuts", xy=(2, 600000),
                fontsize=9, color=C_MED_GRAY, ha="center", style="italic")

    fig.tight_layout()
    return fig


def chart_tam_sam_som():
    """Horizontal bar chart: updated TAM/SAM/SOM with B2B."""
    fig, ax = plt.subplots(figsize=(9, 4.2))

    labels = ["SOM (year 1)", "SOM (year 3)", "SAM", "TAM (B2C)", "TAM (combined)"]
    values = [90, 1000, 7200, 71100, 102000]
    colors = [C_AMBER, C_RED, C_BLUE, C_SOFT_NAVY, C_NAVY]
    display = [
        "$60K-$120K",
        "$800K-$1.2M",
        "$7.2M reachable",
        "$71.1M (B2C individuals)",
        "$102M (B2C + B2B)",
    ]

    bars = ax.barh(labels, values, color=colors, height=0.5, edgecolor="white", linewidth=1.5)
    ax.set_xscale("log")
    ax.set_xlim(20, 300000)

    for bar, disp in zip(bars, display):
        ax.text(bar.get_width() * 1.3, bar.get_y() + bar.get_height()/2,
                disp, va="center", fontsize=11, color=C_NAVY)

    ax.set_title("market sizing: TAM / SAM / SOM (updated with B2B)", fontsize=16,
                 fontweight="bold", color=C_NAVY, pad=12)
    ax.xaxis.set_visible(False)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["bottom"].set_visible(False)

    fig.tight_layout()
    return fig


def chart_quiz_vs_pdf():
    """Grouped bar chart: quiz funnel vs PDF lead magnet conversion metrics."""
    fig, ax = plt.subplots(figsize=(9, 4.2))

    metrics = ["email opt-in\nrate", "IG-specific\nconversion", "revenue per\nrecipient", "email click-\nthrough rate"]
    pdf_vals = [18, 15, 6, 1.0]
    quiz_vals = [40.1, 40.8, 19, 2.0]

    x = np.arange(len(metrics))
    w = 0.32

    bars1 = ax.bar(x - w/2, pdf_vals, w, label="PDF lead magnet", color=C_LAVENDER, edgecolor="white", linewidth=1)
    bars2 = ax.bar(x + w/2, quiz_vals, w, label="quiz funnel", color=C_AMBER, edgecolor="white", linewidth=1)

    for bar, val in zip(bars1, pdf_vals):
        label = f"${val/100:.2f}" if val < 10 else f"{val}%"
        if val == 1.0:
            label = "1x"
        if val == 6:
            label = "$0.06"
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.8,
                label, ha="center", va="bottom", fontsize=10, color=C_MED_GRAY)

    for bar, val in zip(bars2, quiz_vals):
        label = f"${val/100:.2f}" if val < 10 else f"{val}%"
        if val == 2.0:
            label = "2x"
        if val == 19:
            label = "$0.19"
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.8,
                label, ha="center", va="bottom", fontsize=10, fontweight="bold", color=C_NAVY)

    improvements = ["+123%", "+172%", "+217%", "+101%"]
    for i, imp in enumerate(improvements):
        ax.text(x[i] + w/2, quiz_vals[i] + 3.5, imp, ha="center",
                fontsize=9, fontweight="bold", color=C_RED)

    ax.set_xticks(x)
    ax.set_xticklabels(metrics, fontsize=10)
    ax.set_title("quiz funnel vs. PDF lead magnet", fontsize=16,
                 fontweight="bold", color=C_NAVY, pad=12)
    ax.legend(fontsize=10, loc="upper left", framealpha=0.9)
    ax.set_ylim(0, 55)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.yaxis.set_visible(False)

    fig.tight_layout()
    return fig


def chart_value_ladder():
    """Horizontal step chart: the 6-tier value ladder."""
    fig, ax = plt.subplots(figsize=(9, 4.5))

    tiers = [
        "Free\n(quiz + 5-day practice)",
        "$9-$47\n(workbooks + bundles)",
        "$197\n(6-week course)",
        "$39/mo\n(membership)",
        "$997-$3K\n(coaching)",
        "$1.5K-$25K\n(B2B corporate)",
    ]
    # Representative revenue potential (year 3)
    revenue = [0, 90, 158, 281, 100, 316]
    colors = [C_LAVENDER, C_BLUE, C_AMBER, C_RED, C_SOFT_NAVY, C_NAVY]

    y_pos = range(len(tiers) - 1, -1, -1)
    bars = ax.barh(list(y_pos), revenue, color=colors, height=0.55, edgecolor="white", linewidth=2)

    for bar, rev, tier in zip(bars, revenue, tiers):
        if rev > 0:
            ax.text(bar.get_width() + 5, bar.get_y() + bar.get_height()/2,
                    f"${rev}K/yr", va="center", fontsize=11,
                    fontweight="bold", color=C_NAVY)

    ax.set_yticks(list(y_pos))
    ax.set_yticklabels(tiers, fontsize=10)
    ax.set_title("the value ladder: year 3 revenue potential by tier ($K)", fontsize=16,
                 fontweight="bold", color=C_NAVY, pad=12)
    ax.set_xlim(0, 400)
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:.0f}K"))
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    # Total annotation
    ax.text(350, -0.8, "total: $945K+", fontsize=14, fontweight="bold",
            color=C_NAVY, ha="center",
            bbox=dict(boxstyle="round,pad=0.3", facecolor=C_AMBER, alpha=0.3))

    fig.tight_layout()
    return fig


def chart_revenue_by_stream():
    """Horizontal bar chart: $1M revenue breakdown by stream (year 3)."""
    fig, ax = plt.subplots(figsize=(9, 4.5))

    streams = [
        "membership ($39/mo)",
        "digital course ($197)",
        "corporate workshops",
        "corporate packages",
        "outplacement licensing",
        "workbooks ($9-$47)",
        "1:1 coaching ($3K)",
        "speaking + affiliate",
        "group coaching ($997)",
    ]
    revenue = [281, 158, 120, 100, 96, 90, 60, 50, 40]
    colors_list = [C_AMBER, C_BLUE, C_NAVY, C_SOFT_NAVY, C_SOFT_NAVY,
                   C_LAVENDER, C_RED, C_MED_GRAY, C_RED]
    # Mark B2B vs B2C
    is_b2b = [False, False, True, True, True, False, False, False, False]

    bars = ax.barh(range(len(streams) - 1, -1, -1), revenue, color=colors_list,
                   height=0.6, edgecolor="white", linewidth=1.5)

    for i, (bar, rev, b2b) in enumerate(zip(bars, revenue, is_b2b)):
        label = f"${rev}K"
        if b2b:
            label += " (B2B)"
        ax.text(bar.get_width() + 3, bar.get_y() + bar.get_height()/2,
                label, va="center", fontsize=10, color=C_NAVY)

    ax.set_yticks(range(len(streams) - 1, -1, -1))
    ax.set_yticklabels(streams, fontsize=10)
    ax.set_title("$1M revenue breakdown by stream (year 3 target)", fontsize=16,
                 fontweight="bold", color=C_NAVY, pad=12)
    ax.set_xlim(0, 350)
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:.0f}K"))
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    # B2C/B2B split annotation
    ax.text(280, 0, "B2C: 63%  |  B2B: 32%  |  other: 5%", fontsize=10,
            color=C_MED_GRAY, ha="center",
            bbox=dict(boxstyle="round,pad=0.3", facecolor="#f5f6fa", alpha=0.8))

    fig.tight_layout()
    return fig


def chart_36month_revenue():
    """Line chart: 36-month revenue trajectory showing path to $1M."""
    fig, ax = plt.subplots(figsize=(9, 4.5))

    # Monthly cumulative revenue from business-plan-1m.md
    months = list(range(1, 37))

    # Year 1: month-by-month from business plan
    y1_monthly = [800, 1200, 2500, 5000, 6000, 7500, 9000, 10500, 11500, 12500, 14000, 15000]
    y1_cumulative = []
    running = 0
    for m in y1_monthly:
        running += m
        y1_cumulative.append(running)

    # Year 2: quarterly from business plan ($60K, $85K, $110K, $140K)
    y2_quarterly = [60000, 85000, 110000, 140000]
    y2_monthly_avg = []
    for q in y2_quarterly:
        monthly = q / 3
        for _ in range(3):
            y2_monthly_avg.append(monthly)
    y2_cumulative = []
    running = y1_cumulative[-1]
    for m in y2_monthly_avg:
        running += m
        y2_cumulative.append(running)

    # Year 3: quarterly ($200K, $250K, $275K, $300K)
    y3_quarterly = [200000, 250000, 275000, 300000]
    y3_monthly_avg = []
    for q in y3_quarterly:
        monthly = q / 3
        for _ in range(3):
            y3_monthly_avg.append(monthly)
    y3_cumulative = []
    running = y2_cumulative[-1]
    for m in y3_monthly_avg:
        running += m
        y3_cumulative.append(running)

    cumulative = y1_cumulative + y2_cumulative + y3_cumulative

    # Also plot monthly revenue
    all_monthly = y1_monthly + y2_monthly_avg + y3_monthly_avg

    ax.fill_between(months, cumulative, alpha=0.15, color=C_AMBER)
    ax.plot(months, cumulative, color=C_AMBER, linewidth=3, label="cumulative revenue")

    # Monthly revenue on secondary axis
    ax2 = ax.twinx()
    ax2.bar(months, all_monthly, color=C_BLUE, alpha=0.3, width=0.7, label="monthly revenue")
    ax2.set_ylabel("monthly revenue ($)", fontsize=10, color=C_BLUE)
    ax2.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x/1000:.0f}K"))
    ax2.spines["top"].set_visible(False)
    ax2.tick_params(axis="y", colors=C_BLUE)

    # Year markers
    for yr_month, yr_label, yr_rev in [(12, "year 1\n$95K", 95500),
                                        (24, "year 2\n$490K", y2_cumulative[-1]),
                                        (36, "year 3\n$1.52M", y3_cumulative[-1])]:
        ax.axvline(x=yr_month, color=C_MED_GRAY, linewidth=0.8, linestyle="--", alpha=0.5)

    # $1M line
    ax.axhline(y=1000000, color=C_GREEN, linewidth=2, linestyle="--", alpha=0.7)
    ax.text(2, 1050000, "$1M cumulative", fontsize=10, fontweight="bold", color=C_GREEN)

    ax.set_xlabel("month", fontsize=11, color=C_MED_GRAY)
    ax.set_ylabel("cumulative revenue ($)", fontsize=11, color=C_MED_GRAY)
    ax.set_title("36-month revenue trajectory: path to $1M+", fontsize=16,
                 fontweight="bold", color=C_NAVY, pad=12)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(
        lambda x, _: f"${x/1e6:.1f}M" if x >= 1e6 else f"${x/1000:.0f}K"))
    ax.set_ylim(0, max(cumulative) * 1.1)
    ax.set_xlim(0.5, 36.5)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(axis="y", alpha=0.3)
    ax.legend(fontsize=10, loc="upper left", framealpha=0.9)

    fig.tight_layout()
    return fig


def chart_year1_old_vs_new():
    """Grouped bar: old model vs new model year 1 revenue."""
    fig, ax = plt.subplots(figsize=(9, 4))

    categories = ["workbooks\nonly", "workbooks +\ncourse", "workbooks +\ncourse +\nmembership", "full model\n(+ B2B +\ncoaching)"]
    revenue = [16000, 42000, 56000, 95500]
    colors = [C_LAVENDER, C_BLUE, C_AMBER, C_NAVY]

    bars = ax.bar(categories, revenue, color=colors, width=0.55, edgecolor="white", linewidth=1.5)

    for bar, val in zip(bars, revenue):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1500,
                f"${val:,.0f}", ha="center", va="bottom", fontsize=13,
                fontweight="bold", color=C_NAVY)

    # Improvement arrow
    ax.annotate("6x more\nrevenue", xy=(3, 95500), xytext=(3.4, 60000),
                fontsize=12, fontweight="bold", color=C_GREEN,
                arrowprops=dict(arrowstyle="->", color=C_GREEN, lw=2))

    ax.set_title("year 1 revenue: old model vs. new value ladder", fontsize=16,
                 fontweight="bold", color=C_NAVY, pad=12)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x/1000:.0f}K"))
    ax.set_ylim(0, 120000)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    fig.tight_layout()
    return fig


def chart_profitability_36mo():
    """Area chart: 36-month cumulative profit."""
    fig, ax = plt.subplots(figsize=(9, 4))

    years = ["Year 1", "Year 2", "Year 3"]
    revenue = [95500, 395000, 1025000]
    costs = [20024, 102000, 240000]
    profit = [r - c for r, c in zip(revenue, costs)]
    margins = [p / r * 100 for p, r in zip(profit, revenue)]

    x = np.arange(len(years))
    w = 0.3

    bars_r = ax.bar(x - w/2, revenue, w, label="revenue", color=C_AMBER, edgecolor="white", linewidth=1)
    bars_c = ax.bar(x + w/2, costs, w, label="costs", color=C_MED_GRAY, edgecolor="white", linewidth=1, alpha=0.6)

    for i, (xi, p, m) in enumerate(zip(x, profit, margins)):
        ax.text(xi, max(revenue[i], costs[i]) + 25000,
                f"+${p:,.0f}\n({m:.0f}% margin)", ha="center", fontsize=11,
                fontweight="bold", color=C_GREEN)

    ax.set_xticks(x)
    ax.set_xticklabels(years, fontsize=12)
    ax.set_title("revenue vs. costs: 3-year profitability", fontsize=16,
                 fontweight="bold", color=C_NAVY, pad=12)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(
        lambda x, _: f"${x/1e6:.1f}M" if x >= 1e6 else f"${x/1000:.0f}K"))
    ax.legend(fontsize=10, loc="upper left", framealpha=0.9)
    ax.set_ylim(0, 1200000)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    fig.tight_layout()
    return fig


def chart_funnel_conversion():
    """Funnel visualization: extended value ladder conversion."""
    fig, ax = plt.subplots(figsize=(9, 4.5))

    steps = [
        "quiz starts\n(all channels)",
        "email signups\n(40% opt-in)",
        "workbook buyers\n(10-12%)",
        "course enrollees\n(15-20%)",
        "members\n(25-30%)",
        "coaching clients\n(3-5%)",
    ]
    values = [5000, 2000, 220, 40, 12, 2]
    colors = [C_NAVY, C_SOFT_NAVY, C_BLUE, C_AMBER, C_RED, C_LAVENDER]
    revenue_per = ["$0", "$0", "$18 avg", "$197", "$39/mo", "$997+"]

    bars = ax.barh(range(len(steps)-1, -1, -1), values, color=colors,
                   height=0.55, edgecolor="white", linewidth=2)

    for i, (bar, val, step, rev) in enumerate(zip(bars, values, steps, revenue_per)):
        text_x = max(val/2, 100)
        ax.text(text_x, len(steps)-1-i, f"{val:,}/mo",
                ha="center", va="center", fontsize=11,
                fontweight="bold", color="white" if i < 3 else C_NAVY)
        # Revenue label on right
        ax.text(5200, len(steps)-1-i, rev, va="center", fontsize=10,
                color=C_MED_GRAY, style="italic")

    ax.set_yticks(range(len(steps)))
    ax.set_yticklabels(list(reversed(steps)), fontsize=10)
    ax.set_title("monthly funnel: quiz → coaching (month 12 projections)", fontsize=16,
                 fontweight="bold", color=C_NAVY, pad=12)
    ax.set_xlim(0, 6000)
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:,.0f}"))
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    fig.tight_layout()
    return fig


# ── SLIDE BUILDERS ────────────────────────────────────────────────────

def make_table(styles, headers, rows, col_widths=None):
    header_row = [Paragraph(h, styles["TableHeaderStyle"]) for h in headers]
    data = [header_row]
    for row in rows:
        cells = []
        for c in row:
            if isinstance(c, str) and c.startswith("**"):
                cells.append(Paragraph(c.replace("**", ""), styles["TableCellBold"]))
            else:
                cells.append(Paragraph(str(c), styles["TableCellStyle"]))
        data.append(cells)

    if col_widths is None:
        n = len(headers)
        col_widths = [PAGE_W * 0.85 / n] * n

    t = Table(data, colWidths=col_widths)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("BACKGROUND", (0, 1), (-1, -1), LIGHT_GRAY),
        ("GRID", (0, 0), (-1, -1), 0.5, HexColor("#e0e0e0")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, LIGHT_GRAY]),
    ]))
    return t


def metric_box(styles, number, label):
    """Create a metric display (big number + label)."""
    return [
        Paragraph(str(number), styles["BigNumber"]),
        Paragraph(label, styles["BigNumberLabel"]),
    ]


def build_deck():
    setup_chart_style()
    s = create_styles()
    story = []

    # ── SLIDE 1: COVER ──────────────────────────────────────
    story.append(Spacer(1, 1.5 * inch))
    story.append(Paragraph("luminous pulse", s["CoverTitle"]))
    story.append(Spacer(1, 8))
    story.append(Paragraph("the path to $1M: market opportunity &amp; growth strategy", s["CoverSubtitle"]))
    story.append(Spacer(1, 16))
    story.append(HRFlowable(width="40%", thickness=3, color=AMBER, spaceBefore=0, spaceAfter=16))
    story.append(Paragraph("grounding workbooks \u00b7 online course \u00b7 membership \u00b7 B2B corporate", s["CoverTagline"]))
    story.append(Paragraph("multi-platform: instagram + pinterest + etsy + linkedin + SEO", s["CoverTagline"]))
    story.append(Spacer(1, 1 * inch))
    story.append(Paragraph("Christie Parrow \u00b7 February 2026", s["SlideBody"]))
    story.append(slide_break())

    # ── SLIDE 2: THE PROBLEM ────────────────────────────────
    story.append(Paragraph("the problem", s["SlideTitle"]))
    story.append(hr())
    story.append(Paragraph(
        '"the crisis isn\'t a skills gap. it\'s an identity gap."',
        s["QuoteText"]
    ))
    story.append(Spacer(1, 16))

    metrics_data = [
        metric_box(s, "1.2M", "job cuts in 2025\n(+58% from 2024)"),
        metric_box(s, "350K+", "federal workers cut\nby DOGE (2025)"),
        metric_box(s, "60%", "never talk about\ntheir mental health"),
        metric_box(s, "70%", "of college grads tie\nidentity to their job"),
    ]
    row1 = [metrics_data[0][0], metrics_data[1][0], metrics_data[2][0], metrics_data[3][0]]
    row2 = [metrics_data[0][1], metrics_data[1][1], metrics_data[2][1], metrics_data[3][1]]
    t = Table([row1, row2], colWidths=[PAGE_W * 0.2] * 4)
    t.setStyle(TableStyle([
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    story.append(t)
    story.append(Spacer(1, 16))
    story.append(Paragraph(
        "every month, ~100K new people join them. 350,000+ federal workers were displaced by DOGE in 2025 alone. "
        "even after reemployment, research shows life satisfaction does NOT fully recover. the identity wound persists.",
        s["SlideBody"]
    ))
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "sources: BLS Displaced Workers Survey 2024, Challenger Gray &amp; Christmas 2025, OPM / DOGE data, Mind Share Partners, Gallup",
        s["SmallNote"]
    ))
    story.append(slide_break())

    # ── SLIDE 3: THE ACCELERATION ───────────────────────────
    story.append(Paragraph("the market is growing", s["SlideTitle"]))
    story.append(hr())
    story.append(fig_to_image(chart_layoff_trend(), width=8.5, height=4.0))
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "2025 saw 1.2M announced job cuts \u2014 the highest since 2009. 350K+ federal workers displaced by DOGE. "
        "total layoffs &amp; discharges across all industries: ~20.8M/year (BLS JOLTS).",
        s["SmallNote"]
    ))
    story.append(slide_break())

    # ── SLIDE 4: TAM / SAM / SOM ────────────────────────────
    story.append(Paragraph("TAM / SAM / SOM (updated with B2B)", s["SlideTitle"]))
    story.append(hr())
    story.append(fig_to_image(chart_tam_sam_som(), width=8.5, height=4.0))
    story.append(Spacer(1, 8))

    tam_table = make_table(s,
        ["", "B2C", "B2B", "total"],
        [
            ["**TAM**", "$71.1M (3.95M people)", "$31M (outplacement + corporate)", "**$102M**"],
            ["**SAM**", "$4.1M (227K reachable)", "$3.1M (addressable firms)", "**$7.2M**"],
            ["**SOM yr 1**", "$50K-$80K", "$10K-$40K", "**$60K-$120K**"],
            ["**SOM yr 3**", "$350K-$550K", "$300K-$450K", "**$650K-$1M+**"],
        ],
        col_widths=[1.2*inch, 3*inch, 3*inch, 1.6*inch]
    )
    story.append(tam_table)
    story.append(slide_break())

    # ── SLIDE 5: THE WHITESPACE ─────────────────────────────
    story.append(Paragraph("the whitespace", s["SlideTitle"]))
    story.append(hr())
    story.append(Paragraph(
        '"career coaching addresses skills. therapy addresses clinical conditions. '
        'but the \u201cwho am I without my job title?\u201d question \u2014 experienced by 55-70% of '
        'displaced professionals \u2014 has no mainstream product addressing it."',
        s["QuoteText"]
    ))
    story.append(Spacer(1, 12))
    bullets = [
        "\u2022  career coaches: tactical \u2014 resumes, networking, interview prep. $100-$300/session.",
        "\u2022  therapists: clinical \u2014 require diagnosis, insurance, scheduling. $150-$250/session.",
        "\u2022  outplacement firms: tactical \u2014 $500-$1,900/employee. zero emotional support.",
        "\u2022  self-help books: generic \u2014 not specific to displacement. not private. not printable.",
        "\u2022  <b>luminous pulse</b>: emotional grounding for silent sufferers. $9-$47 workbooks \u2192 $197 course \u2192 $39/mo membership \u2192 $1,500-$25K B2B corporate.",
    ]
    for b in bullets:
        story.append(Paragraph(b, s["SlideBullet"]))
    story.append(Spacer(1, 12))
    story.append(Paragraph(
        "adjacent markets: outplacement ($5.65B, CAGR 7.6%), US mental wellness ($73.3B), "
        "personal development ($51.6B), journals &amp; planners ($1.12B).",
        s["SmallNote"]
    ))
    story.append(slide_break())

    # ── SLIDE 6: THE VALUE LADDER ────────────────────────────
    story.append(Paragraph("the value ladder", s["SlideTitle"]))
    story.append(hr())
    story.append(Paragraph(
        "workbooks are the trust-builder, not the business model. the real revenue comes from "
        "higher-ticket products, recurring membership, and B2B corporate.",
        s["SlideSubtitle"]
    ))
    story.append(Spacer(1, 4))
    story.append(fig_to_image(chart_value_ladder(), width=8.5, height=4.2))
    story.append(slide_break())

    # ── SLIDE 7: THE PRODUCT LINE ────────────────────────────
    story.append(Paragraph("the complete product architecture", s["SlideTitle"]))
    story.append(hr())

    prod_table = make_table(s,
        ["tier", "product", "price", "role"],
        [
            ["free", "quiz + 5-day practice PDF", "$0", "email capture, segmentation"],
            ["entry", "8 workbooks + 2 bundles", "$9-$47", "first purchase, trust"],
            ["mid", '"grounded through change" course', "$197", "6-week, self-paced, video + community"],
            ["recurring", '"the sanctuary" membership', "$39/mo", "monthly workbook, weekly live, community"],
            ["high", '"rebuild" group coaching', "$997", "12-week, 8-12 per cohort, quarterly"],
            ["high", "1:1 coaching", "$3,000", "6 sessions, limited to 20/year"],
            ["B2B", "single workshop", "$1,500", "90-min virtual, team of 10-50"],
            ["B2B", "workshop package (4 sessions)", "$5,000", "4-6 weeks for displaced teams"],
            ["B2B", "annual license", "$12,000/yr", "unlimited access + quarterly workshops"],
        ],
        col_widths=[0.8*inch, 2.8*inch, 1.2*inch, 4*inch]
    )
    story.append(prod_table)
    story.append(slide_break())

    # ── SLIDE 8: THE QUIZ FUNNEL ─────────────────────────────
    story.append(Paragraph("the quiz funnel: acquisition engine", s["SlideTitle"]))
    story.append(hr())
    story.append(fig_to_image(chart_quiz_vs_pdf(), width=8.5, height=4.0))
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "a quiz converts 2.2x more email subscribers and generates 3x more revenue per recipient. "
        "for sam \u2014 ashamed, exhausted, drowning in unnamed feelings \u2014 a self-assessment that says "
        "\u201cyou're experiencing this\u201d is the first moment someone sees them. "
        "the quiz feeds the entire value ladder: workbook \u2192 course \u2192 membership \u2192 coaching.",
        s["SlideBody"]
    ))
    story.append(slide_break())

    # ── SLIDE 9: FUNNEL MATH ─────────────────────────────────
    story.append(Paragraph("the funnel math: quiz to coaching", s["SlideTitle"]))
    story.append(hr())
    story.append(fig_to_image(chart_funnel_conversion(), width=8.5, height=4.2))
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "month 12 projections: 5,000 quiz starts/month across all channels (IG, Pinterest, Etsy, SEO, ads). "
        "a sam who enters at $12 (workbook) and ascends to course ($197) + membership ($468/year) has a $677+ LTV.",
        s["SlideBody"]
    ))
    story.append(slide_break())

    # ── SLIDE 10: $1M REVENUE BREAKDOWN ──────────────────────
    story.append(Paragraph("the $1M revenue model", s["SlideTitle"]))
    story.append(hr())
    story.append(fig_to_image(chart_revenue_by_stream(), width=8.5, height=4.2))
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "B2B represents ~32% of revenue but requires far fewer transactions. "
        "8 licensing deals + 100 workshops = $316K. the same revenue from workbooks alone would require 17,556 individual sales.",
        s["SlideBody"]
    ))
    story.append(slide_break())

    # ── SLIDE 11: 36-MONTH TRAJECTORY ────────────────────────
    story.append(Paragraph("36-month revenue trajectory", s["SlideTitle"]))
    story.append(hr())
    story.append(fig_to_image(chart_36month_revenue(), width=8.5, height=4.2))
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "year 1: $95K (foundation \u2014 workbooks + course launch + membership beta + first B2B clients). "
        "year 2: $395K (scale ads, 10-20 corporate clients, 500+ members). "
        "year 3: $1.025M (full value ladder, B2B channel established, small team).",
        s["SlideBodyBold"]
    ))
    story.append(slide_break())

    # ── SLIDE 12: YEAR 1 OLD VS NEW ──────────────────────────
    story.append(Paragraph("year 1: why the value ladder changes everything", s["SlideTitle"]))
    story.append(hr())
    story.append(fig_to_image(chart_year1_old_vs_new(), width=8.5, height=3.8))
    story.append(Spacer(1, 12))

    story.append(Paragraph(
        "the original model (workbooks only) projected $10K-$16K in year 1. "
        "the value ladder generates <b>6x more revenue</b> from the same audience by extending "
        "the customer journey: workbook buyer \u2192 course student \u2192 member \u2192 coaching client.",
        s["SlideBody"]
    ))
    story.append(slide_break())

    # ── SLIDE 13: B2B CORPORATE STRATEGY ─────────────────────
    story.append(Paragraph("B2B: workforce transition resilience program", s["SlideTitle"]))
    story.append(hr())
    story.append(Paragraph(
        "the outplacement market is $5.65B and growing 7.6%/year. luminous pulse fills "
        "the emotional gap that traditional outplacement ignores.",
        s["SlideSubtitle"]
    ))
    story.append(Spacer(1, 8))

    b2b_table = make_table(s,
        ["offering", "price", "for", "delivery"],
        [
            ["single workshop", "$1,500", "displaced teams (10-50 people)", "90-min virtual, workbook bundle included"],
            ["4-session package", "$5,000", "companies conducting layoffs", "4 sessions over 4-6 weeks, full curriculum"],
            ["annual license", "$12,000/yr", "outplacement firms, EAPs", "unlimited digital access + 4 workshops/yr"],
        ],
        col_widths=[1.8*inch, 1*inch, 2.8*inch, 3.2*inch]
    )
    story.append(b2b_table)
    story.append(Spacer(1, 12))

    b2b_bullets = [
        "\u2022  <b>5-10x cheaper</b> than traditional outplacement ($30-$50/employee vs. $500-$1,900).",
        "\u2022  <b>complement, not replacement</b> \u2014 companies can offer both career services + emotional grounding.",
        "\u2022  <b>target buyers:</b> HR directors (use layoffs.fyi for leads), outplacement firm partners, EAP providers.",
        "\u2022  <b>timeline:</b> free workshops for case studies (month 6) \u2192 first paid (month 7-8) \u2192 first license (month 11-12).",
    ]
    for b in b2b_bullets:
        story.append(Paragraph(b, s["SlideBullet"]))
    story.append(slide_break())

    # ── SLIDE 14: MULTI-PLATFORM STRATEGY ────────────────────
    story.append(Paragraph("multi-platform distribution", s["SlideTitle"]))
    story.append(hr())
    story.append(Paragraph(
        "instagram alone caps reach at ~227K reachable sams. the $1M plan needs more channels.",
        s["SlideSubtitle"]
    ))
    story.append(Spacer(1, 8))

    platform_table = make_table(s,
        ["channel", "role", "revenue impact", "when"],
        [
            ["**instagram**", "community, DM sales, paid ads, quiz traffic", "medium", "now"],
            ["**pinterest**", "evergreen discovery engine (6.2x ROAS)", "HIGH", "month 1"],
            ["**etsy**", "marketplace for printable workbooks", "HIGH ($10K+/mo potential)", "month 1-2"],
            ["**linkedin**", "B2B outreach, displaced professionals", "HIGH for B2B", "month 3"],
            ["**SEO/blog**", 'captures "grounding after layoff" searches', "HIGH long-term", "month 1"],
            ["**youtube**", "authority building, course promotion", "medium-high", "month 4-6"],
            ["**tiktok**", "viral discovery, brand awareness", "medium", "month 3-4"],
            ["**amazon KDP**", "physical workbook versions", "medium — passive", "month 6+"],
        ],
        col_widths=[1.5*inch, 3*inch, 2*inch, 1.5*inch]
    )
    story.append(platform_table)
    story.append(slide_break())

    # ── SLIDE 15: PROFITABILITY ──────────────────────────────
    story.append(Paragraph("3-year profitability", s["SlideTitle"]))
    story.append(hr())
    story.append(fig_to_image(chart_profitability_36mo(), width=8.5, height=3.8))
    story.append(Spacer(1, 8))

    profit_bullets = [
        "\u2022  year 1: <b>$95K revenue, $20K costs, $75K profit (79% margin)</b>",
        "\u2022  year 2: <b>$395K revenue, $102K costs, $293K profit (74% margin)</b>",
        "\u2022  year 3: <b>$1.025M revenue, $240K costs, $785K profit (77% margin)</b>",
        "\u2022  digital products + membership = structurally high margins even at scale",
    ]
    for b in profit_bullets:
        story.append(Paragraph(b, s["SlideBullet"]))
    story.append(slide_break())

    # ── SLIDE 16: 36-MONTH MILESTONES ────────────────────────
    story.append(Paragraph("36-month milestones", s["SlideTitle"]))
    story.append(hr())

    miles_table = make_table(s,
        ["milestone", "target", "when"],
        [
            ["quiz live + etsy store launched", "done + 8 listings", "month 1-2"],
            ["pinterest active, 3 blog posts live", "50+ pins", "month 1-2"],
            ["first $1,000 revenue month", "multi-channel", "month 3-4"],
            ["digital course launched", "30+ first cohort", "month 4"],
            ["1,000 email subscribers", "all channels", "month 4-5"],
            ['"the sanctuary" membership launched', "30+ founding members", "month 6"],
            ["first paid corporate workshop", "$1,500", "month 7-8"],
            ["first $10,000 revenue month", "all streams active", "month 10-11"],
            ["first licensing deal signed", "$12,000/yr", "month 11-12"],
            ["**year 1 total**", "**$85K-$120K**", "month 12"],
            ["membership at 250+ members", "$9,750/mo recurring", "month 15"],
            ["10+ corporate clients", "$15K+/mo B2B", "month 16-18"],
            ["**year 2 total**", "**$300K-$500K**", "month 24"],
            ["membership at 500+ members", "$19,500/mo recurring", "month 24"],
            ["first $80,000 revenue month", "all engines running", "month 30-33"],
            ["**year 3 total**", "**$800K-$1.2M**", "month 36"],
        ],
        col_widths=[4*inch, 2.5*inch, 2*inch]
    )
    story.append(miles_table)
    story.append(slide_break())

    # ── SLIDE 17: COSTS ──────────────────────────────────────
    story.append(Paragraph("investment requirements", s["SlideTitle"]))
    story.append(hr())

    cost_table = make_table(s,
        ["item", "year 1 cost", "notes"],
        [
            ["ad spend (scaling)", "$10,200", "$150/mo → $1,500/mo over 12 months"],
            ["tools (Kit, Interact, course platform, Zoom)", "$3,300", "free tiers → $200-$300/mo at scale"],
            ["VA (months 10-12)", "$1,500", "10 hrs/week"],
            ["content creation (freelance)", "$2,400", "$200/mo avg"],
            ["B2B materials (design, legal)", "$800", "one-time"],
            ["course production", "$1,500", "filming, editing, platform setup"],
            ["miscellaneous", "$1,800", "$150/mo"],
            ["**total year 1**", "**$20,024**", "**$95K revenue = 79% margin**"],
        ],
        col_widths=[3.5*inch, 1.5*inch, 3.5*inch]
    )
    story.append(cost_table)
    story.append(Spacer(1, 12))

    cost_bullets = [
        "\u2022  <b>total product development investment:</b> ~$1,500-$6,000 + time (course, B2B deck, licensing package)",
        "\u2022  <b>break-even point:</b> month 1 \u2014 digital products have near-zero marginal cost",
        "\u2022  <b>year 3 costs:</b> ~$240K (team $120K, ads $60K, tools $12K, travel $15K, content $15K, legal $8K, misc $10K)",
    ]
    for b in cost_bullets:
        story.append(Paragraph(b, s["SlideBullet"]))
    story.append(slide_break())

    # ── SLIDE 18: RISK ANALYSIS ──────────────────────────────
    story.append(Paragraph("risk analysis &amp; plan B", s["SlideTitle"]))
    story.append(hr())
    story.append(Spacer(1, 4))

    risk_table = make_table(s,
        ["risk", "impact", "mitigation", "plan B"],
        [
            ["B2B fails to materialize", "high (32% of $1M)", "free workshops for case studies by month 6", "B2C-only ceiling: $600K-$700K"],
            ["ad costs exceed returns", "medium", "cap paid at 30% of acquisition; invest in organic", "Pinterest/Etsy/SEO are free traffic"],
            ["founder burnout", "high", "hire VA by month 10; systematize everything", 'create "train the trainer" program'],
            ["course/membership flops", "medium", "pre-sell course before building; founding-member rate", "multi-platform workbooks: $150K-$250K/yr"],
        ],
        col_widths=[2*inch, 1*inch, 2.8*inch, 2.8*inch]
    )
    story.append(risk_table)
    story.append(Spacer(1, 12))

    scenario_table = make_table(s,
        ["scenario", "year 1", "year 2", "year 3"],
        [
            ["conservative (B2C focus, slow B2B)", "$40K", "$120K", "$300K"],
            ["**moderate (balanced)**", "**$95K**", "**$395K**", "**$1M**"],
            ["aggressive (strong B2B)", "$120K", "$500K", "$1.2M+"],
            ["worst case (high ad costs, no B2B)", "$20K", "$60K", "$150K"],
        ],
        col_widths=[3.5*inch, 1.5*inch, 1.5*inch, 1.5*inch]
    )
    story.append(scenario_table)
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "even the worst case ($150K by year 3) is a real business with 70%+ margins. the floor is high.",
        s["SlideBodyBold"]
    ))
    story.append(slide_break())

    # ── SLIDE 19: DEFENSIBILITY ──────────────────────────────
    story.append(Paragraph("what makes this defensible", s["SlideTitle"]))
    story.append(hr())
    story.append(Spacer(1, 8))

    why_bullets = [
        ("<b>the need is accelerating.</b> 20.8M layoffs/year. 350K+ DOGE federal cuts. "
         "1.9M long-term unemployed. this is structural, not cyclical."),
        ("<b>nobody occupies the space between.</b> career coaches are tactical. therapists are clinical. "
         "nobody addresses the identity crisis \u2014 the \u201cwho am I now?\u201d question."),
        ("<b>the pain persists after reemployment.</b> research shows life satisfaction "
         "does not fully recover. the TAM includes people who found new jobs."),
        ("<b>the quiz builds a moat.</b> every response is zero-party data. "
         "we learn what displaced workers actually feel, in their own words."),
        ("<b>the value ladder compounds LTV.</b> a $12 workbook buyer who ascends to "
         "course ($197) + membership ($468/yr) = $677+ LTV. with 25% ascending, the model compounds."),
        ("<b>B2B creates defensibility.</b> once an outplacement firm licenses the content, "
         "switching costs are high. the grounding methodology becomes embedded."),
        ("<b>the brand voice is inimitable.</b> lowercase, quiet, permission-based. "
         "it can\u2019t be replicated by a corporate wellness vendor with a PowerPoint deck."),
    ]
    for b in why_bullets:
        story.append(Paragraph(f"\u2022  {b}", s["SlideBullet"]))
        story.append(Spacer(1, 4))
    story.append(slide_break())

    # ── SLIDE 20: CLOSING ────────────────────────────────────
    story.append(Spacer(1, 1.5 * inch))
    story.append(Paragraph("luminous pulse", s["CoverTitle"]))
    story.append(Spacer(1, 8))
    story.append(HRFlowable(width="40%", thickness=3, color=AMBER, spaceBefore=0, spaceAfter=16))
    story.append(Paragraph(
        '"where anxious humans come to rest."',
        s["QuoteText"]
    ))
    story.append(Spacer(1, 16))
    story.append(Paragraph(
        "year 1: $95K  \u00b7  year 2: $395K  \u00b7  year 3: $1.025M",
        s["SlideBodyBold"]
    ))
    story.append(Spacer(1, 24))
    story.append(Paragraph("Christie Parrow", s["SlideBody"]))
    story.append(Paragraph("@luminouspulse.co", s["SlideBody"]))
    story.append(Paragraph("luminouspulse.co", s["SlideBody"]))

    return story


def add_page_number(canvas, doc):
    """Add page number and brand footer."""
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(LAVENDER)
    canvas.drawRightString(PAGE_W - 0.5*inch, 0.35*inch,
                           f"luminous pulse  \u00b7  {doc.page}")
    canvas.restoreState()


def main():
    output_path = os.path.join(os.path.dirname(__file__),
                                "Luminous-Pulse-Pitch-Deck.pdf")

    doc = SimpleDocTemplate(
        output_path,
        pagesize=landscape(letter),
        leftMargin=0.75*inch,
        rightMargin=0.75*inch,
        topMargin=0.6*inch,
        bottomMargin=0.5*inch,
    )

    story = build_deck()
    doc.build(story, onFirstPage=add_page_number, onLaterPages=add_page_number)
    print(f"\n\u2713 pitch deck generated: {output_path}")
    print(f"  {doc.page} slides")


if __name__ == "__main__":
    main()
