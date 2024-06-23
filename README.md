# DOCKER IMAGE FOR PYTHON/NODEJS SCRIPTS

Docker environment for python/nodejs scripts

## Requirements

- Nvida gpu capable of running cuda
- NVIDIA Container Toolkit

## Installation

1) Follow the instructions here to install NVIDIA Container Toolkit
https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html

2) Clone the repository
```
git clone https://github.com/ground-creative/openvoice-docker.git
```

3) Select an ubuntu image that is compatible with the nvidia driver version u plan to use from here
https://hub.docker.com/r/nvidia/cuda/tags

You can find out which version is supported by your driver in one of the following ways:

With cuda installed
```
nvcc --version
```

Without cuda you can look at the driver version on your system and check compatibility from here
https://docs.nvidia.com/deploy/cuda-compatibility/index.html


4) Change environment variables in env.sample file and rename it to .env

## Usage

```
# use USRID=$(id -u) GRPID=$(id -g) when installing OpenVoice and/or API folders
USRID=$(id -u) GRPID=$(id -g) docker compose --project-name=openvoice up -d --build
```
Or
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
