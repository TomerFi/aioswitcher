Use the following helper CLI commands to work with Switcher devices.

## Installation

The commands are installed together with aioswitcher, so they always match the installed library version:

```shell
pip install aioswitcher
```

| Command | Description |
| ------- | ----------- |
| `switcher-control-device` | Control devices |
| `switcher-discover-devices` | Discover devices and their states |
| `switcher-get-device-login-key` | Fetch the login key from devices |
| `switcher-validate-token` | Validate your device token |

## Control device

Use to control devices.

```shell title="switcher-control-device"
$ switcher-control-device --help

usage: switcher-control-device [-h]
                               {control_thermostat,create_schedule,delete_schedule,get_schedules,get_state,get_thermostat_state,set_auto_shutdown,set_name,get_shutter_state,set_shutter_position,stop_shutter,turn_off_shutter_child_lock,turn_on_shutter_child_lock,turn_off,turn_on,get_light_state,turn_off_light,turn_on_light,get_heater_state}
                               ...

Control your Switcher device

options:
  -h, --help            show this help message and exit

subcommands:
  supported actions

  {control_thermostat,create_schedule,delete_schedule,get_schedules,get_state,get_thermostat_state,set_auto_shutdown,set_name,get_shutter_state,set_shutter_position,stop_shutter,turn_off_shutter_child_lock,turn_on_shutter_child_lock,turn_off,turn_on,get_light_state,turn_off_light,turn_on_light,get_heater_state}
    control_thermostat  control a breeze device
    create_schedule     create a new schedule
    delete_schedule     delete a device schedule
    get_schedules       retrieve a device schedules
    get_state           get the current state of a device
    get_thermostat_state
                        get the current state a thermostat (breeze) device
    set_auto_shutdown   set the auto shutdown property (1h-24h)
    set_name            set the name of the device
    get_shutter_state   get the current shutter state of a device
    set_shutter_position
                        set shutter position
    stop_shutter        stop shutter
    turn_off_shutter_child_lock
                        turn off shutter child lock
    turn_on_shutter_child_lock
                        turn on shutter child lock
    turn_off            turn off the device
    turn_on             turn on the device
    get_light_state     get the current light state of a device
    turn_off_light      turn off light
    turn_on_light       turn on light
    get_heater_state    get the current state of a heater device
```

### Create schedule

```shell title="switcher-control-device create_schedule"
$ switcher-control-device create_schedule --help

usage: switcher-control-device create_schedule [-h] [-v] -c
                                               {mini,plug,touch,v2esp,v2qual,v4,breeze,runner,runnermini,runners11,runners12,light01,light01mini,light02,light02mini,light03,heater}
                                               [-k TOKEN] -d DEVICE_ID [-l DEVICE_KEY] -i IP_ADDRESS -n START_TIME -f
                                               END_TIME
                                               [-w [{Monday,Tuesday,Wednesday,Thursday,Friday,Saturday,Sunday} ...]]

options:
  -h, --help            show this help message and exit
  -v, --verbose         include the raw message
  -c {mini,plug,touch,v2esp,v2qual,v4,breeze,runner,runnermini,runners11,runners12,light01,light01mini,light02,light02mini,light03,heater}, --device-type {mini,plug,touch,v2esp,v2qual,v4,breeze,runner,runnermini,runners11,runners12,light01,light01mini,light02,light02mini,light03,heater}
                        the type of the device
  -k TOKEN, --token TOKEN
                        the token for communicating with switcher token-based devices
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

example usage:

switcher-control-device create_schedule -c "touch" -d ab1c2d -i "111.222.11.22" -n "14:00" -f "14:30"

switcher-control-device create_schedule -c "touch" -d ab1c2d -i "111.222.11.22" -n "17:30" -f "18:30" -w Sunday Monday Friday
```

### Control thermostat

```shell title="switcher-control-device control_thermostat"
$ switcher-control-device control_thermostat --help

usage: switcher-control-device control_thermostat [-h] [-v] -c
                                                  {mini,plug,touch,v2esp,v2qual,v4,breeze,runner,runnermini,runners11,runners12,light01,light01mini,light02,light02mini,light03,heater}
                                                  [-k TOKEN] -d DEVICE_ID [-l DEVICE_KEY] -i IP_ADDRESS -r REMOTE_ID
                                                  [-s {on,off}] [-m {auto,dry,fan,cool,heat}]
                                                  [-f {low,medium,high,auto}] [-w {off,on}] [-t TEMPERATURE] [-u]

options:
  -h, --help            show this help message and exit
  -v, --verbose         include the raw message
  -c {mini,plug,touch,v2esp,v2qual,v4,breeze,runner,runnermini,runners11,runners12,light01,light01mini,light02,light02mini,light03,heater}, --device-type {mini,plug,touch,v2esp,v2qual,v4,breeze,runner,runnermini,runners11,runners12,light01,light01mini,light02,light02mini,light03,heater}
                        the type of the device
  -k TOKEN, --token TOKEN
                        the token for communicating with switcher token-based devices
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

example usage:

switcher-control-device control_thermostat -c "breeze" -d 3a20b7 -i "192.168.50.77" -r ELEC7001 -s on

switcher-control-device control_thermostat -c "breeze" -d 3a20b7 -i "192.168.50.77" -r ELEC7001 -m cool -f high -t 24

switcher-control-device control_thermostat -c "breeze" -d 3a20b7 -i "192.168.50.77" -r ELEC7001 -m cool -f high -t 24 -u

switcher-control-device control_thermostat -c "breeze" -d 3a20b7 -i "192.168.50.77" -r ELEC7001 -m dry

switcher-control-device control_thermostat -c "breeze" -d 3a20b7 -i "192.168.50.77" -r ELEC7001 -s off
```

