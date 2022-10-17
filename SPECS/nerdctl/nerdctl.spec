%define debug_package %{nil}

Summary:        Docker-compatible CLI for containerd
Name:           nerdctl
Version:        0.23.0
Release:        1%{?dist}
License:        Apache 2.0
URL:            https://github.com/containerd/nerdctl
Group:          Applications/File
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://github.com/containerd/nerdctl/archive/refs/tags/%{name}-%{version}.tar.gz
%define sha512 %{name}=2d3a268cde5e4ef02172f450690d7a8810111e725d1f35a707267cb8e04b64cec4329df0878997dfcd980a73b9dd297ac97f554f37cc7df5159d581e372bdc17

Patch0: fix-makefile.patch

BuildRequires: go
BuildRequires: ca-certificates
BuildRequires: build-essential

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
# git tag commit hash
export REVISION="660680b7ddfde1d38a66ec1c7f08f8d89ab92c68"

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
* Fri Sep 30 2022 Shreenidhi Shedi <sshedi@vmware.com> 0.23.0-1
- First build.
