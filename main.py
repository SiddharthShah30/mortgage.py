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
    print("Or type any number (e.g., 12)")

    choice = input("Choice: ").strip()

    if choice .isdigit():
        n = int(choice)
        return min(n, total)

    mapping = {
        "1": 3,
        "2": 5,
        "3": 10,
        "4": total
    }

    return mapping.get(choice, total)

def get_prepayment_inputs():
    print("\nDo you want to add prepayments?")
    print("1 -> No")
    print("2 -> Extra Monthly Payment")
    print("3 -> Lump Sum Payment")
    print("4 -> Both")

    choice = input("Choice: ").strip()

    extra = 0
    lump = 0
    month = 0

    if choice in ("2","4"):
        extra = float(input("Extra Monthly Payment: "))
    
    if choice in ("3", "4"):
        lump = float(input("Lump Sum Aount: "))
        month = int(input("Month of Lump Sum: "))
    
    return extra, lump, month

def print_prepayment_summary(
        normal_schedule,
        new_schedule,
        extra,
        lump,
        lump_month
):
    normal_interest = sum(r["interest"] for r in normal_schedule)
    new_interest = sum(r["interest"] for r in new_schedule)

    normal_months = len(normal_schedule)
    new_months = len(new_schedule)

    months_saved = normal_months - new_months
    interest_saved = normal_interest - new_interest

    print("\n=== PREPAYMENT SUMMARY ===")
    if extra == 0 and lump == 0:
        print("No prepayments applied")
    
    print("-" * 60)

    print(f"Original tenure : {normal_months} months")
    print(f"New tenure      : {new_months} months")
    print(f"Time saved      : {months_saved} months")
    print(f"Interest saved  : {interest_saved:.2f}")

    if extra > 0:
        print(f"Extra Monthly   : {extra:.2f}")
    if lump > 0:
        print(f"Lump Sum        : {lump:.2f} at month {lump_month}")
    
    print("-" * 60)

def get_loan_for_comparison():
    loans = []

    n = int(get_float("\nHow many loans do you want to compare? "))

    for i in range(1, n+1):
        print(f"Enter details for the loan {i}")
        p = get_float("Loan Amount: ")
        r = get_float("Interest Rate (%): ")
        y = int(get_float("Years: "))

        loans.append((p,r,y))
    
    return loans
    

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
    
    print("\n1 -> Single Loan Analysis")
    print("2 -> Compare Multiple Loans")

    mode = input("Choose Mode: ").strip()

    if mode == "2":
        from comparison import compare_loan, print_comparison

        loans = get_loan_for_comparison()
        results = compare_loan(loans)
        print_comparison(results)
        return
    
    p = get_float("Loan Amount: ")
    r = get_float("Annual Interest Rate (%): ")
    y = int(get_float("Years: "))

    loan = Mortgage(p, r, y)

    emi = loan.emi()

    normal_schedule = generate_schedule(loan)

    extra, lump, month = get_prepayment_inputs()
    schedule = generate_schedule(loan,
                                 extra_payment=int(extra),
                                 lump_sum=int(lump),
                                 lump_sum_month=month)

    print(f"\nMonthly Payment: {emi:.2f}")
    print(f"Total Months: {len(schedule)}")

    total_interest = sum(row["interest"] for row in schedule)
    print(f"Total Interest: {total_interest:.2f}")

    limit = choose_display_count(len(schedule))
    print_schedule(schedule, limit)

    print_prepayment_summary(
        normal_schedule,
        schedule,
        extra,
        lump,
        month
    )

    plot_balance(schedule)
    plot_payment_breakdown(schedule)


if __name__ == "__main__":
    main()