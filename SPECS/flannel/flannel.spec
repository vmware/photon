%define debug_package %{nil}
Summary:        Overlay network for containers based on etcd
Name:           flannel
Version:        0.22.0
Release:        5%{?dist}
License:        ASL 2.0
URL:            https://github.com/coreos/flannel
Source0:        https://github.com/coreos/flannel/archive/%{name}-%{version}.tar.gz
%define sha512  flannel=ddb13b0f23689f19a5ef84c311005a5dc3393e8c32a93af37de09ccebd625b6c7c9adad14264fd374df1f538b1387a01a05d107e4a461535737cc1e07118e361
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon
BuildRequires:  etcd >= 3.5.9
BuildRequires:  gcc
BuildRequires:  unzip
BuildRequires:  go
BuildRequires:  ca-certificates
Requires:       etcd >= 3.5.9

%description
flannel is a virtual network that provides a subnet to a container runtime
host OS for use with containers. flannel uses etcd to store the network
configuration, allocated subnets, and additional data.

%prep
%autosetup -cn src/github.com/coreos/ -p1

%build
export GOPATH=%{_builddir}
echo $GOAPTH
mv %{name}-%{version}  %{name}
pushd %{name}
make dist/flanneld %{?_smp_mflags}
popd

%install
install -vdm 755 %{buildroot}%{_bindir}
install -vpm 0755 -t %{buildroot}%{_bindir}/ %{name}/dist/flanneld

install -vdm 0755 %{buildroot}/usr/share/flannel/docker
install -vpm 0755 -t %{buildroot}/usr/share/flannel/docker/ %{name}/dist/mk-docker-opts.sh

install -vdm 0755 %{buildroot}%{_sysconfdir}/flannel
cat << EOF >> %{buildroot}%{_sysconfdir}/flannel/flanneld.conf
###
# flanneld configuration
#

# etcd endpoints
ETCD_ENDPOINTS="http://127.0.0.1:4001,http://127.0.0.1:2379"

# flannel network config
FLANNEL_NETWORK_CONF='{"Network": "172.17.0.0/16"}'

# kubernetes api server URL
KUBE_API_URL="http://localhost:8080"

# additional flannel options
FLANNEL_OPTIONS=""
EOF

mkdir -p %{buildroot}/usr/lib/systemd/system
cat << EOF >> %{buildroot}/usr/lib/systemd/system/flanneld.service
[Unit]
Description=flanneld overlay network service
After=network.target etcd.service
Before=docker.service

[Service]
Type=notify
EnvironmentFile=-/etc/flannel/flanneld.conf
ExecStartPre=-/usr/bin/etcdctl mk /vmware/network/config \${FLANNEL_NETWORK_CONF}
ExecStart=/usr/bin/flanneld -etcd-prefix=/vmware/network -etcd-endpoints=\${ETCD_ENDPOINTS} --kube-api-url=\${KUBE_API_URL} \${FLANNEL_OPTIONS}
Restart=on-failure

[Install]
WantedBy=multi-user.target
RequiredBy=docker.service
EOF

%check
cd %{name}
GOPATH=%{_builddir} make test %{?_smp_mflags}

%post

%postun

%files
%defattr(-,root,root)
%{_bindir}/flanneld
%{_libdir}/systemd/system/flanneld.service
/usr/share/flannel/docker/mk-docker-opts.sh
%config(noreplace) %{_sysconfdir}/flannel/flanneld.conf

