Summary:        Calico node and documentation for project calico.
Name:           calico
Version:        3.26.4
Release:        2%{?dist}
License:        Apache-2.0
URL:            https://github.com/projectcalico/calico
Source0:        https://github.com/projectcalico/calico/archive/refs/tags/%{name}-%{version}.tar.gz
%define sha512  calico=85a051cf938f771e9bf3173cc1806697b73b36d221053ad53ecf69afae0bfe8f9c0c6fac24de4b5f3e747b095ebf11e79d6358bd0e7a797a5144054010bb15b4
Patch1:         0001-CVE-2024-33522.patch
Patch2:         0002-CVE-2024-33522.patch
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

%package -n     confd
Summary:        confd is a lightweight configuration management tool
Group:          Development/Tools
Conflicts:      %{name}-confd <= 0.16.0-20
Provides:       %{name}-confd = %{version}-%{release}

%description -n confd
This is a Calico-specific version of confd. It is heavily modified from the original and only supports a single backend type - namely a Calico datastore. It has a single purpose which is to monitor Calico BGP configuration and to autogenerate bird BGP templates from that config.

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

#confd
mkdir -p confd/dist
CGO_ENABLED=0 go build -v -o confd/dist/confd ./confd/

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

#confd
install -vdm 755 %{buildroot}/%{_bindir}
install -vpm 0755 -t %{buildroot}/%{_bindir} confd/dist/confd
cp -r confd/etc/ %{buildroot}%{_sysconfdir}

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

%files -n confd
%defattr(-,root,root)
%{_bindir}/confd
%config(noreplace) %{_sysconfdir}/calico

%changelog
* Thu Jun 20 2024 Mukul Sikka <msikka@vmware.com> 3.26.4-2
- Bump version as a part of go upgrade
* Mon May 06 2024 Brennan Lamoreaux <brennan.lamoreaux@broadcom.com> 3.26.4-1
- Update to 3.26.4 and add patches for CVE-2024-33522. Drop patch for
- CVE-2023-41378, as this was included in 3.26.3
* Thu Apr 18 2024 Mukul Sikka <msikka@vmware.com> 3.26.1-7
- Bump version as a part of go upgrade
* Tue Nov 21 2023 Piyush Gupta <gpiyush@vmware.com> 3.26.1-6
- Bump up version to compile with new go
* Fri Nov 17 2023 Prashant S Chauhan <psinghchauha@vmware.com> 3.26.1-5
- Fix CVE-2023-41378
* Wed Oct 11 2023 Piyush Gupta <gpiyush@vmware.com> 3.26.1-4
- Bump up version to compile with new go
* Fri Aug 18 2023 Piyush Gupta <gpiyush@vmware.com> 3.26.1-3
- Bump up version to compile with new go
* Mon Jul 17 2023 Prashant S Chauhan <psinghchauha@vmware.com> 3.26.1-2
- Add conflict with calico-confd package
* Tue Jul 04 2023 Prashant S Chauhan <psinghchauha@vmware.com> 3.26.1-1
- Update to 3.26.1, Fixes multiple second level CVEs
- Create single spec for all calico subpackages
* Tue Jun 20 2023 Piyush Gupta <gpiyush@vmware.com> 3.20.2-14
- Bump up version to compile with new go
* Wed May 03 2023 Piyush Gupta <gpiyush@vmware.com> 3.20.2-13
- Bump up version to compile with new go
* Fri Apr 14 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 3.20.2-12
- Bump version as a part of libbpf upgrade
* Thu Mar 16 2023 Piyush Gupta <gpiyush@vmware.com> 3.20.2-11
- Bump up version to compile with new go
* Tue Dec 20 2022 Piyush Gupta <gpiyush@vmware.com> 3.20.2-10
- Bump up version to compile with new go
* Sun Nov 13 2022 Piyush Gupta <gpiyush@vmware.com> 3.20.2-9
- Bump up version to compile with new go
* Wed Oct 26 2022 Piyush Gupta <gpiyush@vmware.com> 3.20.2-8
- Bump up version to compile with new go
* Thu Sep 15 2022 Piyush Gupta <gpiyush@vmware.com> 3.20.2-7
- Bump up version to compile with new go
* Fri Aug 19 2022 Piyush Gupta <gpiyush@vmware.com> 3.20.2-6
- Bump up version to compile with new go
* Tue Jul 12 2022 Piyush Gupta <gpiyush@vmware.com> 3.20.2-5
- Bump up version to compile with new go
* Sat May 07 2022 Piyush Gupta <gpiyush@vmware.com> 3.20.2-4
- Bump up version to compile with new go
* Tue Feb 22 2022 Piyush Gupta <gpiyush@vmware.com> 3.20.2-3
- Bump up version to compile with new go
* Mon Jan 24 2022 Piyush Gupta <gpiyush@vmware.com> 3.20.2-2
- Bump up version to compile with new go
* Thu Nov 18 2021 Prashant S Chauhan <psinghchauha@vmware.com> 3.20.2-1
- Update calico to 3.20.2
* Wed Oct 20 2021 Piyush Gupta <gpiyush@vmware.com> 3.17.1-5
- Bump up version to compile with new go
* Tue Oct 05 2021 Piyush Gupta <gpiyush@vmware.com> 3.17.1-4
- Bump up version to compile with new go
* Fri Jun 11 2021 Piyush Gupta <gpiyush@vmware.com> 3.17.1-3
- Bump up version to compile with new go
* Thu Mar 25 2021 Piyush Gupta<gpiyush@vmware.com> 3.17.1-2
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
