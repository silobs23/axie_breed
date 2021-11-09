.ONESHELL:
SHELL := /bin/bash
#######
# Help
#######

.DEFAULT_GOAL := help
.PHONY: help

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

####################
# Build Environment
####################

BUILD_DIR := dist
CONDA_ENV_NAME := axie_exploration
ACTIVATE_CONDA_ENV := source $$(conda info --base)/etc/profile.d/conda.sh ; conda activate ;conda activate
CONDA_ENV_DIR := $$(conda info --base)/envs/$(CONDA_ENV_NAME)
APP_VERSION := $$(python setup.py --version)

.PHONY: clean-deploy-conda-env
clean-deploy-conda-env: ## Rmove conda environment files and development environment. 
	rm -rf $(CONDA_ENV_DIR)
	rm -rf $(BUILD_DIR) 
	rm -rf .eggs

.PHONY: build-dev-conda-env
build-dev-conda-env: ## Build the conda environment
	@echo "Updating artifacts for version $(APP_VERSION)"
	@echo "Create conda environment"
	conda env create -f environment_dev.yml
	@echo "Activate conda env"
	$(ACTIVATE_CONDA_ENV) $(CONDA_ENV_NAME)
	@echo "Build python package environment"
	python -m build
	@echo "Install repo methods into environment"
	pip install $(BUILD_DIR)/Axie_Breed-*-py3-none-any.whl --no-deps
	@echo "Setup envrionment kernel for Jupyter."
	python -s -m ipykernel install --user --name $(CONDA_ENV_NAME)
	conda deactivate

.PHONY: clean-dev-conda-env
clean-dev-conda-env: ## Rmove conda environment files and development environment.
	jupyter kernelspec uninstall $(CONDA_ENV_NAME) 
	rm -rf $(CONDA_ENV_DIR)
	rm -rf $(BUILD_DIR) 
	rm -rf .eggs
	rm -rf .ipynb_checkpoints

.PHONY: lint-dev-conda-env
lint-dev-conda-env: ## Run Black linter in dev environment before pushing commits to github.
	$(ACTIVATE_CONDA_ENV) $(CONDA_ENV_NAME)
	black .
	conda deactivate