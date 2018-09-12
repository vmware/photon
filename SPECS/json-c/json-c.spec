Summary:    A JSON implementation in C
Name:       json-c
Version:    0.13.1
Release:    1%{?dist}
License:    MIT
URL:        https://github.com/json-c/json-c/wiki
Source0:    https://s3.amazonaws.com/json-c_releases/releases/%{name}-%{version}.tar.gz
%define sha1 %{name}-%{version}=00e049ffc9878b9c2e3c3dcb6b58c4ce9e65024b
Group:		System Environment/Base
Vendor:	    VMware, Inc.
Distribution:	Photon
%description
JSON-C implements a reference counting object model that allows you to easily construct JSON objects in C, output them as JSON formatted strings and parse JSON formatted strings back into the C representation of JSON objects.

%package devel
Summary:	Development libraries and header files for json-c
Requires:	%{name} = %{version}-%{release}

%description devel
The package contains libraries and header files for
developing applications that use json-c.

%prep
%setup -q

%build
autoreconf -fiv
./configure \
	--prefix=%{_prefix}
make %{?_smp_mflags}
%install
make DESTDIR=%{buildroot} install

%check
make %{?_smp_mflags} check

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_libdir}/lib%{name}.so.*
%{_libdir}/*.a
%{_libdir}/*.la
%files devel
%defattr(-,root,root)
%{_includedir}/%{name}/*
%{_libdir}/lib%{name}.so
%{_libdir}/pkgconfig/%{name}.pc

%changelog
*       Wed Oct 10 2018 Ankit Jain <ankitja@vmware.com> 0.13.1-1
-       Updated package to version 0.13.1
*       Mon Apr 03 2017 Divya Thaluru <dthaluru@vmware.com> 0.12.1-1
-       Updated package to version 0.12.1
*       Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.12-2
-       GA - Bump release of all rpms
*       Wed Jun 17 2015 Divya Thaluru <dthaluru@vmware.com> 0.12-1
-       Initial build. First version

