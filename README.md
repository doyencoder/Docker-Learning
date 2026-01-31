# Docker quick reference

## Core Docker commands
- Build image: `docker build -t myimage:tag .`
- Build with args: `docker build --build-arg KEY=value -t myimage:tag .`
- Run container (port map, env file): `docker run --rm -it -p 8000:8000 --env-file .env myimage:tag`
- List containers: `docker ps` (running), `docker ps -a` (all)
- Logs: `docker logs -f <container>`
- Exec shell: `docker exec -it <container> /bin/sh`
- Stop/remove container: `docker stop <container> && docker rm <container>`
- Remove image: `docker rmi myimage:tag`
- Clean unused: `docker system prune -f` (add `--volumes` to prune volumes)
- Tag and push to registry: `docker tag myimage:tag user/repo:tag` then `docker push user/repo:tag`

## Helpful extras
- Copy file from container: `docker cp <container>:/path/in/container ./local/path`
- Save/load image as tar: `docker save myimage:tag -o image.tar` and `docker load -i image.tar`

## Minimal Dockerfile template
```Dockerfile
FROM python:3.11-slim AS base
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["python", "app.py"]
```

## Dockerfile syntax tips
- `FROM image[:tag] [AS stage]`: choose base image; use stages for multi-stage builds.
- `WORKDIR /path`: sets working directory for subsequent commands.
- `COPY <src> <dest>`: copy files; prefer COPY over ADD unless you need tar auto-extract or remote URLs.
- `RUN <cmd>`: executed at build-time; chain with `&&` and clean caches to keep layers small.
- `ENV KEY=value`: set environment variables for runtime and later build steps.
- `ARG KEY[=default]`: build-time variables; usable until the next stage begins.
- `EXPOSE <port>`: documents container port; does not publish by itself.
- `CMD ["exec", "form"]`: default runtime command; one per Dockerfile (last wins).
- `ENTRYPOINT ["exec", "form"]`: fixed entry; combine with CMD for defaults (`ENTRYPOINT ["app"]` + `CMD ["--help"]`).
- `HEALTHCHECK --interval=30s --timeout=5s --retries=3 CMD curl -f http://localhost:8000/health || exit 1`
- `USER appuser`: drop root where possible; create user first (`RUN useradd -m appuser`).
- `VOLUME ["/data"]`: declare mount points for persistent data.
- `LABEL key=value`: metadata like maintainer, version, vcs-url.
- `ONBUILD <instruction>`: triggers in child builds; avoid unless you know you need it.
- `SHELL ["/bin/bash", "-c"]`: change shell for subsequent shell-form RUN.

## Build and run lifecycle (example)
1) Build: `docker build -t myapp:dev .`
2) Run: `docker run --rm -it -p 8000:8000 myapp:dev`
3) Inspect image layers: `docker history myapp:dev`
4) Clean: `docker system prune -f`

## Quick troubleshooting
- Container exits immediately: run with `docker run -it --entrypoint /bin/sh myimage:tag` to inspect.
- Port conflicts: change host port before colon, e.g., `-p 8081:8000`.
- File changes not appearing: rebuild image or use bind mount during dev (`-v %cd%:/app`).

## Docker Setup & Deployment (Generalized)

### Prerequisites
1. Install Docker
2. Create an account on Docker Hub

### Step 1 – Create a Dockerfile
Define how your application should be built and run inside a container.

### Step 2 – Build the Docker image
```bash
docker build -t <dockerhub-username>/<image-name> .
```

### Step 3 – Login to Docker Hub
```bash
docker login
```

### Step 4 – Push the image to Docker Hub
```bash
docker push <dockerhub-username>/<image-name>
```

### Step 5 – Pull the Docker image (any machine)
```bash
docker pull <dockerhub-username>/<image-name>
```

### Step 6 – Run the Docker image locally
```bash
docker run -d -p <host-port>:<container-port> <dockerhub-username>/<image-name>
```

### Example (for clarity)
```bash
docker build -t johndoe/my-app .
docker push johndoe/my-app
docker run -d -p 8000:8000 johndoe/my-app
```
