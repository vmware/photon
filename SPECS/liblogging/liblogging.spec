Summary:	Logging Libraries
Name:		liblogging
Version:	1.0.6
Release:	1%{?dist}
License: 	BSD
URL:     	http://www.liblogging.org/
Source0: 	http://download.rsyslog.com/liblogging/liblogging-%{version}.tar.gz
%define sha1 liblogging=f07012fc8bd74e0c7bdcacaa772828639d1a9657
Group:		System Environment/Libraries
Vendor:		VMware, Inc.
Distribution:	Photon
%description
liblogging (the upstream project) is a collection of several components.
Namely: stdlog, journalemu, rfc3195.
The stdlog component of liblogging can be viewed as an enhanced version of the
syslog(3) API. It retains the easy semantics, but makes the API more
sophisticated "behind the scenes" with better support for multiple threads
and flexibility for different log destinations (e.g. syslog and systemd
journal).

%package devel
Summary:	Development libraries and header files for liblogging
Requires:	liblogging

%description devel
The package contains libraries and header files for
developing applications that use liblogging.

%prep
%setup -q
%build
./configure \
	--prefix=%{_prefix} \
	--disable-journal
make %{?_smp_mflags}
%install
make DESTDIR=%{buildroot} install

%check
make %{?_smp_mflags} check

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig
%files
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/*.so.*
%{_mandir}/man1/*
%{_mandir}/man3/*
%{_libdir}/*.a
%{_libdir}/*.la
%files devel
%defattr(-,root,root)
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_includedir}/liblogging/*.h
%changelog
*	Tue Apr 11 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 1.0.6-1
-	Updated to version 1.0.6
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.0.5-2
-	GA - Bump release of all rpms
*	Wed Jun 17 2015 Divya Thaluru <dthaluru@vmware.com> 1.0.5-1
-	Initial build. First version

