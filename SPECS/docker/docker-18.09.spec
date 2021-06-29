%define debug_package %{nil}
%define __os_install_post %{nil}
Summary:        Docker
Name:           docker
Version:        18.09.9
Release:        9%{?dist}
License:        ASL 2.0
URL:            http://docs.docker.com
Group:          Applications/File
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://github.com/docker/docker-ce/archive/%{name}-%{version}.tar.gz
%define sha1 docker=efe4cb8b60f888ab83776c84717a2b3078928bce
# Must be in sync with package version
%define DOCKER_GITCOMMIT 039a7df
%define TINI_GITCOMMIT fec3683
Source1:        https://github.com/krallin/tini/archive/tini-fec3683.tar.gz
%define sha1 tini=f7cc697bf7483fbc963c8331ab433d0758b766e9
Source2:        https://github.com/docker/libnetwork/archive/libnetwork-55685ba.tar.gz
%define sha1 libnetwork=11f4cce6793ff8f7b6caf5ed4c68a0eb9a33e32f

%define gopath_comp_engine github.com/docker/docker
%define gopath_comp_cli github.com/docker/cli
%define gopath_comp_libnetwork github.com/docker/libnetwork

Source99:       default-disable.preset
Patch99:        remove-firewalld-1809.patch
Patch98:        disable-docker-cli-md2man-install.patch
Patch97:        tini-disable-git.patch

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
Requires:       containerd >= 1.2.10, containerd < 1.5.0
Requires:       shadow

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
%setup -q -c
mkdir -p "$(dirname "src/%{gopath_comp_engine}")"
mkdir -p "$(dirname "src/%{gopath_comp_cli}")"
mkdir -p "src/%{gopath_comp_libnetwork}"
mkdir tini
mkdir bin
tar -C tini -xf %{SOURCE1}
cd tini
%patch97 -p1
cd -
tar -C src/%{gopath_comp_libnetwork} -xf %{SOURCE2}
cd %{name}-%{version}
%patch99 -p1
%patch98 -p1
mv components/engine ../src/%{gopath_comp_engine}
mv components/cli ../src/%{gopath_comp_cli}
mv components/packaging ../

%build
export GOPATH="$(pwd)"
export GO111MODULE=auto
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
  make dynbinary manpages
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
    . && make tini-static && cp tini-static "$GOPATH/bin/docker-init"
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
install -d -m755 %{buildroot}%{_localstatedir}/lib/docker-engine
install -d -m755 %{buildroot}/lib/udev/rules.d
install -d -m755 %{buildroot}%{_datadir}/bash-completion/completions

# install binary
install -p -m 755 "src/%{gopath_comp_cli}/build/docker" %{buildroot}%{_bindir}/docker
install -p -m 755 "src/%{gopath_comp_engine}/bundles/dynbinary-daemon/dockerd" %{buildroot}%{_bindir}/dockerd

# install proxy
install -p -m 755 bin/docker-proxy %{buildroot}%{_bindir}/docker-proxy

# install tini
install -p -m 755 bin/docker-init %{buildroot}%{_bindir}/docker-init

# install udev rules
install -p -m 644 src/%{gopath_comp_engine}/contrib/udev/80-docker.rules %{buildroot}/lib/udev/rules.d/80-docker.rules

# add init scripts
install -p -m 644 packaging/systemd/docker.service %{buildroot}%{_unitdir}/docker.service
install -p -m 644 packaging/systemd/docker.socket %{buildroot}%{_unitdir}/docker.socket

# add docker-engine metadata
install -p -m 644 distribution_based_engine.json %{buildroot}%{_localstatedir}/lib/docker-engine/distribution_based_engine.json

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

install -v -D -m 0644 %{SOURCE99} %{buildroot}%{_presetdir}/50-docker.preset

%pre engine
if [ $1 -gt 0 ] ; then
    # package upgrade scenario, before new files are installed

    # clear any old state
    rm -f %{_localstatedir}/lib/rpm-state/docker-is-active > /dev/null 2>&1 || :

    # check if docker service is running
    if systemctl is-active docker.service > /dev/null 2>&1; then
        systemctl stop docker > /dev/null 2>&1 || :
        touch %{_localstatedir}/lib/rpm-state/docker-is-active > /dev/null 2>&1 || :
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
    if [ -f %{_localstatedir}/lib/rpm-state/docker-is-active ]; then
        systemctl start docker > /dev/null 2>&1 || :
        rm -f %{_localstatedir}/lib/rpm-state/docker-is-active > /dev/null 2>&1 || :
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
/lib/udev/rules.d/80-docker.rules
%{_localstatedir}/lib/docker-engine/distribution_based_engine.json

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
*   Tue Jun 29 2021 Piyush Gupta <gpiyush@vmware.com> 18.09.9-9
-   Bump up version to compile with new go
*   Tue May 18 2021 Piyush Gupta<gpiyush@vmware.com> 18.09.9-8
-   Bump up version to compile with new go
*   Mon May 10 2021 Bo Gan <ganb@vmware.com> 18.09.9-7
-   Relax containerd dependency
*   Mon Feb 08 2021 Harinadh D <hdommaraju@vmware.com> 18.09.9-6
-   Bump up version to compile with new go
*   Fri Nov 27 2020 HarinadhD <hdommaraju@vmware.com> 18.09.9-5
-   Bump up version to compile with new go
*   Mon Jun 15 2020 Alexey Makhalov <amakhalov@vmware.com> 18.09.9-4
-   Requires: gawk
*   Mon May 04 2020 Harinadh D <hdommaraju@vmware.com> 18.09.9-3
-   Bump up version to compile with go 1.13.3-2
*   Mon Apr 27 2020 Ankit Jain <ankitja@vmware.com> 18.09.9-2
-   Added Requires shadow
-   To fix docker run command, libseccomp >= 2.4.0
*   Tue Oct 22 2019 Bo Gan <ganb@vmware.com> 18.09.9-1
-   Initial packaging for 18.09
-   Split daemon and cli into different RPMs
