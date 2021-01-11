"""Patch asynctest being replaced by unittest in python 3.8."""
# flake8: noqa
import sys

if sys.version_info[:2] < (3, 8):
    from asynctest.mock import *

    AsyncMock = CoroutineMock
else:
    from unittest.mock import *
