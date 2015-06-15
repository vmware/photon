Summary:	Syslog event logger library
Name:		eventlog
Version:	0.2.12
Release:	1%{?dist}
License:	GPL
URL:		https://www.balabit.com
Group:		System Environment/Daemons
Vendor:		VMware, Inc.
Distribution: 	Photon
Source0:	https://www.balabit.com/downloads/files/eventlog/0.2/%{name}_%{version}.tar.gz
BuildRequires:	bison
BuildRequires:	flex

%description
The EventLog library aims to be a replacement of the simple syslog() API
provided on UNIX systems. The major difference between EventLog and syslog
is that EventLog tries to add structure to messages.

EventLog provides an interface to build, format and output an event record.
The exact format and output method can be customized by the administrator
via a configuration file.

This package is the runtime part of the library.

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
	--sysconfdir=/etc
make %{?_smp_mflags}

%install
%makeinstall

%check
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_includedir}/eventlog/*.h
%{_libdir}/*.a
%{_libdir}/*.la
%{_libdir}/*.so
%{_libdir}/*.so.*
%{_libdir}/pkgconfig/eventlog.pc

%changelog
*	Fri Jun 5 2015 Vinay Kulkarni <kulkarniv@vmware.com> 0.2.12-1
-	Add eventlog library for syslog-ng to photon

