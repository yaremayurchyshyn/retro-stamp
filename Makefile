.PHONY: check lint format test build install clean all

# Run all checks (lint + test)
check: lint test

# Lint code
lint:
	python3 -m ruff check src/ tests/
	python3 -m black --check src/ tests/

# Auto-fix lint issues
format:
	python3 -m ruff check src/ tests/ --fix
	python3 -m black src/ tests/

# Run tests
test:
	python3 -m pytest

# Run tests with coverage
test-cov:
	python3 -m pytest --cov=src/retro_stamp --cov-report=term-missing

# Build package
build:
	python3 -m pip install build -q
	python3 -m build

# Install in dev mode
install:
	python3 -m pip install -e ".[dev]"

# Clean build artifacts
clean:
	rm -rf dist/ build/ *.egg-info src/*.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete

# Full check before commit
all: format check
