FROM k8s-base-image:3.0

MAINTAINER kulkarniv@vmware.com

ENV FLANNEL_ARCH=amd64

COPY [ "./stage-rpms-tdnf.conf", "./tmp/stage-rpms.repo", "/tmp/tdnf/" ]
RUN tdnf -c /tmp/tdnf/stage-rpms-tdnf.conf install -y iproute2 iptables --refresh

ADD tmp/flannel/usr/bin/flanneld /opt/bin/flanneld
COPY tmp/flannel/usr/share/flannel/docker/mk-docker-opts.sh /opt/bin/
RUN ln -s /usr/sbin/iptables /usr/local/bin/iptables

ENTRYPOINT ["/opt/bin/flanneld"]
