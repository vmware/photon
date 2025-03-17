Summary:        iSCSI tools for Linux
Name:           open-iscsi
Version:        2.1.6
Release:        4%{?dist}
URL:            https://github.com/open-iscsi/open-iscsi
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        %{name}-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}
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

%package        devel
Summary:        Development Libraries for open-iscsi
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description    devel
Header files for doing development with open-iscsi

%prep
%autosetup

%build
sed -i 's/lib64/lib/g' libopeniscsiusr/Makefile
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install %{?_smp_mflags}
make DESTDIR=%{buildroot} install_systemd %{?_smp_mflags}

%post -p /sbin/ldconfig
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
%{_mandir}/man8/iscsi-gen-initiatorname.8.gz

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
* Thu Mar 20 2025 Ankit Jain <ankit-aj.jain@broadcom.com> 2.1.6-4
- Bump-up to build with kmod-34.1
* Wed Dec 11 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 2.1.6-3
- Release bump for SRP compliance
* Mon Dec 18 2023 Alexey Makhalov <alexey.makhalov@broadcom.com> 2.1.6-2
- Fix for https://github.com/vmware/photon/issues/1491
* Mon Apr 18 2022 Gerrit Photon <photon-checkins@vmware.com> 2.1.6-1
- Automatic Version Bump
* Wed Nov 24 2021 Satya Naga Vasamsetty <svasamsetty@vmware.com> 2.1.4-2
- increment for openssl 3.0.0 compatibility
* Thu May 06 2021 Gerrit Photon <photon-checkins@vmware.com> 2.1.4-1
- Automatic Version Bump
* Tue Feb 16 2021 Susant Sahani <ssahani@vmware.com> 2.1.3-1
- Initial version.
