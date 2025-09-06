.PHONY: all build run deps lint clean help venvs

SHELL := /bin/bash

POETRY ?= poetry
PY ?= $$(poetry env info --path 2>/dev/null)/bin/python
PIP ?= $$(poetry env info --path 2>/dev/null)/bin/pip

all: help

deps:
	@echo "Installing deps (poetry)"
	poetry install

venvs:
	@echo "Creating Poetry virtual environment"
	@poetry --version >/dev/null || { echo "Poetry is required. Install with: brew install poetry"; exit 1; }
	@poetry env use python3.13 || poetry env use python3.12 || poetry env use python3.11 || poetry env use python3
	@echo "Installing dependencies"
	poetry install
	@echo "Venv path: $$(poetry env info --path)"
	@echo "Python: $$(poetry run python -V)"
	@echo "Interpreter: $$(poetry run which python)"

which-python:
	@echo "Poetry venv: $$(poetry env info --path)"
	@echo "Python: $$(poetry run python -V)"
	@echo "Interpreter: $$(poetry run which python)"

python:
	@poetry run python -V

pip-list:
	@poetry run pip list

build:
	@echo "Building (ruff + mypy quick checks)"
	@poetry run ruff --version >/dev/null 2>&1 || poetry install
	@poetry run mypy --version >/dev/null 2>&1 || poetry install
	poetry run ruff check . || true
	poetry run ruff format --check . || true
	poetry run mypy --strict src || true

run:
	@echo "Running LangGraph Studio"
	@poetry run langgraph --version >/dev/null 2>&1 || poetry install
	poetry run langgraph dev

lint:
	poetry run ruff check .
	poetry run ruff format --check .
	poetry run mypy --strict src

clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	rm -rf .mypy_cache .ruff_cache dist build *.egg-info

# No agent-specific commands - use LangGraph Studio via 'make run'



help:
	@echo 'build  - run lints/type checks (non-fatal)'
	@echo 'run     - start LangGraph Studio'
	@echo 'deps   - install poetry deps'
	@echo 'venvs  - create Poetry venv'
	@echo 'lint   - strict lints/type checks'
	@echo 'clean  - remove caches and build artifacts'
	@echo ''
	@echo 'ECS Deep Agent:'
	@echo 'run              - start LangGraph Studio to interact with ecs_deep_agent'


.PHONY: clean-pyc
clean-pyc:
	find . -name '*.pyc' -delete
	find . -type d -name '__pycache__' -exec rm -rf {} +





