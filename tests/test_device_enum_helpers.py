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

"""Switcher integration devices enum helpers test cases."""

from assertpy import assert_that
from pytest import mark

from aioswitcher.device import (
    DeviceCategory,
    DeviceState,
    DeviceType,
    ShutterDirection,
    ThermostatFanLevel,
    ThermostatMode,
    ThermostatSwing,
)


@mark.parametrize(
    "sut_type, expected_value, expected_hex_rep, expected_protocol_type, expected_category, expected_token_needed",
    [
        (DeviceType.MINI, "Switcher Mini", "030f", 1, DeviceCategory.WATER_HEATER, False),
        (
            DeviceType.POWER_PLUG,
            "Switcher Power Plug",
            "01a8",
            1,
            DeviceCategory.POWER_PLUG,
            False,
        ),
        (DeviceType.TOUCH, "Switcher Touch", "030b", 1, DeviceCategory.WATER_HEATER, False),
        (DeviceType.V2_ESP, "Switcher V2 (esp)", "01a7", 1, DeviceCategory.WATER_HEATER, False),
        (
            DeviceType.V2_QCA,
            "Switcher V2 (qualcomm)",
            "01a1",
            1,
            DeviceCategory.WATER_HEATER,
            False,
        ),
        (DeviceType.V4, "Switcher V4", "0317", 1, DeviceCategory.WATER_HEATER, False),
        (DeviceType.BREEZE, "Switcher Breeze", "0e01", 2, DeviceCategory.THERMOSTAT, False),
        (DeviceType.RUNNER, "Switcher Runner", "0c01", 2, DeviceCategory.SHUTTER, False),
        (DeviceType.RUNNER_MINI, "Switcher Runner Mini", "0c02", 2, DeviceCategory.SHUTTER, False),
        (DeviceType.RUNNER_S11, "Switcher Runner S11", "0f01", 2, DeviceCategory.SINGLE_SHUTTER_DUAL_LIGHT, True),
        (DeviceType.RUNNER_S12, "Switcher Runner S12", "0f02", 2, DeviceCategory.DUAL_SHUTTER_SINGLE_LIGHT, True),
        (DeviceType.LIGHT_SL01, "Switcher Light SL01", "0f04", 2, DeviceCategory.LIGHT, True),
        (DeviceType.LIGHT_SL01_MINI, "Switcher Light SL01 Mini", "0f07", 2, DeviceCategory.LIGHT, True),
        (DeviceType.LIGHT_SL02, "Switcher Light SL02", "0f05", 2, DeviceCategory.LIGHT, True),
        (DeviceType.LIGHT_SL02_MINI, "Switcher Light SL02 Mini", "0f08", 2, DeviceCategory.LIGHT, True),
    ],
)
def test_the_given_type_custom_properties_are_returning_the_expected_data(
    sut_type, expected_value, expected_hex_rep, expected_protocol_type, expected_category, expected_token_needed
):
    assert_that(sut_type.value).is_equal_to(expected_value)
    assert_that(sut_type.hex_rep).is_equal_to(expected_hex_rep)
    assert_that(sut_type.protocol_type).is_equal_to(expected_protocol_type)
    assert_that(sut_type.category).is_equal_to(expected_category)
    assert_that(sut_type.token_needed).is_equal_to(expected_token_needed)


@mark.parametrize(
    "sut_state, expected_value, expected_display",
    [(DeviceState.ON, "01", "on"), (DeviceState.OFF, "00", "off")],
)
def test_the_given_state_custom_properties_are_returning_the_expected_data(
    sut_state, expected_value, expected_display
):
    assert_that(sut_state.value).is_equal_to(expected_value)
    assert_that(sut_state.display).is_equal_to(expected_display)


@mark.parametrize(
    "sut_fan_level, expected_value, expected_display",
    [(ThermostatFanLevel.AUTO, "0", "auto"), (ThermostatFanLevel.LOW, "1", "low"), (ThermostatFanLevel.MEDIUM, "2", "medium"), (ThermostatFanLevel.HIGH, "3", "high")],
)
def test_the_given_fan_level_custom_properties_are_returning_the_expected_data(
    sut_fan_level, expected_value, expected_display
):
    assert_that(sut_fan_level.value).is_equal_to(expected_value)
    assert_that(sut_fan_level.display).is_equal_to(expected_display)


@mark.parametrize(
    "sut_mode, expected_value, expected_display",
    [(ThermostatMode.AUTO, "01", "auto"), (ThermostatMode.DRY, "02", "dry"), (ThermostatMode.FAN, "03", "fan"), (ThermostatMode.COOL, "04", "cool"), (ThermostatMode.HEAT, "05", "heat")],
)
def test_the_given_thermostat_mode_custom_properties_are_returning_the_expected_data(
    sut_mode, expected_value, expected_display
):
    assert_that(sut_mode.value).is_equal_to(expected_value)
    assert_that(sut_mode.display).is_equal_to(expected_display)


@mark.parametrize(
    "sut_swing, expected_value, expected_display",
    [(ThermostatSwing.OFF, "0", "off"), (ThermostatSwing.ON, "1", "on")],
)
def test_the_given_thermostat_swing_custom_properties_are_returning_the_expected_data(
    sut_swing, expected_value, expected_display
):
    assert_that(sut_swing.value).is_equal_to(expected_value)
    assert_that(sut_swing.display).is_equal_to(expected_display)


@mark.parametrize(
    "sut_shutter_dir, expected_value, expected_display",
    [(ShutterDirection.SHUTTER_STOP, "0000", "stop"), (ShutterDirection.SHUTTER_DOWN, "0001", "down"), (ShutterDirection.SHUTTER_UP, "0100", "up")],
)
def test_the_given_shutter_direction_custom_properties_are_returning_the_expected_data(
    sut_shutter_dir, expected_value, expected_display
):
    assert_that(sut_shutter_dir.value).is_equal_to(expected_value)
    assert_that(sut_shutter_dir.display).is_equal_to(expected_display)
