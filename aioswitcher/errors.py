"""Switcher Devices Error and Exception Classes."""


class CalculationError(Exception):
    """Exception to be raised when cpu bound calculation is failing."""

    pass


class DecodingError(Exception):
    """Exception to be raised when cpu bound decoding is failing."""

    pass


class EncodingError(Exception):
    """Exception to be raised when cpu bound encoding is failing."""

    pass
