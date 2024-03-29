Name:       basic
Summary:    Metapackage to install minimal profile
Version:    5.0
Release:    2%{?dist}
License:    Apache 2.0
Group:      System Environment/Base
URL:        https://vmware.github.io/photon
Vendor:     VMware, Inc.
Distribution:   Photon

Requires: Linux-PAM
Requires: bash
Requires: bash-completion
Requires: coreutils-selinux
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
Metapackage to install minimal profile

%prep
%build

%files
%defattr(-,root,root,0755)

%changelog
* Tue Aug 15 2023 Shreenidhi Shedi <sshedi@vmware.com> 5.0-2
- Add bash-completion to requires
* Sat Jul 15 2023 Shreenidhi Shedi <sshedi@vmware.com> 5.0-1
- Basic set packages required for Photon
