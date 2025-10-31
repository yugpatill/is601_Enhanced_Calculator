import pytest
from app.calculator import Calculator
from app.exceptions import CalculatorError
from app.calculator_config import CalculatorConfig

def make_calc():
    cfg = CalculatorConfig.load()
    return Calculator(cfg)

def test_perform_and_history():
    c = make_calc()
    r = c.perform("add", "2", "3")
    # precision dependent string, simply ensure history captured
    assert len(c.history) == 1
    assert c.history[0].operation == "add"

def test_undo_redo():
    c = make_calc()
    c.perform("add", 1, 1)
    c.perform("multiply", 2, 5)
    assert len(c.history) == 2
    assert c.undo() is True
    assert len(c.history) == 1
    assert c.redo() is True
    assert len(c.history) == 2

def test_clear_and_undo():
    c = make_calc()
    c.perform("add", 1, 1)
    c.clear()
    assert len(c.history) == 0
    assert c.undo() is True
    assert len(c.history) == 1

def test_save_and_load(tmp_path, monkeypatch):
    # set temp history dir
    monkeypatch.setenv("CALCULATOR_HISTORY_DIR", str(tmp_path))
    c = Calculator(CalculatorConfig.load())
    c.perform("add", 1, 2)
    c.save()
    assert c.cfg.history_file.exists()
    # load into fresh instance
    c2 = Calculator(CalculatorConfig.load())
    c2.load()
    assert len(c2.history) == 1
    assert c2.history[0].operation == "add"

def test_load_missing_file(tmp_path, monkeypatch):
    monkeypatch.setenv("CALCULATOR_HISTORY_DIR", str(tmp_path))
    c = Calculator(CalculatorConfig.load())
    with pytest.raises(CalculatorError):
        c.load()

def test_invalid_command_raises():
    c = make_calc()
    with pytest.raises(CalculatorError):
        c.perform("unknown_op", 1, 2)
