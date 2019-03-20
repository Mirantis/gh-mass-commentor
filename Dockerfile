FROM jfloff/alpine-python:2.7-slim

MAINTAINER Kyle Squizzato: 'kyle.squizzato@docker.com'

WORKDIR /

RUN pip install --upgrade \
    pip \
    requests \
    colored

COPY ./ghcommentor.py /

ENTRYPOINT ["python", "./ghcommentor.py"]
