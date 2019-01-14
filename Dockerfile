FROM python:3.6-slim


MAINTAINER Benyamin Jafari <benyamin@infravision.ir>

ENV PYTHONUNBUFFERED 1

RUN mkdir /app
WORKDIR /

ADD requirements.txt /app
RUN pip install -r app/requirements.txt

ADD . /app

CMD python app
