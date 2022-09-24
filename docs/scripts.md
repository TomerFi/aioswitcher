# Command line scripts

## scripts/discover_devices.py

```shell
usage: discover_devices.py [-h] [-t {1,2,all}] [delay]

Discover and print info of Switcher devices

positional arguments:
  delay                 number of seconds to run, defaults to 60

options:
  -h, --help            show this help message and exit
  -t {1,2,all}, --type {1,2,all}
                        set protocol type: ['1', '2', 'all']

Executing this script will print a serialized version of the discovered Switcher
devices broadcasting on the local network for 60 seconds.
You can change the delay by passing an int argument: discover_devices.py 30

Switcher devices uses two protocol types:
    Protocol type 1 (UDP port 20002), used by: Switcher Mini, Switcher Power Plug, Switcher Touch, Switcher V2 (esp), Switcher V2 (qualcomm), Switcher V4
    Protocol type 2 (UDP port 20003), used by: Switcher Breeze, Switcher Runner, Switcher Runner Mini
You can change the scanned protocol type by passing an int argument: discover_devices.py -t 1

Note:
    WILL PRINT PRIVATE INFO SUCH AS DEVICE ID AND MAC.

Example output:
    Switcher devices broadcast a status message every approximately 4 seconds. This
    script listens for these messages and prints a serialized version of the to the
    standard output, for example (note the ``device_id`` and ``mac_address`` properties)::
    ```
        {   'auto_shutdown': '03:00:00',
            'device_id': 'aaaaaa',
            'device_state': <DeviceState.OFF: ('0000', 'off')>,
            'device_type': <DeviceType.V2_ESP: ('Switcher V2 (esp)', 'a7', <DeviceCategory.WATER_HEATER: 1>)>,
            'electric_current': 0.0,
            'ip_address': '192.168.1.33',
            'last_data_update': datetime.datetime(2021, 6, 13, 11, 11, 44, 883003),
            'mac_address': '12:A1:A2:1A:BC:1A',
            'name': 'My Switcher Boiler',
            'power_consumption': 0,
            'remaining_time': '00:00:00'}
    ```
Print all protocol types devices for 30 seconds:
    python discover_devices.py 30 -t all

Print only protocol type 1 devices:
    python discover_devices.py -t 1

Print only protocol type 2 devices:
    python discover_devices.py -t 2
```

## script/control_device.py

```shell
usage: control_device.py [-h]
                         {control_thermostat,create_schedule,delete_schedule,get_schedules,get_state,set_auto_shutdown,set_name,set_shutter_position,stop_shutter,turn_off,turn_on}
                         ...

Control your Switcher device

options:
  -h, --help            show this help message and exit

subcommands:
  supported actions

  {control_thermostat,create_schedule,delete_schedule,get_schedules,get_state,set_auto_shutdown,set_name,set_shutter_position,stop_shutter,turn_off,turn_on}
    control_thermostat  control a breeze device
    create_schedule     create a new schedule
    delete_schedule     delete a device schedule
    get_schedules       retrieve a device schedules
    get_state           get the current state of a device
    set_auto_shutdown   set the auto shutdown property (1h-24h)
    set_name            set the name of the device
    set_shutter_position
                        set shutter position
    stop_shutter        stop shutter
    turn_off            turn off the device
    turn_on             turn on the device

example usage:

python control_device.py -d ab1c2d -i "111.222.11.22" get_state

python control_device.py -d ab1c2d -i "111.222.11.22" turn_on

python control_device.py -d ab1c2d -i "111.222.11.22" turn_on -t 15

python control_device.py -d ab1c2d -i "111.222.11.22" turn_off

python control_device.py -d ab1c2d -i "111.222.11.22" set_name -n "My Boiler"

python control_device.py -d ab1c2d -i "111.222.11.22" set_auto_shutdown -r 2 -m 30

python control_device.py -d ab1c2d -i "111.222.11.22" get_schedules

python control_device.py -d ab1c2d -i "111.222.11.22" delete_schedule -s 3

python control_device.py -d ab1c2d -i "111.222.11.22" create_schedule -n "14:00" -f "14:30"

python control_device.py -d ab1c2d -i "111.222.11.22" create_schedule -n "17:30" -f "18:30" -w Sunday Monday Friday

python control_device.py -d f2239a -i "192.168.50.98" stop_shutter

python control_device.py -d f2239a -i "192.168.50.98" set_shutter_position -p 50

python control_device.py -d 3a20b7 -i "192.168.50.77" control_thermostat -r ELEC7001 -s on

python control_device.py -d 3a20b7 -i "192.168.50.77" control_thermostat -r ELEC7001 -m cool -f high -t 24

python control_device.py -d 3a20b7 -i "192.168.50.77" control_thermostat -r ELEC7001 -m dry

python control_device.py -d 3a20b7 -i "192.168.50.77" control_thermostat -r ELEC7001 -s off
```

