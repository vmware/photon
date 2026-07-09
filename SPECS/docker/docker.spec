%define debug_package %{nil}
%define __os_install_post %{nil}

# Must be in sync with package version
%define DOCKER_ENGINE_GITCOMMIT     6fdf0a6
%define DOCKER_CLI_GITCOMMIT        0bab007
%define TINI_GITCOMMIT              de40ad0

%define gopath_comp_engine      github.com/docker/docker
%define gopath_comp_containerd  github.com/containerd/containerd
%define gopath_comp_cli         github.com/docker/cli

%define docker_cli_version      25.0.7

Summary:        Docker
Name:           docker
Version:        25.0.16
Release:        1%{?dist}
License:        ASL 2.0
URL:            http://docs.docker.com
Group:          Applications/File
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        https://github.com/moby/moby/archive/moby-%{version}.tar.gz
%define sha512  moby=e8933f1275144168dd4fb2fb5fcfb835990ce397505d6dc4582643693c585a44dfc1bc43386b76fe3a80744fa25e3be11ea34c3d944008cc2353191530872746

Source1:        https://github.com/krallin/tini/archive/tini-0.19.0.tar.gz
%define sha512  tini=3591a6db54b8f35c30eafc6bbf8903926c382fd7fe2926faea5d95c7b562130b5264228df550f2ad83581856fd5291cf4aab44ee078aef3270c74be70886055c

Source2:        https://github.com/docker/cli/archive/refs/tags/%{name}-cli-%{docker_cli_version}.tar.gz
%define sha512  %{name}-cli=0d1a688ab402329b5f4e17c36b596c0db7af4203c376472c6e8585fb9dece33df707b080c35e2866923239f04d623642199dbf3702b02dd99756c8a71b306722

Source3:       %{name}.service
Source4:       %{name}.socket
Source5:       default-disable.preset

Patch0: tini-disable-git.patch
Patch1: dockerd-containerd-CVE-2024-40635.patch
Patch2: CVE-2026-41567.patch
Patch3: CVE-2026-42306-1.patch
Patch4: CVE-2026-42306-2.patch
Patch5: CVE-2026-42306-3.patch

BuildRequires:  systemd-devel
BuildRequires:  systemd-rpm-macros
BuildRequires:  device-mapper-devel
BuildRequires:  btrfs-progs-devel
BuildRequires:  libseccomp-devel
BuildRequires:  libltdl-devel
BuildRequires:  libgcc-devel
BuildRequires:  glibc-devel
BuildRequires:  go1.26
BuildRequires:  go-md2man
BuildRequires:  cmake
BuildRequires:  sed
BuildRequires:  jq
BuildRequires:  libapparmor-devel
BuildRequires:  libslirp-devel
BuildRequires:  slirp4netns

Requires:       %{name}-engine = %{version}-%{release}
Requires:       %{name}-cli = %{version}-%{release}
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
Summary:        Documentation and vimfiles for %{name}
Requires:       %{name} = %{version}-%{release}

%description    doc
Documentation and vimfiles for %{name}

%package    rootless
Summary:    Rootless support for Docker
Requires:   slirp4netns
Requires:   libslirp
Requires:   fuse
Requires:   rootlesskit
Requires:   %{name} = %{version}-%{release}

%description    rootless
Rootless support for Docker.
Use dockerd-rootless.sh to run the daemon.
Use dockerd-rootless-setuptool.sh to setup systemd for dockerd-rootless.sh.

%prep
# Using autosetup is not feasible
%setup -q -c -n moby-%{version}

mkdir -p "$(dirname "src/%{gopath_comp_engine}")" \
         "$(dirname "src/%{gopath_comp_cli}")" \
         tini \
         bin

mv moby-%{version} src/%{gopath_comp_engine}

tar -xf %{SOURCE2}
mv cli-%{docker_cli_version} src/%{gopath_comp_cli}

tar -C tini -xf %{SOURCE1}

pushd tini
%patch -P 0 -p1
popd

