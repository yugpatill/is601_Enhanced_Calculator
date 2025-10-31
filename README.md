# is601_Enhanced_Calculator

Advanced command-line calculator with:
- **Factory** for operations (add, subtract, multiply, divide, **power, root, modulus, int_divide, percent, abs_diff**)
- **Memento** for undo/redo
- **Observer** for logging + auto-save to CSV (pandas)
- **.env**-driven configuration (python-dotenv)
- **Color-coded output** (colorama)
- **90%+ test coverage** and GitHub Actions CI

## 1) Install

```bash
git clone https://github.com/yugpatill/is601_Enhanced_Calculator
cd is601_Enhanced_Calculator
python3 -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## 2) Configure

Create `.env` (defaults shown):
```env
CALCULATOR_LOG_DIR=./logs
CALCULATOR_HISTORY_DIR=./history
CALCULATOR_MAX_HISTORY_SIZE=1000
CALCULATOR_AUTO_SAVE=true
CALCULATOR_PRECISION=8
CALCULATOR_MAX_INPUT_VALUE=1e12
CALCULATOR_DEFAULT_ENCODING=utf-8
```

## 3) Run

```bash
python main.py
```

Example:
```
> add 2 3
Result: 5.00000000
> power 2 10
Result: 1024.00000000
> percent 25 100
Result: 25.00000000
> undo
Undo OK.
> history
1. 2025-10-30T00:00:00Z | add(2,3) = 5.00000000
```

## 4) Usage Guide (Command-Line Interface)

Start the calculator: python main.py

You’ll enter a REPL (Read–Eval–Print Loop) that supports color-coded output and the following commands:

| Command | Description |
|----------|--------------|
| `add a b` | Adds two numbers |
| `subtract a b` | Subtracts **b** from **a** |
| `multiply a b` | Multiplies **a** and **b** |
| `divide a b` | Divides **a** by **b** |
| `power a b` | Raises **a** to the power of **b** |
| `root a b` | Calculates the **b**-th root of **a** |
| `modulus a b` | Computes the remainder of **a ÷ b** |
| `int_divide a b` | Performs integer division of **a ÷ b** |
| `percent a b` | Calculates **(a / b) × 100** |
| `abs_diff a b` | Returns the absolute difference between **a** and **b** |
| `history` | Displays the complete calculation history |
| `undo` | Reverts the last calculation |
| `redo` | Re-applies the last undone calculation |
| `clear` | Clears the calculation history |
| `save` | Saves history to a CSV file manually |
| `load` | Loads saved history from a CSV file |
| `help` | Displays all available commands |
| `exit` | Exits the calculator application |

>Color Codes

- <span style="color:green;">**Green**</span>: Successful operation  
- <span style="color:red;">**Red**</span>: Error message  
- <span style="color:cyan;">**Cyan**</span>: Informational text

**Notes**
- `percent(a,b) = (a/b)*100` (numeric result)
- `int_divide(a,b)` truncates toward zero
- `root(a,b)` uses integer `b`; even root of negative is invalid

## 5) Testing & Coverage

```bash
pytest
```
or

```bash
pytest --cov=app --cov-report=term-missing --cov-fail-under=90
```

## 6) CI (GitHub Actions)

Runs on every push/PR to `main`, installs deps, runs tests, and **fails** if coverage < 90%.

## 7) Design Decisions

- `Decimal` with output rounding at the boundary (no mid-calc rounding).
- Undo/redo stores complete snapshots—simple and reliable.
- Observers never crash the app; errors are logged but non-fatal.
- Single continuous log file as requested.

## 8) Troubleshooting

- **No colors?** Ensure `colorama` is installed and terminal supports ANSI.
- **Load fails:** run `save` at least once; confirm `.env` directories exist.
- **CSV malformed:** delete history CSV and try again.

---
