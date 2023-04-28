%define debug_package %{nil}
%define __os_install_post %{nil}

# Must be in sync with package version
%define DOCKER_GITCOMMIT 99e3ed8
%define TINI_GITCOMMIT fec3683
%define gopath_comp_engine github.com/docker/docker
%define gopath_comp_cli github.com/docker/cli
%define gopath_comp_libnetwork github.com/docker/libnetwork

Summary:        Docker
Name:           docker
Version:        19.03.15
Release:        23%{?dist}
License:        ASL 2.0
URL:            http://docs.docker.com
Group:          Applications/File
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://github.com/docker/docker-ce/archive/%{name}-%{version}.tar.gz
%define sha512 %{name}=ffd8e683a93a6ce69789603d24457aebe3379594692cb3dadc25bc8d407771a29d76087b0ca70856707f151622b1853f283a1071311c033ff90a1e44b0d9ffbc

Source1: https://github.com/krallin/tini/archive/tini-fec3683.tar.gz
%define sha512 tini=dbca1d3717a228dfd1cb8a4dd6cd3b89328714c28666ba9364f1f033e44d4916ef4d12cd18c498f8a1f47b5901fc1fbb0aaf4ad37b44d1ce766fa04d8e6d1341

Source2: https://github.com/docker/libnetwork/archive/libnetwork-2fe6352.tar.gz
%define sha512 libnetwork=320232cc49a383f8f541c57d8a6b18432b5cc71ee8f10908c40bbcb345112f213c78c284a7f92cacd7183d89b0f0d2093391121891ab80796a3bab5430ae5fba

Source3:       default-disable.preset

Patch0:     tini-disable-git.patch
Patch1:     disable-docker-cli-md2man-install.patch
Patch2:     remove-firewalld-1809.patch
Patch3:     CVE-2021-41089.patch

BuildRequires:  systemd
BuildRequires:  systemd-devel
BuildRequires:  device-mapper-devel
BuildRequires:  btrfs-progs-devel
BuildRequires:  libseccomp
BuildRequires:  libseccomp-devel
BuildRequires:  libltdl-devel
BuildRequires:  libgcc-devel
BuildRequires:  glibc-devel
BuildRequires:  go
BuildRequires:  go-md2man
BuildRequires:  cmake
BuildRequires:  sed
BuildRequires:  jq
BuildRequires:  libapparmor
BuildRequires:  libapparmor-devel

Requires:       docker-engine = %{version}-%{release}
Requires:       docker-cli = %{version}-%{release}
# bash completion uses awk
Requires:       gawk

%description
Docker is an open source project to build, ship and run any application as a lightweight container.

%package        engine
Summary:        Docker Engine
Requires:       libapparmor
Requires:       libseccomp >= 2.4.0
Requires:       libltdl
Requires:       device-mapper-libs
Requires:       systemd
Requires:       containerd
Requires(post): /usr/sbin/groupadd
Requires(postun): /usr/sbin/groupdel

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
Requires:       docker = %{version}-%{release}

%description    doc
Documentation and vimfiles for docker

%prep
# Using autosetup is not feasible
%setup -q -c
mkdir -p "$(dirname "src/%{gopath_comp_engine}")" \
          "$(dirname "src/%{gopath_comp_cli}")" \
          "src/%{gopath_comp_libnetwork}" \
          tini bin

tar -C tini -xf %{SOURCE1}
pushd tini
%patch0 -p1
popd

tar -C src/%{gopath_comp_libnetwork} -xf %{SOURCE2}
pushd %{name}-ce-%{version}
%patch1 -p1
%patch2 -p1
%patch3 -p1
mv components/engine ../src/%{gopath_comp_engine}
mv components/cli ../src/%{gopath_comp_cli}
mv components/packaging ../
popd

%build
export GOPATH="$(pwd)" GO111MODULE=auto
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
  GITCOMMIT=%{DOCKER_GITCOMMIT} \
  make dynbinary manpages %{?_smp_mflags}
popd

# Don't use trimpath for now, see https://github.com/golang/go/issues/16860
# Ideally we should remove the RPM build prefixes (.../BUILD/src/...)

#BUILDFLAGS="-gcflags=all=-trimpath=$GOPATH -asmflags=all=-trimpath=$GOPATH"

