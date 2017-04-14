Summary:	Next generation system logger facilty
Name:		syslog-ng
Version:	3.9.1
Release:	1%{?dist}
License:	GPL + LGPL
URL:		https://syslog-ng.org/
Group:		System Environment/Daemons
Vendor: 	VMware, Inc.
Distribution: 	Photon
Source0:	https://github.com/balabit/%{name}/releases/download/%{name}-%{version}/%{name}-%{version}.tar.gz
%define sha1 syslog-ng=1ca437393d8895654452bef8ac0b996fe73284f8
Source1:	60-syslog-ng-journald.conf
Requires:	glib
Requires:	json-glib
Requires:	json-c
Requires:   	eventlog
Requires:	python2
Requires:	systemd
BuildRequires:	eventlog
BuildRequires:	glib-devel
BuildRequires:	json-glib-devel
BuildRequires:	json-c-devel
BuildRequires:	python2-libs
BuildRequires:	python2-devel
BuildRequires:	systemd-devel

%description
 The syslog-ng application is a flexible and highly scalable
 system logging tool. It is often used to manage log messages and implement
 centralized logging, where the aim is to collect the log messages of several
 devices to a single, central log server.

%package	devel
Summary:	Header and development files for syslog-ng
Requires:	%{name} = %{version}
%description	devel
 syslog-ng-devel package contains header files, pkfconfig files, and libraries
 needed to build applications using syslog-ng APIs.

%package	python
Summary:	python interface for syslog-ng
Requires:	%{name} = %{version}
%description	python
 This packages has the python interface to syslog-ng

%prep
%setup -q

%build
./configure \
	CFLAGS="%{optflags}" \
	CXXFLAGS="%{optflags}" \
	--disable-silent-rules \
	--prefix=%{_prefix} \
	--bindir=%{_bindir} \
	--includedir=%{_includedir} \
	--libdir=%{_libdir} \
	--sysconfdir=/etc/syslog-ng \
	--enable-systemd \
	--with-systemdsystemunitdir=%{_libdir}/systemd/system \
	--enable-json=yes \
	--with-jsonc=system \
	--disable-java \
	--disable-redis \
        PKG_CONFIG_PATH=/usr/local/lib/pkgconfig/
make %{?_smp_mflags}

%install
[ %{buildroot} != "/"] && rm -rf %{buildroot}/*
make DESTDIR=%{buildroot} install
find %{buildroot} -name "*.la" -exec rm -f {} \;
rm %{buildroot}/%{_libdir}/pkgconfig/syslog-ng-test.pc
rm %{buildroot}/%{_libdir}/syslog-ng/libtest/libsyslog-ng-test.a
rm -rf %{buildroot}/%{_infodir}
install -vd %{buildroot}%{_sysconfdir}/systemd/journald.conf.d/
install -p -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/systemd/journald.conf.d/
%{_fixperms} %{buildroot}/*

%check
make %{?_smp_mflags} check

%post
if [ $1 -eq 1 ] ; then
  mkdir -p /usr/var/
fi
%systemd_post syslog-ng.service

%preun
%systemd_preun syslog-ng.service

%postun
%systemd_postun_with_restart syslog-ng.service

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/syslog-ng/syslog-ng.conf
%config(noreplace) %{_sysconfdir}/syslog-ng/scl.conf
%{_sysconfdir}/systemd/journald.conf.d/*
%{_libdir}/systemd/system/syslog-ng.service
/usr/bin/*
/usr/sbin/syslog-ng
/usr/sbin/syslog-ng-ctl
%{_libdir}/libsyslog-ng-3.9.so.*
%{_libdir}/syslog-ng/lib*.so
/usr/share/syslog-ng/*

%files devel
%defattr(-,root,root)
%{_includedir}/syslog-ng/*
%{_libdir}/libsyslog-ng.so
%{_libdir}/libsyslog-ng-native-connector.a
%{_libdir}/pkgconfig/*

%files python
%defattr(-,root,root)
/usr/lib/python2.7/site-packages/*

%changelog
*   Tue Apr 11 2017 Vinay Kulkarni <kulkarniv@vmware.com> 3.9.1-1
-   Update to version 3.9.1
*   Tue Oct 04 2016 ChangLee <changlee@vmware.com> 3.6.4-6
-   Modified %check
*   Thu May 26 2016 Divya Thaluru <dthaluru@vmware.com>  3.6.4-5
-   Fixed logic to restart the active services after upgrade
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.6.4-4
-   GA - Bump release of all rpms
*   Wed May 4 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com>  3.6.4-3
-   Fix for upgrade issues
*   Wed Feb 17 2016 Anish Swaminathan <anishs@vmware.com>  3.6.4-2
-   Add journald conf file.
*   Wed Jan 20 2016 Anish Swaminathan <anishs@vmware.com> 3.6.4-1
-   Upgrade version.
*   Tue Jan 12 2016 Anish Swaminathan <anishs@vmware.com>  3.6.2-5
-   Change config file attributes.
*   Wed Dec 09 2015 Mahmoud Bassiouny <mbassiouny@vmware.com> 3.6.2-4
-   Moving files from devel rpm to the main package.
*   Wed Aug 05 2015 Kumar Kaushik <kaushikk@vmware.com> 3.6.2-3
-   Adding preun section.
*   Sat Jul 18 2015 Vinay Kulkarni <kulkarniv@vmware.com> 3.6.2-2
-   Split headers and unshared libs over to devel package.
*   Thu Jun 4 2015 Vinay Kulkarni <kulkarniv@vmware.com> 3.6.2-1
-   Add syslog-ng support to photon.
