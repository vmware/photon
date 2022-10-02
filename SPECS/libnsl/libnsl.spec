Summary:        Libraries for the public client interface for NIS(YP) and NIS+.
Name:           libnsl
Version:        1.3.0
Release:        2%{?dist}
License:        GPLv2+
Group:          System Environment/Libraries
URL:            https://github.com/thkukuk/libnsl
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://github.com/thkukuk/libnsl/archive/v%{version}/libnsl-%{version}.tar.gz
%define sha512  %{name}=ce75ee9e54f1bdd2b31886e8157ff5f654511c3da017e0d9f8d0da6a2a9f9a78ff2e5f72cfb7ce3a23065f57337db51e3c8842a7e990350a62612018f4960342

Requires:       libtirpc
Requires:       rpcsvc-proto

BuildRequires:  libtirpc-devel
BuildRequires:  rpcsvc-proto-devel

%description
The libnsl package contains the public client interface for NIS(YP) and NIS+.
It replaces the NIS library that used to be in glibc.

%package    devel
Summary:    Development files for the libnsl library
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}
Requires:   libtirpc-devel
Requires:   rpcsvc-proto-devel

%description    devel
This package includes header files and libraries necessary for developing programs which use the nsl library.

%prep
%autosetup -p1

%build
autoreconf -fi
%configure $(test %{_host} != %{_build} && echo "--with-sysroot=/target-%{_arch}")
make %{?_smp_mflags}

%install
%make_install %{?_smp_mflags}

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%defattr(-,root,root)
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root)
%{_includedir}/rpcsvc/*
%{_libdir}/pkgconfig/*
%{_libdir}/*.a
%{_libdir}/*.so

%changelog
* Sun Oct 02 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.3.0-2
- Remove .la files
* Tue Sep 29 2020 Gerrit Photon <photon-checkins@vmware.com> 1.3.0-1
- Automatic Version Bump
* Thu Nov 15 2018 Alexey Makhalov <amakhalov@vmware.com> 1.2.0-2
- Cross compilation support
* Fri Sep 21 2018 Alexey Makhalov <amakhalov@vmware.com> 1.2.0-1
- Initial version
