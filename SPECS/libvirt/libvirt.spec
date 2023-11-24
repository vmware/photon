Summary:        Virtualization API library that supports KVM, QEMU, Xen, ESX etc
Name:           libvirt
Version:        8.10.0
Release:        4%{?dist}
License:        LGPL
URL:            http://libvirt.org
Group:          Virtualization/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: http://libvirt.org/sources/%{name}-%{version}.tar.xz
%define sha512 %{name}=1d4006e909e185a89f9163e6d2309841f4086da65b9165c42eb512e2f6ae964749eeb72f74e86476768a09061e2e311cfcc31f4024b4ecbaba04cd3f5f5d849d

BuildRequires:  audit-devel
BuildRequires:  cyrus-sasl-devel
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
BuildRequires:  libxslt-devel
BuildRequires:  lvm2
BuildRequires:  meson
BuildRequires:  ninja-build
BuildRequires:  parted-devel
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
Requires:       lvm2
Requires:       parted
Requires:       python3
Requires:       readline
Requires:       systemd
Requires:       %{name}-docs = %{version}-%{release}

%description
Libvirt is collection of software that provides a convenient way to manage
virtual machines and other virtualization functionality, such as storage
and network interface management. These software pieces include an API library,
a daemon (libvirtd), and a command line utility (virsh). An primary goal of
libvirt is to provide a single way to manage multiple different virtualization
providers/hypervisors. For example, the command 'virsh list --all' can be used
to list the existing virtual machines for any supported hypervisor
(KVM, Xen, VMWare ESX, etc.) No need to learn the hypervisor specific tools.

%package        devel
Summary:        libvirt devel
Group:          Development/Tools
Requires:       %{name} = %{version}-%{release}
Requires:       libtirpc-devel

%description    devel
This contains development tools and libraries for libvirt.

%package        docs
Summary:        libvirt docs
Group:          Development/Tools
Conflicts:      %{name} < 8.10.0-3

%description    docs
The contains libvirt package doc files.

%prep
%autosetup -p1

sed -i '/rst2man/d' meson.build

%build
CONFIGURE_OPTS=(
    -Dapparmor=disabled \
    -Dapparmor_profiles=disabled \
    -Dsecdriver_apparmor=disabled \
    -Dbash_completion=disabled \
    -Daudit=enabled \
    -Dcapng=enabled \
    -Dcurl=enabled \
    -Ddocs=disabled \
    -Ddriver_bhyve=disabled \
    -Ddriver_esx=enabled \
    -Ddriver_interface=disabled \
    -Ddriver_libvirtd=enabled \
    -Ddriver_hyperv=disabled \
    -Ddriver_ch=disabled \
    -Ddriver_qemu=disabled \
    -Ddriver_libxl=disabled \
    -Ddriver_network=enabled \
    -Ddriver_vmware=enabled \
    -Ddriver_vz=disabled \
    -Ddtrace=disabled \
    -Dfuse=disabled \
    -Dfirewalld=disabled \
    -Dfirewalld_zone=disabled \
    -Dglusterfs=disabled \
    -Dinit_script=systemd \
    -Dlibnl=enabled \
    -Dlibpcap=enabled \
    -Dlibssh=disabled \
    -Dnss=disabled \
    -Dnumactl=disabled \
    -Dnumad=disabled \
    -Dsasl=enabled \
    -Dnetcf=disabled \
    -Dnumactl=disabled \
    -Dopenwsman=disabled \
    -Dpciaccess=disabled \
    -Dsanlock=disabled \
    -Dyajl=disabled \
    -Dpm_utils=disabled \
    -Dpolkit=enabled \
    -Dremote_default_mode=legacy \
    -Drpath=disabled \
    -Dpciaccess=disabled \
    -Dselinux=enabled \
    -Dstorage_iscsi=disabled \
    -Dstorage_iscsi_direct=disabled \
    -Dlibiscsi=disabled \
    -Dstorage_gluster=disabled \
    -Dstorage_rbd=disabled \
    -Dstorage_zfs=disabled \
    -Dlibiscsi=disabled \
    -Dstorage_fs=enabled \
    -Dyajl=disabled \
    -Dudev=disabled \
    -Dwireshark_dissector=disabled \
    -Dattr=disabled \
    )

%meson "${CONFIGURE_OPTS[@]}"
%meson_build

%install
%meson_install

%if 0%{?with_check}
%check
%meson_test
%endif

