FROM ubuntu:22.04

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update && \
    apt-get install -y python3.11 && \
    apt-get install -y python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
    
ENV PATH="/usr/bin/python3.11:${PATH}"

RUN apt-get update
RUN apt-get install -y apt-utils
RUN apt-get install -y curl
RUN apt-get install -y lsb-release
RUN apt-get install -y libatlas-base-dev
RUN su
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
RUN curl https://packages.microsoft.com/config/ubuntu/$(lsb_release -rs)/prod.list > /etc/apt/sources.list.d/mssql-release.list
RUN apt-get update
RUN ACCEPT_EULA=Y apt-get install -y msodbcsql17
RUN echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bashrc

RUN  apt install -y unixodbc-dev
RUN  apt-get update
RUN apt-get install -y libpq-dev


RUN mkdir /ic_system
WORKDIR /ic_system
COPY . /ic_system

RUN pip3 install poetry

RUN poetry install --no-root