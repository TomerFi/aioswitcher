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
    Protocol type 1 (UDP port 20002 or port 10002), used by: Switcher Mini, Switcher Power Plug, Switcher Touch, Switcher V2 (esp), Switcher V2 (qualcomm), Switcher V4
    Protocol type 2 (UDP port 20003 or port 10003), used by: Switcher Breeze, Switcher Runner, Switcher Runner Mini, Switcher Runner S11, Switcher Runner S12, Switcher Light SL01, Switcher Light SL01 Mini, Switcher Light SL02, Switcher Light SL02 Mini, Switcher Light SL03
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
                         {control_thermostat,create_schedule,delete_schedule,get_schedules,get_state,get_thermostat_state,set_auto_shutdown,set_name,set_shutter_position,stop_shutter,turn_off,turn_on}
                         ...

Control your Switcher device

options:
  -h, --help            show this help message and exit

subcommands:
  supported actions

  {control_thermostat,create_schedule,delete_schedule,get_schedules,get_state,get_thermostat_state,set_auto_shutdown,set_name,set_shutter_position,stop_shutter,turn_off,turn_on}
    control_thermostat  control a breeze device
    create_schedule     create a new schedule
    delete_schedule     delete a device schedule
    get_schedules       retrieve a device schedules
    get_state           get the current state of a device
    get_thermostat_state
                        get the current state a thermostat (breeze) device
    set_auto_shutdown   set the auto shutdown property (1h-24h)
    set_name            set the name of the device
    set_shutter_position
                        set shutter position
    stop_shutter        stop shutter
    turn_off            turn off the device
    turn_on             turn on the device
    turn_off_light      turn off light
    turn_on_light       turn on light

example usage:

python control_device.py get_state -c "Switcher Touch" -d ab1c2d -i "111.222.11.22"

python control_device.py turn_on -c "Switcher Touch" -d ab1c2d -i "111.222.11.22"

python control_device.py turn_on -c "Switcher Touch" -d ab1c2d -l 18 -i "111.222.11.22"

python control_device.py turn_on -c "Switcher Touch" -d ab1c2d -i "111.222.11.22" -t 15

python control_device.py turn_off -c "Switcher Touch" -d ab1c2d -i "111.222.11.22"

python control_device.py turn_off -c "Switcher Touch" -d ab1c2d -l 18 -i "111.222.11.22"

python control_device.py set_name -c "Switcher Touch" -d ab1c2d -i "111.222.11.22" -n "My Boiler"

python control_device.py set_auto_shutdown -c "Switcher Touch" -d ab1c2d -i "111.222.11.22" -r 2 -m 30

python control_device.py get_schedules -c "Switcher Touch" -d ab1c2d -i "111.222.11.22"

python control_device.py delete_schedule -c "Switcher Touch" -d ab1c2d -i "111.222.11.22" -s 3

python control_device.py create_schedule -c "Switcher Touch" -d ab1c2d -i "111.222.11.22" -n "14:00" -f "14:30"

python control_device.py create_schedule -c "Switcher Touch" -d ab1c2d -i "111.222.11.22" -n "17:30" -f "18:30" -w Sunday Monday Friday

python control_device.py get_shutter_state -c "Switcher Runner" -d f2239a -i "192.168.50.98"

python control_device.py get_shutter_state -c "Switcher Runner S11" -k "zvVvd7JxtN7CgvkD1Psujw==" -d f2239a -i "192.168.50.98"

python control_device.py get_shutter_state -c "Switcher Runner S12" -k "zvVvd7JxtN7CgvkD1Psujw==" -d f2239a -i "192.168.50.98" -x 0

python control_device.py get_shutter_state -c "Switcher Runner S12" -k "zvVvd7JxtN7CgvkD1Psujw==" -d f2239a -i "192.168.50.98" -x 1

python control_device.py stop_shutter -c "Switcher Runner" -d f2239a -i "192.168.50.98"

python control_device.py stop_shutter -c "Switcher Runner S11" -k "zvVvd7JxtN7CgvkD1Psujw==" -d f2239a -i "192.168.50.98"

python control_device.py stop_shutter -c "Switcher Runner S12" -k "zvVvd7JxtN7CgvkD1Psujw==" -d f2239a -i "192.168.50.98" -x 0

python control_device.py stop_shutter -c "Switcher Runner S12" -k "zvVvd7JxtN7CgvkD1Psujw==" -d f2239a -i "192.168.50.98" -x 1

