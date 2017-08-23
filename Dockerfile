#
# Photon Linux Dockerfile
#

FROM scratch
LABEL maintainer tliaqat@vmware.com

ADD stage/photon-rootfs-$PHOTON_RELEASE_VERSION-$PHOTON_BUILD_NUMBER.tar.bz2 /

VOLUME /var/lib/docker

CMD ["bash", "--login"]

