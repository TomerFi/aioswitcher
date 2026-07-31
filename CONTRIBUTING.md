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

With [Python >= 3.14][python-site] use [uv][uv-docs] to install all dependencies:

```shell
  uv sync --all-groups
```

### Get started

After installing, run the testing or linting tools directly:

```shell
uv run pytest --help # display test options
```

Common tasks:

```shell
uv run pytest # will run all unit-tests

# Lint the project
uv run black --check src/ docs/ scripts/
uv run flake8 src/ tests/ docs/ scripts/
uv run isort --check-only src/ tests/ docs/ scripts/
uv run mypy src/ scripts/
uv run yamllint --format colored --strict .

uv run mkdocs serve # will build and serve a local version of the documentation site
```

## Prek Hooks

Install hooks after cloning:

```shell
uv run prek install
```

Hooks match CI commands. See `.pre-commit-config.yaml` for the full list. Test against all files with:

```shell
uv run prek run --all-files
```

Update hook dependencies occasionally:

```shell
uv run prek update --freeze
```

`additional_dependencies` in the config are pinned with exact versions — update them manually when needed.

## AI Policy

This project encourages and assumes the use of AI tools. See [AI_POLICY.md](AI_POLICY.md) for the full policy — the short version: use AI however you want, but verify everything before submitting and own what you contribute.

## Documentation

We use [MkDocs][mkdocs-site] and [Material][material-site] for building our documentation site,
https://aioswitcher.figenblat.com/. See [docs](docs) and [mkdocs.yml](mkdocs.yml).

> [!NOTE]
> We're generating [code documentation][aioswitcher-code-docs] from _docstrings_.

<!-- Links -->
[aioswitcher-code-docs]: https://aioswitcher.figenblat.com/codedocs/
[material-site]: https://squidfunk.github.io/mkdocs-material/
[mkdocs-site]: https://www.mkdocs.org/
[python-site]: https://www.python.org/
[uv-docs]: https://docs.astral.sh/uv/
