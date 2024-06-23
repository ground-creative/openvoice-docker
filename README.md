# DOCKER IMAGE FOR PYTHON/NODEJS SCRIPTS

Docker environment for python/nodejs scripts

## Installation

1) Clone the repository
```
git clone https://github.com/ground-creative/openvoice-docker.git
```
2) Create a folder named volume and store your code there
```
mkdir volume
```

3) Change environment variables in env.sample file and rename it to .env

## Usage

```
docker compose --project-name=openvoice up -d
```
Or
```
docker compose --project-name=openvoice up -d --build
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
| TIMEZONE | server timezone |
| LOG_DRIVER | log driver |
| RESTART | docker restart options |

### Example usage
```
TEST=true COMMAND="tail -f /dev/null" docker compose --project-name=test up -d
```

https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html

curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg \
  && curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
    sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
    sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list

sudo apt-get update

sudo apt-get install -y nvidia-container-toolkit

sudo nvidia-ctk runtime configure --runtime=docker

sudo systemctl restart docker


watch -n 1 nvidia-smi


https://hub.docker.com/r/nvidia/cuda/tags?page=1&page_size=&ordering=&name=


USRID=$(id -u) GRPID=$(id -g) docker compose --project-name=openvoice up -d --build