# containerd source directory
pushd src/%{gopath_comp_engine}/vendor/%{gopath_comp_containerd}
%patch -P 1 -p1
popd

# moby/docker patches
pushd src/%{gopath_comp_engine}
%autopatch -m2 -M5 -p1
popd

%build
export GOPATH="$PWD"
export GO111MODULE=off

CONTAINERD_MIN_VER="1.2.0-beta.1"
BUILDTIME="$(date -u --rfc-3339 ns | sed -e 's/ /T/')"
PLATFORM="Docker Engine - Community"
DEFAULT_PRODUCT_LICENSE="Community Engine"
ENGINE_IMAGE="engine-community"

# cli
pushd "src/%{gopath_comp_cli}"
  DISABLE_WARN_OUTSIDE_CONTAINER=1 \
  VERSION=%{docker_cli_version} \
  BUILDTIME="$BUILDTIME" \
  PLATFORM="$PLATFORM" \
  GITCOMMIT=%{DOCKER_CLI_GITCOMMIT} \
  make %{?_smp_mflags} dynbinary
popd

# daemon
pushd "src/%{gopath_comp_engine}"
  VERSION=%{version} \
  DOCKER_GITCOMMIT=%{DOCKER_ENGINE_GITCOMMIT} \
  PRODUCT=%{name} \
  BUILDTIME="$BUILDTIME" \
  PLATFORM="$PLATFORM" \
  DEFAULT_PRODUCT_LICENSE="$DEFAULT_PRODUCT_LICENSE" \
  DOCKER_BUILDTAGS="seccomp selinux apparmor exclude_graphdriver_aufs" \
  ./hack/make.sh dynbinary
popd

# init
pushd tini
%{cmake} \
    -Dtini_VERSION_GIT:STRING=%{TINI_GITCOMMIT} \
    -Dgit_version_check_ret=0

cd %{__cmake_builddir}
make tini-static %{?_smp_mflags}
cp tini-static "$GOPATH/bin/%{name}-init"
popd

jq -n \
  --arg platform "$PLATFORM" \
  --arg engine_image "$ENGINE_IMGE" \
  --arg containerd_min_ver "$CONTAINERD_MIN_VER" \
  --arg runtime "host_install" \
  '.platform = $platform | .engine_image = $engine_image | .containerd_min_version = $containerd_min_ver | .runtime = $runtime' \
  > distribution_based_engine.json

%install
install -d -m755 %{buildroot}%{_bindir}
install -d -m755 %{buildroot}%{_unitdir}
install -d -m755 %{buildroot}%{_sharedstatedir}/%{name}-engine
install -d -m755 %{buildroot}%{_udevrulesdir}
install -d -m755 %{buildroot}%{_datadir}/bash-completion/completions

install -p -m 755 src/%{gopath_comp_cli}/build/docker %{buildroot}%{_bindir}/docker

# install binary
pushd src/%{gopath_comp_engine}/bundles/dynbinary-daemon
for file in dockerd %{name}-proxy; do
  install -p -m 755 $file %{buildroot}%{_bindir}/$file
done
popd

# install tini
install -p -m 755 bin/%{name}-init %{buildroot}%{_bindir}/%{name}-init

# install udev rules
install -p -m 644 src/%{gopath_comp_engine}/contrib/udev/80-%{name}.rules \
            %{buildroot}%{_udevrulesdir}/80-%{name}.rules

# add init scripts
install -p -m 644 %{SOURCE3} %{buildroot}%{_unitdir}/%{name}.service
install -p -m 644 %{SOURCE4} %{buildroot}%{_unitdir}/%{name}.socket
install -v -D -m 0644 %{SOURCE5} %{buildroot}%{_presetdir}/50-%{name}.preset

# add docker-engine metadata
install -p -m 644 distribution_based_engine.json \
            %{buildroot}%{_sharedstatedir}/%{name}-engine/distribution_based_engine.json

# add bash completions
install -p -m 644 src/%{gopath_comp_cli}/contrib/completion/bash/%{name} \
            %{buildroot}%{_datadir}/bash-completion/completions/%{name}

