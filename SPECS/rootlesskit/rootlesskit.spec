Summary:    Linux-native fakeroot using user namespaces
Name:       rootlesskit
Version:    1.1.0
Release:    2%{?dist}
Group:      Tools/Docker
License:    Apache
URL:        https://github.com/rootless-containers/rootlesskit
Vendor:     VMware, Inc.
Distribution: Photon

Source0:    https://github.com/rootless-containers/rootlesskit/archive/refs/tags/%{name}-%{version}.tar.gz
%define sha512 %{name}=e9ac0211a93806a85943c8a30b3fae07cc3cca69608da50db8ac3da4b5d209f4c1eea00eb12cb21fe59e74e41c70ca6cdd89042711235b3e30c3db282aea8f9e

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
