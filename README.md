# Switcher Boiler Bridge and API Tools
Python module for integrating with the [Switcher Water Heater](https://www.switcher.co.il/).</br>
This module was applicable thanks to the amazing R&D performed by Shai and Aviad [here](https://github.com/NightRang3r/Switcher-V2-Python).</br>
This module is *Asyncio* friendly and [*type-hinted*](https://www.python.org/dev/peps/pep-0484/), it requires the use of *Python 3.5* or above.</br>
Supports Switcher V2 Only.

## Current version
```text
0.2.2
```

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
The second approach is basically a set of loosely coupled functions for controlling the device. </br>

### Threaded bridge
In this approach, we run a loop which will constantly listen for the device's broadcast message.</br>
When initiating the bridge, two callables are needed to be passed as callback arguments to the bridge,</br>
The first callback will be called upon arrival of the first broadcast message, the second callable will be called upon any new broadcast message arriving implicating of a change of the device state and status.</br>
Basically, use the first callback for creating the object representing the device, use the second callback for updating the device state and status.</br>
- Both callbacks will pass the [SwitcherV2Device](#switcherv2device) as an argument.
- Both callbacks will run a thread-safe coroutine within the asyncio event loop passed to the bridge as an argument.

Please Note: this approach will allow you to receive *Real-Time* updates from the device approximately every 4 seconds, yet it will not allow you to control the device, for that you can use the API functions.</br>

#### Example of threaded bridge usage
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

"""Run your app or do whatever you need to keep in running here."""


# Join is only mandatory if the thread's daemon property is set to False.
v2bridge.join(timeout=2)

try:
    # Gracefully stop the bridge (2 seconds timeout is more then enough)
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
from aioswitcher.consts import (COMMAND_ON, COMMAND_OFF,
                                ENABLE_SCHEDULE, DISABLE_SCHEDULE,
                                SUNDAY, WEDNESDAY,
                                SCHEDULE_CREATE_DATA_FORMAT)
from aioswitcher.schedules import SwitcherV2Schedule
from aioswitcher import tools
from datetime import timedelta


your_loop = asyncio.get_event_loop()

# Instruction on getting this data is in,
# https://github.com/NightRang3r/Switcher-V2-Python
ip_address = "your_device's_ip_address"
phone_id = "your_devices's_phone_id"
device_id = "your_devices's_device_id"
device_password = "your_devices's_device_password"

async get_api_responses():
"""Run from the event loop to retrieve the api responses"""
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

    # returns the SwitcherV2SetAutoOffResponseMSG response
    get_set_auto_off_response = await swapi.set_auto_off_to_device(
        ip_address, phone_id, device_id, device_password,
        timedelta(hours=1, minutes=30))  # set the auto-off to one hour and 30 minutes

    # returns the SwitcherV2UpdateNameResponseMSG response
    get_set_name_response = await swapi.update_name_of_device(
        ip_address, phone_id, device_id, device_password,
        "new_name")  # set the device name to "new_name"

    # return the SwitcherV2GetScheduleResponseMSG response
    get_schedules_response = await swapi.get_schedules(
        ip_address, phone_id, device_id, device_password)  # set the device's schedules

    # returns the SwitcherV2DisableEnableScheduleResponseMSG response
    schedule_data = SwitcherV2Schedule.schedule_data  # grab from the schedule object instance
    updated_schedule_data = (schedule_data[0:2] + ENABLE_SCHEDULE + schedule_data[4:])  # Enable schedule
    # updated_schedule_data = (schedule_data[0:2] + DISABLE_SCHEDULE + schedule_data[4:])  # Disable schedule
    get_enable_disable_scheule_response = await swapi.disable_enable_schedule(
        ip_address, phone_id, device_id, device_password,
        updated_schedule_data)  # enable or disable a specific schedule

    # returns the SwitcherV2DeleteScheduleResponseMSG response
    schedule_id = SwitcherV2Schedule.schedule_id  # grab from the appropriate schedule object instance
    get_delete_scheudle_response = await swapi.delete_schedule(
        ip_address, phone_id, device_id, device_password,
        schedule_id)  # delete a specific schedule

    # returns the SwitcherV2CreateScheduleResponseMSG response
    requested_days = [0]

    # skip the next part for non-recurring schedules
    requested_days.append[SUNDAY]
    requested_days.append[WEDNESDAY]

    weekdays = tools.create_weekdays_value(requested_days)
    start_time = tools.timedelta_str_to_schedule_time("20:30")
    end_time = tools.timedelta_str_to_schedule_time("21:00")

    schedule_data = SCHEDULE_CREATE_DATA_FORMAT.format(
        weekdays, start_time, end_time)
    get_create_schedule_response = await swapi.create_schedule(
        ip_address, phone_id, device_id, device_password,
        schedule_data)  # create a new schedule running every Sunday and Wednesday from 20:30 to 21:00


your_loop.run_until_complete(get_api_responses())

your_loop.close()
~~~

## Objects and Properties
There are two main object you need to know about:</br>
The first object is the one representing the device, [aioswitcher/devices/SwitcherV2Device](https://github.com/TomerFi/aioswitcher/blob/master/aioswitcher/devices.py#L7).</br>
The second object is the one representing the device's schedule, [aioswitcher/schedules/SwitcherV2Schedule](https://github.com/TomerFi/aioswitcher/blob/master/aioswitcher/schedules.py#L10).</br>

### SwitcherV2Device properties
- **device_id** Returns a str value representing the unique identification of the device.
- **ip_addr** Returns a str value representing the ip address of the device.
- **mac_addr** Returns a str value representing the mac address of the device.
- **name** Returns a str value representing the name of the device.
- **state** Returns a str value representing the name of the device, possible values representation:
  - *aioswitcher.consts.STATE_ON*
  - *aioswitcher.consts.STATE_OFF*
- **remaining_time** Returns a str value representing the time left to off.
- **auto_off_set** Returns a str value representing the auto-off configuration set.
- **power_consumption** Returns an int value representing the current power consumption in watts.
- **electric_current** Returns a float value representing the electric current in amps.
- **phone_id** Returns a str value representing the device's phone id.
- **last_data_update** Return a datetime object representing the last update of the devices data.
- **last_state_change** Return a datetime object representing the last time the state has changed since running the code.

### SwitcherV2Schedule properties
- **schedule_id** Returns a str value representing the schedule id (0-7).
- **enabled** Returns a bool value representing rather or not the schedule is enabled (includes setter).
- **recurring** Return a bool value representing rather or not the schedule is a recurring schedule.
- **days** Returns a List of str values representing the week days in which the schedule is due to run, possible values representations are:
  - *aioswitcher.consts.MONDAY*
  - *aioswitcher.consts.TUESDAY*
  - *aioswitcher.consts.WEDNESDAY*
  - *aioswitcher.consts.THURSDAY*
  - *aioswitcher.consts.FRIDAY*
  - *aioswitcher.consts.SATURDAY*
  - *aioswitcher.consts.SUNDAY*
  - *aioswitcher.consts.ALL_DAYS*
- **start_time** Returns a str value representing the schedule start time in HH:MM format.
- **end_time** Returns a str value representing the schedule start time in HH:MM format.
- **duration** Returns a str value representing the schedule duration in minutes.
- **schedule_data** Returns a str value representing the schedule data from the Switcher device (includes setter).

### API Response Messages
The following are the response message objects returning from the API functions.
The source of the responses can be found [here](aioswitcher/packets/messages.py).

#### SwitcherV2StateResponseMSG properties
- **unparsed_response** Returns a bytes representation of the unparsed response.
- **successful** Returns a bool value indicating rather or not the request was successful.
- **state** Returns the state of the device, possible values representation:
  - *aioswitcher.consts.STATE_ON*
  - *aioswitcher.consts.STATE_OFF*
- **time_left** Returns a str value representing the time left on the device.
- **auto-off** Returns a str value representing the configured auto-off off the device.
- **power** Returns an int value representing the current power consumption in watts.
- **current** Returns a float value representing the electric current in amps.

#### SwitcherV2ControlResponseMSG properties
- **unparsed_response** Returns a bytes representation of the unparsed response.
- **successful** Returns a bool value indicating rather or not the request was successful.

#### SwitcherV2SetAutoOffResponseMSG properties
- **unparsed_response** Returns a bytes representation of the unparsed response.
- **successful** Returns a bool value indicating rather or not the request was successful.

#### SwitcherV2UpdateNameResponseMSG properties
- **unparsed_response** Returns a bytes representation of the unparsed response.
- **successful** Returns a bool value indicating rather or not the request was successful.

#### SwitcherV2GetScheduleResponseMSG properties
- **unparsed_response** Returns a bytes representation of the unparsed response.
- **successful** Returns a bool value indicating rather or not the request was successful.
- **found_schedules** Returns a bool value indicating rather or not any schedules were found on the device.
- **get_schedules** Return a List of [SwitcherV2Schedule](https://github.com/TomerFi/aioswitcher#switcherv2schedule) instances.</br>
*Please Note: The Switcher V2 device has only 8 schedules indexed from 0 to 7.*

#### SwitcherV2DisableEnableScheduleResponseMSG properties
- **unparsed_response** Returns a bytes representation of the unparsed response.
- **successful** Returns a bool value indicating rather or not the request was successful.

#### SwitcherV2DeleteScheduleResponseMSG properties
- **unparsed_response** Returns a bytes representation of the unparsed response.
- **successful** Returns a bool value indicating rather or not the request was successful.

#### SwitcherV2CreateScheduleResponseMSG properties
- **unparsed_response** Returns a bytes representation of the unparsed response.
- **successful** Returns a bool value indicating rather or not the request was successful.
