%ifarch x86_64
%define archname amd64
%endif
%ifarch aarch64
%define archname arm64
%endif
%define debug_package %{nil}
%define __strip /bin/true

Summary:        Kubernetes cluster management
Name:           kubernetes
Version:        1.23.2
Release:        10%{?dist}
License:        ASL 2.0
URL:            https://github.com/kubernetes/kubernetes/archive/v%{version}.tar.gz
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        kubernetes-%{version}.tar.gz
%define sha512  kubernetes-%{version}.tar.gz=af67745f84efe1e340187e510d42db231bbeef29d59fae3408b8a560bf5a336d3afa21d4a6bdd6a748ebd018aae0b15edcb4ebda594367aae3f91bae173c3a98

Source1:        https://github.com/kubernetes/contrib/archive/contrib-0.7.0.tar.gz
%define sha512  contrib-0.7.0=88dc56ae09f821465a133ef65b5f5b458afe549d60bf82335cfba26a734bc991fb694724b343ed1f90cc28ca6974cc017e168740b6610e20441faf4096cf2448

Source2:        kubelet.service
Source3:        10-kubeadm.conf
Patch0:         CVE-2022-3294.patch
Patch1:         CVE-2022-3162.patch

BuildRequires:  go >= 1.16.2
BuildRequires:  rsync
BuildRequires:  which

Requires:       cni
Requires:       ebtables
Requires:       etcd >= 3.5.0
Requires:       ethtool
Requires:       iptables
Requires:       iproute2
Requires(pre):  /usr/sbin/useradd /usr/sbin/groupadd
Requires(postun):/usr/sbin/userdel /usr/sbin/groupdel
Requires:       socat
Requires:       util-linux
Requires:       cri-tools
Requires:       conntrack-tools

%description
Kubernetes is an open source implementation of container cluster management.

%package        kubeadm
Summary:        kubeadm deployment tool
Group:          Development/Tools
Requires:       %{name} = %{version}
%description    kubeadm
kubeadm is a tool that enables quick and easy deployment of a kubernetes cluster.

%package        pause
Summary:        pause binary
Group:          Development/Tools
%description    pause
A pod setup process that holds a pod's namespace.

%global debug_package %{nil}

%prep -p exit
%autosetup -p1 -n %{name}-%{version}
cd ..
tar xf %{SOURCE1} --no-same-owner
sed -i -e 's|127.0.0.1:4001|127.0.0.1:2379|g' contrib-0.7.0/init/systemd/environ/apiserver
sed -i '/KUBE_ALLOW_PRIV/d' contrib-0.7.0/init/systemd/kubelet.service
cd %{name}-%{version}

%build
# make doesn't support _smp_mflags
make -j8
# make doesn't support _smp_mflags
make -j8 WHAT="cmd/cloud-controller-manager"
pushd build/pause
mkdir -p bin
gcc -Os -Wall -Werror -static -o bin/pause-%{archname} linux/pause.c
strip bin/pause-%{archname}
popd

%install
install -vdm644 %{buildroot}/etc/profile.d
install -m 755 -d %{buildroot}%{_bindir}

# binaries install
binaries=(cloud-controller-manager kube-apiserver kube-controller-manager kubelet kube-proxy kube-scheduler kubectl)
for bin in "${binaries[@]}"; do
  echo "+++ INSTALLING ${bin}"
  install -p -m 755 -t %{buildroot}%{_bindir} _output/local/bin/linux/%{archname}/${bin}
done
install -p -m 755 -t %{buildroot}%{_bindir} build/pause/bin/pause-%{archname}

# kubeadm install
install -vdm644 %{buildroot}/etc/systemd/system/kubelet.service.d
install -p -m 755 -t %{buildroot}%{_bindir} _output/local/bin/linux/%{archname}/kubeadm
install -p -m 755 -t %{buildroot}/etc/systemd/system %{SOURCE2}
install -p -m 644 -t %{buildroot}/etc/systemd/system/kubelet.service.d %{SOURCE3}
sed -i '/KUBELET_CGROUP_ARGS=--cgroup-driver=systemd/d' %{buildroot}/etc/systemd/system/kubelet.service.d/10-kubeadm.conf

