# Copyright Tomer Figenblat.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Configuration file for Sphinx Documentation Generator."""

from os import path as os_path
from sys import path as sys_path

from toml import load as toml_load

sys_path.insert(0, os_path.abspath("../src"))
sys_path.insert(1, os_path.abspath("../scripts"))

toml_path = "{}/pyproject.toml".format(os_path.abspath(".."))
parsed_toml = toml_load(toml_path)

project = parsed_toml["tool"]["poetry"]["name"]
author = copyright = "Tomer Figenblat"
release = version = parsed_toml["tool"]["poetry"]["version"]

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.githubpages",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinxcontrib.autoprogram",
    "sphinxcontrib.spelling",
]

exclude_patterns = ["docsbuild"]
language = "en"
html_theme = "insegel"

autodoc_default_options = {"members": True}
autodoc_typehints = "description"
