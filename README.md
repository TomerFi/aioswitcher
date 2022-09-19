<!-- markdownlint-disable MD033 -->
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
  <td><a href="https://github.com/TomerFi/aioswitcher/blob/dev/.github/CONTRIBUTING.md">Contributing</a></td>
  <td><a href="https://github.com/TomerFi/.github/blob/main/.github/CODE_OF_CONDUCT.md">Code of Conduct</a></td>
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
asyncio.get_event_loop().run_until_complete(print_devices(60))
```

</details>

<details>
  <summary>Power Plug API</summary>

  ```python
  async def control_power_plug(device_ip, device_id) :
      # for connecting to a device we need its id and ip address
      async with SwitcherType1Api(device_ip, device_id) as api:
          # get the device current state
          await api.get_state()
          # turn the device on
          await api.control_device(Command.ON)
          # turn the device off
          await api.control_device(Command.OFF)
          # set the device name to 'my new name'
          await api.set_device_name("my new name")

  asyncio.get_event_loop().run_until_complete(control_power_plug("111.222.11.22", "ab1c2d"))
  ```

</details>

<details>
  <summary>Water Heater API</summary>

  ```python
  async def control_water_heater(device_ip, device_id) :
      # for connecting to a device we need its id and ip address
      async with SwitcherType1Api(device_ip, device_id) as api:
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

  asyncio.get_event_loop().run_until_complete(control_water_heater("111.222.11.22", "ab1c2d"))
  ```

</details>

<details>
  <summary>Runner API</summary>

  ```python
  async def control_runner(device_ip, device_id) :
      # for connecting to a device we need its id and ip address
      async with SwitcherType2Api(device_ip, device_id) as api:
          # get the device current state
          await api.get_shutter_state()
          # open the shutter to 30%
          await api.set_position(30)
          # stop the shutter if currently rolling
          await api.stop()

  asyncio.get_event_loop().run_until_complete(control_runner("111.222.11.22", "ab1c2d"))
  ```

</details>

<details>
  <summary>Breeze API</summary>

  ```python
  async def control_breeze(device_ip, device_id, remote_manager, remote_id) :
      # for connecting to a device we need its id and ip address
      async with SwitcherType2Api(device_ip, device_id) as api:
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
  asyncio.get_event_loop().run_until_complete(control_breeze("111.222.11.22", "ab1c2d", remote_manager, "DLK65863"))
  ```

</details>

## Command Line Helper Scripts

- [discover_devices.py](scripts/discover_devices.py) can discover devices and their
  states.
- [control_device.py](scripts/control_device.py) can control a device.

## Disclaimer

This is **NOT** an official module and it is **NOT** officially supported by the vendor.</br>
That said, thanks are in order to all the people at [Switcher][12] for their cooperation and general support.

## Contributors

Thanks goes to these wonderful people ([emoji key][1]):

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tr>
    <td align="center"><a href="https://github.com/aviadgolan"><img src="https://avatars.githubusercontent.com/u/17742111?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Aviad Golan</b></sub></a><br /><a href="#data-AviadGolan" title="Data">🔣</a></td>
    <td align="center"><a href="https://github.com/dolby360"><img src="https://avatars.githubusercontent.com/u/22151399?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Dolev Ben Aharon</b></sub></a><br /><a href="https://github.com/TomerFi/aioswitcher/commits?author=dolby360" title="Documentation">📖</a></td>
    <td align="center"><a href="http://fabian-affolter.ch/blog/"><img src="https://avatars.githubusercontent.com/u/116184?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Fabian Affolter</b></sub></a><br /><a href="https://github.com/TomerFi/aioswitcher/commits?author=fabaff" title="Code">💻</a></td>
    <td align="center"><a href="https://github.com/OrBin"><img src="https://avatars.githubusercontent.com/u/6897234?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Or Bin</b></sub></a><br /><a href="https://github.com/TomerFi/aioswitcher/commits?author=OrBin" title="Code">💻</a></td>
    <td align="center"><a href="http://exploit.co.il"><img src="https://avatars.githubusercontent.com/u/1768915?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Shai rod</b></sub></a><br /><a href="#data-nightrang3r" title="Data">🔣</a></td>
    <td align="center"><a href="https://github.com/thecode"><img src="https://avatars.githubusercontent.com/u/1858925?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Shay Levy</b></sub></a><br /><a href="https://github.com/TomerFi/aioswitcher/commits?author=thecode" title="Code">💻</a> <a href="#ideas-thecode" title="Ideas, Planning, & Feedback">🤔</a> <a href="#maintenance-thecode" title="Maintenance">🚧</a></td>
    <td align="center"><a href="https://github.com/dmatik"><img src="https://avatars.githubusercontent.com/u/5577386?v=4?s=100" width="100px;" alt=""/><br /><sub><b>dmatik</b></sub></a><br /><a href="#blog-dmatik" title="Blogposts">📝</a> <a href="#ideas-dmatik" title="Ideas, Planning, & Feedback">🤔</a> <a href="#userTesting-dmatik" title="User Testing">📓</a></td>
  </tr>
  <tr>
    <td align="center"><a href="https://github.com/jafar-atili"><img src="https://avatars.githubusercontent.com/u/19508787?v=4?s=100" width="100px;" alt=""/><br /><sub><b>jafar-atili</b></sub></a><br /><a href="https://github.com/TomerFi/aioswitcher/commits?author=jafar-atili" title="Code">💻</a> <a href="https://github.com/TomerFi/aioswitcher/commits?author=jafar-atili" title="Documentation">📖</a></td>
  </tr>
</table>

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->

<!-- Real Links -->
[0]: https://github.com/TomerFi/aioswitcher/wiki
[1]: https://allcontributors.org/docs/en/emoji-key
[3]: https://codecov.io/gh/TomerFi/aioswitcher
[4]: https://github.com/TomerFi/aioswitcher
[7]: https://github.com/TomerFi/aioswitcher/actions/workflows/stage.yml
[8]: https://aioswitcher.tomfi.info/
[11]: https://pypi.org/project/aioswitcher
[12]: https://www.switcher.co.il/
<!-- Badges Links -->
[codecov]: https://codecov.io/gh/TomerFi/aioswitcher/graph/badge.svg
[gh-build-status]: https://github.com/TomerFi/aioswitcher/actions/workflows/stage.yml/badge.svg
[gh-pages-status]: https://github.com/TomerFi/aioswitcher/actions/workflows/pages.yml/badge.svg
[license-badge]: https://img.shields.io/github/license/tomerfi/aioswitcher
[pypi-downloads]: https://img.shields.io/pypi/dm/aioswitcher.svg?logo=pypi&color=1082C2
[pypi-version]: https://img.shields.io/pypi/v/aioswitcher?logo=pypi
