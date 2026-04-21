%global build_if %{photon_subrelease} >= 92

%global debug_package %{nil}

%ifarch x86_64
%global targetArch aarch64
%endif

%ifarch aarch64
%global targetArch x86_64
%endif

Summary:        QEMU utilities and emulators
Name:           qemu
Version:        10.2.2
Release:        1%{?dist}
URL:            https://www.qemu.org
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        https://download.qemu.org/qemu-%{version}.tar.xz
Source1:        license.txt
%include %{SOURCE1}

Source2:        qemu-%{targetArch}-static.conf

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  glib-devel
BuildRequires:  pixman-devel
BuildRequires:  ninja-build
BuildRequires:  ninja-build
BuildRequires:  zstd-devel
BuildRequires:  zlib-devel
BuildRequires:  libselinux-devel

Requires:       %{name}-img = %{version}-%{release}
Requires:       %{name}-user-static-%{targetArch} = %{version}-%{release}

%description
QEMU utilities and emulators

%package img
Summary:        QEMU disk image utility
Requires:       libselinux
Requires:       zstd-libs
Requires:       zlib

%description img
Qemu-img is the tool used to create, manage, convert, shrink etc. the disk images of virtual machines.

%package user-static-%{targetArch}
Summary:            Statically linked user mode emulation for %{targetArch}
Requires(post):     systemd
Requires(postun):   systemd

%description user-static-%{targetArch}
Statically linked user mode emulation for %{targetArch}

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
        --disable-bochs \\\
        --disable-brlapi \\\
        --disable-bsd-user \\\
        --disable-bzip2 \\\
        --disable-guest-agent-msi \\\
        --disable-attr \\\
        --disable-auth-pam \\\
        --disable-cap-ng \\\
        --disable-capstone \\\
        --disable-cloop \\\
        --disable-curl \\\
        --disable-curses \\\
        --disable-debug-info \\\
        --disable-debug-mutex \\\
        --disable-lzfse \\\
        --disable-lzo \\\
        --disable-membarrier \\\
        --disable-modules \\\
        --disable-numa \\\
        --disable-opengl \\\
        --disable-debug-tcg \\\
        --disable-dmg \\\
        --disable-fdt \\\
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

mkdir -p build && pushd build
# Disabling everything except tools
sh ../configure \
        --prefix="%{_prefix}" \
        --libdir="%{_libdir}" \
        --datadir="%{_datadir}" \
        --sysconfdir="%{_sysconfdir}" \
        --localstatedir="%{_var}" \
        --libexecdir="%{_libexecdir}" \
        %{disable_all} \
        --disable-system \
        --disable-linux-user \
        --disable-user \
        --enable-tools

%make_build

popd

mkdir -p build-user-static && pushd build-user-static

sh ../configure \
        --prefix="%{_prefix}" \
        --libdir="%{_libdir}" \
        --datadir="%{_datadir}" \
        --sysconfdir="%{_sysconfdir}" \
        --localstatedir="%{_var}" \
        --libexecdir="%{_libexecdir}" \
        %{disable_all} \
        --target-list=%{targetArch}-linux-user \
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

mv %{buildroot}%{_bindir}/qemu-%{targetArch} %{buildroot}%{_bindir}/qemu-%{targetArch}-static

%global binfmt_dir %{buildroot}%{_libdir}/binfmt.d
mkdir -p %{binfmt_dir}

cp %{SOURCE2} %{binfmt_dir}

popd

# Remove unnessary files
find %{buildroot} \( -name '*.png' \
                     -name '*.bmp' \
                     -name '*.svg' \
                     -name 'qemu.desktop' \) \
                     -delete

rm -r %{buildroot}%{_datadir}/qemu/keymaps

%if 0%{?with_check}
%check
make %{?_smp_mflags} check
%endif

%post user-static-%{targetArch}
/bin/systemctl --system try-restart systemd-binfmt.service &>/dev/null || :

%postun user-static-%{targetArch}
/bin/systemctl --system try-restart systemd-binfmt.service &>/dev/null || :

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
%{_bindir}/qemu-vmsr-helper
%{_datadir}/qemu
%{_libexecdir}/qemu-bridge-helper

%files user-static-%{targetArch}
%defattr(-,root,root)
%{_bindir}/qemu-%{targetArch}-static
%{_libdir}/binfmt.d/qemu-%{targetArch}-static.conf

%changelog
* Tue Apr 14 2026 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 10.2.2-1
- Upgrade to 10.2.2
* Wed Feb 18 2026 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 7.2.0-8
- Bump up release as part of python3 upgrade
* Tue Dec 23 2025 Oliver Kurth <oliver.kurth@broadcom.com> 7.2.0-7
- fix aarch64 build
* Tue Dec 16 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 7.2.0-6
- Fix BuildRequires and Requires
- Use targetArch macro remove duplicate instructions
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
