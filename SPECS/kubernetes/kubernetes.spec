%ifarch x86_64
%define archname amd64
%endif
%ifarch aarch64
%define archname arm64
%endif

%define debug_package %{nil}
%define __strip /bin/true
%define contrib_ver 0.7.0

Summary:        Kubernetes cluster management
Name:           kubernetes
Version:        1.27.13
Release:        4%{?dist}
License:        ASL 2.0
URL:            https://github.com/kubernetes/kubernetes/archive/v%{version}.tar.gz
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://github.com/kubernetes/kubernetes/archive/refs/tags/%{name}-%{version}.tar.gz
%define sha512 %{name}-%{version}.tar.gz=cffb7b0b29ef65bbf234a2743afac284ab119976eb12a0ea3b26582ae65d58b2b584781f72a252ea8dd1b950aa27622839eaafb3b561447bedd8edde09003b1f

Source1: https://github.com/kubernetes/contrib/archive/contrib-%{contrib_ver}.tar.gz
%define sha512 contrib-%{contrib_ver}=88dc56ae09f821465a133ef65b5f5b458afe549d60bf82335cfba26a734bc991fb694724b343ed1f90cc28ca6974cc017e168740b6610e20441faf4096cf2448

Source2:        kubelet.service
Source3:        10-kubeadm.conf

BuildRequires:  go
BuildRequires:  rsync
BuildRequires:  which

Requires:       cni
Requires:       ebtables
Requires:       etcd >= 3.5.7
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
Requires:       %{name} = %{version}-%{release}
%description    kubeadm
kubeadm is a tool that enables quick and easy deployment of a kubernetes cluster.

%package        pause
Summary:        pause binary
Group:          Development/Tools
%description    pause
A pod setup process that holds a pod's namespace.

%prep -p exit
%autosetup -n %{name}-%{version} -p1
cd ..
tar xf %{SOURCE1} --no-same-owner
sed -i -e 's|127.0.0.1:4001|127.0.0.1:2379|g' contrib-%{contrib_ver}/init/systemd/environ/apiserver
sed -i '/KUBE_ALLOW_PRIV/d' contrib-%{contrib_ver}/init/systemd/kubelet.service

%build
make WHAT="cmd/kube-proxy" %{?_smp_mflags}
make WHAT="cmd/kube-apiserver" %{?_smp_mflags}
make WHAT="cmd/kube-controller-manager" %{?_smp_mflags}
make WHAT="cmd/kubelet" %{?_smp_mflags}
make WHAT="cmd/kubeadm" %{?_smp_mflags}
make WHAT="cmd/kube-scheduler" %{?_smp_mflags}
make WHAT="cmd/kubectl" %{?_smp_mflags}
make WHAT="cmd/cloud-controller-manager" %{?_smp_mflags}
pushd build/pause
mkdir -p bin
gcc -Os -Wall -Werror -static -o bin/pause-%{archname} linux/pause.c
strip bin/pause-%{archname}
popd

%install
install -vdm644 %{buildroot}%{_sysconfdir}/profile.d
install -m 755 -d %{buildroot}%{_bindir}

# binaries install
binaries=(cloud-controller-manager kube-apiserver kube-controller-manager kubelet kube-proxy kube-scheduler kubectl)
for bin in "${binaries[@]}"; do
  echo "+++ INSTALLING ${bin}"
  install -p -m 755 -t %{buildroot}%{_bindir} _output/local/bin/linux/%{archname}/${bin}
done
install -p -m 755 -t %{buildroot}%{_bindir} build/pause/bin/pause-%{archname}

# kubeadm install
install -vdm644 %{buildroot}%{_sysconfdir}/systemd/system/kubelet.service.d
install -p -m 755 -t %{buildroot}%{_bindir} _output/local/bin/linux/%{archname}/kubeadm
install -p -m 755 -t %{buildroot}%{_sysconfdir}/systemd/system %{SOURCE2}
install -p -m 644 -t %{buildroot}%{_sysconfdir}/systemd/system/kubelet.service.d %{SOURCE3}
sed -i '/KUBELET_CGROUP_ARGS=--cgroup-driver=systemd/d' %{buildroot}%{_sysconfdir}/systemd/system/kubelet.service.d/10-kubeadm.conf

