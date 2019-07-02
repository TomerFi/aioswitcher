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

*   ``.remarkrc`` is the configuration file for `remark-lint`_ plugin for Remark_ linting
    *markdown* files.

*   ``bandit.yml`` is the configuration file for `Bandit common security issues finder`_ checking
    python scripts.

*   ``.spelling`` is the dictionary file used by both `markdown-spellcheck`_ and scspell3k_.
    Case-insensitive words in this file will not raise a spelling mistake error.

Python
------

*   ``src/aioswitcher`` is the *Python* modules making the package.
*   ``tests`` is where *Python* test-cases are stored and executed with pytest_.
*   ``pyscripts``` is where *Python* scripts are stored.

Requirement files
-----------------

*   ``poetry.lock`` is the lock file describing the module version tree of the pypi modules. This
    helps locking down working versions of modules, it is part of the poetry_ dependency
    management.

*   ``package-lock.json`` is the lock file describing the module version tree of the npm modules.
    This helps locking down working versions of modules, it is part of the npm_ dependency
    management.

*   ``requirements.txt`` has noting to do directly with the package structure. We use poetry_ for
    packaging and building. This file is actually being manually build with
    ``pyscripts/poetry-to-requirements.py`` from the content of ``poetry.lock`` file for legacy
    support (e.g. `Requires-io`_ and Snyk_).

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

As a final step, CircleCi_ will push the `Coverage.py XML Report`_ to both CodeCov_ for code
coverage analysis and Codacy_ for code quality analysis.

Both will of course push their results into the PR conversation.

Please note, Codacy_ is actually getting notified for the PR by a *GitHub* hook. The report being
uploaded is for the dashboard presentation and does not trigger further action.

Some of the steps are considered required and may prevent the PR from being merged.
But no worries, everything is fixable.

CodeCov
-------

CodeCov_ is keeping tabs on our code coverage. When a report is uploaded (by CircleCi_), CodeCov_
will check our code coverage and push its conclusions to PR conversation.

Codacy
------

Codacy_ is here to check the quality of our code. When a PR is created or updated, *GitHub* is
hooked to notify Codacy_ that starts checking the quality of our code and push its conclusions to
the PR conversation.

Requires-io
-----------

`Requires.io`_ is keeping an eye for versions updates upon the *Python* requirements listed in our
legacy ``requirements.txt`` file.

David-DM
--------

`David-DM`_ is keeping an eye for versions updates upon the *Npm* requirements listed in the
``package.json`` file.

Snyk
----

Snyk_ is keeping an eye out for vulnerabilities and in our `npm dependencies`_, our
`pypi requirements`_.

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

*   *Python Module*: nodeenv_, a tool that enables us to create a Node.js virtual environment in
    resemblance to virtualenv_, this tool also allows combining nodeenv_ within virtualenv_, which
    is exactly what we're doing with ``tox``.

*   *NPM Package*: `package-json-validator`_ for validating the ``package.json`` file.

*   *Python Package*: yamllint_ for linting the project yml files.
    *   yamllint_ is configured with ``.yamllint``.

*   *NPM Package*: `markdown-spellcheck`_ for checking the project *markdown* files for spelling
    errors.

    *   `markdown-spellcheck`_ dictionary file is ``.spelling``.

*   *NPM Package*: remark-lint_ which is a plugin for remark_ and the `remark-cli`_ command line
    tool for linting markdown files residing at the ``base path`` and in ``.github``.

    *   `remark-lint`_ uses a couple of presets and tools, all can be found under the dependencies
        key in ``package.json``.

    *   `remark-lint`_ is configured with ``.remarkrc``.

*   *Python Module*: doc8_ for checking restructuredText syntax for files residing in
    ``docs/source`` used to create the documentation site.

*   *Python Module*: scspell3k_ for spell checking restructuredText files residing in
    ``docs/source`` used to create the documentation site.
    *   scspell3k_ dictionary file is ``.spelling``.

*   *Python Module*: sphinx_ for building the documentation site from the *restructuredText* files
    residing in ``docs/source``.

    *   It's worth mentioning that `the documentation site`_, hosted with `Read the Docs`_ is based
        upon the theme `sphinx-rtd-theme`_.

*   *Python Package*: bandit_ for finding common security issues with against the *Python* files.
    *   bandit_ is configured with ``bandit.yml``.

*   *Python Package*: isort_ for sorting *Python* imports.
    -   isort_ is configured with ``pyproject.toml``.

*   *Python Package*: flake8_ for linting *Python* files.

*   *Python Package*: black_ for formatting *Python* files.
    *   black_ is configured with ``pyproject.toml``.

*   *Python Package*: mypy_ for checking static typing in *Python* files.

*   *Python Package*: pytest_ as testing framework for running test-cases written in ``tests``.

Testing
^^^^^^^

Testing is performed with `Pytest, Full-featured Python testing tool`_. The various test-cases is
in ``tests``.

For automated local tests, use Tox_.

Guidelines
^^^^^^^^^^

.. note::

    The project semver_ is handled in both ``pyproject.toml`` and ``package.json``.

Here are some guidelines (recommendations) for contributing to the ``aioswitcher`` project:
*   Code docstrings documentation [here](https://aioswitcher.readthedocs.io/en/stable/codedocs.html)

*   For any change in dependencies, please use ``pyscripts/poetry-to-requirements.py`` for
    creating a valid ``requirements.txt`` file and add it to your PR. This is also done
    automatically with the ``py37`` testenv in ``tox``.

*   While not all the test steps in ``CircleCi`` and in ``Tox`` are parallel to each other, most
    of them are, so tests failing with ``Tox`` will probably also fail with ``CircleCi``.

*   If writing *Python* code, please remember to [static type](https://www.python.org/dev/peps/pep-0484/).

*   You can run npm's script ``spell-md-interactive`` for handling all spelling mistakes before
    testing.
    You can also choose to run ``spell-md-report`` to print a full report instead of handling the
    spelling mistakes one-by-one.
    *   `markdown-spellcheck`_ dictionary is the file ``.spelling``.

NPM Scripts
-----------

Before using the scrips, you need to install the dependencies.
From the ``package.json`` file path, run ``npm install``,
Then you can execute the scripts from the same path.
*   ``npm run lint-md`` will run remark_ against *markdown* files.

*   ``npm run validate-pkg`` will run `package-json-validator`_ against the ``package.json`` file.

*   ``npm run spell-md-interactive`` will run `markdown-spellcheck`_ against *markdown* files in
    an interactive manner allowing us to select the appropriate action.

*   ``npm run spell-md-report`` will run `markdown-spellcheck`_ against *markdown* files and print
    the report to stdout.

Chat
^^^^

Feel free to join the project's public `Slack Channel`_.
GitHub is integrated with the channel and keep its members updated.

Best Practices
^^^^^^^^^^^^^^

This project tries to follow the `CII Best Practices`_ guidelines.

That's not an easy task and I'm not sure achieving 100% is even possible for this specific
project.

At the time writing this, the project has achieved 14% (The writing of this file was actually
according one to those guidelines).

Any contribution bumping up this percentage will be gladly embraced.

Code of Conduct
^^^^^^^^^^^^^^^

The code of conduct can be found [here](https://aioswitcher.readthedocs.io/en/stable/conduct.html).

.. _bandit: https://pypi.org/project/bandit/
.. _bandit common security issues finder: https://github.com/PyCQA/bandit
.. _black: https://pypi.org/project/black/
.. _cii best practices: https://bestpractices.coreinfrastructure.org/en/projects/2889
.. _circleci: https://circleci.com/gh/TomerFi/aioswitcher/tree/dev
.. _circleci Continuous Integration and Deployment Services: https://circleci.com/gh/TomerFi/aioswitcher/tree/dev
.. _codacy: https://app.codacy.com/project/TomerFi/aioswitcher/dashboard
.. _codecov: https://codecov.io/gh/TomerFi/aioswitcher
.. _codecov code coverage: https://codecov.io/gh/TomerFi/aioswitcher
.. _coverage.py: https://coverage.readthedocs.io/en/v4.5.x/
.. _coverage.py xml report: https://coverage.readthedocs.io/en/v4.5.x/
.. _david-dm: https://david-dm.org/TomerFi/aioswitcher
.. _doc8: https://pypi.org/project/doc8/
.. _flake8: https://pypi.org/project/flake8/
.. _isort: https://pypi.org/project/isort/
.. _markdown-spellcheck: https://www.npmjs.com/package/markdown-spellcheck
.. _mypy: https://pypi.org/project/mypy/
.. _nodeenv: https://pypi.org/project/nodeenv/
.. _npm: https://docs.npmjs.com/files/package.json
.. _npm dependencies: https://snyk.io/test/github/TomerFi/aioswitcher?targetFile=package.json
.. _package-json-validator: https://www.npmjs.com/package/package-json-validator
.. _pep518: https://www.python.org/dev/peps/pep-0518/
.. _poetry: https://poetry.eustace.io/
.. _pypi: https://pypi.org/
.. _pypi requirements: https://snyk.io/test/github/TomerFi/aioswitcher?targetFile=requirements.txt
.. _pytest: https://pypi.org/project/pytest/
.. _pytest, full-featured python testing tool: https://docs.pytest.org/en/latest/
.. _pytest-cov plugin: https://pytest-cov.readthedocs.io/en/latest/
.. _python: https://www.python.org/
.. _read the docs: https://readthedocs.org/
.. _remark: https://remark.js.org/
.. _remark-cli: https://www.npmjs.com/package/remark-cli
.. _remark-lint: https://github.com/remarkjs/remark-lint
.. _requires.io: https://requires.io/github/TomerFi/aioswitcher/requirements/?branch=dev
.. _scspell3k: https://pypi.org/project/scspell3k/
.. _semver: https://semver.org/
.. _slack channel: https://tomfi.slack.com/messages/CK3KRBYDP
.. _snyk: https://snyk.io
.. _sphinx: http://www.sphinx-doc.org/en/master/
.. _sphinx documentation: http://www.sphinx-doc.org/en/master/
.. _sphinx-rtd-theme: https://pypi.org/project/sphinx-rtd-theme/
.. _the documentation site: https://aioswitcher.readthedocs.io/en/stable/
.. _tox: https://tox.readthedocs.io/en/latest/
.. _virtualenv: https://pypi.org/project/virtualenv/
.. _yamllint: https://pypi.org/project/yamllint/
.. _yamllint A Linter for YAML Files: https://yamllint.readthedocs.io/en/stable/index.html
