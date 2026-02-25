## Table of Contents

* [Features](#features)
* [Installation](#installation)
* [Usage](#usage)
* [Tech Stack](#tech-stack)
* [Tests](#tests)
* [Contributing](#contributing)
* [License](#license)
* [Credits](#credits)

---

## Features

Key functionalities of the project:

### Core Loan Analysis

* EMI calculation using standard mortgage formulas
* Full amortization schedule with principal, interest, and balance tracking
* Option to display any number of payments or all
* Yearly repayment summary for long-term insight
* Loan balance timeline visualization
* Payment breakdown chart

### Prepayment Simulation

* Extra monthly payment support
* Lump-sum prepayment at a chosen month
* Combined prepayment strategies
* Automatic tenure reduction when loan closes early
* Prepayment impact summary including:

  * Interest saved
  * Time saved
  * New tenure

### Multi-Mode Financial Toolkit

* Single loan deep analysis mode
* Compare multiple loans side-by-side
* Credit card / score checker tool integration
* Clean CLI navigation menu

### Architecture & Design

* Modular codebase with separate financial components
* Dataclass-based mortgage model
* Clear separation between:

  * Calculation logic
  * Display logic
  * Visualization
  * CLI controller

---

## Installation

Follow these steps to run the project locally.

### 1. Clone the repository

```bash
git clone https://github.com/your-username/loan-analysis-cli.git
cd loan-analysis-cli
```

### 2. Ensure Python is installed

Python 3.8+ is recommended.

```bash
python --version
```

### 3. Run the program

```bash
python main.py
```

No external libraries are required.

---

## Usage

After launching the program, choose a mode:

```
1 -> Single Loan Analysis
2 -> Compare Multiple Loans
3 -> Credit Card and Score Checker
```

---

### Single Loan Analysis

Enter:

```
Loan Amount
Annual Interest Rate (%)
Years
```

Then optionally choose prepayment strategy:

```
1 -> No prepayments
2 -> Extra monthly payment
3 -> Lump sum payment
4 -> Both
```

The program outputs:

* Monthly payment
* Total months to repay
* Total interest
* Amortization schedule
* Yearly repayment summary
* Prepayment savings report
* Balance timeline chart
* Payment breakdown chart

---

### Loan Comparison Mode

Enter details for multiple loans.

The program compares:

* EMI values
* Tenure
* Total interest
* Overall repayment cost

---

### Credit Tool Mode

Launches the integrated credit utility module for credit-related checks.

---

## Tech Stack

Technologies used in this project:

* Python 3
* Standard library only
* Dataclasses for financial modeling
* Modular architecture including:

  * Mortgage model module
  * Amortization engine
  * Schedule table renderer
  * Chart visualization module
  * Yearly summary generator
  * Loan comparison module
  * Credit analysis module
  * CLI controller

---

## Tests

No automated tests are included yet.

You can manually test by running:

```bash
python main.py
```

Then verify:

* EMI values are correct
* Prepayments reduce tenure and interest
* Lump-sum logic applies at the correct month
* Yearly summary totals match schedule values
* Comparison mode prints correct results
* Charts render proportionally
* CLI navigation flows correctly

---

## Contributing

Contributions are welcome.

If you'd like to improve this project:

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Open a pull request

For major changes, please open an issue first to discuss the proposal.

---

## License

MIT License

Copyright (c) 2026 SiddharthShah30

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

---

## Credits

* Built using Python standard libraries
* Financial formulas based on standard amortization models
* Developed by SiddharthShah30
