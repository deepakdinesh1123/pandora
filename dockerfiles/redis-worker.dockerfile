FROM python:3.10-bullseye

COPY backend/ /pandora/backend/
WORKDIR /pandora

# RUN apt-get update && apt -y upgrade
# RUN apt install -y python3
# RUN apt install -y python3-pip

RUN pip install rq

ENTRYPOINT [ "rq", "worker", "--url", "redis://redis:6379" ]