cd ..
# install config files
install -d -m 0755 %{buildroot}%{_sysconfdir}/%{name}
install -d -m 0700 %{buildroot}%{_sysconfdir}/%{name}/manifests
install -m 644 -t %{buildroot}%{_sysconfdir}/%{name} contrib-%{contrib_ver}/init/systemd/environ/*
cat << EOF >> %{buildroot}%{_sysconfdir}/%{name}/kubeconfig
apiVersion: v1
clusters:
- cluster:
    server: http://127.0.0.1:8080
EOF
sed -i '/KUBELET_API_SERVER/c\KUBELET_API_SERVER="--kubeconfig=%{_sysconfdir}/%{name}/kubeconfig"' %{buildroot}%{_sysconfdir}/%{name}/kubelet

# install service files
install -d -m 0755 %{buildroot}%{_unitdir}
install -m 0644 -t %{buildroot}%{_unitdir} contrib-%{contrib_ver}/init/systemd/*.service

# install the place the kubelet defaults to put volumes
install -dm755 %{buildroot}%{_sharedstatedir}/kubelet
install -dm755 %{buildroot}%{_var}/run/%{name}

mkdir -p %{buildroot}%{_tmpfilesdir}
cat << EOF >> %{buildroot}%{_tmpfilesdir}/%{name}.conf
d %{_var}/run/%{name} 0755 kube kube -
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
chown -R kube:kube %{_sharedstatedir}/kubelet
chown -R kube:kube %{_var}/run/%{name}
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
systemctl daemon-reload

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
%{_lib}/tmpfiles.d/%{name}.conf
%dir %{_sysconfdir}/%{name}
%dir %{_sharedstatedir}/kubelet
%dir %{_var}/run/%{name}
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
%{_sysconfdir}/systemd/system/kubelet.service
%{_sysconfdir}/systemd/system/kubelet.service.d/10-kubeadm.conf

%files pause
%defattr(-,root,root)
%{_bindir}/pause-%{archname}

%changelog
* Thu Sep 19 2024 Mukul Sikka <mukul.sikka@broadcom.com> 1.27.13-4
- Bump version as a part of go upgrade
* Fri Jul 12 2024 Mukul Sikka <mukul.sikka@broadcom.com> 1.27.13-3
- Bump version as a part of go upgrade
* Thu Jun 20 2024 Mukul Sikka <msikka@vmware.com> 1.27.13-2
- Bump version as a part of go upgrade
* Mon Apr 22 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 1.27.13-1
- Update to 1.27.13, fixes CVE-2024-3177
* Thu Apr 18 2024 Mukul Sikka <msikka@vmware.com> 1.27.3-7
- Bump version as a part of go upgrade
* Tue Mar 19 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.27.3-6
- Bump version as a part of rsync upgrade
* Fri Mar 08 2024 Anmol Jain <anmol.jain@broadcom.com> 1.27.3-5
- Bump version as a part of etcd upgrade
* Tue Nov 21 2023 Piyush Gupta <gpiyush@vmware.com> 1.27.3-4
- Bump up version to compile with new go
* Wed Oct 11 2023 Piyush Gupta <gpiyush@vmware.com> 1.27.3-3
- Bump up version to compile with new go
* Fri Aug 18 2023 Piyush Gupta <gpiyush@vmware.com> 1.27.3-2
- Bump up version to compile with new go
* Tue Jul 04 2023 Prashant S Chauhan <psinghchauha@vmware.com> 1.27.3-1
- Update to 1.27.3, Fixes multiple second level CVEs
* Tue Jun 20 2023 Piyush Gupta <gpiyush@vmware.com> 1.23.9-13
- Bump up version to compile with new go
* Thu May 11 2023 Shreenidhi Shedi <sshedi@vmware.com> 1.23.9-12
- Fix for requires
* Wed May 03 2023 Piyush Gupta <gpiyush@vmware.com> 1.23.9-11
- Bump up version to compile with new go
* Tue Mar 21 2023 Prashant S Chauhan <psinghchauha@vmware.com> 1.23.9-10
- Fix CVE-2022-3294, CVE-2022-3162
* Thu Mar 16 2023 Piyush Gupta <gpiyush@vmware.com> 1.23.9-9
- Bump up version to compile with new go
* Tue Dec 20 2022 Piyush Gupta <gpiyush@vmware.com> 1.23.9-8
- Bump up version to compile with new go
* Sat Nov 19 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.23.9-7
- Bump version as a part of cni upgrade
* Sun Nov 13 2022 Piyush Gupta <gpiyush@vmware.com> 1.23.9-6
- Bump up version to compile with new go
* Wed Oct 26 2022 Piyush Gupta <gpiyush@vmware.com> 1.23.9-5
- Bump up version to compile with new go
* Fri Sep 30 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.23.9-4
- Remove kubectl-extras subpackage
* Thu Sep 15 2022 Piyush Gupta <gpiyush@vmware.com> 1.23.9-3
- Bump up version to compile with new go
* Thu Aug 25 2022 Piyush Gupta <gpiyush@vmware.com> 1.23.9-2
- Bump up version to compile with new go
* Wed Aug 24 2022 Prashant S Chauhan <psinghchauha@vmware.com> 1.23.9-1
- Update to version 1.23.9
* Tue Jul 12 2022 Piyush Gupta <gpiyush@vmware.com> 1.22.4-6
- Bump up version to compile with new go
* Wed Mar 23 2022 Piyush Gupta <gpiyush@vmware.com> 1.22.4-5
- Bump up version to compile with new go
* Mon Mar 07 2022 Prashant S Chauhan <psinghchauha@vmware.com> 1.22.4-4
- Remove smp_flags to fix build failure with "out of memory" message
* Tue Feb 22 2022 Piyush Gupta <gpiyush@vmware.com> 1.22.4-3
- Bump up version to compile with new go
* Mon Jan 24 2022 Piyush Gupta <gpiyush@vmware.com> 1.22.4-2
- Bump up version to compile with new go
* Thu Nov 18 2021 Prashant S Chauhan <psinghchauha@vmware.com> 1.22.4-1
- Update kubernetes to 1.22.4
* Wed Oct 20 2021 Piyush Gupta <gpiyush@vmware.com> 1.19.15-3
- Bump up version to compile with new go
* Sun Oct 03 2021 Piyush Gupta <gpiyush@vmware.com> 1.19.15-2
- Bump up version to compile with new go
* Fri Sep 17 2021 Prashant S Chauhan <psinghchauha@vmware.com> 1.19.15-1
- Update to version 1.19.15, Fix CVE-2021-25741
* Thu Aug 26 2021 Keerthana K <keerthanak@vmware.com> 1.19.10-4
- Bump up version to compile with new glibc
* Tue Jun 22 2021 Prashant S Chauhan <psinghchauha@vmware.com> 1.19.10-3
- Change 10-kubeadm.conf file permission to 644
* Fri Jun 11 2021 Piyush Gupta <gpiyush@vmware.com> 1.19.10-2
- Bump up version to compile with new go
* Tue May 11 2021 Prashant S Chauhan <psinghchauha@vmware.com> 1.19.10-1
- Update to v1.19.10, fixes CVE-2021-3121. Added patch to fix CVE-2021-25737
* Thu Mar 25 2021 Piyush Gupta<gpiyush@vmware.com> 1.19.7-2
- Bump up version to compile with new go
* Tue Feb 09 2021 Prashant S Chauhan <psinghchauha@vmware.com> 1.19.7-1
- Update to v1.19.7
* Fri Feb 05 2021 Harinadh D <hdommaraju@vmware.com> 1.18.8-3
- Bump up version to compile with new go
* Fri Jan 15 2021 Piyush Gupta<gpiyush@vmware.com> 1.18.8-2
- Bump up version to compile with new go
* Wed Aug 26 2020 Ashwin H <ashwinh@vmware.com> 1.18.8-1
- Initial version
