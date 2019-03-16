Name:           minimal
Summary:        Metapackage to install minimal profile
Version:        0.1
Release:        1%{?dist}
License:        Apache 2.0
Group:          System Environment/Base
URL:            https://vmware.github.io/photon/
Vendor:         VMware, Inc.
Distribution:   Photon
Requires:       filesystem
Requires:       pkg-config
Requires:       bzip2
Requires:       procps-ng
Requires:       iana-etc
Requires:       bc
Requires:       libtool
Requires:       net-tools
Requires:       findutils
Requires:       iproute2
Requires:       iptables
Requires:       iputils
Requires:       dbus
Requires:       file
Requires:       e2fsprogs
Requires:       rpm
Requires:       openssh
Requires:       gdbm
Requires:       photon-release
Requires:       photon-repos
Requires:       sed
Requires:       grep
Requires:       util-linux
Requires:       cpio
Requires:       gzip
Requires:       vim
Requires:       tdnf
Requires:       docker
Requires:       bridge-utils
Requires:       cloud-init
Requires:       which
Requires:       cracklib-dicts
%ifarch x86_64
Requires:       open-vm-tools
%endif

%description
Metapackage to install minimal profile

%prep

%build

%files
%defattr(-,root,root,0755)

%changelog
*   Tue Oct 30 2018 Anish Swaminathan <anishs@vmware.com> 0.1-1
-   Initial packaging
