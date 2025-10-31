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

## 4) Commands

- `add a b`, `subtract a b`, `multiply a b`, `divide a b`
- `power a b`, `root a b`, `modulus a b`, `int_divide a b`, `percent a b`, `abs_diff a b`
- `history`, `clear`, `undo`, `redo`, `save`, `load`, `help`, `exit`

**Notes**
- `percent(a,b) = (a/b)*100` (numeric result)
- `int_divide(a,b)` truncates toward zero
- `root(a,b)` uses integer `b`; even root of negative is invalid

## 5) Testing & Coverage

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
