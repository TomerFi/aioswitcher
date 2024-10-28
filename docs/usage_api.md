The following excerpts are examples of using the API to control the various devices.

## Power plug excerpt

```python
import asyncio
from aioswitcher.api import Command, SwitcherApi
from aioswitcher.device import DeviceType

async def control_power_plug(device_type, device_ip, device_id, device_key) :
    # for connecting to a device we need its type, id, login key and ip address
    async with SwitcherApi(device_type, device_ip, device_id, device_key) as api:
        # get the device current state
        await api.get_state()
        # turn the device on
        await api.control_device(Command.ON)
        # turn the device off
        await api.control_device(Command.OFF)
        # set the device name to 'my new name'
        await api.set_device_name("my new name")

asyncio.run(control_power_plug(DeviceType.POWER_PLUG, "111.222.11.22", "ab1c2d", "00"))
```

## Water heater excerpt

```python
import asyncio
from datetime import timedelta
from aioswitcher.api import Command, SwitcherApi
from aioswitcher.device import DeviceType
from aioswitcher.schedule import Days

async def control_water_heater(device_type, device_ip, device_id, device_key):
    # for connecting to a device we need its type, id, login key and ip address
    async with SwitcherApi(device_type, device_ip, device_id, device_key) as api:
        # get the device current state
        await api.get_state()
        # turn the device on for 15 minutes
        await api.control_device(Command.ON, 15)
        # turn the device off
        await api.control_device(Command.OFF)
        # set the device name to 'my new name'
        await api.set_device_name("my new name")
        # configure the device for 02:30 auto shutdown
        await api.set_auto_shutdown(timedelta(hours=2, minutes=30))
        # get the schedules from the device
        await api.get_schedules() # (6)
        # delete and existing schedule with id 1
        await api.delete_schedule("1")
        # create a new recurring schedule for 13:00-14:30
        # executing on sunday and friday
        await api.create_schedule("13:00", "14:30", {Days.SUNDAY, Days.FRIDAY})

asyncio.run(control_water_heater(DeviceType.MINI, "111.222.11.22", "ab1c2d" , "00"))
asyncio.run(control_water_heater(DeviceType.TOUCH, "111.222.11.22", "ab1c2d" , "00"))
asyncio.run(control_water_heater(DeviceType.V2_ESP, "111.222.11.22", "ab1c2d" , "00"))
asyncio.run(control_water_heater(DeviceType.V2_QCA, "111.222.11.22", "ab1c2d" , "00"))
asyncio.run(control_water_heater(DeviceType.V4, "111.222.11.22", "ab1c2d" , "00"))
```

## Runner device excerpt

```python
import asyncio
from aioswitcher.api import SwitcherApi
from aioswitcher.device import DeviceState, DeviceType

async def control_runner(device_type, device_ip, device_id, device_key, token) :
    # for connecting to a device we need its type, id, login key and ip address
    async with SwitcherApi(device_type, device_ip, device_id, device_key, token) as api:
        # get the shutter current state, circuit number is 0
        await api.get_shutter_state(0)
        # open the shutter to 30%, circuit number is 0
        await api.set_position(30, 0)
        # stop the shutter if currently rolling, circuit number is 0
        await api.stop_shutter(0)
        # turn on the light, circuit number is 0 (Only for Runner S11 and Runner S12)
        await api.set_light(DeviceState.ON, 0)
        # turn off the light, circuit number is 0 (Only for Runner S11 and Runner S12)
        await api.set_light(DeviceState.OFF, 0)

asyncio.run(control_runner(DeviceType.RUNNER, "111.222.11.22", "ab1c2d", "00"))
asyncio.run(control_runner(DeviceType.RUNNER_MINI, "111.222.11.22", "ab1c2d", "00"))
asyncio.run(control_runner(DeviceType.RUNNER_S11, "111.222.11.22", "ab1c2d", "00", "zvVvd7JxtN7CgvkD1Psujw=="))
asyncio.run(control_runner(DeviceType.RUNNER_S12, "111.222.11.22", "ab1c2d", "00", "zvVvd7JxtN7CgvkD1Psujw=="))
```

## Breeze device excerpt

```python
import asyncio
from aioswitcher.api import SwitcherApi
from aioswitcher.api.remotes import SwitcherBreezeRemoteManager
from aioswitcher.device import DeviceState, DeviceType, ThermostatFanLevel, ThermostatMode, ThermostatSwing

async def control_breeze(device_type, device_ip, device_id, device_key, remote_manager, remote_id) :
    # for connecting to a device we need its type, id, login key and ip address
    async with SwitcherApi(device_type, device_ip, device_id, device_key) as api:
        # get the device current state
        await api.get_breeze_state()
        # initialize the Breeze RemoteManager and get the remote
        remote = remote_manager.get_remote(remote_id)
        # prepare a control command that turns on the Breeze
        # set to 24 degree (Celsius) cooling with vertical swing
        # send command to the device
        await api.control_breeze_device(
            remote,
            DeviceState.ON,
            ThermostatMode.COOL,
            24,
            ThermostatFanLevel.MEDIUM,
            ThermostatSwing.ON,
        )

# create the remote manager outside the context for re-using
remote_manager = SwitcherBreezeRemoteManager()
asyncio.run(control_breeze(DeviceType.BREEZE, "111.222.11.22", "ab1c2d", "00", remote_manager, "DLK65863"))
```

## Light switch excerpt

```python
import asyncio
from aioswitcher.api import SwitcherApi
from aioswitcher.device import DeviceState, DeviceType

async def control_light(device_type, device_ip, device_id, device_key, token) :
    # for connecting to a device we need its type, id, login key and ip address
    async with SwitcherApi(device_type, device_ip, device_id, device_key, token) as api:
        # get the light current state, circuit number is 0
        await api.get_light_state(0)
        # turn on the light, circuit number is 0 (Only for Runner S11, Runner S12 and Lights)
        await api.set_light(DeviceState.ON, 0)
        # turn off the light, circuit number is 0 (Only for Runner S11, Runner S12 and Lights)
        await api.set_light(DeviceState.OFF, 0)

asyncio.run(control_light(DeviceType.LIGHT_SL01, "111.222.11.22", "ab1c2d", "00", "zvVvd7JxtN7CgvkD1Psujw=="))
asyncio.run(control_light(DeviceType.LIGHT_SL01_MINI, "111.222.11.22", "ab1c2d", "00", "zvVvd7JxtN7CgvkD1Psujw=="))
asyncio.run(control_light(DeviceType.LIGHT_SL02, "111.222.11.22", "ab1c2d", "00", "zvVvd7JxtN7CgvkD1Psujw=="))
asyncio.run(control_light(DeviceType.LIGHT_SL02_MINI, "111.222.11.22", "ab1c2d", "00", "zvVvd7JxtN7CgvkD1Psujw=="))
asyncio.run(control_light(DeviceType.LIGHT_SL03, "111.222.11.22", "ab1c2d", "00", "zvVvd7JxtN7CgvkD1Psujw=="))
```
