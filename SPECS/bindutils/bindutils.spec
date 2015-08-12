Summary:	Domain Name System software
Name:		bindutils
Version:	9.10.1
Release:	1%{?dist}
License:	ISC
URL:		http://www.isc.org/downloads/bind/
Source0:	ftp://ftp.isc.org/isc/bind9/9.10.1-P1/bind-%{version}-P1.tar.gz
%define sha1 bind=24a81ba458a762c27be47461301fcf336cfb1d43
Group:		Development/Tools
Vendor:		VMware, Inc.
Distribution:	Photon
Requires:	openssl
BuildRequires:	openssl-devel
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
%check
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}
%files
%defattr(-,root,root)
%{_bindir}/*
%{_mandir}/man1/*

%changelog
*	Tue Aug 11 2015 Divya Thaluru <dthaluru@vmware.com> 9.10.1-1
-	Fixing release 
*	Tue Jan 20 2015 Divya Thaluru <dthaluru@vmware.com> 9.10.1-P1
-	Initial build. First version
