Summary:        Libraries for the public client interface for NIS(YP) and NIS+.
Name:           libnsl
Version:        1.2.0
Release:        2%{?dist}
Source0:        https://github.com/thkukuk/libnsl/archive/v1.2.0/libnsl-1.2.0.tar.gz
%define sha512 libnsl=30115aa679a04ad01f55cff9dd1890b4c41c730a9bac2adab5add9ae03a0b4687c5f4b6e3b8652ecbb074eefac8faee3f1f13ea60d42cf4432db8a575ca72cd8
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
%configure
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot} %{?_smp_mflags}

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%{_libdir}/*.so.*

%files devel
%{_libdir}/*.so
%{_includedir}/rpcsvc/*
%{_libdir}/pkgconfig/*
%{_libdir}/*.a

%changelog
* Sun Oct 02 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.2.0-2
- Remove .la files
* Fri Sep 21 2018 Alexey Makhalov <amakhalov@vmware.com> 1.2.0-1
- Initial version
