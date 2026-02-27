from datetime import date, timedelta
from ui import (
    section, subsection, alert, notice,
    ask, ask_yn, ask_int, ask_float, ask_choice, ask_percent,
    card_ledger, score_meter, processing_bar, pause,
    result_block, dti_bar,
    get_int, get_float,
    _fmt_inr, _fmt_inr_plain,
)


# ── Luhn & masking ────────────────────────────────────────────────────────────

def luhn_check(card_number: str) -> bool:
    digits   = [int(d) for d in card_number if d.isdigit()]
    checksum = 0
    for i, d in enumerate(reversed(digits)):
        if i % 2 == 1:
            d *= 2
            if d > 9:
                d -= 9
        checksum += d
    return checksum % 10 == 0


def mask_number(num: str) -> str:
    clean = "".join(d for d in num if d.isdigit())
    return ("*" * (len(clean) - 4) + clean[-4:]) if len(clean) >= 4 else "****"


# ── Credit Card Input ─────────────────────────────────────────────────────────

def get_credit_profile() -> list[dict]:
    from datetime import datetime
    current_year = datetime.now().year

    n     = ask_int("Number of cards", min_val=1)
    cards = []

    for i in range(1, n + 1):
        section("", f"Card {i} of {n}")

        issuer = ask("Card Issuer")
        number = ask("Card Number")
        valid  = luhn_check(number)

        if not valid:
            alert("Card number appears INVALID (Luhn check failed).")
            if ask_yn("Re-enter card number"):
                number = ask("Card Number (retry)")
                valid  = luhn_check(number)

        if not valid:
            alert("Card still invalid. Contact your bank or issuer.")
            cards.append({
                "issuer": issuer, "number": number,
                "masked": mask_number(number), "valid": False,
                "util": 0.0, "age": 0, "late": 0, "default": False,
            })
            continue

        limit   = ask_float("Credit Limit",       min_val=0.01, prefix="₹")
        balance = ask_float("Outstanding Balance", min_val=0.0,  prefix="₹")
        if balance > limit:
            alert("Balance exceeds limit — capping utilisation at 100%.")

        opened      = ask_int("Year Opened",   min_val=1950, max_val=current_year)
        late        = ask_int("Late Payments", min_val=0)
        has_default = ask_yn("Any default on card")

        cards.append({
            "issuer":   issuer,
            "number":   number,
            "masked":   mask_number(number),
            "valid":    True,
            "limit":    limit,
            "balance":  balance,
            "age":      current_year - opened,
            "late":     late,
            "default":  has_default,
            "util":     min(balance / limit * 100, 100.0),
        })

    return cards


# ── Credit Score Calculation ──────────────────────────────────────────────────

def combine_cards(cards: list[dict]) -> dict:
    total_limit   = sum(c["limit"]   for c in cards)
    total_balance = sum(c["balance"] for c in cards)
    total_late    = sum(c["late"]    for c in cards)
    return {
        "on_time":     max(0, 100 - total_late * 2),
        "utilization": (total_balance / total_limit * 100) if total_limit else 0.0,
        "history":     max(c["age"] for c in cards),
        "mix":         str(min(len(cards), 3)),
        "default":     any(c["default"] for c in cards),
    }


def calculate_credit_score(profile: dict) -> int:
    score     = 300.0
    repayment = (profile["on_time"] / 100) * (0.5 if profile["default"] else 1.0)
    score += repayment                                        * 0.35 * 600
    score += max(0.0, 1 - profile["utilization"] / 100)     * 0.30 * 600
    score += min(profile["history"] / 20, 1.0)              * 0.15 * 600
    score += {"1": 0.4, "2": 0.8, "3": 1.0}.get(
                 profile["mix"], 0.4)                        * 0.10 * 600
    score += 0.10 * 600
    return round(min(score, 900))


def classify_score(score: int) -> tuple[str, str]:
    india = ("EXCELLENT" if score >= 750 else "GOOD" if score >= 650
             else "FAIR" if score >= 550 else "POOR")
    us    = ("EXCEPTIONAL" if score >= 800 else "GOOD" if score >= 670
             else "FAIR" if score >= 580 else "POOR")
    return india, us


# ── Alternative Credit Scoring ────────────────────────────────────────────────

def run_alternative_credit(return_score: bool = False) -> int | None:
    alert("Alternative Credit Check Initiated...")

    years            = ask_float("Years at current job", min_val=0.0)
    employment_score = (1.0 if years >= 3 else 0.8 if years >= 2
                        else 0.5 if years > 1 else 0.2)

    savings_pct   = ask_percent("Monthly Savings %")
    ratio         = savings_pct / 100
    savings_score = (1.0 if ratio >= 0.30 else 0.8 if ratio >= 0.20
                     else 0.5 if ratio >= 0.10 else 0.2)

    any_late     = ask_yn("Any late bills (last 12m)")
    late_penalty = 0.5 if any_late else 1.0

    weighted    = employment_score * 0.40 + savings_score * 0.30 + late_penalty * 0.30
    proxy_score = round(300 + weighted * 600)
    rating      = ("Excellent" if proxy_score >= 750 else "Good" if proxy_score >= 650
                   else "Fair" if proxy_score >= 550 else "Poor")

    processing_bar("Computing Alternative Credit Score")
    notice("📊", f"Calculated Proxy Credit Score : {proxy_score} ({rating})")

    if   proxy_score >= 750: suggested_rate = 6.5
    elif proxy_score >= 650: suggested_rate = 7.2
    elif proxy_score >= 550: suggested_rate = 9.5
    else:                    suggested_rate = None

    if suggested_rate:
        notice("📈", f"Suggested Interest Rate : {suggested_rate:.2f}%")

    if return_score:
        return proxy_score
    return None


