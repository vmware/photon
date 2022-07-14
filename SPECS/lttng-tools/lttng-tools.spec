Summary:       LTTng is an open source tracing framework for Linux.
Name:          lttng-tools
Version:       2.12.11
Release:       1%{?dist}
License:       GPLv2 and LGPLv2
URL:           https://lttng.org/download
Group:         Development/Tools
Vendor:        VMware, Inc.
Distribution:  Photon

Source:        %{name}-%{version}.tar.bz2
%define sha512 %{name}=c1ff07831508848ede2a69a4350ba6eeef2b9bea0faa9de4a3d9e8a0df81e22258d25131ccab57d1800fcac239a4bc25aa66d5d421d9e5c76d7cb6b9794ae4cd
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
autoreconf -fiv
%configure
%make_build

%install
%make_install %{?_smp_mflags}
find %{buildroot} -name '*.la' -delete

%files
%{_bindir}/*
%{_includedir}/*
%{_libdir}/liblttng*
%{_libdir}/lttng/*
%{_libdir}/pkgconfig/*
%{_datadir}/*
%exclude %dir %{_libdir}/debug

%changelog
* Mon Jul 11 2022 Gerrit Photon <photon-checkins@vmware.com> 2.12.11-1
- Automatic Version Bump to 2.12.11 for lttng-ust 2.12.*
* Mon Jul 11 2022 Gerrit Photon <photon-checkins@vmware.com> 2.13.7-1
- Automatic Version Bump
* Mon Feb 28 2022 Shreenidhi Shedi <sshedi@vmware.com> 2.12.3-3
- Fix binary path
* Wed Nov 17 2021 Nitesh Kumar <kunitesh@vmware.com> 2.12.3-2
- Release bump up to use libxml2 2.9.12-1.
* Tue Apr 13 2021 Gerrit Photon <photon-checkins@vmware.com> 2.12.3-1
- Automatic Version Bump
* Wed Aug 19 2020 Gerrit Photon <photon-checkins@vmware.com> 2.12.2-1
- Automatic Version Bump
* Mon Jun 22 2020 Gerrit Photon <photon-checkins@vmware.com> 2.12.1-1
- Automatic Version Bump
* Tue Mar 24 2020 Alexey Makhalov <amakhalov@vmware.com> 2.10.5-2
- Fix compilation issue with glibc >= 2.30.
* Wed Sep 05 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 2.10.5-1
- Update to version 2.10.5
* Fri Mar 31 2017 Michelle Wang <michellew@vmware.com> 2.9.4-1
- Update package version
* Tue Jul 26 2016 Divya Thaluru <dthaluru@vmware.com> 2.7.1-3
- Added userspace-rcu-devel as build time dependent package
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.7.1-2
- GA - Bump release of all rpms
* Thu Jan 28 2016 Xiaolin Li <xiaolinl@vmware.com> 2.7.1-1
- Updated to version 2.7.1
* Tue Nov 24 2015 Xiaolin Li <xiaolinl@vmware.com> 2.7.0-1
- Initial build.  First version
