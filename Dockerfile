#
# Photon Linux Dockerfile
#

FROM scratch
MAINTAINER tliaqat@vmware.com

ADD stage/photon-rootfs.tar.bz2 /

VOLUME /var/lib/docker

CMD ["bash", "--login"]

