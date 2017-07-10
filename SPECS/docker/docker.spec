%define debug_package %{nil}
%define __os_install_post %{nil}
Summary:        Docker
Name:           docker
Version:        1.13.1
Release:        4%{?dist}
License:        ASL 2.0
URL:            http://docs.docker.com
Group:          Applications/File
Vendor:         VMware, Inc.
Distribution:   Photon
#Git commits must be in sync with docker/hack/dockerfile/binaries-commits
Source0:        https://github.com/docker/moby/archive/moby-%{version}.tar.gz
%define sha1 moby=eb67f8c60bd132d8917335ebf92d90020ba52d27
%define DOCKER_COMMIT 092cba3
Source1:        https://github.com/docker/containerd/tree/containerd-aa8187d.tar.gz
%define CONTAINERD_COMMIT aa8187dbd3b7ad67d8e5e3a15115d3eef43a7ed1
%define sha1 containerd=b8aac40b423e80028ec6b7ff5cca1ccaab617d86
Source2:        https://github.com/docker/runc/tree/runc-9df8b30.tar.gz
%define sha1 runc=35d0c90f634d2327356e7268ff73ecbffdd65d82
%define RUNC_COMMIT 9df8b306d01f59d3a8029be411de015b7304dd8f
Source3:        https://github.com/docker/libnetwork/tree/libnetwork-0f53435.tar.gz
%define sha1 libnetwork=a63774a38bec3aba4b1ff7a0b3e748960da2048b
%define LIBNETWORK_COMMIT 0f534354b813003a754606689722fe253101bc4e
Source4:        docker.service
Source5:        docker-containerd.service
Source6:        docker-completion.bash

BuildRequires:  systemd
BuildRequires:  device-mapper-devel
BuildRequires:  btrfs-progs-devel
BuildRequires:  libseccomp
BuildRequires:  libseccomp-devel
BuildRequires:  unzip
BuildRequires:  go
BuildRequires:  findutils
BuildRequires:  sed
Requires:       libgcc
Requires:       glibc
Requires:       libseccomp
Requires:       systemd
Requires:       device-mapper-libs

%description
Docker is a platform for developers and sysadmins to develop, ship and run applications.
%prep
%setup -q -c
%setup -T -D -a 1
%setup -T -D -a 2
%setup -T -D -a 3

#Fix containerd git commit/branch
find containerd-%{CONTAINERD_COMMIT} -name Makefile \
  -exec sed -i 's/^GIT_COMMIT :=.*$/GIT_COMMIT := %{CONTAINERD_COMMIT}/g' {} \; \
  -exec sed -i 's/^GIT_BRANCH :=.*$/GIT_BRANCH := %{name}-%{version}/g' {} \;

#Fix runc git commit/branch
find runc-%{RUNC_COMMIT} -name Makefile \
  -exec sed -i 's/^GIT_COMMIT :=.*$/GIT_COMMIT := %{RUNC_COMMIT}/g' {} \; \
  -exec sed -i 's/^COMMIT :=.*$/COMMIT := %{RUNC_COMMIT}/g' {} \; \
  -exec sed -i 's/^COMMIT_NO :=.*$/COMMIT_NO := %{RUNC_COMMIT}/g' {} \; \
  -exec sed -i 's/^GIT_BRANCH :=.*$/GIT_BRANCH := %{name}-%{version}/g' {} \;

#Fix docker git commit/branch
find moby-%{version} -name Makefile \
  -exec sed -i 's/^GIT_COMMIT :=.*$/GIT_COMMIT := %{DOCKER_COMMIT}/g' {} \; \
  -exec sed -i 's/^GIT_BRANCH :=.*$/GIT_BRANCH := %{name}-%{version}/g' {} \;

#Fail if there is still "shell git" invocation
find -name Makefile -exec grep "shell git" {} \; | read && exit 1

%build

export GOPATH="${PWD}/gopath"
mkdir -p gopath/src/github.com
cd gopath/src/github.com
mkdir -p docker
mkdir -p opencontainers

ln -snrf ../../../runc-%{RUNC_COMMIT} opencontainers/runc
ln -snrf ../../../containerd-%{CONTAINERD_COMMIT} docker/containerd
ln -snrf ../../../libnetwork-%{LIBNETWORK_COMMIT} docker/libnetwork
ln -snrf ../../../moby-%{version} docker/docker

pushd docker/docker
DOCKER_GITCOMMIT=%{DOCKER_COMMIT} DOCKER_BUILDTAGS='exclude_graphdriver_aufs seccomp' ./hack/make.sh dynbinary
popd

pushd docker/containerd
make
popd

pushd opencontainers/runc
make BUILDTAGS='seccomp'
popd

pushd docker/libnetwork
go build -ldflags="-linkmode=external" -o docker-proxy github.com/docker/libnetwork/cmd/proxy
popd

%install

install -vdm755 %{buildroot}%{_bindir}
install -vdm755 %{buildroot}%{_unitdir}
install -vdm755 %{buildroot}%{_datadir}/bash-completion/completions

pushd gopath/src/github.com/docker
install -m755 docker/bundles/latest/dynbinary-client/%{name}-%{version} %{buildroot}%{_bindir}/%{name}
install -m755 docker/bundles/latest/dynbinary-daemon/%{name}d-%{version} %{buildroot}%{_bindir}/%{name}d
install -m755 containerd/bin/containerd %{buildroot}%{_bindir}/%{name}-containerd
install -m755 containerd/bin/containerd-shim %{buildroot}%{_bindir}/%{name}-containerd-shim
install -m755 containerd/bin/ctr %{buildroot}%{_bindir}/%{name}-containerd-ctr
install -m755 libnetwork/docker-proxy %{buildroot}%{_bindir}/%{name}-proxy
popd

pushd gopath/src/github.com/opencontainers
install -m755 runc/runc %{buildroot}%{_bindir}/%{name}-runc
popd

install -m644 %{SOURCE4} %{buildroot}%{_unitdir}/docker.service
install -m644 %{SOURCE5} %{buildroot}%{_unitdir}/docker-containerd.service
install -m644 %{SOURCE6} %{buildroot}%{_datadir}/bash-completion/completions/docker

#%{_fixperms} %{buildroot}/*

%preun
%systemd_preun docker.service
%systemd_preun docker-containerd.service

%post
/sbin/ldconfig

if [ $1 -eq 1 ] ; then
    getent group  docker  >/dev/null || groupadd -r docker
fi

%postun
/sbin/ldconfig
%systemd_postun_with_restart docker-containerd.service
%systemd_postun_with_restart docker.service

if [ $1 -eq 0 ] ; then
    if getent group docker >/dev/null; then
        groupdel docker
    fi
fi

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_unitdir}/docker-containerd.service
%{_unitdir}/docker.service
%{_bindir}/docker
%{_bindir}/docker-containerd
%{_bindir}/docker-containerd-ctr
%{_bindir}/docker-containerd-shim
%{_bindir}/docker-proxy
%{_bindir}/docker-runc
%{_bindir}/dockerd
%{_datadir}/bash-completion/completions/docker

%changelog
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
