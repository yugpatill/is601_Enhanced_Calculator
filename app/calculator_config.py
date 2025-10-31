import os
from dataclasses import dataclass
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(override=True)

def _get(name: str, default: str) -> str:
    return os.getenv(name, default)

@dataclass
class CalculatorConfig:
    log_dir: Path
    history_dir: Path
    max_history_size: int
    auto_save: bool
    precision: int
    max_input_value: float
    default_encoding: str

    @property
    def log_file(self) -> Path:
        return self.log_dir / "calculator.log"

    @property
    def history_file(self) -> Path:
        return self.history_dir / "calculation_history.csv"

    @classmethod
    def load(cls) -> "CalculatorConfig":
        log_dir = Path(_get("CALCULATOR_LOG_DIR", "./logs")).resolve()
        history_dir = Path(_get("CALCULATOR_HISTORY_DIR", "./history")).resolve()
        max_history_size = int(_get("CALCULATOR_MAX_HISTORY_SIZE", "1000"))
        auto_save = _get("CALCULATOR_AUTO_SAVE", "true").lower() == "true"
        precision = int(_get("CALCULATOR_PRECISION", "8"))
        max_input_value = float(_get("CALCULATOR_MAX_INPUT_VALUE", "1e12"))
        default_encoding = _get("CALCULATOR_DEFAULT_ENCODING", "utf-8")

        log_dir.mkdir(parents=True, exist_ok=True)
        history_dir.mkdir(parents=True, exist_ok=True)

        return cls(
            log_dir=log_dir,
            history_dir=history_dir,
            max_history_size=max_history_size,
            auto_save=auto_save,
            precision=precision,
            max_input_value=max_input_value,
            default_encoding=default_encoding,
        )
