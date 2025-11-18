FROM jenkins/jenkins:lts

USER root

RUN apt-get update && apt-get install -y \
    qemu-system \
    wget \
    unzip \
    python3 \
    python3-pip \
    python3-venv \
    chromium \
    chromium-driver

RUN pip3 install \
    selenium \
    locust \
    requests \
    urllib3

RUN jenkins-plugin-cli --plugins workflow-aggregator git docker-workflow

EXPOSE 8080
EXPOSE 50000
