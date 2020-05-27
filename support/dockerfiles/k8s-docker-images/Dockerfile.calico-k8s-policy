FROM k8s-base-image:3.0

MAINTAINER kulkarniv@vmware.com

ADD tmp/calico/usr/bin/controller /dist/

ENTRYPOINT ["/dist/controller"]
