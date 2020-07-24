Summary:       A JSON implementation in C
Name:          json-c
Version:       0.15
Release:       1%{?dist}
License:       MIT
URL:           https://github.com/json-c/json-c/wiki
Source0:       https://s3.amazonaws.com/json-c_releases/releases/%{name}-%{version}.tar.gz
%define sha1   %{name}-%{version}=dd6473818fe66f16e747ae0df626a2e1559343b9
Group:         System Environment/Base
Vendor:	       VMware, Inc.
Distribution:  Photon
BuildRequires: cmake

%description
JSON-C implements a reference counting object model that allows you to easily construct JSON objects in C,
output them as JSON formatted strings and parse JSON formatted strings back into the C representation of JSON objects.

%package       devel
Summary:       Development libraries and header files for json-c
Requires:      %{name} = %{version}-%{release}

%description  devel
The package contains libraries and header files for
developing applications that use json-c.

%prep
%setup -q -n %{name}-%{name}-%{version}-20200726

%build
mkdir build
cd build
../cmake-configure
make

%install
cd build
make all DESTDIR=%{buildroot} install

%check
make %{?_smp_mflags} check

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
/usr/local/lib64/lib%{name}.so.*
/usr/local/lib64/cmake/json-c/*

%files devel
/usr/local/include/*
/usr/local/lib64/*.so
/usr/local/lib64/*.a
/usr/local/lib64/pkgconfig/*.pc

%changelog
*       Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 0.15-1
-       Automatic Version Bump
*       Fri May 15 2020 Ankit Jain <ankitja@vmware.com> 0.13.1-2
-       Fix for CVE-2020-12762
*       Wed Oct 10 2018 Ankit Jain <ankitja@vmware.com> 0.13.1-1
-       Updated package to version 0.13.1
*       Mon Apr 03 2017 Divya Thaluru <dthaluru@vmware.com> 0.12.1-1
-       Updated package to version 0.12.1
*       Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.12-2
-       GA - Bump release of all rpms
*       Wed Jun 17 2015 Divya Thaluru <dthaluru@vmware.com> 0.12-1
-       Initial build. First version

