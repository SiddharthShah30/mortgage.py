def print_schedule(schedule, limit=None):
    if limit is None or limit > len(schedule):
        limit = len(schedule)
    
    print("\n=== AMORTIZATION SCHEDULE ===")
    print("-" * 78)
    print(
        f"{'Pmt#':<6} "
        f"{'Payment':>12} "
        f"{'Principal':>12}  "
        f"{'Interest':12} "
        f"{'Balance':>14} "
          )
    print("-" * 78)
    
    for row in schedule[:limit]:
        print(
            f"{row['period']:<6}"
            f"{row['payment']:>12.2f}"
            f"{row['principal']:>14.2f}"
            f"{row['interest']:>14.2f}"
            f"{row['balance']:>16.2f}"
        )
    
    print("-" * 78)

    if limit < len(schedule):
        print(f"Showing {limit} of {len(schedule)} months")