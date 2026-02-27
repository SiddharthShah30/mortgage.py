"""
main.py  –  FIN-TECH ANALYTICS ENGINE v2.0
Entry point.  All input → clear → results → action menu.
"""
from datetime import date, timedelta

from mortgage import Mortgage
from amortization import generate_schedule
from yearly_summary import generate_yearly_summary
from credit_tool import get_final_credit_score, run_loan_application
from ui import (
    banner, section, bullet, subsection, clear, pause, alert, notice,
    processing_bar, action_menu,
    stat_boxes, dti_bar, payment_breakdown_bar, amort_table,
    score_meter, prepayment_impact, debt_free_date,
    ask, ask_int, ask_float, ask_percent, ask_choice, ask_yn,
    get_int, get_float,
)


# ── Helpers ───────────────────────────────────────────────────────────────────

def inr(amount: float) -> str:
    """Format a number in Indian comma system with ₹ sign.
    E.g. 1234567.89 → ₹12,34,567.89
    """
    s = f"{amount:.2f}"
    integer_part, decimal_part = s.split(".")
    # Indian grouping: last 3 digits, then groups of 2
    n = integer_part.lstrip("-")
    sign = "-" if integer_part.startswith("-") else ""
    if len(n) <= 3:
        return f"₹{sign}{n}.{decimal_part}"
    last3 = n[-3:]
    rest = n[:-3]
    groups = []
    while rest:
        groups.append(rest[-2:])
        rest = rest[:-2]
    groups.reverse()
    formatted = ",".join(groups) + "," + last3
    return f"₹{sign}{formatted}.{decimal_part}"


def _debt_free(months: int) -> str:
    return debt_free_date(months)


def _dti_label(dti_pct: float) -> str:
    if   dti_pct < 10:  return "Excellent"
    elif dti_pct < 20:  return "Healthy"
    elif dti_pct < 36:  return "Moderate"
    elif dti_pct < 50:  return "Risky"
    else:               return "Dangerous"


# ── Action menu handler ───────────────────────────────────────────────────────

def _handle_actions(loan: Mortgage, schedule: list[dict],
                    yearly: list[dict], prep: dict,
                    credit: dict | None, borrower: dict | None) -> bool:
    """
    Shows the [P][S][R][Q] menu.
    Returns True if the caller should re-run (Recalculate), False otherwise.
    """
    while True:
        key = action_menu()

        if key == "p":
            _do_pdf(loan, schedule, yearly, prep, credit, borrower)

        elif key == "s":
            _do_csv(loan, schedule, yearly)

        elif key == "r":
            return True   # signal: recalculate

        elif key == "q":
            print("\n  Goodbye!\n")
            return False


def _do_pdf(loan, schedule, yearly, prep, credit, borrower):
    from pdf import export_pdf
    path = f"loan_report_{date.today().isoformat()}.pdf"
    processing_bar("Generating PDF Report")
    export_pdf(path, {
        "loan": {
            "principal":      loan.principal,
            "rate":           loan.annual_rate,
            "years":          loan.years,
            "emi":            loan.emi(),
            "total_interest": sum(r["interest"] for r in schedule),
            "months":         len(schedule),
        },
        "schedule": schedule,
        "yearly":   yearly,
        "prepayment": prep,
        "credit":   credit   or {},
        "borrower": borrower or {},
    })
    print(f"  ✅  PDF saved → {path}")


def _do_csv(loan, schedule, yearly):
    from export import export_csv
    path = f"loan_report_{date.today().isoformat()}.csv"
    processing_bar("Exporting CSV")
    export_csv(path, schedule, yearly, {
        "principal":      loan.principal,
        "rate":           loan.annual_rate,
        "years":          loan.years,
        "emi":            loan.emi(),
        "total_interest": sum(r["interest"] for r in schedule),
    })
    print(f"  ✅  CSV saved → {path}")


# ── Single Loan Flow ──────────────────────────────────────────────────────────

