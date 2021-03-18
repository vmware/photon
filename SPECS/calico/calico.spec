Summary:        Calico node and documentation for project calico.
Name:           calico
Version:        3.12.3
Release:        1%{?dist}
License:        Apache-2.0
URL:            https://github.com/projectcalico/node
Source0:        %{name}-%{version}.tar.gz
%define sha1 calico=dda88fd083669067280e7c6b616dcea40d75967f
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
*   Tue May 25 2021 Prashant S Chauhan <psinghchauha@vmware.com> 3.12.3-1
-   Update to 3.12.3
*   Fri Apr 10 2020 Harinadh D <hdommaraju@vmware.com> 3.6.1-5
-   Bump up version to compile with go 1.13.5-2
*   Tue Jan 07 2020 Ashwin H <ashwinh@vmware.com> 3.6.1-4
-   Bump up version to compile with new go
*   Fri Aug 30 2019 Ashwin H <ashwinh@vmware.com> 3.6.1-3
-   Bump up version to compile with new go
*   Fri May 03 2019 Bo Gan <ganb@vmware.com> 3.6.1-2
-   Fix CVE-2018-17846 and CVE-2018-17143
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
