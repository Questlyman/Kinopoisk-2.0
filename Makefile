FORMAT_DIRS=server main.py migrations tests
LINTER_DIRS=server main.py migrations tests
TOML_FILES=poetry.lock pyproject.toml
POETRY_EXEC=poetry
PYTHON_EXEC=$(POETRY_EXEC) run python


.PHONY: help
help:  ## Print this message
	@grep -E -h '\s##\s' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'



.PHONY: install
install:  ## Install dependencies
	python -m poetry install

.PHONY: pretty
pretty: isort autoflake black toml-sort  ## Make formatting of code

.PHONY: lint
lint: isort-check autoflake-check black-check pylint mypy  ## Check code by linters

.PHONY: black
black:
	$(PYTHON_EXEC) -m black -t py310 $(FORMAT_DIRS)

.PHONY: black-check
black-check:
	$(PYTHON_EXEC) -m black -t py310 $(FORMAT_DIRS) --check

.PHONY: isort
isort:
	$(PYTHON_EXEC) -m isort $(FORMAT_DIRS)

.PHONY: isort-check
isort-check:
	$(PYTHON_EXEC) -m isort $(FORMAT_DIRS) --check

.PHONY: autoflake
autoflake:
	$(PYTHON_EXEC) -m autoflake -i -r --verbose --ignore-init-module-imports --remove-all-unused-imports --expand-star-imports $(FORMAT_DIRS)

.PHONY: autoflake-check
autoflake-check:
	$(PYTHON_EXEC) -m autoflake -i -r --verbose --ignore-init-module-imports --remove-all-unused-imports --expand-star-imports $(FORMAT_DIRS) --check


.PHONY: toml-sort
toml-sort:
	$(POETRY_EXEC) run toml-sort $(TOML_FILES) -i -a

.PHONY: mypy
mypy:
	$(POETRY_EXEC) run mypy --show-error-codes $(LINTER_DIRS)

.PHONY: flake8
flake8:
	$(POETRY_EXEC) run flake8 --jobs 4 --statistics --show-source $(LINTER_DIRS)

.PHONY: pylint
pylint:
	$(POETRY_EXEC) run pylint --jobs 4 --rcfile=setup.cfg --extension-pkg-whitelist='pydantic' $(LINTER_DIRS)


.PHONY: test
test:  ## Run unit-tests
	$(POETRY_EXEC) run pytest -n auto $(args)

