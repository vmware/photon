%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%define _python3_sitearch %(python3 -c "from distutils.sysconfig import get_python_lib; import sys; sys.stdout.write(get_python_lib(1))")

Summary:        Repodata downloading library
Name:           librepo
Version:        1.10.2
Release:        6%{?dist}
License:        LGPLv2+
URL:            https://github.com/rpm-software-management/librepo
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://github.com/rpm-software-management/librepo/archive/%{name}-%{version}.tar.gz
%define sha512  %{name}-%{version}=a8b0dff4bb82890aa63006f1ba4216765cb8e59e8d994d285977bc8a8f5f71f6baf1d3070944c92848821a19182046d108837148863d898b603441ae773b703b
Patch0:         librepo-CVE-2020-14352.patch
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
BuildRequires:  python-sphinx
BuildRequires:  python2-devel
BuildRequires:  python3-devel
BuildRequires:  python3-sphinx
Requires:       curl-libs
Requires:       gpgme
Requires:       zchunk

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

%package -n python2-%{name}
Summary:        Python bindings for the librepo library
%{?python_provide:%python_provide python2-%{name}}
Requires:       %{name} = %{version}-%{release}

%description -n python2-%{name}
Python 2 bindings for the librepo library.

%package -n python3-%{name}
Summary:        Python 3 bindings for the librepo library
%{?python_provide:%python_provide python3-%{name}}
Requires:       %{name} = %{version}-%{release}

%description -n python3-%{name}
Python 3 bindings for the librepo library.

%prep
%autosetup -p1
mkdir build-py2
mkdir build-py3

%build
pushd build-py2
  %cmake -DPYTHON_DESIRED:FILEPATH=/usr/bin/python2 -DENABLE_PYTHON_TESTS=%{!?with_pythontests:OFF} ..
  make %{?_smp_mflags}
popd

pushd build-py3
  %cmake -DPYTHON_DESIRED:FILEPATH=/usr/bin/python3 -DENABLE_PYTHON_TESTS=%{!?with_pythontests:OFF} ..
  make %{?_smp_mflags}
popd

%install
pushd build-py2
  make DESTDIR=%{buildroot} install
popd

pushd build-py3
  make DESTDIR=%{buildroot} install
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

%files -n python2-%{name}
%{python_sitearch}/%{name}/

%files -n python3-%{name}
%{_python3_sitearch}/%{name}/

%changelog
* Mon May 29 2023 Harinadh D <hdommaraju@vmware.com> 1.10.2-6
- Version bump to use curl 8.1.1
* Mon Jan 24 2022 Ankit Jain <ankitja@vmware.com> 1.10.2-5
- Version Bump to build with new version of cmake
* Thu Oct 07 2021 Tapas Kundu <tkundu@vmware.com> 1.10.2-4
- Fix build with updated python symlink changes
* Wed Nov 11 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 1.10.2-3
- Fix CVE-2020-14352
* Thu Oct 24 2019 Ankit Jain <ankitja@vmware.com> 1.10.2-2
- Added for ARM Build
* Wed May 15 2019 Ankit Jain <ankitja@vmware.com> 1.10.2-1
- Initial build. First version
