from abc import ABC, abstractmethod
from decimal import Decimal
from typing import Dict, Type
from .exceptions import OperationError, ValidationError
from .calculator_config import CalculatorConfig

class Operation(ABC):
    """Binary operation interface returning a Decimal result."""
    @abstractmethod
    def execute(self, a: Decimal, b: Decimal, cfg: CalculatorConfig) -> Decimal:
        ...

class Add(Operation):
    def execute(self, a, b, cfg): return a + b

class Subtract(Operation):
    def execute(self, a, b, cfg): return a - b

class Multiply(Operation):
    def execute(self, a, b, cfg): return a * b

class Divide(Operation):
    def execute(self, a, b, cfg):
        if b == 0:
            raise OperationError("Division by zero")
        return a / b

class Power(Operation):
    def execute(self, a, b, cfg):
        try:
            return a ** b
        except Exception as e:  # pragma: no cover
            raise OperationError(f"Power failed: {e}")

class Root(Operation):
    def execute(self, a, b, cfg):
        if b == 0:
            raise OperationError("Root with zero degree is undefined")
        if b != int(b):
            raise ValidationError("Root degree must be an integer")  # pragma: no cover
        n = int(b)
        if a < 0 and n % 2 == 0:
            raise OperationError("Even root of a negative number is invalid")
        return a.__abs__() ** (Decimal(1) / Decimal(n)) * (-1 if a < 0 else 1)

class Modulus(Operation):
    def execute(self, a, b, cfg):
        if b == 0:
            raise OperationError("Modulus by zero")     # pragma: no cover
        return a % b

class IntegerDivide(Operation):
    def execute(self, a, b, cfg):
        if b == 0:
            raise OperationError("Integer division by zero")    # pragma: no cover
        return Decimal(int(a / b))

class Percentage(Operation):
    def execute(self, a, b, cfg):
        if b == 0:
            raise OperationError("Percentage with zero denominator")
        return (a / b) * Decimal(100)

class AbsoluteDifference(Operation):
    def execute(self, a, b, cfg):
        return (a - b).__abs__()

class OperationFactory:
    """Factory mapping command names to operation classes."""
    _registry: Dict[str, Type[Operation]] = {
        "add": Add,
        "subtract": Subtract,
        "multiply": Multiply,
        "divide": Divide,
        "power": Power,
        "root": Root,
        "modulus": Modulus,
        "int_divide": IntegerDivide,
        "percent": Percentage,
        "abs_diff": AbsoluteDifference,
    }

    @classmethod
    def create(cls, name: str) -> Operation:
        op_cls = cls._registry.get(name)
        if not op_cls:
            raise OperationError(f"Unknown operation: {name}")
        return op_cls()
