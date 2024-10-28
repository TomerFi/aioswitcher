# Copyright Tomer Figenblat.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Switcher integration parsing devices from datagrams test cases."""

from binascii import unhexlify
from pathlib import Path
from unittest.mock import Mock, patch

from assertpy import assert_that
from pytest import fixture, warns

from aioswitcher.bridge import DatagramParser, _parse_device_from_datagram
from aioswitcher.device import (
    DeviceState,
    SwitcherDualShutterSingleLight,
    SwitcherLight,
    SwitcherPowerPlug,
    SwitcherShutter,
    SwitcherSingleShutterDualLight,
    SwitcherThermostat,
    SwitcherWaterHeater,
)


@fixture
def mock_callback():
    return Mock()


@fixture
def mock_device():
    return Mock()


@patch("logging.Logger.debug")
@patch.object(DatagramParser, "is_switcher_originator", lambda s: False)
def test_an_unknown_datagram_not_produces_device(mock_debug, mock_callback):
    assert_that(_parse_device_from_datagram(mock_callback, "a moot datagram")).is_none()
    mock_debug.assert_called_once_with("received datagram from an unknown source")
    mock_callback.assert_not_called()


@patch.object(DatagramParser, "is_switcher_originator", lambda s: True)
@patch.object(DatagramParser, "get_device_type", lambda s: None)
@patch.object(DatagramParser, "get_device_state", lambda s: DeviceState.OFF)
def test_an_unknown_device_type_produces_a_warning(mock_callback):
    with warns(UserWarning, match="discovered an unknown switcher device"):
        _parse_device_from_datagram(mock_callback, "a moot datagram")
        mock_callback.assert_not_called()


@patch.object(SwitcherWaterHeater, "__new__")
@patch.object(DatagramParser, "is_switcher_originator", lambda s: True)
def test_a_water_heater_datagram_produces_device(mock_device_cls, mock_device, resource_path, mock_callback):
    mock_device_cls.return_value = mock_device
    sut_datagram = Path(f'{resource_path}.txt').read_text().replace('\n', '').encode()
    _parse_device_from_datagram(mock_callback, unhexlify(sut_datagram))
    mock_callback.assert_called_once_with(mock_device)


@patch.object(SwitcherPowerPlug, "__new__")
@patch.object(DatagramParser, "is_switcher_originator", lambda s: True)
def test_a_power_plug_datagram_produces_device(mock_device_cls, mock_device, resource_path, mock_callback):
    mock_device_cls.return_value = mock_device
    sut_datagram = Path(f'{resource_path}.txt').read_text().replace('\n', '').encode()
    _parse_device_from_datagram(mock_callback, unhexlify(sut_datagram))
    mock_callback.assert_called_once_with(mock_device)


@patch.object(SwitcherThermostat, "__new__")
@patch.object(DatagramParser, "is_switcher_originator", lambda s: True)
def test_a_breeze_datagram_produces_device(mock_device_cls, mock_device, resource_path, mock_callback):
    mock_device_cls.return_value = mock_device
    sut_datagram = Path(f'{resource_path}.txt').read_text().replace('\n', '').encode()
    _parse_device_from_datagram(mock_callback, unhexlify(sut_datagram))
    mock_callback.assert_called_once_with(mock_device)


@patch.object(SwitcherShutter, "__new__")
@patch.object(DatagramParser, "is_switcher_originator", lambda s: True)
def test_a_runner_datagram_produces_device(mock_device_cls, mock_device, resource_path, mock_callback):
    mock_device_cls.return_value = mock_device
    sut_datagram = Path(f'{resource_path}.txt').read_text().replace('\n', '').encode()
    _parse_device_from_datagram(mock_callback, unhexlify(sut_datagram))
    mock_callback.assert_called_once_with(mock_device)


@patch.object(SwitcherSingleShutterDualLight, "__new__")
@patch.object(DatagramParser, "is_switcher_originator", lambda s: True)
def test_a_single_runner_dual_light_datagram_produces_device(mock_device_cls, mock_device, resource_path, mock_callback):
    mock_device_cls.return_value = mock_device
    sut_datagram = Path(f'{resource_path}.txt').read_text().replace('\n', '').encode()
    _parse_device_from_datagram(mock_callback, unhexlify(sut_datagram))
    mock_callback.assert_called_once_with(mock_device)


@patch.object(SwitcherDualShutterSingleLight, "__new__")
@patch.object(DatagramParser, "is_switcher_originator", lambda s: True)
def test_a_dual_runner_single_light_datagram_produces_device(mock_device_cls, mock_device, resource_path, mock_callback):
    mock_device_cls.return_value = mock_device
    sut_datagram = Path(f'{resource_path}.txt').read_text().replace('\n', '').encode()
    _parse_device_from_datagram(mock_callback, unhexlify(sut_datagram))
    mock_callback.assert_called_once_with(mock_device)


@patch.object(SwitcherLight, "__new__")
@patch.object(DatagramParser, "is_switcher_originator", lambda s: True)
def test_a_light_datagram_produces_device(mock_device_cls, mock_device, resource_path, mock_callback):
    mock_device_cls.return_value = mock_device
    sut_datagram = Path(f'{resource_path}.txt').read_text().replace('\n', '').encode()
    _parse_device_from_datagram(mock_callback, unhexlify(sut_datagram))
    mock_callback.assert_called_once_with(mock_device)


@patch.object(SwitcherLight, "__new__")
@patch.object(DatagramParser, "is_switcher_originator", lambda s: True)
def test_a_dual_light_datagram_produces_device(mock_device_cls, mock_device, resource_path, mock_callback):
    mock_device_cls.return_value = mock_device
    sut_datagram = Path(f'{resource_path}.txt').read_text().replace('\n', '').encode()
    _parse_device_from_datagram(mock_callback, unhexlify(sut_datagram))
    mock_callback.assert_called_once_with(mock_device)
