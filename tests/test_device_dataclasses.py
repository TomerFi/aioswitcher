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

"""Switcher integration devices dataclasses test cases."""

from dataclasses import dataclass, field
from typing import List

from assertpy import assert_that
from pytest import fixture, mark

from aioswitcher.device import (
    DeviceState,
    DeviceType,
    ShutterDirection,
    SwitcherDualShutterSingleLight,
    SwitcherLight,
    SwitcherPowerPlug,
    SwitcherShutter,
    ShutterChildLock,
    SwitcherSingleShutterDualLight,
    SwitcherThermostat,
    SwitcherWaterHeater,
    ThermostatFanLevel,
    ThermostatMode,
    ThermostatSwing,
)


@dataclass(frozen=True)
class FakeData:
    """Fake data for unit tests."""

    device_id: str = "aaaaaa"
    device_key: str = "18"
    ip_address: str = "192.168.1.33"
    mac_address: str = "12:A1:A2:1A:BC:1A"
    name: str = "My Switcher Boiler"
    token_needed: bool = False
    power_consumption: int = 2600
    electric_current: float = 11.8
    remaining_time: str = "01:30:00"
    auto_shutdown: str = "03:00:00"
    mode: ThermostatMode = ThermostatMode.COOL
    fan_level: ThermostatFanLevel = ThermostatFanLevel.HIGH
    swing: ThermostatSwing = ThermostatSwing.OFF
    target_temperature: int = 24
    temperature: float = 26.5
    remote_id: str = "ELEC7022"
    position: List[int] = field(default_factory=lambda: [50])
    position2: List[int] = field(default_factory=lambda: [50, 50])
    direction: List[ShutterDirection] = field(default_factory=lambda: [ShutterDirection.SHUTTER_STOP])
    direction2: List[ShutterDirection] = field(default_factory=lambda: [ShutterDirection.SHUTTER_STOP, ShutterDirection.SHUTTER_STOP])
    child_lock: List[ShutterChildLock] = field(default_factory=lambda: [ShutterChildLock.OFF])
    child_lock2: List[ShutterChildLock] = field(default_factory=lambda: [ShutterChildLock.OFF, ShutterChildLock.OFF])
    light: List[DeviceState] = field(default_factory=lambda: [DeviceState.ON])
    light2: List[DeviceState] = field(default_factory=lambda: [DeviceState.ON, DeviceState.ON])


@fixture
def fake_data():
    return FakeData()


