
.DEFAULT_GOAL := help

.PHONY: help
help:
	@grep '^[a-zA-Z]' $(MAKEFILE_LIST) | \
	sort | \
	awk -F ':.*?## ' 'NF==2 {printf "\033[35m  %-25s\033[0m %s\n", $$1, $$2}'

all: lint-all tests ## Perform all linting checks, security checks and tests
lint-all:	black pylama yamllint bandit ## Perform all linting and security checks (black, pylama, yamllint and bandit).

black: ## Format code using black
	@echo "--- Performing black reformatting ---"
	black . --check

pylama:	## Perform python linting using pylama
	@echo "--- Performing pylama linting ---"
	pylama .

yamllint:	## Perform YAML linting using yamllint
	@echo "--- Performing yamllint linting ---"
	yamllint .

bandit:	## Perform python code security checks using bandit
	@echo "--- Performing bandit code security scanning ---"
	bandit . -v --exclude ./venv --recursive --format json --verbose -s B101