### script/control_device.py control_thermostat

```shell
usage: control_device.py control_thermostat [-h] [-v] -d DEVICE_ID -i
                                            IP_ADDRESS -r REMOTE_ID
                                            [-s {on,off}]
                                            [-m {auto,dry,fan,cool,heat}]
                                            [-f {low,medium,high,auto}]
                                            [-w {off,on}] [-t TEMPERATURE]

options:
  -h, --help            show this help message and exit
  -v, --verbose         include the raw message
  -d DEVICE_ID, --device-id DEVICE_ID
                        the identification of the device
  -i IP_ADDRESS, --ip-address IP_ADDRESS
                        the ip address assigned to the device
  -r REMOTE_ID, --remote-id REMOTE_ID
                        remote id of your device
  -s {on,off}, --state {on,off}
                        thermostat state
  -m {auto,dry,fan,cool,heat}, --mode {auto,dry,fan,cool,heat}
                        thermostat mode
  -f {low,medium,high,auto}, --fan-level {low,medium,high,auto}
                        thermostat fan level
  -w {off,on}, --swing {off,on}
                        thermostat swing
  -t TEMPERATURE, --temperature TEMPERATURE
                        thermostat temperature, a positive integer
```

### script/control_device.py create_schedule

```shell
usage: control_device.py create_schedule [-h] [-v] -d DEVICE_ID -i IP_ADDRESS
                                         -n START_TIME -f END_TIME
                                         [-w [{Monday,Tuesday,Wednesday,Thursday,Friday,Saturday,Sunday} ...]]

options:
  -h, --help            show this help message and exit
  -v, --verbose         include the raw message
  -d DEVICE_ID, --device-id DEVICE_ID
                        the identification of the device
  -i IP_ADDRESS, --ip-address IP_ADDRESS
                        the ip address assigned to the device
  -n START_TIME, --start-time START_TIME
                        the on time for the schedule, e.g. 13:00
  -f END_TIME, --end-time END_TIME
                        the off time for the schedule, e.g. 13:30
  -w [{Monday,Tuesday,Wednesday,Thursday,Friday,Saturday,Sunday} ...], --weekdays [{Monday,Tuesday,Wednesday,Thursday,Friday,Saturday,Sunday} ...]
                        days for recurring schedules
```

### script/control_device.py delete_schedule

```shell
usage: control_device.py delete_schedule [-h] [-v] -d DEVICE_ID -i IP_ADDRESS
                                         -s SCHEDULE_ID

options:
  -h, --help            show this help message and exit
  -v, --verbose         include the raw message
  -d DEVICE_ID, --device-id DEVICE_ID
                        the identification of the device
  -i IP_ADDRESS, --ip-address IP_ADDRESS
                        the ip address assigned to the device
  -s SCHEDULE_ID, --schedule-id SCHEDULE_ID
                        the id of the schedule for deletion
```

### script/control_device.py get_schedules

