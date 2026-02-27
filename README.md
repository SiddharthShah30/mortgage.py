## Table of Contents

* [Features](#features)
* [Installation](#installation)
* [Usage](#usage)
* [Tech Stack](#tech-stack)
* [Project Structure](#project-structure)
* [Tests](#tests)
* [Contributing](#contributing)
* [License](#license)
* [Credits](#credits)

---

## Features

### Core Loan Analysis

* EMI calculation using standard amortization formulas
* Full month-by-month amortization schedule with principal, interest, and balance tracking
* Configurable table display — view any number of payments or the full schedule
* Yearly repayment summary for long-term insight
* Loan balance timeline visualization
* Principal vs interest payment breakdown chart

### Prepayment Simulation

* Extra monthly payment support
* Lump-sum prepayment at a chosen month
* Combined prepayment strategies (extra monthly + lump sum)
* Automatic tenure reduction when the loan closes early
* Prepayment impact summary showing:
  * Total interest saved
  * Time saved (months and years)
  * Revised debt-free date

### Credit Assessment

* Credit card profile input with Luhn validation and card masking
* Credit score calculation based on repayment history, utilisation, account age, and credit mix
* Alternative scoring path for applicants without a credit card — uses employment stability, savings rate, and bill payment history
* Risk tier assignment (TIER 1 / TIER 2 / TIER 3 / DENIED) with automatic rate mapping
* Debt-to-income (DTI) ratio analysis and visual bar display
* Score meter with classification on both Indian (300–900) and US (300–850) scales

### Multi-Mode Toolkit

* **Mode 1 – Single Loan Analysis:** Full borrower profile → credit check → loan config → results
* **Mode 2 – Multi-Loan Comparison:** Side-by-side comparison of 2–5 loans with DTI impact and debt clearance timeline
* **Mode 3 – Credit Assessment & Loan Application:** Standalone credit check with immediate loan offer output

### Export Options

* PDF report generation via ReportLab — includes stat boxes, amortization table, yearly summary, credit profile, and prepayment impact
* CSV export with loan summary header, full amortization schedule, and yearly summary

### Architecture

* Modular codebase with clear separation between calculation, display, and CLI control
* Dataclass-based `Mortgage` model
* Indian Rupee (₹) number formatting throughout

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/fin-tech-analytics-engine.git
cd fin-tech-analytics-engine
```

### 2. Ensure Python is installed

Python 3.10+ is required (uses `int | None` union type hints).

```bash
python --version
```

### 3. Install dependencies

The only external dependency is `reportlab` for PDF export.

```bash
pip install reportlab
```

### 4. Run the program

```bash
python main.py
```

---

## Usage

After launching, the main menu presents four modes:

```
1 → Single Loan Analysis
2 → Compare Multiple Loans
3 → Credit Assessment & Loan Application
4 → Exit
```

---

### Mode 1 — Single Loan Analysis

You will be prompted through four steps:

**Step 1 – Financial Profile**
```
Full Name
Employment Type  (Salaried / Self-Employed / Business)
Monthly Gross Income  (₹)
Existing Monthly EMI  (₹)
Credit Card Minimum Payment  (₹)
```

**Step 2 – Credit Assessment**

If you have a credit card, the tool collects card details (issuer, number, limit, balance, account age, late payments, defaults) and calculates a credit score. Without a card, an alternative proxy score is computed from job tenure, savings rate, and bill payment history.

**Step 3 – Loan Parameters**
```
Principal Amount  (₹)
Tenure  (years)
```

**Step 4 – Prepayment Options**
```
1. None
2. Extra Monthly Payment
3. Lump Sum at a chosen month
4. Both
```

**Results include:**
* Stat boxes: Total Principal, Total Interest, Debt-Free Date
* Payment breakdown bar
* Amortization table (configurable rows)
* Prepayment impact summary (if applicable)
* Current and projected DTI bars with approval status
* Credit score meter

**Post-results actions:**
```
[P] Export PDF    [S] Export CSV    [R] Recalculate    [Q] Quit
```

---

### Mode 2 — Multi-Loan Comparison

Enter details for 2–5 loans (principal, interest rate, tenure) and your current income and existing EMI. The engine outputs:

* Side-by-side table of EMI, total interest, total paid, and tenure for each option
* Recommended option (lowest interest cost)
* Current and projected DTI bars
* Debt clearance timeline

---

### Mode 3 — Credit Assessment & Loan Application

Runs the full credit check in isolation. Outputs credit score, assigned tier and rate, DTI analysis, and a loan offer summary for a requested amount and tenure.

---

## Tech Stack

* **Python 3.10+**
* **ReportLab** — PDF generation
* **Standard library only** for all other functionality (`csv`, `datetime`, `dataclasses`)

---

## Project Structure

```
.
├── main.py            # Entry point and CLI controller
├── mortgage.py        # Mortgage dataclass with EMI and rate helpers
├── amortization.py    # Amortization schedule generator (supports prepayments)
├── yearly_summary.py  # Yearly rollup from monthly schedule
├── comparison.py      # Multi-loan comparison engine
├── credit_tool.py     # Credit scoring, card validation, DTI analysis
├── ui.py              # All terminal display helpers (banners, tables, bars, input)
├── charts.py          # ASCII balance timeline and payment breakdown chart
├── table.py           # Amortization schedule table printer
├── export.py          # CSV export
└── pdf.py             # PDF report generation via ReportLab
```

---

## Tests

No automated tests are included yet. To verify the application manually:

```bash
python main.py
```

Recommended checks:

* EMI values match an independent mortgage calculator
* Prepayments reduce both tenure and total interest
* Lump sum is applied only at the specified month
* Yearly summary totals match the schedule totals
* Comparison mode correctly identifies the lowest-interest option
* DTI bars reflect the correct percentages
* CSV and PDF exports are generated and contain accurate data
* Luhn check rejects invalid card numbers
* Credit score changes predictably with different input profiles

---

## Contributing

Contributions are welcome.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes
4. Open a pull request

For major changes, open an issue first to discuss the proposal.

---

## License

MIT License

Copyright (c) 2026 SiddharthShah30

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

---

## Credits

* Built using Python standard libraries and ReportLab
* Financial formulas based on standard amortisation models
* Indian number formatting (₹ lakhs/crores system) implemented natively
* Developed by SiddharthShah30
