from decimal import Decimal
from app.calculation import Calculation

def test_calculation_dataclass():
    c = Calculation("add", Decimal(1), Decimal(2), Decimal(3), Calculation.now_iso())
    assert c.operation == "add"
    assert c.a == Decimal(1)
    assert c.result == Decimal(3)
    assert c.timestamp.endswith("Z")
