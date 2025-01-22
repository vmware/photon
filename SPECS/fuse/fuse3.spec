Summary:        File System in Userspace (FUSE) utilities
Name:           fuse3
Version:        3.9.4
Release:        5%{?dist}
License:        GPL+
Url:            http://fuse.sourceforge.net/
Group:          System Environment/Base
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://github.com/libfuse/libfuse/archive/%{name}-%{version}.tar.gz
%define sha512  fuse3=580143e4f2ecf043414947360c07dd768154b593e25fe14546ad037bcb93e738e92e3db5d447631639d4d8b3ea1f84351e4b149b179a50f6ee6d20d029edb688

BuildRequires:  meson >= 0.38.0
BuildRequires:  systemd-devel
%if 0%{?with_check}
BuildRequires:  python3-devel
BuildRequires:  python3
BuildRequires:  python3-libs
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
BuildRequires:  openssl-devel
BuildRequires:  curl-devel
BuildRequires:  python3-pytest
BuildRequires:  python3-six
BuildRequires:  python3-attrs
BuildRequires:  python3-atomicwrites
BuildRequires:  which
BuildRequires:  python3-pip
%endif

%description
With FUSE3 it is possible to implement a fully functional filesystem in a
userspace program.

%package        devel
Summary:        Header and development files
Group:          Development/Libraries
Requires:       %{name} = %{version}
Requires:       systemd-devel

%description    devel
It contains the libraries and header files to create fuse applications.

%prep
%autosetup -p1 -n libfuse-fuse-%{version}

%build
export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8

CONFIGURE_OPTS=(
   --prefix=/usr
   -D examples=false
)

meson build ${CONFIGURE_OPTS[@]}
ninja -C build

%install
export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8
DESTDIR=%{buildroot}/ ninja -C build install

find %{buildroot} -type f -name "*.la" -exec rm -f {} ';'

# change from 4755 to 0755 to allow stripping -- fixed later in files
chmod 0755 %{buildroot}/%{_bindir}/fusermount3

# Get rid of static libs
rm -f %{buildroot}/%{_libdir}/*.a

# No need to create init-script
rm -f %{buildroot}%{_sysconfdir}/init.d/fuse3

%check
pip3 install pluggy more_itertools
python3 -m pytest test/

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
*   Wed Jan 22 2025 Tapas Kundu <tapas.kundu@broadcom.com> 3.9.4-5
-   Bump version as a part of meson upgrade
*   Mon Nov 15 2021 Prashant S Chauhan <psinghchauha@vmware.com> 3.9.4-4
-   Update release to compile with python 3.10
*   Tue Sep 29 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 3.9.4-3
-   openssl 1.1.1
*   Sun Aug 16 2020 Susant Sahani <ssahani@vmware.com> 3.9.4-2
-   Use meson and ninja build system
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
