Summary:        FUSE overlay+shiftfs implementation for rootless containers
Name:           fuse-overlayfs
Version:        1.12
Release:        2%{?dist}
Group:          System Environment/Base
Vendor:         VMware, Inc.
Distribution:   Photon

URL:            https://github.com/containers/fuse-overlayfs
Source0:        https://github.com/containers/fuse-overlayfs/archive/refs/tags/%{name}-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

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
* Thu Dec 12 2024 Guruswamy Basavaiah <guruswamy.basavaiah@broadcom.com> 1.12-2
- Release bump for SRP compliance
* Fri Jun 30 2023 Prashant S Chauhan <psinghchauha@vmware.com> 1.12-1
- Upgrade to 1.12
* Mon Dec 19 2022 Nitesh Kumar <kunitesh@vmware.com> 1.10-1
- Version upgrade to 1.10
* Fri Sep 02 2022 Nitesh Kumar <kunitesh@vmware.com> 1.9-1
- Initial version
