Summary:	Rocket-fast system for log processing
Name:		rsyslog
Version:	8.10.0
Release:	1%{?dist}
License:	GPLv3+ and ASL 2.0
URL:		http://www.rsyslog.com/
Source0:	http://www.rsyslog.com/files/download/rsyslog/%{name}-%{version}.tar.gz
%define sha1 rsyslog=9fddcf1121e438e5291f738bb4619230de525e50
Group:		System Environment/Base
Vendor:		VMware, Inc.
Distribution:	Photon
BuildRequires:	systemd
BuildRequires:	libestr-devel
BuildRequires:	json-c-devel
BuildRequires:	libgcrypt-devel
BuildRequires:	liblogging-devel
BuildRequires:	librelp-devel
Requires:	systemd
Requires:	libestr
Requires:	json-c
Requires:	libgcrypt
Requires:	liblogging
Requires:	librelp
%description
Cronie contains the standard UNIX daemon crond that runs specified programs at
scheduled times and related tools. It is based on the original cron and
has security and configuration enhancements like the ability to use pam and
SELinux.
%prep
%setup -q
%build
./configure \
	--prefix=%{_prefix} \
        --enable-relp
make %{?_smp_mflags}
%install
make DESTDIR=%{buildroot} install
install -vd %{buildroot}%{_libdir}/systemd/system/
mv %{buildroot}/lib/systemd/system/rsyslog.service  %{buildroot}%{_libdir}/systemd/system/rsyslog.service
%check
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}
%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig
%files
%defattr(-,root,root)
%{_sbindir}/*
%{_libdir}/rsyslog/*.so
%{_libdir}/rsyslog/*.la
%{_mandir}/man5/*
%{_mandir}/man8/*
%{_libdir}/systemd/system/rsyslog.service
%changelog
*	Wed Jun 17 2015 Divya Thaluru <dthaluru@vmware.com> 8.10.0-1
-	Initial build. First version

