###########
# BUILDER #
###########

# pull official base image
# FROM python:3.6.3 as builder
FROM python:3.8.1-slim-buster as builder

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install system dependencies
RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive \
    apt-get install -y --quiet --no-install-recommends \
    gcc libyaml-dev \
    && apt-get -y autoremove \
    && apt-get clean autoclean \
    && rm -fr /var/lib/apt/lists/{apt,dpkg,cache,log} /tmp/* /var/tmp/*

RUN pip install --upgrade pip
COPY . /usr/src/app/

# install python dependencies
RUN export FLASK_APP=src/main.py
RUN set FLASK_APP=src/main.py
COPY ./requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r requirements.txt

#########
# FINAL #
#########

# Pull official base image
FROM python:3.8.17-slim-bullseye

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

CMD flask run -h 0.0.0.0