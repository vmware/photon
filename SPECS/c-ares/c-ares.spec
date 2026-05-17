%global build_if %{photon_subrelease} >= 91

Summary:        A library that performs asynchronous DNS operations
Name:           c-ares
Version:        1.34.6
Release:        2%{?dist}
Group:          System Environment/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://c-ares.org/
Source0:        https://github.com/c-ares/c-ares/releases/download/v%{version}/%{name}-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  cmake
BuildRequires:  ninja-build

%description
c-ares is a C library that performs DNS requests and name resolves
asynchronously. c-ares is a fork of the library named 'ares', written
by Greg Hudson at MIT.

%package devel
Summary: Development files for c-ares
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: pkg-config

%description devel
This package contains the header files and libraries needed to
compile applications or shared objects that use c-ares.

%package doc
Summary: Doc amd man page files for c-ares
Conflicts: %{name} < 1.34.6-1

%description doc
This package contains doc files and man pages for c-ares.

%prep
%autosetup -p1

%build
%{cmake} -G Ninja \
    -DCMAKE_BUILD_TYPE=Release \
    -DCARES_SHARED=ON \
    -DCARES_STATIC=OFF \
    -DCARES_BUILD_TESTS=OFF \
    -DCMAKE_INSTALL_LIBDIR=%{_libdir}

%{cmake_build}

%install
%{cmake_install}

%clean
rm -rf %{buildroot}

%ldconfig_scriptlets

%files
%defattr(-, root, root)
%{_bindir}/adig
%{_bindir}/ahost
%{_libdir}/*.so.*

%files devel
%defattr(-, root, root, 0755)
%{_includedir}/ares.h
%{_includedir}/ares_build.h
%{_includedir}/ares_dns.h
%{_includedir}/ares_dns_record.h
%{_includedir}/ares_nameser.h
%{_includedir}/ares_version.h
%{_libdir}/*.so
%{_libdir}/pkgconfig/libcares.pc
%dir %{_libdir}/cmake/c-ares
%{_libdir}/cmake/c-ares/*

%files doc
%defattr(-, root, root, 0755)
%doc README.md README.msvc RELEASE-NOTES.md
%{_mandir}/man3/ares_*
%{_mandir}/man1/adig.1*
%{_mandir}/man1/ahost.1*

%changelog
* Fri May 15 2026 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 1.34.6-2
- Extended to build for subrelease 91 and above
* Mon Apr 6 2026 Harinadh Dommaraju <Harinadh.Dommaraju@broadcom.com> 1.34.6-1
- Upgrade to 1.34.6, switch to CMake build system
* Thu Dec 12 2024 HarinadhD <harinadh.dommaraju@broadcom.com> 1.19.1-3
- Release bump for SRP compliance
* Wed Feb 28 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 1.19.1-2
- Fix CVE-2024-25629
* Tue May 23 2023 Prashant S Chauhan <psinghchauha@vmware.com> 1.19.1-1
- Update to 1.19.1, Fixes multiple CVEs
* Wed Apr 27 2022 Prashant S Chauhan <psinghchauha@vmware.com> 1.18.1-1
- Version update to 1.18.1
* Mon Aug 09 2021 Prashant S Chauhan <psinghchauha@vmware.com> 1.17.1-2
- Fix CVE-2021-3672
* Mon Apr 12 2021 Gerrit Photon <photon-checkins@vmware.com> 1.17.1-1
- Automatic Version Bump
* Mon Jun 22 2020 Gerrit Photon <photon-checkins@vmware.com> 1.16.1-1
- Automatic Version Bump
* Fri Sep 21 2018 Sujay G <gsujay@vmware.com> 1.14.0-1
- Bump c-ares version to 1.14.0
* Fri Sep 29 2017 Dheeraj Shetty <dheerajs@vmware.com>  1.12.0-2
- Fix for CVE-2017-1000381
* Fri Apr 07 2017 Anish Swaminathan <anishs@vmware.com>  1.12.0-1
- Upgrade to 1.12.0
* Wed Oct 05 2016 Xiaolin Li <xiaolinl@vmware.com> 1.10.0-3
- Apply patch for CVE-2016-5180.
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.10.0-2
- GA - Bump release of all rpms
* Wed Feb 03 2016 Anish Swaminathan <anishs@vmware.com> - 1.10.0-1
- Initial version