### Delete schedule

```shell title="switcher-control-device delete_schedule"
$ switcher-control-device delete_schedule --help

usage: switcher-control-device delete_schedule [-h] [-v] -c
                                               {mini,plug,touch,v2esp,v2qual,v4,breeze,runner,runnermini,runners11,runners12,light01,light01mini,light02,light02mini,light03,heater}
                                               [-k TOKEN] -d DEVICE_ID [-l DEVICE_KEY] -i IP_ADDRESS -s SCHEDULE_ID

options:
  -h, --help            show this help message and exit
  -v, --verbose         include the raw message
  -c {mini,plug,touch,v2esp,v2qual,v4,breeze,runner,runnermini,runners11,runners12,light01,light01mini,light02,light02mini,light03,heater}, --device-type {mini,plug,touch,v2esp,v2qual,v4,breeze,runner,runnermini,runners11,runners12,light01,light01mini,light02,light02mini,light03,heater}
                        the type of the device
  -k TOKEN, --token TOKEN
                        the token for communicating with switcher token-based devices
  -d DEVICE_ID, --device-id DEVICE_ID
                        the identification of the device
  -l DEVICE_KEY, --device-key DEVICE_KEY
                        the login key of the device
  -i IP_ADDRESS, --ip-address IP_ADDRESS
                        the ip address assigned to the device
  -s SCHEDULE_ID, --schedule-id SCHEDULE_ID
                        the id of the schedule for deletion

example usage:

switcher-control-device delete_schedule -c "touch" -d ab1c2d -i "111.222.11.22" -s 3
```

### Get light state

```shell title="switcher-control-device get_light_state"
$ switcher-control-device get_light_state --help

usage: switcher-control-device get_light_state [-h] [-v] -c
                                               {mini,plug,touch,v2esp,v2qual,v4,breeze,runner,runnermini,runners11,runners12,light01,light01mini,light02,light02mini,light03,heater}
                                               [-k TOKEN] -d DEVICE_ID [-l DEVICE_KEY] -i IP_ADDRESS [-x INDEX]

options:
  -h, --help            show this help message and exit
  -v, --verbose         include the raw message
  -c {mini,plug,touch,v2esp,v2qual,v4,breeze,runner,runnermini,runners11,runners12,light01,light01mini,light02,light02mini,light03,heater}, --device-type {mini,plug,touch,v2esp,v2qual,v4,breeze,runner,runnermini,runners11,runners12,light01,light01mini,light02,light02mini,light03,heater}
                        the type of the device
  -k TOKEN, --token TOKEN
                        the token for communicating with switcher token-based devices
  -d DEVICE_ID, --device-id DEVICE_ID
                        the identification of the device
  -l DEVICE_KEY, --device-key DEVICE_KEY
                        the login key of the device
  -i IP_ADDRESS, --ip-address IP_ADDRESS
                        the ip address assigned to the device
  -x INDEX, --index INDEX
                        the circuit number to turn off

example usage:

switcher-control-device get_light_state -c "runners11" -k "zvVvd7JxtN7CgvkD1Psujw==" -d ab1c2d -i "111.222.11.22" -x 0

switcher-control-device get_light_state -c "runners11" -k "zvVvd7JxtN7CgvkD1Psujw==" -d ab1c2d -i "111.222.11.22" -x 1

switcher-control-device get_light_state -c "runners12" -k "zvVvd7JxtN7CgvkD1Psujw==" -d ab1c2d -i "111.222.11.22"

switcher-control-device get_light_state -c "light01" -k "zvVvd7JxtN7CgvkD1Psujw==" -d ab1c2d -i "111.222.11.22"

switcher-control-device get_light_state -c "light01mini" -k "zvVvd7JxtN7CgvkD1Psujw==" -d ab1c2d -i "111.222.11.22"

switcher-control-device get_light_state -c "light02" -k "zvVvd7JxtN7CgvkD1Psujw==" -d ab1c2d -i "111.222.11.22" -x 0

switcher-control-device get_light_state -c "light02" -k "zvVvd7JxtN7CgvkD1Psujw==" -d ab1c2d -i "111.222.11.22" -x 1

switcher-control-device get_light_state -c "light02mini" -k "zvVvd7JxtN7CgvkD1Psujw==" -d ab1c2d -i "111.222.11.22" -x 0

switcher-control-device get_light_state -c "light02mini" -k "zvVvd7JxtN7CgvkD1Psujw==" -d ab1c2d -i "111.222.11.22" -x 1

switcher-control-device get_light_state -c "light03" -k "zvVvd7JxtN7CgvkD1Psujw==" -d ab1c2d -i "111.222.11.22" -x 0

switcher-control-device get_light_state -c "light03" -k "zvVvd7JxtN7CgvkD1Psujw==" -d ab1c2d -i "111.222.11.22" -x 1

switcher-control-device get_light_state -c "light03" -k "zvVvd7JxtN7CgvkD1Psujw==" -d ab1c2d -i "111.222.11.22" -x 2
```

