Summary:	Logging Libraries
Name:		liblogging
Version:	1.0.5
Release:	2%{?dist}
License: 	BSD
URL:     	http://www.liblogging.org/
Source0: 	http://download.rsyslog.com/liblogging/liblogging-%{version}.tar.gz
%define sha1 liblogging=e202bf9412747ecd384678e8b3024a4646d45c2f
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
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}
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
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.0.5-2
-	GA - Bump release of all rpms
*	Wed Jun 17 2015 Divya Thaluru <dthaluru@vmware.com> 1.0.5-1
-	Initial build. First version

