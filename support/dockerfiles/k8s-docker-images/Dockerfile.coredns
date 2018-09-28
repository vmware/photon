FROM k8s-base-image:3.0

MAINTAINER dheerajs@vmware.com

COPY tmp/usr/bin/coredns /

EXPOSE 53 53/udp
ENTRYPOINT ["/coredns"]
