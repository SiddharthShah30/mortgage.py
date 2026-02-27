"""
ui.py  –  CLI display primitives for the Mortgage Calculator
Design language (from mockups):
  [ STEP N: TITLE ]  ── section headers
  ? label  : [ value ]  ── bracketed input/echo
  > label  : [ value ]  ── sub-field input
  [!] msg             ── system alerts
  ●  SECTION TITLE    ── bullet subsections
  ┌─ label ─┐         ── stat boxes
  [P] [S] [R] [Q]     ── end-of-session action menu
"""

import os
import time
from datetime import date, timedelta

W = 76   # display width


# ── Indian Number Formatting ──────────────────────────────────────────────────

def _fmt_inr(value: float, prefix: str = "₹") -> str:
    """
    Format a number using the Indian numbering system.
    e.g. 1500000 → ₹15,00,000.00
    """
    negative = value < 0
    value    = abs(value)
    integer  = int(value)
    decimal  = round((value - integer) * 100)

    s = str(integer)
    if len(s) > 3:
        last3 = s[-3:]
        rest  = s[:-3]
        groups = []
        while len(rest) > 2:
            groups.append(rest[-2:])
            rest = rest[:-2]
        if rest:
            groups.append(rest)
        groups.reverse()
        s = ",".join(groups) + "," + last3
    formatted = f"{prefix}{'-' if negative else ''}{s}.{decimal:02d}"
    return formatted


def _fmt_inr_plain(value: float) -> str:
    """Indian number format without currency prefix, no decimals."""
    negative = value < 0
    value    = abs(int(value))
    s = str(value)
    if len(s) > 3:
        last3 = s[-3:]
        rest  = s[:-3]
        groups = []
        while len(rest) > 2:
            groups.append(rest[-2:])
            rest = rest[:-2]
        if rest:
            groups.append(rest)
        groups.reverse()
        s = ",".join(groups) + "," + last3
    return ("-" if negative else "") + s


# ── Primitives ────────────────────────────────────────────────────────────────

def _hr(char: str = "─", width: int = W) -> str:
    return char * width


def clear() -> None:
    os.system("cls" if os.name == "nt" else "clear")


def pause(msg: str = "PRESS ENTER TO CONTINUE") -> None:
    print(f"\n  [{msg}]")
    input()


# ── Banner & Section Headers ──────────────────────────────────────────────────

def banner() -> None:
    print()
    print("┌" + "─" * (W - 2) + "┐")
    print("│" + "  FinTech Project v0.4  ".center(W - 2) + "│")
    print("└" + "─" * (W - 2) + "┘")


def section(step: int | str, title: str) -> None:
    if isinstance(step, int):
        label = f"[{step}] {title.upper()}"
    else:
        label = f"[ {title.upper()} ]"
    print(f"\n{label}")
    print(_hr())


def bullet(title: str) -> None:
    """  ●  PAYMENT BREAKDOWN"""
    print(f"\n● {title}")
    print(_hr())


# ── Stat Boxes ────────────────────────────────────────────────────────────────

def stat_boxes(boxes: list[tuple[str, str]]) -> None:
    """
    Renders a row of up to 3 labelled boxes:
    ┌─ Total Principal ─┐  ┌─ Total Interest ─┐  ┌─ Debt-Free Date ─┐
    │   ₹15,00,000.00    │  │   ₹2,94,312.00    │  │   MAR 2031        │
    └───────────────────┘
    """
    n   = len(boxes)
    bw  = (W - (n - 1) * 2) // n   # box width including borders

    top_row = ""
    mid_row = ""
    bot_row = ""

    for label, value in boxes:
        inner   = bw - 2
        top_row += "┌─ " + label + " " + "─" * max(0, inner - len(label) - 3) + "┐  "
        mid_row += "│ " + value.center(inner) + " │  "
        bot_row += "└" + "─" * inner + "┘  "

    print()
    print(top_row.rstrip())
    print(mid_row.rstrip())
    print(bot_row.rstrip())


# ── DTI Progress Bar ──────────────────────────────────────────────────────────

def dti_bar(label: str, pct: float, bar_width: int = 36) -> None:
    """
    Current DTI: [##########--------------------------] 10.0%
    """
    filled = max(0, min(bar_width, int(pct / 100 * bar_width)))
    empty  = bar_width - filled
    bar    = "#" * filled + "-" * empty
    print(f"  {label:<14} : [{bar}] {pct:.1f}%")


