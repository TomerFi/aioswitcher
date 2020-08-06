# Switcher Water Heater Unofficial Bridge and API</br>[![pypi-version]][11] [![pypi-downloads]][11] [![license-badge]][4] [![conventional-commits]][0]

[![gh-build-status]][7] [![read-the-docs]][8] [![codecov]][3] [![fossa-status]][5]

PyPi module named [aioswitcher][11] for integrating with the [Switcher Water Heater](https://www.switcher.co.il/).</br>
Please check out the [documentation][8].

## Install

```shell
pip install aioswitcher
```

## Usage Example

Please check out the [documentation][8] for the full usage section.

```python
async with SwitcherV2Api(
        your_loop, ip_address, phone_id,
        device_id, device_password) as swapi:
    # get the device state
    state_response = await swapi.get_state()

    # control the device: on / off / on + 30 minutes timer
    turn_on_response = await swapi.control_device(consts.COMMAND_ON)
    turn_off_response = await swapi.control_device(consts.COMMAND_OFF)
    turn_on_30_min_response = await swapi.control_device(consts.COMMAND_ON, '30')
```

## Contributing

The contributing guidelines are [here](.github/CONTRIBUTING.md)

## Code of Conduct

The code of conduct is [here](.github/CODE_OF_CONDUCT.md)

<!-- Real Links -->
[0]: https://conventionalcommits.org
[2]: https://github.com/TomerFi/aioswitcher/releases
[3]: https://codecov.io/gh/TomerFi/aioswitcher
[4]: https://github.com/TomerFi/aioswitcher
[5]: https://app.fossa.com/projects/git%2Bgithub.com%2FTomerFi%2Faioswitcher?ref=badge_shield
[7]: https://github.com/TomerFi/aioswitcher/actions?query=workflow%3ABuild
[8]: https://aioswitcher.tomfi.info/
[11]: https://pypi.org/project/aioswitcher
<!-- Badges Links -->
[codecov]: https://codecov.io/gh/TomerFi/aioswitcher/graph/badge.svg
[conventional-commits]: https://img.shields.io/badge/Conventional%20Commits-1.0.0-yellow.svg
[fossa-status]: https://app.fossa.com/api/projects/git%2Bgithub.com%2FTomerFi%2Faioswitcher.svg?type=shield
[gh-build-status]: https://github.com/TomerFi/aioswitcher/workflows/Build/badge.svg
[license-badge]: https://img.shields.io/github/license/tomerfi/aioswitcher
[pypi-downloads]: https://img.shields.io/pypi/dm/aioswitcher.svg?logo=pypi&color=1082C2
[pypi-version]: https://img.shields.io/pypi/v/aioswitcher?logo=pypi
[read-the-docs]: https://readthedocs.org/projects/aioswitcher/badge/?version=stable
