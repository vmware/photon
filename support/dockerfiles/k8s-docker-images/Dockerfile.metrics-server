FROM k8s-base-image:4.0

MAINTAINER dheerajs@vmware.com

COPY tmp/k8smetserv/usr/bin/metrics-server /

ENTRYPOINT ["/metrics-server"]
