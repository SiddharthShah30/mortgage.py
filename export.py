"""
export.py  –  CSV export for amortization schedule and yearly summary.
"""
import csv
import os
from datetime import datetime


def export_csv(filepath: str, schedule: list[dict], yearly: list[dict],
               loan: dict) -> None:
    """
    Writes two sheets to one CSV:
      - Loan summary header
      - Full amortization schedule
      - Yearly summary
    """
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)

        # Summary header
        w.writerow(["FIN-TECH ANALYTICS ENGINE - Loan Report"])
        w.writerow(["Generated", datetime.now().strftime("%Y-%m-%d %H:%M")])
        w.writerow([])
        w.writerow(["LOAN SUMMARY"])
        w.writerow(["Principal",     f"{loan['principal']:.2f}"])
        w.writerow(["Annual Rate",   f"{loan['rate']}%"])
        w.writerow(["Tenure",        f"{loan['years']} years"])
        w.writerow(["Monthly EMI",   f"{loan['emi']:.2f}"])
        w.writerow(["Total Interest",f"{loan['total_interest']:.2f}"])
        w.writerow(["Total Payment", f"{loan['principal'] + loan['total_interest']:.2f}"])
        w.writerow([])

        # Amortization schedule
        w.writerow(["AMORTIZATION SCHEDULE"])
        w.writerow(["Month", "Payment", "Principal", "Interest", "Balance"])
        for row in schedule:
            w.writerow([
                row["period"],
                f"{row['payment']:.2f}",
                f"{row['principal']:.2f}",
                f"{row['interest']:.2f}",
                f"{row['balance']:.2f}",
            ])
        w.writerow([])

        # Yearly summary
        w.writerow(["YEARLY SUMMARY"])
        w.writerow(["Year", "Interest Paid", "Principal Paid", "Ending Balance"])
        for row in yearly:
            w.writerow([
                row["year"],
                f"{row['interest']:.2f}",
                f"{row['principal']:.2f}",
                f"{row['balance']:.2f}",
            ])