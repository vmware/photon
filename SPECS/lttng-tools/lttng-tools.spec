%global build_if %{photon_subrelease} >= 91

Summary:       LTTng is an open source tracing framework for Linux.
Name:          lttng-tools
Version:       2.15.0
Release:       2%{?dist}
URL:           https://github.com/lttng/lttng-tools
Group:         Development/Tools
Vendor:        VMware, Inc.
Distribution:  Photon

Source0: %{name}-%{version}.tar.bz2

Source1: license.txt
%include %{SOURCE1}

BuildRequires: libxml2-devel
BuildRequires: nss-devel
BuildRequires: m4
BuildRequires: elfutils-devel
BuildRequires: popt-devel
BuildRequires: userspace-rcu-devel
BuildRequires: lttng-ust-devel
BuildRequires: zlib-devel

Requires:   userspace-rcu >= 0.15.6
Requires:   popt
Requires:   lttng-ust-libs
Requires:   %{name}-libs = %{version}-%{release}

%description
LTTng is an open source tracing framework for Linux.

%package libs
Summary:    Library files for %{name}
Requires:   libxml2
Requires:   zlib
Conflicts:  %{name} < 2.15.0

%description libs
%{summary}

%package devel
Summary:    Development headers for %{name}
Requires:   %{name} = %{version}-%{release}
Conflicts:  %{name} < 2.15.0

%description devel
%{summary}

%package doc
Summary:    Documentation for %{name}
Requires:   %{name} = %{version}-%{release}
Conflicts:  %{name} < 2.15.0

%description doc
%{summary}

%prep
%autosetup -p1

%build
autoreconf -fiv
%configure \
    --disable-static \
    --disable-tests

%make_build

%install
%make_install %{?_smp_mflags}
find %{buildroot} -name '*.la' -delete

%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_bindir}/*

%files libs
%defattr(-,root,root)
%{_libdir}/*.so.*
%{_libdir}/lttng/*
%{_datadir}/xml/*

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*
%exclude %dir %{_libdir}/debug

%files doc
%defattr(-,root,root)
%{_mandir}/*
%{_docdir}/*

%changelog
* Wed Jun 03 2026 Harinadh Dommaraju <Harinadh.Dommaraju@broadcom.com> 2.15.0-2
- Release version bump as part of libxml2/libxslt
* Fri May 29 2026 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 2.15.0-1
- Upgrade to v2.15.0
* Wed May 20 2026 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 2.13.8-4
- Build for all subreleases
* Thu May 14 2026 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 2.13.8-3.1.1
- Bump after moving to SPECS/90
* Tue May 12 2026 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 2.13.8-3.1
- Bump after moving to SPECS/90
* Thu Dec 12 2024 Ajay Kaher <ajay.kaher@broadcom.com> 2.13.8-3
- Release bump for SRP compliance
* Thu May 25 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 2.13.8-2
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
