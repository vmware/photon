Summary:        Repodata downloading library
Name:           librepo
Version:        1.14.2
Release:        7%{?dist}
License:        LGPLv2+
URL:            https://github.com/rpm-software-management/librepo
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://github.com/rpm-software-management/librepo/archive/%{name}-%{version}.tar.gz
%define sha512 %{name}-%{version}=cbed7b6ab551366cc9cf9b5e8ac90cfc7395f6e79a1b44b1dcbf1e3ed6edcc644a339cca4efb4560d139355a893d00b6ac1b2e7116478f5bff3c8bfa5fdeb950

BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  check-devel
BuildRequires:  glib-devel >= 2.68.4
BuildRequires:  gpgme-devel
BuildRequires:  attr-devel
BuildRequires:  curl-devel
BuildRequires:  libxml2-devel
BuildRequires:  openssl-devel
BuildRequires:  zchunk-devel
BuildRequires:  python3-devel
BuildRequires:  python3-sphinx

Requires:   curl-libs
Requires:   glib >= 2.68.4
Requires:   libxml2
Requires:   gpgme
Requires:   zchunk
Requires:   openssl

%description
A library providing C and Python (libcURL like) API to downloading repository
metadata.

%package devel
Summary:        Repodata downloading library
Requires:       curl-libs
Requires:       curl-devel
Requires:       libxml2-devel
Requires:       glib-devel >= 2.68.4
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
* Sat Oct 07 2023 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 1.14.2-7
- Bump version as part of glib upgrade
* Mon May 29 2023 Harinadh D <hdommaraju@vmware.com> 1.14.2-6
- Version bump to use curl 8.1.1
* Fri Mar 24 2023 Harinadh D <hdommaraju@vmware.com> 1.14.2-5
- Version bump to use curl 8.0.1
* Thu Dec 09 2021 Prashant S Chauhan <psinghchauha@vmware.com> 1.14.2-4
- Bump up to compile with python 3.10
* Mon Nov 08 2021 Satya Naga Vasamsetty <svasamsetty@vmware.com> 1.14.2-3
- openssl 3.0.0 compatibility
* Tue Sep 21 2021 Nitesh Kumar <kunitesh@vmware.com> 1.14.2-2
- Remove python dependencies.
* Sat Aug 28 2021 Ankit Jain <ankitja@vmware.com> 1.14.2-1
- Updated to 1.14.2
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
