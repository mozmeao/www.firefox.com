DC = $(shell which docker-compose)

all: help

help:
	@echo "Please use \`make <target>' where <target> is one of"
	@echo "  build         - build docker images for dev"
	@echo "  run           - docker-compose up the entire system for dev"
	@echo "  stop          - stop all docker containers"
	@echo "  pull          - pull the latest production images from Docker Hub"
	@echo "  push          - push the latest image built to the Docker Hub"
	@echo "  test          - run the tests against the local container"
	@echo "  test-prod     - run the tests against www.firefox.com"


stop:
	${DC} down

build: stop
	${DC} build --pull

run: build
	${DC} up web

pull: stop
	${DC} pull web test

push:
	${DC} push web test

test: build
	${DC} run test

test-prod: build
	${DC} run test-prod

.PHONY: all help stop build run pull test test-prod
