.PHONY: build help

SHELL:=/bin/bash

build:
	docker build -f Dockerfile -t squizzi/ghcommentor:latest .

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

clean:
	@echo "Cleaning all squizzi/ghcommentor images and cache..."
	@-docker images | grep 'squizzi/ghcommentor' | awk '{print $$3}' | xargs docker rmi -f
