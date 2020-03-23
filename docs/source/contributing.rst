Contributing
************

First off, thank you for taking the time to contribute.

Contributing is pretty straight-forward:
*   Fork the repository
*   Commit your changes
*   Create a pull request against the **dev** branch

Please feel free to contribute, even to this contributing guideline file, if you see fit.

.. contents:: TOC
   :local:
   :depth: 2

Items description
^^^^^^^^^^^^^^^^^

Configuration files
-------------------

*   ``.circle/config.yml`` is the configuration file for
    `CircleCi Continuous Integration and Deployment Services`_.

*   ``.codecov.yml`` is the configuration file for `CodeCov Code Coverage`_.

*   ``.coveragerc`` is the configuration file for `Coverage.py`_ creating coverage reports with the
    `pytest-cov plugin`_.

*   ``.yamllint`` is the configuration for `yamllint A Linter for YAML Files`_ linting yml files.

*   ``bandit.yml`` is the configuration file for `Bandit common security issues finder`_ checking
    python scripts.

*   ``.spelling`` is the dictionary file used by both `markdown-spellcheck`_ and scspell3k_.
    Case-insensitive words in this file will not raise a spelling mistake error.

Python
------

*   ``src/aioswitcher`` is the *Python* modules making the package.
*   ``tests`` is where *Python* test-cases are stored and executed with pytest_.

Package management
------------------

*   The ``package.json`` file specified by npm_ manages our dependencies, scripts and some metadata.

*   The ``pyproject.toml`` is the main configuration file for the pypi package based on PEP518_.
    Please note, this package is being managed, build, packaged and deployed with poetry_.

Documentation
-------------

*   ``docs/sources`` is where the *restructuredText* files for creating the `Sphinx Documentation`_.
    are stored for build, deployment and hosting by `Read the Docs`_.

*   ``docs/Makefile`` the basic *Makefile* for Sphinx_ documentation generator. From the ``docs``
    path, type ``make html`` and sphinx_ will create the documentation site locally in ``docs/build``.

Continuous Integration
^^^^^^^^^^^^^^^^^^^^^^

CircleCi
--------

By hook configuration, for every pull request, CircleCi_ will execute the workflows described in
``.circleci/config.yml`` and update the PR conversation with the results.

As a final step, CircleCi_ will push the `Coverage.py XML Report`_ CodeCov_ for code
coverage analysis.

Both will of course push their results into the PR conversation.

Some of the steps are considered required and may prevent the PR from being merged.
But no worries, everything is fixable.

CodeCov
-------

CodeCov_ is keeping tabs on our code coverage. When a report is uploaded (by CircleCi_), CodeCov_
will check our code coverage and push its conclusions to PR conversation.

Continuous Deployment
^^^^^^^^^^^^^^^^^^^^^

Read the Docs
-------------

By hook configuration, `Read the Docs`_ will build the documentation site based on ``docs/source``
and host it:

