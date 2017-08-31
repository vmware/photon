Summary:        Calico node and documentation for project calico.
Name:           calico
Version:        2.4.1
Release:        1%{?dist}
License:        Apache-2.0
URL:            https://github.com/projectcalico/calico
Source0:        %{name}-%{version}.tar.gz
%define sha1 calico=2d26dbc187819231ec0d0e0fe096d5eb78aee691
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon
BuildRequires:  git
BuildRequires:  glide
BuildRequires:  go >= 1.7
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
*   Wed Aug 16 2017 Vinay Kulkarni <kulkarniv@vmware.com> 2.4.1-1
-   Calico Node for PhotonOS.
