# syntax = docker/dockerfile:experimental

FROM python:3.9.13

RUN apt-get update -o Acquire::Retries=5 && \
    apt-get install -y --no-install-recommends -o Acquire::Retries=5 \
    build-essential \
    gcc \
    g++ \
    libpq-dev \
    libxml2-dev \
    libxslt-dev \
    libmemcached-dev \
    python3-lxml \
    openssl \
    git && \
    rm -rf /var/lib/apt/lists/*

RUN --mount=type=cache,target=/root/.cache/pip pip install --upgrade pip
RUN --mount=type=cache,target=/root/.cache/pip pip install \
    setuptools==50.3.2 \
    setuptools_scm==4.1.2

WORKDIR /opt/goorchids

ENV PIP_DEFAULT_TIMEOUT=100
COPY requirements.txt requirements.in setup.py package.json Gruntfile.js runtime.txt /opt/goorchids/
COPY external/gobotany-app/setup.py /opt/goorchids/external/gobotany-app/setup.py
RUN grep -v '^-e file:' requirements.txt > /tmp/requirements-docker.txt
RUN --mount=type=cache,target=/root/.cache/pip pip install --retries 10 --no-build-isolation \
    -r /tmp/requirements-docker.txt

COPY goorchids /opt/goorchids/goorchids
COPY external /opt/goorchids/external
COPY dev /opt/goorchids/dev
COPY bin /opt/goorchids/bin

# Node v0.8.14 is really too old, npm won't be able to install packages due to
# https://github.blog/2021-08-23-npm-registry-deprecating-tls-1-0-tls-1-1/
ENV NVM_DIR=/root/.nvm
ENV NODE_VERSION=v14.19.3
RUN mkdir -p "${NVM_DIR}" && \
    curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.1/install.sh | PROFILE=/dev/null NVM_DIR="${NVM_DIR}" bash
RUN bash -c ". ${NVM_DIR}/nvm.sh && nvm install ${NODE_VERSION}"
RUN mkdir -p dev/node/bin && \
    ln -s /root/.nvm/versions/node/${NODE_VERSION}/bin/node dev/node/bin/node && \
    ln -s /root/.nvm/versions/node/${NODE_VERSION}/bin/r.js dev/node/bin/r.js
RUN bash -c ". ${NVM_DIR}/nvm.sh && dev/jsbuild"

WORKDIR /opt/goorchids/goorchids
ENV PYTHONPATH=/opt/goorchids:/opt/goorchids/external/gobotany-app
ENV DJANGO_SETTINGS_MODULE=goorchids.settings.docker
EXPOSE 8000
CMD python manage.py runserver 0:8000
