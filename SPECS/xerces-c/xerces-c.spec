Summary:        C++ xml parser.
Name:           xerces-c
Version:        3.2.5
Release:        1%{?dist}
License:        Apache License
URL:            http://xerces.apache.org
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: http://mirror.jax.hugeserver.com/apache//xerces/c/3/sources/%{name}-%{version}.tar.xz
%define sha512 %{name}=77b80148b0a3dbb61af648e2571855d59040512dd0c739a892e8ac6a6d7ddbb43b49850c87c39fcf374f2c7658a9c795b3e3fcd4785efbc6226f831b938d5300

Requires: libstdc++

%description
Xerces-C++ is a validating XML parser written in a portable subset of C++

%package        devel
Summary:        XML library headers
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description    devel
This package contains development headers and static library for xml parser.

%prep
%autosetup -p1

%build
%configure \
  --disable-static

%make_build

%install
%make_install %{?_smp_mflags}

%check
%make_build check

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/*.so

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/pkgconfig/*.pc

%changelog
* Wed Feb 26 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 3.2.5-1
- Upgrade to v3.2.5 to fix CVE-2024-23807
* Tue Oct 25 2022 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 3.2.4-1
- Updated to version 3.2.4
* Sun Oct 02 2022 Shreenidhi Shedi <sshedi@vmware.com> 3.2.3-2
- Remove .la files
* Thu Jun 25 2020 Gerrit Photon <photon-checkins@vmware.com> 3.2.3-1
- Automatic Version Bump
* Mon Apr 16 2018 Xiaolin Li <xiaolinl@vmware.cm> 3.2.1-1
- Update to version to handle CVE-2017-12627
* Mon Jun 05 2017 Bo Gan <ganb@vmware.com> 3.1.4-2
- Fix dependency
* Wed Mar 15 2017 Dheeraj Shetty <dheerajs@vmware.com> 3.1.4-1
- Upgrade to latest version to handle CVE-2016-2099
* Wed Oct 05 2016 ChangLee <changlee@vmware.com> 3.1.3-3
- Modified %check
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.1.3-2
- GA - Bump release of all rpms
* Tue Feb 23 2016 Xiaolin Li <xiaolinl@vmware.com> 3.1.3-1
- Updated to version 3.1.3
* Thu Aug 13 2015 Divya Thaluru <dthaluru@vmware.com> 3.1.2-1
- Updating Package to 3.1.2
* Thu Nov 06 2014 Sharath George <sharathg@vmware.com> 3.1.1
- Initial version
