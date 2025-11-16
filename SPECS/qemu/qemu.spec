%global debug_package %{nil}

Summary:        QEMU utilities and emulators
Name:           qemu
Version:        7.2.0
Release:        5%{?dist}
URL:            https://www.qemu.org
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        https://download.qemu.org/qemu-%{version}.tar.xz
Source1:        license.txt
%include %{SOURCE1}
Source2:        qemu-aarch64-static.conf
Source3:        qemu-x86_64-static.conf

BuildRequires:  python3-devel
BuildRequires:  glib-devel
BuildRequires:  pixman-devel
BuildRequires:  ninja-build

Requires:       %{name}-img = %{version}-%{release}
%ifarch x86_64
Requires:       %{name}-user-static-aarch64 = %{version}-%{release}
%endif
%ifarch aarch64
Requires:       %{name}-user-static-x86_64 = %{version}-%{release}
%endif

%description
QEMU utilities and emulators

%package img
Summary: QEMU disk image utility

%description img
Qemu-img is the tool used to create, manage, convert, shrink etc. the disk images of virtual machines.

%ifarch x86_64
%package user-static-aarch64
Summary: Statically linked user mode emulation for aarch64

%description user-static-aarch64
Statically linked user mode emulation for aarch64
%endif

%ifarch aarch64
%package user-static-x86_64
Summary: Statically linked user mode emulation for x86_64

%description user-static-x86_64
Statically linked user mode emulation for x86_64
%endif

%prep
%autosetup -p1 %{version}

# Remove files to handle unintended copyright inclusions
rm roms/u-boot/tools/logos/u-boot_logo.svg

%build
%define disable_all \\\
        --disable-gcrypt \\\
        --disable-glusterfs \\\
        --disable-gnutls \\\
        --disable-gtk \\\
        --disable-guest-agent \\\
        --disable-blobs \\\
        --disable-bochs \\\
        --disable-brlapi \\\
        --disable-bsd-user \\\
        --disable-bzip2 \\\
        --disable-guest-agent-msi \\\
        --disable-attr \\\
        --disable-auth-pam \\\
        --disable-avx2 \\\
        --disable-cap-ng \\\
        --disable-capstone \\\
        --disable-cloop \\\
        --disable-curl \\\
        --disable-curses \\\
        --disable-debug-info \\\
        --disable-debug-mutex \\\
        --disable-live-block-migration \\\
        --disable-lzfse \\\
        --disable-lzo \\\
        --disable-membarrier \\\
        --disable-modules \\\
        --disable-numa \\\
        --disable-opengl \\\
        --disable-debug-tcg \\\
        --disable-dmg \\\
        --disable-fdt \\\
        --disable-hax \\\
        --disable-hvf \\\
        --disable-iconv \\\
        --disable-kvm \\\
        --disable-cocoa \\\
        --disable-coroutine-pool \\\
        --disable-crypto-afalg \\\
        --disable-libiscsi \\\
        --disable-libnfs \\\
        --disable-libpmem \\\
        --disable-mpath \\\
        --disable-netmap \\\
        --disable-sdl-image \\\
        --disable-seccomp \\\
        --disable-slirp \\\
        --disable-virglrenderer \\\
        --disable-virtfs \\\
        --disable-vnc \\\
        --disable-nettle \\\
        --disable-libssh \\\
        --disable-libusb \\\
        --disable-linux-aio \\\
        --disable-parallels \\\
        --disable-pvrdma \\\
        --disable-qcow1 \\\
        --disable-qed \\\
        --disable-spice \\\
        --disable-tcg \\\
        --disable-vhost-kernel \\\
        --disable-vhost-net \\\
        --disable-qom-cast-debug \\\
        --disable-rbd \\\
        --disable-rdma \\\
        --disable-replication \\\
        --disable-sdl \\\
        --disable-vte \\\
        --disable-vvfat \\\
        --disable-whpx \\\
        --disable-xen \\\
        --disable-xen-pci-passthrough \\\
        --disable-smartcard \\\
        --disable-snappy \\\
        --disable-sparse \\\
        --disable-tpm \\\
        --disable-usb-redir \\\
        --disable-vde \\\
        --disable-vdi \\\
        --disable-vhost-crypto \\\
        --disable-vhost-user \\\
        --disable-vnc-jpeg \\\
        --disable-vnc-sasl \\\
        --disable-docs \\\
        --audio-drv-list= \\\
        --without-default-devices