# docker-rootless
pushd %{_builddir}/moby-%{version}/src/github.com/%{name}/%{name}/contrib
for file in dockerd-rootless.sh dockerd-rootless-setuptool.sh; do
  install -D -p -m 0755 $file %{buildroot}%{_bindir}/$file
done
popd

%pre engine
if [ $1 -gt 0 ]; then
  # package upgrade scenario, before new files are installed

  # clear any old state
  rm -f %{_sharedstatedir}/rpm-state/%{name}-is-active > /dev/null 2>&1 || :

  # check if docker service is running
  if systemctl is-active %{name}.service > /dev/null 2>&1; then
    systemctl stop %{name} > /dev/null 2>&1 || :
    touch %{_sharedstatedir}/rpm-state/%{name}-is-active > /dev/null 2>&1 || :
  fi
fi

%preun engine
%systemd_preun %{name}.service

%post engine
if [ $1 -eq 1 ] ; then
  getent group %{name} >/dev/null || groupadd -r %{name}
fi
%systemd_post %{name}.service

%postun engine
%systemd_postun_with_restart %{name}.service

%posttrans engine
if [ $1 -ge 0 ] ; then
  # package upgrade scenario, after new files are installed

  # check if docker was running before upgrade
  if [ -f %{_sharedstatedir}/rpm-state/%{name}-is-active ]; then
    systemctl start %{name} > /dev/null 2>&1 || :
    rm -f %{_sharedstatedir}/rpm-state/%{name}-is-active > /dev/null 2>&1 || :
  fi
fi

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)

%files engine
%defattr(-,root,root)
%{_unitdir}/%{name}.service
%{_unitdir}/%{name}.socket
%{_presetdir}/50-%{name}.preset
%{_bindir}/%{name}-proxy
%{_bindir}/%{name}-init
%{_bindir}/dockerd
%{_udevrulesdir}/80-%{name}.rules
%{_sharedstatedir}/%{name}-engine/distribution_based_engine.json

%files cli
%defattr(-,root,root)
%{_bindir}/%{name}
%{_datadir}/bash-completion/completions/%{name}

%files doc
%defattr(-,root,root)

%files rootless
%defattr(-,root,root)
%{_bindir}/dockerd-rootless.sh
%{_bindir}/dockerd-rootless-setuptool.sh

