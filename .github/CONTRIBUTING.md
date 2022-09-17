# Contributing to `aioswitcher`</br>[![conventional-commits]][0]

:clap: First off, thank you for taking the time to contribute. :clap:

Contributing is pretty straight-forward:

- Fork the repository
- Create a new branch on your fork
- Commit your changes
- Create a pull request against the `dev` branch

## Install remote development version

Contributions are welcome in all shapes or forms.
If you're a user, you can play around with the current version in development and report back if you bump into anything
suspicious.

Install development version using `pip`:

```shell
pip install git+https://github.com/TomerFi/aioswitcher#dev
```

## Prepare the environment

With [Python >= 3.10](https://www.python.org/) use [pip](https://pypi.org/project/pip/) to install
[poetry](https://poetry.eustace.io/) and the used extensions (mainly [poethepoet](https://github.com/nat-n/poethepoet)):

```shell
  pip install -r requirements.txt
```

## Get started

Install the project in a virtual environment:

```shell
poetry install
```

Start a shell inside the virtual environment:

```shell
poetry shell
```

> Exit the shell using `exit`.

Scroll around [pyproject.toml](../pyproject.toml) and get familiarize with the project,
pay attention to the following section, as most of the developing steps will use these scripts:

```toml
[tool.poe.tasks]
```

To get you going, here are some poe scripts I use constantly while working on *aioswitcher*:

- `poe lint`
- `poe test`
- `poe test_cov --cov-report html`
- `poe lic_check` (requires *deno*)
- `poe black_fix`
- `poe isort_fix`
- `poe docs_build`

> Note, `poethepoet` in installed inside the virtual environment.

## Commit messages

Commit messages must:

- adhere the [Conventional Commits Specification][0]
- be signed-off based on the [Developer Certificate of Origin][1]

## Code of Conduct

Please check the [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).

<!-- Real Links -->
[0]: https://conventionalcommits.org
[1]: https://developercertificate.org
<!-- Badges Links -->
[conventional-commits]: https://img.shields.io/badge/Conventional%20Commits-1.0.0-yellow.svg
