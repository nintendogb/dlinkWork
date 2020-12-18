FROM ubuntu:latest
RUN apt-get update && \
    apt-get install -y software-properties-common && \
    add-apt-repository ppa:deadsnakes/ppa && \
    apt-get install -y python3.7 python3-pip && \
    apt-get install -y dnsutils && \
    apt-get install -y net-tools && \
    apt-get install -y vim nano && \
    apt-get install -y wget
RUN rm /bin/sh && ln -s /bin/bash /bin/sh
RUN pip3 install jsonschema && \
    pip3 install sre_yield && \
    pip3 install sortedcontainers && \
    pip3 install aiohttp
COPY ./dcd_tester_docker /
