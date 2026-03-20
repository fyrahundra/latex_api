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
git clone https://github.com/fyrahundra/latex_api.git
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

## Usage

### Web frontend

1. Start the container:

```bash
make run
```

2. Open:

```text
http://localhost:8080
```

3. Upload a `.zip` containing your LaTeX project and compile.

### API endpoint

The API exposes a compile endpoint:

- `POST /compile`

Example request with `curl`:

```bash
curl -X POST \
	-F "file=@/path/to/project.zip" \
	http://localhost:8080/compile \
	--output output.pdf
```

If compilation succeeds, the response body is a PDF file.

### Notes for ZIP input

- The ZIP must contain at least one `.tex` file.
- The service prefers `garb.tex` if present.
- Max upload size is 5 MB.

## Features

- Dockerized runtime with LaTeX toolchain included.
- Static frontend served at `/` for upload and compile flow.
- API-based compilation via `POST /compile`.
- Automatic `.tex` file discovery in uploaded projects.
- Optional font package fallback patching for `.sty` files (for environments missing `tgpagella`).
- Uses `latexmk` for robust multi-pass LaTeX builds.
- Returns compilation output directly as a PDF response.