.PHONY: all build run deps lint typecheck clean help venvs

help:
	@echo "Available targets:"
	@echo "  make deps       - Install dependencies"
	@echo "  make venvs      - Create virtual environment and install dependencies"
	@echo "  make run        - Start LangGraph Studio"
	@echo "  make lint       - Run ruff linter only"
	@echo "  make typecheck  - Run mypy type checker only"
	@echo "  make build      - Run full validation (lint + typecheck)"
	@echo "  make clean      - Clean up cache files"

deps:
	@echo "Installing dependencies (poetry)"
	poetry install

venvs:
	@echo "Creating Poetry virtual environment"
	poetry install
	@echo "Virtual environment created. Activate with: poetry shell"

run:
	@echo "Starting LangGraph Studio"
	poetry run langgraph dev

lint:
	@echo "Running ruff linter..."
	poetry run ruff check .

typecheck:
	@echo "Running mypy type checker..."
	poetry run mypy --config-file mypy.ini src/

build: lint typecheck
	@echo "✅ All checks passed!"

clean:
	@echo "Cleaning cache files"
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	@echo "Clean complete"

all: deps

