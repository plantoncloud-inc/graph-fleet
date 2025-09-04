.PHONY: all build run deps lint clean help venvs aws-examples aws-example-1 aws-example-2 aws-example-3 aws-example-4 aws-example-5 aws-example-6 aws-example-all

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

# AWS Agent Examples - delegate to aws_agent Makefile
aws-examples:
	@$(MAKE) -C src/agents/aws_agent examples

aws-example-1:
	@$(MAKE) -C src/agents/aws_agent example-1

aws-example-2:
	@$(MAKE) -C src/agents/aws_agent example-2

aws-example-3:
	@$(MAKE) -C src/agents/aws_agent example-3

aws-example-4:
	@$(MAKE) -C src/agents/aws_agent example-4

aws-example-5:
	@$(MAKE) -C src/agents/aws_agent example-5

aws-example-6:
	@$(MAKE) -C src/agents/aws_agent example-6

aws-example-all:
	@$(MAKE) -C src/agents/aws_agent example-all

help:
	@echo 'build  - run lints/type checks (non-fatal)'
	@echo 'run     - start LangGraph Studio'
	@echo 'deps   - install poetry deps'
	@echo 'venvs  - create Poetry venv'
	@echo 'lint   - strict lints/type checks'
	@echo 'clean  - remove caches and build artifacts'
	@echo ''
	@echo 'Agent Examples:'
	@echo 'aws-examples     - run AWS agent examples (interactive menu)'
	@echo 'aws-example-1    - generic AWS assistant'
	@echo 'aws-example-2    - complex ECS debugging'
	@echo 'aws-example-3    - AWS solutions architect'
	@echo 'aws-example-4    - agent with specific region'
	@echo 'aws-example-5    - custom instructions agent'
	@echo 'aws-example-6    - AWS operations with MCP'
	@echo 'aws-example-all  - run all AWS examples'


