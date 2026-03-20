.PHONY: build build-cached run stop terminate

IMAGE_NAME := latex-app
CONTAINER_NAME := latex-app

build: # Build the Docker image without using cache
	docker build --no-cache -t $(IMAGE_NAME) .

build-cached: # Build the Docker image using cache (faster if there are no changes)
	docker build -t $(IMAGE_NAME) .

run: # Run the Docker container, removing any existing container with the same name
	@docker rm -f $(CONTAINER_NAME) >/dev/null 2>&1 || true
	docker run --name $(CONTAINER_NAME) -p 8080:8080 $(IMAGE_NAME)

stop: # Stop the running Docker container if it exists
	@id=$$(docker ps -q --filter name=^$(CONTAINER_NAME)$$); \
	if [ -n "$$id" ]; then \
		docker stop $$id; \
	else \
		echo "No running $(CONTAINER_NAME) container to stop."; \
	fi

terminate: # Remove the Docker container if it exists, whether it's running or not
	@id=$$(docker ps -a -q --filter name=^$(CONTAINER_NAME)$$); \
	if [ -n "$$id" ]; then \
		docker rm $$id; \
	else \
		echo "No $(CONTAINER_NAME) container to remove."; \
	fi
