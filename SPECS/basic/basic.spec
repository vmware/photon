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
Requires: coreutils >= 9.1-10
Requires: cracklib
Requires: cracklib-dicts
Requires: dbus
Requires: filesystem
Requires: findutils
Requires: grep
Requires: grub2-efi-image >= 2.06-15
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
* Tue Nov 19 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 5.0-1
- Initial version.
