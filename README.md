# Switcher Python Integration</br>[![pypi-version]][11] [![pypi-downloads]][11] [![license-badge]][4]

[![gh-build-status]][7] [![gh-pages-status]][8] [![codecov]][3]

PyPi module integrating with various [Switcher][12] devices.</br>
Check out the [wiki pages][0] for a list of supported devices.

```shell
pip install aioswitcher
```

<table>
  <td><a href="https://aioswitcher.tomfi.info/">Documentation</a></td>
  <td><a href="https://github.com/TomerFi/aioswitcher/wiki">Wiki</a></td>
  <td><a href="https://github.com/TomerFi/aioswitcher/blob/dev/CONTRIBUTING.md">Contributing</a></td>
</table>

## Example Usage

<details>
  <summary>State Bridge</summary>

```python
async def print_devices(delay):
    def on_device_found_callback(device):
        # a switcher device will broadcast a state message approximately every 4 seconds
        print(asdict(device))

    async with SwitcherBridge(on_device_found_callback):
        await asyncio.sleep(delay)

# run the bridge for 60 seconds
asyncio.run(print_devices(60))
```

</details>

<details>
  <summary>Power Plug API</summary>

  ```python
  async def control_power_plug(device_type, device_ip, device_id, device_key) :
      # for connecting to a device we need its type, id, login key and ip address
      async with SwitcherType1Api(device_type, device_ip, device_id, device_key) as api:
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

</details>

<details>
  <summary>Water Heater API</summary>

  ```python
  async def control_water_heater(device_type, device_ip, device_id, device_key) :
      # for connecting to a device we need its type, id, login key and ip address
      async with SwitcherType1Api(device_type, device_ip, device_id, device_key) as api:
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
          await api.get_schedules()
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

</details>

<details>
  <summary>Runner API</summary>

  ```python
  async def control_runner(device_type, device_ip, device_id, device_key, token) :
      # for connecting to a device we need its type, id, login key and ip address
      async with SwitcherType2Api(device_type, device_ip, device_id, device_key, token) as api:
          # get the device current state
          await api.get_shutter_state()
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

</details>

<details>
  <summary>Breeze API</summary>

  ```python
  async def control_breeze(device_type, device_ip, device_id, device_key, remote_manager, remote_id) :
      # for connecting to a device we need its type, id, login key and ip address
      async with SwitcherType2Api(device_type, device_ip, device_id, device_key) as api:
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

</details>

<details>
  <summary>Light API</summary>

  ```python
  async def control_light(device_type, device_ip, device_id, device_key, token) :
      # for connecting to a device we need its type, id, login key and ip address
      async with SwitcherType2Api(device_type, device_ip, device_id, device_key, token) as api:
          # get the device current state
          await api.get_light_state()
          # turn on the light, circuit number is 0 (Only for Runner S11 and Runner S12)
          await api.set_light(DeviceState.ON, 0)
          # turn off the light, circuit number is 0 (Only for Runner S11 and Runner S12)
          await api.set_light(DeviceState.OFF, 0)

  asyncio.run(control_light(DeviceType.LIGHT_SL01, "111.222.11.22", "ab1c2d", "00", "zvVvd7JxtN7CgvkD1Psujw=="))
  asyncio.run(control_light(DeviceType.LIGHT_SL01_MINI, "111.222.11.22", "ab1c2d", "00", "zvVvd7JxtN7CgvkD1Psujw=="))
  asyncio.run(control_light(DeviceType.LIGHT_SL02, "111.222.11.22", "ab1c2d", "00", "zvVvd7JxtN7CgvkD1Psujw=="))
  asyncio.run(control_light(DeviceType.LIGHT_SL02_MINI, "111.222.11.22", "ab1c2d", "00", "zvVvd7JxtN7CgvkD1Psujw=="))
  ```

</details>

## Command Line Helper Scripts

