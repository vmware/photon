Summary:        Calico node and documentation for project calico.
Name:           calico
Version:        3.6.1
Release:        1%{?dist}
License:        Apache-2.0
URL:            https://github.com/projectcalico/calico
Source0:        %{name}-%{version}.tar.gz
%define sha1 calico=43310c3ae20b7806ae030d11ae99c135a35badac
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon
BuildRequires:  git
BuildRequires:  glide
BuildRequires:  go >= 1.11
BuildRequires:  make

%description
Calico node is a container that bundles together various components reqiured for networking containers using project calico. This includes key components such as felix agent for programming routes and ACLs, BIRD routing daemon, and confd datastore monitor engine. 

%prep
%setup -n node-%{version}

%build
mkdir -p /root/.glide
mkdir -p ${GOPATH}/src/github.com/projectcalico/node
cp -r * ${GOPATH}/src/github.com/projectcalico/node
pushd ${GOPATH}/src/github.com/projectcalico/node
glide install --strip-vendor
mkdir -p dist
mkdir -p .go-pkg-cache
GOOS=linux GOARCH=amd64 CGO_ENABLED=0 go build -v -i -o dist/calico-node cmd/calico-node/main.go
popd

%install
pushd ${GOPATH}/src/github.com/projectcalico
install -vdm 755 %{buildroot}%{_bindir}
install node/dist/calico-node %{buildroot}%{_bindir}/
install -vdm 0755 %{buildroot}/usr/share/calico/docker/fs
cp -r node/filesystem/etc %{buildroot}/usr/share/calico/docker/fs/
cp -r node/filesystem/sbin %{buildroot}/usr/share/calico/docker/fs/
sed -i 's/. startup.env/source \/startup.env/g' %{buildroot}/usr/share/calico/docker/fs/etc/rc.local
sed -i 's/. startup.env/source \/startup.env/g' %{buildroot}/usr/share/calico/docker/fs/sbin/start_runit

%files
%defattr(-,root,root)
%{_bindir}/calico-node
/usr/share/calico/docker/fs/*

%changelog
*   Thu Apr 11 2019 Ashwin H <ashwinh@vmware.com> 3.6.1-1
-   Update to 3.6.1
*   Mon Aug 06 2018 Dheeraj Shetty <dheerajs@vmware.com> 2.6.7-2
-   Build using go version 1.9.4
*   Tue Mar 20 2018 Dheeraj Shetty <dheerajs@vmware.com> 2.6.7-1
-   Calico Node v2.6.7.
*   Tue Dec 05 2017 Vinay Kulkarni <kulkarniv@vmware.com> 2.6.3-1
-   Calico Node v2.6.3.
*   Fri Nov 03 2017 Vinay Kulkarni <kulkarniv@vmware.com> 2.6.2-1
-   Calico Node v2.6.2.
*   Wed Nov 01 2017 Vinay Kulkarni <kulkarniv@vmware.com> 2.5.1-1
-   Calico Node v2.5.1.
*   Wed Aug 16 2017 Vinay Kulkarni <kulkarniv@vmware.com> 2.4.1-1
-   Calico Node for PhotonOS.
