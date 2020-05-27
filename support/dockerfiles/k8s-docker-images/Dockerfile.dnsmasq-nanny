FROM k8s-base-image:3.0

MAINTAINER kulkarniv@vmware.com

COPY [ "./stage-rpms-tdnf.conf", "./tmp/stage-rpms.repo", "/tmp/tdnf/" ]
RUN tdnf -c /tmp/tdnf/stage-rpms-tdnf.conf install -y dnsmasq --refresh

RUN echo "user=root" > /etc/dnsmasq.conf
RUN mkdir -p /var/run/
STOPSIGNAL SIGCONT

RUN mkdir -p /etc/k8s/dns/dnsmasq-nanny
ADD tmp/k8dns/usr/bin/dnsmasq-nanny /dnsmasq-nanny
ENTRYPOINT ["/dnsmasq-nanny"]
