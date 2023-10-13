# DOCKER IMAGE FOR PYTHON SCRIPTS

Docker environment for python scripts

## Installation

1) Clone the repository
```
git clone https://github.com/ground-creative/docker-python
```
2) Create a folder named volume and store your code there
```
mkdir volume
```

3) Change environment variables in env.sample file and rename it to .env

## Usage

```
docker compose --project-name=test up -d
```
Or
```
docker compose --project-name=test up -d --build
```

### Command Environment Variables

It's possible to override environmet variable file while starting or building a container

| Command | Description |
| ------------- | ------------- |
| CONTAINER_NAME | Container name |
| TEST | Keeps the container running and ignores any startup commands |
| DOCKER_IMAGE | Which image to use |
| COMMAND | Run startup command |
| VOLUME | Which volume to use |
| WORK_DIR | Container working directory |
| DOCKER_FILE | Docker build file |

### Example usage
```
TEST=true COMMAND="tail -f /dev/null" docker compose --project-name=test up -d
```