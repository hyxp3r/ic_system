FROM ubuntu:latest
ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update && \
    apt-get install -y python3.11 && \
    apt-get install -y python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
    
ENV PATH="/usr/bin/python3.11:${PATH}"




RUN mkdir /ic_system
WORKDIR /ic_system
COPY . /ic_system

RUN pip3 install poetry

RUN poetry install --no-root