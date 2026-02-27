from mortgage import Mortgage
from amortization import generate_schedule


def compare_loans(loan_data: list[tuple]) -> list[dict]:
    """
    Build a comparison result list from a list of (principal, rate, years) tuples.
    """
    results = []

    for i, (principal, rate, years) in enumerate(loan_data, start=1):
        loan     = Mortgage(principal, rate, years)
        schedule = generate_schedule(loan)

        total_interest = round(sum(r["interest"] for r in schedule), 2)

        results.append({
            "id":        i,
            "principal": principal,
            "rate":      rate,
            "years":     years,
            "emi":       round(loan.emi(), 2),
            "interest":  total_interest,
            "total":     round(principal + total_interest, 2),
            "months":    len(schedule),
        })

    return results


def print_comparison(results: list[dict]) -> None:
    print("\n=== LOAN COMPARISON ===")
    print("-" * 90)
    print(
        f"{'Loan':<6} "
        f"{'Principal':>12} "
        f"{'Rate %':>8} "
        f"{'Years':>6} "
        f"{'EMI':>12} "
        f"{'Interest':>14} "
        f"{'Total Paid':>14} "
        f"{'Months':>8}"
    )
    print("-" * 90)

    for r in results:
        print(
            f"{r['id']:<6}"
            f"{r['principal']:>12,.2f}"
            f"{r['rate']:>8.2f}"
            f"{r['years']:>6}"
            f"{r['emi']:>12,.2f}"
            f"{r['interest']:>14,.2f}"
            f"{r['total']:>14,.2f}"
            f"{r['months']:>8}"
        )

    print("-" * 90)

    best = min(results, key=lambda x: x["interest"] / x["principal"])
    print(f"\n  Best option: Loan {best['id']} (lowest interest-to-principal ratio)")