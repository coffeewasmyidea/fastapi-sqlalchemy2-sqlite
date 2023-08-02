.PHONY: all

SHELL := /bin/bash

.DEFAULT_GOAL := start

.CURRENT_ENV := ${CURRENT_ENV}

GIT_HASH ?= $(shell git log --format="%h" -n 1)


# Building an image
build:
	docker build -t ${DOCKER_USERNAME}/${APP_NAME}:${GIT_HASH} \
		--no-cache --rm --build-arg CURRENT_ENV=${CURRENT_ENV} .

# Start application
start: 
	scripts/start

# Run in the docker container 
run:
	scripts/run ${APP_NAME} ${DOCKER_USERNAME}/${APP_NAME}:${GIT_HASH}

# Poetry shell
env:
	scripts/env

lint:
	scripts/lint ${APP_FOLDER}

format:
	scripts/format ${APP_FOLDER}

# Remove __pycache__/.pyc/.pyo if needed
clean:
	scripts/clean

push:
	docker push ${DOCKER_USERNAME}/${APP_NAME}:${GIT_HASH} 

release:
	docker pull ${DOCKER_USERNAME}/${APP_NAME}:${GIT_HASH}
	docker tag ${DOCKER_USERNAME}/${APP_NAME}:${GIT_HASH} ${DOCKER_USERNAME}/${APP_NAME}:latest
	docker push ${DOCKER_USERNAME}/${APP_NAME}:latest

alembic_upgrade:
	alembic upgrade head

test:
	pytest -sv app/tests
