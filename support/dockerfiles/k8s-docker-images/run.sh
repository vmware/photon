#!/bin/bash
set -x

spool_dir="/var/spool/wavefront-proxy"
mkdir -p $spool_dir

WAVEFRONT_HOSTNAME=${WAVEFRONT_HOSTNAME:-$(hostname)}
export WAVEFRONT_HOSTNAME

autoconf=/opt/wavefront/wavefront-proxy/bin/autoconf-wavefront-proxy.sh
/bin/bash -x $autoconf

java_heap_usage=${JAVA_HEAP_USAGE:-4G}
java \
	-Xmx$java_heap_usage -Xms$java_heap_usage \
	-Djava.util.logging.manager=org.apache.logging.log4j.jul.LogManager \
	-Dlog4j.configurationFile=/etc/wavefront/wavefront-proxy/log4j2.xml \
	-jar /opt/wavefront-push-agent.jar \
	-f /etc/wavefront/wavefront-proxy/wavefront.conf \
	$WAVEFRONT_PROXY_ARGS
