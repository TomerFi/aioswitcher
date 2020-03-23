# Contributing to `aioswitcher`

:clap: First off, thank you for taking the time to contribute. :clap:

Contributing is pretty straight-forward:

- Fork the repository
- Commit your changes
- Create a pull request against the `dev` branch

Please feel free to contribute, even to this contributing guideline file, if you see fit.

- [Items description](#items-description)
  - [Configuration files](#configuration-files)
  - [Python](#python)
  - [Requirement files](#requirement-files)
  - [Package management](#package-management)
  - [Documentation](#documentation)
- [Continuous Integration](#continuous-integration)
  - [CircleCi](#circleci)
  - [CodeCov](#codecov)
- [Continuous Deployment](#continuous-deployment)
  - [Read the Docs](#read-the-docs)
  - [PyPi](#pypi)
- [Environments and Tools](#environments-and-tools)
- [Testing](#testing)
- [Guidelines](#guidelines)
- [Code of Conduct](#code-of-conduct)

## Items description

### Configuration files

- `.circle/config.yml` is the configuration file for
  [CircleCi Continuous Integration and Deployment Services](https://circleci.com/gh/TomerFi/aioswitcher/tree/dev).
- `.codecov.yml` is the configuration file for [CodeCov Code Coverage](https://codecov.io/gh/TomerFi/aioswitcher).
- `.coveragerc` is the configuration file for [Coverage.py](https://coverage.readthedocs.io/en/v4.5.x/)
    creating coverage reports with the [pytest-cov plugin](https://pytest-cov.readthedocs.io/en/latest/).
- `.yamllint` is the configuration for [yamllint A Linter for YAML Files](https://yamllint.readthedocs.io/en/stable/index.html)
  linting yml files.
- `.remarkrc` is the configuration file for [remark-lint](https://github.com/remarkjs/remark-lint)
  plugin for [Remark](https://remark.js.org/) linting *markdown* files.
- `bandit.yml` is the configuration file for [Bandit common security issues finder](https://github.com/PyCQA/bandit)
  checking python scripts.
- `.spelling` is the dictionary file used by both [markdown-spellcheck](https://www.npmjs.com/package/markdown-spellcheck)
  and [scspell3k](https://pypi.org/project/scspell3k/).
  Case-insensitive words in this file will not raise a spelling mistake error.

### Python

- `src/aioswitcher` is the *Python* modules making the package.
- `tests` is where *Python* test-cases are stored and executed with [pytest](https://pypi.org/project/pytest/).
- `pyscripts` is where *Python* scripts are stored.

### Package management

The [pyproject.toml](pyproject.toml) is the main configuration file for the pypi package based on
[PEP518](https://www.python.org/dev/peps/pep-0518/). Please note, this package is being managed,
build, packaged and deployed with [poetry](https://poetry.eustace.io/).

### Documentation

- `docs/sources` is where the *restructuredText* for creating the [Sphinx Documentation](http://www.sphinx-doc.org/en/master/)
  are stored for build, deployment and hosting by [Read the Docs](https://readthedocs.org/).
- `docs/Makefile` the basic *Makefile* for [Sphinx](http://www.sphinx-doc.org/en/master/)
  documentation generator. From the [docs](docs/) path, type `make html` and
  [sphinx](http://www.sphinx-doc.org/en/master/) will create the documentation site locally in
  `docs/build`.

## Continuous Integration

### CircleCi

By hook configuration, for every pull request, [CircleCi](https://circleci.com/gh/TomerFi/aioswitcher/tree/dev)
will execute the workflows described in [.circleci/config.yml](.circleci/config.yml)
and update the PR conversation with the results.

As a final step, [CircleCi](https://circleci.com/gh/TomerFi/aioswitcher/tree/dev) will push the
[Coverage.py XML Report](https://coverage.readthedocs.io/en/v4.5.x/) to
[CodeCov](https://codecov.io/gh/TomerFi/aioswitcher) for code coverage analysis.</br>

### CodeCov

[CodeCov](https://codecov.io/gh/TomerFi/aioswitcher) is keeping tabs on our code coverage.
When a report is uploaded (by [CircleCi](https://circleci.com/gh/TomerFi/aioswitcher/tree/dev)),
[CodeCov](https://codecov.io/gh/TomerFi/aioswitcher) will check our code coverage and push its
conclusions to the PR conversation.

## Continuous Deployment

### Read the Docs

By hook configuration, [Read the Docs](https://readthedocs.org) will build the documentation site
based on [docs/source](docs/source) and host it:

- `stable` tag [here](https://aioswitcher.readthedocs.io/en/stable/) will be built for every
  release snapshot.
- `latest` tag [here](https://aioswitcher.readthedocs.io/en/latest/) will be built for every
  push the dev branch, so it'll reflect unreleased changes.

### PyPI

As for now, I'm not auto-deploying anything to [PyPi](https://pypi.org/).
Packages are being deployed manually.

## Environments and Tools

> **Please Note**: Python, poetry and Tox needs to be pre-installed.

- [Python](https://www.python.org/), CPython interpreter based, although this package supports
  *Python3.5/3.6/3.7*, *Python3.7* is preferred.
- [Poetry](https://poetry.eustace.io/) is being used for packaging and dependency management.
  - Please install [Poetry](https://poetry.eustace.io/docs/#installation) if you plan on
    developing or testing the package.
- [Tox](https://tox.readthedocs.io/en/latest/) for automating unit testing in your
  local environment.
  - Please install [Tox](https://tox.readthedocs.io/en/latest/) if you want to perform
    local testing automation.
  - Tox utilizes Python's [virtualenv](https://pypi.org/project/virtualenv/).
  - Tox is configured with [pyproject.toml](pyproject.toml).
  - To run tox, simply execute `tox` from the [pyproject.toml](pyproject.toml)'s path.
    It is recommended that you also run `tox --help` to get familiar with the various options
    such as `-e` and `-r` that will help you perform faster and better tests.

> **Please note**: the rest of the steps require no installation on your behalf,
> but knowing them is important seeing they are key elements for testing with `Tox` and/or `CircleCi`.

- [yamllint](https://pypi.org/project/yamllint/) for linting the project yml files.
  [yamllint](https://pypi.org/project/yamllint/) is configured with [.yamllint](.yamllint.yml).

- [doc8](https://pypi.org/project/doc8/) for checking restructuredText syntax for files residing
  in [docs/source](docs/source) used to create the documentation site.

- [scspell3k](https://pypi.org/project/scspell3k/) for spell checking restructuredText files
  residing in [docs/source](docs/source) used to create the documentation site.
  [scspell3k](https://pypi.org/project/scspell3k/) dictionary file is [.spelling](.spelling).

- [sphinx](https://pypi.org/project/Sphinx/) for building the documentation site from the
  restructuredText files residing in [docs/source](docs/source). It's worth mentioning that
  [the documentation site](https://aioswitcher.readthedocs.io/en/stable/), hosted with
  [Read the Docs](https://readthedocs.org) is based upon the theme
  [sphinx-rtd-theme](https://pypi.org/project/sphinx-rtd-theme/).

- [bandit](https://pypi.org/project/bandit/) for finding common security issues with against the
  *Python* files. [bandit](https://pypi.org/project/bandit/) is configured with
  [bandit.yml](bandit.yml).

- [isort](https://pypi.org/project/isort/) for sorting *Python* imports.
  [isort](https://pypi.org/project/isort/) is configured with [pyproject.toml](pyproject.toml).

- [flake8](https://pypi.org/project/flake8/) for linting *Python* files.

- [black](https://pypi.org/project/black/) for formatting *Python* files.
  [black](https://pypi.org/project/black/) is configured with [pyproject.toml](pyproject.toml).

- [mypy](https://pypi.org/project/mypy/) for checking static typing in *Python* files.

- [pytest](https://pypi.org/project/pytest/) as testing framework for running test-cases written in
  [tests](tests).

## Testing

Testing is performed with [Pytest, Full-featured Python testing tool](https://docs.pytest.org/en/latest/).</br>
The various test-cases is in [tests](tests).

For automated local tests, use [Tox](https://tox.readthedocs.io/en/latest/).

## Guidelines

> **Please Note**: the project [semver](https://semver.org/) is handled in both [pyproject.toml](pyproject.toml) and [package.json](package.json).

Here are some guidelines (recommendations) for contributing to the `aioswitcher` project:

- Code docstrings documentation [here](https://aioswitcher.readthedocs.io/en/stable/codedocs.html)
- For any change in dependencies, please use [pyscripts/poetry-to-requirements.py](pyscripts/poetry-to-requirements.py)
  for creating a valid [requirements.txt](requirements.txt) file and add it to your PR.
  This is also done automatically with the `py37` testenv in `tox`.
- While not all the test steps in [CircleCi](.circleci/config.yml) and in
  [Tox](pyproject.toml) are parallel to each other, most of them are, so tests
  failing with `Tox` will probably also fail with `CircleCi`.
- If writing *Python* code, please remember to [static type](https://www.python.org/dev/peps/pep-0484/).

## Code of Conduct

The [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) can also be found
[here](https://aioswitcher.readthedocs.io/en/stable/conduct.html).
