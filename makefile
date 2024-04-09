
# Code Linters #################################################################
check-end-of-file-fixer: ## check consistent end of files
	pre-commit run end-of-file-fixer --all-files

check-gitleaks: ## check for commited secrets with gitleaks
	pre-commit run gitleaks --all-files

check-legal: ## check legal headers for files
	pre-commit run check-legal --all-files

check-nbstripout: ## check output of notebooks (and remove)
	pre-commit run nbstripout --all-files

check-prettier: ## check prettier format of all files
	pre-commit run prettier --all-files

check-ruff: ## check ruff linting
	pre-commit run ruff --all-files
	pre-commit run ruff-format --all-files

check-trailing-whitespace: ## check trailing whitespace
	pre-commit run trailing-whitespace --all-files
