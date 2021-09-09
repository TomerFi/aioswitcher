# Contributing to `aioswitcher`</br>[![conventional-commits]][0]

:clap: First off, thank you for taking the time to contribute. :clap:

Contributing is pretty straight-forward:

- Fork the repository
- Commit your changes
- Create a pull request against the `dev` branch

## Install early-access version

Contributions are welcome in all shapes or forms.
If you're a user, you can play around with the [early-access][1] version and report back if you see anything suspicious.

Install [early-access][1] version using `pip`:

```shell
pip install git+https://github.com/TomerFi/aioswitcher#early-access
```

## Prepare the environment

With [Python >= 3.9](https://www.python.org/) use [pip](https://pypi.org/project/pip/) to install
[poetry](https://poetry.eustace.io/) and the used extensions (mainly [poethepoet](https://github.com/nat-n/poethepoet)):

```shell
  pip install -rrequirements.txt
```

## Get started

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
[1]: https://github.com/TomerFi/aioswitcher/releases/tag/early-access
<!-- Badges Links -->
[conventional-commits]: https://img.shields.io/badge/Conventional%20Commits-1.0.0-yellow.svg
