Summary:        Virtualization API library that supports KVM, QEMU, Xen, ESX etc
Name:           libvirt
Version:        7.3.0
Release:        1%{?dist}
License:        LGPL
URL:            http://libvirt.org/
Source0:        http://libvirt.org/sources/%{name}-%{version}.tar.xz
%define sha1    libvirt=13e14fde2e5477c9e771b3e06571bc652886fa12
Group:          Virtualization/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon

BuildRequires:  audit-devel
BuildRequires:  cyrus-sasl
BuildRequires:  curl-devel
BuildRequires:  c-ares-devel
BuildRequires:  device-mapper-devel
BuildRequires:  e2fsprogs-devel
BuildRequires:  gnutls-devel
BuildRequires:  libcap-ng-devel
BuildRequires:  libnl-devel
BuildRequires:  libselinux-devel
BuildRequires:  libssh2-devel
BuildRequires:  libtirpc-devel
BuildRequires:  libpcap-devel
BuildRequires:  libxml2-devel
BuildRequires:  libxslt
BuildRequires:  meson
BuildRequires:  ninja-build
BuildRequires:  parted
BuildRequires:  python3-devel
BuildRequires:  python3-docutils
BuildRequires:  readline-devel
BuildRequires:  rpcsvc-proto
BuildRequires:  systemd-devel
BuildRequires:  wireshark-devel

Requires:       cyrus-sasl
Requires:       device-mapper
Requires:       e2fsprogs
Requires:       gnutls
Requires:       libcap-ng
Requires:       libnl
Requires:       libpcap
Requires:       libselinux
Requires:       libssh2
Requires:       libtirpc
Requires:       libxml2
Requires:       parted
Requires:       python3
Requires:       readline
Requires:       systemd

%description
Libvirt is collection of software that provides a convenient way to manage
virtual machines and other virtualization functionality, such as storage
and network interface management. These software pieces include an API library,
a daemon (libvirtd), and a command line utility (virsh). An primary goal of
libvirt is to provide a single way to manage multiple different virtualization
providers/hypervisors. For example, the command 'virsh list --all' can be used
to list the existing virtual machines for any supported hypervisor
(KVM, Xen, VMWare ESX, etc.) No need to learn the hypervisor specific tools.

%package devel
Summary:        libvirt devel
Group:          Development/Tools
Requires:       %{name} = %{version}-%{release}
Requires:       libtirpc-devel
%description devel
This contains development tools and libraries for libvirt.

%package docs
Summary:        libvirt docs
Group:          Development/Tools
%description docs
The contains libvirt package doc files.

%prep
%autosetup -p1

sed -i -e 's/rst2html5.py/rst2html53.py/g' meson.build
sed -i  '/rst2man/d' meson.build

%build
CONFIGURE_OPTS=(
    --prefix=%{_prefix} \
    -Dapparmor=disabled \
    -Daudit=enabled \
    -Dcapng=enabled \
    -Dcurl=enabled \
    -Ddocs=disabled \
    -Ddriver_bhyve=disabled \
    -Ddriver_esx=enabled \
    -Ddriver_interface=disabled \
    -Ddriver_libvirtd=enabled \
    -Ddriver_network=enabled \
    -Ddriver_vmware=enabled \
    -Ddriver_vz=disabled \
    -Ddtrace=disabled \
    -Dfirewalld=disabled \
    -Dinit_script=systemd \
    -Dlibnl=enabled \
    -Dlibpcap=enabled \
    -Dnss=disabled \
    -Dpm_utils=disabled \
    -Dpolkit=enabled \
    -Dremote_default_mode=legacy \
    -Drpath=disabled \
    -Dselinux=enabled \
    -Dstorage_fs=enabled \
    -Dudev=disabled \
    )

export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8

meson build ${CONFIGURE_OPTS[@]}
ninja -C build

%install
export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8
DESTDIR=%{buildroot} ninja -C build install

find %{buildroot} -name '*.la' -delete

%check
ninja -C build test

%files
%defattr(-,root,root)
%{_bindir}/*
%{_sbindir}/*

%{_datadir}/augeas/*
%{_datadir}/libvirt/cpu_map/*
%{_datadir}/polkit-1/*

%{_libdir}/libvirt*.so.*
%{_libdir}/libvirt/connection-driver/*
%{_libdir}/libvirt/lock-driver/lockd.so
%{_libdir}/libvirt/storage-backend/*
%{_libdir}/libvirt/storage-file/libvirt_storage_file_fs.so
%{_libdir}/sysctl.d/60-libvirtd.conf
%{_libdir}/systemd/system/*
%{_libdir}/wireshark/plugins/3.4/epan/libvirt.so

%{_libexecdir}/libvirt*
%{_libexecdir}/virt-login-shell-helper

%{_sysconfdir}/libvirt/nwfilter/
%{_sysconfdir}/libvirt/qemu/networks/autostart/default.xml
%{_sysconfdir}/libvirt/qemu/networks/default.xml
%{_sysconfdir}/logrotate.d/*
%{_sysconfdir}/sysconfig/*

%config(noreplace)%{_sysconfdir}/libvirt/*.conf
%config(noreplace)%{_sysconfdir}/sasl2/libvirt.conf

%files devel
%{_includedir}/libvirt/*
%{_libdir}/libvirt*.so
%{_libdir}/pkgconfig/libvirt*

%files docs
%{_datadir}/doc/libvirt/*
%{_datadir}/locale/*
%{_datadir}/libvirt/test-screenshot.png

%changelog
*   Mon May 03 2021 Gerrit Photon <photon-checkins@vmware.com> 7.3.0-1
-   Automatic Version Bump
*   Tue Apr 13 2021 Gerrit Photon <photon-checkins@vmware.com> 7.2.0-1
-   Automatic Version Bump
*   Fri Mar 19 2021 Susat Sahani <ssahani@vmware.com> 7.1.0-1
-   Bump up version
*   Mon Aug 19 2020 Harinadh Dommaraju <hdommaraju@vmware.com> 4.7.0-4
-   fix CVE-2019-10166, CVE-2019-10167, CVE-2019-10168,
-   CVE-2019-3840,CVE-2019-20485,CVE-2020-10703
*   Tue Jun 23 2020 Tapas Kundu <tkundu@vmware.com> 4.7.0-3
-   Build with python3
-   Mass removal python2
*   Tue Sep 25 2018 Alexey Makhalov <amakhalov@vmware.com> 4.7.0-2
-   Use libtirpc
*   Wed Sep 12 2018 Keerthana K <keerthanak@vmware.com> 4.7.0-1
-   Update to version 4.7.0
*   Thu Dec 07 2017 Xiaolin Li <xiaolinl@vmware.com> 3.2.0-4
-   Move so files in folder connection-driver and lock-driver to main package.
*   Mon Dec 04 2017 Xiaolin Li <xiaolinl@vmware.com> 3.2.0-3
-   Fix CVE-2017-1000256
*   Wed Aug 23 2017 Rui Gu <ruig@vmware.com> 3.2.0-2
-   Fix missing deps in devel package
*   Thu Apr 06 2017 Kumar Kaushik <kaushikk@vmware.com> 3.2.0-1
-   Upgrading version to 3.2.0
*   Fri Feb 03 2017 Vinay Kulkarni <kulkarniv@vmware.com> 3.0.0-1
-   Initial version of libvirt package for Photon.
