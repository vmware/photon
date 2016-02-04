Summary:	Rocket-fast system for log processing
Name:		rsyslog
Version:	8.15.0
Release:	1%{?dist}
License:	GPLv3+ and ASL 2.0
URL:		http://www.rsyslog.com/
Source0:	http://www.rsyslog.com/files/download/rsyslog/%{name}-%{version}.tar.gz
%define sha1 rsyslog=e1d5ff63c96bce9945dc65581c8e195950256d3c
Group:		System Environment/Base
Vendor:		VMware, Inc.
Distribution:	Photon
BuildRequires:	systemd
BuildRequires:	libestr-devel
BuildRequires:	json-c-devel
BuildRequires:	libgcrypt-devel
BuildRequires:	liblogging-devel
BuildRequires:	librelp-devel
BuildRequires:  autogen
BuildRequires:  gnutls-devel
Requires:   gnutls
Requires:	systemd
Requires:	libestr
Requires:	json-c
Requires:	libgcrypt
Requires:	liblogging
Requires:	librelp
%description
RSYSLOG is the rocket-fast system for log processing.
It offers high-performance, great security features and a modular design. While it started as a regular syslogd, rsyslog has evolved into a kind of swiss army knife of logging, being able to accept inputs from a wide variety of sources, transform them, and output to the results to diverse destinations.
%prep
%setup -q
%build
./configure \
	--prefix=%{_prefix} \
    --enable-relp \
    --enable-gnutls\
	--enable-imfile \
	--enable-imjournal \
	--enable-impstats \
	--enable-imptcp

make %{?_smp_mflags}
%install
make DESTDIR=%{buildroot} install
install -vd %{buildroot}%{_libdir}/systemd/system/
mv %{buildroot}/lib/systemd/system/rsyslog.service  %{buildroot}%{_libdir}/systemd/system/rsyslog.service
find %{buildroot} -name '*.la' -delete
%check
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}
%post
/sbin/ldconfig
/bin/systemctl enable  rsyslog.service

%postun
/sbin/ldconfig
/bin/systemctl disable rsyslog.service

%files
%defattr(-,root,root)
%{_sbindir}/*
%{_libdir}/rsyslog/*.so
%{_mandir}/man5/*
%{_mandir}/man8/*
%{_libdir}/systemd/system/rsyslog.service
%changelog
*   Mon Jan 11  2016 Xiaolin Li <xiaolinl@vmware.com> 8.15.0-1
-   Update rsyslog to 8.15.0
*	Wed Jun 17 2015 Divya Thaluru <dthaluru@vmware.com> 8.10.0-1
-	Initial build. First version

