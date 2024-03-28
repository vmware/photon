Summary:        Repodata downloading library
Name:           librepo
Version:        1.14.5
Release:        7%{?dist}
License:        LGPLv2+
URL:            https://github.com/rpm-software-management/librepo
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://github.com/rpm-software-management/librepo/archive/%{name}-%{version}.tar.gz
%define sha512 %{name}-%{version}=9dda5067142b04e46e8ee344a47df21dae89a9c26e91588fc92bcbaee5291348a38ee79a5e807d7a8cba6cb13af78985e8b2e9b23d7f9eabecd0123459c43935

BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  check-devel
BuildRequires:  glib-devel
BuildRequires:  gpgme-devel
BuildRequires:  attr-devel
BuildRequires:  curl-devel
BuildRequires:  libxml2-devel
BuildRequires:  openssl-devel
BuildRequires:  zchunk-devel
BuildRequires:  python3-devel
BuildRequires:  python3-sphinx

%if 0%{?with_check}
BuildRequires:  python3-pip
%endif

Requires:   curl-libs
Requires:   gpgme
Requires:   zchunk

%description
A library providing C and Python (libcURL like) API to downloading repository
metadata.

%package devel
Summary:        Repodata downloading library
Requires:       curl-devel
Requires:       glib-devel
Requires:       libxml2-devel
Requires:       %{name} = %{version}-%{release}

%description devel
Development files for librepo.

%package -n python3-librepo
Summary:        Python 3 bindings for the librepo library
Provides:       python3-librepo
Requires:       %{name} = %{version}-%{release}
Requires:       python3-packaging
Requires:       python3-sphinx

%description -n python3-librepo
Python 3 bindings for the librepo library.

%prep
%autosetup -p1

%build
%cmake \
    -DCMAKE_BUILD_TYPE=Debug \
    -DENABLE_PYTHON=ON \
    -DCMAKE_INSTALL_LIBDIR=%{_libdir} \
    -DCMAKE_INSTALL_PREFIX=%{_prefix} \
    -DENABLE_TESTS=ON

%cmake_build

%install
%cmake_install

%if 0%{?with_check}
%check
pip3 install pygpgme xattr
%ctest
%endif

%clean
rm -rf %{buildroot}/*

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%doc COPYING
%doc README.md
%{_libdir}/%{name}.so.*

%files devel
%defattr(-,root,root)
%{_libdir}/%{name}.so
%{_libdir}/pkgconfig/%{name}.pc
%{_includedir}/%{name}/

%files -n python3-librepo
%defattr(-,root,root)
%{python3_sitearch}/%{name}/

%changelog
* Thu Mar 28 2024 Ashwin Dayanand Kamat <ashwin.kamat@broadcom.com> 1.14.5-7
- Bump version as a part of libxml2 upgrade
* Tue Feb 20 2024 Ashwin Dayanand Kamat <ashwin.kamat@broadcom.com> 1.14.5-6
- Bump version as a part of libxml2 upgrade
* Sun Nov 19 2023 Shreenidhi Shedi <sshedi@vmware.com> 1.14.5-5
- Bump version as a part of openssl upgrade
* Fri Sep 29 2023 Shreenidhi Shedi <sshedi@vmware.com> 1.14.5-4
- Fix devel package requires
* Wed Apr 19 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 1.14.5-3
- Bump version as a part of libxml2 upgrade
* Tue Dec 06 2022 Prashant S Chauhan <psinghchauha@vmware.com> 1.14.5-2
- Update release to compile with python 3.11
* Fri Oct 07 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.14.5-1
- Upgrade to v1.14.5
* Fri Jun 17 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.14.2-3
- Fix build with latest cmake
* Mon Nov 08 2021 Satya Naga Vasamsetty <svasamsetty@vmware.com> 1.14.2-2
- openssl 3.0.0 compatibility
* Mon Oct 18 2021 Shreenidhi Shedi <sshedi@vmware.com> 1.14.2-1
- Bump to verion 1.14.2
* Fri Sep 24 2021 Nitesh Kumar <kunitesh@vmware.com> 1.12.1-5
- Remove python dependencies.
* Tue Dec 15 2020 Shreenidhi Shedi <sshedi@vmware.com> 1.12.1-4
- Fix build with new rpm
* Tue Sep 29 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 1.12.1-3
- openssl 1.1.1
* Mon Sep 07 2020 Ankit Jain <ankitja@vmware.com> 1.12.1-2
- Fixed string parsing logic
* Fri Aug 28 2020 Gerrit Photon <photon-checkins@vmware.com> 1.12.1-1
- Automatic Version Bump
* Thu Aug 13 2020 Ankit Jain <ankitja@vmware.com> 1.12.0-1
- Updated to 1.12.0
* Mon Jun 15 2020 Tapas Kundu <tkundu@vmware.com> 1.10.2-3
- Mass removal python2
* Thu Oct 24 2019 Ankit Jain <ankitja@vmware.com> 1.10.2-2
- Added for ARM Build
* Wed May 15 2019 Ankit Jain <ankitja@vmware.com> 1.10.2-1
- Initial build. First version
