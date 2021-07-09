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

from aioswitcher.device import DeviceCategory, DeviceState, DeviceType


@mark.parametrize("sut_type, expected_value, expected_hex_rep, expected_category", [
    (DeviceType.MINI, "Switcher Mini", "0f", DeviceCategory.WATER_HEATER),
    (DeviceType.POWER_PLUG, "Switcher Power Plug", "a8", DeviceCategory.POWER_PLUG),
    (DeviceType.TOUCH, "Switcher Touch", "0b", DeviceCategory.WATER_HEATER),
    (DeviceType.V2_ESP, "Switcher V2 (esp)", "a7", DeviceCategory.WATER_HEATER),
    (DeviceType.V2_QCA, "Switcher V2 (qualcomm)", "a1", DeviceCategory.WATER_HEATER),
    (DeviceType.V4, "Switcher V4", "17", DeviceCategory.WATER_HEATER),
])
def test_the_given_type_custom_properties_are_returning_the_expected_data(sut_type, expected_value, expected_hex_rep, expected_category):
    assert_that(sut_type.value).is_equal_to(expected_value)
    assert_that(sut_type.hex_rep).is_equal_to(expected_hex_rep)
    assert_that(sut_type.category).is_equal_to(expected_category)


@mark.parametrize("sut_state, expected_value, expected_display", [
    (DeviceState.ON, "0100", "on"), (DeviceState.OFF, "0000", "off")
])
def test_the_given_state_custom_properties_are_returning_the_expected_data(sut_state, expected_value, expected_display):
    assert_that(sut_state.value).is_equal_to(expected_value)
    assert_that(sut_state.display).is_equal_to(expected_display)
