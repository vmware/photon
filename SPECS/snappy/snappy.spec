Summary:    Fast compression and decompression library
Name:       snappy
Version:    1.1.9
Release:    1%{?dist}
License:    BSD and LGPLv2 and Sleepycat
URL:        http://code.google.com/p/snappy
Group:      System/Libraries
Vendor:     VMware, Inc.
Distribution:   Photon

Source0: https://github.com/google/%{name}/archive/%{name}-%{version}.tar.gz
%define sha512 %{name}=f1f8a90f5f7f23310423574b1d8c9acb84c66ea620f3999d1060395205e5760883476837aba02f0aa913af60819e34c625d8308c18a5d7a9c4e190f35968b024

Patch0: snappy-inline.patch
Patch1: snappy-thirdparty.patch

BuildRequires: cmake
BuildRequires: gtest-devel
BuildRequires: google-benchmark-devel

%description
Snappy is a compression/decompression library. It does not aim for maximum
compression, or compatibility with any other compression library; instead, it
aims for very high speeds and reasonable compression. For instance, compared to
the fastest mode of zlib, Snappy is an order of magnitude faster for most
inputs, but the resulting compressed files are anywhere from 20% to 100%
bigger.

%package    devel
Summary:    Header and development files
Requires:   %{name} = %{version}-%{release}
%description    devel
It contains the libraries and header files to create applications

%prep
%autosetup -p1

%build
%{cmake} \
    -DBUILD_SHARED_LIBS=ON \
    -DCMAKE_BUILD_TYPE=Debug \
    -DCMAKE_INSTALL_LIBDIR=%{_libdir}

%{cmake_build}

%install
%{cmake_install}

%clean
rm -rf %{buildroot}

%if 0%{?with_check}
%check
%{ctest}
%endif

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_libdir}/*.so.*
%exclude %{_libdir}/cmake

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/libsnappy.so

%changelog
* Thu Jan 12 2023 Shreenidhi Shedi <sshedi@vmware.com> 1.1.9-1
- Upgrade to v1.1.9
* Tue Jun 30 2020 Gerrit Photon <photon-checkins@vmware.com> 1.1.8-1
- Automatic Version Bump
* Wed Jan 09 2019 Michelle Wang <michellew@vmware.com> 1.1.7-2
- Fix make check for snappy.
* Wed Sep 19 2018 Srinidhi Rao <srinidhir@vmware.com> 1.1.7-1
- Updating the version to 1.1.7.
* Fri Dec 16 2016 Dheeraj Shetty <Dheerajs@vmware.com> 1.1.3-1
- Initial build. First version.
