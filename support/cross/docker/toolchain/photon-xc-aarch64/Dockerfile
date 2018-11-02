FROM photon:3.0-20181030
MAINTAINER "Sriram Nambakam" <snambakam@vmware.com>
ENV container=docker
ENV PATH /opt/cross/bin:$PATH

COPY cross-aarch64-tools-1.0.0-4.ph2.x86_64.rpm /

RUN sed -i 's/^\(enabled=\).*/\10/' /etc/yum.repos.d/photon-extras.repo && \
    sed -i 's/^\(enabled=\).*/\10/' /etc/yum.repos.d/photon-updates.repo && \
    tdnf update -qy  tdnf  && \
    tdnf erase -qy toybox && \
    tdnf install -qy \
        autoconf-2.69 \
        automake-1.16.1 \
        libtool-2.4.6 \
        binutils-2.31.1 \
        bison-3.1 \
        bzip2-1.0.6 \
        cpio-2.12 \
        diffutils-3.6 \
        elfutils-libelf-devel-0.174 \
        elfutils-0.174 \
        elfutils-devel-0.174 \
        file-5.34 \
        findutils-4.6.0 \
        gawk-4.2.1 \
        gcc-7.3.0 \
        gettext-0.19.8.1 \
        glibc-devel-2.28 \
        glibc-iconv-2.28 \
        glibc-i18n-2.28 \
        glibc-lang-2.28 \
        gzip-1.9 \
        libgcc-7.3.0 \
        linux-api-headers-4.18.9 \
        make-4.2.1 \
        ncurses-6.1 \
        ncurses-devel-6.1 \
        ncurses-terminfo-6.1 \
        patch-2.7.6 \
        rpm-4.14.2 \
        rpm-build-4.14.2 \
        rpm-devel-4.14.2 \
        sed-4.5 \
        tar-1.30  \
        texinfo-6.5 \
        unzip-6.0 \
        vim-8.1.0388 \
        wget-1.19.5 \
        xz-5.2.4 \
        xz-devel-5.2.4 && \
    rpm -i cross-aarch64-tools-*.rpm && \
    rm -f cross-aarch64-tools-*.rpm
