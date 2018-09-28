FROM k8s-base-image:3.0

MAINTAINER kulkarniv@vmware.com

COPY [ "./stage-rpms-tdnf.conf", "./tmp/stage-rpms.repo", "/tmp/tdnf/" ]
RUN tdnf -c /tmp/tdnf/stage-rpms-tdnf.conf install -y openssl nginx shadow zlib-devel --refresh
RUN useradd --system --no-create-home -U -s /bin/false nginx

# forward nginx access and error logs to stdout and stderr
RUN ln -sf /proc/1/fd/1 /var/log/nginx/access.log && \
    ln -sf /proc/1/fd/2 /var/log/nginx/error.log

COPY [ "./tmp/nginxinc/usr/share/nginx-ingress/docker/nginx.ingress.tmpl", \
       "./tmp/nginxinc/usr/share/nginx-ingress/docker/nginx.tmpl", \
       "./tmp/nginxinc/usr/bin/nginx-ingress", \
       "/" ]

RUN mkdir -p /etc/nginx/secrets/ && \
    mkdir -p /etc/nginx/conf.d && \
    cd /etc/nginx/secrets && \
    openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout default.key -out default.crt -subj "/CN=NGINXIngressController" && \
    cat default.key default.crt > default && \
    rm default.key default.crt

ENTRYPOINT ["/nginx-ingress"]
