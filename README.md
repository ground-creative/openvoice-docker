# DOCKER IMAGE FOR OPENVOICE

Docker environment for openvoice<br />
https://github.com/myshell-ai/OpenVoice/tree/main


## Requirements

- Nvida gpu capable of running cuda
- NVIDIA Container Toolkit

## Installation

1) Follow the instructions here to install NVIDIA Container Toolkit<br />
https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html


2) Clone the repository
```
git clone https://github.com/ground-creative/openvoice-docker.git
```


3) Select an ubuntu image that is compatible with the nvidia driver version u plan to use from here<br />
https://hub.docker.com/r/nvidia/cuda/tags

You can find out which version is supported by your driver in one of the following ways:

With cuda installed
```
nvcc --version
```


Without cuda you can look at the driver version on your system and check compatibility from here<br />
https://docs.nvidia.com/deploy/cuda-compatibility/index.html


4) Change environment variables in env.sample file and rename it to .env

** You can remove the link to the api from the env file if you jut want to install openvoice

## Usage

```
# use USRID=$(id -u) GRPID=$(id -g) when installing OpenVoice and/or API folders to add the correct permissions
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

It's possible to override environmet variable file while starting or building a container as shown below:
```
TEST=true COMMAND="tail -f /dev/null" docker compose --project-name=openvoice up -d
```
