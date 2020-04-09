# Contributing to `aioswitcher`

:clap: First off, thank you for taking the time to contribute. :clap:

Contributing is pretty straight-forward:

- Fork the repository
- Commit your changes
- Create a pull request against the `dev` branch

Please feel free to contribute, even to this contributing guideline file, if you see fit.

- [Package management](#package-management)
- [Documentation](#documentation)
- [Testing](#testing)
- [Code of Conduct](#code-of-conduct)

## Package management

The [pyproject.toml](pyproject.toml) is the main configuration file for the pypi package based on
[PEP518](https://www.python.org/dev/peps/pep-0518/). Please note, this package is being managed,
build, packaged and deployed with [poetry](https://poetry.eustace.io/).

## Documentation

- `docs/sources` is where the *restructuredText* for creating the [Sphinx Documentation](http://www.sphinx-doc.org)
  are stored for build, deployment and hosting by [Read the Docs](https://readthedocs.org/).
- `docs/Makefile` the basic *Makefile* for [Sphinx](http://www.sphinx-doc.org)
  documentation generator. From the [docs](docs/) path, type `make html` and
  [sphinx](http://www.sphinx-doc.org) will create the documentation site locally in
  `docs/build`.

## Testing

Testing is performed with [Pytest, Full-featured Python testing tool](https://docs.pytest.org).</br>
The various test-cases are in [tests](tests).

For automated local tests, use [Tox](https://tox.readthedocs.io).

## Code of Conduct

Please check the [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) markdown file.
