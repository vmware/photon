Summary:        Docker
Name:           docker
Version:        1.13.1
Release:        2%{?dist}
License:        ASL 2.0
URL:            http://docs.docker.com
Group:          Applications/File
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://github.com/docker/docker/archive/%{name}-%{version}.tar.gz
%define sha1 docker=8a39c44c9e665495484fd86fbefdfbc9ab9d815d 
Source1:        https://github.com/docker/containerd/archive/containerd-0.2.5.tar.gz
%define sha1 containerd=aaf6fd1c5176b8575af1d8edf82af3d733528451
Source2:        https://github.com/opencontainers/runc/archive/runc-1.0.0-rc2.tar.gz
%define sha1 runc=27ab28ba1c81c4f2f62ed11601f8e3a2fafd229f
Source3:        https://github.com/docker/libnetwork/archive/docker-libnetwork-master-0.8.1.tar.gz
%define sha1 docker-libnetwork-master=231c59f72a17f5e3f33e75e1efa164623e1852d8
Source4:        docker.service
Source5:        docker-containerd.service
Source6:        docker-completion.bash

BuildRequires:  systemd
BuildRequires:  systemd-devel
BuildRequires:  device-mapper-devel
BuildRequires:  btrfs-progs-devel
BuildRequires:  libseccomp
BuildRequires:  libseccomp-devel
Requires:       libgcc
Requires:       glibc
Requires:       libseccomp
Requires:       systemd
Requires:       device-mapper-libs

%description
Docker is a platform for developers and sysadmins to develop, ship and run applications.
%prep
%setup -q
%setup -T -D -a 1
%setup -T -D -a 2
%setup -T -D -a 3

%build

export AUTO_GOPATH=1
export DOCKER_BUILDTAGS='exclude_graphdriver_aufs'
export DOCKER_GITCOMMIT="092cba3"

./hack/make.sh dynbinary

mkdir -p /usr/share/gocode/src/github.com/docker/
cd /usr/share/gocode/src/github.com/docker/
mv /usr/src/photon/BUILD/docker-1.13.1/containerd-0.2.5 .
mv containerd-0.2.5 containerd
cd containerd

make

mkdir -p /usr/share/gocode/src/github.com/opencontainers/
cd /usr/share/gocode/src/github.com/opencontainers/
mv /usr/src/photon/BUILD/docker-1.13.1/runc-1.0.0-rc2 .
mv runc-1.0.0-rc2 runc
cd runc
make BUILDTAGS='seccomp'

cd /usr/share/gocode/src/github.com/docker/
mv /usr/src/photon/BUILD/docker-1.13.1/libnetwork-master/ .
mv libnetwork-master libnetwork
cd libnetwork
go build -ldflags="-linkmode=external" -o docker-proxy github.com/docker/libnetwork/cmd/proxy

%install
install -vdm755 %{buildroot}/usr/bin
mv -v %{_builddir}/%{name}-%{version}/bundles/latest/dynbinary-client/%{name}-%{version} %{buildroot}/usr/bin/%{name}
mv -v %{_builddir}/%{name}-%{version}/bundles/latest/dynbinary-daemon/%{name}d-%{version} %{buildroot}/usr/bin/%{name}d
mv -v /usr/share/gocode/src/github.com/docker/containerd/bin/containerd %{buildroot}/usr/bin/%{name}-containerd
mv -v /usr/share/gocode/src/github.com/docker/containerd/bin/containerd-shim %{buildroot}/usr/bin/%{name}-containerd-shim
mv -v /usr/share/gocode/src/github.com/docker/containerd/bin/ctr %{buildroot}/usr/bin/%{name}-containerd-ctr
mv -v /usr/share/gocode/src/github.com/opencontainers/runc/runc %{buildroot}/usr/bin/%{name}-runc
mv -v /usr/share/gocode/src/github.com/docker/libnetwork/docker-proxy %{buildroot}/usr/bin/%{name}-proxy
install -vd %{buildroot}/lib/systemd/system
cp %{SOURCE4} %{buildroot}/lib/systemd/system/docker.service
cp %{SOURCE5} %{buildroot}/lib/systemd/system/docker-containerd.service
install -vdm 755 %{buildroot}%{_datadir}/bash-completion/completions
install -m 0644 %{SOURCE6} %{buildroot}%{_datadir}/bash-completion/completions/docker

%{_fixperms} %{buildroot}/*

%preun
%systemd_preun docker.service
%systemd_preun docker-containerd.service

%post
/sbin/ldconfig

if [ $1 -eq 1 ] ; then
  groupadd docker
  useradd -g docker photon-docker
fi

%postun
/sbin/ldconfig
%systemd_postun_with_restart docker-containerd.service
%systemd_postun_with_restart docker.service

if [ $1 -eq 0 ] ; then
  userdel photon-docker
  groupdel docker
fi

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
/lib/systemd/system/docker-containerd.service
/lib/systemd/system/docker.service
/usr/bin
/usr/bin/docker
/usr/bin/docker-containerd
/usr/bin/docker-containerd-ctr
/usr/bin/docker-containerd-shim
/usr/bin/docker-proxy
/usr/bin/docker-runc
/usr/bin/dockerd
/usr/share/bash-completion/completions/docker

%changelog
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
