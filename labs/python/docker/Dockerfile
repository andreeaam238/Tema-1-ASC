FROM ubuntu:20.04

LABEL maintainer="stefan_dan.ciocirlan@upb.ro,eduard.staniloiu@upb.ro" \
      name="ASC Grid - Labs Docker Image" \
      version="${VERSION}"

ENV DEBIAN_FRONTEND="noninteractive"

RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install python3-pip -y
RUN apt-get install nano -y
RUN apt-get install git -y
RUN apt-get install unzip -y
RUN apt-get install wget -y

RUN python3 -m pip install -U pip
RUN python3 -m pip install -U pylint

ENV DISPLAY=host.docker.internal:0.0

WORKDIR /app
