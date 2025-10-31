from decimal import Decimal, InvalidOperation, getcontext, ROUND_HALF_UP
from typing import Union
from .exceptions import ValidationError
from .calculator_config import CalculatorConfig

NumberLike = Union[int, float, str, Decimal]

def to_decimal(value: NumberLike, name: str) -> Decimal:
    """Convert allowed types to Decimal with friendly errors."""
    try:
        d = Decimal(str(value))
        return d
    except (InvalidOperation, ValueError):      # pragma: no cover
        raise ValidationError(f"Non-numeric input for {name}: {value!r}")   # pragma: no cover

def check_range(d: Decimal, cfg: CalculatorConfig, name: str) -> None:
    max_abs = Decimal(str(cfg.max_input_value))
    if d.copy_abs() > max_abs:
        raise ValidationError(f"Input out of range for {name}: {d} (>|{max_abs}|)")     # pragma: no cover

def apply_precision(d: Decimal, cfg: CalculatorConfig) -> Decimal:
    """Apply output rounding at the boundary, not mid-calc."""
    q = Decimal("1").scaleb(-cfg.precision)  # 10^-precision
    return d.quantize(q, rounding=ROUND_HALF_UP)

def validate_two_numbers(a: NumberLike, b: NumberLike, cfg: CalculatorConfig) -> tuple[Decimal, Decimal]:
    da = to_decimal(a, "a")
    db = to_decimal(b, "b")
    for name, val in (("a", da), ("b", db)):
        if not val.is_finite():
            raise ValidationError(f"Non-finite input for {name}: {val}")    # pragma: no cover
    check_range(da, cfg, "a")
    check_range(db, cfg, "b")
    getcontext().prec = max(28, cfg.precision + 6)
    return da, db
