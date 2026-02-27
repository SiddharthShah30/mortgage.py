def generate_yearly_summary(
    schedule: list[dict],
    payments_per_year: int = 12,
) -> list[dict]:
    summary = []

    for year_start in range(0, len(schedule), payments_per_year):
        year_slice = schedule[year_start : year_start + payments_per_year]
        year_num   = year_start // payments_per_year + 1

        summary.append({
            "year":      year_num,
            "interest":  round(sum(p["interest"]  for p in year_slice), 2),
            "principal": round(sum(p["principal"] for p in year_slice), 2),
            "balance":   year_slice[-1]["balance"],
        })

    return summary


def print_yearly_summary(summary: list[dict]) -> None:
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

    total_interest  = sum(r["interest"]  for r in summary)
    total_principal = sum(r["principal"] for r in summary)
    print(
        f"{'TOTAL':<6}"
        f"{total_interest:>18.2f}"
        f"{total_principal:>18.2f}"
    )
    print("-" * 70)