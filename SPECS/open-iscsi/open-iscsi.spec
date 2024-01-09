Summary:        iSCSI tools for Linux
Name:           open-iscsi
Version:        2.1.3
Release:        3%{?dist}
License:        GPLv2
URL:            https://github.com/open-iscsi/open-iscsi
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        %{name}-%{version}.tar.gz
%define sha512  open=0de417dc45b765458c5a1f09029b5df9b5c18d45d7a8fb6b38d539b7013f512a3c8731d5046f554611eccc77b93fea0df30fe4932d79cea44776ac944c398a52

BuildRequires:  open-isns-devel
BuildRequires:  openssl-devel
BuildRequires:  kmod-devel
BuildRequires:  systemd-devel
BuildRequires:  util-linux-devel

Requires:       openssl
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
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install %{?_smp_mflags}
install -d %{buildroot}%{_unitdir}
install -pm 644 etc/systemd/iscsi.service %{buildroot}%{_unitdir}
install -pm 644 etc/systemd/iscsi-init.service %{buildroot}%{_unitdir}
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
%{_unitdir}/iscsi-init.service
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
%{_includedir}/libopeniscsiusr_node.h
%{_libdir}/libopeniscsiusr.so
%{_libdir}/pkgconfig/libopeniscsiusr.pc

%changelog
* Tue Jan 09 2024 Brennan Lamoreaux <blamoreaux@vmware.com> 2.1.3-3
- Package iscsi-init service file as well
* Wed Nov 24 2021 Satya Naga Vasamsetty <svasamsetty@vmware.com> 2.1.3-2
- increment for openssl 3.0.0 compatibility
* Tue Feb 16 2021 Susant Sahani <ssahani@vmware.com> 2.1.3-1
- Initial version.
