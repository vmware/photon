Summary:        fork of the original IJG libjpeg which uses SIMD.
Name:           libjpeg-turbo
Version:        2.1.4
Release:        2%{?dist}
License:        IJG
URL:            http://sourceforge.net/projects/libjpeg-turbo
Group:          System Environment/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        http://downloads.sourceforge.net/libjpeg-turbo/%{name}-%{version}.tar.gz
%define sha512  %{name}=511f065767c022da06b6c36299686fa44f83441646f7e33b766c6cfab03f91b0e6bfa456962184071dadaed4057ba9a29cba685383f3eb86a4370a1a53731a70

%ifarch x86_64
BuildRequires:  nasm
%endif

BuildRequires:  cmake

%description
libjpeg-turbo is a fork of the original IJG libjpeg which uses SIMD to accelerate baseline JPEG compression and decompression.
libjpeg is a library that implements JPEG image encoding, decoding and transcoding.

%package        devel
Summary:        Header and development files
Requires:       %{name} = %{version}-%{release}

%description    devel
It contains the libraries and header files to create applications

%prep
%autosetup -p1

%build
%cmake -DCMAKE_SKIP_RPATH:BOOL=YES \
       -DCMAKE_BUILD_TYPE=Debug \
       -DCMAKE_SKIP_INSTALL_RPATH:BOOL=YES \
       -DCMAKE_INSTALL_LIBDIR=%{_libdir} \
       -DENABLE_STATIC:BOOL=NO

%cmake_build

%install
%cmake_install
find %{buildroot} -name "*.la" -delete

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/*.so.*
%{_datadir}/*

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/cmake/*
%{_libdir}/pkgconfig/*.pc

%changelog
* Mon Apr 17 2023 Nitesh Kumar <kunitesh@vmware.com> 2.1.4-2
- Bump version as a part of nasm v2.16.01 upgrade
* Wed Aug 17 2022 Gerrit Photon <photon-checkins@vmware.com> 2.1.4-1
- Automatic Version Bump
* Fri Jun 17 2022 Shreenidhi Shedi <sshedi@vmware.com> 2.1.3-2
- Fix build with latest cmake
* Mon Apr 18 2022 Gerrit Photon <photon-checkins@vmware.com> 2.1.3-1
- Automatic Version Bump
* Fri Apr 23 2021 Gerrit Photon <photon-checkins@vmware.com> 2.1.0-1
- Automatic Version Bump
* Tue Apr 13 2021 Gerrit Photon <photon-checkins@vmware.com> 2.0.6-1
- Automatic Version Bump
* Wed Jul 08 2020 Gerrit Photon <photon-checkins@vmware.com> 2.0.5-1
- Automatic Version Bump
* Mon Mar 04 2019 Keerthana K <keerthanak@vmware.com> 2.0.0-4
- Update BuildRequires nasm only for x86_64.
* Wed Feb 06 2019 Sujay G <gsujay@vmware.com> 2.0.0-3
- Added patch to fix CVE-2018-19664
* Thu Jan 10 2019 Sujay G <gsujay@vmware.com> 2.0.0-2
- Added patch to fix CVE-2018-20330
* Thu Sep 20 2018 Bo Gan <ganb@vmware.com> 2.0.0-1
- Update to 2.0.0
- cmake build system
* Mon Dec 11 2017 Xiaolin Li <xiaolinl@vmware.com> 1.5.2-2
- Fix CVE-2017-15232
* Wed Aug 09 2017 Dheeraj Shetty <dheerajs@vmware.com> 1.5.2-1
- Updated to version 1.5.2
* Tue Apr 11 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 1.5.1-1
- Updated to version 1.5.1
* Wed Jul 27 2016 Divya Thaluru <dthaluru@vmware.com> 1.5.0-1
- Initial version.
