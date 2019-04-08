Summary:        Domain Name System software
Name:           bindutils
Version:        9.10.6
Release:        2%{?dist}
License:        ISC
URL:            http://www.isc.org/downloads/bind/
Source0:        ftp://ftp.isc.org/isc/bind9/%{version}-P8/bind-%{version}-P1.tar.gz
%define sha1    bind=adb06033d5538f2412c8f61ffca123e293ca393a
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon
Requires:       openssl
Requires:       shadow
BuildRequires:  openssl-devel
%description
BIND is open source software that implements the Domain Name System (DNS) protocols 
for the Internet. It is a reference implementation of those protocols, but it is 
also production-grade software, suitable for use in high-volume and high-reliability applications.
%prep
%setup -qn bind-%{version}-P1
%build
./configure \
        --prefix=%{_prefix}
make -C lib/dns %{?_smp_mflags}
make -C lib/isc %{?_smp_mflags}
make -C lib/bind9 %{?_smp_mflags}
make -C lib/isccfg %{?_smp_mflags}
make -C lib/lwres %{?_smp_mflags}
make -C bin/dig %{?_smp_mflags}
%install
make -C bin/dig DESTDIR=%{buildroot} install
find %{buildroot} -name '*.la' -delete
mkdir -p %{buildroot}/%{_sysconfdir}
mkdir -p %{buildroot}/%{_prefix}/lib/tmpfiles.d
%check
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}

%post -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_bindir}/*
%{_mandir}/man1/*

%changelog
*   Mon Apr 08 2019 Ajay Kaher <akaher@vmware.com> 9.10.6-2
-   Removed named.conf, not require for bind client
*   Mon Feb 12 2018 Xiaolin Li <xiaolinl@vmware.com> 9.10.6-1
-   Upgrading version to 9.10.6-P1, fix CVE-2017-3145
*   Thu Jun 15 2017 Kumar Kaushik <kaushikk@vmware.com> 9.10.4-2
-   Upgraded the version to 9.10.4-P8, fixing CVE-2016-2776
*   Mon Jun 06 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 9.10.4-1
-   Upgraded the version to 9.10.4
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 9.10.3-3
-   GA - Bump release of all rpms
*   Fri Apr 29 2016 Xiaolin Li <xiaolinl@vmware.com> 9.10.3-2
-   Add group named and user named
*   Thu Jan 21 2016 Xiaolin Li <xiaolinl@vmware.com> 9.10.3-1
-   Updated to version 9.10.3
*   Tue Aug 11 2015 Divya Thaluru <dthaluru@vmware.com> 9.10.1-1
-   Fixing release 
*   Tue Jan 20 2015 Divya Thaluru <dthaluru@vmware.com> 9.10.1-P1
-   Initial build. First version
