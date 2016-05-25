Summary:	A JSON implementation in C
Name:		json-c
Version:	0.12
Release:	2%{?dist}
License:        MIT
URL:            https://github.com/json-c/json-c/wiki
Source0:        https://s3.amazonaws.com/json-c_releases/releases/json-c-0.12.tar.gz
%define sha1 json-c=5580aad884076c219d41160cbd8bc12213d12c37
Group:		System Environment/Base
Vendor:		VMware, Inc.
Distribution:	Photon
%description
JSON-C implements a reference counting object model that allows you to easily construct JSON objects in C, output them as JSON formatted strings and parse JSON formatted strings back into the C representation of JSON objects.

%package devel
Summary:	Development libraries and header files for json-c
Requires:	json-c

%description devel
The package contains libraries and header files for
developing applications that use json-c.

%prep
%setup -q
sed -i 's|-Werror ||g' Makefile.am.inc
%build
autoreconf -fiv
./configure \
	--prefix=%{_prefix}
make %{?_smp_mflags}
%install
make DESTDIR=%{buildroot} install
%check
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}
%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig
%files
%defattr(-,root,root)
%{_libdir}/libjson-c.so.*
%{_libdir}/*.a
%{_libdir}/*.la
%files devel
%defattr(-,root,root)
%{_includedir}/json-c/*
%{_libdir}/libjson-c.so
%{_libdir}/pkgconfig/json-c.pc
%changelog
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 	0.12-2
-	GA - Bump release of all rpms
*	Wed Jun 17 2015 Divya Thaluru <dthaluru@vmware.com> 0.12-1
-	Initial build. First version

