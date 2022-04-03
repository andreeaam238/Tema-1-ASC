FROM tgagor/centos:stream8
#FROM centos:centos7

LABEL maintainer="eduard.staniloiu@upb.ro" \
      name="ASC Grid Docker Image" \
      version=${VERSION}

ENV DEBIAN_FRONTEND="noninteractive"

ENV TZ=Europe/Bucharest

RUN yum install -y epel-release

RUN yum install -y dnf-plugins-core

# Uncomment for CentOS7
#RUN yum-config-manager --enable repository powertools

# Uncomment for CentOS8
RUN yum config-manager --set-enabled powertools

RUN yum install -y gcc gcc-c++ kernel-devel make

RUN yum install -y valgrind

RUN yum install -y kcachegrind

RUN yum install -y graphviz

RUN yum install -y dbus-x11

RUN yum install -y blas blas-devel atlas atlas-devel lapack-devel

RUN yum install -y gnuplot

RUN yum install -y wget

RUN yum install -y vim

#RUN wget https://download.oracle.com/java/18/latest/jdk-18_linux-x64_bin.rpm

#RUN rpm -ivh jdk-18_linux-x64_bin.rpm

WORKDIR /asc

RUN mkdir kcachegrind-dbus

COPY ./startup.sh /asc/

RUN ["chmod", "+x", "/asc/startup.sh"]

ENTRYPOINT ["/asc/startup.sh"]
