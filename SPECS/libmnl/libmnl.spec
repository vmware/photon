Summary:       A minimalistic user-space library oriented to Netlink developers.
Name:          libmnl
Version:       1.0.5
Release:       3%{?dist}
URL:           http://netfilter.org/projects/libmnl
Group:         System Environment/libraries
Vendor:        VMware, Inc.
Distribution:  Photon
Source0:       http://netfilter.org/projects/libmnl/files/%{name}-%{version}.tar.bz2
%define sha512 libmnl=16fa48e74c9da7724a85c655dfb0abd8369392627934639d65de951543e1447ac3e048d231248f1ce8861443c2ef62654a85a81feeedbbffaf2e5744f6cf4c9f

Source1: license.txt
%include %{SOURCE1}
Obsoletes:     libmnl-static

%description
libmnl is a minimalistic user-space library oriented to Netlink developers.
There are a lot of common tasks in parsing, validating, constructing of both
the Netlink header and TLVs that are repetitive and easy to get wrong. This
library aims to provide simple helpers that allows you to re-use code and to
avoid re-inventing the wheel.

%package       devel
Summary:       Development files for %{name}
Group:         Development/Libraries
Requires:      libmnl >= 1.0.4

%description   devel
Libraries and header files for libnml library.

%prep
%autosetup

%build
%configure --enable-static=no
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot} %{?_smp_mflags}

%check
make %{?_smp_mflags} -k check

%ldconfig_scriptlets

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_libdir}/libmnl.so.*

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/libmnl.so
%{_libdir}/pkgconfig/*

%changelog
* Wed Dec 11 2024 Mukul Sikka <mukul.sikka@broadcom.com> 1.0.5-3
- Release bump for SRP compliance
* Sun Aug 07 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.0.5-2
- Remove .la files
* Mon Apr 18 2022 Gerrit Photon <photon-checkins@vmware.com> 1.0.5-1
- Automatic Version Bump
* Mon Aug 02 2021 Susant Sahani <ssahani@vmware.com> 1.0.4-4
- Use autosetup and ldconfig scriptlets
* Mon Sep 17 2018 Bo Gan <ganb@vmware.com> 1.0.4-3
- Cleanup spec file
* Wed Jul 5 2017 Divya Thaluru <dthaluru@vmware.com> 1.0.4-2
- Added obsoletes for libmnl-static package which is deprecated
* Wed Aug 3 2016 Xiaolin Li <xiaolinl@vmware.com> 1.0.4-1
- Initial build. First version.
