FROM jenkins/jenkins:lts

USER root

RUN echo "deb http://deb.debian.org/debian bookworm main" > /etc/apt/sources.list && \
    echo "deb http://deb.debian.org/debian bookworm-updates main" >> /etc/apt/sources.list && \
    echo "deb http://security.debian.org/debian-security bookworm-security main" >> /etc/apt/sources.list

RUN apt-get update && apt-get install -y \
    qemu-system \
    wget \
    unzip \
    python3 \
    python3-pip \
    chromium \
    chromium-driver

RUN pip3 install \
    selenium \
    locust 

RUN jenkins-plugin-cli --plugins workflow-aggregator git docker-workflow

EXPOSE 8080
EXPOSE 50000
