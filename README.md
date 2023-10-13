# DOCKER IMAGE FOR PYTHON SCRIPTS

Docker environment for python scripts

## Installation

1) Clone the repository
```
git clone https://github.com/ground-creative/docker-python
```
2) Create a folder named code and store there the python scripts with a requirements.txt file

## Usage

```
NAME=test docker compose --project-name=test up -d --build
```

### Command Environment Variables

| Command | Description | Default Value | Required |
| ------------- | ------------- | ------------- | ------------- |
| NAME= | Container name | None | Yes |
| TEST= | (true\|false) Container name | false | No |