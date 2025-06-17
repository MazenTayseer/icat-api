### Build and install packages
FROM --platform=$BUILDPLATFORM python:3.10 as build-python

ENV PYTHONDONTWRITEBYTECODE 1
ENV APP_DIR=/opt/app

WORKDIR $APP_DIR

RUN apt-get -y update \
  && apt-get install -y gettext apache2 apache2-dev \
  # Cleanup apt cache
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /opt/app/pip/requirements.txt
RUN pip3 install pre-commit
COPY .pre-commit-config.yaml .

RUN pip3 install -r /opt/app/pip/requirements.txt

ADD . $APP_DIR

RUN pre-commit install

RUN mkdir -p /opt/python/log/
RUN mkdir -p /opt/app/logs
RUN touch /opt/python/log/icat.log
RUN chown -R www-data:www-data /opt/python/log/

EXPOSE 8000
