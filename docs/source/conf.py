"""Configuration file for Sphinx Documentation Generator."""

from os import path as os_path

from toml import load as toml_load

# Considering we're in aioswitcher/docs/source
# We need to go back twice to reach aioswitcher/pyproject.toml
toml_path = "{}/pyproject.toml".format(os_path.abspath("../.."))
parsed_toml = toml_load(toml_path)

project = parsed_toml["tool"]["poetry"]["name"]
copyright = "2019, Tomer Figenblat"
author = "Tomer Figenblat"
version = parsed_toml["tool"]["poetry"]["version"]
release = version
extensions = ["sphinx.ext.autodoc", "sphinx.ext.todo", "sphinx.ext.viewcode"]
templates_path = ["_templates"]
source_suffix = ".rst"
master_doc = "index"
language = None
exclude_patterns = ["_build"]
pygments_style = "sphinx"
# html_static_path = ["_static"]
html_theme = "sphinx_rtd_theme"
language = "en"

show_authors = True
linkcheck_anchors = True

# autodoc configuration
# autodoc_mock_imports = []
