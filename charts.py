def plot_balance(schedule, width=60, points=20):
    print("\n=== LOAN BALANCE TIMELINE ===")

    step = max(1, len(schedule)//points)
    sampled = schedule[::step]

    max_balance = max(row["balance"] for row in sampled)

    print("-" * 78)
    print(f"{'Period':>8} {'Balance':>14}   Chart")
    print("-" * 78)

    for row in sampled:
        ratio = row["balance"] / max_balance
        bars = int(ratio * width)

        left = f"P{row['period']:>6} {row['balance']:>14.2f}"

        print(f"{left:<26}   " + "█"*bars)

    print("-" * 78)
    print("Scale: bar length proportional to remaining loan balance")


def plot_payment_breakdown(schedule, width=50):
    print("\n=== PAYMENT BREAKDOWN ===")

    total_principal = sum(r['principal'] for r in schedule)
    total_interest = sum(r['interest'] for r in schedule)
    total = total_principal + total_interest

    p_ratio = total_principal / total
    i_ratio = total_interest / total

    p_bar = int(p_ratio * width)
    i_bar = int(i_ratio * width)

    print("-" * 70)
    print(f"{'Type':<12}{'Amount':>15}{'Percent':>10}  Chart")
    print("-" * 70)

    print(
        f"{'Principal':<12}"
        f"{total_principal:>15.2f}"
        f"{p_ratio*100:>9.1f}%  "
        + "█"*p_bar
    )

    print(
        f"{'Interest':<12}"
        f"{total_interest:>15.2f}"
        f"{i_ratio*100:>9.1f}%  "
        + "█"*i_bar
    )

    print("-" * 70)