ARG APP_IMAGE=python:3.9.10-alpine

FROM $APP_IMAGE AS base

FROM base as builder

RUN mkdir /install
WORKDIR /install

COPY requirements.txt /requirements.txt

RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install --prefix=/install -r /requirements.txt

USER guest

FROM base
ENV FLASK_APP=router.py
WORKDIR /project
COPY --from=builder /install /usr/local
ADD . /project

ENTRYPOINT ["python", "-m", "flask", "run", "--host=0.0.0.0"]