python control_device.py set_shutter_position -c "Switcher Runner" -d f2239a -i "192.168.50.98" -p 50

python control_device.py set_shutter_position -c "Switcher Runner S11" -k "zvVvd7JxtN7CgvkD1Psujw==" -d f2239a -i "192.168.50.98" -p 50

python control_device.py set_shutter_position -c "Switcher Runner S12" -k "zvVvd7JxtN7CgvkD1Psujw==" -d f2239a -i "192.168.50.98" -p 50 -x 0

python control_device.py set_shutter_position -c "Switcher Runner S12" -k "zvVvd7JxtN7CgvkD1Psujw==" -d f2239a -i "192.168.50.98" -p 50 -x 1

python control_device.py get_light_state -c "Switcher Runner S11" -k "zvVvd7JxtN7CgvkD1Psujw==" -d ab1c2d -i "111.222.11.22" -x 0

python control_device.py get_light_state -c "Switcher Runner S11" -k "zvVvd7JxtN7CgvkD1Psujw==" -d ab1c2d -i "111.222.11.22" -x 1

python control_device.py get_light_state -c "Switcher Runner S12" -k "zvVvd7JxtN7CgvkD1Psujw==" -d ab1c2d -i "111.222.11.22"

python control_device.py get_light_state -c "Switcher Light SL01" -k "zvVvd7JxtN7CgvkD1Psujw==" -d ab1c2d -i "111.222.11.22"

python control_device.py get_light_state -c "Switcher Light SL01 Mini" -k "zvVvd7JxtN7CgvkD1Psujw==" -d ab1c2d -i "111.222.11.22"

python control_device.py get_light_state -c "Switcher Light SL02" -k "zvVvd7JxtN7CgvkD1Psujw==" -d ab1c2d -i "111.222.11.22" -x 0

python control_device.py get_light_state -c "Switcher Light SL02" -k "zvVvd7JxtN7CgvkD1Psujw==" -d ab1c2d -i "111.222.11.22" -x 1

python control_device.py get_light_state -c "Switcher Light SL02 Mini" -k "zvVvd7JxtN7CgvkD1Psujw==" -d ab1c2d -i "111.222.11.22" -x 0

python control_device.py get_light_state -c "Switcher Light SL02 Mini" -k "zvVvd7JxtN7CgvkD1Psujw==" -d ab1c2d -i "111.222.11.22" -x 1

python control_device.py get_light_state -c "Switcher Light SL03" -k "zvVvd7JxtN7CgvkD1Psujw==" -d ab1c2d -i "111.222.11.22" -x 0

python control_device.py get_light_state -c "Switcher Light SL03" -k "zvVvd7JxtN7CgvkD1Psujw==" -d ab1c2d -i "111.222.11.22" -x 1

python control_device.py get_light_state -c "Switcher Light SL03" -k "zvVvd7JxtN7CgvkD1Psujw==" -d ab1c2d -i "111.222.11.22" -x 2

python control_device.py turn_on_light -c "Switcher Runner S11" -k "zvVvd7JxtN7CgvkD1Psujw==" -d ab1c2d -i "111.222.11.22" -x 0

python control_device.py turn_on_light -c "Switcher Runner S11" -k "zvVvd7JxtN7CgvkD1Psujw==" -d ab1c2d -i "111.222.11.22" -x 1

python control_device.py turn_on_light -c "Switcher Runner S12" -k "zvVvd7JxtN7CgvkD1Psujw==" -d ab1c2d -i "111.222.11.22"

python control_device.py turn_on_light -c "Switcher Light SL01" -k "zvVvd7JxtN7CgvkD1Psujw==" -d ab1c2d -i "111.222.11.22"

python control_device.py turn_on_light -c "Switcher Light SL01 Mini" -k "zvVvd7JxtN7CgvkD1Psujw==" -d ab1c2d -i "111.222.11.22"

python control_device.py turn_on_light -c "Switcher Light SL02" -k "zvVvd7JxtN7CgvkD1Psujw==" -d ab1c2d -i "111.222.11.22" -x 0

python control_device.py turn_on_light -c "Switcher Light SL02" -k "zvVvd7JxtN7CgvkD1Psujw==" -d ab1c2d -i "111.222.11.22" -x 1

python control_device.py turn_on_light -c "Switcher Light SL02 Mini" -k "zvVvd7JxtN7CgvkD1Psujw==" -d ab1c2d -i "111.222.11.22" -x 0

