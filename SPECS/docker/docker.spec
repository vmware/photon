%define network_required 1
%define debug_package %{nil}
%define __os_install_post %{nil}

# Must be in sync with package version
%define DOCKER_ENGINE_GITCOMMIT 3ab5c7d
%define DOCKER_CLI_GITCOMMIT 3ab4256
%define TINI_GITCOMMIT de40ad0

%define gopath_comp_engine github.com/docker/docker
%define gopath_comp_cli github.com/docker/cli
%define gopath_comp_libnetwork github.com/docker/libnetwork

Summary:        Docker
Name:           docker
Version:        27.3.1
Release:        4%{?dist}
URL:            http://docs.docker.com
Group:          Applications/File
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://github.com/moby/moby/archive/moby-%{version}.tar.gz

Source1: https://github.com/krallin/tini/archive/tini-0.19.0.tar.gz

Source2: https://github.com/docker/libnetwork/archive/libnetwork-64b7a45.tar.gz

Source3: https://github.com/docker/cli/archive/refs/tags/docker-cli-%{version}.tar.gz

Source4:       docker-post19.service
Source5:       docker-post19.socket
Source6:       default-disable.preset

Source7: license.txt
%include %{SOURCE7}

Patch0:        tini-disable-git.patch
Patch1:        bridge-networking.patch

BuildRequires:  systemd-devel
BuildRequires:  device-mapper-devel
BuildRequires:  btrfs-progs-devel
BuildRequires:  libseccomp-devel
BuildRequires:  libltdl-devel
BuildRequires:  libgcc-devel
BuildRequires:  glibc-devel
BuildRequires:  go
BuildRequires:  go-md2man
BuildRequires:  cmake
BuildRequires:  sed
BuildRequires:  jq
BuildRequires:  libapparmor-devel
BuildRequires:  libslirp-devel
BuildRequires:  slirp4netns

Requires:       docker-engine = %{version}-%{release}
Requires:       docker-cli = %{version}-%{release}
# bash completion uses awk
Requires:       gawk

%description
Docker is an open source project to build, ship and run any application as a lightweight container.

%package        engine
Summary:        Docker Engine
Requires:       libapparmor
Requires:       libseccomp
Requires:       libltdl
Requires:       device-mapper-libs
Requires:       systemd
Requires:       containerd
# 20.10 uses containerd v2 shim by default
Requires:       /usr/bin/containerd-shim-runc-v2
Requires:       iptables

%description    engine
Docker is an open source project to build, ship and run any application as a lightweight container.

%package        cli
Summary:        Docker CLI
Requires:       libgcc
Requires:       glibc

%description    cli
Docker is an open source project to build, ship and run any application as a lightweight container.

%package        doc
Summary:        Documentation and vimfiles for docker
Requires:       %{name} = %{version}-%{release}

%description    doc
Documentation and vimfiles for docker

%package    rootless
Summary:    Rootless support for Docker
Requires:   slirp4netns
Requires:   libslirp
Requires:   fuse
Requires:   rootlesskit
Requires:   %{name} = %{version}-%{release}
Requires:   dbus-user-session

%description    rootless
Rootless support for Docker.
Use dockerd-rootless.sh to run the daemon.
Use dockerd-rootless-setuptool.sh to setup systemd for dockerd-rootless.sh.

%prep
# Using autosetup is not feasible
%setup -q -c -n moby-%{version}
pushd moby-%{version}
%autopatch -p1 1
popd

mkdir -p "$(dirname "src/%{gopath_comp_engine}")" \
         "$(dirname "src/%{gopath_comp_cli}")" \
         "src/%{gopath_comp_libnetwork}" \
         tini \
         bin

mv moby-%{version} src/%{gopath_comp_engine}

tar -xf %{SOURCE3}
mv cli-%{version} src/%{gopath_comp_cli}

tar -C tini -xf %{SOURCE1}

tar -C src/%{gopath_comp_libnetwork} -xf %{SOURCE2}

# Patch sources
pushd tini
%autopatch -p1 0
popd

%build
export GOPATH="${PWD}"
export GO111MODULE=off

