Usage
*****

This module provides two separate integrations with the Switcher device, both fully asynchronous.

The first integration is a `UDP Bridge`_ constantly listening to broadcast messages launched from
the device approximately every 4 seconds. This integration provides constant device state updates.

The second integration is a `TCP Socket API`_ providing the ability, to not only get the current
state of the device, but also control it.

.. contents:: TOC
   :local:
   :depth: 2

UDP Bridge
^^^^^^^^^^

With the `UDP Bridge`_ integration, we're constantly listening to messages broadcast from the
device containing information about the device and the device's state.

The message is being broadcast from the device approximately every 4 seconds,
once the message is received and verified it will be ``put`` in a `asyncio.Queue`_ with the max
size of 1, which means the ``Queue`` always has ``1`` or ``None``  messages waiting, containing the
latest state received.

Each message will be an updated instance of the SwitcherV2Device_ object.

The bridge can be used as a ``Context Manager`` as well as being instantiated and controlled
manually.

.. note::

   The `UDP Bridge`_ integration will allow you to receive **Real-Time** updates from the device
   approximately every 4 seconds, yet it will not allow you to control the device.

   For controlling the device you can use the `TCP Socket API`_ integration. (Both work
   simultaneously).

Example of UDP Bridge usage
---------------------------

.. code-block:: python

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
           your_loop, phone_id, device_id, device_password
       )
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

       # stop the bridge
       await v2bridge.stop()

       return None

   """Use as context manager."""
   async def run_as_context_manager() -> None:
       async with SwitcherV2Bridge(
           your_loop,
           phone_id,
           device_id,
           device_password,
       ) as v2bridge:
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

TCP Socket API
^^^^^^^^^^^^^^

With `TCP Socket API`_ integration we gain the following abilities:

.. hlist::
   :columns: 1

   * Get the device status
   * Control the device
   * Get the schedules from the device
   * Set the device name
   * Set the device Auto-Off configuration
   * Create/Delete/Enable/Disable schedules on the device.

