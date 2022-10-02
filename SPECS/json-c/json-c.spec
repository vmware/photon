Summary:    A JSON implementation in C
Name:       json-c
Version:    0.13.1
Release:    4%{?dist}
License:    MIT
URL:        https://github.com/json-c/json-c/wiki
Group:      System Environment/Base
Vendor:     VMware, Inc.
Distribution:   Photon

Source0:    https://s3.amazonaws.com/json-c_releases/releases/%{name}-%{version}.tar.gz
%define sha512 %{name}-%{version}=e984db2a42b9c95b52c798b2e8dd1b79951a8dcba27370af30c43b9549fbb00008dbcf052a535c528209aaee38e6d1f760168b706905ae72f3e704ed20f8a1a1

Patch0:     CVE-2020-12762-Protect-array_list.patch
Patch1:     CVE-2020-12762-division-by-zero.patch
Patch2:     CVE-2020-12762-integer-overflow.patch

%description
JSON-C implements a reference counting object model that allows you to easily construct JSON objects in C, output them as JSON formatted strings and parse JSON formatted strings back into the C representation of JSON objects.

%package devel
Summary:    Development libraries and header files for json-c
Requires:   %{name} = %{version}-%{release}

%description devel
The package contains libraries and header files for
developing applications that use json-c.

%prep
%autosetup -p1

%build
autoreconf -fiv
%configure
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install %{?_smp_mflags}

%check
make %{?_smp_mflags} check

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_libdir}/lib%{name}.so.*
%{_libdir}/*.a

%files devel
%defattr(-,root,root)
%{_includedir}/%{name}/*
%{_libdir}/lib%{name}.so
%{_libdir}/pkgconfig/%{name}.pc

%changelog
* Sun Oct 02 2022 Shreenidhi Shedi <sshedi@vmware.com> 0.13.1-4
- Remove .la files
* Thu May 28 2020 Harinadh Dommaraju <hdommaraju@vmware.com> 0.13.1-3
- Fix for size issue in CVE-2020-12762-integer-overflow.patch
* Fri May 15 2020 Ankit Jain <ankitja@vmware.com> 0.13.1-2
- Fix for CVE-2020-12762
* Wed Oct 10 2018 Ankit Jain <ankitja@vmware.com> 0.13.1-1
- Updated package to version 0.13.1
* Mon Apr 03 2017 Divya Thaluru <dthaluru@vmware.com> 0.12.1-1
- Updated package to version 0.12.1
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.12-2
- GA - Bump release of all rpms
* Wed Jun 17 2015 Divya Thaluru <dthaluru@vmware.com> 0.12-1
- Initial build. First version
