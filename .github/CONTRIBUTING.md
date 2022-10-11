# Contributing to `aioswitcher`</br>[![conventional-commits-badge]][conventional-commits-site]

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

With [Python >= 3.10][python-site] use [pip][pip-docs] to install [poetry][poetry-site]:

```shell
  pip install -r requirements.txt
```

## Get started

### Get started using make

If you prefer using _GNU_'s [make][make-manual], here are some targets to get you started:

```shell
make install # install all dependencies and the current project
make test # will run all unit-tests
make lint # will lint the project using black, flake8, isort, mypy, and yamllint
make docs-serve # will build and serve a local version of the documentation site
```

### Get started using poethepoet

If you prefer using _Python_'s [poethepoet][poethepoet-site], here are some scripts to get you started:

```shell
poetry run poe install # install all dependencies and the current project
poetry run poe test # will run all unit-tests
poetry run poe lint # will lint the project using black, flake8, isort, mypy, and yamllint
poetry run poe docs_serve # will build and serve a local version of the documentation site
```

## Commit messages

Commit messages must:

- adhere the [Conventional Commits Specifications][conventional-commits-site]
- be signed-off based on the [Developer Certificate of Origin][developer-certificate-origin]

## Code of Conduct

Please check the [CODE_OF_CONDUCT.md][code-of-conduct-github].

<!-- Links -->
[code-of-conduct-github]: https://github.com/TomerFi/.github/blob/main/.github/CODE_OF_CONDUCT.md
[conventional-commits-badge]: https://img.shields.io/badge/Conventional%20Commits-1.0.0-yellow.svg
[conventional-commits-site]: https://conventionalcommits.org
[developer-certificate-origin]: https://developercertificate.org
[make-manual]: https://www.gnu.org/software/make/manual/make.html
[pip-docs]: https://pypi.org/project/pip/
[poethepoet-site]: https://github.com/nat-n/poethepoet
[poetry-site]: https://poetry.eustace.io/
[python-site]: https://www.python.org/
