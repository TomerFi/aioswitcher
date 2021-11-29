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
```

Check out the [documentation][8] for a more detailed usage section.

## Command Line Helper Scripts

- [discover_devices.py](scripts/discover_devices.py) can discover devices and their
  states.
- [control_device.py](scripts/control_device.py) can to control a device.

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

<!-- ALL-CONTRIBUTORS-LIST:END -->

<!-- Real Links -->
[0]: https://github.com/TomerFi/aioswitcher/wiki
[1]: https://allcontributors.org/docs/en/emoji-key
[2]: https://github.com/TomerFi/aioswitcher/releases
[3]: https://codecov.io/gh/TomerFi/aioswitcher
[4]: https://github.com/TomerFi/aioswitcher
[7]: https://github.com/TomerFi/aioswitcher/actions/workflows/pre_release.yml
[8]: https://aioswitcher.tomfi.info/
[11]: https://pypi.org/project/aioswitcher
[12]: https://www.switcher.co.il/
[13]: https://github.com/NightRang3r
[14]: https://github.com/NightRang3r/Switcher-V2-Python
[15]: https://github.com/thecode
<!-- Badges Links -->
[codecov]: https://codecov.io/gh/TomerFi/aioswitcher/graph/badge.svg
[gh-build-status]: https://github.com/TomerFi/aioswitcher/actions/workflows/pre_release.yml/badge.svg
[gh-pages-status]: https://github.com/TomerFi/aioswitcher/actions/workflows/pages_deploy.yml/badge.svg
[license-badge]: https://img.shields.io/github/license/tomerfi/aioswitcher
[pypi-downloads]: https://img.shields.io/pypi/dm/aioswitcher.svg?logo=pypi&color=1082C2
[pypi-version]: https://img.shields.io/pypi/v/aioswitcher?logo=pypi
