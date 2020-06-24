Summary:        iSNS server and client for Linux
Name:           open-isns
Version:        0.100
Release:        1%{?dist}
License:        LGPLv2.1
URL:            https://github.com/open-iscsi/open-isns
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        %{name}-%{version}.tar.gz
%define sha1    open=0c625a22714c2ba4bdd58db5ec05ef93fb3c3639
Patch0:         fix-openssl-1.1.1-build-issue.patch
BuildRequires:  nxtgn-openssl-devel
Requires:       nxtgn-openssl
%description
iSNS server and client for Linux

%package devel
Summary: Development Libraries for open-isns
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
%description devel
Header files for doing development with open-isns.

%prep
%setup -q
%patch0 -p1

%build
export CFLAGS="-Werror=unused-result"
%configure
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install
make DESTDIR=%{buildroot} install_hdrs
make DESTDIR=%{buildroot} install_lib

%files
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/isns/isnsadm.conf
%config(noreplace) %{_sysconfdir}/isns/isnsd.conf
%config(noreplace) %{_sysconfdir}/isns/isnsdd.conf
%{_libdir}/systemd/system/isnsd.service
%{_libdir}/systemd/system/isnsd.socket
%{_sbindir}/isnsadm
%{_sbindir}/isnsd
%{_sbindir}/isnsdd
%{_mandir}/man5/isns_config.5.gz
%{_mandir}/man8/isnsadm.8.gz
%{_mandir}/man8/isnsd.8.gz
%{_mandir}/man8/isnsdd.8.gz

%files devel
%defattr(-,root,root)
%{_includedir}/libisns
%{_libdir}/libisns.a

%changelog
* Wed Jun 24 2020 Alexey Makhalov <amakhalov@vmware.com> 0.100-1
- Initial version.