### Get schedules

```shell title="switcher-control-device get_schedules"
$ switcher-control-device get_schedules --help

usage: switcher-control-device get_schedules [-h] [-v] -c
                                             {mini,plug,touch,v2esp,v2qual,v4,breeze,runner,runnermini,runners11,runners12,light01,light01mini,light02,light02mini,light03,heater}
                                             [-k TOKEN] -d DEVICE_ID [-l DEVICE_KEY] -i IP_ADDRESS

options:
  -h, --help            show this help message and exit
  -v, --verbose         include the raw message
  -c {mini,plug,touch,v2esp,v2qual,v4,breeze,runner,runnermini,runners11,runners12,light01,light01mini,light02,light02mini,light03,heater}, --device-type {mini,plug,touch,v2esp,v2qual,v4,breeze,runner,runnermini,runners11,runners12,light01,light01mini,light02,light02mini,light03,heater}
                        the type of the device
  -k TOKEN, --token TOKEN
                        the token for communicating with switcher token-based devices
  -d DEVICE_ID, --device-id DEVICE_ID
                        the identification of the device
  -l DEVICE_KEY, --device-key DEVICE_KEY
                        the login key of the device
  -i IP_ADDRESS, --ip-address IP_ADDRESS
                        the ip address assigned to the device

example usage:

switcher-control-device get_schedules -c "touch" -d ab1c2d -i "111.222.11.22"
```

### Get shutter state

```shell title="switcher-control-device get_shutter_state"
$ switcher-control-device get_shutter_state --help

usage: switcher-control-device get_shutter_state [-h] [-v] -c
                                                 {mini,plug,touch,v2esp,v2qual,v4,breeze,runner,runnermini,runners11,runners12,light01,light01mini,light02,light02mini,light03,heater}
                                                 [-k TOKEN] -d DEVICE_ID [-l DEVICE_KEY] -i IP_ADDRESS [-x INDEX]

options:
  -h, --help            show this help message and exit
  -v, --verbose         include the raw message
  -c {mini,plug,touch,v2esp,v2qual,v4,breeze,runner,runnermini,runners11,runners12,light01,light01mini,light02,light02mini,light03,heater}, --device-type {mini,plug,touch,v2esp,v2qual,v4,breeze,runner,runnermini,runners11,runners12,light01,light01mini,light02,light02mini,light03,heater}
                        the type of the device
  -k TOKEN, --token TOKEN
                        the token for communicating with switcher token-based devices
  -d DEVICE_ID, --device-id DEVICE_ID
                        the identification of the device
  -l DEVICE_KEY, --device-key DEVICE_KEY
                        the login key of the device
  -i IP_ADDRESS, --ip-address IP_ADDRESS
                        the ip address assigned to the device
  -x INDEX, --index INDEX
                        the circuit number to operate

example usage:

switcher-control-device get_shutter_state -c "runner" -d f2239a -i "192.168.50.98"

switcher-control-device get_shutter_state -c "runnermini" -d f2239a -i "192.168.50.98"

switcher-control-device get_shutter_state -c "runners11" -k "zvVvd7JxtN7CgvkD1Psujw==" -d f2239a -i "192.168.50.98"

switcher-control-device get_shutter_state -c "runners12" -k "zvVvd7JxtN7CgvkD1Psujw==" -d f2239a -i "192.168.50.98" -x 0

switcher-control-device get_shutter_state -c "runners12" -k "zvVvd7JxtN7CgvkD1Psujw==" -d f2239a -i "192.168.50.98" -x 1
```

### Get state

```shell title="switcher-control-device get_state"
$ switcher-control-device get_state --help

usage: switcher-control-device get_state [-h] [-v] -c
                                         {mini,plug,touch,v2esp,v2qual,v4,breeze,runner,runnermini,runners11,runners12,light01,light01mini,light02,light02mini,light03,heater}
                                         [-k TOKEN] -d DEVICE_ID [-l DEVICE_KEY] -i IP_ADDRESS

options:
  -h, --help            show this help message and exit
  -v, --verbose         include the raw message
  -c {mini,plug,touch,v2esp,v2qual,v4,breeze,runner,runnermini,runners11,runners12,light01,light01mini,light02,light02mini,light03,heater}, --device-type {mini,plug,touch,v2esp,v2qual,v4,breeze,runner,runnermini,runners11,runners12,light01,light01mini,light02,light02mini,light03,heater}
                        the type of the device
  -k TOKEN, --token TOKEN
                        the token for communicating with switcher token-based devices
  -d DEVICE_ID, --device-id DEVICE_ID
                        the identification of the device
  -l DEVICE_KEY, --device-key DEVICE_KEY
                        the login key of the device
  -i IP_ADDRESS, --ip-address IP_ADDRESS
                        the ip address assigned to the device

example usage:

switcher-control-device get_state -c "touch" -d ab1c2d -i "111.222.11.22"
```

### Get thermostat state

