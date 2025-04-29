FROM python:3.6-slim

ENV PYTHONUNBUFFERED 1
ENV CONFIG_PATH=/app/config/config.json

RUN mkdir /app
WORKDIR /

ADD requirements.txt /app
RUN pip install -r app/requirements.txt

ADD . /app
WORKDIR /app

CMD python snmp_collector
