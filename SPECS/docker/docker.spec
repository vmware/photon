%global security_hardening nopie
%define debug_package %{nil}
%define __os_install_post %{nil}
Summary:        Docker
Name:           docker
Version:        17.06.0
Release:        7%{?dist}
License:        ASL 2.0
URL:            http://docs.docker.com
Group:          Applications/File
Vendor:         VMware, Inc.
Distribution:   Photon
#Git commits must be in sync with docker/hack/dockerfile/binaries-commits
Source0:        https://github.com/docker/moby/archive/docker-ce-02c1d87.tar.gz
%define sha1 docker-ce=40deab51330b39d16abc23831063a6123ff0a570
Source1:        https://github.com/docker/containerd/tree/containerd-cfb82a8.tar.gz
%define sha1 containerd=2adb56ddd2d89af5c6ab649de93c34d421b62649
Source2:        https://github.com/docker/runc/tree/runc-2d41c04.tar.gz
%define sha1 runc=41cd104b168cef29032c268e0d6de1bad5dadc25
Source3:        https://github.com/docker/libnetwork/tree/libnetwork-7b2b1fe.tar.gz
%define sha1 libnetwork=0afeb8c802998344753fb933f827427da23975f8
#Source4:        https://github.com/docker/cli/tree/cli-3dfb834.tar.gz
#%define sha1 cli=9dd33ca7d8e554fe875138000c6767167228e125
Source4:        https://github.com/krallin/tini/tree/tini-949e6fa.tar.gz
%define sha1 tini=e1a0e72ff74e1486e0701dd52983014777a7d949
Source5:        https://github.com/cpuguy83/go-md2man/tree/go-md2man-a65d4d2.tar.gz
%define sha1 go-md2man=e3d0865c583150f7c76e385a8b4a3f2432ca8ad8
Source6:        default-disable.preset
Patch0:         remove-firewalld.patch
Patch1:         fix-apparmor-not-being-applied-to-exec-processes.patch

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
BuildRequires:  go = 1.9.4
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
Docker is a platform for developers and sysadmins to develop, ship and run applications.

%package        doc
Summary:        Documentation and vimfiles for docker
Requires:       %{name} = %{version}

%description    doc
Documentation and vimfiles for docker

%prep
%setup -q -c
%setup -T -D -a 1
%setup -T -D -a 2
%setup -T -D -a 3
%setup -T -D -a 4
%setup -T -D -a 5

ln -s docker-ce/components/cli cli
ln -s docker-ce/components/engine engine
ln -s docker-ce/components/packaging packaging

%patch0 -p2
%patch1 -p2

mkdir -p /go/src/github.com
cd /go/src/github.com
mkdir opencontainers
mkdir containerd
mkdir cpuguy83
mkdir docker

ln -snrf "$OLDPWD/containerd" containerd/
ln -snrf "$OLDPWD/engine" docker/docker
ln -snrf "$OLDPWD/runc" opencontainers/
ln -snrf "$OLDPWD/go-md2man" cpuguy83/
ln -snrf "$OLDPWD/libnetwork" docker/
ln -snrf "$OLDPWD/cli" docker/

ln -snrf "$OLDPWD/tini" /go/

sed -i '/^\s*git clone.*$/d' docker/docker/hack/dockerfile/install-binaries.sh

#catch git clone
git config --global http.proxy http://localhost:0

%build

export GOPATH="/go"
export PATH="$PATH:$GOPATH/bin"

export DOCKER_BUILDTAGS="pkcs11 seccomp apparmor exclude_graphdriver_aufs"
export RUNC_BUILDTAGS="seccomp apparmor"

cd /go/src/github.com

pushd docker/cli
make VERSION="$(cat VERSION)" dynbinary manpages
popd

pushd docker/docker
TMP_GOPATH="$GOPATH" ./hack/dockerfile/install-binaries.sh runc-dynamic containerd-dynamic proxy-dynamic tini
DOCKER_GITCOMMIT="$(git rev-parse --short HEAD)" ./hack/make.sh dynbinary
popd

%install

