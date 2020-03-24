# Contributing to `aioswitcher`

:clap: First off, thank you for taking the time to contribute. :clap:

Contributing is pretty straight-forward:

- Fork the repository
- Commit your changes
- Create a pull request against the `dev` branch

Please feel free to contribute, even to this contributing guideline file, if you see fit.

- [Source files](#source-files)
- [Package management](#package-management)
- [Documentation](#documentation)
  - [Read the Docs](#read-the-docs)
- [Testing](#testing)
- [Code of Conduct](#code-of-conduct)

## Source files

- `src/aioswitcher` is the *Python* modules making the package.
- `tests` is where *Python* test-cases are stored and executed with [pytest](https://pypi.org/project/pytest/).

## Package management

The [pyproject.toml](pyproject.toml) is the main configuration file for the pypi package based on
[PEP518](https://www.python.org/dev/peps/pep-0518/). Please note, this package is being managed,
build, packaged and deployed with [poetry](https://poetry.eustace.io/).

## Documentation

- `docs/sources` is where the *restructuredText* for creating the [Sphinx Documentation](http://www.sphinx-doc.org/en/master/)
  are stored for build, deployment and hosting by [Read the Docs](https://readthedocs.org/).
- `docs/Makefile` the basic *Makefile* for [Sphinx](http://www.sphinx-doc.org/en/master/)
  documentation generator. From the [docs](docs/) path, type `make html` and
  [sphinx](http://www.sphinx-doc.org/en/master/) will create the documentation site locally in
  `docs/build`.

### Read the Docs

By hook configuration, [Read the Docs](https://readthedocs.org) will build the documentation site
based on [docs/source](docs/source) and host it:

- `stable` tag [here](https://aioswitcher.readthedocs.io/en/stable/) will be built for every
  release snapshot.
- `latest` tag [here](https://aioswitcher.readthedocs.io/en/latest/) will be built for every
  push the dev branch, so it'll reflect unreleased changes.

## Testing

Testing is performed with [Pytest, Full-featured Python testing tool](https://docs.pytest.org/en/latest/).</br>
The various test-cases is in [tests](tests).

For automated local tests, use [Tox](https://tox.readthedocs.io/en/latest/).

## Code of Conduct

The [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) can also be found
[here](https://aioswitcher.readthedocs.io/en/stable/conduct.html).
