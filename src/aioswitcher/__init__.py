"""Switcher water heater unofficial API and bridge.

.. codeauthor:: Tomer Figenblat <tomer.figenblat@gmail.com>

"""
from enum import Enum

name = "aioswitcher"

__all__ = ["api", "bridge", "devices", "schedules", "utils"]


class Weekday(Enum):
    """Enum class represnting the weekday."""

    MONDAY = ("Monday", 0x02, 2)
    TUESDAY = ("Tuesday", 0x04, 4)
    WEDNESDAY = ("Wednesday", 0x08, 8)
    THURSDAY = ("Thursday", 0x10, 16)
    FRIDAY = ("Friday", 0x20, 32)
    SATURDAY = ("Saturday", 0x40, 64)
    SUNDAY = ("Sunday", 0x80, 128)

    def __new__(cls, value: str, hex_rep: int, bit_rep: int) -> "Weekday":
        """Override the default enum constructor and include extra properties."""
        new_enum = object.__new__(cls)
        new_enum._value_ = value
        new_enum._hex_rep = hex_rep
        new_enum._bit_rep = bit_rep
        return new_enum

    def bit_rep(self) -> int:
        return self._bit_rep  # type: ignore

    def hex_rep(self) -> int:
        return self._hex_rep  # type: ignore
