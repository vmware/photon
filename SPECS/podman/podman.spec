%global build_if %{photon_subrelease} >= 92

%global gvisorvers 0.8.9

Summary:        A tool to manage Pods, Containers and Container Images
Name:           podman
Version:        5.8.5
Release:        2%{?dist}
URL:            https://github.com/containers/podman
Group:          Podman
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://github.com/containers/podman/archive/refs/tags/%{name}-%{version}.tar.gz

Source1: 50-podman-network.conf

Source2: https://github.com/containers/gvisor-tap-vsock/archive/refs/tags/gvisor-tap-vsock-%{gvisorvers}.tar.gz

Source3: license.txt
%include %{SOURCE3}

BuildRequires:  gcc
BuildRequires:  glibc-devel
BuildRequires:  libgpg-error-devel
BuildRequires:  shadow-tools
BuildRequires:  pkg-config
BuildRequires:  make
BuildRequires:  systemd-devel
BuildRequires:  containers-common
BuildRequires:  go-md2man
BuildRequires:  go
BuildRequires:  libassuan-devel
BuildRequires:  gpgme-devel
BuildRequires:  btrfs-progs-devel
BuildRequires:  device-mapper-devel
BuildRequires:  libseccomp-devel
BuildRequires:  libselinux-devel

Provides:       pkgconfig(devmapper)

Requires:       libassuan
Requires:       gpgme
Requires:       conmon
Requires:       containers-common
Requires:       iptables
Requires:       shadow
Requires:       slirp4netns
Requires:       netavark

Obsoletes:      podman-plugins < 5.8.5-1

%description
%{name} is a daemonless, open source, Linux native tool designed to make it easy to find, run, build,
share and deploy applications using OCI Containers and Container Images.

%package tests
Summary: Tests for %{name}
Requires: bats
Requires: jq

%description tests
This package contains system tests for %{name}

%package remote
Summary: (Experimental) Remote client for managing %{name} containers

%description remote
Remote client to connect with a %{name} client for managing %{name} containers. This experimental
remote client is under heavy development. Please do not run %{name}-remote in production.

%package gvproxy
Summary: Go replacement for libslirp and VPNKit

%description gvproxy
A replacement for libslirp and VPNKit, written in pure Go. It is based on the network stack of gVisor.
Compared to libslirp, gvisor-tap-vsock brings a configurable DNS server and dynamic port forwarding.

%package docs
Summary:    %{name} docs
Group:      Documentation
Requires:   %{name} = %{version}-%{release}

%description docs
Contains man pages for %{name}

%prep
%autosetup -p1 -n %{name}-%{version}
rm -v vendor/github.com/opencontainers/go-digest/LICENSE.docs \
      vendor/github.com/opencontainers/go-digest/README.md \
      vendor/github.com/opencontainers/go-digest/CONTRIBUTING.md
tar xf %{SOURCE2} --no-same-owner \
  --exclude=vendor/github.com/opencontainers/go-digest/LICENSE.docs \
  --exclude=vendor/github.com/opencontainers/go-digest/README.md \
  --exclude=vendor/github.com/opencontainers/go-digest/CONTRIBUTING.md

%build
#build podman
export BUILDTAGS="seccomp exclude_graphdriver_devicemapper $(hack/btrfs_installed_tag.sh) $(hack/btrfs_tag.sh) $(hack/libdm_tag.sh) $(hack/selinux_tag.sh) $(hack/systemd_tag.sh) $(hack/libsubid_tag.sh)"
%make_build

#build gvproxy
pushd gvisor-tap-vsock-%{gvisorvers}
%make_build
popd

%install
#install podman
export PREFIX=%{_prefix}

%make_install %{?_smp_mflags} LIBEXECDIR=%{_libexecdir} \
     install.bin install.man install.systemd install.completions \
     install.remote

install -dp %{buildroot}%{_sysconfdir}/containers/containers.conf.d
install -Dp -m0644 %{SOURCE1} -t %{buildroot}%{_sysconfdir}/containers/containers.conf.d

install -d -p %{buildroot}%{_datadir}/%{name}/test/system
cp -pav test/system %{buildroot}%{_datadir}/%{name}/test/

# Man pages go to the docs subpackage, excluding podman-remote's own man page
rm -f podman-docs.file-list
for file in $(find %{buildroot}%{_mandir}/man[15] -type f | sed "s,%{buildroot},," | grep -v -e remote); do
  echo "$file*" >> podman-docs.file-list
done

#install gvproxy
pushd gvisor-tap-vsock-%{gvisorvers}
install -dp %{buildroot}%{_libexecdir}/%{name}
install -p -m0755 bin/gvproxy %{buildroot}%{_libexecdir}/%{name}
popd

rm -rv %{buildroot}%{_datadir}/zsh \
       %{buildroot}%{_datadir}/fish

