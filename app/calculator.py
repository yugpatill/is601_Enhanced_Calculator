from __future__ import annotations
from typing import List
from decimal import Decimal
import pandas as pd

from .calculation import Calculation
from .calculator_config import CalculatorConfig
from .calculator_memento import CalculatorMemento
from .exceptions import OperationError, ValidationError, CalculatorError
from .input_validators import validate_two_numbers, apply_precision
from .operations import OperationFactory
from .history import HistoryObserver, LoggingObserver, AutoSaveObserver
from .logger import get_logger

class Calculator:
    """Calculator core with Factory ops, Memento undo/redo, and Observers."""

    def __init__(self, cfg: CalculatorConfig | None = None):
        self.cfg = cfg or CalculatorConfig.load()
        self._logger = get_logger()
        self._history: List[Calculation] = []
        self._past: List[CalculatorMemento] = []   # undo stack
        self._future: List[CalculatorMemento] = [] # redo stack
        self._observers: List[HistoryObserver] = [
            LoggingObserver(self._logger),
            AutoSaveObserver(),
        ]

    # ----- Observer management -----
    def register_observer(self, obs: HistoryObserver) -> None:
        self._observers.append(obs)     # pragma: no cover

    def _notify(self, calc: Calculation) -> None:
        for obs in self._observers:
            obs.on_new_calculation(calc, self._history, self.cfg)

    # ----- Memento helpers -----
    def _snapshot(self) -> CalculatorMemento:
        return CalculatorMemento(history=list(self._history))

    def _restore(self, m: CalculatorMemento) -> None:
        self._history = list(m.history)

    # ----- Public API -----
    @property
    def history(self) -> List[Calculation]:
        return list(self._history)

    def clear(self) -> None:
        if self._history:
            self._past.append(self._snapshot())
            self._future.clear()
            self._history.clear()

    def perform(self, op_name: str, a, b):
        da, db = validate_two_numbers(a, b, self.cfg)
        op = OperationFactory.create(op_name)
        res = op.execute(da, db, self.cfg)
        res = apply_precision(res, self.cfg)

        calc = Calculation(
            operation=op_name,
            a=da,
            b=db,
            result=res,
            timestamp=Calculation.now_iso(),
        )

        # push memento then mutate
        self._past.append(self._snapshot())
        self._future.clear()
        self._history.append(calc)

        # notify observers (log + autosave)
        self._notify(calc)
        return res

    def undo(self) -> bool:
        if not self._past:
            return False        # pragma: no cover
        current = self._snapshot()
        last = self._past.pop()
        self._future.append(current)
        self._restore(last)
        return True

    def redo(self) -> bool:
        if not self._future:
            return False        # pragma: no cover
        current = self._snapshot()
        nxt = self._future.pop()
        self._past.append(current)
        self._restore(nxt)
        return True

    # ----- Persistence -----
    def save(self) -> None:
        from .history import AutoSaveObserver
        try:
            df = AutoSaveObserver.history_to_df(self._history)
            df.to_csv(self.cfg.history_file, index=False, encoding=self.cfg.default_encoding)
        except Exception as e:      # pragma: no cover
            raise OperationError(f"Failed to save history: {e}")        # pragma: no cover

    def load(self) -> None:
        try:
            df = pd.read_csv(self.cfg.history_file, encoding=self.cfg.default_encoding)
        except FileNotFoundError:
            raise OperationError("No history file found to load")
        except Exception as e:   # pragma: no cover
            raise OperationError(f"Failed to load history: {e}")    # pragma: no cover

        required = {"timestamp", "operation", "a", "b", "result"}
        if not required.issubset(set(df.columns)):
            raise OperationError("Malformed history CSV: missing columns")  # pragma: no cover

        new_hist: List[Calculation] = []
        for _, row in df.iterrows():
            new_hist.append(
                Calculation(
                    operation=str(row["operation"]),
                    a=Decimal(str(row["a"])),
                    b=Decimal(str(row["b"])),
                    result=Decimal(str(row["result"])),
                    timestamp=str(row["timestamp"]),
                )
            )

        self._past.append(self._snapshot())
        self._future.clear()
        self._history = new_hist
