%define debug_package %{nil}

Summary:        fuse-overlayfs plugin for rootless containerd
Name:           fuse-overlayfs-snapshotter
Version:        1.0.6
Release:        5%{?dist}
License:        GPL3
URL:            https://github.com/containerd/fuse-overlayfs-snapshotter
Group:          Applications/File
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://github.com/containerd/%{name}/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
%define sha512 %{name}=7ad7f1e433695045ecb09cda6a49b9822779c953105001fa20773b61128e73b1d57d15c05043ff52a2c9415ae899f75ce1ae5ac62843c4d94640c42aee26a7d3

BuildRequires: go
BuildRequires: ca-certificates
BuildRequires: build-essential

Requires: rootlesskit
Requires: fuse3
Requires: fuse-overlayfs

%description
fuse-overlayfs snapshotter plugin for containerd.
fuse-overlayfs-snapshotter is a non-core sub-project of containerd.

%prep
%autosetup -p1

%build
export VERSION="%{version}-%{release}"
# git tag commit hash
export REVISION="a705ae6f22850358821ec1e7d968bc79003934ef"
%make_build

%install
export BINDIR="%{buildroot}%{_bindir}"
%make_install %{?_smp_mflags}

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_bindir}/containerd-fuse-overlayfs-grpc

%changelog
* Thu Apr 18 2024 Mukul Sikka <msikka@vmware.com> 1.0.6-5
- Bump version as a part of go upgrade
* Tue Nov 21 2023 Piyush Gupta <gpiyush@vmware.com> 1.0.6-4
- Bump up version to compile with new go
* Wed Oct 11 2023 Piyush Gupta <gpiyush@vmware.com> 1.0.6-3
- Bump up version to compile with new go
* Fri Aug 18 2023 Piyush Gupta <gpiyush@vmware.com> 1.0.6-2
- Bump up version to compile with new go
* Fri Jun 30 2023 Prashant S Chauhan <psinghchauha@vmware.com> 1.0.6-1
- Update to 1.0.6
* Tue Jun 20 2023 Piyush Gupta <gpiyush@vmware.com> 1.0.4-5
- Bump up version to compile with new go
* Wed May 03 2023 Piyush Gupta <gpiyush@vmware.com> 1.0.4-4
- Bump up version to compile with new go
* Thu Mar 16 2023 Piyush Gupta <gpiyush@vmware.com> 1.0.4-3
- Bump up version to compile with new go
* Tue Dec 20 2022 Piyush Gupta <gpiyush@vmware.com> 1.0.4-2
- Bump up version to compile with new go
* Thu Nov 03 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.0.4-1
- Initial build. Needed by containerd-rootless.
