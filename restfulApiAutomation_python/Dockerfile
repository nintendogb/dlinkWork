FROM ubuntu:latest

RUN apt-get update && \
    apt-get install -y software-properties-common && \
    add-apt-repository ppa:deadsnakes/ppa && \
    apt-get install -y python3.7 python3-pip && \
    apt-get install -y vim nano && \
    pip3 install setuptools && \
    pip3 install -I cryptography && \
    pip3 install -I Authlib
COPY . /
RUN python3 setup.py install
ENV LANG=C.UTF-8 \
    LC_ALL=C.UTF-8