install -d -m755 %{buildroot}%{_mandir}/man1
install -d -m755 %{buildroot}%{_mandir}/man5
install -d -m755 %{buildroot}%{_mandir}/man8
install -d -m755 %{buildroot}%{_bindir}
install -d -m755 %{buildroot}%{_unitdir}
install -d -m755 %{buildroot}lib/udev/rules.d
install -d -m755 %{buildroot}%{_datadir}/bash-completion/completions

# install binary
install -p -m 755 cli/build/docker %{buildroot}%{_bindir}/docker
install -p -m 755 "$(readlink -f engine/bundles/latest/dynbinary-daemon/dockerd)" %{buildroot}%{_bindir}/dockerd

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
install -p -m 644 engine/contrib/udev/80-docker.rules %{buildroot}lib/udev/rules.d/80-docker.rules

# add init scripts
install -p -m 644 packaging/rpm/systemd/docker.service %{buildroot}%{_unitdir}/docker.service

# add bash, zsh, and fish completions
install -p -m 644 engine/contrib/completion/bash/docker %{buildroot}%{_datadir}/bash-completion/completions/docker

# install manpages
install -p -m 644 cli/man/man1/*.1 %{buildroot}%{_mandir}/man1
install -p -m 644 cli/man/man5/*.5 %{buildroot}%{_mandir}/man5
install -p -m 644 cli/man/man8/*.8 %{buildroot}%{_mandir}/man8

# add vimfiles
install -d -m 755 %{buildroot}%{_datadir}/vim/vimfiles/doc
install -d -m 755 %{buildroot}%{_datadir}/vim/vimfiles/ftdetect
install -d -m 755 %{buildroot}%{_datadir}/vim/vimfiles/syntax
install -p -m 644 engine/contrib/syntax/vim/doc/dockerfile.txt %{buildroot}%{_datadir}/vim/vimfiles/doc/dockerfile.txt
install -p -m 644 engine/contrib/syntax/vim/ftdetect/dockerfile.vim %{buildroot}%{_datadir}/vim/vimfiles/ftdetect/dockerfile.vim
install -p -m 644 engine/contrib/syntax/vim/syntax/dockerfile.vim %{buildroot}%{_datadir}/vim/vimfiles/syntax/dockerfile.vim

mkdir -p build-docs
for engine_file in AUTHORS CHANGELOG.md CONTRIBUTING.md LICENSE MAINTAINERS NOTICE README.md; do
    cp "engine/$engine_file" "build-docs/engine-$engine_file"
done
for cli_file in LICENSE MAINTAINERS NOTICE README.md; do
    cp "cli/$cli_file" "build-docs/cli-$cli_file"
done

install -v -D -m 0644 %{SOURCE6} %{buildroot}%{_presetdir}/50-docker.preset

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
*   Tue Sep 25 2018 Tapas Kundu <tkundu@vmware.com> 17.06.0-7
-   Use go 1.9 rather than latest go toolchain
*   Thu Sep 20 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 17.06.0-6
-   Fix AppArmor not being applied to exec processes.
*   Thu Aug 30 2018 Keerthana K <keerthanak@vmware.com> 17.06.0-5
-   Updated BuildTags to include apparmor.
*   Fri Sep 22 2017 Bo Gan <ganb@vmware.com> 17.06.0-4
-   disable docker service by default
*   Fri Sep 08 2017 Bo Gan <ganb@vmware.com> 17.06.0-3
-   Fix post scriptlet to invoke systemd_post
*   Mon Aug 28 2017 Alexey Makhalov <amakhalov@vmware.com> 17.06.0-2
-   Use nopie option to build
*   Tue Jul 18 2017 Bo Gan <ganb@vmware.com> 17.06.0-1
-   Update to 17.06.0-ce
*   Thu May 04 2017 Kumar Kaushik <kaushikk@vmware.com> 1.13.1-4
-   Adding build requires GO.
*   Wed May 03 2017 Kumar Kaushik <kaushikk@vmware.com> 1.13.1-3
-   Fixing docker plugin runc version github issue # 640.
*   Mon Apr 24 2017 Kumar Kaushik <kaushikk@vmware.com> 1.13.1-2
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
