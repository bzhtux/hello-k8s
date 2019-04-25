FLASK_ENV ?= dev
local_user = $(shell whoami)
DOCKER_VERSION = $(shell grep DOCKER_VERSION instance/dev.py| awk -F '=' '{gsub(" ",""); print $$2;}' | sed 's/"//g')

.PHONY: run
run: ## Run Flask app
	@echo "Running in ${FLASK_ENV} mode"
	@if [ -z "${FLASK_ENV}" ];then echo "FLASK_ENV is missing" ; exit 1;fi
	@FLASK_ENV=${FLASK_ENV} python3 app.py

.PHONY: docker-build
docker-build: ## B uild docker image for hello-k8s-api
	@docker build -t bzhtux/hello-k8s-api:${DOCKER_VERSION} .

.PHONY: docker-push
docker-push: ## Push docker image to docker hub
	@docker push bzhtux/hello-k8s-api:${DOCKER_VERSION}

.PHONY: help
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.DEFAULT_GOAL := help