# ── Final Credit Score ────────────────────────────────────────────────────────

def get_final_credit_score() -> float:
    section(2, "Credit & Liability Audit")

    has_history = ask_yn("Do you have an existing Credit Card")

    if has_history:
        cards = get_credit_profile()
        card_ledger(cards)

        subsection("📨", "EXISTING LOAN OBLIGATIONS")
        total_emi, remaining_months = _collect_existing_loans_inline()

        valid_cards = [c for c in cards if c["valid"]]
        if not valid_cards:
            alert("No valid cards found. Switching to Alternative Scoring…")
            alt = run_alternative_credit(return_score=True)
            return float(alt) if alt is not None else 0.0

        processing_bar("Calculating Credit Score")
        score = calculate_credit_score(combine_cards(valid_cards))
        score_meter(score)
        return float(score)

    alt = run_alternative_credit(return_score=True)
    return float(alt) if alt is not None else 0.0


def _collect_existing_loans_inline() -> tuple[float, int]:
    has_loans = ask_yn("Any active loans")
    if not has_loans:
        return 0.0, 0

    n          = ask_int("Number of active loans", min_val=1)
    total_emi  = 0.0
    max_months = 0

    for i in range(1, n + 1):
        print(f"\n  Loan {i}")
        emi    = ask_float(f"Monthly EMI (Loan {i})",      min_val=0.0, prefix="₹")
        months = ask_int(  f"Remaining Months (Loan {i})", min_val=0)
        total_emi  += emi
        max_months  = max(max_months, months)

    # FIX: use Indian number formatting for the summary echo
    print(f"\n  Monthly EMI Total : [ {_fmt_inr(total_emi):<16} ]")
    print(f"  Remaining Months  : [ {max_months:<16} ]")
    return total_emi, max_months


# ── Debt burden ───────────────────────────────────────────────────────────────

def analyze_debt_burden(total_emi: float, remaining_months: int,
                        income: float) -> None:
    if total_emi == 0:
        alert("No active loans detected.")
        return

    dti    = total_emi / income * 100
    status = ("Healthy"    if dti < 20 else
              "Moderate"   if dti < 36 else
              "Risky"      if dti < 50 else
              "Dangerous")
    completion = date.today() + timedelta(days=remaining_months * 30)

    # FIX: render the DTI as a visual bar (was printing plain text, bar never showed)
    dti_bar("Current DTI", dti)
    print(f"  Status             : {status}")
    print(f"  Loans clear by     : {completion.strftime('%b %Y').upper()}")

    if dti >= 36:
        alert("Recommendation: Consider applying after current loans are cleared.")
    else:
        notice("✅", "Debt ratio is manageable. You may proceed.")


# ── Tier & rate ───────────────────────────────────────────────────────────────

def determine_tier(score: float) -> tuple[str, float | None]:
    if   score >= 750: return "TIER 1 (PRIME)",     6.5
    elif score >= 650: return "TIER 2 (STANDARD)",  7.5
    elif score >= 550: return "TIER 3 (HIGH RISK)", 9.5
    else:              return "DENIED",              None


# ── Loan application (used by credit-only mode) ───────────────────────────────

def run_loan_application(score: float) -> None:
    section(3, "Loan Configuration")

    tier, rate = determine_tier(score)

    print(f"\n  [!] SYSTEM CALCULATION...")
    print(f"      > Calculated Credit Score : {int(score)}")
    print(f"      > Assigned Risk Tier      : {tier}")
    if rate:
        print(f"      > Base Interest Rate      : {rate:.2f}%")
    else:
        print(f"      > Status                  : DENIED")

    if rate is None:
        alert("Loan application DENIED based on credit score.")
        return

    income = ask_float("Monthly Income", min_val=0.01, prefix="₹")
    total_emi, remaining_months = _collect_existing_loans_inline()
    analyze_debt_burden(total_emi, remaining_months, income)

    purpose_key = ask_choice(
        "Select Loan Purpose",
        ["1. Real Estate", "2. Business Expansion", "3. Education"],
    )
    purpose_map = {"1": "Real Estate", "2": "Business Expansion", "3": "Education"}
    purpose     = purpose_map.get(purpose_key, "General")

    principal = ask_float("Enter Requested Amount", min_val=1.0, prefix="₹")
    years     = ask_int(  "Enter Desired Tenure",   min_val=1)

    processing_bar("Processing Amortization Engine")
    pause("PRESS ENTER TO VIEW RESULTS")

    # FIX: handle zero interest rate edge case to avoid ZeroDivisionError
    months        = years * 12
    monthly_rate  = rate / 100 / 12
    if monthly_rate == 0:
        emi = principal / months
    else:
        emi = (principal * monthly_rate * (1 + monthly_rate) ** months
               / ((1 + monthly_rate) ** months - 1))

    total_payment  = emi * months
    total_interest = total_payment - principal

    section("", "Loan Offer Summary")
    # FIX: all currency values now use Indian ₹ formatting
    print(f"\n  > Purpose          : {purpose}")
    print(f"  > Principal        : {_fmt_inr(principal)}")
    print(f"  > Interest Rate    : {rate:.2f}%")
    print(f"  > Tenure           : {years} Year{'s' if years != 1 else ''}  /  {months} Months")
    print(f"  > Monthly EMI      : {_fmt_inr(emi)}")
    print(f"  > Total Interest   : {_fmt_inr(total_interest)}")
    print(f"  > Total Payment    : {_fmt_inr(total_payment)}")