# Contributing to `aioswitcher` [![conventional-commits]][0]

:clap: First off, thank you for taking the time to contribute. :clap:

Contributing is pretty straight-forward:

- Fork the repository
- Commit your changes
- Create a pull request against the `dev` branch

Please feel free to contribute, even to this contributing guideline file, if you see fit.

- [Package management](#package-management)
- [Code of Conduct](#code-of-conduct)

## Prepare environment

With [Python >= 3.9](https://www.python.org/) use [pip](https://pypi.org/project/pip/) to install
[poetry](https://poetry.eustace.io/) and the used extensions (mainly [poethepoet](https://github.com/nat-n/poethepoet)):

```shell
  pip install -rrequirements.txt
```

Scroll around [pyproject.toml](../pyproject.toml) and get familiarize with the project,
pay attention to the following section, as most of the developing steps will use these scripts:

```toml
[tool.poe.tasks]
```

To get you going, here are some poe scripts I use constantly while working on *aioswitcher*:

- ```poe lint```
- ```poe test```
- ```poe test_cov --cov-report html```
- ```poe install_all```
- ```poe lic_check``` (requires *deno*)
- ```poe black_fix```
- ```poe isort_fix```
- ```poe sphinx_spelling```
- ```poe sphinx_build```

## Code of Conduct

Please check the [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).

<!-- Real Links -->
[0]: https://conventionalcommits.org
<!-- Badges Links -->
[conventional-commits]: https://img.shields.io/badge/Conventional%20Commits-1.0.0-yellow.svg
