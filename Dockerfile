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
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc libyaml-dev && \
    apt-get clean

# lint
RUN pip install --upgrade pip
# RUN pip install flake8
COPY . /usr/src/app/
# RUN flake8 --ignore=E501,F401 .

# install python dependencies
RUN export FLASK_APP=src/main.py
RUN set FLASK_APP=src/main.py
COPY ./requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r requirements.txt


#########
# FINAL #
#########

# pull official base image
# FROM python:3.6.3 as builder
FROM python:3.8.1-slim-buster

# create directory for the app user
RUN mkdir -p /home/app

# create the app user
RUN addgroup --system app && adduser --system --group app


# create the appropriate directories
ENV HOME=/home/app
ENV APP_HOME=/home/app/web

RUN mkdir $APP_HOME
WORKDIR $APP_HOME

# install dependencies
RUN apt-get update && apt-get install -y --no-install-recommends netcat
COPY --from=builder /usr/src/app/wheels /wheels
COPY --from=builder /usr/src/app/requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache /wheels/*

# copy project
COPY . $APP_HOME

# chown all the files to the app user
RUN chown -R app:app $APP_HOME

# change to the app user
USER app

# Exporter des variables sur votre terminal
RUN export FLASK_APP=src/main.py
# Configurer
RUN set FLASK_APP=src/main.py

# env app
ENV FLASK_APP=${FLASK_APP}
ENV FLASK_ENV=${FLASK_ENV}
ENV DATABASE_URL=${DATABASE_URL}
ENV SQL_HOST=${SQL_HOST}
ENV SQL_PORT=${SQL_PORT}
ENV DATABASE=${DATABASE}
ENV APP_FOLDER=${APP_FOLDER}

ENV DATABASE_PROD_IP=${DATABASE_PROD_IP}
ENV DATABASE_PROD_NAME=${DATABASE_PROD_NAME}
ENV DATABASE_PROD_USER=${DATABASE_PROD_USER}
ENV DATABASE_PROD_PASSWORD=${DATABASE_PROD_PASSWORD}

ENV DATABASE_DEV_IP=${DATABASE_DEV_IP}
ENV DATABASE_DEV_NAME=${DATABASE_DEV_NAME}
ENV DATABASE_DEV_USER=${DATABASE_DEV_USER}
ENV DATABASE_DEV_PASSWORD=${DATABASE_DEV_PASSWORD}

ENV DATABASE_TEST_IP=${DATABASE_TEST_IP}
ENV DATABASE_TEST_NAME=${DATABASE_TEST_NAME}
ENV DATABASE_TEST_USER=${DATABASE_TEST_USER}
ENV DATABASE_TEST_PASSWORD=${DATABASE_TEST_PASSWORD}

ENV JWT_SECRET=${JWT_SECRET}
ENV JWT_TEST_TOKEN=${JWT_TEST_TOKEN}

# Mode Debug
RUN export FLASK_DEBUG=false

EXPOSE 80
VOLUME $APP_HOME

# CMD ["python", "-m", "unittest", "discover", "-v", "-s", "tests/", "-p", "'*_tests.py'"]
CMD flask run -h 0.0.0.0