@mark.parametrize("device_type", [DeviceType.MINI, DeviceType.TOUCH, DeviceType.V2_ESP, DeviceType.V2_QCA, DeviceType.V4])
def test_given_a_device_of_type_water_heater_when_instantiating_as_a_water_heater_should_be_instatiated_properly(fake_data, device_type):
    sut = SwitcherWaterHeater(
        device_type,
        DeviceState.ON,
        fake_data.device_id,
        fake_data.device_key,
        fake_data.ip_address,
        fake_data.mac_address,
        fake_data.name,
        fake_data.token_needed,
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
    assert_that(sut.auto_off_set).is_equal_to(fake_data.auto_shutdown)


def test_given_a_device_of_type_power_plug_when_instantiating_as_a_power_plug_should_be_instatiated_properly(fake_data):
    sut = SwitcherPowerPlug(
        DeviceType.POWER_PLUG,
        DeviceState.ON,
        fake_data.device_id,
        fake_data.device_key,
        fake_data.ip_address,
        fake_data.mac_address,
        fake_data.name,
        fake_data.token_needed,
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


def test_given_a_device_of_type_thermostat_when_instantiating_as_a_thermostat_should_be_instatiated_properly(fake_data):
    sut = SwitcherThermostat(
        DeviceType.BREEZE,
        DeviceState.ON,
        fake_data.device_id,
        fake_data.device_key,
        fake_data.ip_address,
        fake_data.mac_address,
        fake_data.name,
        fake_data.token_needed,
        fake_data.mode,
        fake_data.temperature,
        fake_data.target_temperature,
        fake_data.fan_level,
        fake_data.swing,
        fake_data.remote_id
    )

    assert_that(sut.device_type).is_equal_to(DeviceType.BREEZE)
    assert_that(sut.device_state).is_equal_to(DeviceState.ON)
    assert_that(sut.device_id).is_equal_to(fake_data.device_id)
    assert_that(sut.ip_address).is_equal_to(fake_data.ip_address)
    assert_that(sut.mac_address).is_equal_to(fake_data.mac_address)
    assert_that(sut.name).is_equal_to(fake_data.name)
    assert_that(sut.mode).is_equal_to(fake_data.mode)
    assert_that(sut.temperature).is_equal_to(fake_data.temperature)
    assert_that(sut.target_temperature).is_equal_to(fake_data.target_temperature)
    assert_that(sut.fan_level).is_equal_to(fake_data.fan_level)
    assert_that(sut.swing).is_equal_to(fake_data.swing)
    assert_that(sut.remote_id).is_equal_to(fake_data.remote_id)


def test_given_a_device_of_type_shutter_when_instantiating_as_a_shutter_should_be_instatiated_properly(fake_data):
    sut = SwitcherShutter(
        DeviceType.RUNNER,
        DeviceState.ON,
        fake_data.device_id,
        fake_data.device_key,
        fake_data.ip_address,
        fake_data.mac_address,
        fake_data.name,
        fake_data.token_needed,
        fake_data.position,
        fake_data.direction,
        fake_data.child_lock
    )

    assert_that(sut.device_type).is_equal_to(DeviceType.RUNNER)
    assert_that(sut.device_state).is_equal_to(DeviceState.ON)
    assert_that(sut.device_id).is_equal_to(fake_data.device_id)
    assert_that(sut.ip_address).is_equal_to(fake_data.ip_address)
    assert_that(sut.mac_address).is_equal_to(fake_data.mac_address)
    assert_that(sut.name).is_equal_to(fake_data.name)
    assert_that(sut.position).is_equal_to(fake_data.position)
    assert_that(sut.direction).is_equal_to(fake_data.direction)
    assert_that(sut.child_lock).is_equal_to(fake_data.child_lock)


def test_given_a_device_of_type_single_shutter_dual_light_when_instantiating_as_a_shutter_should_be_instatiated_properly(fake_data):
    sut = SwitcherSingleShutterDualLight(
        DeviceType.RUNNER_S11,
        DeviceState.ON,
        fake_data.device_id,
        fake_data.device_key,
        fake_data.ip_address,
        fake_data.mac_address,
        fake_data.name,
        fake_data.token_needed,
        fake_data.position,
        fake_data.direction,
        fake_data.child_lock,
        fake_data.light
    )

    assert_that(sut.device_type).is_equal_to(DeviceType.RUNNER_S11)
    assert_that(sut.device_state).is_equal_to(DeviceState.ON)
    assert_that(sut.device_id).is_equal_to(fake_data.device_id)
    assert_that(sut.ip_address).is_equal_to(fake_data.ip_address)
    assert_that(sut.mac_address).is_equal_to(fake_data.mac_address)
    assert_that(sut.name).is_equal_to(fake_data.name)
    assert_that(sut.position).is_equal_to(fake_data.position)
    assert_that(sut.direction).is_equal_to(fake_data.direction)
    assert_that(sut.child_lock).is_equal_to(fake_data.child_lock)
    assert_that(sut.light).is_equal_to(fake_data.light)


def test_given_a_device_of_type_dual_shutter_single_light_when_instantiating_as_a_shutter_should_be_instatiated_properly(fake_data):
    sut = SwitcherDualShutterSingleLight(
        DeviceType.RUNNER_S12,
        DeviceState.ON,
        fake_data.device_id,
        fake_data.device_key,
        fake_data.ip_address,
        fake_data.mac_address,
        fake_data.name,
        fake_data.token_needed,
        fake_data.position,
        fake_data.direction,
        fake_data.child_lock,
        fake_data.light
    )

    assert_that(sut.device_type).is_equal_to(DeviceType.RUNNER_S12)
    assert_that(sut.device_state).is_equal_to(DeviceState.ON)
    assert_that(sut.device_id).is_equal_to(fake_data.device_id)
    assert_that(sut.ip_address).is_equal_to(fake_data.ip_address)
    assert_that(sut.mac_address).is_equal_to(fake_data.mac_address)
    assert_that(sut.name).is_equal_to(fake_data.name)
    assert_that(sut.position).is_equal_to(fake_data.position)
    assert_that(sut.direction).is_equal_to(fake_data.direction)
    assert_that(sut.child_lock).is_equal_to(fake_data.child_lock)
    assert_that(sut.light).is_equal_to(fake_data.light)


def test_given_a_device_of_type_light_when_instantiating_as_a_shutter_should_be_instatiated_properly(fake_data):
    sut = SwitcherLight(
        DeviceType.LIGHT_SL01,
        DeviceState.ON,
        fake_data.device_id,
        fake_data.device_key,
        fake_data.ip_address,
        fake_data.mac_address,
        fake_data.name,
        fake_data.token_needed,
        fake_data.light
    )

    assert_that(sut.device_type).is_equal_to(DeviceType.LIGHT_SL01)
    assert_that(sut.device_state).is_equal_to(DeviceState.ON)
    assert_that(sut.device_id).is_equal_to(fake_data.device_id)
    assert_that(sut.ip_address).is_equal_to(fake_data.ip_address)
    assert_that(sut.mac_address).is_equal_to(fake_data.mac_address)
    assert_that(sut.name).is_equal_to(fake_data.name)
    assert_that(sut.light).is_equal_to(fake_data.light)


@mark.parametrize("device_type", [DeviceType.MINI, DeviceType.TOUCH, DeviceType.V2_ESP, DeviceType.V2_QCA, DeviceType.V4])
def test_given_a_device_of_type_water_heater_when_instantiating_as_a_power_plug_should_raise_an_error(fake_data, device_type):
    assert_that(SwitcherPowerPlug).raises(ValueError).when_called_with(
        device_type,
        DeviceState.ON,
        fake_data.device_id,
        fake_data.device_key,
        fake_data.ip_address,
        fake_data.mac_address,
        fake_data.name,
        fake_data.token_needed,
        fake_data.power_consumption,
        fake_data.electric_current,
    ).is_equal_to("only power plugs are allowed")


def test_given_a_device_of_type_power_plug_when_instantiating_as_a_water_heater_should_raise_an_error(fake_data):
    assert_that(SwitcherWaterHeater).raises(ValueError).when_called_with(
        DeviceType.POWER_PLUG,
        DeviceState.ON,
        fake_data.device_id,
        fake_data.device_key,
        fake_data.ip_address,
        fake_data.mac_address,
        fake_data.name,
        fake_data.token_needed,
        fake_data.power_consumption,
        fake_data.electric_current,
        fake_data.remaining_time,
        fake_data.auto_shutdown,
    ).is_equal_to("only water heaters are allowed")


def test_given_a_device_of_type_power_plug_when_instantiating_as_a_thermostatr_should_raise_an_error(fake_data):
    assert_that(SwitcherThermostat).raises(ValueError).when_called_with(
        DeviceType.POWER_PLUG,
        DeviceState.ON,
        fake_data.device_id,
        fake_data.device_key,
        fake_data.ip_address,
        fake_data.mac_address,
        fake_data.name,
        fake_data.token_needed,
        fake_data.mode,
        fake_data.temperature,
        fake_data.target_temperature,
        fake_data.fan_level,
        fake_data.swing,
        fake_data.remote_id
    ).is_equal_to("only thermostats are allowed")


def test_given_a_device_of_type_power_plug_when_instantiating_as_a_shutter_should_raise_an_error(fake_data):
    assert_that(SwitcherShutter).raises(ValueError).when_called_with(
        DeviceType.POWER_PLUG,
        DeviceState.ON,
        fake_data.device_id,
        fake_data.device_key,
        fake_data.ip_address,
        fake_data.mac_address,
        fake_data.name,
        fake_data.token_needed,
        fake_data.position,
        fake_data.direction,
        fake_data.child_lock
    ).is_equal_to("only shutters are allowed")


def test_given_a_device_of_type_power_plug_when_instantiating_as_a_single_shutter_dual_light_should_raise_an_error(fake_data):
    assert_that(SwitcherSingleShutterDualLight).raises(ValueError).when_called_with(
        DeviceType.POWER_PLUG,
        DeviceState.ON,
        fake_data.device_id,
        fake_data.device_key,
        fake_data.ip_address,
        fake_data.mac_address,
        fake_data.name,
        fake_data.token_needed,
        fake_data.position,
        fake_data.direction,
        fake_data.child_lock,
        fake_data.light2
    ).is_equal_to("only shutters with dual lights are allowed")


def test_given_a_device_of_type_power_plug_when_instantiating_as_a_dual_shutter_single_light_should_raise_an_error(fake_data):
    assert_that(SwitcherDualShutterSingleLight).raises(ValueError).when_called_with(
        DeviceType.POWER_PLUG,
        DeviceState.ON,
        fake_data.device_id,
        fake_data.device_key,
        fake_data.ip_address,
        fake_data.mac_address,
        fake_data.name,
        fake_data.token_needed,
        fake_data.position2,
        fake_data.direction2,
        fake_data.child_lock2,
        fake_data.light
    ).is_equal_to("only dual shutters with single lights are allowed")


def test_given_a_device_of_type_power_plug_when_instantiating_as_a_light_should_raise_an_error(fake_data):
    assert_that(SwitcherLight).raises(ValueError).when_called_with(
        DeviceType.POWER_PLUG,
        DeviceState.ON,
        fake_data.device_id,
        fake_data.device_key,
        fake_data.ip_address,
        fake_data.mac_address,
        fake_data.name,
        fake_data.token_needed,
        fake_data.light
    ).is_equal_to("only lights are allowed")
