%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%define _python3_sitearch %(python3 -c "from distutils.sysconfig import get_python_lib; import sys; sys.stdout.write(get_python_lib(1))")

Summary:        Repodata downloading library
Name:           librepo
Version:        1.14.2
Release:        1%{?dist}
License:        LGPLv2+
URL:            https://github.com/rpm-software-management/librepo
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://github.com/rpm-software-management/librepo/archive/%{name}-%{version}.tar.gz
%define sha1    %{name}-%{version}=c9f39d7497d310ae220df2dfbd8e95f347e2bc8c
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  check
BuildRequires:  glib-devel
BuildRequires:  gpgme-devel
BuildRequires:  attr-devel
BuildRequires:  curl-devel
BuildRequires:  libxml2-devel
BuildRequires:  openssl-devel
BuildRequires:  zchunk-devel
BuildRequires:  python3-devel
BuildRequires:  python3-sphinx

Requires:   python3-packaging
Requires:   curl-libs
Requires:   gpgme
Requires:   zchunk
Requires:   python3-sphinx

%description
A library providing C and Python (libcURL like) API to downloading repository
metadata.

%package devel
Summary:        Repodata downloading library
Requires:       curl-libs
Requires:       curl-devel
Requires:       %{name} = %{version}-%{release}

%description devel
Development files for librepo.

%package -n python3-librepo
Summary:        Python 3 bindings for the librepo library
Provides:       python3-librepo
Requires:       %{name} = %{version}-%{release}

%description -n python3-librepo
Python 3 bindings for the librepo library.

%prep
%autosetup -p1
mkdir build-py3

%build
pushd build-py3
%cmake -DPYTHON_DESIRED:FILEPATH=/usr/bin/python3 -DENABLE_PYTHON_TESTS=%{!?with_pythontests:OFF} ..
make %{?_smp_mflags}
popd

%install
pushd build-py3
make DESTDIR=%{buildroot} install %{?_smp_mflags}
popd

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc COPYING
%doc README.md
%{_libdir}/%{name}.so.*

%files devel
%{_libdir}/%{name}.so
%{_libdir}/pkgconfig/%{name}.pc
%{_includedir}/%{name}/

%files -n python3-librepo
%{_python3_sitearch}/%{name}/

%changelog
*   Sat Aug 28 2021 Ankit Jain <ankitja@vmware.com> 1.14.2-1
-   Updated to 1.14.2
*   Tue Dec 15 2020 Shreenidhi Shedi <sshedi@vmware.com> 1.12.1-4
-   Fix build with new rpm
*   Tue Sep 29 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 1.12.1-3
-   openssl 1.1.1
*   Mon Sep 07 2020 Ankit Jain <ankitja@vmware.com> 1.12.1-2
-   Fixed string parsing logic
*   Fri Aug 28 2020 Gerrit Photon <photon-checkins@vmware.com> 1.12.1-1
-   Automatic Version Bump
*   Thu Aug 13 2020 Ankit Jain <ankitja@vmware.com> 1.12.0-1
-   Updated to 1.12.0
*   Mon Jun 15 2020 Tapas Kundu <tkundu@vmware.com> 1.10.2-3
-   Mass removal python2
*   Thu Oct 24 2019 Ankit Jain <ankitja@vmware.com> 1.10.2-2
-   Added for ARM Build
*   Wed May 15 2019 Ankit Jain <ankitja@vmware.com> 1.10.2-1
-   Initial build. First version
