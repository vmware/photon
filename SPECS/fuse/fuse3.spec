Summary:        File System in Userspace (FUSE) utilities
Name:           fuse3
Version:        3.2.6
Release:        1%{?dist}
License:        GPL+
Url:            http://fuse.sourceforge.net/
Group:          System Environment/Base
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://github.com/libfuse/libfuse/archive/%{name}-%{version}.tar.gz
%define sha1    fuse3=cd2e28231751d2854afdec9efc0380ef294efa3f
BuildRequires:  ninja-build
BuildRequires:  meson >= 0.38.0
BuildRequires:  python3
BuildRequires:  python-pytest
BuildRequires:  systemd
BuildRequires:  systemd-devel

%description
With FUSE3 it is possible to implement a fully functional filesystem in a
userspace program.

%package        devel
Summary:        Header and development files
Group:          Development/Libraries
Requires:       %{name} = %{version}
BuildRequires:  ninja-build
BuildRequires:  meson >= 0.38.0
BuildRequires:  python3
BuildRequires:  systemd
BuildRequires:  systemd-devel

%description    devel
It contains the libraries and header files to create fuse applications.

%prep
%setup -q -n fuse3-%{version}

%build
mkdir build &&
cd    build &&
meson --prefix=%{_prefix} .. &&
ninja -C ./

%install
cd build
DESTDIR=%{buildroot}/ ninja -C ./ install

#%check
#cd build
#python3 -m pytest test/

%files
%defattr(-, root, root)
%{_libdir}/libfuse3.so*
/lib/udev/rules.d/*
%{_bindir}/*
%{_sysconfdir}/fuse*
%{_datadir}/man/*
%{_sbindir}/mount.fuse3
%exclude %{_sysconfdir}/init.d/fuse3

%files devel
%{_includedir}/*
%{_libdir}/pkgconfig/fuse3.pc
%{_libdir}/libfuse3.so*

%changelog
*   Mon Sep 24 2018 Srinidhi Rao <srinidhir@vmware.com> 3.2.6-1
-   Move pkgconfig folder to devel package.
*   Wed Jul 05 2017 Xiaolin Li <xiaolinl@vmware.com> 3.0.1-2
-   Move pkgconfig folder to devel package.
*   Mon Apr 17 2017 Danut Moraru <dmoraru@vmware.com> 3.0.1-1
-   Initial version.
