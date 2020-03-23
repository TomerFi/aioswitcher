<!--lint disable maximum-heading-length-->
# Switcher Boiler Unofficial Bridge and API Tools</br>[![pypi-version]][11] [![pypi-license]][11] [![pypi-downloads]][11] [![shields-io-maintenance]][0]

| Stage     | Badges                                                                     |
| --------- | -------------------------------------------------------------------------- |
| `Build`   | [![circleci]][7] [![read-the-docs]][8] [![codecov]][3]                     |
| `Etc`     | [![code-style-black]][5] [![checked-with-mypy]][6]                         |

PyPi module named [aioswitcher][11] for integrating with the [Switcher Water Heater](https://www.switcher.co.il/).
Please check out the [documentation](https://aioswitcher.readthedocs.io) hosted with
[readthedocs.io](https://readthedocs.org/).

This module:

- Is packaged with [poetry](https://poetry.eustace.io/).
- Works concurrently using Python's Asynchronous I/O module [asyncio](https://docs.python.org/3/library/asyncio.html#module-asyncio).
- Is static typed and checked with [mypy](https://mypy.readthedocs.io/en/latest/index.html) based
  on [PEP484](https://www.python.org/dev/peps/pep-0484/).
- Follows [black code style](https://black.readthedocs.io/en/stable/) rules and guidelines.
- Package is described using [pyproject.toml](pyproject.toml) based on [PEP517](https://www.python.org/dev/peps/pep-0517/)
  and [PEP518](https://www.python.org/dev/peps/pep-0518/).

Although the [aioswitcher][11] module requires the use of *Python 3.5/3.6/3.7*,
The use of *Python 3.7* is preferable.

<!-- Real Links -->
[0]: https://github.com/TomerFi/aioswitcher
[3]: https://codecov.io/gh/TomerFi/aioswitcher
[5]: https://black.readthedocs.io/en/stable/
[6]: http://mypy-lang.org/
[7]: https://circleci.com/gh/TomerFi/aioswitcher
[8]: https://aioswitcher.readthedocs.io/en/stable
[11]: https://pypi.org/project/aioswitcher/
<!-- Badges Links -->
[checked-with-mypy]: http://www.mypy-lang.org/static/mypy_badge.svg
[circleci]: https://circleci.com/gh/TomerFi/aioswitcher.svg?style=shield
[codecov]: https://codecov.io/gh/TomerFi/aioswitcher/graph/badge.svg
[code-style-black]: https://img.shields.io/badge/code%20style-black-000000.svg
[pypi-downloads]: https://img.shields.io/pypi/dm/aioswitcher.svg
[pypi-license]: https://img.shields.io/pypi/l/aioswitcher.svg
[pypi-version]: https://badge.fury.io/py/aioswitcher.svg
[read-the-docs]: https://readthedocs.org/projects/aioswitcher/badge/?version=stable
[shields-io-maintenance]: https://img.shields.io/badge/Maintained%3F-yes-green.svg
