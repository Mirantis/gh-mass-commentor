FROM python:3.7.2-slim

MAINTAINER Kyle Squizzato: 'kyle.squizzato@docker.com'

RUN pip install --upgrade \
    pip \
    shell==1.0.1 \
    LogrusFormatter==0.1a0 \
    PyGithub==1.43.5 \
    six==1.11.0

COPY ghcommentor.py /ghcommentor.py
RUN chmod +x /ghcommentor.py

ENTRYPOINT ["python3", "/ghcommentor.py"]
