.PHONY: all build run deps gen-stubs lint clean help venvs

help:
	@echo "Available targets:"
	@echo "  make gen-stubs  - Generate Python stubs from Buf BSR"
	@echo "  make deps       - Install dependencies (generates stubs first)"
	@echo "  make venvs      - Create virtual environment and install dependencies"
	@echo "  make run        - Start LangGraph Studio"
	@echo "  make build      - Run lints and type checks"
	@echo "  make clean      - Clean up cache files"

gen-stubs:
	@echo "Generating Python stubs from Buf BSR"
	buf generate --template buf.gen.planton-cloud.yaml
	buf generate --template buf.gen.project-planton.yaml
	@echo "Stubs generated in apis/stubs/python/"

deps: gen-stubs
	@echo "Installing dependencies (poetry)"
	poetry install

venvs: gen-stubs
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

