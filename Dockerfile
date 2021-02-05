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

# RUN echo "pathes: root: '{tc_root_dir}' config: '{tc_root_dir}/config' database: '{tc_root_dir}/resources/database' database: # path: '{tc_root_dir}/resources/database/taxon_concept.sqlite3' host: ${DATABASE_PROD_IP} port: ${SQL_PORT} name: ${DATABASE_PROD_NAME} user: ${DATABASE_PROD_USER} password: ${DATABASE_PROD_PASSWORD} # Database engine : sqlite, postgresql engine: postgresql test_database: host: ${DATABASE_DEV_IP} port: ${SQL_PORT} name: ${DATABASE_DEV_NAME} user: ${DATABASE_DEV_USER} password: ${DATABASE_DEV_PASSWORD} engine: postgresql jwt: secret: ${JWT_SECRET} expires_in: 28800 # 60*60*8 test_token: token: ${JWT_TEST_TOKEN} logging: pathes: config: '{tc_root_dir}/config/logging.yml' storage: '{tc_root_dir}/var/log/api.log'" >> /usr/src/app/config/config.yml

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

COPY --from=builder /usr/src/app/config/_config.yml ./config/
RUN mv ./config/_config.yml ./config/config.yml

COPY --from=builder /usr/src/app/config/_google-credentials.json.yml ./config/
RUN mv ./config/_google-credentials.json.yml ./config/google-credentials.json.yml

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
ARG FLASK_APP=${FLASK_APP}
ARG FLASK_ARG=${FLASK_ARG}
ARG DATABASE_URL=${DATABASE_URL}
ARG SQL_HOST=${SQL_HOST}
ARG SQL_PORT=${SQL_PORT}
ARG DATABASE=${DATABASE}
ARG APP_FOLDER=${APP_FOLDER}

ARG DATABASE_PROD_IP=${DATABASE_PROD_IP}
ARG DATABASE_PROD_NAME=${DATABASE_PROD_NAME}
ARG DATABASE_PROD_USER=${DATABASE_PROD_USER}
ARG DATABASE_PROD_PASSWORD=${DATABASE_PROD_PASSWORD}

ARG DATABASE_DEV_IP=${DATABASE_DEV_IP}
ARG DATABASE_DEV_NAME=${DATABASE_DEV_NAME}
ARG DATABASE_DEV_USER=${DATABASE_DEV_USER}
ARG DATABASE_DEV_PASSWORD=${DATABASE_DEV_PASSWORD}

ARG DATABASE_TEST_IP=${DATABASE_TEST_IP}
ARG DATABASE_TEST_NAME=${DATABASE_TEST_NAME}
ARG DATABASE_TEST_USER=${DATABASE_TEST_USER}
ARG DATABASE_TEST_PASSWORD=${DATABASE_TEST_PASSWORD}

ARG JWT_SECRET=${JWT_SECRET}
ARG JWT_TEST_TOKEN=${JWT_TEST_TOKEN}
RUN echo $JWT_TEST_TOKEN

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
RUN echo $JWT_TEST_TOKEN

RUN export FLASK_APP=${FLASK_APP}
RUN export FLASK_ENV=${FLASK_ENV}
RUN export DATABASE_URL=${DATABASE_URL}
RUN export SQL_HOST=${SQL_HOST}
RUN export SQL_PORT=${SQL_PORT}
RUN export DATABASE=${DATABASE}
RUN export APP_FOLDER=${APP_FOLDER}

RUN export DATABASE_PROD_IP=${DATABASE_PROD_IP}
RUN export DATABASE_PROD_NAME=${DATABASE_PROD_NAME}
RUN export DATABASE_PROD_USER=${DATABASE_PROD_USER}
RUN export DATABASE_PROD_PASSWORD=${DATABASE_PROD_PASSWORD}

RUN export DATABASE_DEV_IP=${DATABASE_DEV_IP}
RUN export DATABASE_DEV_NAME=${DATABASE_DEV_NAME}
RUN export DATABASE_DEV_USER=${DATABASE_DEV_USER}
RUN export DATABASE_DEV_PASSWORD=${DATABASE_DEV_PASSWORD}

RUN export DATABASE_TEST_IP=${DATABASE_TEST_IP}
RUN export DATABASE_TEST_NAME=${DATABASE_TEST_NAME}
RUN export DATABASE_TEST_USER=${DATABASE_TEST_USER}
RUN export DATABASE_TEST_PASSWORD=${DATABASE_TEST_PASSWORD}

RUN export JWT_SECRET=${JWT_SECRET}
RUN export JWT_TEST_TOKEN=${JWT_TEST_TOKEN}

# RUN echo "pathes: root: '{tc_root_dir}' config: '{tc_root_dir}/config' database: '{tc_root_dir}/resources/database' database: # path: '{tc_root_dir}/resources/database/taxon_concept.sqlite3' host: ${DATABASE_PROD_IP} port: ${SQL_PORT} name: ${DATABASE_PROD_NAME} user: ${DATABASE_PROD_USER} password: ${DATABASE_PROD_PASSWORD} # Database engine : sqlite, postgresql engine: postgresql test_database: host: ${DATABASE_DEV_IP} port: ${SQL_PORT} name: ${DATABASE_DEV_NAME} user: ${DATABASE_DEV_USER} password: ${DATABASE_DEV_PASSWORD} engine: postgresql jwt: secret: ${JWT_SECRET} expires_in: 28800 # 60*60*8 test_token: token: ${JWT_TEST_TOKEN} logging: pathes: config: '{tc_root_dir}/config/logging.yml' storage: '{tc_root_dir}/var/log/api.log'" >> $APP_HOME/config/config.yml

# Mode Debug
RUN export FLASK_DEBUG=false

EXPOSE 5000
VOLUME ./config/
VOLUME ./var/log/

# CMD ["python", "-m", "unittest", "discover", "-v", "-s", "tests/", "-p", "'*_tests.py'"]
CMD flask run -h 0.0.0.0