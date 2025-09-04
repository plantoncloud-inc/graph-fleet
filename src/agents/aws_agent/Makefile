.PHONY: examples example-1 example-2 example-3 example-4 example-5 example-6 example-all help

SHELL := /bin/bash

# Get the root directory (3 levels up from aws_agent)
ROOT_DIR := $(shell cd ../../../ && pwd)
POETRY := cd $(ROOT_DIR) && poetry
PYTHON := $(POETRY) run python

# Path to the example script relative to root
EXAMPLE_SCRIPT := examples/aws_agent_example.py

examples:
	@echo "AWS Agent Examples"
	@echo "=================="
	@echo ""
	@echo "Available examples:"
	@echo "1. Generic AWS Assistant (MCP)"
	@echo "2. Complex ECS Debugging (Planning + Sub-agents)"
	@echo "3. AWS Solutions Architect"
	@echo "4. Agent with Specific Region"
	@echo "5. Custom Instructions Agent"
	@echo "6. AWS Operations with MCP"
	@echo "7. Run all examples"
	@echo ""
	@echo "Run with: make example-<number> or make example-all"
	@echo "Or use root Makefile: make aws-example-<number>"

example-1:
	@echo "Running Example 1: Generic AWS Assistant (MCP)"
	@echo "=============================================="
	cd $(ROOT_DIR) && echo "1" | $(PYTHON) $(EXAMPLE_SCRIPT)

example-2:
	@echo "Running Example 2: Complex ECS Debugging (Planning + Sub-agents)"
	@echo "=============================================================="
	cd $(ROOT_DIR) && echo "2" | $(PYTHON) $(EXAMPLE_SCRIPT)

example-3:
	@echo "Running Example 3: AWS Solutions Architect"
	@echo "========================================="
	cd $(ROOT_DIR) && echo "3" | $(PYTHON) $(EXAMPLE_SCRIPT)

example-4:
	@echo "Running Example 4: Agent with Specific Region"
	@echo "============================================"
	cd $(ROOT_DIR) && echo "4" | $(PYTHON) $(EXAMPLE_SCRIPT)

example-5:
	@echo "Running Example 5: Custom Instructions Agent"
	@echo "==========================================="
	cd $(ROOT_DIR) && echo "5" | $(PYTHON) $(EXAMPLE_SCRIPT)

example-6:
	@echo "Running Example 6: AWS Operations with MCP"
	@echo "========================================="
	cd $(ROOT_DIR) && echo "6" | $(PYTHON) $(EXAMPLE_SCRIPT)

example-all:
	@echo "Running All AWS Agent Examples"
	@echo "============================="
	cd $(ROOT_DIR) && echo "7" | $(PYTHON) $(EXAMPLE_SCRIPT)

help:
	@echo "AWS Agent Makefile Commands"
	@echo "=========================="
	@echo ""
	@echo "examples     - show available examples menu"
	@echo "example-1    - generic AWS assistant"
	@echo "example-2    - complex ECS debugging"
	@echo "example-3    - AWS solutions architect"
	@echo "example-4    - agent with specific region"
	@echo "example-5    - custom instructions agent"
	@echo "example-6    - AWS operations with MCP"
	@echo "example-all  - run all examples"
	@echo ""
	@echo "Prerequisites:"
	@echo "- Run 'make venvs' from root directory first"
	@echo "- Set OPENAI_API_KEY environment variable"
	@echo "- Optionally set ANTHROPIC_API_KEY for Claude models"
