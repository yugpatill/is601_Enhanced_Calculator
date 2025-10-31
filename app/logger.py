import logging
from .calculator_config import CalculatorConfig

_LOGGER = None  

def get_logger() -> logging.Logger:
    """Return a configured logger that writes to a single continuous file."""
    global _LOGGER
    if _LOGGER:
        return _LOGGER

    cfg = CalculatorConfig.load()
    logger = logging.getLogger("calculator")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    fmt = logging.Formatter("%(asctime)s | lvl=%(levelname)s | %(message)s")
    fh = logging.FileHandler(cfg.log_file, encoding=cfg.default_encoding)
    fh.setLevel(logging.INFO)
    fh.setFormatter(fmt)

    if not logger.handlers:
        logger.addHandler(fh)

    _LOGGER = logger
    return _LOGGER
