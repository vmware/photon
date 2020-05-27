FROM k8s-base-image:3.0

MAINTAINER kulkarniv@vmware.com

ADD tmp/k8dns/usr/bin/kube-dns /kube-dns
ENTRYPOINT ["/kube-dns"]
