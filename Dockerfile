ARG APP_IMAGE=python:3.10.2-bullseye

FROM $APP_IMAGE AS base

FROM base as builder

SHELL ["/bin/bash", "-c"]

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

ENV FLASK_APP=router.py

RUN apt update

USER root

RUN echo "DSP{N3TW0RK_S3CUR1TY_FL4G}" > /flag.txt
RUN chown root:root /flag.txt
RUN chmod 700 /flag.txt

RUN groupadd --gid 12345 docker
RUN useradd --gid 12345 -p Admin123! admin

RUN chmod u+s /usr/bin/base64

USER admin

CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0"]