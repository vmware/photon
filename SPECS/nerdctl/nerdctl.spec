%define debug_package %{nil}
# git tag commit hash
# update commit id upon every new version release
%define commit_hash 18944bc70784dfa83010d37054d75487a58ab581

Summary:        Docker-compatible CLI for containerd
Name:           nerdctl
Version:        1.1.0
Release:        1%{?dist}
License:        Apache 2.0
URL:            https://github.com/containerd/nerdctl
Group:          Applications/File
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://github.com/containerd/nerdctl/archive/refs/tags/%{name}-%{version}.tar.gz
%define sha512 %{name}=68c0e13c1fe7c19c91753c5e290247f8dad043538fed1014a34e9881e3da438044441473b2c01657ae923ce23e10d0d3b97ae18168a785d8fbfffdcf43c7b3d2

BuildRequires:  go
BuildRequires:  build-essential
BuildRequires:  ca-certificates

Requires: cni >= 1.1.1
Requires: containerd
Requires: slirp4netns
Requires: libslirp
Requires: rootlesskit
Requires: fuse-overlayfs
Requires: fuse-overlayfs-snapshotter

%description
%{summary}
contaiNERD CTL - Docker-compatible CLI for containerd, with support for
Compose, Rootless, eStargz, OCIcrypt, IPFS, ...
This package also provides containerd-rootless scripts.

%prep
%autosetup -p1

%build
export VERSION="%{version}-%{release}"
export REVISION=%{commit_hash}

%make_build

%install
export BINDIR="%{_bindir}"
%make_install %{?_smp_mflags}

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_bindir}/%{name}
%{_bindir}/containerd-rootless.sh
%{_bindir}/containerd-rootless-setuptool.sh

%changelog
* Wed Dec 21 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.1.0-1
- Upgrade to v1.1.0
* Fri Sep 30 2022 Shreenidhi Shedi <sshedi@vmware.com> 0.23.0-1
- First build.
