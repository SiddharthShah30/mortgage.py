from mortgage import Mortgage
from amortization import generate_schedule
from table import print_schedule
from charts import plot_balance, plot_payment_breakdown


def get_float(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Invalid input. Please enter a number.")


def choose_display_count(total):
    print("\nShow how many months of payments you want to see?")
    print("1 -> First 3")
    print("2 -> First 5")
    print("3 -> First 10")
    print("4 -> All")

    choice = input("Choice: ").strip()

    mapping = {
        "1": 3,
        "2": 5,
        "3": 10,
        "4": total
    }

    return mapping.get(choice, total)


def main():
    print("""\n
███╗   ███╗ ██████╗ ██████╗ ████████╗ ██████╗  █████╗  ██████╗ ███████╗
████╗ ████║██╔═══██╗██╔══██╗╚══██╔══╝██╔════╝ ██╔══██╗██╔════╝ ██╔════╝
██╔████╔██║██║   ██║██████╔╝   ██║   ██║  ███╗███████║██║  ███╗█████╗  
██║╚██╔╝██║██║   ██║██╔══██╗   ██║   ██║   ██║██╔══██║██║   ██║██╔══╝  
██║ ╚═╝ ██║╚██████╔╝██║  ██║   ██║   ╚██████╔╝██║  ██║╚██████╔╝███████╗
╚═╝     ╚═╝ ╚═════╝ ╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚══════╝

 ██████╗ █████╗ ██╗      ██████╗██╗   ██╗██╗      █████╗ ████████╗ ██████╗ ██████╗ 
██╔════╝██╔══██╗██║     ██╔════╝██║   ██║██║     ██╔══██╗╚══██╔══╝██╔═══██╗██╔══██╗
██║     ███████║██║     ██║     ██║   ██║██║     ███████║   ██║   ██║   ██║██████╔╝
██║     ██╔══██║██║     ██║     ██║   ██║██║     ██╔══██║   ██║   ██║   ██║██╔══██╗
╚██████╗██║  ██║███████╗╚██████╗╚██████╔╝███████╗██║  ██║   ██║   ╚██████╔╝██║  ██║
 ╚═════╝╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═════╝╚══════╝╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝ 
""")

    p = get_float("Loan Amount: ")
    r = get_float("Annual Interest Rate (%): ")
    y = int(get_float("Years: "))

    loan = Mortgage(p, r, y)

    emi = loan.emi()
    schedule = generate_schedule(loan)

    print(f"\nMonthly Payment: {emi:.2f}")
    print(f"Total Payments: {len(schedule)}")

    total_interest = sum(row["interest"] for row in schedule)
    print(f"Total Interest: {total_interest:.2f}")

    limit = choose_display_count(len(schedule))
    print_schedule(schedule, limit)

    plot_balance(schedule)
    plot_payment_breakdown(schedule)


if __name__ == "__main__":
    main()