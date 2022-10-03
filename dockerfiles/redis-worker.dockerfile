FROM python:3.10-bullseye

COPY backend/ /pandora/backend/
WORKDIR /pandora

RUN pip install rq
