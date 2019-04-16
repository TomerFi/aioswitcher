
# Switcher Boiler Bridge and API Tools

[![PyPI version](https://badge.fury.io/py/aioswitcher.svg)](https://badge.fury.io/py/aioswitcher) 
[![Build Status](https://travis-ci.org/TomerFi/aioswitcher.svg?branch=unit-tests)](https://travis-ci.org/TomerFi/aioswitcher) 
[![Coverage Status](https://coveralls.io/repos/github/TomerFi/aioswitcher/badge.svg?branch=unit-tests)](https://coveralls.io/github/TomerFi/aioswitcher?branch=unit-tests) 
[![codecov](https://codecov.io/gh/TomerFi/aioswitcher/branch/master/graph/badge.svg)](https://codecov.io/gh/TomerFi/aioswitcher) 


Python module for integrating with the [Switcher Water Heater](https://www.switcher.co.il/).</br>
This module was applicable thanks to the amazing R&D performed by Shai and Aviad [here](https://github.com/NightRang3r/Switcher-V2-Python).</br>
This module is *Asyncio* friendly [*static-typed*](https://www.python.org/dev/peps/pep-0484/), it requires the use of *Python 3.5* or above.</br>
Tested with the Switcher V2 Only.

## Current version
```text
2019.3.21
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
This module provides two separate integrations with the Switcher device, both fully asynchronous.</br>
The first integration is a `UDP Bridge`constantly listening to broadcast messages launched from the device every approximately 4 seconds. This integration provides constant device state updates.</br>
The second integration is a `TCP Socket API`providing the ability to not only get the state of the device, but also control it.</br>

### UDP Bridge
In this integration, we're constantly listening to messages broadcast from the device and containing information about the device and the device's state.</br>
The message is being broadcast from the device approximately every 4 seconds, once the message is recieved and verified it will be `put` in an [asyncio.Queue](https://docs.python.org/3.5/library/asyncio-queue.html#queue) with max size of 1, which means the `Queue` always has `1` or `None`  messages waiting, each message will be an updated instance of the [SwitcherV2Device](#switcherv2device) object.</br>

The bridge can be used as a `Context Manager` as well as being instantiated and controlled manually.

Please Note: this integration will allow you to receive *Real-Time* updates from the device approximately every 4 seconds, yet it will not allow you to control the device, for that you can use the API integration.</br>

#### Example of UDP Bridge usage
~~~python
import asyncio
from datetime import datetime
from aioswitcher.bridge import SwitcherV2Bridge
from aioswitcher.devices import SwitcherV2Device

# instructions on getting this data is in,
# https://github.com/NightRang3r/Switcher-V2-Python
phone_id = "your_devices's_phone_id"
device_id = "your_devices's_device_id"
device_password = "your_devices's_device_password"

# create a new event loop
your_loop = asyncio.get_event_loop()

"""Use as instance."""
async def run_as_instance() -> None:
    v2bridge = SwitcherV2Bridge(
        your_loop, phone_id, device_id, device_password)
    # start the bridge
    await v2bridge.start()

    # get the Queue
    queue = v2bridge.queue  # type: asyncio.Queue

    # create an event to signal your coroutine to start/stop
    signal_event = asyncio.Event()
    signal_event.set()

    # coroutine for getting the device from the queue
    async def get_device_from_queue() -> None:
        device = await queue.get()  # type: SwitcherV2Device
        print("instance state is: {}".format(device.state))
        print(datetime.now())
        if signal_event.is_set():
            your_loop.call_soon(get_device_from_queue)
        return None

    # chedule your coroutine which will wait for the device
    # to be put in the queue, and print the time and its state
    # afterwards it will call itself again, the result will be
    # the device state being printed every approximately 4 seconds
    your_loop.call_soon(get_device_from_queue)

    # wait for 40 seconds
    # the state should be printed about 8 to 10 times
    await asyncio.sleep(40)

    # stop the coroutine
    signal_event.clear()

    # stop the bridge
    await v2bridge.stop()

    return None

"""Use as context manager."""
async def run_as_context_manager() -> None:
    async with SwitcherV2Bridge(
            your_loop, phone_id, device_id,
            device_password) as v2bridge:
        # get the Queue
        queue = v2bridge.queue  # type: asyncio.Queue

        # create an event to signal your coroutine to start/stop
        signal_event = asyncio.Event()
        signal_event.set()

        # coroutine for getting the device from the queue
        async def get_device_from_queue() -> None:
            device = await queue.get()  # type: SwitcherV2Device
            print("context manager state is: {}".format(device.state))
            print(datetime.now())
            if signal_event.is_set():
                your_loop.call_soon(get_device_from_queue)
            return None

        # schedule your coroutine which will wait for the device
        # to be put in the queue, and print the time and its state
        # afterwards it will call itself again, the result will be
        # the device state being printed every approximately 4 seconds
        your_loop.call_soon(get_device_from_queue)

        # wait for 40 seconds
        # the state should be printed about 8 to 10 times
        await asyncio.sleep(40)

        # stop the coroutine
        signal_event.clear()

    return None

your_loop.run_until_complete(run_as_instance())
your_loop.run_until_complete(run_as_context_manager())

loop.close()

~~~

### TCP Socket API
This integration provides the following abilities:
- Get the device status
- Control the device
- Get the schedules from the device
- Set the device name
- Set the device Auto-Off configuration
- Create/Delete/Enable/Disable schedules on the device.</br>

Although this API is applicable as a `context manager` and as an instance of an object, it is preferable to use it as a `context manager` due to the nature of the `tcp` connection (you don't want to occupy a connection slot on the device any longer then you have to or you'll start seeing `TimeOutErrors`).</br>
For use as an instance (which will not be covered here), you can rely on the `UDP Bridge` example and substitute  `start()` and `stop()` with `connect()` and `disconnect()`.</br>

The various responses are covered in the [API Response Messages](#api-response-messages) section.

#### Example of TCP Socket API usage
~~~python
import asyncio
from datetime import timedelta
from aioswitcher import consts, tools
from aioswitcher.api import SwitcherV2Api, messages
from aioswitcher.schedules import SwitcherV2Schedule


# create a new event loop
your_loop = asyncio.get_event_loop()

# if you're also using the udp bridge,
# the ip address is available at (SwitcherV2Device).ip_addr
ip_address = "your_device's_ip_address"

# instructions on getting this data is in
# https://github.com/NightRang3r/Switcher-V2-Python
phone_id = "your_devices's_phone_id"
device_id = "your_devices's_device_id"
device_password = "your_devices's_device_password"

"""Use as context manager."""
async def run_as_context_manager() -> None:
    async with SwitcherV2Api(
            your_loop, ip_address, phone_id,
            device_id, device_password) as swapi:
        # get the device state
        # response: messages.SwitcherV2StateResponseMSG
        state_response = await swapi.get_state()

        # control the device: on / off / on + (15/30/45/60) minutes timer
        # response: messages.SwitcherV2ControlResponseMSG
        turn_on_response = await swapi.control_device(
            consts.COMMAND_ON)
        turn_off_response = await swapi.control_device(
            consts.COMMAND_OFF)
        turn_on_30_min_response = await swapi.control_device(
            consts.COMMAND_ON, '30')

        # set the limit time to auto-shutdown the device (1 < hours < 24)
        # response: messages.SwitcherV2SetAutoOffResponseMSG
        time_to_off = timedelta(hours=1, minutes=30)
        set_auto_off_response = await swapi.set_auto_shutdown(time_to_off)

        # set the device name (2 < length < 33)
        # response: messages.SwitcherV2UpdateNameResponseMSG
        set_name_response = await swapi.set_device_name("new device name")

        # get the configured schedules from the device
        # response: messages.SwitcherV2GetScheduleResponseMSG
        get_schedules_response = await swapi.get_schedules()

        # disable or enable a schedule
        # schedule_data = (SwitcherV2Schedule).schedule_data
        # response: messages.SwitcherV2DisableEnableScheduleResponseMSG
        enable_disable_response = await swapi.disable_enable_schedule(
            schedule_data)

        # delete a schedule (0 <= schedule_id <= 7)
        # schedule_id = (SwitcherV2Schedule).schedule_id
        # response: messages.SwitcherV2DeleteScheduleResponseMSG
        delete_response = await swapi.delete_schedule(schedule_id)

        # create a schedule to turn on at 20:30 and off at 21:00
        # response: messages.SwitcherV2CreateScheduleResponseMSG
        schedule_days = [0]
        # append selected days, if non-recurring skip next
        schedule_days.append(consts.DAY_TO_INT_DICT[consts.SUNDAY])
        schedule_days.append(consts.DAY_TO_INT_DICT[consts.MONDAY])
        schedule_days.append(consts.DAY_TO_INT_DICT[consts.TUESDAY])
        schedule_days.append(consts.DAY_TO_INT_DICT[consts.WEDNESDAY])
        schedule_days.append(consts.DAY_TO_INT_DICT[consts.THURSDAY])
        schedule_days.append(consts.DAY_TO_INT_DICT[consts.FRIDAY])
        schedule_days.append(consts.DAY_TO_INT_DICT[consts.SATURDAY])
        # skip here if non-recurring
        weekdays = await tools.create_weekdays_value(
            your_loop, schedule_days)
        start_time = await tools.timedelta_str_to_schedule_time(
            your_loop, str(timedelta(hours=20, minutes=30)))
        end_time = await tools.timedelta_str_to_schedule_time(
            your_loop, str(timedelta(hours=21)))
        schedule_data = consts.SCHEDULE_CREATE_DATA_FORMAT.format(
            weekdays, start_time, end_time)
        create_response = await swapi.create_schedule(schedule_data)

    return None

your_loop.run_until_complete(run_as_context_manager())

your_loop.close()

~~~

## Objects and Properties
There are two main objects you need to be aware of:</br>
The first object is the one representing the device, [aioswitcher/devices/SwitcherV2Device](aioswitcher/devices.py#L7).</br>
The second object is the one representing the device's schedule, [aioswitcher/schedules/SwitcherV2Schedule](aioswitcher/schedules.py#L12).</br>

### SwitcherV2Device
| Property | Type | Description | Possible Values | Default |
| -------- | ---- | ----------- | --------------- | ------- |
| *device_id* | `str` | Return the device id. | ab1c2d||
| *ip_addr* | `str` | Return the ip address. | 192.168.100.157 | waiting_for_data |
| *mac_addr* | `str` | Return the mac address. | A1:B2:C3:45:67:D8 | waiting_for_data |
| *name* | `str` | Return the device name. | device name | waiting_for_data |
| *state* | `str` | Return the device state. | on, off ||
| *remaining_time* | `str` | Return the auto-off configuration value. | %H:%M:%S | waiting_for_data|
| *auto_off_set* | `str` | Return the time left to auto-off. | %H:%M:%S | waiting_for_data |
| *power_consumption* | `int` | Return the power consumption in watts. | 2780 | 0 |
| *electric_current* | `float` | Return the power consumption in amps. | 12.8 | 0.0 |
| *phone_id* | `str ` | Return the the phone id. | 1234 ||
| *last_data_update* | `datetime` | Return the timestamp of the last update. | %Y-%m-%dTH:%M:%S.%F ||
| *last_state_change* | `datetime` | Return the timestamp of the state change. | %Y-%m-%dTH:%M:%S.%F ||


### SwitcherV2Schedule
| Property | Type | Description | Possible Values | Default |
| -------- | ---- | ----------- | --------------- | ------- |
| *schedule_id* | `str` | Return the schedule id. | 0, 1, 2, 3, 4, 5, 6, 7 ||
| *enabled* | `bool` | Return true if enabled. | True, False | False |
| *recurring* | `bool` | Return true if recurring. | True, False | False |
| *days* | `List[str]` | Return the weekdays of the schedule. | Sunday, Monday, Tuesday, Wednesday,  Thursday, Friday,  Saturday or **Every day** ||
| *start_time* | `str` | Return the start time of the schedule. | %H:%M | waiting_for_data |
| *end_time* | `str` | Return the end time of the schedule. | %H:%M | waiting_for_data |
| *duration* | `str` | Return the duration of the schedule. | 0:30:00 | waiting_for_data |
| *schedule_data* | `str` | Return the schedule data for managing the schedule. | Any | waiting_for_data |
| *init_future* | `asyncio.Future` | Return the future of the initialization. | SwitcherV2Schedule ||
- *enabled* has a setter for manipulating the schedule status.
- *schedule_data* has a setter for manipulating the schedule data.


### API Response Messages
The following are the response message objects returning from the API functions.
The source of the responses can be found [here](aioswitcher/api/messages.py).</br>
Please note the [ResponseMessageType](aioswitcher/api/messages.py#L15) *Enum Class* for identifying the response message types:
- *AUTO_OFF*
- *CONTROL*
- *CREATE_SCHEDULE*
- *DELETE_SCHEDULE*
- *DISABLE_ENABLE_SCHEDULE*
- *GET_SCHEDULES*
- *STATE*
- *UPDATE_NAME*

#### SwitcherV2BaseResponseMSG
| Property | Type | Description |
| -------- | ---- | ----------- |
| *unparsed_response* | `bytes` | Return the unparsed response message. |
| *successful* | `bool` | Return the status of the message. |
| *msg_type* | `ResponseMessageType` | Return the response message type. |

#### SwitcherV2StateResponseMSG (SwitcherV2BaseResponseMSG)
- *ResponseMessageType.STATE*
 
| Property | Type | Description |
| -------- | ---- | ----------- |
| *state* | `str` | Return the state. Values will be `STATE_ON` or `STATE_OFF` located in [aioswitcher.consts](aioswitcher/consts.py)  |
| *time_left* | `str` | Return the time left to auto-off. |
| *auto_off* | `str` | Return the auto-off configuration value. |
| *power* | `Optional[int]` | Return the current power consumption in watts. |
| *current* | `Optional[float]` | Return the power consumption in amps. |
| *init_future* | `asyncio.Future` | Return the future of the initialization. As the initiliazation of this message requires some asyncronous actions, please use `await init_future.result()` to get the message object. |

#### SwitcherV2ControlResponseMSG (SwitcherV2BaseResponseMSG)
- *ResponseMessageType.CONTROL*

#### SwitcherV2SetAutoOffResponseMSG (SwitcherV2BaseResponseMSG)
- *ResponseMessageType.AUTO_OFF*

#### SwitcherV2UpdateNameResponseMSG (SwitcherV2BaseResponseMSG)
- *ResponseMessageType.UPDATE_NAME*

#### SwitcherV2GetScheduleResponseMSG (SwitcherV2BaseResponseMSG)
- *ResponseMessageType.GET_SCHEDULES*

| Property | Type | Description |
| -------- | ---- | ----------- |
| *found_schedules* | `bool` | Return true if found schedules in the response. | 
| *get_schedules* | `List[SwitcherV2Schedule]` | Return a list of [SwitcherV2Schedule](#switcherv2schedule). |

#### SwitcherV2DisableEnableScheduleResponseMSG (SwitcherV2BaseResponseMSG)
- *ResponseMessageType.DISABLE_ENABLE_SCHEDULE*

#### SwitcherV2DeleteScheduleResponseMSG (SwitcherV2BaseResponseMSG)
- *ResponseMessageType.DELETE_SCHEDULE*

#### SwitcherV2CreateScheduleResponseMSG (SwitcherV2BaseResponseMSG)
- *ResponseMessageType.CREATE_SCHEDULE*
