"""
pdf_export.py  –  Generate a professional PDF report using reportlab.
"""
from datetime import date
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT

PAGE_W, PAGE_H = A4
MARGIN = 20 * mm

# ── Colour palette ────────────────────────────────────────────────────────────
C_DARK   = colors.HexColor("#1a1a2e")
C_ACCENT = colors.HexColor("#4a90d9")
C_LIGHT  = colors.HexColor("#f0f4f8")
C_GREEN  = colors.HexColor("#27ae60")
C_RED    = colors.HexColor("#e74c3c")
C_BORDER = colors.HexColor("#cccccc")
C_WHITE  = colors.white
C_BLACK  = colors.black


def _styles():
    base = getSampleStyleSheet()
    custom = {
        "title": ParagraphStyle("title", parent=base["Normal"],
                                fontSize=20, textColor=C_WHITE,
                                fontName="Helvetica-Bold", alignment=TA_CENTER,
                                spaceAfter=4),
        "subtitle": ParagraphStyle("subtitle", parent=base["Normal"],
                                   fontSize=10, textColor=C_LIGHT,
                                   fontName="Helvetica", alignment=TA_CENTER,
                                   spaceAfter=2),
        "section": ParagraphStyle("section", parent=base["Normal"],
                                  fontSize=12, textColor=C_DARK,
                                  fontName="Helvetica-Bold", spaceAfter=4,
                                  spaceBefore=12),
        "body": ParagraphStyle("body", parent=base["Normal"],
                               fontSize=9, textColor=C_DARK,
                               fontName="Helvetica", spaceAfter=2),
        "label": ParagraphStyle("label", parent=base["Normal"],
                                fontSize=8, textColor=colors.HexColor("#666666"),
                                fontName="Helvetica"),
        "value": ParagraphStyle("value", parent=base["Normal"],
                                fontSize=11, textColor=C_DARK,
                                fontName="Helvetica-Bold"),
        "green": ParagraphStyle("green", parent=base["Normal"],
                                fontSize=9, textColor=C_GREEN,
                                fontName="Helvetica-Bold"),
        "red": ParagraphStyle("red", parent=base["Normal"],
                              fontSize=9, textColor=C_RED,
                              fontName="Helvetica-Bold"),
    }
    return custom


