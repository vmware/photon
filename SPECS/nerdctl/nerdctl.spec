%define network_required 1
%define debug_package %{nil}
# git tag commit hash
# update commit id upon every new version release
%define commit_hash 7e8114a82da342cdbec9a518c5c6a1cce58105e9

Summary:        Docker-compatible CLI for containerd
Name:           nerdctl
Version:        1.4.0
Release:        12%{?dist}
URL:            https://github.com/containerd/nerdctl
Group:          Applications/File
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://github.com/containerd/nerdctl/archive/refs/tags/%{name}-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  go
BuildRequires:  build-essential
BuildRequires:  ca-certificates

Requires: cni >= 1.1.1
Requires: containerd
Requires: slirp4netns
Requires: libslirp
Requires: rootlesskit
Requires: fuse-overlayfs
Requires: dbus-user-session >= 1.15.4-2

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
* Fri Jan 10 2025 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 1.4.0-12
- Fix go input dependencies which have Capital letters in name.
* Wed Jan 08 2025 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 1.4.0-11
- Release bump for network_required packages
* Thu Dec 12 2024 Ajay Kaher <ajay.kaher@broadcom.com> 1.4.0-10
- Release bump for SRP compliance
* Thu Sep 19 2024 Mukul Sikka <mukul.sikka@broadcom.com> 1.4.0-9
- Bump version as a part of go upgrade
* Fri Jul 12 2024 Mukul Sikka <mukul.sikka@broadcom.com> 1.4.0-8
- Bump version as a part of go upgrade
* Thu Jun 20 2024 Mukul Sikka <msikka@vmware.com> 1.4.0-7
- Bump version as a part of go upgrade
* Thu Feb 22 2024 Mukul Sikka <msikka@vmware.com> 1.4.0-6
- Bump version as a part of go upgrade
* Tue Nov 21 2023 Piyush Gupta <gpiyush@vmware.com> 1.4.0-5
- Bump up version to compile with new go
* Wed Oct 11 2023 Piyush Gupta <gpiyush@vmware.com> 1.4.0-4
- Bump up version to compile with new go
* Mon Sep 18 2023 Piyush Gupta <gpiyush@vmware.com> 1.4.0-3
- Bump up version to compile with new go
* Mon Jul 17 2023 Piyush Gupta <gpiyush@vmware.com> 1.4.0-2
- Bump up version to compile with new go
* Tue Jul 04 2023 Shreenidhi Shedi <sshedi@vmware.com> 1.4.0-1
- Upgrade to v1.4.0
* Thu Jun 22 2023 Piyush Gupta <gpiyush@vmware.com> 1.1.0-8
- Bump up version to compile with new go
* Fri May 19 2023 Piyush Gupta <gpiyush@vmware.com> 1.1.0-7
- Bump up version to compile with containerd upgrade.
* Wed May 03 2023 Piyush Gupta <gpiyush@vmware.com> 1.1.0-6
- Bump up version to compile with new go
* Tue Mar 14 2023 Shreenidhi Shedi <sshedi@vmware.com> 1.1.0-5
- Require dbus-user-sessvion v1.15.4-2
* Thu Mar 09 2023 Piyush Gupta <gpiyush@vmware.com> 1.1.0-4
- Bump up version to compile with new go
* Sat Feb 11 2023 Shreenidhi Shedi <sshedi@vmware.com> 1.1.0-3
- Bump version as a part of rootlesskit upgrade
* Thu Jan 19 2023 Shreenidhi Shedi <sshedi@vmware.com> 1.1.0-2
- Add dbus-user-session to requires
* Wed Dec 21 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.1.0-1
- Upgrade to v1.1.0
* Fri Sep 30 2022 Shreenidhi Shedi <sshedi@vmware.com> 0.23.0-1
- First build.
