Summary:       A JSON implementation in C
Name:          json-c
Version:       0.15
Release:       2%{?dist}
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
mkdir build

%build
pushd build
cmake .. \
      -DCMAKE_INSTALL_PREFIX=%{_prefix} \
      -DBUILD_STATIC_LIBS=OFF
make %{?_smp_mflags}
popd

%install
pushd build
make install DESTDIR=%{buildroot}
popd

%check
pushd build
make %{?_smp_mflags} check
popd

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_lib64dir}/lib%{name}.so.*

%files devel
%defattr(-,root,root,-)
%{_includedir}/%{name}/*
%{_lib64dir}/lib%{name}.so
%{_lib64dir}/pkgconfig/%{name}.pc
%{_lib64dir}/cmake/%{name}

%changelog
*       Tue Sep 01 2020 Ankit Jain <ankitja@vmware.com> 0.15-2
-       Fix json-c packaging
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

