# ==============================
# Automaton Auditor - Makefile
# ==============================

PYTHON=python
UV=uv
SRC_DIR=src
ENTRY=$(SRC_DIR)/main.py

# Default target
.DEFAULT_GOAL := help

# ------------------------------
# Setup & Installation
# ------------------------------

install:
	@echo "📦 Installing dependencies using uv..."
	$(UV) sync
	@echo "✅ Installation complete."

venv:
	@echo "🔧 Creating virtual environment..."
	$(UV) venv
	@echo "✅ Virtual environment created."

# ------------------------------
# Run Application
# ------------------------------

run:
	@echo "🚀 Running Digital Courtroom..."
	PYTHONPATH=. uv run python -m src.main

debug:
	@echo "🐞 Running in debug mode..."
	PYTHONPATH=.:$(SRC_DIR) $(UV) run python -X dev $(ENTRY)

# ------------------------------
# Testing
# ------------------------------

test:
	@echo "🧪 Running tests..."
	PYTHONPATH=.:$(SRC_DIR) $(UV) run pytest -v

test-fast:
	@echo "⚡ Running fast tests..."
	PYTHONPATH=.:$(SRC_DIR) $(UV) run pytest -q

coverage:
	@echo "📊 Running tests with coverage..."
	PYTHONPATH=.:$(SRC_DIR) $(UV) run pytest --cov=$(SRC_DIR) --cov-report=term-missing

# ------------------------------
# Code Quality
# ------------------------------

lint:
	@echo "🔎 Linting code..."
	$(UV) run ruff check .

format:
	@echo "🎨 Formatting code..."
	$(UV) run ruff format .

typecheck:
	@echo "🧠 Running type checks..."
	$(UV) run mypy $(SRC_DIR)

# ------------------------------
# Cleanup
# ------------------------------

clean:
	@echo "🧹 Cleaning project..."
	rm -rf .pytest_cache
	rm -rf .mypy_cache
	rm -rf __pycache__
	rm -rf .coverage
	rm -rf htmlcov
	find . -type d -name "__pycache__" -exec rm -rf {} +

# ------------------------------
# Dev Combo
# ------------------------------

dev: format lint test
	@echo "🔥 Dev pipeline complete."

# ------------------------------
# Help
# ------------------------------

help:
	@echo ""
	@echo "🏛 Automaton Auditor Make Commands"
	@echo "-------------------------------------"
	@echo "install      Install dependencies"
	@echo "venv         Create virtual environment"
	@echo "run          Run the Digital Courtroom"
	@echo "debug        Run with Python debug flags"
	@echo "test         Run tests (verbose)"
	@echo "test-fast    Run tests (quiet)"
	@echo "coverage     Run tests with coverage"
	@echo "lint         Lint with ruff"
	@echo "format       Auto-format with ruff"
	@echo "typecheck    Run mypy"
	@echo "clean        Remove cache files"
	@echo "dev          Format + Lint + Test"
	@echo ""