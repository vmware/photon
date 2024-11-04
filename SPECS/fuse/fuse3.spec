Summary:        File System in Userspace (FUSE) utilities
Name:           fuse3
Version:        3.12.0
Release:        2%{?dist}
Url:            http://fuse.sourceforge.net/
Group:          System Environment/Base
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        https://github.com/libfuse/libfuse/archive/%{name}-%{version}.tar.gz
%define sha512  fuse3=70acaa11ba976f4fb83ce25017725aa486d490ba8f7c1cdf9f98e93e6e0a331b5e3fd78c746d1b4dbb783987397ff30ccc5f6e49e150e34c5b2dfc977fc22d01

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  meson >= 0.38.0
BuildRequires:  systemd-devel
%if 0%{?with_check}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
BuildRequires:  openssl-devel
BuildRequires:  curl-devel
BuildRequires:  python3-pytest
BuildRequires:  python3-six
BuildRequires:  python3-attrs
BuildRequires:  python3-pip
BuildRequires:  python3-atomicwrites
BuildRequires:  which
%endif

%description
With FUSE3 it is possible to implement a fully functional filesystem in a
userspace program.

%package        devel
Summary:        Header and development files
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       systemd-devel

%description    devel
It contains the libraries and header files to create fuse applications.

%prep
%autosetup -n libfuse-fuse-%{version}

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
*   Tue Nov 05 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 3.12.0-2
-   Release bump for SRP compliance
*   Wed Nov 30 2022 Piyush Gupta <gpiyush@vmware.com> 3.12.0-1
-   Upgrade to 3.12.0.
*   Wed Jun 01 2022 Gerrit Photon <photon-checkins@vmware.com> 3.11.0-1
-   Automatic Version Bump
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