# Do not build QEMU's ivshmem
sed -i 's#ivshmem=yes#ivshmem=no#g' configure
mkdir build && pushd build
# Disabling everything except tools
sh ../configure \
        --prefix="%{_prefix}" \
        --libdir="%{_libdir}" \
        --datadir="%{_datadir}" \
        --sysconfdir="%{_sysconfdir}" \
        --localstatedir="%{_localstatedir}" \
        --libexecdir="%{_libexecdir}" \
        %{disable_all} \
        --disable-system \
        --disable-linux-user \
        --disable-user \
        --enable-tools

%make_build

popd

mkdir build-user-static && pushd build-user-static

sh ../configure \
        --prefix="%{_prefix}" \
        --libdir="%{_libdir}" \
        --datadir="%{_datadir}" \
        --sysconfdir="%{_sysconfdir}" \
        --localstatedir="%{_localstatedir}" \
        --libexecdir="%{_libexecdir}" \
        %{disable_all} \
%ifarch x86_64
        --target-list=aarch64-linux-user \
%endif
%ifarch aarch64
        --target-list=x86_64-linux-user \
%endif
        --enable-attr \
        --enable-linux-user \
        --enable-tcg \
        --static

%make_build

popd

%install
pushd build
%make_install
popd

pushd build-user-static
%make_install

%ifarch x86_64
mv %{buildroot}%{_bindir}/qemu-aarch64 %{buildroot}%{_bindir}/qemu-aarch64-static
%endif

%ifarch aarch64
mv %{buildroot}%{_bindir}/qemu-x86_64 %{buildroot}%{_bindir}/qemu-x86_64-static
%endif

%global binfmt_dir %{buildroot}%{_libdir}/binfmt.d
mkdir -p %{binfmt_dir}

cp %{SOURCE2} %{binfmt_dir}
cp %{SOURCE3} %{binfmt_dir}

%ifarch aarch64
rm %{binfmt_dir}/qemu-aarch64-static.conf
%endif

%ifarch x86_64
rm %{binfmt_dir}/qemu-x86_64-static.conf
%endif

popd

# Remove unnessary files
find %{buildroot} \( -name '*.png' \
                     -name '*.bmp' \
                     -name '*.svg' \
                     -name 'qemu.desktop' \) \
                     -delete
rm -rf %{buildroot}%{_datadir}/qemu/keymaps

%if 0%{?with_check}
%check
make %{?_smp_mflags} check
%endif

%ifarch x86_64
%post user-static-aarch64
/bin/systemctl --system try-restart systemd-binfmt.service &>/dev/null || :

%postun user-static-aarch64
/bin/systemctl --system try-restart systemd-binfmt.service &>/dev/null || :
%endif

%ifarch aarch64
%post user-static-x86_64
/bin/systemctl --system try-restart systemd-binfmt.service &>/dev/null || :

%postun user-static-x86_64
/bin/systemctl --system try-restart systemd-binfmt.service &>/dev/null || :
%endif

%files
%defattr(-,root,root)

%files img
%defattr(-,root,root)
%{_bindir}/qemu-edid
%{_bindir}/qemu-img
%{_bindir}/qemu-io
%{_bindir}/qemu-nbd
%{_bindir}/qemu-storage-daemon
%{_bindir}/qemu-pr-helper
%{_datadir}/qemu
%{_libexecdir}/qemu-bridge-helper

%ifarch x86_64
%files user-static-aarch64
%defattr(-,root,root)
%{_bindir}/qemu-aarch64-static
%{_libdir}/binfmt.d/qemu-aarch64-static.conf
%endif

%ifarch aarch64
%files user-static-x86_64
%defattr(-,root,root)
%{_bindir}/qemu-x86_64-static
%{_libdir}/binfmt.d/qemu-x86_64-static.conf
%endif

%changelog
* Fri Nov 21 2025 Oliver Kurth <oliver.kurth@broadcom.com> 7.2.0-5
- add qemu-user-static-* packages
* Tue Aug 12 2025 Bo Gan <bo.gan@broadcom.com> 7.2.0-4
- Cleanup and rescan licenses
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
