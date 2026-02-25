from mortgage import Mortgage
from amortization import generate_schedule

def compare_loan(loan_data):
    results = []

    for i, data in enumerate(loan_data, start=1):
        principal, rate, years = data

        loan = Mortgage(principal, rate, years)
        schedule = generate_schedule(loan)

        emi = loan.emi()
        total_interest = sum(r["interest"] for r in schedule)
        total_paid = principal + total_interest
        months = len(schedule)

        results.append({
            "id": i,
            "principal": principal,
            "rate": rate,
            "years": years,
            "emi": emi,
            "interest": total_interest,
            "total": total_paid,
            "months":months
        })
    
    return results

def print_comparison(results):
    print("\n=== LOAN COMPARISON ===")
    print("-" * 90)

    print(
        f"{'Loan':<6} "
        f"{'Principal':>12} "
        f"{'Rate':>8} "
        f"{'Years':>8} "
        f"{'EMI':>12} "
        f"{'Interest':14} "
        f"{'Total Paid':>14} "
    )

    print("-" * 90)

    for r in results:
        print(
            f"{r['id']:<6}"
            f"{r['principal']:>12.2f}"
            f"{r['rate']:>8.2f}"
            f"{r['years']:>8}"
            f"{r['emi']:>12.2f}"
            f"{r['interest']:>14.2f}"
            f"{r['total']:>14.2f}"
        )
    print("-" * 90)

    best = min(results, key=lambda x: x["interest"] / x["principal"])
    print(f"\nBest option: Loan {best['id']} (lowest interest ratio)")