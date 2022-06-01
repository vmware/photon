Summary:        user space RCU (read-copy-update)
Name:           userspace-rcu
Version:        0.13.1
Release:        1%{?dist}
License:        LGPLv2+
URL:            https://github.com/urcu/userspace-rcu/releases
Source:         %{name}-%{version}.tar.gz
%define sha512  userspace-rcu=6534b7c5246f23680abe3b5db244e37f2365bcf93be655701046ef69781dea26230e06ec61c49880ae3742d31ca1b8d6d57962f70e5835ff928bc8711c010c9d
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon

BuildRequires:  libxml2-devel
BuildRequires:  nss-devel
BuildRequires:  m4
BuildRequires:  elfutils-devel
BuildRequires:  popt-devel

%description
This data synchronization library provides read-side access which scales linearly with the number of cores.

%package devel
Summary: Development Libraries for openssl
Group: Development/Libraries
Requires: userspace-rcu = %{version}-%{release}
%description devel
Library files for doing development with userspace-rcu.

%prep
%autosetup

%build
autoreconf -fiv
%configure \
    --disable-static
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} %{?_smp_mflags} install
find %{buildroot} -name '*.la' -delete

%check
make %{?_smp_mflags} check

%files
%{_lib}/*.so.*
%{_includedir}/*
%{_datadir}/*

%files devel
%defattr(-,root,root)
%{_libdir}/pkgconfig/*
%{_libdir}/*.so
%{_includedir}/*

%changelog
*   Wed Jun 01 2022 Gerrit Photon <photon-checkins@vmware.com> 0.13.1-1
-   Automatic Version Bump
*   Mon Jun 22 2020 Gerrit Photon <photon-checkins@vmware.com> 0.12.1-1
-   Automatic Version Bump
*   Mon Sep 10 2018 Michelle Wang <michellew@vmware.com> 0.10.1-1
-   Updated to version 0.10.1.
*   Wed Apr 05 2017 Xiaolin Li <xiaolinl@vmware.com> 0.9.3-1
-   Updated to version 0.9.3.
*   Wed Oct 05 2016 ChangLee <changlee@vmware.com> 0.9.1-4
-   Modified %check
*   Mon Jul 25 2016 Divya Thaluru <dthaluru@vmware.com> 0.9.1-3
-   Added devel package and removed packaging of debug files
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.9.1-2
-   GA - Bump release of all rpms
*   Tue Nov 24 2015 Xiaolin Li <xiaolinl@vmware.com> 2.7.0-1
-   Initial build.  First version
