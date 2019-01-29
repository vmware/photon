Summary:        Calico node and documentation for project calico.
Name:           calico
Version:        2.6.7
Release:        4%{?dist}
License:        Apache-2.0
URL:            https://github.com/projectcalico/calico
Source0:        %{name}-%{version}.tar.gz
%define sha1 calico=d74b2103f84ed470322b5f33b75cf552db93d830
Source1:         go-27704.patch
Source2:         go-27842.patch
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon
BuildRequires:  git
BuildRequires:  glide
BuildRequires:  go = 1.9.7
BuildRequires:  make

%description
Calico node is a container that bundles together various components reqiured for networking containers using project calico. This includes key components such as felix agent for programming routes and ACLs, BIRD routing daemon, and confd datastore monitor engine.

%prep
%setup

%build
mkdir -p /root/.glide
mkdir -p ${GOPATH}/src/github.com/projectcalico/calico
cp -r * ${GOPATH}/src/github.com/projectcalico/calico/.
pushd ${GOPATH}/src/github.com/projectcalico/calico
cd calico_node
glide install --strip-vendor
pushd vendor/golang.org/x/net
patch -p1 < %{SOURCE1}
patch -p1 < %{SOURCE2}
popd
mkdir -p dist
mkdir -p .go-pkg-cache
make CALICO_GIT_VER=%{version} allocate-ipip-addr
make CALICO_GIT_VER=%{version} startup

%install
pushd ${GOPATH}/src/github.com/projectcalico/calico
install -vdm 755 %{buildroot}%{_bindir}
install calico_node/dist/allocate-ipip-addr %{buildroot}%{_bindir}/
install calico_node/dist/startup %{buildroot}%{_bindir}/
install -vdm 0755 %{buildroot}/usr/share/calico/docker/fs
cp -r calico_node/filesystem/etc %{buildroot}/usr/share/calico/docker/fs/
cp -r calico_node/filesystem/sbin %{buildroot}/usr/share/calico/docker/fs/
sed -i 's/. startup.env/source \/startup.env/g' %{buildroot}/usr/share/calico/docker/fs/etc/rc.local
sed -i 's/. startup.env/source \/startup.env/g' %{buildroot}/usr/share/calico/docker/fs/sbin/start_runit

%files
%defattr(-,root,root)
%{_bindir}/allocate-ipip-addr
%{_bindir}/startup
/usr/share/calico/docker/fs/*

%changelog
*   Mon Jan 28 2019 Bo Gan <ganb@vmware.com> 2.6.7-4
-   Fix CVE-2018-17846 and CVE-2018-17143
*   Mon Jan 21 2019 Bo Gan <ganb@vmware.com> 2.6.7-3
-   Build using go 1.9.7
*   Mon Sep 24 2018 Tapas Kundu <tkundu@vmware.com> 2.6.7-2
-   Build using go version 1.9
*   Fri May 18 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 2.6.7-1
-   Calico Node v2.6.7.
*   Tue Dec 05 2017 Vinay Kulkarni <kulkarniv@vmware.com> 2.6.3-1
-   Calico Node v2.6.3.
*   Fri Nov 03 2017 Vinay Kulkarni <kulkarniv@vmware.com> 2.6.2-1
-   Calico Node v2.6.2.
*   Wed Nov 01 2017 Vinay Kulkarni <kulkarniv@vmware.com> 2.5.1-1
-   Calico Node v2.5.1.
*   Wed Aug 16 2017 Vinay Kulkarni <kulkarniv@vmware.com> 2.4.1-1
-   Calico Node for PhotonOS.