def run_single_loan() -> None:
    while True:   # outer loop for Recalculate

        # ── STEP 1: FINANCIAL PROFILE ─────────────────────────────────────
        section(1, "Financial Profile")

        name       = ask("Full Name")
        emp_key    = ask_choice("Employment Type",
                                ["1. Salaried", "2. Self-Employed", "3. Business"])
        emp_map    = {"1": "Salaried", "2": "Self-Employed", "3": "Business"}
        employment = emp_map.get(emp_key, "Other")
        income     = ask_float("Monthly Gross Income", min_val=0.01, prefix="₹")
        exist_emi  = ask_float("Existing Monthly EMI",  min_val=0.0, prefix="₹")
        cc_min_pay = ask_float("Credit Card Min Pay",   min_val=0.0, prefix="₹")

        # ── STEP 2: CREDIT ASSESSMENT ─────────────────────────────────────
        section(2, "Credit Assessment")

        has_card = ask_yn("Do you have an active Credit Card")
        credit_info: dict = {}

        if has_card:
            score = get_final_credit_score()
        else:
            alert("Alternative Credit Check Initiated...")
            years_job   = ask_float("Years at current job", min_val=0.0)
            savings_pct = ask_percent("Monthly Savings %")
            any_late    = ask_yn("Any late bills (12m)")

            emp_score = (1.0 if years_job >= 3 else 0.8 if years_job >= 2
                         else 0.5 if years_job > 1 else 0.2)
            sav_ratio = savings_pct / 100
            sav_score = (1.0 if sav_ratio >= 0.30 else 0.8 if sav_ratio >= 0.20
                         else 0.5 if sav_ratio >= 0.10 else 0.2)
            late_pen  = 0.5 if any_late else 1.0
            weighted  = emp_score * 0.40 + sav_score * 0.30 + late_pen * 0.30
            score     = round(300 + weighted * 600)

            rating = ("Excellent" if score >= 750 else "Good" if score >= 650
                      else "Fair" if score >= 550 else "Poor")
            notice("📊", f"Proxy Credit Score: {score} ({rating})")

            if   score >= 750: sug_rate = 6.5
            elif score >= 650: sug_rate = 7.2
            elif score >= 550: sug_rate = 9.5
            else:              sug_rate = None

            if sug_rate:
                notice("📈", f"Suggested Interest Rate: {sug_rate}%")

        # Determine tier & rate
        if   score >= 750: tier, base_rate = "TIER 1 (PRIME)",     6.5
        elif score >= 650: tier, base_rate = "TIER 2 (STANDARD)",  7.5
        elif score >= 550: tier, base_rate = "TIER 3 (HIGH RISK)", 9.5
        else:              tier, base_rate = "DENIED",             None

        credit_info = {"score": score, "tier": tier, "rate": base_rate}

        if base_rate is None:
            alert("Loan application DENIED based on credit score.")
            return

        # ── STEP 3: LOAN PARAMETERS ──────────────────────────────────────
        section(3, "Loan Parameters")

        principal = ask_float("Principal Amount", min_val=1.0, prefix="₹")
        years     = ask_int("Tenure (Years)", min_val=1)

        # ── STEP 4: PREPAYMENT (OPTIONAL) ────────────────────────────────
        section(4, "Prepayment Options")

        prep_key = ask_choice("Prepayment Strategy",
                              ["1. None", "2. Extra Monthly",
                               "3. Lump Sum", "4. Both"])
        extra = 0.0; lump = 0.0; lump_month = 0
        if prep_key in ("2", "4"):
            extra = ask_float("Extra Monthly Amount", min_val=0.0, prefix="₹")
        if prep_key in ("3", "4"):
            lump       = ask_float("Lump Sum Amount", min_val=0.0, prefix="₹")
            lump_month = ask_int("Lump Sum Month", min_val=1)

        # ── COMPUTE ───────────────────────────────────────────────────────
        processing_bar("Running Amortization Engine")

        loan         = Mortgage(principal, base_rate, years)
        normal_sched = generate_schedule(loan)
        schedule     = generate_schedule(loan, extra_payment=extra,
                                         lump_sum=lump, lump_sum_month=lump_month)
        yearly       = generate_yearly_summary(schedule)

        total_interest = sum(r["interest"] for r in schedule)
        total_paid     = principal + total_interest
        months_saved   = len(normal_sched) - len(schedule)
        interest_saved = (sum(r["interest"] for r in normal_sched) - total_interest)

        current_dti = (exist_emi + cc_min_pay) / income * 100 if income else 0
        new_emi_val = loan.emi() + extra
        new_dti     = (exist_emi + cc_min_pay + new_emi_val) / income * 100 if income else 0

        prep_data = {
            "extra": extra, "lump": lump, "lump_month": lump_month,
            "months_saved": months_saved, "interest_saved": interest_saved,
        }
        borrower_data = {
            "Name":           name,
            "Employment":     employment,
            "Monthly Income": inr(income),
            "Existing EMI":   inr(exist_emi),
        }

        pause("PRESS ENTER TO VIEW RESULTS")

        # ════════════════════════════════════════════════════════════════════
        # RESULTS SCREEN
        # ════════════════════════════════════════════════════════════════════
        clear()
        banner()

        # ── Stat boxes ────────────────────────────────────────────────────
        stat_boxes([
            ("Total Principal", inr(principal)),
            ("Total Interest",  inr(total_interest)),
            ("Debt-Free Date",  _debt_free(len(schedule))),
        ])

        # ── Payment Breakdown ─────────────────────────────────────────────
        bullet("PAYMENT BREAKDOWN")
        payment_breakdown_bar(principal, total_interest)

        # ── Amortization Summary ──────────────────────────────────────────
        while True:
            raw = input("\n? Show how many months in table (number or ALL): ").strip().lower()
            if raw == "all":
                limit = len(schedule); break
            if raw.isdigit() and int(raw) > 0:
                limit = min(int(raw), len(schedule)); break
            print("  [!] Enter a number or ALL.")
        print(f"\033[1A\033[2K? Months in table: [ {raw.upper():<6} ]")

        bullet(f"AMORTIZATION SUMMARY (First {limit} Months)")
        amort_table(schedule, limit)

        # ── Prepayment Impact ─────────────────────────────────────────────
        if extra > 0 or lump > 0:
            prepayment_impact(months_saved, interest_saved, extra, lump, lump_month)

        # ── Financial Health Check ────────────────────────────────────────
        bullet("FINANCIAL HEALTH CHECK")
        dti_bar("Current DTI", current_dti)
        dti_bar("New DTI",     new_dti)

        dti_ok = new_dti < 36
        dot    = "🟢" if dti_ok else "🔴"
        status = ("APPROVED (DTI below 36% threshold)"
                  if dti_ok else "CAUTION – DTI exceeds safe threshold")
        print(f"  Status: {dot} {status}")

        # ── System Calculation Summary ────────────────────────────────────
        bullet("SYSTEM CALCULATION")
        print(f"  > Current DTI:   {current_dti:.1f}% ({_dti_label(current_dti)})")
        print(f"  > Projected DTI: {new_dti:.1f}% ({_dti_label(new_dti)})")
        print(f"  > Interest Rate: {base_rate}% (based on credit score)")
        print(f"  > Monthly EMI:   {inr(loan.emi())}")

        # ── Credit Score Meter ────────────────────────────────────────────
        bullet("CREDIT PROFILE")
        score_meter(int(score))

        # ── Action Menu ───────────────────────────────────────────────────
        should_recalc = _handle_actions(loan, schedule, yearly,
                                        prep_data, credit_info, borrower_data)
        if not should_recalc:
            break


