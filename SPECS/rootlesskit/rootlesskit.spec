%define network_required 1
Summary:    Linux-native fakeroot using user namespaces
Name:       rootlesskit
Version:    1.1.0
Release:    13%{?dist}
Group:      Tools/Docker
URL:        https://github.com/rootless-containers/rootlesskit
Vendor:     VMware, Inc.
Distribution: Photon

Source0:    https://github.com/rootless-containers/rootlesskit/archive/refs/tags/%{name}-%{version}.tar.gz
%define sha512 %{name}=e9ac0211a93806a85943c8a30b3fae07cc3cca69608da50db8ac3da4b5d209f4c1eea00eb12cb21fe59e74e41c70ca6cdd89042711235b3e30c3db282aea8f9e

Source1: license.txt
%include %{SOURCE1}

BuildRequires: go
BuildRequires: git

Requires: slirp4netns
Requires: libslirp
Requires: fuse

Conflicts: docker-rootless < 20.10.14-3

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
* Wed Dec 11 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 1.1.0-13
- Release bump for SRP compliance
* Thu Sep 19 2024 Mukul Sikka <mukul.sikka@broadcom.com> 1.1.0-12
- Bump version as a part of go upgrade
* Fri Jul 12 2024 Mukul Sikka <mukul.sikka@broadcom.com> 1.1.0-11
- Bump version as a part of go upgrade
* Thu Jun 20 2024 Mukul Sikka <msikka@vmware.com> 1.1.0-10
- Bump version as a part of go upgrade
* Thu Feb 22 2024 Mukul Sikka <msikka@vmware.com> 1.1.0-9
- Bump version as a part of go upgrade
* Tue Nov 21 2023 Piyush Gupta <gpiyush@vmware.com> 1.1.0-8
- Bump up version to compile with new go
* Wed Oct 11 2023 Piyush Gupta <gpiyush@vmware.com> 1.1.0-7
- Bump up version to compile with new go
* Mon Sep 18 2023 Piyush Gupta <gpiyush@vmware.com> 1.1.0-6
- Bump up version to compile with new go
* Mon Jul 17 2023 Piyush Gupta <gpiyush@vmware.com> 1.1.0-5
- Bump up version to compile with new go
* Thu Jun 22 2023 Piyush Gupta <gpiyush@vmware.com> 1.1.0-4
- Bump up version to compile with new go
* Wed May 03 2023 Piyush Gupta <gpiyush@vmware.com> 1.1.0-3
- Bump up version to compile with new go
* Thu Mar 09 2023 Piyush Gupta <gpiyush@vmware.com> 1.1.0-2
- Bump up version to compile with new go
* Wed Dec 14 2022 Gerrit Photon <photon-checkins@vmware.com> 1.1.0-1
- Automatic Version Bump
* Mon Nov 21 2022 Piyush Gupta <gpiyush@vmware.com> 1.0.1-3
- Bump up version to compile with new go
* Wed Oct 26 2022 Piyush Gupta <gpiyush@vmware.com> 1.0.1-2
- Bump up version to compile with new go
* Sun Jul 10 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.0.1-1
- Initial version. Needed for docker-rootless.
