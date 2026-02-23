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

* Monthly EMI calculation using standard mortgage formula 
* Full amortization schedule with principal, interest, and balance tracking 
* Option to display only selected months of the schedule
* Text-based visualization of loan balance over time
* Payment breakdown chart showing principal vs interest proportions
* Modular architecture with separated components:

  * Mortgage model
  * Schedule generator
  * Table renderer
  * Chart visualizer
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

### 2. Program output

The application will display:

* Monthly payment amount
* Total number of payments
* Total interest paid
* Amortization schedule (first few or all months)
* Loan balance timeline chart
* Payment breakdown chart

### 3. Example flow

```
Loan Amount: 500000
Annual Interest Rate (%): 7.5
Years: 20
```

The program calculates EMI, prints the schedule, and shows visual charts in the terminal.

---

## Tech Stack

Technologies used in this project:

* Python 3
* Standard library only
* Dataclasses for financial model structure 
* Modular design:

  * Schedule generator module 
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

* EMI matches expected financial calculations
* Schedule balance decreases to zero
* Interest totals are correct
* Display limit works correctly
* Charts render proportionally
* Zero-interest loans divide evenly

---

## Contributing

Contributions are welcome.

If you'd like to improve this project:

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Open a pull request

For larger changes, please open an issue first to discuss the proposal.

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
