FROM python:3.9

COPY . /app
WORKDIR /app

RUN make install-dependencies
