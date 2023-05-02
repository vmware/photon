%define debug_package %{nil}

Summary:        fuse-overlayfs plugin for rootless containerd
Name:           fuse-overlayfs-snapshotter
Version:        1.0.4
Release:        4%{?dist}
License:        GPL3
URL:            https://github.com/containers/fuse-overlayfs
Group:          Applications/File
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://github.com/containerd/nerdctl/archive/refs/tags/%{name}-%{version}.tar.gz
%define sha512 %{name}=b4a7a3edc7c2baebdc1d6f3717a71aecdf4b8d31c0a26d1efa5dae5325ac19cb915588bb3da1fdd14a6d16377dcf17ed5be3f5b2ec5ae19627adf66332995a71

Patch0: fix-makefile.patch
Patch1: makefile-destdir-fix.patch

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
export REVISION="db90194f0cf2f42ee8cdc3c542f6ed2c92ef8ffc"
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
* Wed May 03 2023 Piyush Gupta <gpiyush@vmware.com> 1.0.4-4
- Bump up version to compile with new go
* Thu Mar 16 2023 Piyush Gupta <gpiyush@vmware.com> 1.0.4-3
- Bump up version to compile with new go
* Tue Dec 20 2022 Piyush Gupta <gpiyush@vmware.com> 1.0.4-2
- Bump up version to compile with new go
* Thu Nov 03 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.0.4-1
- Initial build. Needed by containerd-rootless.
