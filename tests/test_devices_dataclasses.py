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

"""Switcher unofficial integration devices dataclasses test cases."""

from dataclasses import dataclass

from assertpy import assert_that
from pytest import fixture, mark

from aioswitcher.devices import (
    DeviceState,
    DeviceType,
    SwitcherPowerPlug,
    SwitcherWaterHeater,
)


@dataclass(frozen=True)
class FakeData:
    """Fake data for unit tests."""

    device_id: str = "aaaaaa"
    ip_address: str = "192.168.1.33"
    mac_address: str = "12:A1:A2:1A:BC:1A"
    name: str = "My Switcher Boiler"
    power_consumption: int = 2600
    electric_current: float = 11.8
    remaining_time: str = "01:30:00"
    auto_shutdown: str = "03:00:00"


@fixture
def fake_data():
    return FakeData()


@mark.parametrize("device_type", [DeviceType.MINI, DeviceType.TOUCH, DeviceType.V2_ESP, DeviceType.V2_QCA, DeviceType.V4])
def test_given_a_device_of_type_water_heater_when_instantiating_as_a_water_heater_should_be_instatiated_properly(fake_data, device_type):
    sut = SwitcherWaterHeater(
        device_type,
        DeviceState.ON,
        fake_data.device_id,
        fake_data.ip_address,
        fake_data.mac_address,
        fake_data.name,
        fake_data.power_consumption,
        fake_data.electric_current,
        fake_data.remaining_time,
        fake_data.auto_shutdown,
    )

    assert_that(sut.device_type).is_equal_to(device_type)
    assert_that(sut.device_state).is_equal_to(DeviceState.ON)
    assert_that(sut.device_id).is_equal_to(fake_data.device_id)
    assert_that(sut.ip_address).is_equal_to(fake_data.ip_address)
    assert_that(sut.mac_address).is_equal_to(fake_data.mac_address)
    assert_that(sut.name).is_equal_to(fake_data.name)
    assert_that(sut.power_consumption).is_equal_to(fake_data.power_consumption)
    assert_that(sut.electric_current).is_equal_to(fake_data.electric_current)
    assert_that(sut.remaining_time).is_equal_to(fake_data.remaining_time)
    assert_that(sut.auto_shutdown).is_equal_to(fake_data.auto_shutdown)


def test_given_a_device_of_type_power_plug_when_instantiating_as_a_power_plug_should_be_instatiated_properly(fake_data):
    sut = SwitcherPowerPlug(
        DeviceType.POWER_PLUG,
        DeviceState.ON,
        fake_data.device_id,
        fake_data.ip_address,
        fake_data.mac_address,
        fake_data.name,
        fake_data.power_consumption,
        fake_data.electric_current,
    )

    assert_that(sut.device_type).is_equal_to(DeviceType.POWER_PLUG)
    assert_that(sut.device_state).is_equal_to(DeviceState.ON)
    assert_that(sut.device_id).is_equal_to(fake_data.device_id)
    assert_that(sut.ip_address).is_equal_to(fake_data.ip_address)
    assert_that(sut.mac_address).is_equal_to(fake_data.mac_address)
    assert_that(sut.name).is_equal_to(fake_data.name)
    assert_that(sut.power_consumption).is_equal_to(fake_data.power_consumption)
    assert_that(sut.electric_current).is_equal_to(fake_data.electric_current)


@mark.parametrize("device_type", [DeviceType.MINI, DeviceType.TOUCH, DeviceType.V2_ESP, DeviceType.V2_QCA, DeviceType.V4])
def test_given_a_device_of_type_water_heater_when_instantiating_as_a_power_plug_should_raise_an_error(fake_data, device_type):
    assert_that(SwitcherPowerPlug).raises(ValueError).when_called_with(
        device_type,
        DeviceState.ON,
        fake_data.device_id,
        fake_data.ip_address,
        fake_data.mac_address,
        fake_data.name,
        fake_data.power_consumption,
        fake_data.electric_current,
    ).is_equal_to("only power plugs are allowed")


def test_given_a_device_of_type_power_plug_when_instantiating_as_a_water_heater_should_raise_an_error(fake_data):
    assert_that(SwitcherWaterHeater).raises(ValueError).when_called_with(
        DeviceType.POWER_PLUG,
        DeviceState.ON,
        fake_data.device_id,
        fake_data.ip_address,
        fake_data.mac_address,
        fake_data.name,
        fake_data.power_consumption,
        fake_data.electric_current,
        fake_data.remaining_time,
        fake_data.auto_shutdown,
    ).is_equal_to("only water heaters are allowed")