%files
%defattr(-,root,root)
%license LICENSE
%doc README.md CONTRIBUTING.md install.md transfer.md
%{_bindir}/%{name}
%{_bindir}/podmansh
%dir %{_libexecdir}/%{name}
%{_libexecdir}/%{name}/rootlessport
%{_libexecdir}/%{name}/quadlet
%{_datadir}/bash-completion/completions/%{name}
%{_unitdir}/%{name}*
%{_userunitdir}/%{name}*
%{_tmpfilesdir}/%{name}.conf
%{_systemdgeneratordir}/%{name}-system-generator
%{_systemdusergeneratordir}/%{name}-user-generator
%dir %{_sysconfdir}/containers/containers.conf.d
%config(noreplace) %{_sysconfdir}/containers/containers.conf.d/50-podman-network.conf

%files docs -f %{name}-docs.file-list
%defattr(-,root,root)
%{_mandir}/man7/%{name}-*.gz

%files remote
%defattr(-,root,root)
%license LICENSE
%{_bindir}/%{name}-remote
%{_mandir}/man1/%{name}-remote*.*
%{_datadir}/bash-completion/completions/%{name}-remote

%files tests
%defattr(-,root,root)
%license LICENSE
%{_datadir}/%{name}/test

%files gvproxy
%defattr(-,root,root)
%{_libexecdir}/%{name}/gvproxy

%changelog
* Tue Oct 20 2026 Alexey Makhalov <alexey.makhalov@broadcom.com> 5.8.5-2
- Bump version as a part of go upgrade
* Tue Aug 11 2026 Prashant Singh Chauhan <prashant.singh-chauhan@broadcom.com> 5.8.5-1
- Upgrade to v5.8.5, split man pages into a podman-docs subpackage
* Fri May 15 2026 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 4.5.1-15
- Extended to build for subrelease 91 and above
* Thu Mar 12 2026 Guruswamy Baasavaiah <guruswamy.basavaiah@broadcom.com> 4.5.1-14
- Version bump for removing lzo support in podman
* Wed Feb 04 2026 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 4.5.1-13
- Bump version as a part of go upgrade
* Thu Oct 09 2025 Mukul Sikka <mukul.sikka@broadcom.com> 4.5.1-12
- Bump version as a part of go upgrade
* Tue Aug 12 2025 Dweep Advani <dweep.advani@broadcom.com> 4.5.1-11
- Bump release to rescan licenses
* Wed Dec 11 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 4.5.1-10
- Release bump for SRP compliance
* Thu Sep 19 2024 Mukul Sikka <mukul.sikka@broadcom.com> 4.5.1-9
- Bump version as a part of go upgrade
* Fri Jul 12 2024 Mukul Sikka <mukul.sikka@broadcom.com> 4.5.1-8
- Bump version as a part of go upgrade
* Thu Jun 20 2024 Mukul Sikka <msikka@vmware.com> 4.5.1-7
- Bump version as a part of go upgrade
* Thu Feb 22 2024 Mukul Sikka <msikka@vmware.com> 4.5.1-6
- Bump version as a part of go upgrade
* Tue Nov 21 2023 Piyush Gupta <gpiyush@vmware.com> 4.5.1-5
- Bump up version to compile with new go
* Wed Oct 11 2023 Piyush Gupta <gpiyush@vmware.com> 4.5.1-4
- Bump up version to compile with new go
* Mon Sep 18 2023 Piyush Gupta <gpiyush@vmware.com> 4.5.1-3
- Bump up version to compile with new go
* Mon Jul 17 2023 Piyush Gupta <gpiyush@vmware.com> 4.5.1-2
- Bump up version to compile with new go
* Tue Jun 27 2023 Prashant S Chauhan <psingchauha@vmware.com> 4.5.1-1
- Update to 4.5.1, Fixes second level CVE-2022-2990, CVE-2023-25173
* Thu Jun 22 2023 Piyush Gupta <gpiyush@vmware.com> 4.3.1-5
- Bump up version to compile with new go
* Wed May 03 2023 Piyush Gupta <gpiyush@vmware.com> 4.3.1-4
- Bump up version to compile with new go
* Tue Mar 14 2023 Nitesh Kumar <kunitesh@vmware.com> 4.3.1-3
- Upgrade gvisor-tap-vsock to compile with latest go
* Thu Dec 22 2022 Guruswamy Basavaiah <bguruswamy@vmware.com> 4.3.1-2
- Bump release as a part of libgpg-error upgrade to 1.46
* Mon Dec 19 2022 Nitesh Kumar <kunitesh@vmware.com> 4.3.1-1
- Version upgrade to v4.3.1
* Thu Nov 24 2022 Shreenidhi Shedi <sshedi@vmware.com> 4.3.0-3
- Bump version as a part of cni upgrade
* Mon Nov 21 2022 Piyush Gupta <gpiyush@vmware.com> 4.3.0-2
- Bump up version to compile with new go
* Wed Nov 2 2022 Gerrit Photon <photon-checkins@vmware.com> 4.3.0-1
- Automatic Version Bump
* Wed Oct 26 2022 Piyush Gupta <gpiyush@vmware.com> 4.2.1-2
- Bump up version to compile with new go
* Thu Oct 06 2022 Gerrit Photon <photon-checkins@vmware.com> 4.2.1-1
- Automatic Version Bump
* Fri Sep 02 2022 Nitesh Kumar <kunitesh@vmware.com> 4.2.0-1
- Initial version
