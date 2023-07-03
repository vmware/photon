Summary:        FUSE overlay+shiftfs implementation for rootless containers
Name:           fuse-overlayfs
Version:        1.12
Release:        1%{?dist}
License:        GPLv3+
Group:          System Environment/Base
Vendor:         VMware, Inc.
Distribution:   Photon

URL:            https://github.com/containers/fuse-overlayfs
Source0:        https://github.com/containers/fuse-overlayfs/archive/refs/tags/%{name}-%{version}.tar.gz
%define sha512 %{name}=f113ac20b389d2f1c5e5ff160a60c308017e74c9c85d74a7200bab81a4cfa30335a64740c173f17c91ab4feddffb138ca4378e92894645a67eea5ac73d42890f

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
* Fri Jun 30 2023 Prashant S Chauhan <psinghchauha@vmware.com> 1.12-1
- Upgrade to 1.12
* Mon Dec 19 2022 Nitesh Kumar <kunitesh@vmware.com> 1.10-1
- Version upgrade to 1.10
* Fri Sep 02 2022 Nitesh Kumar <kunitesh@vmware.com> 1.9-1
- Initial version
