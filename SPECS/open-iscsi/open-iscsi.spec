Summary:        iSCSI tools for Linux
Name:           open-iscsi
Version:        2.1.1
Release:        3%{?dist}
License:        GPLv2
URL:            https://github.com/open-iscsi/open-iscsi
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://github.com/open-iscsi/open-iscsi/archive/refs/tags/%{name}-%{version}.tar.gz
%define sha512  open=88dbea433fe5266714c5c73ce4b60dfb8ddeffcaad4ff77abbdda2a865d29d4307ca51b8f45376f54542b19baed30d5f2f1836a8c136eb0af840f489f47e4fb3
Patch0:         CVE-2020-13987.patch
Patch1:         CVE-2020-17437.patch
Patch2:         CVE-2020-13988.patch
BuildRequires:  open-isns-devel
BuildRequires:  nxtgn-openssl-devel
BuildRequires:  kmod-devel
BuildRequires:  systemd-devel
BuildRequires:  util-linux-devel
Requires:       nxtgn-openssl
Requires:       kmod
Requires:       systemd
Requires:       util-linux
%description
iSCSI tools for Linux

%package devel
Summary: Development Libraries for open-iscsi
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
%description devel
Header files for doing development with open-iscsi.

%prep
%autosetup -p1

%build
sed -i 's/lib64/lib/g' libopeniscsiusr/Makefile
%make_build %{?_smp_mflags}

%install
%make_install %{?_smp_mflags}
install -d %{buildroot}%{_unitdir}
install -pm 644 etc/systemd/iscsi.service %{buildroot}%{_unitdir}
install -pm 644 etc/systemd/iscsid.service %{buildroot}%{_unitdir}
install -pm 644 etc/systemd/iscsid.socket %{buildroot}%{_unitdir}
install -pm 644 etc/systemd/iscsiuio.service %{buildroot}%{_unitdir}
install -pm 644 etc/systemd/iscsiuio.socket %{buildroot}%{_unitdir}

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_sysconfdir}/iscsi/ifaces/iface.example
%config(noreplace) %{_sysconfdir}/iscsi/initiatorname.iscsi
%config(noreplace) %{_sysconfdir}/iscsi/iscsid.conf
/sbin/iscsi-gen-initiatorname
/sbin/iscsi-iname
/sbin/iscsi_discovery
/sbin/iscsi_fw_login
/sbin/iscsi_offload
/sbin/iscsiadm
/sbin/iscsid
/sbin/iscsistart
/sbin/iscsiuio
%{_unitdir}/iscsi.service
%{_unitdir}/iscsid.service
%{_unitdir}/iscsid.socket
%{_unitdir}/iscsiuio.service
%{_unitdir}/iscsiuio.socket
%{_libdir}/libopeniscsiusr.so.*
%{_mandir}/man8/iscsi-iname.8.gz
%{_mandir}/man8/iscsi_discovery.8.gz
%{_mandir}/man8/iscsi_fw_login.8.gz
%{_mandir}/man8/iscsiadm.8.gz
%{_mandir}/man8/iscsid.8.gz
%{_mandir}/man8/iscsistart.8.gz
%{_mandir}/man8/iscsiuio.8.gz

%files devel
%defattr(-,root,root)
%{_includedir}/libopeniscsiusr.h
%{_includedir}/libopeniscsiusr_common.h
%{_includedir}/libopeniscsiusr_iface.h
%{_includedir}/libopeniscsiusr_session.h
%{_libdir}/libopeniscsiusr.so
%{_libdir}/pkgconfig/libopeniscsiusr.pc

%changelog
* Tue May 09 2023 Harinadh D <hdommaraju@vmware.com> 2.1.1-3
- Fix CVE-2020-13988
* Tue Aug 09 2022 Harinadh D <hdommaraju@vmware.com> 2.1.1-2
- Fix CVE-2020-13987,CVE-2020-17437
* Wed Jun 24 2020 Alexey Makhalov <amakhalov@vmware.com> 2.1.1-1
- Initial version.
