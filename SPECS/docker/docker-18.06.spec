%global security_hardening nopie
%define debug_package %{nil}
%define __os_install_post %{nil}
Summary:        Docker
Name:           docker
Version:        18.06.2
Release:        2%{?dist}
License:        ASL 2.0
URL:            http://docs.docker.com
Group:          Applications/File
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://github.com/docker/docker-ce/archive/docker-%{version}-ce.tar.gz
%define sha1 docker=d67890d32c8e4ee09bf2a00585d95211d8def486
%define DOCKER_GITCOMMIT 6d37f41e333ee478440ef969392020f7e3915cd3
Source99:       default-disable.preset
Patch99:        remove-firewalld.patch

BuildRequires:  systemd
BuildRequires:  systemd-devel
BuildRequires:  device-mapper-devel
BuildRequires:  btrfs-progs-devel
BuildRequires:  libseccomp
BuildRequires:  libseccomp-devel
BuildRequires:  libltdl-devel
BuildRequires:  libgcc-devel
BuildRequires:  glibc-devel
BuildRequires:  unzip
BuildRequires:  go = 1.10.7
BuildRequires:  sed
BuildRequires:  cmake
BuildRequires:  findutils
BuildRequires:  git
BuildRequires:  libapparmor
BuildRequires:  libapparmor-devel
Requires:       libapparmor
Requires:       libltdl
Requires:       libgcc
Requires:       glibc
Requires:       libseccomp
Requires:       systemd
Requires:       device-mapper-libs

%description
Docker is an open source project to build, ship and run any application as a lightweight container.

%package        doc
Summary:        Documentation and vimfiles for docker
Requires:       %{name} = %{version}

%description    doc
Documentation and vimfiles for docker

%prep
%setup -q -c

%patch99 -p1

mkdir -p /go/src/github.com
cd /go/src/github.com
mkdir opencontainers
mkdir docker

ln -snrf "$OLDPWD/docker-ce-%{version}-ce/components/engine" docker/docker
ln -snrf "$OLDPWD/docker-ce-%{version}-ce/components/cli" docker/cli

%build
export GOPATH="/go"
export PATH="$PATH:$GOPATH/bin"

GIT_COMMIT=%{DOCKER_GITCOMMIT}
GIT_COMMIT_SHORT=${GIT_COMMIT:0:7}

cd "$GOPATH/src/github.com/docker"

pushd cli
DISABLE_WARN_OUTSIDE_CONTAINER=1 make VERSION=%{version} GITCOMMIT=${GIT_COMMIT_SHORT} dynbinary manpages
popd

pushd docker
for component in tini "proxy dynamic" "runc all" "containerd dynamic"; do
  RUNC_BUILDTAGS="seccomp apparmor" \
  hack/dockerfile/install/install.sh $component
done
DOCKER_BUILDTAGS="pkcs11 seccomp apparmor exclude_graphdriver_aufs" \
VERSION=%{version}-ce DOCKER_GITCOMMIT=${GIT_COMMIT_SHORT} PRODUCT=docker hack/make.sh dynbinary
popd

%install
install -d -m755 %{buildroot}%{_mandir}/man1
install -d -m755 %{buildroot}%{_mandir}/man5
install -d -m755 %{buildroot}%{_mandir}/man8
install -d -m755 %{buildroot}%{_bindir}
install -d -m755 %{buildroot}%{_unitdir}
install -d -m755 %{buildroot}/lib/udev/rules.d
install -d -m755 %{buildroot}%{_datadir}/bash-completion/completions

# install binary
install -p -m 755 "$(readlink -f docker-ce-%{version}-ce/components/cli/build/docker)" %{buildroot}%{_bindir}/docker
install -p -m 755 "$(readlink -f docker-ce-%{version}-ce/components/engine/bundles/latest/dynbinary-daemon/dockerd)" %{buildroot}%{_bindir}/dockerd

# install proxy
install -p -m 755 /usr/local/bin/docker-proxy %{buildroot}%{_bindir}/docker-proxy

# install containerd
install -p -m 755 /usr/local/bin/docker-containerd %{buildroot}%{_bindir}/docker-containerd
install -p -m 755 /usr/local/bin/docker-containerd-shim %{buildroot}%{_bindir}/docker-containerd-shim
install -p -m 755 /usr/local/bin/docker-containerd-ctr %{buildroot}%{_bindir}/docker-containerd-ctr

