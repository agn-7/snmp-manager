FROM python:3.6-slim


MAINTAINER Benyamin Jafari <benyamin@infravision.ir>

ENV PYTHONUNBUFFERED 1
ENV CONFIG_PATH=/app/config/config.json
ENV SENTRY_DSN=http://78bb380df55444c584d010e0edfc3859@192.168.1.136/5

RUN mkdir /app
WORKDIR /

ADD requirements.txt /app
RUN pip install -r app/requirements.txt

ADD . /app

CMD python app
