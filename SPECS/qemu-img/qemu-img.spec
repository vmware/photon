%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
Summary:    QEMU disk image utility
Name:       qemu-img
Version:    4.2.0
Release:    1%{?dist}
License:    GNU GPLv2
URL:        https://www.qemu.org
Group:      Development/Tools
Vendor:     VMware, Inc.
Distribution:   Photon
Source0:    https://download.qemu.org/qemu-%{version}.tar.xz
%define sha1 qemu=b27aa828a8457bd8551ae3c81b80cc365e1f6bfe
BuildRequires:  python3-devel
BuildRequires:  glib-devel
BuildRequires:  pixman-devel

%global debug_package %{nil}

%description
Qemu-img is the tool used to create, manage, convert shrink etc. the disk images of virtual machines.

%prep
%setup -q -n qemu-%{version}
# Do not build QEMU's ivshmem 
sed -i 's#ivshmem=yes#ivshmem=no#g' configure
mkdir build

%build
pushd build
# Disabling everything except tools
../configure --prefix=%{_prefix} --python=%{_bindir}/python3 \
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
        --disable-pie \
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
        --disable-vxhs \
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
popd

%install
pushd build
make DESTDIR=%{buildroot} install
# Removed unnessary files
find %{buildroot}/%{_datadir} -name '*.png' -delete
find %{buildroot}/%{_datadir} -name '*.bmp' -delete
find %{buildroot}/%{_datadir} -name '*.svg' -delete
rm -rf %{buildroot}/%{_datadir}/applications/qemu.desktop
popd

%check
make %{?_smp_mflags} check

%files
%defattr(-,root,root)
%{_bindir}/qemu-edid
%{_bindir}/qemu-img
%{_bindir}/qemu-io
%{_bindir}/qemu-nbd
%{_datadir}/qemu

%changelog
*   Mon Mar 09 2020 Ankit Jain <ankitja@vmware.com> 4.2.0-1
-   Initial build.  First version
