.PHONY: help

.DEFAULT_GOAL := help

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'
clean: ## Remove files and directories created during installation, and uninstall the service and all it's dependencies
	rm -rf build dist **/__pycache__
	python setup.py develop --uninstall
	pip uninstall -y $(SERVICE) || true
	pip uninstall -y `pip freeze` || true

migrate: # Run migrations
	python manage.py migrate
