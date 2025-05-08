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
         requests==2.32.3 \
         charset-normalizer==3.4.2 \
         lxml==5.4.0 \
         markupsafe==3.0.2 \
         pyyaml==6.0.2 \
         redis==6.0.0 \
         argparse==1.4.0
RUN mkdir -p /root/photon-lic-tool
COPY ./ /root/photon-lic-tool
RUN python3 /root/photon-lic-tool/photon-lic-tool.py lic-db --trim
