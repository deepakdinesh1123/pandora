FROM ubuntu:22.04
RUN apt -y update && apt -y upgrade && apt install curl
RUN curl -fsSL https://deb.nodesource.com/setup_19.x | bash - &&\
apt-get install -y nodejs