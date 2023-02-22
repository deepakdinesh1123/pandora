# Use an existing base image with an operating system and pre-installed tools
FROM ubuntu:20.04

# Install Java
RUN apt-get update && \
    apt-get install -y default-jdk

# Set environment variables
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
ENV PATH="$PATH:$JAVA_HOME/bin"