python control_device.py turn_on_light -c "Switcher Light SL02 Mini" -k "zvVvd7JxtN7CgvkD1Psujw==" -d ab1c2d -i "111.222.11.22" -x 1

python control_device.py turn_on_light -c "Switcher Light SL03" -k "zvVvd7JxtN7CgvkD1Psujw==" -d ab1c2d -i "111.222.11.22 -x 0

python control_device.py turn_on_light -c "Switcher Light SL03" -k "zvVvd7JxtN7CgvkD1Psujw==" -d ab1c2d -i "111.222.11.22 -x 1

python control_device.py turn_on_light -c "Switcher Light SL03" -k "zvVvd7JxtN7CgvkD1Psujw==" -d ab1c2d -i "111.222.11.22 -x 2

python control_device.py turn_off_light -c "Switcher Runner S11" -k "zvVvd7JxtN7CgvkD1Psujw==" -d ab1c2d -i "111.222.11.22" -x 0

python control_device.py turn_off_light -c "Switcher Runner S11" -k "zvVvd7JxtN7CgvkD1Psujw==" -d ab1c2d -i "111.222.11.22" -x 1

python control_device.py turn_off_light -c "Switcher Runner S12" -k "zvVvd7JxtN7CgvkD1Psujw==" -d ab1c2d -i "111.222.11.22"

python control_device.py turn_off_light -c "Switcher Light SL01" -k "zvVvd7JxtN7CgvkD1Psujw==" -d ab1c2d -i "111.222.11.22"

python control_device.py turn_off_light -c "Switcher Light SL01 Mini" -k "zvVvd7JxtN7CgvkD1Psujw==" -d ab1c2d -i "111.222.11.22"

python control_device.py turn_off_light -c "Switcher Light SL02" -k "zvVvd7JxtN7CgvkD1Psujw==" -d ab1c2d -i "111.222.11.22" -x 0

python control_device.py turn_off_light -c "Switcher Light SL02" -k "zvVvd7JxtN7CgvkD1Psujw==" -d ab1c2d -i "111.222.11.22" -x 1

python control_device.py turn_off_light -c "Switcher Light SL02 Mini" -k "zvVvd7JxtN7CgvkD1Psujw==" -d ab1c2d -i "111.222.11.22" -x 0

python control_device.py turn_off_light -c "Switcher Light SL02 Mini" -k "zvVvd7JxtN7CgvkD1Psujw==" -d ab1c2d -i "111.222.11.22" -x 1

python control_device.py turn_off_light -c "Switcher Light SL03" -k "zvVvd7JxtN7CgvkD1Psujw==" -d ab1c2d -i "111.222.11.22" -x 0

python control_device.py turn_off_light -c "Switcher Light SL03" -k "zvVvd7JxtN7CgvkD1Psujw==" -d ab1c2d -i "111.222.11.22" -x 1

python control_device.py turn_off_light -c "Switcher Light SL03" -k "zvVvd7JxtN7CgvkD1Psujw==" -d ab1c2d -i "111.222.11.22" -x 2

python control_device.py get_thermostat_state -c "Switcher Breeze" -d 3a20b7 -i "192.168.50.77"

python control_device.py control_thermostat -c "Switcher Breeze" -d 3a20b7 -i "192.168.50.77" -r ELEC7001 -s on

python control_device.py control_thermostat -c "Switcher Breeze" -d 3a20b7 -i "192.168.50.77" -r ELEC7001 -m cool -f high -t 24

python control_device.py control_thermostat -c "Switcher Breeze" -d 3a20b7 -i "192.168.50.77" -r ELEC7001 -m cool -f high -t 24 -u

python control_device.py control_thermostat -c "Switcher Breeze" -d 3a20b7 -i "192.168.50.77" -r ELEC7001 -m dry

python control_device.py control_thermostat -c "Switcher Breeze" -d 3a20b7 -i "192.168.50.77" -r ELEC7001 -s off
```

### script/control_device.py control_thermostat

```shell
usage: control_device.py control_thermostat [-h] [-v] -c DEVICE_TYPE -d DEVICE_ID [-l DEVICE_KEY] -i
                                            IP_ADDRESS -r REMOTE_ID
                                            [-s {on,off}]
                                            [-m {auto,dry,fan,cool,heat}]
                                            [-f {low,medium,high,auto}]
                                            [-w {off,on}] [-t TEMPERATURE]
                                            [-u]

