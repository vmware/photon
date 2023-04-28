Summary:        Calico node and documentation for project calico.
Name:           calico
Version:        3.25.0
Release:        3%{?dist}
License:        Apache-2.0
URL:            https://github.com/projectcalico/calico
Source0:        https://github.com/projectcalico/calico/archive/refs/tags/%{name}-%{version}.tar.gz
%define sha512  calico=8899b65be0b3b93f371942113f6bb0c958b31ff0db106d181152c3c5bf6f2f3e842719bc3ac21c573ae5fd681176ee46222798b43ebf029140a5c32ab27d9fbf
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon
BuildRequires:  git
BuildRequires:  go

%description
Calico node is a container that bundles together various components reqiured for networking
containers using project calico.
This includes key components such as felix agent for programming routes and ACLs,
BIRD routing daemon, and confd datastore monitor engine.

%package        cni
Summary:        Calico networking for CNI
Group:          Development/Tools
Requires:       cni

%description    cni
Project Calico network plugin for CNI. This allows kubernetes to use Calico networking. This repository includes a top-level CNI networking plugin, as well as a CNI IPAM plugin which makes use of Calico IPAM.

%package        felix
Summary:        A per-host daemon for Calico
Group:          Applications/System

%description    felix
Main task is to program routes and ACLs, and anything else required on the host to provide
desired connectivity for the endpoints on that host. Runs on each machine that hosts endpoints.
Runs as an agent daemon.

%package        k8s-policy
Summary:        Calico Network Policy for Kubernetes
Group:          Development/Tools
Requires:       python3
Requires:       python3-setuptools

%description    k8s-policy
Calico Network Policy enables Calico to enforce network policy on top of Calico BGP, Flannel, or GCE native.

%prep
%autosetup -p1 -n calico-%{version}

%build
#node
mkdir -p node/dist
CGO_ENABLED=0 go build -v -o node/dist/calico-node ./node/cmd/calico-node/main.go

#cni
mkdir -p cni-plugin/dist
CGO_ENABLED=0 go build -v -o cni-plugin/dist/calico -ldflags "-X main.VERSION= -s -w" ./cni-plugin/cmd/calico
CGO_ENABLED=0 go build -v -o cni-plugin/dist/calico-ipam -ldflags "-X main.VERSION= -s -w" ./cni-plugin/cmd/calico
CGO_ENABLED=0 go build -v -o cni-plugin/dist/install -ldflags "-X main.VERSION= -s -w" ./cni-plugin/cmd/calico

#felix
mkdir -p felix/dist
CGO_ENABLED=0 go build -v -o felix/dist/calico-felix -v \
  -ldflags " -X github.com/projectcalico/felix/buildinfo.GitVersion=<unknown>" \
  ./felix/cmd/calico-felix

#k8s-policy
mkdir -p kube-controllers/dist
CGO_ENABLED=0 go build -v -o kube-controllers/dist/controller -ldflags "-X main.VERSION=%{version}" ./kube-controllers/cmd/kube-controllers/

%install
#node
install -vdm 755 %{buildroot}%{_bindir}
install node/dist/calico-node %{buildroot}%{_bindir}/
install -vdm 0755 %{buildroot}%{_datadir}/calico/docker/fs
cp -r node/filesystem/etc %{buildroot}%{_datadir}/calico/docker/fs/
cp -r node/filesystem/sbin %{buildroot}/usr/share/calico/docker/fs/
sed -i 's/. startup.env/source \/startup.env/g' %{buildroot}/usr/share/calico/docker/fs/etc/rc.local
sed -i 's/. startup.env/source \/startup.env/g' %{buildroot}/usr/share/calico/docker/fs/sbin/start_runit

#cni
install -vdm 755 %{buildroot}/opt/cni/bin
install -vpm 0755 -t %{buildroot}/opt/cni/bin/ cni-plugin/dist/calico
install -vpm 0755 -t %{buildroot}/opt/cni/bin/ cni-plugin/dist/calico-ipam
install -vpm 0755 -t %{buildroot}/opt/cni/bin/ cni-plugin/dist/install

