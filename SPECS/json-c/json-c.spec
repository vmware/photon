Summary:	A JSON implementation in C
Name:		json-c
Version:	0.13.1
Release:	1%{?dist}
License:        MIT
URL:            https://github.com/json-c/json-c/wiki
Source0:        https://s3.amazonaws.com/json-c_releases/releases/%{name}-%{version}.tar.gz
%define sha1 json-c=00e049ffc9878b9c2e3c3dcb6b58c4ce9e65024b
Group:		System Environment/Base
Vendor:		VMware, Inc.
Distribution:	Photon
Patch0:         CVE-2020-12762-Protect-array_list.patch
Patch1:         CVE-2020-12762-division-by-zero.patch
Patch2:         CVE-2020-12762-integer-overflow.patch
Patch3:         CVE-2020-12762-Fix-backwards-check.patch

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
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

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
*       Fri May 15 2020 Ankit Jain <ankitja@vmware.com> 0.13.1-1
-       Updated to 0.13.1 and fixed CVE-2020-12762
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.12-2
-	GA - Bump release of all rpms
*	Wed Jun 17 2015 Divya Thaluru <dthaluru@vmware.com> 0.12-1
-	Initial build. First version

