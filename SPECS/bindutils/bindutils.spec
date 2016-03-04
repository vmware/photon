Summary:	Domain Name System software
Name:		bindutils
Version:	9.10.3
Release:	1%{?dist}
License:	ISC
URL:		http://www.isc.org/downloads/bind/
Source0:	ftp://ftp.isc.org/isc/bind9/bind-9-10-3-p2/bind-%{version}-P2.tar.gz
%define sha1 bind=c23663a9b464cff6f2279e80513ef97f9fe5803b
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
%setup -qn bind-%{version}-P2
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
cat << EOF >> %{buildroot}/%{_sysconfdir}/named.conf
zone "." in {
    type master;
    allow-update {none;}; // no DDNS by default
};
EOF
echo "d /run/named 0755 named named - -" > %{buildroot}/%{_prefix}/lib/tmpfiles.d/named.conf
%check
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}
%files
%defattr(-,root,root)
%{_bindir}/*
%{_mandir}/man1/*
%{_sysconfdir}/*
%{_prefix}/lib/tmpfiles.d/named.conf


%changelog
*   Thu Jan 21 2016 Xiaolin Li <xiaolinl@vmware.com> 9.10.3-1
-   Updated to version 9.10.3
*	Tue Aug 11 2015 Divya Thaluru <dthaluru@vmware.com> 9.10.1-1
-	Fixing release 
*	Tue Jan 20 2015 Divya Thaluru <dthaluru@vmware.com> 9.10.1-P1
-	Initial build. First version
