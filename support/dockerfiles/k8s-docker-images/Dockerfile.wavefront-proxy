FROM k8s-base-image:3.0

# This script may automatically configure wavefront without prompting, based on
# these variables:
#  WAVEFRONT_URL           (required)
#  WAVEFRONT_TOKEN         (required)
#  JAVA_HEAP_USAGE         (default is 4G)
#  WAVEFRONT_HOSTNAME      (default is the docker containers hostname)
#  WAVEFRONT_USE_GRAPHITE  (default is false)

COPY [ "./stage-rpms-tdnf.conf", "./tmp/stage-rpms.repo", "/tmp/tdnf/" ]
RUN tdnf -c /tmp/tdnf/stage-rpms-tdnf.conf install -y openjre8 shadow --refresh
# Copy files
COPY [ "./tmp/wavefront-proxy/etc/wavefront/wavefront-proxy/log4j2-stdout.xml", \
       "./tmp/wavefront-proxy/etc/wavefront/wavefront-proxy/log4j2.xml", \
       "./tmp/wavefront-proxy/etc/wavefront/wavefront-proxy/preprocessor_rules.yaml",\
       "./tmp/wavefront-proxy/etc/wavefront/wavefront-proxy/wavefront.conf", \
       "/etc/wavefront/wavefront-proxy/" ]

COPY ./tmp/wavefront-proxy/lib/systemd/system/wavefront-proxy.service /lib/systemd/system/ 
COPY ./tmp/wavefront-proxy/opt/wavefront-push-agent.jar /opt/
COPY ./tmp/wavefront-proxy/opt/wavefront/wavefront-proxy/bin/autoconf-wavefront-proxy.sh /opt/wavefront/wavefront-proxy/bin/
COPY ./tmp/wavefront-proxy/opt/wavefront/wavefront-proxy/bin/run.sh /

# Configure agent
ENV DO_SERVICE_RESTART=false
RUN echo '\nephemeral=true' >> /etc/wavefront/wavefront-proxy/wavefront.conf
RUN echo '\nflushThreads=6' >> /etc/wavefront/wavefront-proxy/wavefront.conf

# Run the agent
EXPOSE 3878
EXPOSE 2878
EXPOSE 4242
ENV PATH=/opt/wavefront/wavefront-proxy/jre/bin:$PATH
ENV WAVEFRONT_USE_GRAPHITE=false
ENTRYPOINT ["/bin/bash", "/run.sh"]