CONTAINERD_MIN_VER="1.2.0-beta.1"
BUILDTIME="$(date -u --rfc-3339 ns | sed -e 's/ /T/')"
PLATFORM="Docker Engine - Community"
DEFAULT_PRODUCT_LICENSE="Community Engine"
ENGINE_IMAGE="engine-community"

# cli
pushd "src/%{gopath_comp_cli}"
  DISABLE_WARN_OUTSIDE_CONTAINER=1 \
  VERSION=%{version} \
  BUILDTIME="$BUILDTIME" \
  PLATFORM="$PLATFORM" \
  GITCOMMIT=%{DOCKER_CLI_GITCOMMIT} \
  make dynbinary manpages %{?_smp_mflags}
popd

# Don't use trimpath for now, see https://github.com/golang/go/issues/16860
# Ideally we should remove the RPM build prefixes (.../BUILD/src/...)

#BUILDFLAGS="-gcflags=all=-trimpath=$GOPATH -asmflags=all=-trimpath=$GOPATH"

# daemon
pushd "src/%{gopath_comp_engine}"
  VERSION=%{version} \
  DOCKER_GITCOMMIT=%{DOCKER_ENGINE_GITCOMMIT} \
  PRODUCT=docker \
  BUILDTIME="$BUILDTIME" \
  PLATFORM="$PLATFORM" \
  DEFAULT_PRODUCT_LICENSE="$DEFAULT_PRODUCT_LICENSE" \
  DOCKER_BUILDTAGS="seccomp selinux apparmor exclude_graphdriver_aufs" \
  ./hack/make.sh dynbinary
popd

# proxy
pushd "src/%{gopath_comp_libnetwork}"
  go build -buildmode=pie -ldflags=-linkmode=external -o "$GOPATH/bin/docker-proxy" %{gopath_comp_libnetwork}/cmd/proxy
popd

# init
pushd tini
%cmake \
    -Dtini_VERSION_GIT:STRING=%{TINI_GITCOMMIT} \
    -Dgit_version_check_ret=0

cd %{__cmake_builddir}
make tini-static %{?_smp_mflags}
cp tini-static "$GOPATH/bin/docker-init"
popd

jq -n \
  --arg platform "$PLATFORM" \
  --arg engine_image "$ENGINE_IMGE" \
  --arg containerd_min_ver "$CONTAINERD_MIN_VER" \
  --arg runtime "host_install" \
  '.platform = $platform | .engine_image = $engine_image | .containerd_min_version = $containerd_min_ver | .runtime = $runtime' \
  > distribution_based_engine.json

%install
install -d -m755 %{buildroot}%{_mandir}/man1
install -d -m755 %{buildroot}%{_mandir}/man5
install -d -m755 %{buildroot}%{_mandir}/man8
install -d -m755 %{buildroot}%{_bindir}
install -d -m755 %{buildroot}%{_unitdir}
install -d -m755 %{buildroot}%{_sharedstatedir}/docker-engine
install -d -m755 %{buildroot}%{_udevrulesdir}
install -d -m755 %{buildroot}%{_datadir}/bash-completion/completions

# install binary
install -p -m 755 src/%{gopath_comp_cli}/build/docker %{buildroot}%{_bindir}/docker
install -p -m 755 src/%{gopath_comp_engine}/bundles/dynbinary-daemon/dockerd %{buildroot}%{_bindir}/dockerd

# install proxy
install -p -m 755 bin/docker-proxy %{buildroot}%{_bindir}/docker-proxy

# install tini
install -p -m 755 bin/docker-init %{buildroot}%{_bindir}/docker-init

# install udev rules
install -p -m 644 src/%{gopath_comp_engine}/contrib/udev/80-docker.rules %{buildroot}%{_udevrulesdir}/80-docker.rules

# add init scripts
install -p -m 644 %{SOURCE4} %{buildroot}%{_unitdir}/docker.service
install -p -m 644 %{SOURCE5} %{buildroot}%{_unitdir}/docker.socket

# add docker-engine metadata
install -p -m 644 distribution_based_engine.json %{buildroot}%{_sharedstatedir}/docker-engine/distribution_based_engine.json

