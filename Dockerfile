#!/bin/bash

FROM python:bookworm

RUN DEBIAN_FRONTEND=noninteractive apt-get update && \
	apt-get install -yq apt-utils nano

COPY run.sh .

RUN chmod +x run.sh

WORKDIR /app

COPY code/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt
Run pip install git+https://github.com/russian-developer/txsocksx.git

COPY . .

CMD [ "/bin/sh", "/run.sh" ]