%changelog
* Fri Mar 08 2024 Anmol Jain <anmol.jain@broadcom.com> 0.22.0-5
- Bump version as a part of etcd upgrade
* Tue Nov 21 2023 Piyush Gupta <gpiyush@vmware.com> 0.22.0-4
- Bump up version to compile with new go
* Wed Oct 11 2023 Piyush Gupta <gpiyush@vmware.com> 0.22.0-3
- Bump up version to compile with new go
* Fri Aug 18 2023 Piyush Gupta <gpiyush@vmware.com> 0.22.0-2
- Bump up version to compile with new go
* Tue Jul 04 2023 Prashant S Chauhan <psinghchauha@vmware.com> 0.22.0-1
- Update to 0.22.0
* Tue Jun 20 2023 Piyush Gupta <gpiyush@vmware.com> 0.15.0-13
- Bump up version to compile with new go
* Wed May 03 2023 Piyush Gupta <gpiyush@vmware.com> 0.15.0-12
- Bump up version to compile with new go
* Thu Mar 16 2023 Piyush Gupta <gpiyush@vmware.com> 0.15.0-11
- Bump up version to compile with new go
* Tue Dec 20 2022 Piyush Gupta <gpiyush@vmware.com> 0.15.0-10
- Bump up version to compile with new go
* Sun Nov 13 2022 Piyush Gupta <gpiyush@vmware.com> 0.15.0-9
- Bump up version to compile with new go
* Wed Oct 26 2022 Piyush Gupta <gpiyush@vmware.com> 0.15.0-8
- Bump up version to compile with new go
* Thu Sep 15 2022 Piyush Gupta <gpiyush@vmware.com> 0.15.0-7
- Bump up version to compile with new go
* Fri Aug 19 2022 Piyush Gupta <gpiyush@vmware.com> 0.15.0-6
- Bump up version to compile with new go
* Tue Jul 12 2022 Piyush Gupta <gpiyush@vmware.com> 0.15.0-5
- Bump up version to compile with new go
* Sat May 07 2022 Piyush Gupta <gpiyush@vmware.com> 0.15.0-4
- Bump up version to compile with new go
* Tue Feb 22 2022 Piyush Gupta <gpiyush@vmware.com> 0.15.0-3
- Bump up version to compile with new go
* Mon Jan 24 2022 Piyush Gupta <gpiyush@vmware.com> 0.15.0-2
- Bump up version to compile with new go
* Thu Nov 11 2021 Prashant S Chauhan <psinghchauha@vmware.com> 0.15.0-1
- Update to version 0.15.0
* Wed Oct 20 2021 Piyush Gupta <gpiyush@vmware.com> 0.13.0-6
- Bump up version to compile with new go
* Tue Sep 07 2021 Piyush Gupta <gpiyush@vmware.com> 0.13.0-5
- Bump up version to compile with new go
* Thu Aug 26 2021 Keerthana K <keerthanak@vmware.com> 0.13.0-4
- Bump up version to compile with new glibc
* Fri Jun 11 2021 Piyush Gupta <gpiyush@vmware.com> 0.13.0-3
- Bump up version to compile with new go
* Thu Mar 25 2021 Piyush Gupta<gpiyush@vmware.com> 0.13.0-2
- Bump up version to compile with new go
* Tue Feb 09 2021 Prashant S Chauhan<psinghchauha@vmware.com> 0.13.0-1
- Update to version 0.13.0
* Fri Feb 05 2021 Harinadh D <hdommaraju@vmware.com> 0.12.0-3
- Bump up version to compile with new go
* Fri Jan 15 2021 Piyush Gupta<gpiyush@vmware.com> 0.12.0-2
- Bump up version to compile with new go
* Mon Jun 22 2020 Gerrit Photon <photon-checkins@vmware.com> 0.12.0-1
- Automatic Version Bump
* Tue Dec 05 2017 Vinay Kulkarni <kulkarniv@vmware.com> 0.9.1-1
- Flannel 0.9.1.
* Tue Nov 14 2017 Vinay Kulkarni <kulkarniv@vmware.com> 0.9.0-1
- Flannel 0.9.0.
* Fri Sep 01 2017 Chang Lee <changlee@vmware.com> 0.8.0-2
- Fixed %check according to version upgrade
* Tue Aug 08 2017 Vinay Kulkarni <kulkarniv@vmware.com> 0.8.0-1
- Flannel 0.8.0 and systemd service file.
* Fri May 05 2017 Chang Lee <changlee@vmware.com> 0.7.1-1
- Updated to version 0.7.1
* Tue Apr 04 2017 Chang Lee <changlee@vmware.com> 0.7.0-1
- Updated to version 0.7.0
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.5.5-2
- GA - Bump release of all rpms
* Tue Feb 23 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 0.5.5-1
- Upgraded to version 0.5.5
* Mon Aug 03 2015 Vinay Kulkarni <kulkarniv@vmware.com> 0.5.2-1
- Add flannel package to photon.
