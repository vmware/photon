Summary:       LTTng is an open source tracing framework for Linux.
Name:          lttng-tools
Version:       2.13.8
Release:       6%{?dist}
License:       GPLv2 and LGPLv2
URL:           https://lttng.org/download
Group:         Development/Tools
Vendor:        VMware, Inc.
Distribution:  Photon

Source:        %{name}-%{version}.tar.bz2
%define sha512 %{name}=6daafb1fd458cfbaa7e19b3a8aaafa958116bb836f389febf7ac4035e5d7884d308a9fdefb4e9063329cb7d837853a79ddae0e263d3b58db1f87519bba2dcb3b

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
* Thu Mar 14 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 2.13.8-6
- Bump version as a part of nss upgrade
* Tue Feb 20 2024 Ashwin Dayanand Kamat <ashwin.kamat@broadcom.com> 2.13.8-5
- Bump version as a part of libxml2 upgrade
* Tue Jul 11 2023 Shreenidhi Shedi <sshedi@vmware.com> 2.13.8-4
- Bump version as a part of elfutils upgrade
* Tue May 09 2023 Shreenidhi Shedi <sshedi@vmware.com> 2.13.8-3
- Bump version as a part of nss upgrade
* Wed Apr 19 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 2.13.8-2
- Bump version as a part of libxml2 upgrade
* Tue Jan 31 2023 Gerrit Photon <photon-checkins@vmware.com> 2.13.8-1
- Automatic Version Bump
* Fri Jan 06 2023 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 2.13.7-2
- Bump up due to change in elfutils
* Sun Aug 21 2022 Gerrit Photon <photon-checkins@vmware.com> 2.13.7-1
- Automatic Version Bump
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
