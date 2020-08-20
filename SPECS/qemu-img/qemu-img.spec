%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%global debug_package %{nil}
Summary:        QEMU disk image utility
Name:           qemu-img
Version:        5.1.0
Release:        1%{?dist}
License:        GNU GPLv2
URL:            https://www.qemu.org
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://download.qemu.org/qemu-%{version}.tar.xz
%define sha1    qemu=8c70ce2b65349e9b42bd20c9dec2c90f8e7b960a
BuildRequires:  python3-devel
BuildRequires:  glib-devel
BuildRequires:  pixman-devel

%description
Qemu-img is the tool used to create, manage, convert shrink etc. the disk images of virtual machines.

%prep
%setup -q -n qemu-%{version}

%build
# Do not build QEMU's ivshmem
sed -i 's#ivshmem=yes#ivshmem=no#g' configure
mkdir build
cd build
# Disabling everything except tools
../configure \
        --disable-system \
        --disable-linux-user \
        --disable-user \
        --disable-gcrypt \
        --disable-glusterfs \
        --disable-gnutls \
        --disable-gtk \
        --disable-guest-agent \
        --disable-blobs \
        --disable-bochs \
        --disable-brlapi \
        --disable-bsd-user \
        --disable-bzip2 \
        --disable-guest-agent-msi \
        --disable-attr \
        --disable-auth-pam \
        --disable-avx2 \
        --disable-cap-ng \
        --disable-capstone \
        --disable-cloop \
        --disable-curl \
        --disable-curses \
        --disable-debug-info \
        --disable-debug-mutex \
        --disable-live-block-migration \
        --disable-lzfse \
        --disable-lzo \
        --disable-membarrier \
        --disable-modules \
        --disable-numa \
        --disable-opengl \
        --disable-debug-tcg \
        --disable-dmg \
        --disable-fdt \
        --disable-hax \
        --disable-hvf \
        --disable-iconv \
        --disable-jemalloc \
        --disable-kvm \
        --disable-cocoa \
        --disable-coroutine-pool \
        --disable-crypto-afalg \
        --disable-libiscsi \
        --disable-libnfs \
        --disable-libpmem \
        --disable-mpath \
        --disable-netmap \
        --disable-xfsctl \
        --disable-sdl-image \
        --disable-seccomp \
        --disable-sheepdog \
        --disable-slirp \
        --disable-vhost-vsock \
        --disable-virglrenderer \
        --disable-virtfs \
        --disable-vnc \
        --disable-nettle \
        --disable-libssh \
        --disable-libusb \
        --disable-libxml2 \
        --disable-linux-aio \
        --disable-parallels \
        --disable-pvrdma \
        --disable-qcow1 \
        --disable-qed \
        --disable-spice \
        --disable-tcg \
        --disable-tcmalloc \
        --disable-vhost-kernel \
        --disable-vhost-net \
        --disable-qom-cast-debug \
        --disable-rbd \
        --disable-rdma \
        --disable-replication \
        --disable-sdl \
        --disable-vte \
        --disable-vvfat \
        --disable-whpx \
        --disable-xen \
        --disable-xen-pci-passthrough \
        --disable-smartcard \
        --disable-snappy \
        --disable-sparse \
        --disable-tpm \
        --disable-usb-redir \
        --disable-vde \
        --disable-vdi \
        --disable-vhost-crypto \
        --disable-vhost-scsi \
        --disable-vhost-user \
        --disable-vnc-jpeg \
        --disable-vnc-png \
        --disable-vnc-sasl \
        --disable-docs \
        --audio-drv-list= \
        --without-default-devices \
        --enable-tools
make %{?_smp_mflags}

%install
cd build
make DESTDIR=%{buildroot} install
# Removed unnessary files
find %{buildroot} -name '*.png' -delete
find %{buildroot} -name '*.bmp' -delete
find %{buildroot} -name '*.svg' -delete
find %{buildroot} -name 'qemu.desktop' -delete

%check
make %{?_smp_mflags} check

%files
%defattr(-,root,root)
/usr/local/bin/qemu-edid
/usr/local/bin/qemu-img
/usr/local/bin/qemu-io
/usr/local/bin/qemu-nbd
/usr/local/bin/qemu-storage-daemon
/usr/local/share/qemu

%changelog
*   Wed Aug 19 2020 Gerrit Photon <photon-checkins@vmware.com> 5.1.0-1
-   Automatic Version Bump
*   Mon Mar 09 2020 Ankit Jain <ankitja@vmware.com> 4.2.0-1
-   Initial build.  First version