options:
  -h, --help            show this help message and exit
  -v, --verbose         include the raw message
  -c DEVICE_TYPE, --device-type DEVICE_TYPE
                        the type of the device
  -d DEVICE_ID, --device-id DEVICE_ID
                        the identification of the device
  -l DEVICE_KEY, --device-key DEVICE_KEY
                        the login key of the device
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
  -u, --update          update state without control
```

### script/control_device.py create_schedule

```shell
usage: control_device.py create_schedule [-h] [-v] -c DEVICE_TYPE -d DEVICE_ID [-l DEVICE_KEY] -i IP_ADDRESS
                                         -n START_TIME -f END_TIME
                                         [-w [{Monday,Tuesday,Wednesday,Thursday,Friday,Saturday,Sunday} ...]]

options:
  -h, --help            show this help message and exit
  -v, --verbose         include the raw message
  -c DEVICE_TYPE, --device-type DEVICE_TYPE
                        the type of the device
  -d DEVICE_ID, --device-id DEVICE_ID
                        the identification of the device
  -l DEVICE_KEY, --device-key DEVICE_KEY
                        the login key of the device
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
usage: control_device.py delete_schedule [-h] [-v] -c DEVICE_TYPE -d DEVICE_ID [-l DEVICE_KEY] -i IP_ADDRESS
                                         -s SCHEDULE_ID

options:
  -h, --help            show this help message and exit
  -v, --verbose         include the raw message
  -c DEVICE_TYPE, --device-type DEVICE_TYPE
                        the type of the device
  -d DEVICE_ID, --device-id DEVICE_ID
                        the identification of the device
  -l DEVICE_KEY, --device-key DEVICE_KEY
                        the login key of the device
  -i IP_ADDRESS, --ip-address IP_ADDRESS
                        the ip address assigned to the device
  -s SCHEDULE_ID, --schedule-id SCHEDULE_ID
                        the id of the schedule for deletion
```

### script/control_device.py get_schedules

```shell
usage: control_device.py get_schedules [-h] [-v] -c DEVICE_TYPE -d DEVICE_ID [-l DEVICE_KEY] -i IP_ADDRESS

options:
  -h, --help            show this help message and exit
  -v, --verbose         include the raw message
  -c DEVICE_TYPE, --device-type DEVICE_TYPE
                        the type of the device
  -d DEVICE_ID, --device-id DEVICE_ID
                        the identification of the device
  -l DEVICE_KEY, --device-key DEVICE_KEY
                        the login key of the device
  -i IP_ADDRESS, --ip-address IP_ADDRESS
                        the ip address assigned to the device
```

### script/control_device.py get_state

```shell
usage: control_device.py get_state [-h] [-v] -c DEVICE_TYPE -d DEVICE_ID [-l DEVICE_KEY] -i IP_ADDRESS

options:
  -h, --help            show this help message and exit
  -v, --verbose         include the raw message
  -c DEVICE_TYPE, --device-type DEVICE_TYPE
                        the type of the device
  -d DEVICE_ID, --device-id DEVICE_ID
                        the identification of the device
  -l DEVICE_KEY, --device-key DEVICE_KEY
                        the login key of the device
  -i IP_ADDRESS, --ip-address IP_ADDRESS
                        the ip address assigned to the device
```

### script/control_device.py get_thermostat_state

```shell
usage: control_device.py get_thermostat_state [-h] [-v] -c DEVICE_TYPE -d DEVICE_ID [-l DEVICE_KEY] -i
                                              IP_ADDRESS

options:
  -h, --help            show this help message and exit
  -v, --verbose         include the raw message
  -c DEVICE_TYPE, --device-type DEVICE_TYPE
                        the type of the device
  -d DEVICE_ID, --device-id DEVICE_ID
                        the identification of the device
  -l DEVICE_KEY, --device-key DEVICE_KEY
                        the login key of the device
  -i IP_ADDRESS, --ip-address IP_ADDRESS
                        the ip address assigned to the device
```

### script/control_device.py set_auto_shutdown

```shell
usage: control_device.py set_auto_shutdown [-h] [-v] -c DEVICE_TYPE -d DEVICE_ID [-l DEVICE_KEY] -i
                                           IP_ADDRESS -r HOURS [-m [MINUTES]]

options:
  -h, --help            show this help message and exit
  -v, --verbose         include the raw message
  -c DEVICE_TYPE, --device-type DEVICE_TYPE
                        the type of the device
  -d DEVICE_ID, --device-id DEVICE_ID
                        the identification of the device
  -l DEVICE_KEY, --device-key DEVICE_KEY
                        the login key of the device
  -i IP_ADDRESS, --ip-address IP_ADDRESS
                        the ip address assigned to the device
  -r HOURS, --hours HOURS
                        number hours for the auto shutdown
  -m [MINUTES], --minutes [MINUTES]
                        number hours for the auto shutdown