%changelog
* Thu Jul 09 2026 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 25.0.16-1
- Upgrade to v25, LTS series
* Wed Jul 08 2026 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 24.0.9-11
- Don't apply CVE-2026-42306.patch
* Thu Jun 25 2026 Guruswamy Basavaiah <guruswamy.basavaiah@broadcom.com> 24.0.9-10
- Fix CVE-2026-41567, CVE-2026-42306
* Thu Apr 30 2026 Mukul Sikka <mukul.sikka@broadcom.com> 24.0.9-9
- Fix CVE-2026-33997, CVE-2026-34040
* Wed Feb 11 2026 Mukul Sikka <mukul.sikka@broadcom.com> 24.0.9-8
- Bump up as part of go upgrade
* Wed Jan 07 2026 Mukul Sikka <mukul.sikka@broadcom.com> 24.0.9-7
- Fixes CVE-2023-44487 in grpc
* Tue Jan 06 2026 Harinadh Dommaraju <Harinadh.Dommaraju@broadcom.com> 24.0.9-6
- Fixes CVE-2025-30204 in golang-jwt and CVE-2024-24786 in protobuf
* Tue Dec 30 2025 Harinadh Dommaraju <Harinadh.Dommaraju@broadcom.com> 24.0.9-5
- Fixes CVE-2024-45337,CVE-2025-22869 in crypto ssh module
* Fri Dec 19 2025 Ankit Jain <ankit-aj.jain@broadcom.com> 24.0.9-4
- Fixes CVE-2024-40635 containerd component in docker vendor source
* Tue Aug 19 2025 Guruswamy Basavaiah <guruswamy.basavaiah@broadcom.com> 24.0.9-3
- Fixes CVE-2024-41110
* Thu Jul 24 2025 Mukul Sikka <mukul.sikka@broadcom.com> 24.0.9-2
- Bump version as a part of jq upgrade
* Thu Oct 24 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 24.0.9-1
- Update to 24.0.9, Fixes CVE-2024-24557
* Thu Sep 19 2024 Mukul Sikka <mukul.sikka@broadcom.com> 24.0.5-8
- Bump version as a part of go upgrade
* Fri Jul 12 2024 Mukul Sikka <mukul.sikka@broadcom.com> 24.0.5-7
- Bump version as a part of go upgrade
* Thu Jun 20 2024 Mukul Sikka <msikka@vmware.com> 24.0.5-6
- Bump version as a part of go upgrade
* Thu Apr 18 2024 Mukul Sikka <msikka@vmware.com> 24.0.5-5
- Bump version as a part of go upgrade
* Fri Mar 29 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 24.0.5-4
- Add iptables to docker-engine requires
* Tue Nov 21 2023 Piyush Gupta <gpiyush@vmware.com> 24.0.5-3
- Bump up version to compile with new go
* Wed Oct 11 2023 Piyush Gupta <gpiyush@vmware.com> 24.0.5-2
- Bump up version to compile with new go
* Fri Aug 18 2023 Piyush Gupta <gpiyush@vmware.com> 24.0.5-1
- Upgrade to 24.0.5.
* Tue Jun 20 2023 Piyush Gupta <gpiyush@vmware.com> 20.10.14-13
- Bump up version to compile with new go
* Wed May 03 2023 Piyush Gupta <gpiyush@vmware.com> 20.10.14-12
- Bump up version to compile with new go
* Thu Mar 16 2023 Piyush Gupta <gpiyush@vmware.com> 20.10.14-11
- Bump up version to compile with new go
* Tue Dec 20 2022 Piyush Gupta <gpiyush@vmware.com> 20.10.14-10
- Bump up version to compile with new go
* Sat Nov 19 2022 Shreenidhi Shedi <sshedi@vmware.com> 20.10.14-9
- Bump version as a part of containerd upgrade
* Sun Nov 13 2022 Piyush Gupta <gpiyush@vmware.com> 20.10.14-8
- Bump up version to compile with new go
* Wed Oct 26 2022 Piyush Gupta <gpiyush@vmware.com> 20.10.14-7
- Bump up version to compile with new go
* Thu Sep 15 2022 Piyush Gupta <gpiyush@vmware.com> 20.10.14-6
- Bump up version to compile with new go
* Fri Aug 19 2022 Piyush Gupta <gpiyush@vmware.com> 20.10.14-5
- Bump up version to compile with new go
* Sat Jul 23 2022 Shreenidhi Shedi <sshedi@vmware.com> 20.10.14-4
- Move rootlesskit into a seperate package.
* Tue Jul 12 2022 Piyush Gupta <gpiyush@vmware.com> 20.10.14-3
- Bump up version to compile with new go
* Tue May 24 2022 Piyush Gupta <gpiyush@vmware.com> 20.10.14-2
- Bump up version to compile with new go.
* Tue May 10 2022 Shreenidhi Shedi <sshedi@vmware.com> 20.10.14-1
- Add docker-rootless support
- Upgrade to v20.10.14
* Fri Apr 29 2022 Shreenidhi Shedi <sshedi@vmware.com> 20.10.11-5
- Enable selinux in DOCKER_BUILDTAGS
* Tue Feb 22 2022 Piyush Gupta <gpiyush@vmware.com> 20.10.11-4
- Bump up version to compile with new go
* Fri Feb 11 2022 Piyush Gupta <gpiyush@vmware.com> 20.10.11-3
- Bump up version to compile with new go
* Tue Dec 21 2021 Nitesh Kumar <kunitesh@vmware.com> 20.10.11-2
- Bump up version to use containerd 1.4.12.
* Mon Nov 29 2021 Bo Gan <ganb@vmware.com> 20.10.11-1
- Initial packaging of 20.10
