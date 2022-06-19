FROM python:3.10-alpine

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt

RUN apk add --update --no-cache postgresql-client jpeg-dev
RUN apk add --update --no-cache --virtual .temp-build-deps \
    gcc libc-dev linux-headers postgresql-dev musl-dev zlib zlib-dev
RUN pip install -r requirements.txt
RUN apk del .temp-build-deps

RUN mkdir /www
WORKDIR /www
COPY . /www

RUN adduser -D nazrul
RUN chown -R nazrul:nazrul /www
RUN chmod -R 755 /www
USER nazrul