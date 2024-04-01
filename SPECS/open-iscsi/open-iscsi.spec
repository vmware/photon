Summary:        iSCSI tools for Linux
Name:           open-iscsi
Version:        2.1.6
Release:        4%{?dist}
License:        GPLv2
URL:            https://github.com/open-iscsi/open-iscsi
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: %{name}-%{version}.tar.gz
%define sha512 open=4a32a76c1c32d7d1a01fe3a0f88ce9616a54323ec043757be73051eb41ebae8de90ce057acce72fb6fe07aa47e814c9bc6ee88b13fa7d7769ca10c5175974f1d

BuildRequires:  open-isns-devel
BuildRequires:  openssl-devel
BuildRequires:  kmod-devel
BuildRequires:  systemd-devel
BuildRequires:  util-linux-devel

Requires:       openssl-libs
Requires:       kmod
Requires:       systemd
Requires:       util-linux

%description
iSCSI tools for Linux

%package        devel
Summary:        Development Libraries for open-iscsi
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description    devel
Header files for doing development with open-iscsi

%prep
%autosetup -p1

%build
%make_build LIB_DIR=%{_libdir} sbindir=%{_sbindir}

%install
%make_install %{?_smp_mflags} \
        LIB_DIR=%{_libdir} sbindir=%{_sbindir} \
        install_systemd

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_sysconfdir}/iscsi/ifaces/iface.example
%config(noreplace) %{_sysconfdir}/iscsi/initiatorname.iscsi
%config(noreplace) %{_sysconfdir}/iscsi/iscsid.conf
%{_sbindir}/iscsi*
%{_unitdir}/*.service
%{_unitdir}/*.socket
%{_libdir}/libopeniscsiusr.so.*
%{_mandir}/man8/*.gz

%files devel
%defattr(-,root,root)
%{_includedir}/*.h
%{_libdir}/libopeniscsiusr.so
%{_libdir}/pkgconfig/libopeniscsiusr.pc

%changelog
* Mon Apr 01 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 2.1.6-4
- Bump version as a part of util-linux upgrade
* Sun Nov 19 2023 Shreenidhi Shedi <sshedi@vmware.com> 2.1.6-3
- Bump version as a part of openssl upgrade
* Thu Oct 12 2023 Shreenidhi Shedi <sshedi@vmware.com> 2.1.6-2
- Fix systemd unit file generation
* Mon Apr 18 2022 Gerrit Photon <photon-checkins@vmware.com> 2.1.6-1
- Automatic Version Bump
* Wed Nov 24 2021 Satya Naga Vasamsetty <svasamsetty@vmware.com> 2.1.4-2
- increment for openssl 3.0.0 compatibility
* Thu May 06 2021 Gerrit Photon <photon-checkins@vmware.com> 2.1.4-1
- Automatic Version Bump
* Tue Feb 16 2021 Susant Sahani <ssahani@vmware.com> 2.1.3-1
- Initial version.
