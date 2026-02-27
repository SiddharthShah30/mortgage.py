BAR_WIDTH = 40


def plot_balance(schedule: list[dict]) -> None:
    """Print a horizontal bar chart of the loan balance over time."""
    print("\n=== LOAN BALANCE TIMELINE ===")

    step    = max(1, len(schedule) // 8)
    sampled = schedule[::step]

    # Make sure the final row is always included
    if schedule[-1] not in sampled:
        sampled = sampled + [schedule[-1]]

    max_balance = max(row["balance"] for row in sampled) or 1  # avoid div-by-zero

    for row in sampled:
        ratio = row["balance"] / max_balance
        bars  = int(ratio * BAR_WIDTH)
        print(
            f"Month {row['period']:>4} | "
            f"{'█' * bars:<{BAR_WIDTH}} "
            f"  {row['balance']:>14,.2f}"
        )


def plot_payment_breakdown(schedule: list[dict]) -> None:
    """Print a horizontal bar showing the principal vs interest split."""
    print("\n=== PAYMENT BREAKDOWN ===")

    total_principal = sum(r["principal"] for r in schedule)
    total_interest  = sum(r["interest"]  for r in schedule)
    total           = total_principal + total_interest

    if total == 0:
        print("  No data to display.")
        return

    p_ratio = total_principal / total
    i_ratio = total_interest  / total

    p_bar = int(p_ratio * BAR_WIDTH)
    i_bar = int(i_ratio * BAR_WIDTH)

    print(f"Principal  {'█' * p_bar:<{BAR_WIDTH}}  {p_ratio * 100:>5.1f}%  ({total_principal:>14,.2f})")
    print(f"Interest   {'█' * i_bar:<{BAR_WIDTH}}  {i_ratio * 100:>5.1f}%  ({total_interest:>14,.2f})")
    print(f"\n  Total Paid : {total:>,.2f}")