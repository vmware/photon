Summary:        FUSE overlay+shiftfs implementation for rootless containers
Name:           fuse-overlayfs
Version:        1.10
Release:        1%{?dist}
License:        GPLv3+
Group:          System Environment/Base
Vendor:         VMware, Inc.
Distribution:   Photon

URL:            https://github.com/containers/fuse-overlayfs
Source0:        https://github.com/containers/fuse-overlayfs/archive/refs/tags/%{name}-%{version}.tar.gz
%define sha512 %{name}=cb399a56f2cb0ccf3d294d82cfaa9682db6812e709b1b6d3edf6ce4f7653ddddeffb2810d1c5f8a4178dcdb42e0f65af878fd5c007b31ed18538464482ad1dcf

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  fuse3-devel
BuildRequires:  make
BuildRequires:  systemd-rpm-macros

Requires:       fuse3
Requires:       kmod

%description
fuse-overlayfs provides an overlayfs FUSE implementation so that it can be used since
Linux 4.18 by unprivileged users in an user namespace.

%package        devel
Summary:        Header and development files
Group:          Development/Libraries
BuildArch:      noarch
Requires:       %{name} = %{version}

%description    devel
This package contains library source intended for building other packages which use
import path with %{import_path} prefix.

%prep
%autosetup -p1

%build
./autogen.sh
%configure
make %{?_smp_mflags}

%install
%make_install
install -d %{buildroot}%{_modulesloaddir}
echo fuse > %{buildroot}%{_modulesloaddir}/fuse-overlayfs.conf

%files
%defattr(-,root,root)
%license COPYING
%doc README.md
%{_bindir}/%{name}
%{_mandir}/man1/*
%config(noreplace) %{_modulesloaddir}/fuse-overlayfs.conf

%changelog
* Mon Dec 19 2022 Nitesh Kumar <kunitesh@vmware.com> 1.10-1
- Version upgrade to 1.10
* Fri Sep 02 2022 Nitesh Kumar <kunitesh@vmware.com> 1.9-1
- Initial version
