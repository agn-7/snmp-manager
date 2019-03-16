FROM python:3.6-slim


MAINTAINER Benyamin Jafari <benyamin@infravision.ir>

ENV PYTHONUNBUFFERED 1
ENV CONFIG_PATH=/app/config/config.json
ENV SENTRY_DSN=http://3c50d4696400490daa1781671331221b@192.168.1.136/5

RUN mkdir /app
WORKDIR /

ADD requirements.txt /app
RUN pip install -r app/requirements.txt

ADD . /app

CMD python app
