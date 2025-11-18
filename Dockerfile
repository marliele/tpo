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
    python3-venv \
    chromium \
    chromium-driver

RUN pip3 install \
    selenium \
    locust \
    requests \
    urllib3

RUN ln -sf /usr/bin/python3 /usr/bin/python || true
RUN ln -sf /usr/local/bin/locust /usr/bin/locust || true

RUN ls -la /usr/bin/python* && \
    ls -la /usr/bin/locust /usr/local/bin/locust 2>/dev/null || echo "Python and Locust links created"

RUN jenkins-plugin-cli --plugins workflow-aggregator git docker-workflow

EXPOSE 8080
EXPOSE 50000
