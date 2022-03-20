FROM ubuntu:20.04

LABEL maintainer="eduard.staniloiu@upb.ro" \
      name="ASC Grid Docker Image" \
      version=${VERSION}

ENV DEBIAN_FRONTEND="noninteractive"

ENV TZ=Europe/Bucharest


RUN apt-get update

RUN apt-get install -y build-essential

RUN apt-get install -y gcc

RUN apt-get install -y valgrind

RUN apt-get install -y kcachegrind

RUN apt-get install -y dbus-x11

RUN apt-get install -y libatlas-base-dev liblapack-dev libblas-dev

#ENV DISPLAY=host.docker.internal:0.0

WORKDIR /asc

RUN mkdir kcachegrind-dbus

#ENV XDG_RUNTIME_DIR=/asc/kcachegrind-dbus
#RUN export $(dbus-launch)

COPY ./startup.sh /asc/

RUN ["chmod", "+x", "/asc/startup.sh"]

ENTRYPOINT ["/asc/startup.sh"]
