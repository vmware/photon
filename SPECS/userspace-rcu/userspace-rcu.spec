Summary:        user space RCU (read-copy-update)
Name:           userspace-rcu
Version:        0.12.1
Release:        1%{?dist}
License:        LGPLv2+
URL:            https://github.com/urcu/userspace-rcu/releases
Source:         %{name}-%{version}.tar.gz
%define         sha1 userspace-rcu=20bc93b4b1aecf1e69fe5d205899ee2270148d9e
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
%setup -q

%build
autoreconf -fiv
./configure \
    --prefix=%{_prefix} \
    --disable-static

make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install
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
