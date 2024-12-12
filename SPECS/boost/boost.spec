%define main_version 1_80_0
Summary:        Boost
Name:           boost
Version:        1.80.0
Release:        2%{?dist}
URL:            http://www.boost.org
Group:          System Environment/Security
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://boostorg.jfrog.io/artifactory/main/release/%{version}/source/boost_%{main_version}.tar.bz2
%define sha512  boost=829a95b463473d69ff79ea41799c68429bb79d3b2321fbdb71df079af237ab01de9ad7e9612d8783d925730acada010068d2d1aa856c34244ee5c0ece16f208f

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  bzip2-devel

%description
Boost provides a set of free peer-reviewed portable C++ source libraries.
It includes libraries for linear algebra, pseudorandom number generation,
multithreading, image processing, regular expressions and unit testing.

%package        devel
Summary:        Development files for boost
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description    devel
The boost-devel package contains libraries, header files and documentation for developing applications that use boost.

%package        static
Summary:        boost static libraries
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description    static
The boost-static package contains boost static libraries.

%prep
%autosetup -p1 -n boost_%{main_version}

%build
./bootstrap.sh --prefix=%{buildroot}%{_prefix}
./b2 %{?_smp_mflags} stage threading=multi

%install
./b2 install threading=multi

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_libdir}/libboost_*.so.*
%{_libdir}/cmake/*.cmake
%{_libdir}/cmake/*/*.cmake

%files devel
%defattr(-,root,root)
%{_includedir}/boost/*
%{_libdir}/libboost_*.so

%files static
%defattr(-,root,root)
%{_libdir}/libboost_*.a

%changelog
* Thu Dec 12 2024 HarinadhD <harinadh.dommaraju@broadcom.com> 1.80.0-2
- Release bump for SRP compliance
* Fri Aug 19 2022 Ajay Kaher <akaher@vmware.com> 1.80.0-1
- Version update
* Mon Apr 12 2021 Gerrit Photon <photon-checkins@vmware.com> 1.76.0-1
- Automatic Version Bump
* Fri Aug 28 2020 Gerrit Photon <photon-checkins@vmware.com> 1.74.0-1
- Automatic Version Bump
* Tue Sep 11 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 1.66.0-1
- Update to version 1.66.0
* Thu Apr 06 2017 Anish Swaminathan <anishs@vmware.com> 1.63.0-1
- Upgraded to version 1.63.0
* Thu Mar 23 2017 Vinay Kulkarni <kulkarniv@vmware.com> 1.60.0-3
- Build static libs in additon to shared.
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.60.0-2
- GA - Bump release of all rpms
* Wed Apr 27 2016 Xiaolin Li <xiaolinl@vmware.com> 1.60.0-1
- Update to version 1.60.0.
* Thu Oct 01 2015 Xiaolin Li <xiaolinl@vmware.com> 1.56.0-2
- Move header files to devel package.
* Tue Feb 10 2015 Divya Thaluru <dthaluru@vmware.com> 1.56.0-1
- Initial build. First version
