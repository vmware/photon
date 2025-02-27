FROM photon:5.0
RUN tdnf install -y \
         python3 \
         python3-pip \
         redis \
         rpm \
         rpm-build \
         build-essential \
         ruby-devel \
         dwarves-devel
RUN pip3 install \
         scancode-toolkit==32.2.1 \
         requests \
         pyyaml \
         redis \
         argparse
RUN mkdir -p /root/photon-lic-tool
COPY ./ /root/photon-lic-tool
RUN python3 /root/photon-lic-tool/photon-lic-tool.py lic-db --trim
