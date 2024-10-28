# Contributing to *aioswitcher*

:clap: First off, thank you for taking the time to contribute. :clap:

Contributing is pretty straight-forward:

- Fork the repository
- Create a new branch on your fork
- Commit your changes
- Create a pull request against the `dev` branch

## Installing

### Install remote development version

Contributions are welcome in all shapes or forms. If you're a user, you can play around with the current development
version and report back any findings.

Install the remote development version using `pip`:

```shell
pip install git+https://github.com/TomerFi/aioswitcher#dev
```

### Install local development version

If you need to test your changes locally, you can install your work-in-progress from your active working branch.

Install the local development version using `pip`:

```shell
pip install --upgrade .
```

## Developing

### Prepare the development environment

With [Python >= 3.10][python-site] use [pip][pip-docs] to install [poetry][poetry-site]:

```shell
  pip install -r requirements.txt
```

### Get started with poetry

```shell
poetry run poe install # install all dependencies and the current project
poetry run poe test # will run all unit-tests
poetry run poe lint # will lint the project using black, flake8, isort, mypy, and yamllint
poetry run poe docs_serve # will build and serve a local version of the documentation site
```

## Documentation

We use [MkDocs][mkdocs-site] and [Material][material-site] for building our documentation site,
https://aioswitcher.tomfi.info/. See [docs](docs) and [mkdocs.yml](mkdocs.yml). 

> [!NOTE]   
> We're generating [code documentation][aioswitcher-code-docs] from _docstrings_.

<!-- Links -->
[aioswitcher-code-docs]: https://aioswitcher.tomfi.info/codedocs/
[material-site]: https://squidfunk.github.io/mkdocs-material/
[mkdocs-site]: https://www.mkdocs.org/
[pip-docs]: https://pypi.org/project/pip/
[poethepoet-site]: https://github.com/nat-n/poethepoet
[poetry-site]: https://poetry.eustace.io/
[python-site]: https://www.python.org/
