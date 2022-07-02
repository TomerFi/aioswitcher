# Switcher Python Integration</br>[![pypi-version]][11] [![pypi-downloads]][11] [![license-badge]][4]

[![gh-build-status]][7] [![gh-pages-status]][8] [![codecov]][3]

PyPi module integrating with various [Switcher][12] devices.</br>
Check out the [wiki pages][0] for a list of supported devices.

## Install

```shell
pip install aioswitcher
```

## Usage Example

```python
async with SwitcherApi(device_ip, device_id) as swapi:
    # get the device state
    state_response = await swapi.get_state()

    # control the device on for 15 minutes and then turn it off
    await swapi.control_device(Command.ON, 15)
    await swapi.control_device(Command.OFF)

    # create a new recurring schedule
    await swapi.create_schedule("13:00", "14:30", {Days.SUNDAY, Days.FRIDAY})


# control Type 2 devices such as Breeze, Runner and Runner Mini

# control a breeze device
async with SwitcherType2Api(device_ip, device_id) as api_type2:
    # get the Breeze device state
    resp: SwitcherThermostatStateResponse = await api_type2.get_breeze_state()

    # initialize the Breeze RemoteManager
    rm = BreezeRemoteManager()

    # get the remote structure (downloaded from the internet)
    async with ClientSession() as session:
    remote: BreezeRemote = await rm.get_remote(resp.remote_id, api_type2, session)

    # prepare a control command that turns on the Breeze 
    # (24 degree (Celsius), cooling and high Fan level with vertical swing)  
    command = remote.get_command(
          DeviceState.ON, 
          ThermostatMode.COOL, 
          24, 
          ThermostatFanLevel.HIGH, 
          ThermostatSwing.ON,
          resp.state
      )

    # send command to the device
    await api_type2.control_breeze_device(command)
  
# control Runner device  
async with SwitcherType2Api(device_ip, device_id) as api:
  # get the runner state
  state_response: SwitcherShutterStateResponse = api.get_shutter_state()

  # open the shutter all the way up
  await api.set_position(100)
  # stop the shutter from rolling
  await api.stop()
  # set the shutter position to 30% opened
  await api.set_position(30)
  # close the shutter all the way down
  await api.set_position(0)

```

Check out the [documentation][8] for a more detailed usage section.

## Command Line Helper Scripts

- [discover_devices.py](scripts/discover_devices.py) can discover devices and their
  states.
- [control_device.py](scripts/control_device.py) can control a device.

## Contributing

The contributing guidelines are [here](.github/CONTRIBUTING.md)

## Code of Conduct

The code of conduct is [here](.github/CODE_OF_CONDUCT.md)

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
[2]: https://github.com/TomerFi/aioswitcher/releases
[3]: https://codecov.io/gh/TomerFi/aioswitcher
[4]: https://github.com/TomerFi/aioswitcher
[7]: https://github.com/TomerFi/aioswitcher/actions/workflows/stage.yml
[8]: https://aioswitcher.tomfi.info/
[11]: https://pypi.org/project/aioswitcher
[12]: https://www.switcher.co.il/
[14]: https://github.com/NightRang3r/Switcher-V2-Python
<!-- Badges Links -->
[codecov]: https://codecov.io/gh/TomerFi/aioswitcher/graph/badge.svg
[gh-build-status]: https://github.com/TomerFi/aioswitcher/actions/workflows/stage.yml/badge.svg
[gh-pages-status]: https://github.com/TomerFi/aioswitcher/actions/workflows/pages.yml/badge.svg
[license-badge]: https://img.shields.io/github/license/tomerfi/aioswitcher
[pypi-downloads]: https://img.shields.io/pypi/dm/aioswitcher.svg?logo=pypi&color=1082C2
[pypi-version]: https://img.shields.io/pypi/v/aioswitcher?logo=pypi
