%global _vpath_srcdir .
%global _vpath_builddir %{_target_platform}
%global __global_cflags  %{optflags}
%global __global_cxxflags  %{optflags}
%global __global_ldflags -Wl,-z,relro

Summary:        File System in Userspace (FUSE) utilities
Name:           fuse3
Version:        3.9.4
Release:        1%{?dist}
License:        GPL+
Url:            http://fuse.sourceforge.net/
Group:          System Environment/Base
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://github.com/libfuse/libfuse/archive/%{name}-%{version}.tar.gz
%define sha1    fuse3=412f063f1aafc4d409271810f40b0f31e07239bb
BuildRequires:  meson >= 0.38.0
BuildRequires:  systemd-devel
%if %{with_check}
BuildRequires:  python3-devel
BuildRequires:  python3
BuildRequires:  python3-libs
BuildRequires:	python3-setuptools
BuildRequires:  python3-xml
BuildRequires:  openssl-devel
BuildRequires:  curl-devel
BuildRequires:  python3-pytest
BuildRequires:  python3-six
BuildRequires:  python3-attrs
BuildRequires:  python3-atomicwrites
BuildRequires:  which
%endif

%description
With FUSE3 it is possible to implement a fully functional filesystem in a
userspace program.

%package        devel
Summary:        Header and development files
Group:          Development/Libraries
Requires:       %{name} = %{version}
Requires:	systemd-devel

%description    devel
It contains the libraries and header files to create fuse applications.

%prep
%setup -qn libfuse-fuse-%{version}

%build
%meson -D examples=false
%meson_build

%check
easy_install_3=$(ls /usr/bin |grep easy_install |grep 3)
$easy_install_3 pluggy more_itertools
python3 -m pytest test/

%install
export MESON_INSTALL_DESTDIR_PREFIX=%{buildroot}/usr %meson_install

find %{buildroot} .
find %{buildroot} -type f -name "*.la" -exec rm -f {} ';'

# change from 4755 to 0755 to allow stripping -- fixed later in files
chmod 0755 %{buildroot}/%{_bindir}/fusermount3

# Get rid of static libs
rm -f %{buildroot}/%{_libdir}/*.a

# No need to create init-script
rm -f %{buildroot}%{_sysconfdir}/init.d/fuse3

%files
%defattr(-, root, root)
%{_libdir}/libfuse3.so*
%{_bindir}/*
%{_datadir}/man/*
%{_sbindir}/mount.fuse3
%{_sysconfdir}/fuse*
%{_libdir}/udev/rules.d/99-fuse3.rules

%files devel
%{_includedir}/*
%{_libdir}/pkgconfig/fuse3.pc
%{_libdir}/libfuse3.so*

%changelog
*   Wed Jul 15 2020 Gerrit Photon <photon-checkins@vmware.com> 3.9.4-1
-   Automatic Version Bump
*   Tue Apr 07 2020 Susant Sahani <ssahani@vmware.com> 3.9.1-1
-   Update to 3.9.1
*   Fri Nov 23 2018 Ashwin H <ashwinh@vmware.com> 3.2.6-2
-   Fix %check
*   Mon Sep 24 2018 Srinidhi Rao <srinidhir@vmware.com> 3.2.6-1
-   Update to version 3.2.6.
*   Wed Jul 05 2017 Xiaolin Li <xiaolinl@vmware.com> 3.0.1-2
-   Move pkgconfig folder to devel package.
*   Mon Apr 17 2017 Danut Moraru <dmoraru@vmware.com> 3.0.1-1
-   Initial version.
