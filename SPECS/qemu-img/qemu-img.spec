%global debug_package %{nil}

Summary:        QEMU disk image utility
Name:           qemu-img
Version:        7.1.0
Release:        1%{?dist}
License:        GNU GPLv2
URL:            https://www.qemu.org
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        https://download.qemu.org/qemu-%{version}.tar.xz
%define sha512  qemu=c60c5ff8ec99b7552e485768908920658fdd8035ff7a6fa370fb6881957dc8b7e5f18ff1a8f49bd6aa22909ede2a7c084986d8244f12074ccd33ebe40a0c411f

BuildRequires:  python3-devel
BuildRequires:  glib-devel
BuildRequires:  pixman-devel
BuildRequires:  ninja-build

%description
Qemu-img is the tool used to create, manage, convert shrink etc. the disk images of virtual machines.

%prep
%autosetup -p1 -n qemu-%{version}

%build
# Do not build QEMU's ivshmem
sed -i 's#ivshmem=yes#ivshmem=no#g' configure
mkdir build && cd build
# Disabling everything except tools
sh ../configure \
        --prefix="%{_prefix}" \
        --libdir="%{_libdir}" \
        --datadir="%{_datadir}" \
        --sysconfdir="%{_sysconfdir}" \
        --localstatedir="%{_localstatedir}" \
        --libexecdir="%{_libexecdir}" \
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
        --disable-kvm \
        --disable-cocoa \
        --disable-coroutine-pool \
        --disable-crypto-afalg \
        --disable-libiscsi \
        --disable-libnfs \
        --disable-libpmem \
        --disable-mpath \
        --disable-netmap \
        --disable-sdl-image \
        --disable-seccomp \
        --disable-slirp \
        --disable-virglrenderer \
        --disable-virtfs \
        --disable-vnc \
        --disable-nettle \
        --disable-libssh \
        --disable-libusb \
        --disable-linux-aio \
        --disable-parallels \
        --disable-pvrdma \
        --disable-qcow1 \
        --disable-qed \
        --disable-spice \
        --disable-tcg \
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
        --disable-vhost-user \
        --disable-vnc-jpeg \
        --disable-vnc-sasl \
        --disable-docs \
        --audio-drv-list= \
        --without-default-devices \
        --enable-tools

make %{?_smp_mflags}

%install
cd build
make %{?_smp_mflags} DESTDIR=%{buildroot} install

# Remove unnessary files
find %{buildroot} \( -name '*.png' \
                     -name '*.bmp' \
                     -name '*.svg' \
                     -name 'qemu.desktop' \) \
                     -delete

%if 0%{?with_check}
%check
make %{?_smp_mflags} check
%endif

%files
%defattr(-,root,root)
%{_bindir}/qemu-edid
%{_bindir}/qemu-img
%{_bindir}/qemu-io
%{_bindir}/qemu-nbd
%{_bindir}/qemu-storage-daemon
%{_bindir}/qemu-pr-helper
%{_datadir}/qemu
%{_libexecdir}/qemu-bridge-helper

%changelog
* Fri Oct 28 2022 Gerrit Photon <photon-checkins@vmware.com> 7.1.0-1
- Automatic Version Bump
* Sun Jun 12 2022 Shreenidhi Shedi <sshedi@vmware.com> 7.0.0-2
- Fix file packaging & spec improvements
* Tue Apr 19 2022 Gerrit Photon <photon-checkins@vmware.com> 7.0.0-1
- Automatic Version Bump
* Tue Apr 13 2021 Gerrit Photon <photon-checkins@vmware.com> 6.0.0-1
- Automatic Version Bump
* Wed Aug 19 2020 Gerrit Photon <photon-checkins@vmware.com> 5.1.0-1
- Automatic Version Bump
* Mon Mar 09 2020 Ankit Jain <ankitja@vmware.com> 4.2.0-1
- Initial build.  First version
