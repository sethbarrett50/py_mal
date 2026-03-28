SHELL := /usr/bin/env bash
.DEFAULT_GOAL := help

UV    ?= uv
RUFF  ?= ruff
PY    ?= python

REV_SHELL_HOST ?= 127.0.0.1
REV_SHELL_PORT ?= 6767

.PHONY: help sync lint format check test run sample build clean

help: ## Show targets
	@grep -E '^[a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-12s\033[0m %s\n", $$1, $$2}'

sync: ## Install/sync deps (including dev group)
	$(UV) sync --dev

format: ## Format code
	$(UV) run $(RUFF) format .

check: ## Lint (no fixes)
	$(UV) run $(RUFF) check .

lint: ## Format + lint with fixes
	$(UV) run $(RUFF) format .
	$(UV) run $(RUFF) check . --fix

test: ## Run tests
	$(UV) run pytest -q

build: ## Build sdist/wheel
	$(UV) build

clean: ## Remove build & test artifacts
	rm -rf dist build *.egg-info
	find . -type d -name "__pycache__" -exec rm -rf {} + && rm -rf .pytest_cache
	
preflight: ## Build + run twine metadata checks
	$(UV) build
	uvx twine check dist/*

r.rev_shell: ## Runs remote shell with given args
	$(UV) run rev_shell --host $(REV_SHELL_HOST) --port $(REV_SHELL_PORT)