# ── Bullet Subsection ─────────────────────────────────────────────────────────

def subsection(icon: str, title: str) -> None:
    print(f"\n  {icon}  {title}")


# ── Generic bordered table ────────────────────────────────────────────────────

def bordered_table(headers: list[str], rows: list[list[str]],
                   col_widths: list[int] | None = None) -> None:
    """
    Renders a table with ┌─┬─┐ borders matching the mockup style.
    """
    if col_widths is None:
        col_widths = [max(len(str(r[i])) for r in ([headers] + rows))
                      for i in range(len(headers))]
        col_widths = [max(w, 8) for w in col_widths]

    def _border(left, mid, right, fill="─"):
        segs = [fill * (w + 2) for w in col_widths]
        return left + mid.join(segs) + right

    def _row(cells):
        parts = [f" {str(c):<{w}} " for c, w in zip(cells, col_widths)]
        return "│" + "│".join(parts) + "│"

    print("  " + _border("┌", "┬", "┐"))
    print("  " + _row(headers))
    print("  " + _border("├", "┼", "┤"))
    for row in rows:
        print("  " + _row(row))
    print("  " + _border("└", "┴", "┘"))


# ── Amortization schedule table ───────────────────────────────────────────────

def amort_table(schedule: list[dict], limit: int | None = None) -> None:
    total  = len(schedule)
    limit  = min(limit or total, total)

    headers    = ["Month", "Payment", "Principal", "Interest", "Balance"]
    col_widths = [6, 16, 16, 16, 18]   # widened for Indian ₹ formatted values

    def _border(left, mid, right, fill="─"):
        segs = [fill * (w + 2) for w in col_widths]
        return left + mid.join(segs) + right

    def _row(cells):
        parts = [f" {str(c):<{w}} " for c, w in zip(cells, col_widths)]
        return "  │" + "│".join(parts) + "│"

    print("  " + _border("┌", "┬", "┐"))
    print("  │" + "│".join(f" {h:<{w}} " for h, w in zip(headers, col_widths)) + "│")
    print("  " + _border("├", "┼", "┤"))

    for row in schedule[:limit]:
        cells = [
            row["period"],
            _fmt_inr(row["payment"]),
            _fmt_inr(row["principal"]),
            _fmt_inr(row["interest"]),
            _fmt_inr(row["balance"]),
        ]
        print("  │" + "│".join(f" {str(c):<{w}} " for c, w in zip(cells, col_widths)) + "│")

    print("  " + _border("└", "┴", "┘"))
    if limit < total:
        print(f"  (Showing {limit} of {total} months)")


# ── Payment Breakdown Bar ─────────────────────────────────────────────────────

def payment_breakdown_bar(principal: float, interest: float,
                          bar_width: int = 36) -> None:
    """
    Principal: ████████████████████████████  83.6%
    Interest:  ██████                        16.4%
    """
    total = principal + interest
    if total == 0:
        return
    p_ratio = principal / total
    i_ratio = interest  / total
    p_fill = round(p_ratio * bar_width)
    i_fill = bar_width - p_fill          # guarantees both bars always sum to bar_width
    p_bar  = "█" * p_fill
    i_bar  = "█" * i_fill

    print(f"\n  Principal : {p_bar:<{bar_width}}  {p_ratio * 100:.1f}%")
    print(f"  Interest  : {i_bar:<{bar_width}}  {i_ratio * 100:.1f}%")


# ── Score meter ───────────────────────────────────────────────────────────────

def score_meter(score: int) -> None:
    bar_width = 40
    filled    = int((score - 300) / 600 * bar_width)
    filled    = max(0, min(filled, bar_width))
    empty     = bar_width - filled
    bar       = "█" * filled + "░" * empty

    rating = ("POOR"      if score < 550 else
              "FAIR"      if score < 650 else
              "GOOD"      if score < 750 else
              "EXCELLENT")

    print(f"\n  CREDIT SCORE  [{bar}]  {score} / 900")
    print(f"  Rating        : {rating}")
    print("  " + _hr("─", bar_width + 30))


# ── Card ledger ───────────────────────────────────────────────────────────────

