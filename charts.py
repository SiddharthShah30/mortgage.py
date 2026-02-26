def plot_balance(schedule):

    print("\n=== LOAN BALANCE TIMELINE ===")

    step = max(1, len(schedule)//8)
    sampled = schedule[::step]

    max_balance = max(row['balance'] for row in sampled)
    bar_width = 40

    for row in sampled:
        ratio = row['balance'] / max_balance
        bars = int(ratio * bar_width)

        print(
            f"Month {row['period']:>3} | "
            + "█" * bars
        )

def plot_payment_breakdown(schedule):

    print("\n=== PAYMENT BREAKDOWN ===")

    total_principal = sum(r['principal'] for r in schedule)
    total_interest = sum(r['interest'] for r in schedule)
    total = total_principal + total_interest

    bar_width = 40

    p_ratio = total_principal / total
    i_ratio = total_interest  / total

    p_bar = int(p_ratio * bar_width)
    i_bar = int(i_ratio * bar_width)

    print(
        f"Principal "
        + "█" * p_bar
        + f" {p_ratio*100:.1f}%"
    )

    print(
        f"Interest "
        + "█" * i_bar
        + f" {i_ratio*100:.1f}%"
    )