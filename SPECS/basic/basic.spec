Name:       basic
Summary:    Metapackage to install minimal profile
Version:    5.0
Release:    1%{?dist}
Group:      System Environment/Base
URL:        https://vmware.github.io/photon
Vendor:     VMware, Inc.
Distribution:   Photon

Source0: license.txt
%include %{SOURCE0}

Requires: Linux-PAM
Requires: bash
Requires: bash-completion
Requires: (coreutils or coreutils-selinux)
Requires: cracklib
Requires: cracklib-dicts
Requires: dbus
Requires: filesystem
Requires: findutils
Requires: grep
Requires: grub2-efi-image
Requires: grub2-theme
Requires: openssh
Requires: photon-release
Requires: photon-repos
Requires: sed
Requires: systemd
Requires: systemd-udev
Requires: tdnf

%description
Metapackage to install basic profile

%prep
%build

%files

%changelog
* Mon Jan 05 2026 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 5.0-1
- Basic set of packages required for Photon's basic iso
