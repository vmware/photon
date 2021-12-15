Summary: LTTng is an open source tracing framework for Linux.
Name:    lttng-tools
Version: 2.10.9
Release: 2%{?dist}
License: GPLv2 and LGPLv2
URL: https://lttng.org/download/
Source: %{name}-%{version}.tar.bz2
%define sha1 lttng-tools=36c4d2b401b286f62fd742dbbd983635e4ae2b50
Group:      Development/Tools
Vendor:     VMware, Inc.
Distribution:  Photon

BuildRequires: libxml2-devel >= 2.7.6
BuildRequires: nss-devel
BuildRequires: m4
BuildRequires: elfutils-devel
BuildRequires: popt-devel
BuildRequires: userspace-rcu-devel >= 0.8.0
BuildRequires: lttng-ust-devel >= 2.9.0
Requires:      userspace-rcu
Requires:      elfutils
Requires:      nss
Requires:      libxml2
%description
LTTng is an open source tracing framework for Linux.

%prep
%autosetup -p1

%build
%configure --disable-lttng-ust

make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install %{?_smp_mflags}
find %{buildroot} -name '*.la' -delete

%files
%{_bindir}/*
%{_includedir}/*
%{_lib}/*
%{_datadir}/*
%exclude %{_libdir}/debug

%changelog
*   Thu Nov 18 2021 Nitesh Kumar <kunitesh@vmware.com> 2.10.9-2
-   Version bump up to use libxml2 2.9.11-4.
*   Mon Dec 14 2020 Gerrit Photon <photon-checkins@vmware.com> 2.10.9-1
-   Automatic Version Bump
*   Wed Sep 05 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 2.10.5-1
-   Update to version 2.10.5
*   Fri Mar 31 2017 Michelle Wang <michellew@vmware.com> 2.9.4-1
-   Update package version
*   Tue Jul 26 2016 Divya Thaluru <dthaluru@vmware.com> 2.7.1-3
-   Added userspace-rcu-devel as build time dependent package
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.7.1-2
-   GA - Bump release of all rpms
*   Thu Jan 28 2016 Xiaolin Li <xiaolinl@vmware.com> 2.7.1-1
-   Updated to version 2.7.1
*   Tue Nov 24 2015 Xiaolin Li <xiaolinl@vmware.com> 2.7.0-1
-   Initial build.  First version