```shell title="switcher-control-device get_thermostat_state"
$ switcher-control-device get_thermostat_state --help

usage: switcher-control-device get_thermostat_state [-h] [-v] -c
                                                    {mini,plug,touch,v2esp,v2qual,v4,breeze,runner,runnermini,runners11,runners12,light01,light01mini,light02,light02mini,light03,heater}
                                                    [-k TOKEN] -d DEVICE_ID [-l DEVICE_KEY] -i IP_ADDRESS

options:
  -h, --help            show this help message and exit
  -v, --verbose         include the raw message
  -c {mini,plug,touch,v2esp,v2qual,v4,breeze,runner,runnermini,runners11,runners12,light01,light01mini,light02,light02mini,light03,heater}, --device-type {mini,plug,touch,v2esp,v2qual,v4,breeze,runner,runnermini,runners11,runners12,light01,light01mini,light02,light02mini,light03,heater}
                        the type of the device
  -k TOKEN, --token TOKEN
                        the token for communicating with switcher token-based devices
  -d DEVICE_ID, --device-id DEVICE_ID
                        the identification of the device
  -l DEVICE_KEY, --device-key DEVICE_KEY
                        the login key of the device
  -i IP_ADDRESS, --ip-address IP_ADDRESS
                        the ip address assigned to the device

example usage:

switcher-control-device get_thermostat_state -c "breeze" -d 3a20b7 -i "192.168.50.77"
```

### Set auto shutdown

```shell title="switcher-control-device set_auto_shutdown"
$ switcher-control-device set_auto_shutdown --help

usage: switcher-control-device set_auto_shutdown [-h] [-v] -c
                                                 {mini,plug,touch,v2esp,v2qual,v4,breeze,runner,runnermini,runners11,runners12,light01,light01mini,light02,light02mini,light03,heater}
                                                 [-k TOKEN] -d DEVICE_ID [-l DEVICE_KEY] -i IP_ADDRESS -r HOURS
                                                 [-m [MINUTES]]

options:
  -h, --help            show this help message and exit
  -v, --verbose         include the raw message
  -c {mini,plug,touch,v2esp,v2qual,v4,breeze,runner,runnermini,runners11,runners12,light01,light01mini,light02,light02mini,light03,heater}, --device-type {mini,plug,touch,v2esp,v2qual,v4,breeze,runner,runnermini,runners11,runners12,light01,light01mini,light02,light02mini,light03,heater}
                        the type of the device
  -k TOKEN, --token TOKEN
                        the token for communicating with switcher token-based devices
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

example usage:

switcher-control-device set_auto_shutdown -c "touch" -d ab1c2d -i "111.222.11.22" -r 2 -m 30
```

### Set name

```shell title="switcher-control-device set_name"
$ switcher-control-device set_name --help

usage: switcher-control-device set_name [-h] [-v] -c
                                        {mini,plug,touch,v2esp,v2qual,v4,breeze,runner,runnermini,runners11,runners12,light01,light01mini,light02,light02mini,light03,heater}
                                        [-k TOKEN] -d DEVICE_ID [-l DEVICE_KEY] -i IP_ADDRESS -n NAME

options:
  -h, --help            show this help message and exit
  -v, --verbose         include the raw message
  -c {mini,plug,touch,v2esp,v2qual,v4,breeze,runner,runnermini,runners11,runners12,light01,light01mini,light02,light02mini,light03,heater}, --device-type {mini,plug,touch,v2esp,v2qual,v4,breeze,runner,runnermini,runners11,runners12,light01,light01mini,light02,light02mini,light03,heater}
                        the type of the device
  -k TOKEN, --token TOKEN
                        the token for communicating with switcher token-based devices
  -d DEVICE_ID, --device-id DEVICE_ID
                        the identification of the device
  -l DEVICE_KEY, --device-key DEVICE_KEY
                        the login key of the device
  -i IP_ADDRESS, --ip-address IP_ADDRESS
                        the ip address assigned to the device
  -n NAME, --name NAME  new name for the device

example usage:

switcher-control-device set_name -c "touch" -d ab1c2d -i "111.222.11.22" -n "My Boiler"
```

### Set shutter position

```shell title="switcher-control-device set_shutter_position"
$ switcher-control-device set_shutter_position --help

usage: switcher-control-device set_shutter_position [-h] [-v] -c
                                                    {mini,plug,touch,v2esp,v2qual,v4,breeze,runner,runnermini,runners11,runners12,light01,light01mini,light02,light02mini,light03,heater}
                                                    [-k TOKEN] -d DEVICE_ID [-l DEVICE_KEY] -i IP_ADDRESS -p POSITION
                                                    [-x INDEX]

options:
  -h, --help            show this help message and exit
  -v, --verbose         include the raw message
  -c {mini,plug,touch,v2esp,v2qual,v4,breeze,runner,runnermini,runners11,runners12,light01,light01mini,light02,light02mini,light03,heater}, --device-type {mini,plug,touch,v2esp,v2qual,v4,breeze,runner,runnermini,runners11,runners12,light01,light01mini,light02,light02mini,light03,heater}
                        the type of the device
  -k TOKEN, --token TOKEN
                        the token for communicating with switcher token-based devices
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

example usage:

switcher-control-device set_shutter_position -c "runner" -d f2239a -i "192.168.50.98" -p 50

switcher-control-device set_shutter_position -c "runnermini" -d f2239a -i "192.168.50.98" -p 50

switcher-control-device set_shutter_position -c "runners11" -k "zvVvd7JxtN7CgvkD1Psujw==" -d f2239a -i "192.168.50.98" -p 50

switcher-control-device set_shutter_position -c "runners12" -k "zvVvd7JxtN7CgvkD1Psujw==" -d f2239a -i "192.168.50.98" -p 50 -x 0

switcher-control-device set_shutter_position -c "runners12" -k "zvVvd7JxtN7CgvkD1Psujw==" -d f2239a -i "192.168.50.98" -p 50 -x 1
```