#felix
install -vdm 755 %{buildroot}%{_bindir}
install felix/dist/calico-felix %{buildroot}%{_bindir}/

#k8s-policy
install -vdm 755 %{buildroot}%{_bindir}
install -vpm 0755 -t %{buildroot}%{_bindir}/ kube-controllers/dist/controller

%files
%defattr(-,root,root)
%{_bindir}/calico-node
/usr/share/calico/docker/fs/*

%files cni
%defattr(-,root,root)
/opt/cni/bin/calico
/opt/cni/bin/calico-ipam
/opt/cni/bin/install

%files felix
%defattr(-,root,root)
%{_bindir}/calico-felix

%files k8s-policy
%defattr(-,root,root)
%{_bindir}/controller

%changelog
* Wed Apr 19 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 3.25.0-3
- Bump version as a part of libbpf upgrade
* Mon Apr 17 2023 Prashant S Chauhan <psinghchauha@vmware.com> 3.25.0-2
- Create single spec for all calico subpackages
* Thu Mar 09 2023 Prashant S Chauhan <psinghchauha@vmware.com> 3.25.0-1
- Update to 3.25.0
* Thu Mar 09 2023 Piyush Gupta <gpiyush@vmware.com> 3.17.1-6
- Bump up version to compile with new go
* Mon Nov 21 2022 Piyush Gupta <gpiyush@vmware.com> 3.17.1-5
- Bump up version to compile with new go
* Wed Oct 26 2022 Piyush Gupta <gpiyush@vmware.com> 3.17.1-4
- Bump up version to compile with new go
* Fri Jun 17 2022 Piyush Gupta <gpiyush@vmware.com> 3.17.1-3
- Bump up version to compile with new go
* Fri Jun 11 2021 Piyush Gupta<gpiyush@vmware.com> 3.17.1-2
- Bump up version to compile with new go
* Tue Feb 09 2021 Prashant S Chauhan <psinghchauha@vmware.com> 3.17.1-1
- Update to version 3.17.1
* Fri Feb 05 2021 Harinadh D <hdommaraju@vmware.com> 3.15.2-3
- Bump up version to compile with new go
* Fri Jan 15 2021 Piyush Gupta<gpiyush@vmware.com> 3.15.2-2
- Bump up version to compile with new go
* Sat Aug 29 2020 Ashwin H <ashwinh@vmware.com> 3.15.2-1
- Update to 3.15.2
* Wed Jun 17 2020 Ashwin H <ashwinh@vmware.com> 3.6.1-3
- Fix dependency for cloud.google.com-go
* Tue Jun 09 2020 Ashwin H <ashwinh@vmware.com> 3.6.1-2
- Use cache for dependencies
* Wed May 08 2019 Ashwin H <ashwinh@vmware.com> 3.6.1-1
- Update to 3.6.1
* Mon Jan 28 2019 Bo Gan <ganb@vmware.com> 2.6.7-4
- Fix CVE-2018-17846 and CVE-2018-17143
* Mon Jan 21 2019 Bo Gan <ganb@vmware.com> 2.6.7-3
- Build using go 1.9.7
* Mon Sep 24 2018 Tapas Kundu <tkundu@vmware.com> 2.6.7-2
- Build using go version 1.9
* Fri May 18 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 2.6.7-1
- Calico Node v2.6.7.
* Tue Dec 05 2017 Vinay Kulkarni <kulkarniv@vmware.com> 2.6.3-1
- Calico Node v2.6.3.
* Fri Nov 03 2017 Vinay Kulkarni <kulkarniv@vmware.com> 2.6.2-1
- Calico Node v2.6.2.
* Wed Nov 01 2017 Vinay Kulkarni <kulkarniv@vmware.com> 2.5.1-1
- Calico Node v2.5.1.
* Wed Aug 16 2017 Vinay Kulkarni <kulkarniv@vmware.com> 2.4.1-1
- Calico Node for PhotonOS.