.. note::
   Although the `TCP Socket API`_ is applicable as a ``context manager`` and as an instance of an
   object, It is preferable to use it as a ``context manager`` due to the nature of the
   ``tcp connection`` (you don't want to occupy a connection slot on the device any longer then you
   have to or you'll start seeing ``TimeOutErrors``).

   To use as an instance (which will not be covered here), you can rely on the ``UDP Bridge``
   example and just substitute ``start()`` and ``stop()`` with ``connect()`` and ``disconnect()``.

The various responses are covered in the `API Response Messages`_ section.

Example of TCP Socket API usage
-------------------------------

.. code-block:: python

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
           #
           # the following will enable the schedule:
           # updated_schedule_data = (
           #    schedule_data[0:2] + consts.ENABLE_SCHEDULE + schedule_data[4:])
           #
           # the following will disable the schedule:
           # updated_schedule_data = (
           #    schedule_data[0:2] + consts.DISABLE_SCHEDULE + schedule_data[4:])
           enable_disable_response = await swapi.disable_enable_schedule(
               updated_schedule_data)

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

Objects and Properties
^^^^^^^^^^^^^^^^^^^^^^

There are two main objects you need to be aware of:

*  The first object is the one representing the device itself,
   ``aioswitcher.devices.SwitcherV2Device`` SwitcherV2Device_.

*  The second object is the one representing the device's schedule,
   ``aioswitcher.schedules.SwitcherV2Schedule`` SwitcherV2Schedule_.

SwitcherV2Device
----------------

+-----------------------+--------------+----------------+---------------------+------------------+
| Property              | Type         | Description    | Possible Values     | Default Value    |
+=======================+==============+================+=====================+==================+
| **device_id**         | ``str``      | Return the     | ab1c2d              |                  |
|                       |              | device id.     |                     |                  |
+-----------------------+--------------+----------------+---------------------+------------------+
| **ip_addr**           | ``str``      | Return the     | 192.168.100.157     | waiting_for_data |
|                       |              | ip address.    |                     |                  |
+-----------------------+--------------+----------------+---------------------+------------------+
| **mac_addr**          | ``str``      | Return the mac | A1:B2:C3:45:67:D8   | waiting_for_data |
|                       |              | address.       |                     |                  |
+-----------------------+--------------+----------------+---------------------+------------------+
| **name**              | ``str``      | Return the     | device name         | waiting_for_data |
|                       |              | device name.   |                     |                  |
+-----------------------+--------------+----------------+---------------------+------------------+
| **state**             | ``str``      | Return the     | on, off             |                  |
|                       |              | device state.  |                     |                  |
+-----------------------+--------------+----------------+---------------------+------------------+
| **remaining_time**    | ``str``      | Return the     | %H:%M:%S            | waiting_for_data |
|                       |              | auto-off       |                     |                  |
|                       |              | configuration  |                     |                  |
|                       |              | value.         |                     |                  |
+-----------------------+--------------+----------------+---------------------+------------------+
| **auto_off_set**      | ``str``      | Return the     | %H:%M:%S            | waiting_for_data |
|                       |              | time left to   |                     |                  |
|                       |              | auto-off.      |                     |                  |
+-----------------------+--------------+----------------+---------------------+------------------+
| **power_consumption** | ``int``      | Return the     | 2780                | 0                |
|                       |              | power          |                     |                  |
|                       |              | consumption in |                     |                  |
|                       |              | watts.         |                     |                  |
+-----------------------+--------------+----------------+---------------------+------------------+
| **electric_current**  | ``float``    | Return the     | 12.8                | 0.0              |
|                       |              | power          |                     |                  |
|                       |              | consumption in |                     |                  |
|                       |              | amps.          |                     |                  |
+-----------------------+--------------+----------------+---------------------+------------------+
| **phone_id**          | ``str``      | Return the the | 1234                |                  |
|                       |              | phone id.      |                     |                  |
+-----------------------+--------------+----------------+---------------------+------------------+
| **last_data_update**  | ``datetime`` | Return the     | %Y-%m-%dTH:%M:%S.%F |                  |
|                       |              | timestamp of   |                     |                  |
|                       |              | the last       |                     |                  |
|                       |              | update.        |                     |                  |
+-----------------------+--------------+----------------+---------------------+------------------+
| **last_state_change** | ``datetime`` | Return the     | %Y-%m-%dTH:%M:%S.%F |                  |
|                       |              | timestamp of   |                     |                  |
|                       |              | the last       |                     |                  |
|                       |              | state change.  |                     |                  |
+-----------------------+--------------+----------------+---------------------+------------------+

SwitcherV2Schedule
------------------

+-------------------+--------------------+---------------+---------------------+------------------+
| Property          | Type               | Description   | Possible Values     | Default          |
+===================+====================+===============+=====================+==================+
| **schedule_id**   | ``str``            | Return the    | 0-7                 |                  |
|                   |                    | schedule id.  |                     |                  |
+-------------------+--------------------+---------------+---------------------+------------------+
| **enabled**       | ``bool``           | Return true   | True, False         | False            |
|                   |                    | if enabled.   |                     |                  |
|                   |                    |               |                     |                  |
|                   |                    | Has a setter  |                     |                  |
|                   |                    | manipulating  |                     |                  |
|                   |                    | the schedule  |                     |                  |
|                   |                    | status.       |                     |                  |
+-------------------+--------------------+---------------+---------------------+------------------+
| **recurring**     | ``bool``           | Return true   | True, False         | False            |
|                   |                    | if recurring. |                     |                  |
+-------------------+--------------------+---------------+---------------------+------------------+
| **days**          | ``List[str]``      | Return the    | -  Sunday           |                  |
|                   |                    | weekdays of   | -  Monday           |                  |
|                   |                    | the schedule. | -  Tuesday          |                  |
|                   |                    |               | -  Wednesday        |                  |
|                   |                    |               | -  Thursday         |                  |
|                   |                    |               | -  Friday           |                  |
|                   |                    |               | -  Saturday         |                  |
|                   |                    |               | -  **Every day**    |                  |
+-------------------+--------------------+---------------+---------------------+------------------+
| **start_time**    | ``str``            | Return the    | %H:%M               | waiting_for_data |
|                   |                    | start time of |                     |                  |
|                   |                    | the schedule. |                     |                  |
+-------------------+--------------------+---------------+---------------------+------------------+
| **end_time**      | ``str``            | Return the    | %H:%M               | waiting_for_data |
|                   |                    | end time of   |                     |                  |
|                   |                    | the schedule. |                     |                  |
+-------------------+--------------------+---------------+---------------------+------------------+
| **duration**      | ``str``            | Return the    | 0:30:00             | waiting_for_data |
|                   |                    | duration time |                     |                  |
|                   |                    | of the        |                     |                  |
|                   |                    | schedule.     |                     |                  |
+-------------------+--------------------+---------------+---------------------+------------------+
| **schedule_data** | ``str``            | Return the    | Any                 | waiting_for_data |
|                   |                    | schedule data |                     |                  |
|                   |                    | for managing  |                     |                  |
|                   |                    | the schedule. |                     |                  |
|                   |                    |               |                     |                  |
|                   |                    | has a setter  |                     |                  |
|                   |                    | manipulating  |                     |                  |
|                   |                    | the schedule  |                     |                  |
|                   |                    | data.         |                     |                  |
+-------------------+--------------------+---------------+---------------------+------------------+
| **init_future**   | ``asyncio.Future`` | Return the    | SwitcherV2Schedule  |                  |
|                   |                    | future of the |                     |                  |
|                   |                    | init.         |                     |                  |
+-------------------+--------------------+---------------+---------------------+------------------+


API Response Messages
^^^^^^^^^^^^^^^^^^^^^

The following are the response message objects returning from the various API functions.
The source of the responses can be found ``aioswitcher.api.messages``.

Please note the ``aioswitcher.api.messagesResponseMessageType`` *Enum Class* for identifying the
response message types:

.. hlist::
   :columns: 4

   * *AUTO_OFF*
   * *CONTROL*
   * *CREATE_SCHEDULE*
   * *DELETE_SCHEDULE*
   * *DISABLE_ENABLE_SCHEDULE*
   * *GET_SCHEDULES*
   * *STATE*
   * *UPDATE_NAME*

SwitcherV2BaseResponseMSG
-------------------------

+-----------------------+-------------------------+---------------------------------------+
| Property              | Type                    | Description                           |
+=======================+=========================+=======================================+
| **unparsed_response** | ``bytes``               | Return the unparsed response message. |
+-----------------------+-------------------------+---------------------------------------+
| **successful**        | ``bool``                | Return the status of the message.     |
+-----------------------+-------------------------+---------------------------------------+
| **msg_type**          | ``ResponseMessageType`` | Return the response message type.     |
+-----------------------+-------------------------+---------------------------------------+

SwitcherV2StateResponseMSG
--------------------------

:Extends: SwitcherV2BaseResponseMSG_

:Response Type: ``ResponseMessageType.STATE``

+-----------------+---------------------+-----------------------------------------------------+
| Property        | Type                | Description                                         |
+=================+=====================+=====================================================+
| **state**       | ``str``             | Return the state. Possible values are:              |
|                 |                     |                                                     |
|                 |                     |    * ``aioswitcher.consts.STATE_ON``                |
|                 |                     |    * ``aioswitcher.consts.STATE_OFF``               |
+-----------------+---------------------+-----------------------------------------------------+
| **time_left**   | ``str``             | Return the time left to auto-off.                   |
+-----------------+---------------------+-----------------------------------------------------+
| **auto_off**    | ``str``             | Return the auto-off configuration value.            |
+-----------------+---------------------+-----------------------------------------------------+
| **power**       | ``Optional[int]``   | Return the current power consumption in watts.      |
+-----------------+---------------------+-----------------------------------------------------+
| **current**     | ``Optional[float]`` | Return the power consumption in amps.               |
+-----------------+---------------------+-----------------------------------------------------+
| **init_future** | ``asyncio.Future``  | Return the future of the initialization.            |
|                 |                     |                                                     |
|                 |                     | As the initialization of this message requires some |
|                 |                     | asynchronous actions, please use                    |
|                 |                     | ``init_future.result()`` to get the message object. |
+-----------------+---------------------+-----------------------------------------------------+

SwitcherV2ControlResponseMSG
----------------------------

:Extends: SwitcherV2BaseResponseMSG_

:Response Type: ``ResponseMessageType.CONTROL``

::

   No properties are added by object.

SwitcherV2SetAutoOffResponseMSG
-------------------------------

:Extends: SwitcherV2BaseResponseMSG_

:Response Type: ``ResponseMessageType.AUTO_OFF``

::

   No properties are added by object.

SwitcherV2UpdateNameResponseMSG
-------------------------------

:Extends: SwitcherV2BaseResponseMSG_

:Response Type: ``ResponseMessageType.UPDATE_NAME``

::

   No properties are added by object.

SwitcherV2GetScheduleResponseMSG
--------------------------------

:Extends: SwitcherV2BaseResponseMSG_

:Response Type: ``ResponseMessageType.GET_SCHEDULES``

+---------------------+------------------------------+---------------------------------------+
| Property            | Type                         | Description                           |
+=====================+==============================+=======================================+
| **found_schedules** | ``bool``                     | Return true if found schedules in the |
|                     |                              | response.                             |
+---------------------+------------------------------+---------------------------------------+
| **get_schedules**   | ``List[SwitcherV2Schedule]`` | Return a list of SwitcherV2Schedule_. |
+---------------------+------------------------------+---------------------------------------+

SwitcherV2DisableEnableScheduleResponseMSG
------------------------------------------

:Extends: SwitcherV2BaseResponseMSG_

:Response Type: ``ResponseMessageType.DISABLE_ENABLE_SCHEDULE``

::

   No properties are added by object.

SwitcherV2DeleteScheduleResponseMSG
-----------------------------------

:Extends: SwitcherV2BaseResponseMSG_

:Response Type: ``ResponseMessageType.DELETE_SCHEDULE``

::

   No properties are added by object.

SwitcherV2CreateScheduleResponseMSG
-----------------------------------

:Extends: SwitcherV2BaseResponseMSG_

:Response Type: ``ResponseMessageType.CREATE_SCHEDULE``

::

   No properties are added by object.

.. _asyncio.Queue: https://docs.python.org/3.5/library/asyncio-queue.html#queue