### Stop shutter

```shell title="switcher-control-device stop_shutter"
$ switcher-control-device stop_shutter --help

usage: switcher-control-device stop_shutter [-h] [-v] -c
                                            {mini,plug,touch,v2esp,v2qual,v4,breeze,runner,runnermini,runners11,runners12,light01,light01mini,light02,light02mini,light03,heater}
                                            [-k TOKEN] -d DEVICE_ID [-l DEVICE_KEY] -i IP_ADDRESS [-x INDEX]

options:
  -h, --help            show this help message and exit
  -v, --verbose         include the raw message
  -c {mini,plug,touch,v2esp,v2qual,v4,breeze,runner,runnermini,runners11,runners12,light01,light01mini,light02,light02mini,light03,heater}, --device-type {mini,plug,touch,v2esp,v2qual,v4,breeze,runner,runnermini,runners11,runners12,light01,light01mini,light02,light02mini,light03,heater}
                        the type of the device
  -k TOKEN, --token TOKEN
                        the token for communicating with switcher token-based devices
  -d DEVICE_ID, --device-id DEVICE_ID
                        the identification of the device
  -l DEVICE_KEY, --device-key DEVICE_KEY
                        the login key of the device
  -i IP_ADDRESS, --ip-address IP_ADDRESS
                        the ip address assigned to the device
  -x INDEX, --index INDEX
                        the circuit number to operate

example usage:

switcher-control-device stop_shutter -c "runner" -d f2239a -i "192.168.50.98"

switcher-control-device stop_shutter -c "runnermini" -d f2239a -i "192.168.50.98"

switcher-control-device stop_shutter -c "runners11" -k "zvVvd7JxtN7CgvkD1Psujw==" -d f2239a -i "192.168.50.98"

switcher-control-device stop_shutter -c "runners12" -k "zvVvd7JxtN7CgvkD1Psujw==" -d f2239a -i "192.168.50.98" -x 0

switcher-control-device stop_shutter -c "runners12" -k "zvVvd7JxtN7CgvkD1Psujw==" -d f2239a -i "192.168.50.98" -x 1
```

### Turn off

```shell title="switcher-control-device turn_off"
$ switcher-control-device turn_off --help

usage: switcher-control-device turn_off [-h] [-v] -c
                                        {mini,plug,touch,v2esp,v2qual,v4,breeze,runner,runnermini,runners11,runners12,light01,light01mini,light02,light02mini,light03,heater}
                                        [-k TOKEN] -d DEVICE_ID [-l DEVICE_KEY] -i IP_ADDRESS

options:
  -h, --help            show this help message and exit
  -v, --verbose         include the raw message
  -c {mini,plug,touch,v2esp,v2qual,v4,breeze,runner,runnermini,runners11,runners12,light01,light01mini,light02,light02mini,light03,heater}, --device-type {mini,plug,touch,v2esp,v2qual,v4,breeze,runner,runnermini,runners11,runners12,light01,light01mini,light02,light02mini,light03,heater}
                        the type of the device
  -k TOKEN, --token TOKEN
                        the token for communicating with switcher token-based devices
  -d DEVICE_ID, --device-id DEVICE_ID
                        the identification of the device
  -l DEVICE_KEY, --device-key DEVICE_KEY
                        the login key of the device
  -i IP_ADDRESS, --ip-address IP_ADDRESS
                        the ip address assigned to the device

example usage:

switcher-control-device turn_off -c "touch" -d ab1c2d -i "111.222.11.22"

switcher-control-device turn_off -c "touch" -d ab1c2d -l 18 -i "111.222.11.22"
```

### Turn on

```shell title="switcher-control-device turn_on"
$ switcher-control-device turn_on --help

usage: switcher-control-device turn_on [-h] [-v] -c
                                       {mini,plug,touch,v2esp,v2qual,v4,breeze,runner,runnermini,runners11,runners12,light01,light01mini,light02,light02mini,light03,heater}
                                       [-k TOKEN] -d DEVICE_ID [-l DEVICE_KEY] -i IP_ADDRESS [-t [TIMER]]

options:
  -h, --help            show this help message and exit
  -v, --verbose         include the raw message
  -c {mini,plug,touch,v2esp,v2qual,v4,breeze,runner,runnermini,runners11,runners12,light01,light01mini,light02,light02mini,light03,heater}, --device-type {mini,plug,touch,v2esp,v2qual,v4,breeze,runner,runnermini,runners11,runners12,light01,light01mini,light02,light02mini,light03,heater}
                        the type of the device
  -k TOKEN, --token TOKEN
                        the token for communicating with switcher token-based devices
  -d DEVICE_ID, --device-id DEVICE_ID
                        the identification of the device
  -l DEVICE_KEY, --device-key DEVICE_KEY
                        the login key of the device
  -i IP_ADDRESS, --ip-address IP_ADDRESS
                        the ip address assigned to the device
  -t [TIMER], --timer [TIMER]
                        set minutes timer for turn on operation

example usage:

switcher-control-device turn_on -c "touch" -d ab1c2d -i "111.222.11.22"

switcher-control-device turn_on -c "touch" -d ab1c2d -l 18 -i "111.222.11.22"

switcher-control-device turn_on -c "touch" -d ab1c2d -i "111.222.11.22" -t 15
```