# ── Loan Comparison Flow ──────────────────────────────────────────────────────

def run_comparison() -> None:
    from comparison import compare_loans
    from ui import loan_comparison_table, debt_clearance_timeline

    while True:
        section("", "Loan Comparison")
        n = ask_int("Number of loans to compare", min_val=2, max_val=5)
        loans = []
        for i in range(1, n + 1):
            print(f"\n  Loan {i}")
            p = ask_float(f"Loan Amount {i}",     min_val=0.01, prefix="₹")
            r = ask_float(f"Interest Rate {i} %", min_val=0.0)
            y = ask_int(  f"Tenure {i} (years)",  min_val=1)
            loans.append((p, r, y))

        income    = ask_float("Monthly Income",    min_val=0.01, prefix="₹")
        exist_emi = ask_float("Existing Monthly EMI", min_val=0.0, prefix="₹")

        processing_bar("Comparing Loans")
        results = compare_loans(loans)

        rec_idx = min(range(len(results)), key=lambda i: results[i]["interest"])

        pause("PRESS ENTER TO VIEW RESULTS")
        clear()
        banner()

        # DTI bars
        bullet("FINANCIAL HEALTH CHECK")
        curr_dti = exist_emi / income * 100 if income else 0
        rec_emi  = results[rec_idx]["emi"]
        new_dti  = (exist_emi + rec_emi) / income * 100 if income else 0
        dti_bar("Current DTI", curr_dti)
        dti_bar("New DTI",     new_dti)
        dti_ok = new_dti < 36
        dot    = "🟢" if dti_ok else "🔴"
        print(f"  Status: {dot} {'APPROVED' if dti_ok else 'CAUTION'}"
              f" (DTI {'below' if dti_ok else 'above'} 36% threshold)")

        # Comparison table
        opts = [{"rate": r["rate"], "years": r["years"], "emi": r["emi"],
                 "interest": r["interest"], "months": r["months"]}
                for r in results]
        loan_comparison_table(opts, recommended_idx=rec_idx)

        # Debt clearance timeline
        debt_clearance_timeline(
            existing_months=round(exist_emi / (rec_emi / results[rec_idx]["months"]))
                             if rec_emi > 0 else 0,
            new_months=results[rec_idx]["months"],
            recommended_label=f"Opt {chr(65 + rec_idx)}",
        )

        print("\n" + "─" * 60)
        print("  [R] Recalculate   [Q] Exit")
        print("─" * 60)
        key = ""
        while key not in ("r", "q"):
            key = input("  Select: ").strip().lower()
        if key == "q":
            print("\n  Goodbye!\n")
            break


# ── Credit Only Flow ──────────────────────────────────────────────────────────

def run_credit_only() -> None:
    score = get_final_credit_score()
    run_loan_application(score)


# ── Main Menu ─────────────────────────────────────────────────────────────────

def main() -> None:
    clear()
    banner()

    while True:
        section("MENU", "Select Mode")
        print("  1 → Single Loan Analysis")
        print("  2 → Compare Multiple Loans")
        print("  3 → Credit Assessment & Loan Application")
        print("  4 → Exit")

        mode = input("\n? Choose mode (1-4): ").strip()
        print(f"\033[1A\033[2K? Choose mode (1-4): [ {mode:<4} ]")

        if mode == "1":
            run_single_loan()
        elif mode == "2":
            run_comparison()
        elif mode == "3":
            run_credit_only()
        elif mode == "4":
            print("\n  Goodbye!\n")
            break
        else:
            alert("Invalid choice. Enter 1, 2, 3, or 4.")


if __name__ == "__main__":
    main()