*   ``stable`` tag [here](https://aioswitcher.readthedocs.io/en/stable/) will be built for every
    release snapshot.

*   ``latest`` tag [here](https://aioswitcher.readthedocs.io/en/latest/) will be built for every
    push the dev branch, so it'll reflect unreleased changes.

PyPI
----

As for now, I'm not auto-deploying anything to PyPi_. Packages are being deployed manually.

Environments and Tools
^^^^^^^^^^^^^^^^^^^^^^

.. note::
    Python, poetry and Tox needs to be pre-installed.

*   Python_, CPython interpreter based, although this package supports *Python3.5/3.6/3.7*,
    *Python3.7* is preferred.

*   Poetry_ is being used for packaging and dependency management.
    *   Please install Poetry_ if you plan on developing or testing the package.

*   Tox_ for automating unit testing in your local environment.
    *   Please install Tox_ if you want to perform local testing automation.

    *   Tox utilizes Python's virtualenv_.

    *   Tox is configured with ``pyproject.toml``.

    *   To run tox, simply execute ``tox`` from the ``pyproject.toml``'s path.
        It is recommended that you also run ``tox --help`` to get familiar with the various options
        such as ``-e`` and ``-r`` that will help you perform faster and better tests.

.. note::
    The rest of the steps require no installation on your behalf,
    but knowing them is important seeing they are key elements for testing with ``Tox`` and/or
    ``CircleCi``.

*   yamllint_ for linting the project yml files. yamllint_ is configured with ``.yamllint``.

*   doc8_ for checking restructuredText syntax for files residing in ``docs/source`` used to create
    the documentation site.

*   scspell3k_ for spell checking restructuredText files residing in ``docs/source`` used to create
    the documentation site. scspell3k_ dictionary file is ``.spelling``.

*   sphinx_ for building the documentation site from the *restructuredText* files residing in
    ``docs/source``. It's worth mentioning that `the documentation site`_, hosted with
    `Read the Docs`_ is based upon the theme `sphinx-rtd-theme`_.

*   bandit_ for finding common security issues with against the *Python* files. bandit_ is
    configured with ``bandit.yml``.

*   isort_ for sorting *Python* imports. isort_ is configured with ``pyproject.toml``.

*   flake8_ for linting *Python* files.

*   black_ for formatting *Python* files. black_ is configured with ``pyproject.toml``.

*   mypy_ for checking static typing in *Python* files.

*   pytest_ as testing framework for running test-cases written in ``tests``.

Testing
^^^^^^^

Testing is performed with `Pytest Full-featured Python testing tool`_. The various test-cases is
in ``tests``.

For automated local tests, use Tox_.

Guidelines
^^^^^^^^^^

.. note::

    The project semver_ is handled in both ``pyproject.toml`` and ``package.json``.

Here are some guidelines (recommendations) for contributing to the ``aioswitcher`` project:
*   Code docstrings documentation [here](https://aioswitcher.readthedocs.io/en/stable/codedocs.html)

*   While not all the test steps in ``CircleCi`` and in ``Tox`` are parallel to each other, most
    of them are, so tests failing with ``Tox`` will probably also fail with ``CircleCi``.

*   If writing *Python* code, please remember to [static type](https://www.python.org/dev/peps/pep-0484/).

Code of Conduct
^^^^^^^^^^^^^^^

The code of conduct can be found [here](https://aioswitcher.readthedocs.io/en/stable/conduct.html).

.. _bandit: https://pypi.org/project/bandit/
.. _bandit common security issues finder: https://github.com/PyCQA/bandit
.. _black: https://pypi.org/project/black/
.. _circleci: https://circleci.com/gh/TomerFi/aioswitcher/tree/dev
.. _circleci Continuous Integration and Deployment Services: https://circleci.com/gh/TomerFi/aioswitcher/tree/dev
.. _codecov: https://codecov.io/gh/TomerFi/aioswitcher
.. _codecov code coverage: https://codecov.io/gh/TomerFi/aioswitcher
.. _coverage.py: https://coverage.readthedocs.io/en/v4.5.x/
.. _coverage.py xml report: https://coverage.readthedocs.io/en/v4.5.x/
.. _doc8: https://pypi.org/project/doc8/
.. _flake8: https://pypi.org/project/flake8/
.. _isort: https://pypi.org/project/isort/
.. _markdown-spellcheck: https://www.npmjs.com/package/markdown-spellcheck
.. _mypy: https://pypi.org/project/mypy/
.. _nodeenv: https://pypi.org/project/nodeenv/
.. _npm: https://docs.npmjs.com/files/package.json
.. _package-json-validator: https://www.npmjs.com/package/package-json-validator
.. _pep518: https://www.python.org/dev/peps/pep-0518/
.. _poetry: https://poetry.eustace.io/
.. _pypi: https://pypi.org/
.. _pytest: https://pypi.org/project/pytest/
.. _pytest full-featured python testing tool: https://docs.pytest.org/en/latest/
.. _pytest-cov plugin: https://pytest-cov.readthedocs.io/en/latest/
.. _python: https://www.python.org/
.. _read the docs: https://readthedocs.org/
.. _scspell3k: https://pypi.org/project/scspell3k/
.. _semver: https://semver.org/
.. _sphinx: http://www.sphinx-doc.org/en/master/
.. _sphinx documentation: http://www.sphinx-doc.org/en/master/
.. _sphinx-rtd-theme: https://pypi.org/project/sphinx-rtd-theme/
.. _the documentation site: https://aioswitcher.readthedocs.io/en/stable/
.. _tox: https://tox.readthedocs.io/en/latest/
.. _virtualenv: https://pypi.org/project/virtualenv/
.. _yamllint: https://pypi.org/project/yamllint/
.. _yamllint A Linter for YAML Files: https://yamllint.readthedocs.io/en/stable/index.html
