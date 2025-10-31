from dataclasses import dataclass
from typing import List
from .calculation import Calculation

@dataclass(frozen=True)
class CalculatorMemento:
    """Snapshot of the calculator's history state for undo/redo."""
    history: List[Calculation]
