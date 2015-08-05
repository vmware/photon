Summary:	Next generation system logger facilty
Name:		syslog-ng
Version:	3.6.2
Release:	3%{?dist}
License:	GPL + LGPL
URL:		https://www.balabit.com/network-security/syslog-ng/opensource-logging-system
Group:		System Environment/Daemons
Vendor:		VMware, Inc.
Distribution: 	Photon
Source0:	http://my.balabit.com/downloads/syslog-ng/open-source-edition/%{version}/source/%{name}_%{version}.tar.gz
%define sha1 syslog-ng=36eeaf920383ee8cb1c17d945205b7562f9fbbb2
Requires:	glib
Requires:	python2
BuildRequires:	eventlog
BuildRequires:	glib-devel
BuildRequires:	python2-libs
BuildRequires:	python2-devel

%description
 The syslog-ng application is a flexible and highly scalable
 system logging tool. It is often used to manage log messages and implement
 centralized logging, where the aim is to collect the log messages of several
 devices to a single, central log server.

%package	devel
Summary:	Header and development files for syslog-ng
Requires:	%{name} = %{version}
%description    devel
 syslog-ng-devel package contains header files, pkfconfig files, and libraries
 needed to build applications using syslog-ng APIs.

%prep
%setup -q
%build
./configure \
	CFLAGS="%{optflags}" \
	CXXFLAGS="%{optflags}" \
	--disable-silent-rules \
	--prefix=%{_prefix} \
	--bindir=%{_bindir} \
	--libdir=%{_libdir} \
	--sysconfdir=/etc/syslog-ng \
        PKG_CONFIG_PATH=/usr/local/lib/pkgconfig/
make %{?_smp_mflags}

%install
[ %{buildroot} != "/"] && rm -rf %{buildroot}/*
make DESTDIR=%{buildroot} install
mkdir -p %{buildroot}/etc/systemd/system/
cat << EOF >> %{buildroot}/etc/systemd/system/syslog-ng.service
[Unit]
Description=Next generation system logger facility

[Service]
Type=forking
ExecStart=/usr/sbin/syslog-ng

[Install]
WantedBy=multi-user.target
EOF

find %{buildroot} -name "*.la" -exec rm -f {} \;
rm %{buildroot}/%{_libdir}/pkgconfig/syslog-ng-test.pc
rm %{buildroot}/%{_libdir}/syslog-ng/libtest/libsyslog-ng-test.a
rm -rf %{buildroot}/%{_infodir}

%{_fixperms} %{buildroot}/*

%check
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}

%post
mkdir -p /usr/var/
/bin/systemctl enable syslog-ng

%preun
/bin/systemctl disable syslog-ng

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
/etc/syslog-ng/*.conf
/etc/systemd/system/syslog-ng.service
/usr/bin/*
/usr/lib/libsyslog-ng*
/usr/sbin/syslog-ng
/usr/sbin/syslog-ng-ctl
/usr/share/man/*

%files devel
/usr/include/syslog-ng/*.h
/usr/include/syslog-ng/compat/*.h
/usr/include/syslog-ng/control/*.h
/usr/include/syslog-ng/filter/*.h
/usr/include/syslog-ng/ivykis/*.h
/usr/include/syslog-ng/libtest/*.h
/usr/include/syslog-ng/logproto/*.h
/usr/include/syslog-ng/parser/*.h
/usr/include/syslog-ng/rewrite/*.h
/usr/include/syslog-ng/stats/*.h
/usr/include/syslog-ng/template/*.h
/usr/include/syslog-ng/transport/*.h
/usr/lib/syslog-ng/lib*.so
/usr/lib/pkgconfig/syslog-ng.pc
/usr/share/include/scl/*
/usr/share/tools/*
/usr/share/xsd/*

%changelog
*       Wed Aug 05 2015 Kumar Kaushik <kaushikk@vmware.com> 3.6.2-3
-       Adding preun section.
*	Sat Jul 18 2015 Vinay Kulkarni <kulkarniv@vmware.com> 3.6.2-2
-	Split headers and unshared libs over to devel package.
*	Thu Jun 4 2015 Vinay Kulkarni <kulkarniv@vmware.com> 3.6.2-1
-	Add syslog-ng support to photon.