def card_ledger(cards: list[dict]) -> None:
    subsection("💳", "CREDIT CARD LEDGER (Masked for Security)")
    print()
    headers    = ["#", "Issuer", "Card Number", "Limit (₹)", "Balance (₹)"]
    col_widths = [3, 20, 20, 14, 14]

    rows = []
    for i, c in enumerate(cards, 1):
        if c["valid"]:
            rows.append([
                i,
                c["issuer"],
                _spaced_mask(c["masked"]),
                _fmt_inr_plain(c["limit"]),
                _fmt_inr_plain(c["balance"]),
            ])
        else:
            rows.append([i, c["issuer"], _spaced_mask(c["masked"]), "INVALID", "—"])

    bordered_table(headers, [list(map(str, r)) for r in rows], col_widths)


def _spaced_mask(masked: str) -> str:
    stars  = masked.count("*")
    digits = "".join(d for d in masked if d.isdigit())
    grouped = " ".join("*" * 4 for _ in range(stars // 4))
    return (grouped + " " + digits).strip()


# ── Input helpers ─────────────────────────────────────────────────────────────

def ask(label: str, field_width: int = 20) -> str:
    raw = input(f"? {label:<24} : ").strip()
    print(f"\033[1A\033[2K? {label:<24} : [ {raw:<{field_width}} ]")
    return raw


def ask_choice(label: str, options: list[str], field_width: int = 22) -> str:
    opts_str = "  ".join(options)
    raw = input(f"? {label:<24} : ({opts_str}) -> ").strip()
    chosen_label = next(
        (o.split(". ", 1)[1] for o in options if o.startswith(raw + ".")), raw
    )
    print(f"\033[1A\033[2K? {label:<24} : [ {chosen_label:<{field_width}} ]")
    return raw


def ask_yn(label: str) -> bool:
    raw    = input(f"? {label:<24} (y/N) : ").strip().lower()
    result = raw == "y"
    disp   = "Yes" if result else "No"
    print(f"\033[1A\033[2K? {label:<24} : [ {disp:<20} ]")
    return result


def ask_int(label: str, min_val: int | None = None,
            max_val: int | None = None, field_width: int = 18) -> int:
    while True:
        try:
            raw   = input(f"> {label:<24} : ").strip()
            value = int(raw)
            if (min_val is not None and value < min_val) or \
               (max_val is not None and value > max_val):
                lo = min_val if min_val is not None else "-inf"
                hi = max_val if max_val is not None else "+inf"
                print(f"  [!] Enter a value between {lo} and {hi}.")
                continue
            print(f"\033[1A\033[2K> {label:<24} : [ {value:<{field_width}} ]")
            return value
        except ValueError:
            print("  [!] Enter a valid integer.")


def ask_float(label: str, min_val: float | None = None,
              prefix: str = "", field_width: int = 20) -> float:
    while True:
        try:
            raw   = input(f"> {label:<24} : ").strip().lstrip("₹").lstrip("$")
            value = float(raw)
            if min_val is not None and value < min_val:
                print(f"  [!] Value must be >= {min_val}.")
                continue
            disp = _fmt_inr(value) if not prefix else f"{prefix}{_fmt_inr_plain(int(value))}"
            print(f"\033[1A\033[2K> {label:<24} : [ {disp:<{field_width}} ]")
            return value
        except ValueError:
            print("  [!] Enter a valid number.")


def ask_percent(label: str, field_width: int = 18) -> float:
    while True:
        try:
            raw   = input(f"> {label:<24} : ").strip().rstrip("%")
            value = float(raw)
            if value < 0:
                print("  [!] Percentage cannot be negative.")
                continue
            print(f"\033[1A\033[2K> {label:<24} : [ {value:.2f}%{'':<{field_width - 7}} ]")
            return value
        except ValueError:
            print("  [!] Enter a valid number.")


# ── Result block ──────────────────────────────────────────────────────────────

def result_block(title: str, rows: list[tuple[str, str]]) -> None:
    print(f"\n  [!] SYSTEM CALCULATION — {title}")
    for label, value in rows:
        print(f"      > {label:<30} : {value}")


def alert(msg: str) -> None:
    print(f"\n  [!] {msg}")


def notice(icon: str, msg: str) -> None:
    print(f"  {icon}  {msg}")


# ── Processing bar ────────────────────────────────────────────────────────────

def processing_bar(msg: str, steps: int = 20, delay: float = 0.04) -> None:
    print(f"\n  [!] {msg}...")
    print("  [", end="", flush=True)
    for _ in range(steps):
        time.sleep(delay)
        print("█", end="", flush=True)
    print("] 100% Complete.")


# ── Prepayment impact block ───────────────────────────────────────────────────

def prepayment_impact(months_saved: int, interest_saved: float,
                      extra: float, lump: float, lump_month: int) -> None:
    desc = []
    if extra > 0:
        desc.append(f"{_fmt_inr(extra)} extra added monthly")
    if lump > 0:
        desc.append(f"{_fmt_inr(lump)} lump sum at month {lump_month}")
    tag = " + ".join(desc) if desc else "no prepayments"

    bullet(f"PREPAYMENT IMPACT (If {tag})")

    yrs     = months_saved // 12
    mns     = months_saved % 12
    time_str = (
        f"{yrs} Year{'s' if yrs != 1 else ''}, {mns} Month{'s' if mns != 1 else ''}"
        if yrs > 0 else
        f"{mns} Month{'s' if mns != 1 else ''}"
    )

    print(f"  ⏰ Time Saved     : {time_str}")
    print(f"  💰 Interest Saved : {_fmt_inr(interest_saved)}")
    if months_saved > 0:
        print(f"  ✅ New Status     : \"Accelerated Payoff\"")
    else:
        print(f"  ℹ️  No change — no prepayments applied.")


# ── Loan comparison table ─────────────────────────────────────────────────────

def loan_comparison_table(options: list[dict], recommended_idx: int = 0) -> None:
    """
    options: list of dicts with keys: rate, years, emi, interest, months
    """
    bullet("LOAN COMPARISON TABLE (New Loan Options)")

    n        = len(options)
    labels   = [
        f"Option {chr(65 + i)}" + (" (Rec)" if i == recommended_idx else "")
        for i in range(n)
    ]
    features = ["Interest Rate", "Tenure", "Monthly EMI", "Total Interest", "Time to Clear"]
    col_w    = [15] + [16] * n

    rows = [
        [f"{o['rate']:.2f}%"         for o in options],
        [f"{o['years']} Years"        for o in options],
        [_fmt_inr(o["emi"])           for o in options],
        [_fmt_inr(o["interest"])      for o in options],
        [f"{o['months']} Months"      for o in options],
    ]

    headers    = ["Feature"] + labels
    table_rows = [[features[i]] + rows[i] for i in range(len(features))]
    bordered_table(headers, table_rows, col_w)


# ── Debt clearance timeline ───────────────────────────────────────────────────

def debt_clearance_timeline(existing_months: int, new_months: int,
                            recommended_label: str = "Opt C") -> None:
    today         = date.today()
    existing_date = today + timedelta(days=existing_months * 30)
    new_date      = today + timedelta(days=new_months * 30)
    total_months  = max(existing_months, new_months)
    total_years   = round(total_months / 12)

    bullet("DEBT CLEARANCE TIMELINE (Combined Loans)")
    print(f"\n  Current Loans      : Will be cleared by {existing_date.strftime('%b %Y').upper()}")
    print(f"  New Loan ({recommended_label:<6})  : Will be cleared by {new_date.strftime('%b %Y').upper()}")
    print(f"  Total Debt Free    : {total_years} Year{'s' if total_years != 1 else ''} from today.")


# ── Debt-free date helper ─────────────────────────────────────────────────────

def debt_free_date(months: int) -> str:
    d = date.today() + timedelta(days=months * 30)
    return d.strftime("%b %Y").upper()


# ── End-of-session action menu ────────────────────────────────────────────────

def action_menu() -> str:
    """
    Displays:  [P] PDF Report  [S] Save to CSV  [R] Recalculate  [Q] Exit
    Returns the key pressed: 'p', 's', 'r', or 'q'
    """
    print("\n" + _hr())
    print("  [P] PDF Report    [S] Save to CSV    [R] Recalculate    [Q] Exit")
    print(_hr())
    while True:
        key = input("  Select : ").strip().lower()
        if key in ("p", "s", "r", "q"):
            return key
        print("  [!] Enter P, S, R, or Q.")


# ── Plain getters (for loops / internal use) ──────────────────────────────────

def get_int(prompt: str, min_val: int | None = None,
            max_val: int | None = None) -> int:
    while True:
        try:
            value = int(input(prompt))
            if (min_val is not None and value < min_val) or \
               (max_val is not None and value > max_val):
                print(f"  [!] Enter a value between {min_val} and {max_val}.")
            else:
                return value
        except ValueError:
            print("  [!] Enter a valid integer.")


def get_float(prompt: str, min_val: float | None = None) -> float:
    while True:
        try:
            value = float(input(prompt))
            if min_val is not None and value < min_val:
                print(f"  [!] Value must be >= {min_val}.")
            else:
                return value
        except ValueError:
            print("  [!] Enter a valid number.")