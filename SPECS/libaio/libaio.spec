Summary:	Linux-native asynchronous I/O access library
Name:		libaio
Version:	0.3.110
Release: 	2%{?dist}
License:	LGPLv2+
Group:		System Environment/Libraries
Vendor:		VMware, Inc.
Distribution:	Photon
Source0:	https://fedorahosted.org/releases/l/i/libaio/libaio-0.3.110.tar.gz
%define sha1 libaio=f8f6ed15f22e528f6f415939b07854539e3360e4
Patch0:		libaio-install-to-destdir-slash-usr.patch

%description
The Linux-native asynchronous I/O facility ("async I/O", or "aio") has a
richer API and capability set than the simple POSIX async I/O facility.
This library, libaio, provides the Linux-native API for async I/O.
The POSIX async I/O facility requires this library in order to provide
kernel-accelerated async I/O capabilities, as do applications which
require the Linux-native async I/O API.

%package	devel
Summary:	Development files for Linux-native asynchronous I/O access
Group:		Development/System
Requires:	libaio

%description	devel
This package provides header files to include and libraries to link with
for the Linux-native asynchronous I/O facility ("async I/O", or "aio").

%prep
%setup -q -a 0
%patch0 -p0 -b .install-to-destdir-slash-usr
%patch0 -p1 -b .install-to-destdir-slash-usr


%build
# A library with a soname of 1.0.0 was inadvertantly released.  This
# build process builds a version of the library with the broken soname in
# the libaio-0.3.103 directory, and then builds the library again
# with the correct soname.
cd %{name}-%{version}
make soname='libaio.so.1.0.0' libname='libaio.so.1.0.0'
cd ..
make

%install
cd %{name}-%{version}
install -D -m 755 src/libaio.so.1.0.0 %{buildroot}/%{_libdir}/libaio.so.1.0.0
cd ..
make destdir=%{buildroot} prefix=%{_prefix} libdir=/lib usrlibdir=%{_libdir} includedir=%{_includedir} install

%check
make %{?_smp_mflags} -k check

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%attr(0755,root,root) %{_libdir}/libaio.so.*
%doc COPYING TODO

%files devel
%attr(0644,root,root) %{_includedir}/*
%attr(0755,root,root) %{_libdir}/libaio.so
%attr(0755,root,root) %{_libdir}/libaio.a

%changelog
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.3.110-2
-	GA - Bump release of all rpms
* Tue Mar 3 2015 Divya Thaluru <dthaluru@vmware.com> 0.3.110-1
- Initial version


