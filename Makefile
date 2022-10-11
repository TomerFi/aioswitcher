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

#######################
#### Build targets ####
#######################
build: clean-dist
	poetry build

clean-dist:
	rm -rf ./dist

install: install-all-deps

install-all-deps:
	poetry install --no-interaction

install-docs-only-deps:
	poetry install --no-interaction --without dev

publish: clean-dist # PYPI_TOKEN is required for this target
	poetry publish --build --no-interaction -u __token__ -p $(PYPI_TOKEN)

.PHONY: build dist publish install install-all-deps install-docs-only-deps

#########################
#### Testing targets ####
#########################
test:
	poetry run pytest -v

test-with-coverage:
	poetry run pytest -v --cov --cov-report=term

test-with-coverage-reports:
	poetry run pytest -v --cov --cov-report=xml:coverage.xml --junit-xml junit.xml

test-pypi-publish: clean-dist # requires testpypi configuration for poetry
	poetry publish --build --repository testpypi

.PHONY: test test-with-coverage test-with-coverage-reports test-pypi-publish

#########################
#### Linting targets ####
#########################
lint: black flake8 isort mypy yamllint

black:
	poetry run black --check src/ docs/ scripts/

black-with-fix:
	poetry run black src/ docs/ scripts/

flake8:
	poetry run flake8 src/ tests/ docs/ scripts/

isort:
	poetry run isort --check-only src/ tests/ docs/ scripts/

isort-with-fix:
	poetry run isort src/ tests/ docs/ scripts/

mypy:
	poetry run mypy src/ scripts/

yamllint:
	poetry run yamllint --format colored --strict .

.PHONY: lint black black-with-fix flake8 isort isort-with-fix mypy yamllint

###############################
#### Documentation targets ####
###############################
docs-clean:
	rm -rf ./site

docs-build:
	poetry run mkdocs build --strict

docs-serve:
	poetry run mkdocs serve

.PHONY: docs-build docs-serve

#########################
#### License targets ####
#########################
verify-license-headers: # requires deno (https://deno.land/#installation)
	deno run --unstable --allow-read https://deno.land/x/license_checker@v3.1.3/main.ts

.PHONY: verify-license-headers
