FROM python:3.7

MAINTAINER fantaso "fantaso.code@gmail.com"

ENV PYTHONUNBUFRFERED 1
ENV APP_DIR=/app

WORKDIR $APP_DIR

ADD requirements.txt $APP_DIR

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 5000

ADD . $APP_DIR

CMD python application.py runserver 0.0.0.0:8000
