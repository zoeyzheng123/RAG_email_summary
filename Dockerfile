# syntax = docker/dockerfile:1.3
FROM python:3.13-slim

RUN --mount=type=cache,target=/root/.cache pip install pip==22.3 pip-tools==6.9.0

COPY src /src
COPY requirements /requirements

RUN --mount=type=cache,target=/root/.cache cd /requirements; pip-sync requirements.txt

RUN pip install black isort

ARG SENTRY_RELEASE=local_sentry_release

ENV PYTHONIOENCODING=utf-8 \
	PYTHONDONTWRITEBYTECODE=1 \
	PYTHONPATH=/src \
	SENTRY_RELEASE=${SENTRY_RELEASE}

WORKDIR /src