### Turn off light

```shell title="switcher-control-device turn_off_light"
$ switcher-control-device turn_off_light --help

usage: switcher-control-device turn_off_light [-h] [-v] -c
                                              {mini,plug,touch,v2esp,v2qual,v4,breeze,runner,runnermini,runners11,runners12,light01,light01mini,light02,light02mini,light03,heater}
                                              [-k TOKEN] -d DEVICE_ID [-l DEVICE_KEY] -i IP_ADDRESS [-x INDEX]

options:
  -h, --help            show this help message and exit
  -v, --verbose         include the raw message
  -c {mini,plug,touch,v2esp,v2qual,v4,breeze,runner,runnermini,runners11,runners12,light01,light01mini,light02,light02mini,light03,heater}, --device-type {mini,plug,touch,v2esp,v2qual,v4,breeze,runner,runnermini,runners11,runners12,light01,light01mini,light02,light02mini,light03,heater}
                        the type of the device
  -k TOKEN, --token TOKEN
                        the token for communicating with switcher token-based devices
  -d DEVICE_ID, --device-id DEVICE_ID
                        the identification of the device
  -l DEVICE_KEY, --device-key DEVICE_KEY
                        the login key of the device
  -i IP_ADDRESS, --ip-address IP_ADDRESS
                        the ip address assigned to the device
  -x INDEX, --index INDEX
                        the circuit number to turn off

example usage:

switcher-control-device turn_off_light -c "runners11" -k "zvVvd7JxtN7CgvkD1Psujw==" -d ab1c2d -i "111.222.11.22" -x 0

switcher-control-device turn_off_light -c "runners11" -k "zvVvd7JxtN7CgvkD1Psujw==" -d ab1c2d -i "111.222.11.22" -x 1

switcher-control-device turn_off_light -c "runners12" -k "zvVvd7JxtN7CgvkD1Psujw==" -d ab1c2d -i "111.222.11.22"

switcher-control-device turn_off_light -c "light01" -k "zvVvd7JxtN7CgvkD1Psujw==" -d ab1c2d -i "111.222.11.22"

switcher-control-device turn_off_light -c "light01mini" -k "zvVvd7JxtN7CgvkD1Psujw==" -d ab1c2d -i "111.222.11.22"

switcher-control-device turn_off_light -c "light02" -k "zvVvd7JxtN7CgvkD1Psujw==" -d ab1c2d -i "111.222.11.22" -x 0

switcher-control-device turn_off_light -c "light02" -k "zvVvd7JxtN7CgvkD1Psujw==" -d ab1c2d -i "111.222.11.22" -x 1

switcher-control-device turn_off_light -c "light02mini" -k "zvVvd7JxtN7CgvkD1Psujw==" -d ab1c2d -i "111.222.11.22" -x 0

switcher-control-device turn_off_light -c "light02mini" -k "zvVvd7JxtN7CgvkD1Psujw==" -d ab1c2d -i "111.222.11.22" -x 1

switcher-control-device turn_off_light -c "light03" -k "zvVvd7JxtN7CgvkD1Psujw==" -d ab1c2d -i "111.222.11.22" -x 0

switcher-control-device turn_off_light -c "light03" -k "zvVvd7JxtN7CgvkD1Psujw==" -d ab1c2d -i "111.222.11.22" -x 1

switcher-control-device turn_off_light -c "light03" -k "zvVvd7JxtN7CgvkD1Psujw==" -d ab1c2d -i "111.222.11.22" -x 2
```

### Turn on light