%clean
rm -rf %{buildroot}/*

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_bindir}/*
%{_sbindir}/*
%{_libdir}/%{name}*.so.*
%{_libdir}/%{name}/connection-driver/*
%{_libdir}/%{name}/lock-driver/lockd.so
%{_libdir}/%{name}/storage-backend/*
%{_libdir}/%{name}/storage-file/libvirt_storage_file_fs.so
%{_libdir}/sysctl.d/60-libvirtd.conf
%{_unitdir}/*
%{_libexecdir}/%{name}*
%{_libexecdir}/virt-login-shell-helper
%{_sysconfdir}/%{name}/nwfilter/
%{_sysconfdir}/%{name}/qemu/networks/autostart/default.xml
%{_sysconfdir}/%{name}/qemu/networks/default.xml
%{_sysconfdir}/logrotate.d/*

%config(noreplace)%{_sysconfdir}/%{name}/*.conf
%config(noreplace)%{_sysconfdir}/sasl2/%{name}.conf

%files devel
%defattr(-,root,root)
%{_includedir}/%{name}/*
%{_libdir}/%{name}*.so
%{_libdir}/pkgconfig/%{name}*

%files docs
%defattr(-,root,root)
%{_docdir}/%{name}/*
%{_datadir}/locale/*
%{_datadir}/%{name}/test-screenshot.png
%{_datadir}/%{name}/schemas/*.rng
%{_datadir}/augeas/*
%{_datadir}/%{name}/cpu_map/*
%{_datadir}/polkit-1/*

%changelog
* Fri Nov 24 2023 Shreenidhi Shedi <sshedi@vmware.com> 8.10.0-4
- Bump version as a part of gnutls upgrade
* Thu Jun 08 2023 Shreenidhi Shedi <sshedi@vmware.com> 8.10.0-3
- Move doc files to docs sub package
* Wed Apr 19 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 8.10.0-2
- Bump version as a part of libxml2 upgrade
* Sat Jan 07 2023 Susant Sahani <ssahani@vmware.com> 8.10.0-1
- Version Bump
* Tue Dec 20 2022 Guruswamy Basavaiah <bguruswamy@vmware.com> 8.8.0-4
- Bump release as a part of readline upgrade
* Tue Dec 06 2022 Prashant S Chauhan <psinghchauha@vmware.com> 8.8.0-3
- Update release to compile with python 3.11
* Sun Nov 13 2022 Shreenidhi Shedi <sshedi@vmware.com> 8.8.0-2
- Bump version as a part of libtirpc upgrade
* Thu Nov 03 2022 Nitesh Kumar <kunitesh@vmware.com> 8.8.0-1
- Version upgrade to v8.8.0
* Fri Oct 07 2022 Shreenidhi Shedi <sshedi@vmware.com> 8.2.0-4
- Bump version as a part of libxslt upgrade
* Tue Aug 30 2022 Shreenidhi Shedi <sshedi@vmware.com> 8.2.0-3
- Bump version as a part of gnutls upgrade
* Thu Jun 16 2022 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 8.2.0-2
- Bump version as a part of libxslt upgrade
* Mon Apr 18 2022 Gerrit Photon <photon-checkins@vmware.com> 8.2.0-1
- Automatic Version Bump
* Thu Mar 17 2022 Nitesh Kumar <kunitesh@vmware.com> 7.10.0-2
- Version Bump up to consume original python files from python-docutils
* Thu Dec 02 2021 Susant Sahani <ssahani@vmware.com> 7.10.0-1
- Version Bump
* Wed Nov 17 2021 Nitesh Kumar <kunitesh@vmware.com> 7.5.0-2
- Release bump up to use libxml2 2.9.12-1.
* Wed Jul 14 2021 Susant Sahani <ssahani@vmware.com> 7.5.0-1
- Version Bump and switch to meson
* Mon May 03 2021 Gerrit Photon <photon-checkins@vmware.com> 7.3.0-1
- Automatic Version Bump
* Tue Apr 13 2021 Gerrit Photon <photon-checkins@vmware.com> 7.2.0-1
- Automatic Version Bump
* Fri Mar 19 2021 Susat Sahani <ssahani@vmware.com> 7.1.0-1
- Bump up version
* Wed Aug 19 2020 Harinadh Dommaraju <hdommaraju@vmware.com> 4.7.0-4
- fix CVE-2019-10166, CVE-2019-10167, CVE-2019-10168,
- CVE-2019-3840,CVE-2019-20485,CVE-2020-10703
* Tue Jun 23 2020 Tapas Kundu <tkundu@vmware.com> 4.7.0-3
- Build with python3
- Mass removal python2
* Tue Sep 25 2018 Alexey Makhalov <amakhalov@vmware.com> 4.7.0-2
- Use libtirpc
* Wed Sep 12 2018 Keerthana K <keerthanak@vmware.com> 4.7.0-1
- Update to version 4.7.0
* Thu Dec 07 2017 Xiaolin Li <xiaolinl@vmware.com> 3.2.0-4
- Move so files in folder connection-driver and lock-driver to main package.
* Mon Dec 04 2017 Xiaolin Li <xiaolinl@vmware.com> 3.2.0-3
- Fix CVE-2017-1000256
* Wed Aug 23 2017 Rui Gu <ruig@vmware.com> 3.2.0-2
- Fix missing deps in devel package
* Thu Apr 06 2017 Kumar Kaushik <kaushikk@vmware.com> 3.2.0-1
- Upgrading version to 3.2.0
* Fri Feb 03 2017 Vinay Kulkarni <kulkarniv@vmware.com> 3.0.0-1
- Initial version of libvirt package for Photon.
