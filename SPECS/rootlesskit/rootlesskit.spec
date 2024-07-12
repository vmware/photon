Summary:    Linux-native fakeroot using user namespaces
Name:       rootlesskit
Version:    1.0.1
Release:    15%{?dist}
Group:      Tools/Docker
License:    Apache
URL:        https://github.com/rootless-containers/rootlesskit
Vendor:     VMware, Inc.
Distribution: Photon

Source0:    https://github.com/rootless-containers/rootlesskit/archive/refs/tags/%{name}-%{version}.tar.gz
%define sha512 %{name}=a83a07b80f3b99329bab851eec2f2e388357b254817868d35904550fde84022a41245db290ab8a117cd631a8dda32606738528e9354c1dd5d46fbd824fa49112

BuildRequires: go
BuildRequires: git

Requires: slirp4netns
Requires: libslirp
Requires: fuse

Conflicts: docker-rootless < 20.10.14-4

%description
RootlessKit is a Linux-native implementation of "fake root" using user_namespaces(7).
The purpose of RootlessKit is to run Docker and Kubernetes as an unprivileged user
(known as "Rootless mode"), so as to protect the real root on the host from potential
container-breakout attacks.

%prep
%autosetup -Sgit -p1

%build
%make_build

%install
export BINDIR=%{_bindir}
%make_install

%files
%{_bindir}/%{name}
%{_bindir}/%{name}-docker-proxy
%{_bindir}/rootlessctl

%changelog
* Fri Jul 12 2024 Mukul Sikka <mukul.sikka@broadcom.com> 1.0.1-15
- Bump version as a part of go upgrade
* Thu Jun 20 2024 Mukul Sikka <msikka@vmware.com> 1.0.1-14
- Bump version as a part of go upgrade
* Thu Apr 18 2024 Mukul Sikka <msikka@vmware.com> 1.0.1-13
- Bump version as a part of go upgrade
* Tue Nov 21 2023 Piyush Gupta <gpiyush@vmware.com> 1.0.1-12
- Bump up version to compile with new go
* Wed Oct 11 2023 Piyush Gupta <gpiyush@vmware.com> 1.0.1-11
- Bump up version to compile with new go
* Fri Aug 18 2023 Piyush Gupta <gpiyush@vmware.com> 1.0.1-10
- Bump up version to compile with new go
* Tue Jun 20 2023 Piyush Gupta <gpiyush@vmware.com> 1.0.1-9
- Bump up version to compile with new go
* Wed May 03 2023 Piyush Gupta <gpiyush@vmware.com> 1.0.1-8
- Bump up version to compile with new go
* Thu Mar 16 2023 Piyush Gupta <gpiyush@vmware.com> 1.0.1-7
- Bump up version to compile with new go
* Tue Dec 20 2022 Piyush Gupta <gpiyush@vmware.com> 1.0.1-6
- Bump up version to compile with new go
* Sun Nov 13 2022 Piyush Gupta <gpiyush@vmware.com> 1.0.1-5
- Bump up version to compile with new go
* Wed Oct 26 2022 Piyush Gupta <gpiyush@vmware.com> 1.0.1-4
- Bump up version to compile with new go
* Thu Sep 15 2022 Piyush Gupta <gpiyush@vmware.com> 1.0.1-3
- Bump up version to compile with new go
* Fri Aug 19 2022 Piyush Gupta <gpiyush@vmware.com> 1.0.1-2
- Bump up version to compile with new go
* Sun Jul 10 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.0.1-1
- Initial version. Needed for docker-rootless.