cd ..
# install config files
install -d -m 0755 %{buildroot}%{_sysconfdir}/%{name}
install -d -m 0700 %{buildroot}%{_sysconfdir}/%{name}/manifests
install -m 644 -t %{buildroot}%{_sysconfdir}/%{name} contrib-0.7.0/init/systemd/environ/*
cat << EOF >> %{buildroot}%{_sysconfdir}/%{name}/kubeconfig
apiVersion: v1
clusters:
- cluster:
    server: http://127.0.0.1:8080
EOF
sed -i '/KUBELET_API_SERVER/c\KUBELET_API_SERVER="--kubeconfig=/etc/kubernetes/kubeconfig"' %{buildroot}%{_sysconfdir}/%{name}/kubelet

# install service files
install -d -m 0755 %{buildroot}/usr/lib/systemd/system
install -m 0644 -t %{buildroot}/usr/lib/systemd/system contrib-0.7.0/init/systemd/*.service

# install the place the kubelet defaults to put volumes
install -dm755 %{buildroot}/var/lib/kubelet
install -dm755 %{buildroot}/var/run/kubernetes
cat << EOF >> %{buildroot}/var/lib/kubelet/config.yaml
apiVersion: kubelet.config.k8s.io/v1beta1
kind: KubeletConfiguration
address: 127.0.0.1
EOF

mkdir -p %{buildroot}/%{_lib}/tmpfiles.d
cat << EOF >> %{buildroot}/%{_lib}/tmpfiles.d/kubernetes.conf
d /var/run/kubernetes 0755 kube kube -
EOF

%check
export GOPATH=%{_builddir}
go get golang.org/x/tools/cmd/cover
# make doesn't support _smp_mflags
make -j8 check

%clean
rm -rf %{buildroot}/*

%pre
if [ $1 -eq 1 ]; then
    # Initial installation.
    getent group kube >/dev/null || groupadd -r kube
    getent passwd kube >/dev/null || useradd -r -g kube -d / -s /sbin/nologin \
            -c "Kubernetes user" kube
fi

%post
chown -R kube:kube /var/lib/kubelet
chown -R kube:kube /var/run/kubernetes
systemctl daemon-reload

%post kubeadm
systemctl daemon-reload
systemctl stop kubelet
systemctl enable kubelet

%preun kubeadm
if [ $1 -eq 0 ]; then
    systemctl stop kubelet
fi

%postun
if [ $1 -eq 0 ]; then
    # Package deletion
    userdel kube
    groupdel kube
    systemctl daemon-reload
fi

%postun kubeadm
if [ $1 -eq 0 ]; then
    systemctl daemon-reload
fi

%files
%defattr(-,root,root)
%{_bindir}/cloud-controller-manager
%{_bindir}/kube-apiserver
%{_bindir}/kube-controller-manager
%{_bindir}/kubelet
%{_bindir}/kube-proxy
%{_bindir}/kube-scheduler
%{_bindir}/kubectl
%{_lib}/systemd/system/kube-apiserver.service
%{_lib}/systemd/system/kubelet.service
%{_lib}/systemd/system/kube-scheduler.service
%{_lib}/systemd/system/kube-controller-manager.service
%{_lib}/systemd/system/kube-proxy.service
%{_lib}/tmpfiles.d/kubernetes.conf
%dir %{_sysconfdir}/%{name}
%dir /var/lib/kubelet
/var/lib/kubelet/config.yaml
%dir /var/run/kubernetes
%config(noreplace) %{_sysconfdir}/%{name}/config
%config(noreplace) %{_sysconfdir}/%{name}/apiserver
%config(noreplace) %{_sysconfdir}/%{name}/controller-manager
%config(noreplace) %{_sysconfdir}/%{name}/proxy
%config(noreplace) %{_sysconfdir}/%{name}/kubelet
%config(noreplace) %{_sysconfdir}/%{name}/kubeconfig
%config(noreplace) %{_sysconfdir}/%{name}/scheduler

%files kubeadm
%defattr(-,root,root)
%{_bindir}/kubeadm
/etc/systemd/system/kubelet.service
/etc/systemd/system/kubelet.service.d/10-kubeadm.conf

%files pause
%defattr(-,root,root)
%{_bindir}/pause-%{archname}

%changelog
* Tue Apr 04 2023 Piyush Gupta <gpiyush@vmware.com> 1.23.2-10
- Bump up version to compile with new go
* Mon Mar 27 2023 Prashant S Chauhan <psinghchauha@vmware.com> 1.23.2-9
- Fix CVE-2022-3294, CVE-2022-3162
* Mon Jan 02 2023 Shreenidhi Shedi <sshedi@vmware.com> 1.23.2-8
- Bump version as a part of cni upgrade
- Remove kubectl-extra s subpackage
* Tue Dec 20 2022 Piyush Gupta <gpiyush@vmware.com> 1.23.2-7
- Bump up version to compile with new go
* Sun Nov 13 2022 Piyush Gupta <gpiyush@vmware.com> 1.23.2-6
- Bump up version to compile with new go
* Wed Oct 26 2022 Piyush Gupta <gpiyush@vmware.com> 1.23.2-5
- Bump up version to compile with new go
* Thu Sep 15 2022 Piyush Gupta <gpiyush@vmware.com> 1.23.2-4
- Bump up version to compile with new go
* Thu Aug 18 2022 Piyush Gupta <gpiyush@vmware.com> 1.23.2-3
- Bump up version to compile with new go
* Fri May 27 2022 Piyush Gupta <gpiyush@vmware.com> 1.23.2-2
- Bump up version to compile with new go
* Tue May 17 2022 Prashant S Chauhan <psinghchauha@vmware.com> 1.23.2-1
- Update kubernetes to 1.23.2
* Mon Mar 21 2022 Prashant S Chauhan <psinghchauha@vmware.com> 1.18.19-13
- Remove smp_flags to fix build failure with "out of memory" message
* Fri Mar 18 2022 Piyush Gupta <gpiyush@vmware.com> 1.18.19-13
- Bump up version to compile with new go
* Fri Mar 11 2022 Prashant S Chauhan <psinghchauha@vmware.com> 1.18.19-12
- Fix CVE-2020-8554
* Tue Feb 22 2022 Piyush Gupta <gpiyush@vmware.com> 1.18.19-11
- Bump up version to compile with new go
* Mon Jan 24 2022 Piyush Gupta <gpiyush@vmware.com> 1.18.19-10
- Bump up version to compile with new go
* Tue Nov 16 2021 Piyush Gupta <gpiyush@vmware.com> 1.18.19-9
- Bump up version to compile with new go
* Wed Oct 20 2021 Piyush Gupta <gpiyush@vmware.com> 1.18.19-8
- Bump up version to compile with new go
* Fri Sep 17 2021 Prashant S Chauhan <psinghchauha@vmware.com> 1.18.19-7
- Fix CVE-2021-25741
* Thu Aug 26 2021 Keerthana K <keerthanak@vmware.com> 1.18.19-6
- Bump up version to compile with new glibc
* Sat Aug 21 2021 Piyush Gupta<gpiyush@vmware.com> 1.18.19-5
- Bump up version to compile with new go
* Tue Jun 29 2021 Piyush Gupta <gpiyush@vmware.com> 1.18.19-4
- Bump up version to compile with new go
* Tue Jun 22 2021 Prashant S Chauhan <psinghchauha@vmware.com> 1.18.19-3
- Change 10-kubeadm.conf file permission to 644
* Wed Jun 02 2021 Piyush Gupta<gpiyush@vmware.com> 1.18.19-2
- Bump up version to compile with new go
* Thu Mar 18 2021 Prashant S Chauhan <psinghchauha@vmware.com> 1.18.19-1
- Update to version 1.18.19, Fix CVE-2020-8565, CVE-2021-25737, CVE-2021-3121
* Thu Feb 18 2021 Harinadh D <hdommaraju@vmware.com> 1.17.11-4
- Bump up version to compile with new go
* Wed Feb 03 2021 Prashant S Chauhan <psinghchauha@vmware.com> 1.17.11-3
- Fix CVE-2020-8564, CVE-2020-8566
* Fri Nov 27 2020 HarinadhD <hdommaraju@vmware.com> 1.17.11-2
- Bump up version to compile with new go
* Wed Sep 16 2020 Ashwin H <ashwinh@vmware.com> 1.17.11-1
- Initial version 1.17.11
