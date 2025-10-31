class CalculatorError(Exception):
    """Base class for calculator errors."""


class ValidationError(CalculatorError):
    """Raised when user input is invalid or out of allowed range."""


class OperationError(CalculatorError):
    """Raised when an operation fails (e.g., divide by zero, invalid root)."""
