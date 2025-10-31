from abc import ABC, abstractmethod
from typing import List
import pandas as pd
from .calculation import Calculation
from .calculator_config import CalculatorConfig

class HistoryObserver(ABC):
    """Observer notified whenever a new calculation is appended."""
    @abstractmethod
    def on_new_calculation(self, calc: Calculation, all_history: List[Calculation], cfg: CalculatorConfig) -> None:
        ...

class LoggingObserver(HistoryObserver):
    def __init__(self, logger):
        self._logger = logger

    def on_new_calculation(self, calc: Calculation, all_history: List[Calculation], cfg: CalculatorConfig) -> None:
        self._logger.info(
            f"{calc.operation}({calc.a},{calc.b}) -> {calc.result} @ {calc.timestamp}"
        )

class AutoSaveObserver(HistoryObserver):
    def on_new_calculation(self, calc: Calculation, all_history: List[Calculation], cfg: CalculatorConfig) -> None:
        if not cfg.auto_save:
            return  # pragma: no cover
        try:
            df = self.history_to_df(all_history)
            df.to_csv(cfg.history_file, index=False, encoding=cfg.default_encoding)
        except Exception:   # pragma: no cover
            # observer shouldn't crash the app
            pass  # pragma: no cover

    @staticmethod
    def history_to_df(history: List[Calculation]) -> pd.DataFrame:
        rows = [
            {
                "timestamp": c.timestamp,
                "operation": c.operation,
                "a": str(c.a),
                "b": str(c.b),
                "result": str(c.result),
            }
            for c in history
        ]
        return pd.DataFrame(rows)
