"""Switcher water heater unofficial API and bridge.

.. codeauthor:: Tomer Figenblat <tomer.figenblat@gmail.com>

"""
from enum import Enum

name = "aioswitcher"

__all__ = ["api", "bridge", "devices", "schedules", "tools"]


class Weekday(Enum):
    """Enum class represnting the weekday."""

    def __new__(cls, value: str, hex_rep: int, bit_rep: int) -> Enum:
        """Override the default enum constructor and include extra properties."""
        new_enum = object.__new__(cls)
        new_enum._value_ = value
        new_enum.hex_rep = hex_rep
        new_enum.bit_rep = bit_rep
        return new_enum

    MONDAY = ("Monday", 0x02, 2)
    TUESDAY = ("Tuesday", 0x04, 4)
    WEDNESDAY = ("Wednesday", 0x08, 8)
    THURSDAY = ("Thursday", 0x10, 16)
    FRIDAY = ("Friday", 0x20, 32)
    SATURDAY = ("Saturday", 0x40, 64)
    SUNDAY = ("Sunday", 0x80, 128)
