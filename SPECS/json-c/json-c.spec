%define timestamp 20220414
Summary:       A JSON implementation in C
Name:          json-c
Version:       0.16
Release:       2%{?dist}
URL:           https://github.com/json-c/json-c/wiki
Group:         System Environment/Base
Vendor:        VMware, Inc.
Distribution:  Photon
Source0:       https://s3.amazonaws.com/json-c_releases/releases/%{name}-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}
BuildRequires: cmake

%description
JSON-C implements a reference counting object model that allows you to easily construct JSON objects in C,
output them as JSON formatted strings and parse JSON formatted strings back into the C representation of JSON objects.

%package       devel
Summary:       Development libraries and header files for json-c
Requires:      %{name} = %{version}-%{release}

%description   devel
The package contains libraries and header files for developing applications that use json-c.

%prep
%autosetup -n %{name}-%{name}-%{version}-%{timestamp} -p1

%build
%cmake \
      -DCMAKE_BUILD_TYPE=Debug \
      -DCMAKE_INSTALL_PREFIX=%{_prefix} \
      -DCMAKE_INSTALL_LIBDIR=%{_libdir} \
      -DBUILD_STATIC_LIBS=OFF \
      -DCMAKE_BUILD_TYPE:STRING=RELEASE \
      -DCMAKE_C_FLAGS_RELEASE:STRING="" \
      -DDISABLE_BSYMBOLIC:BOOL=OFF \
      -DDISABLE_WERROR:BOOL=ON \
      -DENABLE_RDRAND:BOOL=ON \
      -DENABLE_THREADING:BOOL=ON
%cmake_build

%install
%cmake_install

%if 0%{?with_check}
%check
make %{?_smp_mflags} check
%endif

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_libdir}/lib%{name}.so.*

%files devel
%defattr(-,root,root,-)
%{_includedir}/%{name}/*
%{_libdir}/lib%{name}.so
%{_libdir}/pkgconfig/%{name}.pc
%{_libdir}/cmake/%{name}

%changelog
* Wed Dec 11 2024 Tapas Kundu <tapas.kundu@broadcom.com> 0.16-2
- Release bump for SRP compliance
* Mon Jul 11 2022 Gerrit Photon <photon-checkins@vmware.com> 0.16-1
- Automatic Version Bump
* Fri Jun 17 2022 Shreenidhi Shedi <sshedi@vmware.com> 0.15-4
- Fix build with latest cmake
* Tue Jan 05 2021 Susant Sahani <ssahani@vmware.com> 0.15-3
- Move from lib64 to lib
* Tue Sep 01 2020 Ankit Jain <ankitja@vmware.com> 0.15-2
- Fix json-c packaging
* Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 0.15-1
- Automatic Version Bump
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
