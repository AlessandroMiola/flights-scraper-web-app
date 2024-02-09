# Use PowerShell instead of sh
# set shell := ["powershell.exe", "-c"]

help:
  @just --list

install:
  @echo "🚀 Installing dependencies"
  @poetry install --with dev

install-pre-commit:
  @echo "🚀 Setting up the hooks"
  @poetry run pre-commit install

check-project:
  @echo "🚀 Checking consistency between poetry.lock and pyproject.toml"
  @poetry check --lock
  @echo "🚀 Running the hooks against all files"
  @poetry run pre-commit run --all-files

ruff:
  @echo "🚀 Linting the project with Ruff"
  @poetry run ruff check .

ruff-show-violations:
  @echo "🚀 Linting the project with Ruff and show violations"
  @poetry run ruff check --output-format="grouped" .

ruff-fix:
  @echo "🚀 Linting the project with Ruff and autofix violations (where possible)"
  @poetry run ruff check --fix .

black:
  @echo "🚀 Formatting the code with Black"
  @poetry run black .

black-check:
  @echo "🚀 Listing files Black would reformat"
  @poetry run black --check .

black-diff:
  @echo "🚀 Checking formatting advices from Black"
  @poetry run black --diff .

lint-and-format: ruff-fix black
