FROM k8s-base-image:3.0

MAINTAINER kaushikk@vmware.com

ADD tmp/k8heapster/usr/bin/heapster /heapster
ADD tmp/k8heapster/usr/bin/eventer /eventer

#   nobody:nobody
USER 65534:65534
ENTRYPOINT ["/heapster"]
