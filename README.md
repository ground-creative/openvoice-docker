# DOCKER IMAGE FOR PYTHON SCRIPTS

Docker environment for python scripts

## Installation

Clone the repository
```
git clone https://github.com/ground-creative/docker-python
```

## Usage

```
NAME=test docker compose --project-name=test up -d --build
```

### Command Environment Variables

| Command | Description | Default Value | Required |
| ------------- | ------------- | ------------- | ------------- |
| NAME=  | Container name | None | Yes |
| TEST=  | (true\|false) Container name | false | No |