- [discover_devices.py](https://github.com/TomerFi/aioswitcher/blob/dev/scripts/discover_devices.py) can discover devices and their states (can be run by `poetry run discover_devices`).
- [control_device.py](https://github.com/TomerFi/aioswitcher/blob/dev/scripts/control_device.py) can control a device (can be run by `poetry run control_device`).
- [get_device_login_key.py](https://github.com/TomerFi/aioswitcher/blob/dev/scripts/get_device_login_key) can get a device login key (can be run by `poetry run get_device_login_key`).
- [validate_token.py](https://github.com/TomerFi/aioswitcher/blob/dev/scripts/validate_token.py) can validate a device token which is a must for newer devices, used for communicating with devices (can be run by `poetry run validate_token`).

## Disclaimer

This is **NOT** an official module and it is **NOT** officially supported by the vendor.</br>
That said, thanks are in order to all the people at [Switcher][12] for their cooperation and general support.

## Contributors [![all-contributors]][2]

Thanks goes to these wonderful people ([emoji key][1]):

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tbody>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/aviadgolan"><img src="https://avatars.githubusercontent.com/u/17742111?v=4?s=100" width="100px;" alt="Aviad Golan"/><br /><sub><b>Aviad Golan</b></sub></a><br /><a href="#data-AviadGolan" title="Data">🔣</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/dolby360"><img src="https://avatars.githubusercontent.com/u/22151399?v=4?s=100" width="100px;" alt="Dolev Ben Aharon"/><br /><sub><b>Dolev Ben Aharon</b></sub></a><br /><a href="https://github.com/TomerFi/aioswitcher/commits?author=dolby360" title="Documentation">📖</a></td>
      <td align="center" valign="top" width="14.28%"><a href="http://fabian-affolter.ch/blog/"><img src="https://avatars.githubusercontent.com/u/116184?v=4?s=100" width="100px;" alt="Fabian Affolter"/><br /><sub><b>Fabian Affolter</b></sub></a><br /><a href="https://github.com/TomerFi/aioswitcher/commits?author=fabaff" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/oranja"><img src="https://avatars.githubusercontent.com/u/679184?v=4?s=100" width="100px;" alt="Itzik Ephraim"/><br /><sub><b>Itzik Ephraim</b></sub></a><br /><a href="https://github.com/TomerFi/aioswitcher/commits?author=oranja" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/Kesav890"><img src="https://avatars.githubusercontent.com/u/82559951?v=4?s=100" width="100px;" alt="Kesav890"/><br /><sub><b>Kesav890</b></sub></a><br /><a href="https://github.com/TomerFi/aioswitcher/commits?author=Kesav890" title="Documentation">📖</a></td>
      <td align="center" valign="top" width="14.28%"><a href="http://liad.avrah.am"><img src="https://avatars.githubusercontent.com/u/7263223?v=4?s=100" width="100px;" alt="Liad Avraham"/><br /><sub><b>Liad Avraham</b></sub></a><br /><a href="https://github.com/TomerFi/aioswitcher/commits?author=liadav" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/cdce8p"><img src="https://avatars.githubusercontent.com/u/30130371?v=4?s=100" width="100px;" alt="Marc Mueller"/><br /><sub><b>Marc Mueller</b></sub></a><br /><a href="https://github.com/TomerFi/aioswitcher/commits?author=cdce8p" title="Code">💻</a></td>
    </tr>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/OrBin"><img src="https://avatars.githubusercontent.com/u/6897234?v=4?s=100" width="100px;" alt="Or Bin"/><br /><sub><b>Or Bin</b></sub></a><br /><a href="https://github.com/TomerFi/aioswitcher/commits?author=OrBin" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/5c077m4n"><img src="https://avatars.githubusercontent.com/u/35409124?v=4?s=100" width="100px;" alt="Roeeeee"/><br /><sub><b>Roeeeee</b></sub></a><br /><a href="https://github.com/TomerFi/aioswitcher/commits?author=5c077m4n" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="http://exploit.co.il"><img src="https://avatars.githubusercontent.com/u/1768915?v=4?s=100" width="100px;" alt="Shai rod"/><br /><sub><b>Shai rod</b></sub></a><br /><a href="#data-nightrang3r" title="Data">🔣</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/thecode"><img src="https://avatars.githubusercontent.com/u/1858925?v=4?s=100" width="100px;" alt="Shay Levy"/><br /><sub><b>Shay Levy</b></sub></a><br /><a href="https://github.com/TomerFi/aioswitcher/commits?author=thecode" title="Code">💻</a> <a href="#ideas-thecode" title="Ideas, Planning, & Feedback">🤔</a> <a href="#maintenance-thecode" title="Maintenance">🚧</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/YogevBokobza"><img src="https://avatars.githubusercontent.com/u/22839127?v=4?s=100" width="100px;" alt="YogevBokobza"/><br /><sub><b>YogevBokobza</b></sub></a><br /><a href="https://github.com/TomerFi/aioswitcher/commits?author=YogevBokobza" title="Code">💻</a> <a href="https://github.com/TomerFi/aioswitcher/commits?author=YogevBokobza" title="Tests">⚠️</a> <a href="#maintenance-YogevBokobza" title="Maintenance">🚧</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/gmyuval"><img src="https://avatars.githubusercontent.com/u/28506179?v=4?s=100" width="100px;" alt="Yuval Moran"/><br /><sub><b>Yuval Moran</b></sub></a><br /><a href="https://github.com/TomerFi/aioswitcher/commits?author=gmyuval" title="Code">💻</a> <a href="https://github.com/TomerFi/aioswitcher/commits?author=gmyuval" title="Tests">⚠️</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/ayal"><img src="https://avatars.githubusercontent.com/u/121446?v=4?s=100" width="100px;" alt="ayal"/><br /><sub><b>ayal</b></sub></a><br /><a href="https://github.com/TomerFi/aioswitcher/issues?q=author%3Aayal" title="Bug reports">🐛</a> <a href="https://github.com/TomerFi/aioswitcher/commits?author=ayal" title="Code">💻</a></td>
    </tr>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/dmatik"><img src="https://avatars.githubusercontent.com/u/5577386?v=4?s=100" width="100px;" alt="dmatik"/><br /><sub><b>dmatik</b></sub></a><br /><a href="#blog-dmatik" title="Blogposts">📝</a> <a href="#ideas-dmatik" title="Ideas, Planning, & Feedback">🤔</a> <a href="#userTesting-dmatik" title="User Testing">📓</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/epenet"><img src="https://avatars.githubusercontent.com/u/6771947?v=4?s=100" width="100px;" alt="epenet"/><br /><sub><b>epenet</b></sub></a><br /><a href="https://github.com/TomerFi/aioswitcher/issues?q=author%3Aepenet" title="Bug reports">🐛</a> <a href="https://github.com/TomerFi/aioswitcher/commits?author=epenet" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/jafar-atili"><img src="https://avatars.githubusercontent.com/u/19508787?v=4?s=100" width="100px;" alt="jafar-atili"/><br /><sub><b>jafar-atili</b></sub></a><br /><a href="https://github.com/TomerFi/aioswitcher/commits?author=jafar-atili" title="Code">💻</a> <a href="https://github.com/TomerFi/aioswitcher/commits?author=jafar-atili" title="Documentation">📖</a></td>
    </tr>
  </tbody>
</table>

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->

<!-- Real Links -->
[0]: https://github.com/TomerFi/aioswitcher/wiki
[1]: https://allcontributors.org/docs/en/emoji-key
[2]: https://allcontributors.org
[3]: https://codecov.io/gh/TomerFi/aioswitcher
[4]: https://github.com/TomerFi/aioswitcher
[7]: https://github.com/TomerFi/aioswitcher/actions/workflows/stage.yml
[8]: https://aioswitcher.tomfi.info/
[11]: https://pypi.org/project/aioswitcher
[12]: https://www.switcher.co.il/
<!-- Badges Links -->
[all-contributors]: https://img.shields.io/github/all-contributors/tomerfi/aioswitcher?color=ee8449&style=flat-square
[codecov]: https://codecov.io/gh/TomerFi/aioswitcher/graph/badge.svg
[gh-build-status]: https://github.com/TomerFi/aioswitcher/actions/workflows/stage.yml/badge.svg
[gh-pages-status]: https://github.com/TomerFi/aioswitcher/actions/workflows/pages.yml/badge.svg
[license-badge]: https://img.shields.io/github/license/tomerfi/aioswitcher
[pypi-downloads]: https://img.shields.io/pypi/dm/aioswitcher.svg?logo=pypi&color=1082C2
[pypi-version]: https://img.shields.io/pypi/v/aioswitcher?logo=pypi
