
# Usage

## Bridge

We can use the Bridge implementation to discover devices and their state.
The following code will print all discovered devices for 60 seconds.

```python
    async def print_devices(delay):
        def on_device_found_callback(device):
            print(asdict(device))

        async with SwitcherBridge(on_device_found_callback):
            await asyncio.sleep(delay)

    asyncio.get_event_loop().run_until_complete(print_devices(60))
```

!!!note
    A Switcher device will broadcast every 4 seconds.
    Discovered devices can either be a [Power Plug](./codedocs.md#switcherpowerplug) or a [Power Plug](./codedocs.md#switcherwaterheater)

## API

### Type1 API (Switcher Plug, V2, Touch, V4)

We can use the Type1 API to gain the following capabilities:

- Get the current state
- Turn on and off
- Set the name
- Configure auto shutdown
- Retrieve the schedules
- Create and Delete schedules

```python
    async def control_device(device_ip, device_id) :
        # for connecting to a device we need its id and ip address
        async with SwitcherType1Api(device_ip, device_id) as api:
            # get the device current state
            await api.get_state()
            # turn the device on for 15
            await api.control_device(Command.ON, 15)
            # turn the device off
            await api.control_device(Command.OFF)
            # set the device name
            await api.set_device_name("my new name")
            # configure the device for 02:30 auto shutdown
            await api.set_auto_shutdown(timedelta(hours=2, minutes=30))
            # get the schedules from the device
            await api.get_schedules()
            # delete and existing schedule with id 1
            await api.delete_schedule("1")
            # create a new recurring schedule for 13:00-14:30 executing on sunday and friday
            await api.create_schedule("13:00", "14:30", {Days.SUNDAY, Days.FRIDAY})

    asyncio.get_event_loop().run_until_complete(control_device("111.222.11.22", "ab1c2d"))
```

### Type2 API (Switcher Breeze and Runner)

We can use the Type2 API to gain the following capabilities on Switcher Breeze and Runner:

- Get the current state
- Control Runner position
- Control Breeze (State, Mode, Fan Level, Target Temperature, Vertical Swing)

```python
    async def control_runner_device(device_ip, device_id) :
        # for connecting to a device we need its id and ip address
        async with SwitcherType2Api(device_ip, device_id) as api:
            
            # get the device current state
            state: SwitcherShutterStateResponse = await api.get_shutter_state()
            # state.position (int) holds the current position of the shutter
            # state.direction (ShutterDirection) holds the current direction

            # open the shutter to 30%
            await api.set_position(30)
            # stop the shutter if currently rolling
            await api.stop()

    asyncio.get_event_loop().run_until_complete(control_runner_device("192.168.50.98", "f2239a"))
```

```python
    async def control_breeze_device(device_ip, device_id) :
        # for connecting to a device we need its id and ip address
        async with SwitcherType2Api(device_ip, device_id) as api:
            
            # get the device current state
            response: SwitcherThermostatStateResponse = await api.get_breeze_state()

            # Control Breeze Device
            
            # initialize the Breeze RemoteManager
            rm = BreezeRemoteManager()

            # get the remote structure (downloaded from the internet)
            # alternatively, you can get supply local directory path to the BreezeRemoteManager
            # and the BreezeRemoteManager will save and cache downloaded remotes into the directory

            async with ClientSession() as session:
                remote: BreezeRemote = await rm.get_remote(response.remote_id, api, session)
                
                # prepare a control command that turns on the Breeze 
                # (24 degree (Celsius), cooling with vertical swing and keep the current Fan Level)  
                command: SwitcherBreezeCommand = remote.get_command(
                        DeviceState.ON, 
                        ThermostatMode.COOL, 
                        24, 
                        resp.fan_level, 
                        ThermostatSwing.ON,
                        response.state
                    )

        # send command to the device
        await api.control_breeze_device(command)

    asyncio.get_event_loop().run_until_complete(control_breeze_device("192.168.50.77", "3a20b7"))

```

!!! note
    All requests return a response, you can use the
    [asdict](https://docs.python.org/3/library/dataclasses.html#dataclasses.asdict)
    __utility function to get familiarize with the various responses.
    You can visit the [API response messages section](./codedocs.md#switcherbaseresponse) and review the
    various response objects. Note that if a request doesn't have a specific response extending the
    base response, then the base response is the yielding response.

## Supported Devices

!!! info
    You can find the supported device types stated as [this enum](./codedocs.md#devicetype) members.
