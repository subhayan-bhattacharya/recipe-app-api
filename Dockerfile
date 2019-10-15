FROM python:3.7-alpine

MAINTAINER Subhayan Bhattacharya

ENV PYTHONUNBUFFERED 1

COPY Pipfile* /tmp/

RUN cd /tmp && pip install pipenv && pipenv lock --requirements > requirements.txt

RUN apk add --update --no-cache postgresql-client

RUN apk add --update --no-cache --virtual .tmp-build-deps \
    gcc libc-dev linux-headers postgresql-dev

RUN pip install -r /tmp/requirements.txt

RUN apk del .tmp-build-deps

RUN mkdir /app

WORKDIR /app

COPY ./app /app

RUN adduser -D user
USER user




