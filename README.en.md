# Latex API

## Description

This is an api running with a static frontend with a docker sandbox. The purpose of this project is to give an alternative to websites like overleaf for latex compilation. This project is also connected to this [CLI](https://github.com/fyrahundra/latex_cli).

## Content

- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)

## Installation

### Prerequisites

- Linux, macOS, or Windows with WSL2
- [Docker](https://docs.docker.com/get-docker/) installed and running
- `make` available in terminal
- An open local port `8080`

### Step-by-step setup

1. Clone the repository and move into the project folder:

```bash
git clone <repository-url>
cd latex_api
```

2. Build the Docker image (no cache):

```bash
make build
```

Optional: faster build using Docker cache:

```bash
make build-cached
```

3. Run the API container:

```bash
make run
```

4. Open the app in your browser (or use the CLI):

```text
http://localhost:8080
```

5. Stop the running container when done (often not necessary):

```bash
make stop
```

6. Remove the container completely (optional cleanup):

```bash
make terminate
```