#! python3

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

"""Python script for controlling Switcher devices using API."""

import asyncio

from aioswitcher.api import Command, SwitcherType1Api, SwitcherType2Api
from aioswitcher.device import DeviceType, LightState


async def control_power_plug(device_type, device_ip, device_id):
    """Control Power Plug."""
    # for connecting to a device we need its id and ip address
    async with SwitcherType1Api(device_type, device_ip, device_id) as api:
        # get the device current state
        print(await api.get_state())
        # turn the device on
        await api.control_device(Command.ON)
        # turn the device off
        await api.control_device(Command.OFF)
        # set the device name to 'my new name'
        await api.set_device_name("my new name")


async def control_runner(device_type, device_ip, device_id, token):
    """Control Runner."""
    # for connecting to a device we need its id and ip address
    async with SwitcherType2Api(device_type, device_ip, device_id, token) as api:
        # get the device current state (1)
        print(await api.get_shutter_state(1))
        # open the shutter to 30%, shutter id is 1
        await api.set_position(90, 1)
        # stop the shutter if currently rolling, shutter id is 1
        await api.stop_shutter(1)


async def control_runner_s11(device_type, device_ip, device_id, token):
    """Control Runner S11."""
    # for connecting to a device we need its id and ip address
    async with SwitcherType2Api(device_type, device_ip, device_id, token) as api:
        # get the device current state (1)
        print(await api.get_shutter_state(1))
        # turn on light, shutter id is 1
        await api.set_light(LightState.ON, 1)
        # turn on light, shutter id is 2
        await api.set_light(LightState.ON, 2)
        # turn off light, shutter id is 1
        await api.set_light(LightState.OFF, 1)
        # turn off light, shutter id is 2
        await api.set_light(LightState.OFF, 2)
        # open the shutter to 30%, shutter id is 1
        await api.set_position(90, 1)
        # stop the shutter if currently rolling, shutter id is 1
        await api.stop_shutter(1)


async def control_runner_s12(device_type, device_ip, device_id, token):
    """Control Runner S12."""
    # for connecting to a device we need its id and ip address
    async with SwitcherType2Api(device_type, device_ip, device_id, token) as api:
        # get the device current state (1)
        print(await api.get_shutter_state(1))
        # get the device current state (2)
        print(await api.get_shutter_state(2))
        # turn on light, shutter id is 1
        await api.set_light(LightState.ON, 1)
        # turn off light, shutter id is 1
        await api.set_light(LightState.OFF, 1)
        # open the shutter to 30%, shutter id is 1
        await api.set_position(100, 1)
        # open the shutter to 30%, shutter id is 2
        await api.set_position(100, 2)
        # stop the shutter if currently rolling, shutter id is 1
        await api.stop_shutter(1)
        # # stop the shutter if currently rolling, shutter id is 1
        await api.stop_shutter(2)


# Examples
asyncio.run(control_power_plug(DeviceType.POWER_PLUG, "111.222.11.22", "ab1c2d"))

asyncio.run(control_runner(DeviceType.RUNNER, "111.222.11.22", "ab1c2d", ""))

asyncio.run(control_runner(DeviceType.RUNNER_MINI, "111.222.11.22", "ab1c2d", ""))

asyncio.run(
    control_runner_s11(
        DeviceType.RUNNER_S11, "111.222.11.22", "ab1c2d", "zvVvd7JxtN7CgvkD1Psujw=="
    )
)

asyncio.run(
    control_runner_s12(
        DeviceType.RUNNER_S12, "111.222.11.22", "ab1c2d", "zvVvd7JxtN7CgvkD1Psujw=="
    )
)