```shell
usage: control_device.py get_schedules [-h] [-v] -d DEVICE_ID -i IP_ADDRESS

options:
  -h, --help            show this help message and exit
  -v, --verbose         include the raw message
  -d DEVICE_ID, --device-id DEVICE_ID
                        the identification of the device
  -i IP_ADDRESS, --ip-address IP_ADDRESS
                        the ip address assigned to the device
```

### script/control_device.py get_state

```shell
usage: control_device.py get_state [-h] [-v] -d DEVICE_ID -i IP_ADDRESS

options:
  -h, --help            show this help message and exit
  -v, --verbose         include the raw message
  -d DEVICE_ID, --device-id DEVICE_ID
                        the identification of the device
  -i IP_ADDRESS, --ip-address IP_ADDRESS
                        the ip address assigned to the device
```

### script/control_device.py set_auto_shutdown

```shell
usage: control_device.py set_auto_shutdown [-h] [-v] -d DEVICE_ID -i
                                           IP_ADDRESS -r HOURS [-m [MINUTES]]

options:
  -h, --help            show this help message and exit
  -v, --verbose         include the raw message
  -d DEVICE_ID, --device-id DEVICE_ID
                        the identification of the device
  -i IP_ADDRESS, --ip-address IP_ADDRESS
                        the ip address assigned to the device
  -r HOURS, --hours HOURS
                        number hours for the auto shutdown
  -m [MINUTES], --minutes [MINUTES]
                        number hours for the auto shutdown
```

### script/control_device.py set_name

```shell
usage: control_device.py set_name [-h] [-v] -d DEVICE_ID -i IP_ADDRESS -n NAME

options:
  -h, --help            show this help message and exit
  -v, --verbose         include the raw message
  -d DEVICE_ID, --device-id DEVICE_ID
                        the identification of the device
  -i IP_ADDRESS, --ip-address IP_ADDRESS
                        the ip address assigned to the device
  -n NAME, --name NAME  new name for the device
```

### script/control_device.py set_shutter_position

```shell
usage: control_device.py set_shutter_position [-h] [-v] -d DEVICE_ID -i
                                              IP_ADDRESS -p POSITION

options:
  -h, --help            show this help message and exit
  -v, --verbose         include the raw message
  -d DEVICE_ID, --device-id DEVICE_ID
                        the identification of the device
  -i IP_ADDRESS, --ip-address IP_ADDRESS
                        the ip address assigned to the device
  -p POSITION, --position POSITION
                        Shutter position percentage
```

### script/control_device.py stop_shutter

```shell
usage: control_device.py stop_shutter [-h] [-v] -d DEVICE_ID -i IP_ADDRESS

options:
  -h, --help            show this help message and exit
  -v, --verbose         include the raw message
  -d DEVICE_ID, --device-id DEVICE_ID
                        the identification of the device
  -i IP_ADDRESS, --ip-address IP_ADDRESS
                        the ip address assigned to the device
```

### script/control_device.py turn_off

```shell
usage: control_device.py turn_off [-h] [-v] -d DEVICE_ID -i IP_ADDRESS

options:
  -h, --help            show this help message and exit
  -v, --verbose         include the raw message
  -d DEVICE_ID, --device-id DEVICE_ID
                        the identification of the device
  -i IP_ADDRESS, --ip-address IP_ADDRESS
                        the ip address assigned to the device
```

### script/control_device.py turn_on

```shell
usage: control_device.py turn_on [-h] [-v] -d DEVICE_ID -i IP_ADDRESS
                                 [-t [TIMER]]

options:
  -h, --help            show this help message and exit
  -v, --verbose         include the raw message
  -d DEVICE_ID, --device-id DEVICE_ID
                        the identification of the device
  -i IP_ADDRESS, --ip-address IP_ADDRESS
                        the ip address assigned to the device
  -t [TIMER], --timer [TIMER]
                        set minutes timer for turn on operation
```
