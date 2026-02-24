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

* Monthly EMI calculation using the standard mortgage formula
* Full amortization schedule with principal, interest, and balance tracking
* Support for **extra monthly payments** to accelerate loan payoff
* Support for **lump-sum prepayments** at a chosen month
* Automatic schedule shortening when loan is paid off early
* Option to display only selected months of the schedule
* Terminal-based visualization of loan balance over time
* Payment breakdown chart showing principal vs interest proportions
* Modular architecture separating:

  * Mortgage model
  * Schedule generator
  * Table renderer
  * Chart visualizer
  * CLI controller
* Handles zero-interest loans correctly
* Clean CLI interaction with input validation

---

## Installation

Follow these steps to run the project locally.

### 1. Clone the repository

```bash
git clone https://github.com/your-username/mortgage-calculator-cli.git
cd mortgage-calculator-cli
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

After launching the program:

### 1. Enter loan details

```
Loan Amount:
Annual Interest Rate (%):
Years:
```

### 2. (If enabled in your version) provide repayment strategy

```
Extra monthly payment:
Lump-sum payment amount:
Lump-sum payment month:
```

These values allow simulation of early repayment scenarios.

### 3. Program output

The application will display:

* Monthly payment amount
* Total number of payments
* Total interest paid
* Amortization schedule
* Loan balance timeline chart
* Payment breakdown chart

### 4. Example flow

```
Loan Amount: 500000
Annual Interest Rate (%): 7.5
Years: 20
Extra monthly payment: 2000
Lump-sum payment: 50000
Lump-sum month: 24
```

The program recalculates the schedule and shows how the loan closes earlier.

---

## Tech Stack

Technologies used in this project:

* Python 3
* Standard library only
* Dataclasses for financial modeling
* Modular design:

  * Mortgage model module
  * Amortization generator module
  * Table formatting module
  * Chart rendering module
  * CLI controller module

---

## Tests

No automated tests are included yet.

You can manually test by running:

```bash
python main.py
```

Then verify:

* EMI calculation matches expected values
* Extra monthly payments reduce balance faster
* Lump-sum payments shorten the loan term
* Schedule stops when balance reaches zero
* Interest totals adjust correctly
* Charts render proportionally

---

## Contributing

Contributions are welcome.

If you'd like to improve this project:

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Open a pull request

For major feature changes, please open an issue first to discuss the proposal.

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
