#===============================================
#======  Using Python 3.9 build Imange =========
#===============================================

FROM python:3.9.5-slim-buster

LABEL maintainer="Thai Hoc <nguyenthaihoc@outlook.com>"

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
RUN apt-get update

COPY ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
