Summary:        Calico node and documentation for project calico.
Name:           calico
Version:        3.15.2
Release:        2%{?dist}
License:        Apache-2.0
URL:            https://github.com/projectcalico/node
Source0:        %{name}-%{version}.tar.gz
%define sha1 calico=269368d04748548fcdd22dccbf2bd81d76535ed3
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon
BuildRequires:  git
BuildRequires:  go
BuildRequires:  make

%description
Calico node is a container that bundles together various components reqiured for networking containers using project calico. This includes key components such as felix agent for programming routes and ACLs, BIRD routing daemon, and confd datastore monitor engine.

%prep
%setup -n node-%{version}

%build
export GO111MODULE=auto
mkdir -p dist
go build -v -i -o dist/calico-node cmd/calico-node/main.go

%install
install -vdm 755 %{buildroot}%{_bindir}
install dist/calico-node %{buildroot}%{_bindir}/
install -vdm 0755 %{buildroot}/usr/share/calico/docker/fs
cp -r filesystem/etc %{buildroot}/usr/share/calico/docker/fs/
cp -r filesystem/sbin %{buildroot}/usr/share/calico/docker/fs/
sed -i 's/. startup.env/source \/startup.env/g' %{buildroot}/usr/share/calico/docker/fs/etc/rc.local
sed -i 's/. startup.env/source \/startup.env/g' %{buildroot}/usr/share/calico/docker/fs/sbin/start_runit

%files
%defattr(-,root,root)
%{_bindir}/calico-node
/usr/share/calico/docker/fs/*

%changelog
*   Wed Jun 02 2021 Piyush Gupta<gpiyush@vmware.com> 3.15.2-2
-   Bump up version to compile with new go
*   Tue May 25 2021 Prashant S Chauhan <psinghchauha@vmware.com> 3.15.2-1
-   Update to 3.15.2
*   Mon Feb 08 2021 Harinadh D <hdommaraju@vmware.com> 3.6.1-7
-   Bump up version to compile with new go
*   Fri Nov 27 2020 HarinadhD <hdommaraju@vmware.com> 3.6.1-6
-   Bump up version to compile with new go
*   Tue Aug 18 2020 Ashwin H <ashwinh@vmware.com> 3.6.1-5
-   Bump up version to compile with new go
*   Fri Apr 10 2020 Harinadh D <hdommaraju@vmware.com> 3.6.1-4
-   Bump up version to compile with go 1.13.3-2
*   Tue Oct 22 2019 Ashwin H <ashwinh@vmware.com> 3.6.1-3
-   Bump up version to compile with go 1.13.3
*   Fri Aug 30 2019 Ashwin H <ashwinh@vmware.com> 3.6.1-2
-   Bump up version to compile with new go
*   Wed May 08 2019 Ashwin H <ashwinh@vmware.com> 3.6.1-1
-   Update to 3.6.1
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
