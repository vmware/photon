Name:       minimal
Summary:    Metapackage to install minimal profile for cloud images
Version:    5.0
Release:    2%{?dist}
License:    Apache 2.0
Group:      System Environment/Base
URL:        https://vmware.github.io/photon
Vendor:     VMware, Inc.
Distribution:   Photon

Requires: bash-completion
Requires: bc
Requires: bridge-utils
Requires: bzip2
Requires: cloud-init
Requires: cpio
Requires: docker
Requires: dracut
Requires: e2fsprogs
Requires: file
Requires: gdbm
Requires: grep
Requires: gzip
Requires: iana-etc
Requires: initramfs
Requires: iproute2
Requires: iptables
Requires: iputils
Requires: basic
Requires: motd
Requires: net-tools
Requires: open-vm-tools
Requires: open-vm-tools-gosc
Requires: procps-ng
Requires: rpm
Requires: rpm-plugin-systemd-inhibit
Requires: tzdata
Requires: util-linux
Requires: vim
Requires: which

%description
Metapackage to install minimal profile

%prep
%build

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root,0755)

%changelog
* Fri Dec 06 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 5.0-2
- Add bash-completion to requires
* Sat Jul 15 2023 Shreenidhi Shedi <sshedi@vmware.com> 5.0-1
- Sort the require list and chop down package into basic
* Mon Jul 18 2022 <okurth@vmware.com> 0.1-7
- Remove pkg-config and libtool
* Wed Oct 20 2021 Shreenidhi Shedi <sshedi@vmware.com> 0.1-6
- Add rpm-plugin-systemd-inhibit
* Thu Oct 14 2021 Shreenidhi Shedi <sshedi@vmware.com> 0.1-5
- Add open-vm-tools for all platforms
* Mon Aug 17 2020 Susant Sahani <ssahani@vmware.com> 0.1-4
- Add systemd packages, sort requires packages in alphabetical order
* Thu Mar 12 2020 Alexey Makhalov <amakhalov@vmware.com> 0.1-3
- Add grub2 packages
* Thu Nov 15 2018 Alexey Makhalov <amakhalov@vmware.com> 0.1-2
- Add open-vm-tools as requires only for x86_64
* Tue Oct 30 2018 Anish Swaminathan <anishs@vmware.com> 0.1-1
- Initial packaging
