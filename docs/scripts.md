# Command line scripts

## Discover Devices

### scripts/discover_devices.py

```shell
usage: discover_devices.py [-h] [delay]

Discover and print info of Switcher devices

positional arguments:
  delay       number of seconds to run, defaults to 60

options:
  -h, --help  show this help message and exit
```

### script/control_device.py

```shell
usage: control_device.py [-h] [-v] -d DEVICE_ID -i IP_ADDRESS
                         {get_state,turn_on,turn_off,set_name,set_auto_shutdown,get_schedules,delete_schedule,
                          create_schedule,stop_shutter,set_shutter_position,control_thermostat}
                         ...

Control your Switcher device

options:
  -h, --help            show this help message and exit
  -v, --verbose         include the raw message
  -d DEVICE_ID, --device-id DEVICE_ID
                        the identification of the device
  -i IP_ADDRESS, --ip-address IP_ADDRESS
                        the ip address assigned to the device

subcommands:
  supported actions

  {get_state,turn_on,turn_off,set_name,set_auto_shutdown,get_schedules,delete_schedule,create_schedule,stop_shutter,
    set_shutter_position,control_thermostat}

    get_state           get the current state of a device
    turn_on             turn on the device
    turn_off            turn off the device
    set_name            set the name of the device
    set_auto_shutdown   set the auto shutdown property (1h-24h)
    get_schedules       retrive a device schedules
    delete_schedule     delete a device schedule
    create_schedule     create a new schedule
    stop_shutter        stop shutter
    set_shutter_position
                        set shutter position
    control_thermostat  create a new schedule

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
python control_device.py -d 3a20b7 -i "192.168.50.77" control_thermostat -m dry

python control_device.py -d 3a20b7 -i "192.168.50.77" control_thermostat -s off

```

## script/control_device.py create_schedule

```shell
usage: control_device.py create_schedule [-h] -n START_TIME -f END_TIME [-w [{Monday,Tuesday,Wednesday,Thursday,Friday,
                                                                              Saturday,Sunday} ...]]

options:
  -h, --help            show this help message and exit
  -n START_TIME, --start-time START_TIME
                        the on time for the schedule, e.g. 13:00
  -f END_TIME, --end-time END_TIME
                        the off time for the schedule, e.g. 13:30
  -w [{Monday,Tuesday,Wednesday,Thursday,Friday,Saturday,Sunday} ...], --weekdays [{Monday,Tuesday,Wednesday,Thursday,
                                                                                    Friday,Saturday,Sunday} ...]
                        days for recurring schedules, possible values: ['Monday', 'Tuesday', 'Wednesday', 'Thursday',
                                                                        'Friday', 'Saturday', 'Sunday']
```

## script/control_device.py delete_schedule

```shell
usage: control_device.py delete_schedule [-h] -s SCHEDULE_ID

options:
  -h, --help            show this help message and exit
  -s SCHEDULE_ID, --schedule-id SCHEDULE_ID
                        the id of the schedule for deletion
```

## script/control_device.py get_schedules

```shell
usage: control_device.py get_schedules [-h]

options:
  -h, --help  show this help message and exit
```

## script/control_device.py get_state

```shell
usage: control_device.py get_state [-h]

options:
  -h, --help  show this help message and exit
```

## script/control_device.py set_auto_shutdown

```shell
usage: control_device.py set_auto_shutdown [-h] -r HOURS [-m [MINUTES]]

options:
  -h, --help            show this help message and exit
  -r HOURS, --hours HOURS
                        number hours for the auto shutdown
  -m [MINUTES], --minutes [MINUTES]
                        number hours for the auto shutdown
```

## script/control_device.py set_name

```shell
usage: control_device.py set_name [-h] -n NAME

options:
  -h, --help            show this help message and exit
  -n NAME, --name NAME  new name for the device
```

## script/control_device.py turn_off

```shell
usage: control_device.py turn_off [-h]

options:
  -h, --help  show this help message and exit
```

## script/control_device.py turn_on

```shell
usage: control_device.py turn_on [-h] [-t [TIMER]]

options:
  -h, --help            show this help message and exit
  -t [TIMER], --timer [TIMER]
                        set minutes timer for turn on operation
```

## script/control_device.py set_shutter_position

```shell
usage: control_device.py set_shutter_position [-h] -p POSITION

options:
  -h, --help            show this help message and exit
  -p POSITION, --position POSITION
                        Shutter position percentage
```

## script/control_device.py stop_shutter

```shell
usage: control_device.py stop_shutter [-h]

options:
  -h, --help  show this help message and exit
```

## script/control_device.py control_thermostat

```shell
usage: control_device.py control_thermostat [-h] [-s {on,off}] [-m {auto,dry,fan,cool,heat}] [-f {low,medium,high,auto}]
                                            [-w {off,on}] [-t TEMPERATURE]

options:
  -h, --help            show this help message and exit
  -s {on,off}, --state {on,off}
                        thermostat state, possible values
  -m {auto,dry,fan,cool,heat}, --mode {auto,dry,fan,cool,heat}
                        thermostat mode
  -f {low,medium,high,auto}, --fan-level {low,medium,high,auto}
                        thermostat fan level
  -w {off,on}, --swing {off,on}
                        thermostat swing
  -t TEMPERATURE, --temperature TEMPERATURE
                        thermostat temperature
```