```shell title="switcher-control-device turn_on_light"
$ switcher-control-device turn_on_light --help

usage: switcher-control-device turn_on_light [-h] [-v] -c
                                             {mini,plug,touch,v2esp,v2qual,v4,breeze,runner,runnermini,runners11,runners12,light01,light01mini,light02,light02mini,light03,heater}
                                             [-k TOKEN] -d DEVICE_ID [-l DEVICE_KEY] -i IP_ADDRESS [-x INDEX]

options:
  -h, --help            show this help message and exit
  -v, --verbose         include the raw message
  -c {mini,plug,touch,v2esp,v2qual,v4,breeze,runner,runnermini,runners11,runners12,light01,light01mini,light02,light02mini,light03,heater}, --device-type {mini,plug,touch,v2esp,v2qual,v4,breeze,runner,runnermini,runners11,runners12,light01,light01mini,light02,light02mini,light03,heater}
                        the type of the device
  -k TOKEN, --token TOKEN
                        the token for communicating with switcher token-based devices
  -d DEVICE_ID, --device-id DEVICE_ID
                        the identification of the device
  -l DEVICE_KEY, --device-key DEVICE_KEY
                        the login key of the device
  -i IP_ADDRESS, --ip-address IP_ADDRESS
                        the ip address assigned to the device
  -x INDEX, --index INDEX
                        the circuit number to turn on

example usage:

switcher-control-device turn_on_light -c "runners11" -k "zvVvd7JxtN7CgvkD1Psujw==" -d ab1c2d -i "111.222.11.22" -x 0

switcher-control-device turn_on_light -c "runners11" -k "zvVvd7JxtN7CgvkD1Psujw==" -d ab1c2d -i "111.222.11.22" -x 1

switcher-control-device turn_on_light -c "runners12" -k "zvVvd7JxtN7CgvkD1Psujw==" -d ab1c2d -i "111.222.11.22"

switcher-control-device turn_on_light -c "light01" -k "zvVvd7JxtN7CgvkD1Psujw==" -d ab1c2d -i "111.222.11.22"

switcher-control-device turn_on_light -c "light01mini" -k "zvVvd7JxtN7CgvkD1Psujw==" -d ab1c2d -i "111.222.11.22"

switcher-control-device turn_on_light -c "light02" -k "zvVvd7JxtN7CgvkD1Psujw==" -d ab1c2d -i "111.222.11.22" -x 0

switcher-control-device turn_on_light -c "light02" -k "zvVvd7JxtN7CgvkD1Psujw==" -d ab1c2d -i "111.222.11.22" -x 1

switcher-control-device turn_on_light -c "light02mini" -k "zvVvd7JxtN7CgvkD1Psujw==" -d ab1c2d -i "111.222.11.22" -x 0

switcher-control-device turn_on_light -c "light02mini" -k "zvVvd7JxtN7CgvkD1Psujw==" -d ab1c2d -i "111.222.11.22" -x 1

switcher-control-device turn_on_light -c "light03" -k "zvVvd7JxtN7CgvkD1Psujw==" -d ab1c2d -i "111.222.11.22" -x 0

switcher-control-device turn_on_light -c "light03" -k "zvVvd7JxtN7CgvkD1Psujw==" -d ab1c2d -i "111.222.11.22" -x 1

switcher-control-device turn_on_light -c "light03" -k "zvVvd7JxtN7CgvkD1Psujw==" -d ab1c2d -i "111.222.11.22" -x 2
```

### Turn off shutter child lock

```shell title="switcher-control-device turn_off_shutter_child_lock"
$ switcher-control-device turn_off_shutter_child_lock --help

usage: switcher-control-device turn_off_shutter_child_lock [-h] [-v] -c
                                                           {mini,plug,touch,v2esp,v2qual,v4,breeze,runner,runnermini,runners11,runners12,light01,light01mini,light02,light02mini,light03,heater}
                                                           [-k TOKEN] -d DEVICE_ID [-l DEVICE_KEY] -i IP_ADDRESS
                                                           [-x INDEX]

options:
  -h, --help            show this help message and exit
  -v, --verbose         include the raw message
  -c {mini,plug,touch,v2esp,v2qual,v4,breeze,runner,runnermini,runners11,runners12,light01,light01mini,light02,light02mini,light03,heater}, --device-type {mini,plug,touch,v2esp,v2qual,v4,breeze,runner,runnermini,runners11,runners12,light01,light01mini,light02,light02mini,light03,heater}
                        the type of the device
  -k TOKEN, --token TOKEN
                        the token for communicating with switcher token-based devices
  -d DEVICE_ID, --device-id DEVICE_ID
                        the identification of the device
  -l DEVICE_KEY, --device-key DEVICE_KEY
                        the login key of the device
  -i IP_ADDRESS, --ip-address IP_ADDRESS
                        the ip address assigned to the device
  -x INDEX, --index INDEX
                        the circuit number to turn off

example usage:

switcher-control-device turn_off_shutter_child_lock -c "runner" -k "zvVvd7JxtN7CgvkD1Psujw==" -d ab1c2d -i "111.222.11.22"

switcher-control-device turn_off_shutter_child_lock -c "runnermini" -k "zvVvd7JxtN7CgvkD1Psujw==" -d ab1c2d -i "111.222.11.22"

switcher-control-device turn_off_shutter_child_lock -c "runners11" -k "zvVvd7JxtN7CgvkD1Psujw==" -d ab1c2d -i "111.222.11.22" -x 0

switcher-control-device turn_off_shutter_child_lock -c "runners11" -k "zvVvd7JxtN7CgvkD1Psujw==" -d ab1c2d -i "111.222.11.22" -x 1

switcher-control-device turn_off_shutter_child_lock -c "runners12" -k "zvVvd7JxtN7CgvkD1Psujw==" -d ab1c2d -i "111.222.11.22"
```

### Turn on shutter child lock

