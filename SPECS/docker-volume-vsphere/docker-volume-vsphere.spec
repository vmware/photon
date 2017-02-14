Summary:        vSphere Docker Volume Service
Name:           docker-volume-vsphere
Version:        0.11
Release:        1%{?dist}
License:        Apache 2.0
URL:            https://github.com/vmware/docker-volume-vsphere
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        %{name}-%{version}.tar.gz
%define sha1    docker-volume-vsphere=79ce62b5a809ab4d3238c4ce4ee9cec24bc6a5b0

BuildRequires:  go

%description
vSphere Docker Volume Service enables customers to address persistent storage requirements for Docker containers in vSphere environments.
%prep
%setup -q

%build
cd ..
mkdir  mkdir -p build/src/github.com/vmware/docker-volume-vsphere
cp -r docker-volume-vsphere-0.11/* build/src/github.com/vmware/docker-volume-vsphere/.
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
cp ./misc/scripts/install/docker-volume-vsphere.service %{buildroot}/%{_libdir}/systemd/system/.

%post
%systemd_post docker-volume-vsphere.service

%preun
%systemd_preun docker-volume-vsphere.service

%postun
%systemd_postun_with_restart docker-volume-vsphere.service

%files
%defattr(-,root,root)
%{_lib}/systemd/system/*
/usr/local/bin/*



%changelog
*   Mon Feb 13 2017 Xiaolin Li <xiaolinl@vmware.com> 0.11-1
-   Initial version
