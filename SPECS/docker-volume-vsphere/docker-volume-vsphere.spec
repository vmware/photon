Summary:        vSphere Docker Volume Service
Name:           docker-volume-vsphere
Version:        0.12
Release:        2%{?dist}
License:        Apache 2.0
URL:            https://github.com/vmware/docker-volume-vsphere
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        %{name}-%{version}.tar.gz
%define sha1    docker-volume-vsphere=3182700280e8f6589c7402b30dc237172af5a249

BuildRequires:  go

%description
vSphere Docker Volume Service enables customers to address persistent storage requirements for Docker containers in vSphere environments.
%prep
%setup -q

%build
cd ..
mkdir  mkdir -p build/src/github.com/vmware/docker-volume-vsphere
cp -r docker-volume-vsphere-0.12/* build/src/github.com/vmware/docker-volume-vsphere/.
cd build
mkdir bin
export GOPATH=`pwd`
cd bin
export GOBIN=`pwd`
export PATH=$PATH:$GOBIN
cd ../src/github.com/vmware/docker-volume-vsphere/vmdk_plugin
go build
go install

%install
mkdir -p %{buildroot}/usr/local/bin
mkdir -p %{buildroot}/%{_libdir}/systemd/system
cp ../build/bin/vmdk_plugin %{buildroot}/usr/local/bin/docker-volume-vsphere
chmod 755 %{buildroot}/usr/local/bin/docker-volume-vsphere
cp ./misc/scripts/install/*.sh %{buildroot}/usr/local/bin/.
chmod 755 %{buildroot}/usr/local/bin/*.sh
cp ./misc/scripts/install/docker-volume-vsphere.service %{buildroot}/%{_libdir}/systemd/system/.

%post
/usr/local/bin/after-install.sh

%preun
/usr/local/bin/before-remove.sh

%files
%defattr(-,root,root)
%{_lib}/systemd/system/*
/usr/local/bin/*

%changelog
*   Thu Jun 01 2017 Xiaolin Li <xiaolinl@vmware.com> 0.12-2
-   Use scripts from docker-volume-vsphere as post and preun scriptlets.
*   Wed Mar 29 2017 Chang Lee <changlee@vmware.com> 0.12-1
-   update to version 0.12
*   Mon Feb 13 2017 Xiaolin Li <xiaolinl@vmware.com> 0.11-1
-   Initial version
