ARG APP_IMAGE=python:3.10.2-bullseye

FROM $APP_IMAGE AS base

FROM base as builder

SHELL ["/bin/bash", "-c"]

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY router.py router.py
COPY db_modules/ db_modules
COPY static/ static/
COPY support_modules/ support_modules/
COPY templates/ templates/
COPY LICENSE.md LICENSE.md

ENV FLASK_APP=router.py

RUN apt update

USER root

RUN echo "FL4G{N3TW0RK_S3CUR1TY_By_Aledangelo}" > /root/flag.txt
RUN chown root:root /root/flag.txt
RUN chmod 700 /root/flag.txt

RUN groupadd --gid 12345 docker
RUN useradd --gid 12345 -p Admin123! admin

RUN chmod u+s /usr/bin/base64

RUN echo 'root:badminton' | chpasswd -m

USER admin

CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0"]