# AnyModel Makefile

.DEFAULT_GOAL := help
CLAUDE ?= $(shell which ~/.claude/local/claude || which claude || echo claude)

.PHONY: help
help: ## Show this help message
	@echo "Usage: make [target]"
	@echo ""
	@echo "Available targets:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-20s %s\n", $$1, $$2}'

.PHONY: install
install: ## Install package and dependencies
	uv sync

.PHONY: install-dev
install-dev: ## Install package with development dependencies
	uv sync --all-extras

.PHONY: test
test: ## Run tests
	uv run pytest

.PHONY: test-verbose
test-verbose: ## Run tests with verbose output
	uv run pytest -v

.PHONY: test-coverage
test-coverage: ## Run tests with coverage report
	uv run pytest --cov=anymodel --cov-report=term-missing

.PHONY: check
check: ## Run code quality checks (linting and formatting)
	uv run ruff check .
	uv run ruff format --check .

.PHONY: fix
fix: ## Fix auto-fixable issues and format code
	uv run ruff check --fix .
	uv run ruff format .

.PHONY: docs
docs: docs-generate ## Build documentation
	cd docs && uv run make clean html

.PHONY: docs-serve
docs-serve: docs ## Build and serve documentation locally
	@echo "Serving documentation at http://localhost:8888"
	cd docs/_build/html && uv run python -m http.server 8888

.PHONY: docs-serve-dev
docs-serve-dev: docs-generate ## Serve documentation with auto-reload for development
	@echo "Starting auto-reloading documentation server at http://localhost:8888"
	cd docs && uv run sphinx-autobuild . _build/html --port 8888 --watch ../anymodel

.PHONY: docs-generate
docs-generate: ## Generate API reference documentation
	uv run python bin/generate_reference.py

.PHONY: clean
clean: ## Clean build artifacts
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf .pytest_cache/
	rm -rf .ruff_cache/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	cd docs && make clean

.PHONY: build
build: ## Build package
	uv build
