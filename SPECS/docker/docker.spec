%global security_hardening nopie
%define debug_package %{nil}
%define __os_install_post %{nil}
Summary:        Docker
Name:           docker
Version:        18.03.0
Release:        3%{?dist}
License:        ASL 2.0
URL:            http://docs.docker.com
Group:          Applications/File
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://github.com/docker/docker-ce/archive/docker-%{version}-ce.tar.gz
%define sha1 docker=873472d4b722aaf0e000ba0d0b1fa3d63d276ffc
%define DOCKER_GITCOMMIT 0520e243029d1361649afb0706a1c5d9a1c012b8
Source99:       default-disable.preset
Patch0:         fix-apparmor-not-being-applied-to-exec-processes.patch
Patch1:         CVE-2019-5736.patch
Patch99:        remove-firewalld.patch

BuildRequires:  systemd
BuildRequires:  device-mapper-devel
BuildRequires:  btrfs-progs-devel
BuildRequires:  libseccomp
BuildRequires:  libseccomp-devel
BuildRequires:  libltdl-devel
BuildRequires:  libgcc-devel
BuildRequires:  glibc-devel
BuildRequires:  unzip
BuildRequires:  go
BuildRequires:  sed
BuildRequires:  cmake
BuildRequires:  findutils
BuildRequires:  git
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

%patch0 -p1
%patch1 -p1
%patch99 -p1

mkdir -p /go/src/github.com
cd /go/src/github.com
mkdir opencontainers
mkdir docker

ln -snrf "$OLDPWD/components/engine" docker/docker
ln -snrf "$OLDPWD/components/cli" docker/cli

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
  RUNC_BUILDTAGS="seccomp" \
  hack/dockerfile/install/install.sh $component
done
DOCKER_BUILDTAGS="pkcs11 seccomp exclude_graphdriver_aufs" \
VERSION=%{version} DOCKER_GITCOMMIT=${GIT_COMMIT_SHORT} hack/make.sh dynbinary
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
install -p -m 755 "$(readlink -f components/cli/build/docker)" %{buildroot}%{_bindir}/docker
install -p -m 755 "$(readlink -f components/engine/bundles/latest/dynbinary-daemon/dockerd)" %{buildroot}%{_bindir}/dockerd

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
install -p -m 644 components/engine/contrib/udev/80-docker.rules %{buildroot}/lib/udev/rules.d/80-docker.rules

# add init scripts
install -p -m 644 components/packaging/rpm/systemd/docker.service %{buildroot}%{_unitdir}/docker.service

# add bash completions
install -p -m 644 components/cli/contrib/completion/bash/docker %{buildroot}%{_datadir}/bash-completion/completions/docker

