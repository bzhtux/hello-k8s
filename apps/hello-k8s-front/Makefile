.PHONY: help run

flask_env = ${FLASK_ENV}
local_user = $(shell whoami)

run: ## Run Flask app
	@echo "Running in ${flask_env} mode"
	@if [ -z "${flask_env}" ];then echo "FLASK_ENV is missing" ; exit 1;fi
	@python3 app.py

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.DEFAULT_GOAL := help