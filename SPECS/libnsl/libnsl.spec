Summary:        Libraries for the public client interface for NIS(YP) and NIS+.
Name:           libnsl
Version:        2.0.0
Release:        1%{?dist}
Source0:        https://github.com/thkukuk/libnsl/archive/v%{version}/libnsl-%{version}.tar.gz
%define sha512  libnsl=86a7738707a3e4e56b60c8de0445fb576e66148bc12fa2a6aab422ea81eb4b42be3287a12f78384acd2b8bfb3885e9a0ce4f7328f078da3a5099acb66a35a935
License:        GPLv2+
Group:          System Environment/Libraries
URL:            https://github.com/thkukuk/libnsl
Vendor:         VMware, Inc.
Distribution:   Photon
Requires:       libtirpc
Requires:       rpcsvc-proto
BuildRequires:  libtirpc-devel
BuildRequires:  rpcsvc-proto-devel

%description
The libnsl package contains the public client interface for NIS(YP) and NIS+.
It replaces the NIS library that used to be in glibc.

%package        devel
Summary:        Development files for the libnsl library
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       libtirpc-devel
Requires:       rpcsvc-proto-devel

%description    devel
This package includes header files and libraries necessary for developing programs which use the nsl library.

%prep
%autosetup

%build
autoreconf -fi
%configure $(test %{_host} != %{_build} && echo "--with-sysroot=/target-%{_arch}")
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot} %{?_smp_mflags}

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%{_libdir}/*.so
%{_libdir}/*.so.*

%files devel
%{_includedir}/rpcsvc/*
%{_libdir}/pkgconfig/*
%{_libdir}/*.a
%{_libdir}/*.la

%changelog
* Mon Apr 18 2022 Gerrit Photon <photon-checkins@vmware.com> 2.0.0-1
- Automatic Version Bump
* Tue Sep 29 2020 Gerrit Photon <photon-checkins@vmware.com> 1.3.0-1
- Automatic Version Bump
* Thu Nov 15 2018 Alexey Makhalov <amakhalov@vmware.com> 1.2.0-2
- Cross compilation support
* Fri Sep 21 2018 Alexey Makhalov <amakhalov@vmware.com> 1.2.0-1
- Initial version.
