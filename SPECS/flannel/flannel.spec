Summary:        Overlay network for containers based on etcd
Name:           flannel
Version:        0.15.0
Release:        8%{?dist}
License:        ASL 2.0
URL:            https://github.com/coreos/flannel
Source0:        https://github.com/coreos/flannel/archive/%{name}-%{version}.tar.gz
%define sha512  flannel=1cf2a04101897032c09dd1840a0de6c3aee49f2a24784fdd2140ca5848ef563a597613164134d0dc5743f762982a179fb5aac1deb79264fccfb9d11abcc1fade
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon
BuildRequires:  etcd >= 2.0.0
BuildRequires:  gcc
BuildRequires:  unzip
BuildRequires:  go
Requires:       etcd >= 2.0.0
%define debug_package %{nil}

%description
flannel is a virtual network that provides a subnet to a container runtime
host OS for use with containers. flannel uses etcd to store the network
configuration, allocated subnets, and additional data.

%prep
%autosetup -cn src/github.com/coreos/

%build
export GOPATH=%{_builddir}
export GO111MODULE=auto
echo $GOAPTH
mv %{name}-%{version}  %{name}
pushd %{name}
make %{?_smp_mflags} dist/flanneld
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
* Tue Apr 04 2023 Piyush Gupta <gpiyush@vmware.com> 0.15.0-8
- Bump up version to compile with new go
* Tue Dec 20 2022 Piyush Gupta <gpiyush@vmware.com> 0.15.0-7
- Bump up version to compile with new go
* Sun Nov 13 2022 Piyush Gupta <gpiyush@vmware.com> 0.15.0-6
- Bump up version to compile with new go
* Wed Oct 26 2022 Piyush Gupta <gpiyush@vmware.com> 0.15.0-5
- Bump up version to compile with new go
* Thu Sep 15 2022 Piyush Gupta <gpiyush@vmware.com> 0.15.0-4
- Bump up version to compile with new go
* Thu Aug 18 2022 Piyush Gupta <gpiyush@vmware.com> 0.15.0-3
- Bump up version to compile with new go
* Fri May 27 2022 Piyush Gupta <gpiyush@vmware.com> 0.15.0-2
- Bump up version to compile with new go.
* Tue May 17 2022 Prashant S Chauhan <psinghchauha@vmware.com> 0.15.0-1
- Update kubernetes to 0.15.0
* Wed Mar 16 2022 Piyush Gupta <gpiyush@vmware.com> 0.11.0-15
- Bump up version to compile with new go
* Tue Feb 22 2022 Piyush Gupta <gpiyush@vmware.com> 0.11.0-14
- Bump up version to compile with new go
* Mon Jan 24 2022 Piyush Gupta <gpiyush@vmware.com> 0.11.0-13
- Bump up version to compile with new go
* Tue Nov 16 2021 Piyush Gupta <gpiyush@vmware.com> 0.11.0-12
- Bump up version to compile with new go
* Wed Oct 20 2021 Piyush Gupta <gpiyush@vmware.com> 0.11.0-11
- Bump up version to compile with new go
* Thu Aug 26 2021 Keerthana K <keerthanak@vmware.com> 0.11.0-10
- Bump up version to compile with new glibc
* Sat Aug 21 2021 Piyush Gupta<gpiyush@vmware.com> 0.11.0-9
- Bump up version to compile with new go
* Tue Jun 29 2021 Piyush Gupta <gpiyush@vmware.com> 0.11.0-8
- Bump up version to compile with new go
* Mon May 03 2021 Piyush Gupta<gpiyush@vmware.com> 0.11.0-7
- Bump up version to compile with new go
* Mon Feb 08 2021 Harinadh D <hdommaraju@vmware.com> 0.11.0-6
- Bump up version to compile with new go
* Fri Nov 27 2020 HarinadhD <hdommaraju@vmware.com> 0.11.0-5
- Bump up version to compile with new go
* Fri Apr 10 2020 Harinadh D <hdommaraju@vmware.com> 0.11.0-4
- Bump up version to compile with go 1.13.3-2
* Tue Oct 22 2019 Ashwin H <ashwinh@vmware.com> 0.11.0-3
- Bump up version to compile with go 1.13.3
* Fri Aug 30 2019 Ashwin H <ashwinh@vmware.com> 0.11.0-2
- Bump up version to compile with new go
* Sat Mar 16 2019 Ashwin H <ashwinh@vmware.com> 0.11.0-1
- Update Flannel to 0.11.0.
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
