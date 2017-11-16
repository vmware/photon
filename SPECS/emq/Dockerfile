# Copyright (c) 2017 VMware, Inc.

FROM vmware/photon:1.0

MAINTAINER ucp-eng <ucp-eng@vmware.com>

ENV EMQ_VERSION=v2.1.2

COPY ./start.sh /opt/emqttd/start.sh
COPY ./emqttd-2.1.2-1.x86_64.rpm /emqttd-2.1.2-1.x86_64.rpm

RUN set -ex \
    && tdnf install sed gawk shadow net-tools -y \
    && rpm -ivh emqttd-2.1.2-1.x86_64.rpm \
    && chmod +x /opt/emqttd/start.sh \
    && ln -s /opt/emqttd/bin/* /usr/local/bin/

WORKDIR /opt/emqttd

CMD ["/opt/emqttd/start.sh"]

VOLUME ["/opt/emqttd/log", "/opt/emqttd/data", "/opt/emqttd/lib", "/opt/emqttd/etc"]

# emqttd will occupy these port:
# - 1883 port for MQTT
# - 8883 port for MQTT(SSL)
# - 8083 for WebSocket/HTTP
# - 8084 for WSS/HTTPS
# - 18083 for dashboard
# - 4369 for port mapping
# - 6000-6999 for distributed node
EXPOSE 1883 8883 8083 8084 18083 4369 6000-6999
