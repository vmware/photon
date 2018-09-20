Summary:    A minimalistic user-space library oriented to Netlink developers.
Name:       libmnl
Version:    1.0.4
Release:    3%{?dist}
License:    LGPLv2.1+
URL:        http://netfilter.org/projects/libmnl
Group:      System Environment/libraries
Vendor:     VMware, Inc.
Distribution: Photon
Source0:     http://netfilter.org/projects/libmnl/files/%{name}-%{version}.tar.bz2
%define sha1 libmnl=2db40dea612e88c62fd321906be40ab5f8f1685a
Obsoletes:  libmnl-static
%description
libmnl is a minimalistic user-space library oriented to Netlink developers. There are a lot of common tasks in parsing, validating, constructing of both the Netlink header and TLVs that are repetitive and easy to get wrong. This library aims to provide simple helpers that allows you to re-use code and to avoid re-inventing the wheel.

%package devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       libmnl >= 1.0.4
%description devel
Libraries and header files for libnml library.

%prep
%setup -q

%build
%configure --enable-static=no
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}

%check
make %{?_smp_mflags} -k check

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_libdir}/libmnl.so.*

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/libmnl.so
%{_libdir}/libmnl.la
%{_libdir}/pkgconfig/*

%changelog
*   Mon Sep 17 2018 Bo Gan <ganb@vmware.com> 1.0.4-3
-   Cleanup spec file
*   Wed Jul 5 2017 Divya Thaluru <dthaluru@vmware.com> 1.0.4-2
-   Added obsoletes for libmnl-static package which is deprecated
*   Wed Aug 3 2016 Xiaolin Li <xiaolinl@vmware.com> 1.0.4-1
-   Initial build.	First version
