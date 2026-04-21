FROM photon:5.0

ARG BASE_URL
ENV URL=${BASE_URL}

# Set LANG to ensure extractcode behaves consistently
# Otherwise, file paths with tricky/unencodeable characters
# may turn out differently depending on encoding
ENV LANG="en_US.UTF-8"

RUN REPO_FILE=/etc/yum.repos.d/photon-updates.repo && \
    if [ -n "$URL" ]; then \
        sed -i "s|^baseurl=.*|baseurl=${URL}|" "$REPO_FILE"; \
    fi && \
    cat "$REPO_FILE"

RUN tdnf install --nogpgcheck -y --refresh \
         python3-devel \
         python3-pip \
         docker-py3 \
         redis \
         rpm-build \
         build-essential \
         ruby-devel \
         icu-devel \
         dwarves-devel \
         unzip \
    && rm -r /var/cache/tdnf

RUN pip3 install \
    binaryornot==0.4.4 \
    scancode-toolkit==32.4.1 \
    requests==2.32.5 \
    charset-normalizer==3.4.4 \
    lxml==6.0.2 \
    markupsafe==3.0.3 \
    pyyaml==6.0.3 \
    redis==7.1.0 \
    argparse==1.4.0\
    click==8.3.1 \
    ruamel.yaml==0.18.16 \
   && pip3 cache purge

ENV LIC_TOOL_DIR=/root/photon-lic-tool

COPY ./ ${LIC_TOOL_DIR}
RUN python3 "${LIC_TOOL_DIR}/photon-lic-tool.py" lic-db --trim \
    && rm -r "${LIC_TOOL_DIR}"