# daemon
pushd "src/%{gopath_comp_engine}"
  VERSION=%{version} \
  DOCKER_GITCOMMIT=%{DOCKER_GITCOMMIT} \
  PRODUCT=docker \
  BUILDTIME="$BUILDTIME" \
  PLATFORM="$PLATFORM" \
  DEFAULT_PRODUCT_LICENSE="$DEFAULT_PRODUCT_LICENSE" \
  DOCKER_BUILDTAGS="seccomp apparmor exclude_graphdriver_aufs" \
  ./hack/make.sh dynbinary
popd

# proxy
pushd "src/%{gopath_comp_libnetwork}"
  go build -buildmode=pie -ldflags=-linkmode=external -o "$GOPATH/bin/docker-proxy" %{gopath_comp_libnetwork}/cmd/proxy
popd

# init
pushd tini
  cmake \
    -Dtini_VERSION_GIT:STRING=%{TINI_GITCOMMIT} \
    -Dgit_version_check_ret=0 \
    . && make tini-static %{?_smp_mflags} && cp tini-static "$GOPATH/bin/docker-init"
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
install -p -m 755 "src/%{gopath_comp_cli}/build/docker" %{buildroot}%{_bindir}/docker
install -p -m 755 "src/%{gopath_comp_engine}/bundles/dynbinary-daemon/dockerd" %{buildroot}%{_bindir}/dockerd

# install proxy
install -p -m 755 bin/docker-proxy %{buildroot}%{_bindir}/docker-proxy

# install tini
install -p -m 755 bin/docker-init %{buildroot}%{_bindir}/docker-init

# install udev rules
install -p -m 644 src/%{gopath_comp_engine}/contrib/udev/80-docker.rules \
            %{buildroot}%{_udevrulesdir}/80-docker.rules

# add init scripts
install -p -m 644 packaging/systemd/docker.service %{buildroot}%{_unitdir}/docker.service
install -p -m 644 packaging/systemd/docker.socket %{buildroot}%{_unitdir}/docker.socket

# add docker-engine metadata
install -p -m 644 distribution_based_engine.json %{buildroot}%{_sharedstatedir}/docker-engine/distribution_based_engine.json

# add bash completions
install -p -m 644 src/%{gopath_comp_cli}/contrib/completion/bash/docker %{buildroot}%{_datadir}/bash-completion/completions/docker

