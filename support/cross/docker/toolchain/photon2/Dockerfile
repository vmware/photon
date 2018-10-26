FROM vmware/photon2:20180214
MAINTAINER "Sriram Nambakam" <snambakam@vmware.com>
ENV container=docker

RUN tdnf update -qy  tdnf  && \
    tdnf erase -qy toybox && \
    tdnf install -qy \
        binutils-2.31 \
        bison-3.0.4 \
        bzip2-1.0.6 \
        cpio-2.12 \
        diffutils-3.5 \
        elfutils-0.169 \
        file-5.30 \
        findutils-4.6.0 \
        gawk-4.1.4 \
        gcc-6.3.0 \
        glibc-devel-2.26 \
        gzip-1.8 \
        linux-api-headers-4.9.124 \
        make-4.2.1 \
        patch-2.7.5 \
        rpm-4.13.0.1 \
        rpm-build-4.13.0.1 \
        rpm-devel-4.13.0.1 \
        sed-4.4 \
        tar-1.29  \
        texinfo-6.3 \
        unzip-6.0 \
        vim-8.0.0533 \
        wget-1.19.1 \
        xz-5.2.3
