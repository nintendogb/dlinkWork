FROM ubuntu:latest

RUN apt-get update && \
    apt-get install -y software-properties-common && \
    add-apt-repository ppa:deadsnakes/ppa && \
    apt-get install -y python3.7 python3-pip && \
    pip3 install setuptools
COPY . /
RUN python3 setup.py install
ENV PYTHONIOENCODING=utf-8
ENTRYPOINT ["python3"]
CMD ["./webpage/start.py"]
