.PHONY: build build-cached run stop terminate

IMAGE_NAME := latex-app
CONTAINER_NAME := latex-app

build: # Build the Docker image without using cache
	docker build --no-cache -t $(IMAGE_NAME) .

build-cached: # Build the Docker image using cache (faster if there are no changes)
	docker build -t $(IMAGE_NAME) .

run: build-cached # Build image (cached) then run container, removing any existing container with the same name
	-@docker rm -f $(CONTAINER_NAME)
	docker run --name $(CONTAINER_NAME) -p 8080:8080 $(IMAGE_NAME)

stop: # Stop the running Docker container if it exists
	-@docker stop $(CONTAINER_NAME)

terminate: # Remove the Docker container if it exists, whether it's running or not
	-@docker rm -f $(CONTAINER_NAME)
