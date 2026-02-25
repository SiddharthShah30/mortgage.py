def generate_yearly_summary(schedule, payments_per_year=12):
    summary=[]

    for year_start in range(0, len(schedule), payments_per_year):
        year_slice = schedule[year_start:year_start+payments_per_year]

        year_num = year_start // payments_per_year + 1

        interest = sum(p["interest"] for p in year_slice)
        principal = sum(p["principal"] for p in year_slice)
        ending_balance = year_slice[-1]["balance"]

        summary.append({
            "year": year_num,
            "interest": interest,
            "principal": principal,
            "balance": ending_balance
        })
    
    return summary

def print_yearly_summary(summary):
    print("\n=== YEARLY SUMMARY ===")
    print("-" * 70)

    print(
        f"{'Year':<6}"
        f"{'Interest Paid':>18}"
        f"{'Principal Paid':>18}"
        f"{'Ending Balance':>18}"
    )

    print("-" * 70)

    for row in summary:
        print(
            f"{row['year']:<6}"
            f"{row['interest']:>18.2f}"
            f"{row['principal']:>18.2f}"
            f"{row['balance']:>18.2f}"
        )
    print("-" * 70)