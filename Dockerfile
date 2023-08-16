#+----------------------------------------------------------------------+
# BUILDER

# Pull official base image
FROM python:3.8.1-slim-bullseye AS builder

# Set work directory
WORKDIR /usr/src/app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies
RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive \
        apt-get install -y --quiet --no-install-recommends \
        gcc libyaml-dev \
    && apt-get -y autoremove \
    && apt-get clean autoclean \
    && rm -fr /var/lib/apt/lists/{apt,dpkg,cache,log} /tmp/* /var/tmp/*

# Lint
RUN pip install --upgrade pip
# TODO: See if we need to install and run Flake8
# RUN pip install flake8==6.0.0
COPY . /usr/src/app/
# RUN flake8 --ignore=E501,F401 .

# Install python dependencies
RUN export FLASK_APP=src/main.py
RUN set FLASK_APP=src/main.py
COPY ./requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r requirements.txt


#+----------------------------------------------------------------------+
# Base

# Pull official base image
FROM python:3.8.17-slim-bullseye AS base

# Set default environment variables
ENV HOME="/home/app"
ENV APP_HOME="/home/app/web"
ENV FLASK_APP="src/main.py"

# Create new user "app" with group and home directory
RUN useradd --create-home --shell /bin/bash app

# Uncomment alias from user "app" .bashrc file
RUN sed -i -r 's/^#(alias|export|eval)/\1/' "$HOME/.bashrc"

# Create the web app directory and set as default
RUN mkdir $APP_HOME
WORKDIR $APP_HOME

# Install additional packages
RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive \
        apt-get install -y --quiet --no-install-recommends \
        netcat vim iputils-ping curl \
    && apt-get -y autoremove \
    && apt-get clean autoclean \
    && rm -fr /var/lib/apt/lists/{apt,dpkg,cache,log} /tmp/* /var/tmp/*

# Add /etc/vim/vimrc.local
RUN echo "runtime! defaults.vim" > /etc/vim/vimrc.local \
    && echo "let g:skip_defaults_vim = 1" >> /etc/vim/vimrc.local  \
    && echo "set mouse=" >> /etc/vim/vimrc.local

# Copy files from "builder" temporary image
COPY --from=builder /usr/src/app/wheels /wheels
COPY --from=builder /usr/src/app/requirements.txt .

COPY --from=builder /usr/src/app/config/_config.yml ./config/
RUN mv ./config/_config.yml ./config/config.yml

COPY --from=builder /usr/src/app/config/_google-credentials.json ./config/
RUN mv ./config/_google-credentials.json ./config/google-credentials.json

# Install dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache /wheels/*

# Copy project
COPY . $APP_HOME

# Chown all the files to the "app" user
RUN chown -R app:app $APP_HOME

# Change to the "app" user
USER app

EXPOSE 5000
VOLUME ./config/
VOLUME ./var/log/


#+----------------------------------------------------------------------+
# Development
FROM base AS development

CMD flask run -h 0.0.0.0


#+----------------------------------------------------------------------+
# Production
FROM base AS production

RUN pip install --no-cache-dir gunicorn==21.2.0

CMD [ "gunicorn", "--bind", "0.0.0.0:5000", "manage:app" ]
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 CMD curl -f http://localhost:5000/health