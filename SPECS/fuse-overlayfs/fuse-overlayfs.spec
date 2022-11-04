Summary:        FUSE overlay+shiftfs implementation for rootless containers
Name:           fuse-overlayfs
Version:        1.9
Release:        1%{?dist}
License:        GPLv3+
Group:          System Environment/Base
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://github.com/containers/fuse-overlayfs

Source0: https://github.com/containers/fuse-overlayfs/archive/refs/tags/%{name}-%{version}.tar.gz
%define sha512 %{name}=16f4feb8426c0d6f78082065a2c1c6afb96e4fc665e40e79e2b2692b0b21e77998a2195cf2cd81f505d0167318ed843f55be4eb16956aadaeab56f47ccbddc0b

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  fuse3-devel
BuildRequires:  make
BuildRequires:  systemd-devel

Requires:       fuse3
Requires:       kmod

%description
fuse-overlayfs provides an overlayfs FUSE implementation so that it can be used since
Linux 4.18 by unprivileged users in an user namespace.

%package        devel
Summary:        Header and development files
Group:          Development/Libraries
BuildArch:      noarch
Requires:       %{name} = %{version}-%{release}

%description    devel
This package contains library source intended for building other packages which use
import path with %{import_path} prefix.

%prep
%autosetup -p1

%build
sh ./autogen.sh
%configure
%make_build

%install
%make_install %{?_smp_mflags}
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
* Fri Nov 04 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.9-1
- Initial build. Needed by containerd-rootless.
