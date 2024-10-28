# Switcher Python Integration

[![pypi-ver-badge]][pypi-aioswitcher] [![pypi-down-badge]][pypi-aioswitcher] [![license-badge]][repo-aioswitcher]<br/>
[![gh-build-badge]][ci-stage] [![pages-badge]][docs-aioswitcher] [![codecov-badge]][codecov-aioswitcher]

PyPi module integrating with various [Switcher][switcher] devices.</br>

```shell
pip install aioswitcher
```

Check the docs: [https://aioswitcher.tomfi.info][docs-aioswitcher]

Looking for a containerized solution? Check [https://switcher-webapi.tomfi.info][switcher-webapi].

## Command Line Helper Scripts

- [discover_devices.py](https://github.com/TomerFi/aioswitcher/blob/dev/scripts/discover_devices.py) can discover devices and their states (can be run by `poetry run discover_devices`).
- [control_device.py](https://github.com/TomerFi/aioswitcher/blob/dev/scripts/control_device.py) can control a device (can be run by `poetry run control_device`).
- [get_device_login_key.py](https://github.com/TomerFi/aioswitcher/blob/dev/scripts/get_device_login_key) can get a device login key (can be run by `poetry run get_device_login_key`).
- [validate_token.py](https://github.com/TomerFi/aioswitcher/blob/dev/scripts/validate_token.py) can validate a device token which is a must for newer devices, used for communicating with devices (can be run by `poetry run validate_token`).

## Disclaimer

This is **NOT** an official module, and it is **NOT** officially supported by the vendor.</br>
Thanks to all the people at [Switcher][switcher] for their cooperation and general support.

<!-- Real Links -->
[ci-stage]: https://github.com/TomerFi/aioswitcher/actions/workflows/stage.yml
[pages-badge]: https://github.com/TomerFi/aioswitcher/actions/workflows/pages.yml/badge.svg
[codecov-aioswitcher]: https://codecov.io/gh/TomerFi/aioswitcher
[docs-aioswitcher]: https://aioswitcher.tomfi.info/
[pypi-aioswitcher]: https://pypi.org/project/aioswitcher
[repo-aioswitcher]: https://github.com/TomerFi/aioswitcher
[switcher]: https://www.switcher.co.il/
[switcher-webapi]: https://switcher-webapi.tomfi.info
<!-- Badges Links -->
[codecov-badge]: https://codecov.io/gh/TomerFi/aioswitcher/graph/badge.svg
[gh-build-badge]: https://github.com/TomerFi/aioswitcher/actions/workflows/stage.yml/badge.svg
[license-badge]: https://img.shields.io/github/license/tomerfi/aioswitcher
[pypi-down-badge]: https://img.shields.io/pypi/dm/aioswitcher.svg?logo=pypi&color=1082C2
[pypi-ver-badge]: https://img.shields.io/pypi/v/aioswitcher?logo=pypi
