#
# Ubuntu-Dev Dockerfile for building Linux Distribution.
#

FROM ubuntu:14.04

RUN \
  sed -i 's/# \(.*multiverse$\)/\1/g' /etc/apt/sources.list && \
  apt-get update && \
  apt-get -y upgrade && \
  apt-get install -y build-essential && \
  apt-get install -y bison gawk g++ createrepo python-aptdaemon genisoimage docker.io && \
  rm -f /bin/sh && \
  ln -s /bin/bash /bin/sh && \
  rm -rf /var/lib/apt/lists/*

WORKDIR ~/

CMD ["bash"]
