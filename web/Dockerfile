FROM python:3.7-slim

# install system dependencies
RUN apt-get update && apt-get install -y netcat

RUN python -m pip install --upgrade pip

COPY requirements.txt requirements.txt
RUN python -m pip install -r requirements.txt

COPY  . .