```shell title="switcher-control-device turn_on_shutter_child_lock"
$ switcher-control-device turn_on_shutter_child_lock --help

usage: switcher-control-device turn_on_shutter_child_lock [-h] [-v] -c
                                                          {mini,plug,touch,v2esp,v2qual,v4,breeze,runner,runnermini,runners11,runners12,light01,light01mini,light02,light02mini,light03,heater}
                                                          [-k TOKEN] -d DEVICE_ID [-l DEVICE_KEY] -i IP_ADDRESS
                                                          [-x INDEX]

options:
  -h, --help            show this help message and exit
  -v, --verbose         include the raw message
  -c {mini,plug,touch,v2esp,v2qual,v4,breeze,runner,runnermini,runners11,runners12,light01,light01mini,light02,light02mini,light03,heater}, --device-type {mini,plug,touch,v2esp,v2qual,v4,breeze,runner,runnermini,runners11,runners12,light01,light01mini,light02,light02mini,light03,heater}
                        the type of the device
  -k TOKEN, --token TOKEN
                        the token for communicating with switcher token-based devices
  -d DEVICE_ID, --device-id DEVICE_ID
                        the identification of the device
  -l DEVICE_KEY, --device-key DEVICE_KEY
                        the login key of the device
  -i IP_ADDRESS, --ip-address IP_ADDRESS
                        the ip address assigned to the device
  -x INDEX, --index INDEX
                        the circuit number to turn on

example usage:

switcher-control-device turn_on_shutter_child_lock -c "runner" -k "zvVvd7JxtN7CgvkD1Psujw==" -d ab1c2d -i "111.222.11.22"

switcher-control-device turn_on_shutter_child_lock -c "runnermini" -k "zvVvd7JxtN7CgvkD1Psujw==" -d ab1c2d -i "111.222.11.22"

switcher-control-device turn_on_shutter_child_lock -c "runners11" -k "zvVvd7JxtN7CgvkD1Psujw==" -d ab1c2d -i "111.222.11.22" -x 0

switcher-control-device turn_on_shutter_child_lock -c "runners11" -k "zvVvd7JxtN7CgvkD1Psujw==" -d ab1c2d -i "111.222.11.22" -x 1

switcher-control-device turn_on_shutter_child_lock -c "runners12" -k "zvVvd7JxtN7CgvkD1Psujw==" -d ab1c2d -i "111.222.11.22"
```

### Get heater state

```shell title="switcher-control-device get_heater_state"
$ switcher-control-device get_heater_state --help

usage: switcher-control-device get_heater_state [-h] [-v] -c
                                                {mini,plug,touch,v2esp,v2qual,v4,breeze,runner,runnermini,runners11,runners12,light01,light01mini,light02,light02mini,light03,heater}
                                                [-k TOKEN] -d DEVICE_ID [-l DEVICE_KEY] -i IP_ADDRESS

options:
  -h, --help            show this help message and exit
  -v, --verbose         include the raw message
  -c {mini,plug,touch,v2esp,v2qual,v4,breeze,runner,runnermini,runners11,runners12,light01,light01mini,light02,light02mini,light03,heater}, --device-type {mini,plug,touch,v2esp,v2qual,v4,breeze,runner,runnermini,runners11,runners12,light01,light01mini,light02,light02mini,light03,heater}
                        the type of the device
  -k TOKEN, --token TOKEN
                        the token for communicating with switcher token-based devices
  -d DEVICE_ID, --device-id DEVICE_ID
                        the identification of the device
  -l DEVICE_KEY, --device-key DEVICE_KEY
                        the login key of the device
  -i IP_ADDRESS, --ip-address IP_ADDRESS
                        the ip address assigned to the device

example usage:

switcher-control-device get_heater_state -c "heater" -k "zvVvd7JxtN7CgvkD1Psujw==" -d ab1c2d -i "111.222.11.22"
```

## Discover devices

Use to discover devices and their states.

```shell title="switcher-discover-devices"
$ switcher-discover-devices --help

usage: switcher-discover-devices [-h] [delay]

Discover and print info of Switcher devices

positional arguments:
  delay       number of seconds to run, defaults to 60

options:
  -h, --help  show this help message and exit

Executing this script will print a serialized version of the discovered Switcher
devices broadcasting on the local network for 60 seconds.
You can change the delay by passing an int argument: switcher-discover-devices 30

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
Print devices for 30 seconds:
    switcher-discover-devices 30
```

## Get device login key

Use to fetch the login key from devices.

```shell title="switcher-get-device-login-key"
$ switcher-get-device-login-key --help

usage: switcher-get-device-login-key [-h] -i IP_ADDRESS -p {20002,10002,20003,10003}

Get the login key of your Switcher device

options:
  -h, --help            show this help message and exit
  -i IP_ADDRESS, --ip-address IP_ADDRESS
                        the ip address assigned to the device
  -p {20002,10002,20003,10003}, --port {20002,10002,20003,10003}
                        the UDP port of the device

example usage:

switcher-get-device-login-key -i "111.222.11.22" -p 10002
```

## Validate token

Use to validate your device token.

```shell title="switcher-validate-token"
$ switcher-validate-token --help

usage: switcher-validate-token [-h] -u USERNAME -t TOKEN

Validate a Token from Switcher by username and token

options:
  -h, --help            show this help message and exit
  -u USERNAME, --username USERNAME
                        the username of the user (Email address)
  -t TOKEN, --token TOKEN
                        the token of the user sent by Email

example usage:

switcher-validate-token -u "email" -t "YOUR_TOKEN"

switcher-validate-token --username "email" --token "YOUR_TOKEN"
```
