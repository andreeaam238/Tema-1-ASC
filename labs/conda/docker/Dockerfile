FROM ubuntu:20.04

LABEL maintainer="eduard.staniloiu@upb.ro" \
      name="ASC Grid Docker Image" \
      version=${VERSION}

ENV DEBIAN_FRONTEND="noninteractive"

ENV TZ=Europe/Bucharest

WORKDIR /app

RUN apt-get update

RUN apt-get install -y wget

RUN apt-get install -y python3

RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh

RUN chmod +x ~/miniconda.sh && ~/miniconda.sh -b -p $HOME/miniconda

COPY ./conda-env.yml /app/

COPY ./entrypoint.sh /entrypoint.sh

RUN ["chmod", "+x", "/entrypoint.sh"]

RUN /entrypoint.sh conda init bash
RUN /entrypoint.sh conda env create -f /app/conda-env.yml
#RUN ~/miniconda/bin/conda create -f /app/conda-env.yml

ENTRYPOINT ["/entrypoint.sh"]
