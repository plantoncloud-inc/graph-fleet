.PHONY: all build run deps lint clean help venvs

help:
	@echo "Available targets:"
	@echo "  make deps       - Install dependencies"
	@echo "  make venvs      - Create virtual environment and install dependencies"
	@echo "  make run        - Start LangGraph Studio"
	@echo "  make build      - Run lints and type checks"
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

build:
	@echo "Running lints and type checks"
	poetry run ruff check .
	poetry run mypy src/

clean:
	@echo "Cleaning cache files"
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	@echo "Clean complete"

all: deps

