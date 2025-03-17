Summary:        iSNS server and client for Linux
Name:           open-isns
Version:        0.101
Release:        3%{?dist}
URL:            https://github.com/open-iscsi/open-isns
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: %{name}-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  openssl-devel
BuildRequires:  systemd-devel

Requires:       openssl
Requires:       systemd

%description
iSNS server and client for Linux

%package devel
Summary:    Development Libraries for open-isns
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}

%description devel
Header files for doing development with open-isns.

%prep
%autosetup -p1

%build
export CFLAGS="-Werror=unused-result"
%configure
%make_build

%install
%make_install %{?_smp_mflags}
%make_install %{?_smp_mflags} install_hdrs
%make_install %{?_smp_mflags} install_lib

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/isns/isnsadm.conf
%config(noreplace) %{_sysconfdir}/isns/isnsd.conf
%config(noreplace) %{_sysconfdir}/isns/isnsdd.conf
%{_unitdir}/isnsd.service
%{_unitdir}/isnsd.socket
%{_sbindir}/isnsadm
%{_sbindir}/isnsd
%{_sbindir}/isnsdd
%{_mandir}/man5/isns_config.5.gz
%{_mandir}/man8/isnsadm.8.gz
%{_mandir}/man8/isnsd.8.gz
%{_mandir}/man8/isnsdd.8.gz
%{_mandir}/man8/isnssetup.8.gz

%files devel
%defattr(-,root,root)
%{_includedir}/libisns
%{_libdir}/libisns.a

%changelog
* Wed Dec 11 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 0.101-3
- Release bump for SRP compliance
* Mon Nov 15 2021 Satya Naga Vasamsetty <svasamsetty@vmware.com> 0.101-2
- Increment for openssl 3.0.0 compatibility
* Wed Feb 17 2021 Ankit Jain <ankitja@vmware.com> 0.101-1
- Initial version.
