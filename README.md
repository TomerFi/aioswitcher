# Switcher Boiler Bridge and API Tools
Python module for integrating with the [Switcher Water Heater](https://www.switcher.co.il/).</br>
This module was applicable thanks to the amazing R&D preformed by Shai and Aviad [here](https://github.com/NightRang3r/Switcher-V2-Python).</br>
This module is *AsyncIO* friendly and [*type-hinted*](https://www.python.org/dev/peps/pep-0484/), it requires the use of *Python 3.5* or above.</br>
Supports Switcher V2 Only.

## Installation
```shell
pip install aioswitcher
```

## Requirements
```text
python 3.5+
```

## Hardware
```text
Switcher V2
```

## Usage
The package takes two separate approaches for the integration, you can use either one or mix them up.</br>
The first approach is running a separate thread as a bridge to the device, the thread will constantly watch for broadcast messages from the device and run thread-safe coroutines for creation or update of the device.</br>

### Threaded Bridge
In this approach, we run a loop which will constantly listen for the device's broadcast message.</br>
When initiating the bridge, two callables are needed to be passed as callback arguments to the bridge,</br>
The first callback will be called upon arrival of the first broadcast message, the second callable will be called upon any new broadcast message arriving implicating of a change of the device state and status.</br>
Basically, use the first callback for creating the object representing the device, use the second callback for updating the device state and status.</br>
- Both callbacks will pass the [SwitcherV2Device](#switcherv2device) as an argument.
- Both callback will run a thread-safe coroutine within the asyncio event loop passed to the bridge as an argument.

Please Note: this approach will allow you to receive *Real-Time* updates from the device approximately every 4 seconds, yet it will not allow you to control the device, for that you can use the API functions.</br>

#### Example of bridge usage
~~~python
import asyncio
from aioswitcher.devices import SwitcherV2Device
from aioswitcher.bridge import SwitcherV2Thread


async def initial_device_cb(
    device_data: SwitcherV2Device) -> None:
    """Use for the initial device creation."""
    
    return None

async def update_device_cb(
    device_data: SwitcherV2Device) -> None:
    """Use for the update of the device data."""
    
    return None

your_loop = asyncio.get_event_loop()

# Instruction on getting this data is in,
# https://github.com/NightRang3r/Switcher-V2-Python
phone_id = "your_devices's_phone_id"
device_id = "your_devices's_device_id"
device_password = "your_devices's_device_password"

# There are two optional arguments for the bridge,
# in the following order:
# thread_name, for setting the thread name, default is "SwitcherV2Bridge".
# is_daemon, for setting the daemon property of the thread, default is True.
v2bridge = SwitcherV2Thread(
            phone_id, device_id, device_password, initial_device_cb,
            update_device_cb, your_loop)

# Start the thread
v2bridge.start()

"""Run your app or do what ever you need to keep in running here."""


# Join is only mandatory if the thread's daemon property is set to False.
v2bridge.join(timeout=2)

try:
    # Gracefully stop the bridge (2 seconds timeout is more the enough)
    your_loop.run_until_complete(
        asyncio.wait_for(v2bridge.stop(), timeout=2))
except asyncio.TimeoutError:
    pass

your_loop.close()

~~~

### Loosely coupled API functions
The second approach is basically a loosely coupled set of API functions that will allow you to:
- Get the device status
- Control the device
- Get the schedules from the device
- Set the device name
- Set the device Auto-Off configuration
- Create/Delete/Enable/Disable schedules on the device.

The responses of the functions is covered in the [API Response Messages](#api-response-messages) section.

#### Example of API usage
~~~python
import asyncio
import aioswitcher.swapi
from aioswitcher.consts import COMMAND_ON, COMMAND_OFF
from datetime import timedelta


your_loop = asyncio.get_event_loop()

# Instruction on getting this data is in,
# https://github.com/NightRang3r/Switcher-V2-Python
ip_address = "your_device's_ip_address"
phone_id = "your_devices's_phone_id"
device_id = "your_devices's_device_id"
device_password = "your_devices's_device_password"

async get_api_responses():
"""Run from the event loop to retirieve the api responses"""
    # returns the SwitcherV2StateResponseMSG response
    get_state_response = await swapi.get_state_of_device(
        ip_address, phone_id, device_id, device_password)

    # returns the SwitcherV2ControlResponseMSG response
    get_turn_on_response = await swapi.send_command_to_device(
        ip_address, phone_id, device_id, device_password,
        COMMAND_ON)   # turn-on
    get_turn_off_response = await swapi.send_command_to_device(
        ip_address, phone_id, device_id, device_password,
        COMMAND_OFF)   # turn-off
    get_turn_on_timer_response = await swapi.send_command_to_device(
        ip_address, phone_id, device_id, device_password,
        COMMAND_ON, "30")   # turn-on with a 30 minutes timer

    # return the SwitcherV2SetAutoOffResponseMSG response
    get_set_auto_off_response = await swapi.set_auto_off_to_device(
        ip_address, phone_id, device_id, device_password,
        timedelta(hours=1, minutes=30))  # set the auto-off to one hour and 30 minutes

your_loop.run_until_complete(
    swapi.get_state_of_device(get_api_responses)

your_loop.close()
~~~

## Objects and Properties
The are two main object you need to know about:</br>
The first object is the one representing the device, [aioswitcher/devices/SwitcherV2Device](https://github.com/TomerFi/aioswitcher/blob/master/aioswitcher/devices.py#L7).</br>
The second object is the one representing the device's schedule, [aioswitcher/schedules/SwitcherV2Schedule](https://github.com/TomerFi/aioswitcher/blob/master/aioswitcher/schedules.py#L10).</br>

### SwitcherV2Device

### SwitcherV2Schedule

### API Response Messages
The following are the response message objects returning from the API functions.

from aioswitcher.packets.messages

#### SwitcherV2StateResponseMSG

#### SwitcherV2ControlResponseMSG

#### SwitcherV2SetAutoOffResponseMSG

#### SwitcherV2UpdateNameResponseMSG

#### SwitcherV2GetScheduleResponseMSG

#### SwitcherV2DisableEnableScheduleResponseMSG

#### SwitcherV2DeleteScheduleResponseMSG

#### SwitcherV2CreateScheduleResponseMSG
