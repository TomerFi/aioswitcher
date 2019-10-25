<!--lint disable maximum-heading-length list-item-indent-->
# Switcher Boiler Unofficial Bridge and API Tools</br>[![shields-io-maintenance]][0] [![pypi-version]][11] [![pypi-license]][11] [![pypi-downloads]][11] [![self-hosted-slack-channel]][1] [![shields-io-cii-best-practices-summary]][2]

| Stage     | Badges                                                                                              |
| --------- | --------------------------------------------------------------------------------------------------- |
| `Code`    | [![codecov]][3] [![codacy]][4] [![code-style-black]][5] [![checked-with-mypy]][6]                   |
| `Builds`  | [![circleci]][7] [![read-the-docs]][8] [![license-scan]][15]                                        |
| `Pypi`    | [![requires-io]][9] [![snyk-pypi]][13]                                                              |
| `Npm`     | [![david-dm-dev-package-json-dependencies-status]][10] [![snyk-npm]][12] [![greenkeeper-badge]][14] |

[![Python Versions](https://img.shields.io/pypi/pyversions/django.svg)]((https://pypi.org/project/aioswitcher/))

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
[1]: https://tomfi.slack.com/messages/CK3KRBYDP
[2]: https://bestpractices.coreinfrastructure.org/projects/2889
[3]: https://codecov.io/gh/TomerFi/aioswitcher
[4]: https://www.codacy.com/app/TomerFi/aioswitcher?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=TomerFi/aioswitcher&amp;utm_campaign=Badge_Grade
[5]: https://black.readthedocs.io/en/stable/
[6]: http://mypy-lang.org/
[7]: https://circleci.com/gh/TomerFi/aioswitcher
[8]: https://aioswitcher.readthedocs.io/en/stable
[9]: https://requires.io/github/TomerFi/aioswitcher/requirements
[10]: https://david-dm.org/TomerFi/aioswitcher
[11]: https://pypi.org/project/aioswitcher/
[12]: https://snyk.io//test/github/TomerFi/aioswitcher?targetFile=package.json
[13]: https://snyk.io//test/github/TomerFi/aioswitcher?targetFile=requirements.txt
[14]: https://greenkeeper.io/
[15]: https://app.fossa.io/projects/git%2Bgithub.com%2FTomerFi%2Faioswitcher
<!-- Badges Links -->
[checked-with-mypy]: http://www.mypy-lang.org/static/mypy_badge.svg
[circleci]: https://circleci.com/gh/TomerFi/aioswitcher.svg?style=shield
[codacy]: https://api.codacy.com/project/badge/Grade/49a3c3b0987e4d9a8f400eb49db423d8
[codecov]: https://codecov.io/gh/TomerFi/aioswitcher/graph/badge.svg
[code-style-black]: https://img.shields.io/badge/code%20style-black-000000.svg
[david-dm-dev-package-json-dependencies-status]: https://david-dm.org/TomerFi/aioswitcher/status.svg
[greenkeeper-badge]: https://badges.greenkeeper.io/TomerFi/aioswitcher.svg
[license-scan]: https://app.fossa.io/api/projects/git%2Bgithub.com%2FTomerFi%2Faioswitcher.svg?type=shield
[pypi-downloads]: https://img.shields.io/pypi/dm/aioswitcher.svg
[pypi-license]: https://img.shields.io/pypi/l/aioswitcher.svg
[pypi-version]: https://badge.fury.io/py/aioswitcher.svg
[read-the-docs]: https://readthedocs.org/projects/aioswitcher/badge/?version=stable
[requires-io]: https://requires.io/github/TomerFi/aioswitcher/requirements.svg
[self-hosted-slack-channel]: https://slack.tomfi.info:8443/aioswitcher.svg
[shields-io-cii-best-practices-summary]: https://img.shields.io/cii/summary/2889.svg
[shields-io-maintenance]: https://img.shields.io/badge/Maintained%3F-yes-green.svg
[snyk-npm]: https://snyk.io//test/github/TomerFi/aioswitcher/badge.svg?targetFile=package.json
[snyk-pypi]: https://snyk.io//test/github/TomerFi/aioswitcher/badge.svg?targetFile=requirements.txt
