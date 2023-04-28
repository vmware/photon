%define debug_package %{nil}
# git commit hash
# update commit id upon every new version release
%define commit_hash 11c45f4d24689d8cb279813fbcb9bbd01773e0e8

Summary:        fuse-overlayfs plugin for rootless containerd
Name:           fuse-overlayfs-snapshotter
Version:        1.0.5
Release:        3%{?dist}
License:        GPL3
URL:            https://github.com/containerd/fuse-overlayfs-snapshotter
Group:          Applications/File
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://github.com/containerd/fuse-overlayfs-snapshotter/archive/refs/tags/%{name}-%{version}.tar.gz
%define sha512 %{name}=f275e3f9f35c70f7048a3027f69b5cef79e4293aff5eeca7da8b483c49a58a44cfb63d3560bcab0ad24e951b1c4d20a304eccf7e81856a818ad08b0665952ca6

BuildRequires:  go
BuildRequires:  ca-certificates
BuildRequires:  build-essential

Requires:       rootlesskit
Requires:       fuse3
Requires:       fuse-overlayfs

%description
fuse-overlayfs snapshotter plugin for containerd.
fuse-overlayfs-snapshotter is a non-core sub-project of containerd.

%prep
%autosetup -p1

%build
export VERSION="%{version}-%{release}"
export REVISION=%{commit_hash}
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
* Thu Mar 09 2023 Piyush Gupta <gpiyush@vmware.com> 1.0.5-3
- Bump up version to compile with new go
* Sat Feb 11 2023 Shreenidhi Shedi <sshedi@vmware.com> 1.0.5-2
- Bump version as a part of rootlesskit upgrade
* Wed Dec 21 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.0.5-1
- Upgrade to v1.0.5
* Mon Dec 19 2022 Nitesh Kumar <kunitesh@vmware.com> 1.0.4-2
- Version bump up to use fuse-overlayfs v1.10
* Thu Nov 03 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.0.4-1
- Initial build. Needed by containerd-rootless.
