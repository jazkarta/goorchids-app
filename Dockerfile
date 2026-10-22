# syntax = docker/dockerfile:experimental

# Python >= 3.10 is required by pip >= 26.2.2 (eMudhra/emSign CA distrust)
FROM python:3.10.22-bookworm

RUN apt-get update && \
    apt-get install -y \
    build-essential \
    gcc \
    g++ \
    libpq-dev \
    libxml2-dev \
    libxslt-dev \
    libmemcached-dev \
    python3-lxml \
    openssl \
    ca-certificates \
    git && \
    rm -rf /var/lib/apt/lists/*

# Pinned by hash: pip < 26.2.2 trusts the compromised emSign CA via its
# vendored certifi. See https://discuss.python.org/t/109576
RUN pip install "pip @ https://files.pythonhosted.org/packages/3f/06/3e4420302363fbb71be3c7f35ce042f54bfca330e3e66b3a2e3c4cca579f/pip-26.2.2-py3-none-any.whl#sha256=fd7f4dfa8190e014013b9f08f3e973f4e4c26ffd179a204895533a7254813a70"
RUN --mount=type=cache,target=/root/.cache/pip pip install \
    setuptools==50.3.2 \
    setuptools_scm==4.1.2

WORKDIR /opt/goorchids
COPY . /opt/goorchids

RUN --mount=type=cache,target=/root/.cache/pip pip install -r requirements.txt

RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.1/install.sh | bash

# Node v0.8.14 is really too old, npm won't be able to install packages due to
# https://github.blog/2021-08-23-npm-registry-deprecating-tls-1-0-tls-1-1/
ENV NODE_VERSION=v14.19.3
# Node and npm (used by dev/jsbuild to npm install build tools) trust only
# the system CA store, not Node's bundled roots, which still include the
# compromised emSign ECC Root CA - G3. See https://discuss.python.org/t/109576
ENV NODE_OPTIONS=--use-openssl-ca
RUN bash -c "source ~/.bashrc && nvm install ${NODE_VERSION}"
RUN mkdir -p dev/node/bin && \
    ln -s /root/.nvm/versions/node/${NODE_VERSION}/bin/node dev/node/bin/node && \
    ln -s /root/.nvm/versions/node/${NODE_VERSION}/bin/r.js dev/node/bin/r.js
RUN bash -c "source ~/.bashrc && dev/jsbuild"

WORKDIR /opt/goorchids/goorchids
ENV DJANGO_SETTINGS_MODULE=goorchids.settings.docker
EXPOSE 8000
CMD python manage.py runserver 0:8000