```

### script/control_device.py set_name

```shell
usage: control_device.py set_name [-h] [-v] -c DEVICE_TYPE -d DEVICE_ID [-l DEVICE_KEY] -i IP_ADDRESS -n NAME

options:
  -h, --help            show this help message and exit
  -v, --verbose         include the raw message
  -c DEVICE_TYPE, --device-type DEVICE_TYPE
                        the type of the device
  -d DEVICE_ID, --device-id DEVICE_ID
                        the identification of the device
  -l DEVICE_KEY, --device-key DEVICE_KEY
                        the login key of the device
  -i IP_ADDRESS, --ip-address IP_ADDRESS
                        the ip address assigned to the device
  -n NAME, --name NAME  new name for the device
```

### script/control_device.py get_shutter_state

```shell
usage: control_device.py get_shutter_state [-h] [-v] -c DEVICE_TYPE [-k TOKEN] -d DEVICE_ID [-l DEVICE_KEY] -i IP_ADDRESS
                                           [-x INDEX]

options:
  -h, --help            show this help message and exit
  -v, --verbose         include the raw message
  -c DEVICE_TYPE, --device-type DEVICE_TYPE
                        the type of the device
  -k TOKEN, --token TOKEN
                        the token for communicating with the new switcher devices
  -d DEVICE_ID, --device-id DEVICE_ID
                        the identification of the device
  -l DEVICE_KEY, --device-key DEVICE_KEY
                        the login key of the device
  -i IP_ADDRESS, --ip-address IP_ADDRESS
                        the ip address assigned to the device
  -x INDEX, --index INDEX
                        the circuit number to operate
```

### script/control_device.py set_shutter_position

```shell
usage: control_device.py set_shutter_position [-h] [-v] -c DEVICE_TYPE [-k TOKEN] -d DEVICE_ID [-l DEVICE_KEY] -i
                                              IP_ADDRESS -p POSITION [-x INDEX]

options:
  -h, --help            show this help message and exit
  -v, --verbose         include the raw message
  -c DEVICE_TYPE, --device-type DEVICE_TYPE
                        the type of the device
  -k TOKEN, --token TOKEN
                        the token for communicating with the new switcher devices
  -d DEVICE_ID, --device-id DEVICE_ID
                        the identification of the device
  -l DEVICE_KEY, --device-key DEVICE_KEY
                        the login key of the device
  -i IP_ADDRESS, --ip-address IP_ADDRESS
                        the ip address assigned to the device
  -p POSITION, --position POSITION
                        Shutter position percentage
  -x INDEX, --index INDEX
                        the circuit number to operate
```

### script/control_device.py stop_shutter

```shell
usage: control_device.py stop_shutter [-h] [-v] -c DEVICE_TYPE [-k TOKEN] -d DEVICE_ID [-l DEVICE_KEY] -i IP_ADDRESS [-x INDEX]

options:
  -h, --help            show this help message and exit
  -v, --verbose         include the raw message
  -c DEVICE_TYPE, --device-type DEVICE_TYPE
                        the type of the device
  -k TOKEN, --token TOKEN
                        the token for communicating with the new switcher devices
  -d DEVICE_ID, --device-id DEVICE_ID
                        the identification of the device
  -l DEVICE_KEY, --device-key DEVICE_KEY
                        the login key of the device
  -i IP_ADDRESS, --ip-address IP_ADDRESS
                        the ip address assigned to the device
  -x INDEX, --index INDEX
                        the circuit number to operate
```

### script/control_device.py turn_off

```shell
usage: control_device.py turn_off [-h] [-v] -c DEVICE_TYPE -d DEVICE_ID [-l DEVICE_KEY] -i IP_ADDRESS

options:
  -h, --help            show this help message and exit
  -v, --verbose         include the raw message
  -c DEVICE_TYPE, --device-type DEVICE_TYPE
                        the type of the device
  -d DEVICE_ID, --device-id DEVICE_ID
                        the identification of the device
  -l DEVICE_KEY, --device-key DEVICE_KEY
                        the login key of the device
  -i IP_ADDRESS, --ip-address IP_ADDRESS
                        the ip address assigned to the device