# install runc
install -p -m 755 /usr/local/bin/docker-runc %{buildroot}%{_bindir}/docker-runc

# install tini
install -p -m 755 /usr/local/bin/docker-init %{buildroot}%{_bindir}/docker-init

# install udev rules
install -p -m 644 docker-ce-%{version}-ce/components/engine/contrib/udev/80-docker.rules %{buildroot}/lib/udev/rules.d/80-docker.rules

# add init scripts
install -p -m 644 docker-ce-%{version}-ce/components/packaging/rpm/systemd/docker.service %{buildroot}%{_unitdir}/docker.service

# add bash completions
install -p -m 644 docker-ce-%{version}-ce/components/cli/contrib/completion/bash/docker %{buildroot}%{_datadir}/bash-completion/completions/docker

# install manpages
install -p -m 644 docker-ce-%{version}-ce/components/cli/man/man1/*.1 %{buildroot}%{_mandir}/man1
install -p -m 644 docker-ce-%{version}-ce/components/cli/man/man5/*.5 %{buildroot}%{_mandir}/man5
install -p -m 644 docker-ce-%{version}-ce/components/cli/man/man8/*.8 %{buildroot}%{_mandir}/man8

# add vimfiles
install -d -m 755 %{buildroot}%{_datadir}/vim/vimfiles/doc
install -d -m 755 %{buildroot}%{_datadir}/vim/vimfiles/ftdetect
install -d -m 755 %{buildroot}%{_datadir}/vim/vimfiles/syntax
install -p -m 644 docker-ce-%{version}-ce/components/engine/contrib/syntax/vim/doc/dockerfile.txt %{buildroot}%{_datadir}/vim/vimfiles/doc/dockerfile.txt
install -p -m 644 docker-ce-%{version}-ce/components/engine/contrib/syntax/vim/ftdetect/dockerfile.vim %{buildroot}%{_datadir}/vim/vimfiles/ftdetect/dockerfile.vim
install -p -m 644 docker-ce-%{version}-ce/components/engine/contrib/syntax/vim/syntax/dockerfile.vim %{buildroot}%{_datadir}/vim/vimfiles/syntax/dockerfile.vim

mkdir -p build-docs
for engine_file in AUTHORS CHANGELOG.md CONTRIBUTING.md LICENSE MAINTAINERS NOTICE README.md; do
    cp "docker-ce-%{version}-ce/components/engine/$engine_file" "build-docs/engine-$engine_file"
done
for cli_file in LICENSE MAINTAINERS NOTICE README.md; do
    cp "docker-ce-%{version}-ce/components/cli/$cli_file" "build-docs/cli-$cli_file"
done

install -v -D -m 0644 %{SOURCE99} %{buildroot}%{_presetdir}/50-docker.preset

%pre
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

%preun
%systemd_preun docker.service

%post
if [ $1 -eq 1 ] ; then
    getent group docker >/dev/null || groupadd -r docker
fi
%systemd_post docker.service

%postun
%systemd_postun_with_restart docker.service
if [ $1 -eq 0 ] ; then
    getent group docker >/dev/null && groupdel docker || :
fi

%posttrans
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
%{_unitdir}/docker.service
%{_presetdir}/50-docker.preset
%{_bindir}/docker
%{_bindir}/dockerd
%{_bindir}/docker-containerd
%{_bindir}/docker-containerd-ctr
%{_bindir}/docker-containerd-shim
%{_bindir}/docker-proxy
%{_bindir}/docker-runc
%{_bindir}/docker-init
%{_datadir}/bash-completion/completions/docker
/lib/udev/rules.d/80-docker.rules

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
*   Thu Feb 14 2019 Bo Gan <ganb@vmware.com> 18.06.2-2
-   Fix docker version string
*   Mon Feb 11 2019 Him Kalyan Bordoloi <bordoloih@vmware.com> 18.06.2-1
-   Upgrade Docker to fix CVE-2019-5736
*   Mon Jan 21 2019 Bo Gan <ganb@vmware.com> 18.06.1-2
-   Build using go 1.10.7
*   Mon Jan 17 2019 Bo Gan <ganb@vmware.com> 18.06.1-1
-   Update to 18.06.1-ce