# install manpages
install -p -m 644 components/cli/man/man1/*.1 %{buildroot}%{_mandir}/man1
install -p -m 644 components/cli/man/man5/*.5 %{buildroot}%{_mandir}/man5
install -p -m 644 components/cli/man/man8/*.8 %{buildroot}%{_mandir}/man8

# add vimfiles
install -d -m 755 %{buildroot}%{_datadir}/vim/vimfiles/doc
install -d -m 755 %{buildroot}%{_datadir}/vim/vimfiles/ftdetect
install -d -m 755 %{buildroot}%{_datadir}/vim/vimfiles/syntax
install -p -m 644 components/engine/contrib/syntax/vim/doc/dockerfile.txt %{buildroot}%{_datadir}/vim/vimfiles/doc/dockerfile.txt
install -p -m 644 components/engine/contrib/syntax/vim/ftdetect/dockerfile.vim %{buildroot}%{_datadir}/vim/vimfiles/ftdetect/dockerfile.vim
install -p -m 644 components/engine/contrib/syntax/vim/syntax/dockerfile.vim %{buildroot}%{_datadir}/vim/vimfiles/syntax/dockerfile.vim

mkdir -p build-docs
for engine_file in AUTHORS CHANGELOG.md CONTRIBUTING.md LICENSE MAINTAINERS NOTICE README.md; do
    cp "components/engine/$engine_file" "build-docs/engine-$engine_file"
done
for cli_file in LICENSE MAINTAINERS NOTICE README.md; do
    cp "components/cli/$cli_file" "build-docs/cli-$cli_file"
done

install -v -D -m 0644 %{SOURCE99} %{buildroot}%{_presetdir}/50-docker.preset

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
    getent group docker >/dev/null && groupdel docker
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
*   Mon Feb 11 2019 Him Kalyan Bordoloi <bordoloih@vmware.com> 18.03.0-3
-   Patch to fix CVE-2019-5736
*   Fri Sep 07 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 18.03.0-2
-   Fix apparmor not being applied to exec processes
*   Mon Apr 09 2018 Bo Gan <ganb@vmware.com> 18.03.0-1
-   Update to 18.03.0-ce
*   Mon Apr 09 2018 Bo Gan <ganb@vmware.com> 17.12.1-1
-   Update to 17.12.1-ce
*   Mon Apr 09 2018 Bo Gan <ganb@vmware.com> 17.09.1-1
-   Update to 17.09.1-ce
*   Mon Jan 15 2018 Bo Gan <ganb@vmware.com> 17.06.0-3
-   disable docker service by default
-   Fix post scriptlet to invoke systemd_post
*   Thu Dec 21 2017 Kumar Kaushik <kaushikk@vmware.com> 17.06.0-2
-   Applying patch for CVE-2017-14992
*   Tue Jul 18 2017 Bo Gan <ganb@vmware.com> 17.06.0-1
-   Update to 17.06.0-ce
*   Mon Jul 10 2017 Bo Gan <ganb@vmware.com> 1.13.1-4
-   Fix runc/containerd/libnetwork versions
-   Do not strip binaries
*   Thu May 04 2017 Kumar Kaushik <kaushikk@vmware.com> 1.13.1-3
-   Docker build requires GO.
*   Wed May 03 2017 Kumar Kaushik <kaushikk@vmware.com> 1.13.1-2
-   Fixing docker plugin runc version github issue # 640.
-   Adding docker group for non-sudo users, GitHub issue # 207.
*   Tue Apr 11 2017 Kumar Kaushik <kaushikk@vmware.com> 1.13.1-1
-   Building docker from source.
*   Fri Jan 13 2017 Xiaolin Li <xiaolinl@vmware.com> 1.12.6-1
-   Upgraded to version 1.12.6
*   Wed Sep 21 2016 Xiaolin Li <xiaolinl@vmware.com> 1.12.1-1
-   Upgraded to version 1.12.1
*   Mon Aug 22 2016 Alexey Makhalov <amakhalov@vmware.com> 1.12.0-2
-   Added bash completion file
*   Tue Aug 09 2016 Anish Swaminathan <anishs@vmware.com> 1.12.0-1
-   Upgraded to version 1.12.0
*   Tue Jun 28 2016 Anish Swaminathan <anishs@vmware.com> 1.11.2-1
-   Upgraded to version 1.11.2
*   Thu May 26 2016 Divya Thaluru <dthaluru@vmware.com>  1.11.0-6
-   Fixed logic to restart the active services after upgrade 
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.11.0-5
-   GA - Bump release of all rpms
*   Tue May 10 2016 Anish Swaminathan <anishs@vmware.com> 1.11.0-4
-   Remove commented post actions
*   Tue May 3 2016 Divya Thaluru <dthaluru@vmware.com>  1.11.0-3
-   Fixing spec file to handle rpm upgrade scenario correctly
*   Sat Apr 30 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.11.0-2
-   Add $DOCKER_OPTS to start in docker.service
*   Fri Apr 15 2016 Anish Swaminathan <anishs@vmware.com> 1.11.0-1
-   Updated to version 1.11.0.
*   Tue Feb 23 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 1.10.2-1
-   Upgraded to version 1.10.2
*   Thu Dec 10 2015 Xiaolin Li <xiaolinl@vmware.com>  1.9.0-2
-   Add systemd to Requires and BuildRequires.
-   Use systemctl to enable/disable service.
*   Fri Nov 06 2015 Vinay Kulkarni <kulkarniv@vmware.com> 1.9.0-1
-   Update to version 1.9.0
*   Mon Aug 17 2015 Divya Thaluru <dthaluru@vmware.com> 1.8.1-1
-   Update to new version 1.8.1.
*   Fri Jun 19 2015 Fabio Rapposelli <fabio@vmware.com> 1.7.0-1
-   Update to new version.
*   Mon May 18 2015 Touseef Liaqat <tliaqat@vmware.com> 1.6.0-3
-   Update according to UsrMove.
*   Fri May 15 2015 Divya Thaluru <dthaluru@vmware.com> 1.6.0-2
-   Updated to version 1.6
*   Wed Mar 4 2015 Divya Thaluru <dthaluru@vmware.com> 1.5.0-1
-   Initial build. First version