```

### script/control_device.py turn_on

```shell
usage: control_device.py turn_on [-h] [-v] -c DEVICE_TYPE -d DEVICE_ID [-l DEVICE_KEY] -i IP_ADDRESS
                                 [-t [TIMER]]

options:
  -h, --help            show this help message and exit
  -v, --verbose         include the raw message
  -c DEVICE_TYPE, --device-type DEVICE_TYPE
                        the type of the device
  -d DEVICE_ID, --device-id DEVICE_ID
                        the identification of the device
  -l DEVICE_KEY, --device-key DEVICE_KEY
                        the login key of the device
  -i IP_ADDRESS, --ip-address IP_ADDRESS
                        the ip address assigned to the device
  -t [TIMER], --timer [TIMER]
                        set minutes timer for turn on operation
```

### script/control_device.py get_light_state

```shell
usage: control_device.py get_light_state [-h] [-v] -c DEVICE_TYPE [-k TOKEN] -d DEVICE_ID [-l DEVICE_KEY] -i IP_ADDRESS [-x INDEX]

options:
  -h, --help            show this help message and exit
  -v, --verbose         include the raw message
  -c DEVICE_TYPE, --device-type DEVICE_TYPE
                        the type of the device
  -k TOKEN, --token TOKEN
                        the token for communicating with the new switcher devices
  -d DEVICE_ID, --device-id DEVICE_ID
                        the identification of the device
  -l DEVICE_KEY, --device-key DEVICE_KEY
                        the login key of the device
  -i IP_ADDRESS, --ip-address IP_ADDRESS
                        the ip address assigned to the device
  -x INDEX, --index INDEX
                        the circuit number to turn off
```

### script/control_device.py turn_off_light

```shell
usage: control_device.py turn_off_light [-h] [-v] -c DEVICE_TYPE [-k TOKEN] -d DEVICE_ID [-l DEVICE_KEY] -i IP_ADDRESS [-x INDEX]

options:
  -h, --help            show this help message and exit
  -v, --verbose         include the raw message
  -c DEVICE_TYPE, --device-type DEVICE_TYPE
                        the type of the device
  -k TOKEN, --token TOKEN
                        the token for communicating with the new switcher devices
  -d DEVICE_ID, --device-id DEVICE_ID
                        the identification of the device
  -l DEVICE_KEY, --device-key DEVICE_KEY
                        the login key of the device
  -i IP_ADDRESS, --ip-address IP_ADDRESS
                        the ip address assigned to the device
  -x INDEX, --index INDEX
                        the circuit number to turn off
```

### script/control_device.py turn_on_light

```shell
usage: control_device.py turn_on_light [-h] [-v] -c DEVICE_TYPE [-k TOKEN] -d DEVICE_ID [-l DEVICE_KEY] -i IP_ADDRESS [-x INDEX]

options:
  -h, --help            show this help message and exit
  -v, --verbose         include the raw message
  -c DEVICE_TYPE, --device-type DEVICE_TYPE
                        the type of the device
  -k TOKEN, --token TOKEN
                        the token for communicating with the new switcher devices
  -d DEVICE_ID, --device-id DEVICE_ID
                        the identification of the device
  -l DEVICE_KEY, --device-key DEVICE_KEY
                        the login key of the device
  -i IP_ADDRESS, --ip-address IP_ADDRESS
                        the ip address assigned to the device
  -x INDEX, --index INDEX
                        the circuit number to turn on
```

## script/get_device_login_key.py

```shell
usage: get_device_login_key.py [-h] -i IP_ADDRESS -p {20002,10002,20003,10003}

Get the login key of your Switcher device

options:
  -h, --help            show this help message and exit
  -i IP_ADDRESS, --ip-address IP_ADDRESS
                        the ip address assigned to the device
  -p {20002,10002,20003,10003}, --port {20002,10002,20003,10003}

example usage:

python get_device_login_key.py -i "111.222.11.22" -p 10002
```

## script/validate_token.py

```shell
usage: validate_token.py [-h] -u USERNAME -t TOKEN

Validate a Token from Switcher by username and token

options:
  -h, --help            show this help message and exit
  -u USERNAME, --username USERNAME
                        the username of the user (Email address)
  -t TOKEN, --token TOKEN
                        the token of the user sent by Email

example usage:

python validate_token.py -u "email" -t "zvVvd7JxtN7CgvkD1Psujw=="

python validate_token.py --username "email" --token "zvVvd7JxtN7CgvkD1Psujw=="
```
