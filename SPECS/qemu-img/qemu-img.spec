%global debug_package %{nil}

Summary:        QEMU disk image utility
Name:           qemu-img
Version:        7.2.0
Release:        3%{?dist}
URL:            https://www.qemu.org
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        https://download.qemu.org/qemu-%{version}.tar.xz

Source1: license.txt
%include %{SOURCE1}

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

%make_build

%install
cd build
%make_install

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
* Wed Dec 11 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 7.2.0-3
- Release bump for SRP compliance
* Wed May 24 2023 Him Kalyan Bordoloi <bordoloih@vmware.com> 7.2.0-2
- Bump version as a part of pixman upgrade
* Sat Jan 07 2023 Susant Sahani <ssahani@vmware.com> 7.2.0-1
- Version Bump
* Tue Dec 06 2022 Prashant S Chauhan <psinghchauha@vmware.com> 7.1.0-2
- Update release to compile with python 3.11
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
- Initial build. First version
