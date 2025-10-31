import sys
from colorama import init as colorama_init, Fore, Style
from app.calculator import Calculator
from app.exceptions import CalculatorError
from app.calculator_config import CalculatorConfig

class ColorOut:
    @staticmethod
    def ok(msg: str): print(Fore.GREEN + msg + Style.RESET_ALL)
    @staticmethod
    def warn(msg: str): print(Fore.YELLOW + msg + Style.RESET_ALL)
    @staticmethod
    def err(msg: str): print(Fore.RED + msg + Style.RESET_ALL)
    @staticmethod
    def info(msg: str): print(Fore.CYAN + msg + Style.RESET_ALL)

HELP = """Commands:
  add a b | subtract a b | multiply a b | divide a b
  power a b | root a b | modulus a b | int_divide a b | percent a b | abs_diff a b
  history     - show calculation history
  clear       - clear calculation history
  undo        - undo last change
  redo        - redo last undone change
  save        - save history to CSV
  load        - load history from CSV
  help        - show this help
  exit        - quit
"""

def main() -> int:
    colorama_init(autoreset=True)
    cfg = CalculatorConfig.load()
    calc = Calculator(cfg)

    ColorOut.info("Enhanced Calculator REPL. Type 'help' for commands.")
    while True:
        try:
            line = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            return 0

        if not line:
            continue

        parts = line.split()
        cmd = parts[0].lower()

        if cmd == "exit":
            ColorOut.info("Bye!")
            return 0
        if cmd == "help":
            print(HELP); continue
        if cmd == "history":
            items = calc.history
            if not items:
                ColorOut.warn("History is empty.")
            else:
                for i, c in enumerate(items, 1):
                    ColorOut.info(f"{i}. {c.timestamp} | {c.operation}({c.a},{c.b}) = {c.result}")
            continue
        if cmd == "clear":
            calc.clear()
            ColorOut.warn("History cleared.")
            continue
        if cmd == "undo":
            if calc.undo():
                ColorOut.warn("Undo OK.")
            else:
                ColorOut.warn("Nothing to undo.")
            continue
        if cmd == "redo":
            if calc.redo():
                ColorOut.warn("Redo OK.")
            else:
                ColorOut.warn("Nothing to redo.")
            continue
        if cmd == "save":
            try:
                calc.save()
                ColorOut.ok("History saved.")
            except CalculatorError as e:
                ColorOut.err(f"Save failed: {e}")
            continue
        if cmd == "load":
            try:
                calc.load()
                ColorOut.ok("History loaded.")
            except CalculatorError as e:
                ColorOut.err(f"Load failed: {e}")
            continue

        # Operations with two args
        if len(parts) == 3:
            op, a, b = parts[0], parts[1], parts[2]
            try:
                res = calc.perform(op, a, b)
                ColorOut.ok(f"Result: {res}")
            except CalculatorError as e:
                ColorOut.err(f"Error: {e}")
            continue

        ColorOut.err("Invalid command or arity. Type 'help'.")

if __name__ == "__main__":
    sys.exit(main())
