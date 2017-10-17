Summary:        Overlay network for containers based on etcd
Name:           flannel
Version:        0.8.0
Release:        2%{?dist}
License:        ASL 2.0
URL:            https://github.com/coreos/flannel
Source0:        https://github.com/coreos/flannel/archive/%{name}-%{version}.tar.gz
%define sha1 flannel=d8eb057233de1babd306297d4fc3af098ccbea16
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
%setup -cqn src/github.com/coreos/

%build
export GOPATH=%{_builddir}
echo $GOAPTH
mv %{name}-%{version}  %{name}
pushd %{name}
make dist/flanneld
popd

%install
install -vdm 755 %{buildroot}%{_bindir}
install -vpm 0755 -t %{buildroot}%{_bindir}/ %{name}/dist/flanneld

install -vdm 0755 %{buildroot}/usr/share/flannel/docker
install -vpm 0755 -t %{buildroot}/usr/share/flannel/docker/ %{name}/dist/mk-docker-opts.sh

install -vdm 0755 %{buildroot}%{_sysconfdir}/flannel
cat << EOF >> %{buildroot}%{_sysconfdir}/flannel/flanneld
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
EnvironmentFile=-/etc/flannel/flanneld
ExecStartPre=-/usr/bin/etcdctl mk /vmware/network/config \${FLANNEL_NETWORK_CONF}
ExecStart=/usr/bin/flanneld -etcd-prefix=/vmware/network -etcd-endpoints=\${ETCD_ENDPOINTS} --kube-api-url=\${KUBE_API_URL} \${FLANNEL_OPTIONS}
Restart=on-failure

[Install]
WantedBy=multi-user.target
RequiredBy=docker.service
EOF

%check
pushd %{name}
go get golang.org/x/tools/cmd/cover
sed -e 's:^func TestRemote:func _TestRemote:' -i remote/remote_test.go || die
./test
popd

%post

%postun

%files
%defattr(-,root,root)
%{_bindir}/flanneld
%{_libdir}/systemd/system/flanneld.service
%{_sysconfdir}/flannel/flanneld
/usr/share/flannel/docker/mk-docker-opts.sh
%config(noreplace) %{_sysconfdir}/flannel/flanneld

%changelog
*   Thu Oct 12 2017 Vinay Kulkarni <kulkarniv@vmware.com> 0.8.0-2
-   Create flannel network config if not exist, tolerate errcode if exists.
*   Fri Aug 11 2017 Vinay Kulkarni <kulkarniv@vmware.com> 0.8.0-1
-   Flannel 0.8.0 and systemd service file.
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.5.5-2
-   GA - Bump release of all rpms
*   Tue Feb 23 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 0.5.5-1
-   Upgraded to version 0.5.5
*   Mon Aug 03 2015 Vinay Kulkarni <kulkarniv@vmware.com> 0.5.2-1
-   Add flannel package to photon.