# install manpages
install -p -m 644 src/%{gopath_comp_cli}/man/man1/*.1 %{buildroot}%{_mandir}/man1
install -p -m 644 src/%{gopath_comp_cli}/man/man5/*.5 %{buildroot}%{_mandir}/man5
install -p -m 644 src/%{gopath_comp_cli}/man/man8/*.8 %{buildroot}%{_mandir}/man8

# add vimfiles
install -d -m 755 %{buildroot}%{_datadir}/vim/vimfiles/doc
install -d -m 755 %{buildroot}%{_datadir}/vim/vimfiles/ftdetect
install -d -m 755 %{buildroot}%{_datadir}/vim/vimfiles/syntax
install -p -m 644 src/%{gopath_comp_engine}/contrib/syntax/vim/doc/dockerfile.txt %{buildroot}%{_datadir}/vim/vimfiles/doc/dockerfile.txt
install -p -m 644 src/%{gopath_comp_engine}/contrib/syntax/vim/ftdetect/dockerfile.vim %{buildroot}%{_datadir}/vim/vimfiles/ftdetect/dockerfile.vim
install -p -m 644 src/%{gopath_comp_engine}/contrib/syntax/vim/syntax/dockerfile.vim %{buildroot}%{_datadir}/vim/vimfiles/syntax/dockerfile.vim

mkdir -p build-docs
for engine_file in AUTHORS CHANGELOG.md CONTRIBUTING.md LICENSE MAINTAINERS NOTICE README.md; do
    cp "src/%{gopath_comp_engine}/$engine_file" "build-docs/engine-$engine_file"
done
for cli_file in AUTHORS LICENSE MAINTAINERS NOTICE README.md; do
    cp "src/%{gopath_comp_cli}/$cli_file" "build-docs/cli-$cli_file"
done

install -v -D -m 0644 %{SOURCE3} %{buildroot}%{_presetdir}/50-docker.preset

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
%doc build-docs/engine-AUTHORS build-docs/engine-CHANGELOG.md build-docs/engine-CONTRIBUTING.md build-docs/engine-LICENSE build-docs/engine-MAINTAINERS build-docs/engine-NOTICE build-docs/engine-README.md
%doc build-docs/cli-LICENSE build-docs/cli-MAINTAINERS build-docs/cli-NOTICE build-docs/cli-README.md
%doc
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_mandir}/man8/*
%{_datadir}/vim/vimfiles/doc/dockerfile.txt
%{_datadir}/vim/vimfiles/ftdetect/dockerfile.vim
%{_datadir}/vim/vimfiles/syntax/dockerfile.vim

%changelog
* Tue Apr 04 2023 Piyush Gupta <gpiyush@vmware.com> 19.03.15-23
- Bump up version to compile with new go
* Mon Jan 02 2023 Shreenidhi Shedi <sshedi@vmware.com> 19.03.15-22
- Bump version as a part of containerd upgrade
* Tue Dec 20 2022 Piyush Gupta <gpiyush@vmware.com> 19.03.15-21
- Bump up version to compile with new go
* Sun Nov 13 2022 Piyush Gupta <gpiyush@vmware.com> 19.03.15-20
- Bump up version to compile with new go
* Wed Oct 26 2022 Piyush Gupta <gpiyush@vmware.com> 19.03.15-19
- Bump up version to compile with new go
* Thu Sep 15 2022 Piyush Gupta <gpiyush@vmware.com> 19.03.15-18
- Bump up version to compile with new go
* Thu Aug 18 2022 Piyush Gupta <gpiyush@vmware.com> 19.03.15-17
- Bump up version to compile with new go
* Mon May 09 2022 Piyush Gupta <gpiyush@vmware.com> 19.03.15-16
- Bump up version to compile with new go
* Wed Mar 16 2022 Piyush Gupta <gpiyush@vmware.com> 19.03.15-15
- Bump up version to compile with new go
* Tue Feb 22 2022 Piyush Gupta <gpiyush@vmware.com> 19.03.15-14
- Bump up version to compile with new go
* Wed Feb 02 2022 Piyush Gupta <gpiyush@vmware.com> 19.03.15-13
- Bump up version to compile with new go
* Mon Jan 24 2022 Ankit Jain <ankitja@vmware.com> 19.03.15-12
- Version Bump to build with new version of cmake
* Thu Nov 25 2021 Shreenidhi Shedi <sshedi@vmware.com> 19.03.15-11
- Depend on libseccomp >= 2.4.0
* Tue Nov 16 2021 Piyush Gupta <gpiyush@vmware.com> 19.03.15-10
- Bump up version to compile with new go
* Wed Oct 20 2021 Piyush Gupta <gpiyush@vmware.com> 19.03.15-9
- Bump up version to compile with new go
* Thu Sep 30 2021 Bo Gan <ganb@vmware.com> 19.03.15-8
- Fix CVE-2021-41089
* Thu Aug 26 2021 Keerthana K <keerthanak@vmware.com> 19.03.15-7
- Bump up version to compile with new glibc
* Sat Aug 21 2021 Piyush Gupta<gpiyush@vmware.com> 19.03.15-6
- Bump up version to compile with new go
* Sat Jul 31 2021 Piyush Gupta <gpiyush@vmware.com> 19.03.15-5
- Added Requires(post) groupadd and Requires(postun) groupdel
- in docker-engine.
* Tue Jun 29 2021 Piyush Gupta <gpiyush@vmware.com> 19.03.15-4
- Bump up version to compile with new go
* Tue May 18 2021 Piyush Gupta<gpiyush@vmware.com> 19.03.15-3
- Bump up version to compile with new go
* Mon May 10 2021 Bo Gan <ganb@vmware.com> 19.03.15-2
- Relax containerd dependency
* Thu Apr 22 2021 Ankit Jain <ankitja@vmware.com> 19.03.15-1
- Update to 19.03.15
* Mon Feb 08 2021 Harinadh D <hdommaraju@vmware.com> 19.03.10-4
- Bump up version to compile with new go
* Fri Nov 27 2020 HarinadhD <hdommaraju@vmware.com> 19.03.10-3
- Bump up version to compile with new go
* Mon Jun 15 2020 Alexey Makhalov <amakhalov@vmware.com> 19.03.10-2
- Requires: gawk
* Fri May 29 2020 Ashwin H <ashwinh@vmware.com> 19.03.10-1
- Initial version