def _stat_table(boxes: list[tuple[str, str, str]]) -> Table:
    """3-column stat box row. boxes = [(label, value, sub), ...]"""
    styles = _styles()
    data = [[
        [Paragraph(label, styles["label"]), Paragraph(val, styles["value"]),
         Paragraph(sub, styles["body"])]
        for label, val, sub in boxes
    ]]
    col_w = (PAGE_W - 2 * MARGIN) / len(boxes)
    t = Table(data, colWidths=[col_w] * len(boxes))
    t.setStyle(TableStyle([
        ("BOX",        (0, 0), (-1, -1), 0.8, C_BORDER),
        ("INNERGRID",  (0, 0), (-1, -1), 0.5, C_BORDER),
        ("BACKGROUND", (0, 0), (-1, -1), C_LIGHT),
        ("VALIGN",     (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING",    (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("LEFTPADDING",   (0, 0), (-1, -1), 10),
    ]))
    return t


def _data_table(headers: list[str], rows: list[list[str]],
                highlight_col: int | None = None) -> Table:
    styles = _styles()
    col_w  = (PAGE_W - 2 * MARGIN) / len(headers)

    head_row = [Paragraph(f"<b>{h}</b>", styles["body"]) for h in headers]
    data_rows = [
        [Paragraph(str(cell), styles["body"]) for cell in row]
        for row in rows
    ]

    t = Table([head_row] + data_rows, colWidths=[col_w] * len(headers),
              repeatRows=1)
    style_cmds = [
        ("BACKGROUND",    (0, 0), (-1, 0),  C_DARK),
        ("TEXTCOLOR",     (0, 0), (-1, 0),  C_WHITE),
        ("FONTNAME",      (0, 0), (-1, 0),  "Helvetica-Bold"),
        ("FONTSIZE",      (0, 0), (-1, -1), 8),
        ("ROWBACKGROUNDS",(0, 1), (-1, -1), [C_WHITE, C_LIGHT]),
        ("GRID",          (0, 0), (-1, -1), 0.4, C_BORDER),
        ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING",    (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING",   (0, 0), (-1, -1), 6),
    ]
    if highlight_col is not None:
        style_cmds.append(
            ("BACKGROUND", (highlight_col, 1), (highlight_col, -1),
             colors.HexColor("#e8f5e9"))
        )
    t.setStyle(TableStyle(style_cmds))
    return t


def _section_heading(title: str, story: list, styles: dict) -> None:
    story.append(Spacer(1, 6 * mm))
    story.append(Paragraph(f"● {title}", styles["section"]))
    story.append(HRFlowable(width="100%", thickness=0.5, color=C_BORDER))
    story.append(Spacer(1, 3 * mm))


# ── Main export function ──────────────────────────────────────────────────────

def export_pdf(filepath: str, data: dict) -> None:
    """
    data keys expected:
      loan        : dict  (principal, rate, years, emi, total_interest, months)
      schedule    : list[dict]
      yearly      : list[dict]
      prepayment  : dict  (extra, lump, lump_month, months_saved, interest_saved)
      credit      : dict  (score, tier, rate)  – optional
      borrower    : dict  (name, income, employment) – optional
    """
    doc     = SimpleDocTemplate(
        filepath, pagesize=A4,
        leftMargin=MARGIN, rightMargin=MARGIN,
        topMargin=MARGIN, bottomMargin=MARGIN,
    )
    styles  = _styles()
    story   = []
    today   = date.today()
    loan    = data["loan"]
    sched   = data["schedule"]
    yearly  = data.get("yearly", [])
    prep    = data.get("prepayment", {})
    credit  = data.get("credit", {})
    borrower = data.get("borrower", {})

    # ── Cover Header ─────────────────────────────────────────────────────────
    header_data = [[
        Paragraph("FIN-TECH ANALYTICS ENGINE v2.0", styles["title"]),
        Paragraph("Mortgage & Loan Analysis Report", styles["subtitle"]),
        Paragraph(f"Generated: {today.strftime('%d %B %Y')}", styles["subtitle"]),
    ]]
    header_t = Table(header_data, colWidths=[PAGE_W - 2 * MARGIN])
    header_t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), C_DARK),
        ("TOPPADDING",    (0, 0), (-1, -1), 12),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
        ("LEFTPADDING",   (0, 0), (-1, -1), 16),
    ]))
    story.append(header_t)
    story.append(Spacer(1, 6 * mm))

    # ── Borrower Info ────────────────────────────────────────────────────────
    if borrower:
        _section_heading("BORROWER PROFILE", story, styles)
        brows = [[k, str(v)] for k, v in borrower.items()]
        story.append(_data_table(["Field", "Detail"], brows))

    # ── Stat Boxes ───────────────────────────────────────────────────────────
    from ui import debt_free_date
    story.append(Spacer(1, 4 * mm))
    dfd = debt_free_date(loan["months"])
    story.append(_stat_table([
        ("Total Principal",  f"${loan['principal']:,.2f}", "Loan Amount"),
        ("Total Interest",   f"${loan['total_interest']:,.2f}", f"@ {loan['rate']}% p.a."),
        ("Debt-Free Date",   dfd, f"{loan['months']} Monthly Payments"),
    ]))

    # ── Credit Info ──────────────────────────────────────────────────────────
    if credit:
        _section_heading("CREDIT ASSESSMENT", story, styles)
        crows = [
            ["Credit Score",    str(credit.get("score", "N/A"))],
            ["Risk Tier",       credit.get("tier",  "N/A")],
            ["Interest Rate",   f"{credit.get('rate', loan['rate'])}%"],
        ]
        story.append(_data_table(["Metric", "Value"], crows))

    # ── Payment Breakdown ─────────────────────────────────────────────────────
    _section_heading("PAYMENT BREAKDOWN", story, styles)
    total = loan["principal"] + loan["total_interest"]
    p_pct = loan["principal"]      / total * 100
    i_pct = loan["total_interest"] / total * 100

    breakdown_data = [
        ["Component", "Amount", "Percentage"],
        ["Principal",  f"${loan['principal']:,.2f}",      f"{p_pct:.1f}%"],
        ["Interest",   f"${loan['total_interest']:,.2f}", f"{i_pct:.1f}%"],
        ["Total",      f"${total:,.2f}",                  "100.0%"],
    ]
    story.append(_data_table(breakdown_data[0], breakdown_data[1:]))

    # ── Amortization Schedule (first 24 rows) ─────────────────────────────────
    _section_heading(f"AMORTIZATION SCHEDULE (First {min(24, len(sched))} Months)", story, styles)
    amort_headers = ["Month", "Payment", "Principal", "Interest", "Balance"]
    amort_rows    = [
        [r["period"],
         f"${r['payment']:,.2f}",
         f"${r['principal']:,.2f}",
         f"${r['interest']:,.2f}",
         f"${r['balance']:,.2f}"]
        for r in sched[:24]
    ]
    story.append(_data_table(amort_headers, [list(map(str, r)) for r in amort_rows]))

    # ── Yearly Summary ────────────────────────────────────────────────────────
    if yearly:
        _section_heading("YEARLY SUMMARY", story, styles)
        y_headers = ["Year", "Interest Paid", "Principal Paid", "Ending Balance"]
        y_rows    = [
            [r["year"],
             f"${r['interest']:,.2f}",
             f"${r['principal']:,.2f}",
             f"${r['balance']:,.2f}"]
            for r in yearly
        ]
        story.append(_data_table(y_headers, [list(map(str, r)) for r in y_rows]))

    # ── Prepayment Impact ─────────────────────────────────────────────────────
    if prep and (prep.get("extra", 0) > 0 or prep.get("lump", 0) > 0):
        _section_heading("PREPAYMENT IMPACT", story, styles)
        yrs = prep["months_saved"] // 12
        mns = prep["months_saved"] % 12
        time_str = (f"{yrs}y {mns}m" if yrs > 0 else f"{mns} months")
        p_rows = [
            ["Original Tenure",  f"{loan['months']} months"],
            ["New Tenure",       f"{loan['months'] - prep['months_saved']} months"],
            ["Time Saved",       time_str],
            ["Interest Saved",   f"${prep['interest_saved']:,.2f}"],
        ]
        if prep.get("extra", 0):
            p_rows.append(["Extra Monthly", f"${prep['extra']:,.2f}"])
        if prep.get("lump", 0):
            p_rows.append(["Lump Sum", f"${prep['lump']:,.2f} at month {prep['lump_month']}"])
        story.append(_data_table(["Metric", "Value"], p_rows))

    # ── Footer ────────────────────────────────────────────────────────────────
    story.append(Spacer(1, 8 * mm))
    story.append(HRFlowable(width="100%", thickness=0.5, color=C_BORDER))
    story.append(Spacer(1, 2 * mm))
    story.append(Paragraph(
        "This report is generated for informational purposes only and does not "
        "constitute financial advice. All calculations use standard amortization formulas.",
        styles["label"]
    ))

    doc.build(story)