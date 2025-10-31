from dataclasses import dataclass
from decimal import Decimal
from datetime import datetime, timezone

@dataclass(frozen=True)
class Calculation:
    """Immutable record of a single calculation event."""
    operation: str
    a: Decimal
    b: Decimal
    result: Decimal
    timestamp: str  

    @staticmethod
    def now_iso() -> str:
        return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")
