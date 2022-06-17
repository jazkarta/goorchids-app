# syntax = docker/dockerfile:experimental

FROM python:3.9.13

RUN apt-get update
RUN apt-get install -y \
    build-essential \
    gcc \
    g++ \
    libpq-dev \
    libxml2-dev \
    libxslt-dev \
    libmemcached-dev \
    python3-lxml \
    openssl \
    git

RUN pip install --upgrade pip
RUN pip install \
    setuptools==50.3.2 \
    setuptools_scm==4.1.2

WORKDIR /opt/goorchids
COPY . /opt/goorchids

RUN --mount=type=cache,target=/root/.cache/pip pip install -r requirements.txt

RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.1/install.sh | bash

# Node v0.8.14 is really too old, npm won't be able to install packages due to
# https://github.blog/2021-08-23-npm-registry-deprecating-tls-1-0-tls-1-1/
ENV NODE_VERSION=v14.19.3
RUN bash -c "source ~/.bashrc && nvm install ${NODE_VERSION}"
RUN mkdir -p dev/node/bin && \
    ln -s /root/.nvm/versions/node/${NODE_VERSION}/bin/node dev/node/bin/node && \
    ln -s /root/.nvm/versions/node/${NODE_VERSION}/bin/r.js dev/node/bin/r.js
RUN bash -c "source ~/.bashrc && dev/jsbuild"

WORKDIR /opt/goorchids/goorchids
ENV DJANGO_SETTINGS_MODULE=goorchids.settings.docker
EXPOSE 8000
CMD python manage.py runserver 0:8000
