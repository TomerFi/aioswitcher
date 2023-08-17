from aioswitcher.api import SwitcherType1Api, SwitcherType2Api, Command
import asyncio

from aioswitcher.device import DeviceType

async def control_power_plug(device_type, device_ip, device_id) :
    # for connecting to a device we need its id and ip address
    async with SwitcherType1Api(device_type, device_ip, device_id) as api:
        # get the device current state
        await api.get_state()
        # turn the device on
        await api.control_device(Command.ON)
        # turn the device off
        await api.control_device(Command.OFF)
        # set the device name to 'my new name'
        await api.set_device_name("my new name")

async def control_runner(device_type, device_ip, device_id, token) :
    # for connecting to a device we need its id and ip address
    async with SwitcherType2Api(device_type, device_ip, device_id, token) as api:
        # get the device current state (1)
        await api.get_shutter_state()
        # open the shutter to 30%, shutter id is 3 (2)
        await api.set_position(30, 3)
        # stop the shutter if currently rolling, shutter id is 3 (3)
        await api.stop_shutter(3)

asyncio.run(
    control_power_plug(DeviceType.POWER_PLUG, "111.222.11.22", "ab1c2d")
)

asyncio.run(
    control_runner(DeviceType.RUNNER, "111.222.11.22", "ab1c2d", "")
)

asyncio.run(
    control_runner(DeviceType.RUNNER_MINI, "111.222.11.22", "ab1c2d", "")
)

asyncio.run(
    control_runner(DeviceType.RUNNER_S11, "111.222.11.22", "ab1c2d", "zvVvd7JxtN7CgvkD1Psujw==")
)

asyncio.run(
    control_runner(DeviceType.RUNNER_S12, "111.222.11.22", "ab1c2d", "zvVvd7JxtN7CgvkD1Psujw==")
)

