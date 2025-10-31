import pytest
from decimal import Decimal
from app.operations import OperationFactory
from app.calculator_config import CalculatorConfig

CFG = CalculatorConfig.load()

@pytest.mark.parametrize("a,b,expected", [
    ("2","3", Decimal("5")),
    ("-2","3", Decimal("1")),
])
def test_add(a,b,expected):
    res = OperationFactory.create("add").execute(Decimal(a), Decimal(b), CFG)
    assert res == expected

@pytest.mark.parametrize("a,b,expected", [
    ("2","3", Decimal("-1")),
    ("3","-2", Decimal("5")),
])
def test_subtract(a,b,expected):
    res = OperationFactory.create("subtract").execute(Decimal(a), Decimal(b), CFG)
    assert res == expected

@pytest.mark.parametrize("a,b,expected", [
    ("2","3", Decimal("6")),
    ("-2","3", Decimal("-6")),
])
def test_multiply(a,b,expected):
    res = OperationFactory.create("multiply").execute(Decimal(a), Decimal(b), CFG)
    assert res == expected

@pytest.mark.parametrize("a,b,expected", [
    ("6","3", Decimal("2")),
    ("-6","3", Decimal("-2")),
])
def test_divide(a,b,expected):
    res = OperationFactory.create("divide").execute(Decimal(a), Decimal(b), CFG)
    assert res == expected

def test_divide_by_zero():
    with pytest.raises(Exception):
        OperationFactory.create("divide").execute(Decimal(1), Decimal(0), CFG)

@pytest.mark.parametrize("a,b,expected", [
    ("2","3", Decimal("8")),
    ("9","0.5", Decimal("3")),  # sqrt(9)
])
def test_power(a,b,expected):
    res = OperationFactory.create("power").execute(Decimal(a), Decimal(b), CFG)
    assert res.quantize(Decimal("1.000")) == expected.quantize(Decimal("1.000"))

@pytest.mark.parametrize("a,b,expected", [
    ("9","2", Decimal("3")),
    ("-8","3", Decimal("-2")),
])
def test_root(a,b,expected):
    res = OperationFactory.create("root").execute(Decimal(a), Decimal(b), CFG)
    assert res == expected

def test_root_invalid_degree_zero():
    with pytest.raises(Exception):
        OperationFactory.create("root").execute(Decimal(9), Decimal(0), CFG)

def test_root_even_negative():
    with pytest.raises(Exception):
        OperationFactory.create("root").execute(Decimal(-9), Decimal(2), CFG)

@pytest.mark.parametrize("a,b,expected", [
    ("7","3", Decimal("1")),
    ("-7","3", Decimal("-1")),
])
def test_modulus(a,b,expected):
    res = OperationFactory.create("modulus").execute(Decimal(a), Decimal(b), CFG)
    assert res == expected

@pytest.mark.parametrize("a,b,expected", [
    ("7","3", Decimal("2")),
    ("-7","3", Decimal("-2")),  # trunc toward zero
])
def test_int_divide(a,b,expected):
    res = OperationFactory.create("int_divide").execute(Decimal(a), Decimal(b), CFG)
    assert res == expected

@pytest.mark.parametrize("a,b,expected", [
    ("25","100", Decimal("25")),
    ("1","2", Decimal("50")),
])
def test_percent(a,b,expected):
    res = OperationFactory.create("percent").execute(Decimal(a), Decimal(b), CFG)
    assert res == expected

def test_percent_zero_denominator():
    with pytest.raises(Exception):
        OperationFactory.create("percent").execute(Decimal(1), Decimal(0), CFG)

@pytest.mark.parametrize("a,b,expected", [
    ("5","3", Decimal("2")),
    ("3","5", Decimal("2")),
])
def test_abs_diff(a,b,expected):
    res = OperationFactory.create("abs_diff").execute(Decimal(a), Decimal(b), CFG)
    assert res == expected
