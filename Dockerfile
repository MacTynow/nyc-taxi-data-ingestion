FROM python:alpine

RUN apk add -U build-base

WORKDIR /app
COPY requirements.txt /app
RUN pip install -r requirements.txt
COPY . /app

CMD python ingest.py
