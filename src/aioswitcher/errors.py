"""Switcher Devices Error and Exception Classes."""


class CalculationError(Exception):
    """Exception to be raised when cpu bound calculation is failing."""


class DecodingError(Exception):
    """Exception to be raised when cpu bound decoding is failing."""


class EncodingError(Exception):
    """Exception to be raised when cpu bound encoding is failing."""