# add bash completions
install -p -m 644 src/%{gopath_comp_cli}/contrib/completion/bash/docker %{buildroot}%{_datadir}/bash-completion/completions/docker

# install manpages
install -p -m 644 src/%{gopath_comp_cli}/man/man1/*.1 %{buildroot}%{_mandir}/man1
install -p -m 644 src/%{gopath_comp_cli}/man/man5/*.5 %{buildroot}%{_mandir}/man5
install -p -m 644 src/%{gopath_comp_cli}/man/man8/*.8 %{buildroot}%{_mandir}/man8

# vimfiles are now upstream, no vim files installed

mkdir -p build-docs
for engine_file in AUTHORS CONTRIBUTING.md LICENSE MAINTAINERS NOTICE README.md; do
  cp "src/%{gopath_comp_engine}/$engine_file" "build-docs/engine-$engine_file"
done
for cli_file in AUTHORS LICENSE MAINTAINERS NOTICE README.md; do
  cp "src/%{gopath_comp_cli}/$cli_file" "build-docs/cli-$cli_file"
done

install -v -D -m 0644 %{SOURCE6} %{buildroot}%{_presetdir}/50-docker.preset

# docker-rootless
install -D -p -m 0755 %{_builddir}/moby-%{version}/src/github.com/docker/docker/contrib/dockerd-rootless.sh %{buildroot}%{_bindir}/dockerd-rootless.sh
install -D -p -m 0755 %{_builddir}/moby-%{version}/src/github.com/docker/docker/contrib/dockerd-rootless-setuptool.sh %{buildroot}%{_bindir}/dockerd-rootless-setuptool.sh

%pre engine
if [ $1 -gt 0 ] ; then
  # package upgrade scenario, before new files are installed

  # clear any old state
  rm -f %{_sharedstatedir}/rpm-state/docker-is-active > /dev/null 2>&1 || :

  # check if docker service is running
  if systemctl is-active docker.service > /dev/null 2>&1; then
    systemctl stop docker > /dev/null 2>&1 || :
    touch %{_sharedstatedir}/rpm-state/docker-is-active > /dev/null 2>&1 || :
  fi
fi

%preun engine
%systemd_preun docker.service

%post engine
if [ $1 -eq 1 ] ; then
  getent group docker >/dev/null || groupadd -r docker
fi
%systemd_post docker.service

%postun engine
%systemd_postun_with_restart docker.service
if [ $1 -eq 0 ] ; then
  getent group docker >/dev/null && groupdel docker || :
fi

%posttrans engine
if [ $1 -ge 0 ] ; then
  # package upgrade scenario, after new files are installed

  # check if docker was running before upgrade
  if [ -f %{_sharedstatedir}/rpm-state/docker-is-active ]; then
    systemctl start docker > /dev/null 2>&1 || :
    rm -f %{_sharedstatedir}/rpm-state/docker-is-active > /dev/null 2>&1 || :
  fi
fi

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)

%files engine
%defattr(-,root,root)
%{_unitdir}/docker.service
%{_unitdir}/docker.socket
%{_presetdir}/50-docker.preset
%{_bindir}/docker-proxy
%{_bindir}/docker-init
%{_bindir}/dockerd
%{_udevrulesdir}/80-docker.rules
%{_sharedstatedir}/docker-engine/distribution_based_engine.json

%files cli
%defattr(-,root,root)
%{_bindir}/docker
%{_datadir}/bash-completion/completions/docker

%files doc
%defattr(-,root,root)
%doc build-docs/engine-AUTHORS build-docs/engine-CONTRIBUTING.md build-docs/engine-LICENSE build-docs/engine-MAINTAINERS build-docs/engine-NOTICE build-docs/engine-README.md
%doc build-docs/cli-LICENSE build-docs/cli-MAINTAINERS build-docs/cli-NOTICE build-docs/cli-README.md
%doc
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_mandir}/man8/*

%files rootless
%{_bindir}/dockerd-rootless.sh
%{_bindir}/dockerd-rootless-setuptool.sh

%changelog
* Fri Jan 10 2025 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 27.3.1-4
- Fix go input dependencies which have Capital letters in name.
* Wed Jan 08 2025 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 27.3.1-3
- Release bump for network_required packages
* Thu Dec 12 2024 Guruswamy Basavaiah <guruswamy.basavaiah@broadcom.com> 27.3.1-2
- Release bump for SRP compliance
* Mon Nov 25 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 27.3.1-1
- Upgrade to v27.3.1
* Thu Nov 21 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 27.2.0-1
- Update to 27.2.0
* Thu Oct 24 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 24.0.9-1
- Update to 24.0.9, Fixes CVE-2024-24557
* Thu Sep 19 2024 Mukul Sikka <mukul.sikka@broadcom.com> 24.0.5-9
- Bump version as a part of go upgrade
* Fri Jul 12 2024 Mukul Sikka <mukul.sikka@broadcom.com> 24.0.5-8
- Bump version as a part of go upgrade
* Thu Jun 20 2024 Mukul Sikka <msikka@vmware.com> 24.0.5-7
- Bump version as a part of go upgrade
* Fri Mar 29 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 24.0.5-6
- Add iptables to docker-engine requires
* Thu Feb 22 2024 Mukul Sikka <msikka@vmware.com> 24.0.5-5
- Bump version as a part of go upgrade
* Tue Nov 21 2023 Piyush Gupta <gpiyush@vmware.com> 24.0.5-4
- Bump up version to compile with new go
* Wed Oct 11 2023 Piyush Gupta <gpiyush@vmware.com> 24.0.5-3
- Bump up version to compile with new go
* Mon Sep 18 2023 Piyush Gupta <gpiyush@vmware.com> 24.0.5-2
- Bump up version to compile with new go
* Thu Jul 20 2023 Piyush Gupta <gpiyush@vmware.com> 24.0.5-1
- Upgrade to 24.0.5.
* Thu Jun 22 2023 Piyush Gupta <gpiyush@vmware.com> 23.0.2-4
- Bump up version to compile with new go
* Fri May 19 2023 Piyush Gupta <gpiyush@vmware.com> 23.0.2-3
- Bump up version to compile with containerd upgrade
* Wed May 03 2023 Piyush Gupta <gpiyush@vmware.com> 23.0.2-2
- Bump up version to compile with new go
* Thu Mar 30 2023 Prashant S Chauhan <psinghchauha@vmware.com> 23.0.2-1
- Update to 23.0.2, Add libapparmor as requires
* Fri Mar 24 2023 Prashant S Chauhan <psinghchauha@vmware.com> 23.0.1-2
- Add apparmor-profiles as Requires, fixes apparmor profile not applied
* Fri Mar 10 2023 Prashant S Chauhan <psinghchauha@vmware.com> 23.0.1-1
- Update to 23.0.1
* Thu Mar 09 2023 Piyush Gupta <gpiyush@vmware.com> 20.10.14-9
- Bump up version to compile with new go
* Sat Feb 11 2023 Shreenidhi Shedi <sshedi@vmware.com> 20.10.14-8
- Bump version as a part of rootlesskit upgrade
* Thu Jan 19 2023 Shreenidhi Shedi <sshedi@vmware.com> 20.10.14-7
- Add dbus-user-session to requires
* Thu Nov 24 2022 Shreenidhi Shedi <sshedi@vmware.com> 20.10.14-6
- Bump version as a part of containerd upgrade
* Mon Nov 21 2022 Piyush Gupta <gpiyush@vmware.com> 20.10.14-5
- Bump up version to compile with new go
* Wed Oct 26 2022 Piyush Gupta <gpiyush@vmware.com> 20.10.14-4
- Bump up version to compile with new go
* Sun Jul 10 2022 Shreenidhi Shedi <sshedi@vmware.com> 20.10.14-3
- Add seperate package for rootlesskit & add proper conflicts.
* Tue May 10 2022 Shreenidhi Shedi <sshedi@vmware.com> 20.10.14-2
- Add docker-rootless support
* Wed Apr 27 2022 Shreenidhi Shedi <sshedi@vmware.com> 20.10.14-1
- Initial packaging of 20.10
