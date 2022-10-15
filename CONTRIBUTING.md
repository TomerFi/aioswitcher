# Contributing to *aioswitcher*

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

Note the [code documentation][aioswitcher-code-docs], hosted in this project's [documentation site][aioswitcher-docs-site].<br/>

### Get started using poethepoet

If you prefer using *Python*'s [poethepoet][poethepoet-site], here are some scripts to get you started:

```shell
poetry run poe install # install all dependencies and the current project
poetry run poe test # will run all unit-tests
poetry run poe lint # will lint the project using black, flake8, isort, mypy, and yamllint
poetry run poe docs_serve # will build and serve a local version of the documentation site
```

### Get started using make

If you prefer using *GNU*'s [make][make-manual], here are some targets to get you started:

```shell
make install # install all dependencies and the current project
make test # will run all unit-tests
make lint # will lint the project using black, flake8, isort, mypy, and yamllint
make docs-serve # will build and serve a local version of the documentation site
```

<!-- Links -->
[aioswitcher-code-docs]: https://aioswitcher.tomfi.info/codedocs/
[aioswitcher-docs-site]: https://aioswitcher.tomfi.info/
[make-manual]: https://www.gnu.org/software/make/manual/make.html
[pip-docs]: https://pypi.org/project/pip/
[poethepoet-site]: https://github.com/nat-n/poethepoet
[poetry-site]: https://poetry.eustace.io/
[python-site]: https://www.python.org/
