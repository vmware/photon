%define network_required 1
%ifarch x86_64
%define archname amd64
%endif
%ifarch aarch64
%define archname arm64
%endif

%define debug_package %{nil}
%define __strip /bin/true
%define contrib_ver 0.7.0
%define isolcpu_ver c15e3e1a3a

Summary:        Kubernetes cluster management
Name:           kubernetes
Version:        1.27.16
Release:        1%{?dist}
URL:            https://github.com/kubernetes/kubernetes/archive/v%{version}.tar.gz
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://github.com/kubernetes/kubernetes/archive/refs/tags/%{name}-%{version}.tar.gz

Source1: https://github.com/%{name}/contrib/archive/contrib-%{contrib_ver}.tar.gz

Source2:        kubelet.service
Source3:        10-kubeadm.conf
Source4:        %{name}.sysusers

# Sources for isolcpu device plugin
# Source tarball of https://opendev.org/starlingx/integ/src/commit/c15e3e1a3af2c797caa1bc408315beb0101ae623/kubernetes/plugins/isolcpus-device-plugin/files
Source5:        isolcpu-plugin-%{isolcpu_ver}.tar.bz2

Source6: license.txt
%include %{SOURCE6}

Patch0:         0001-kubelet-cpumanager-introduce-concept-of-isolated-CPU.patch
Patch1:         0001-Use-vmware.com-isolcpu-property-name.patch
Patch2:         CVE-2024-10220.patch

BuildRequires:  go
BuildRequires:  rsync
BuildRequires:  which
BuildRequires:  systemd-devel

Requires:       cni
Requires:       ebtables
Requires:       etcd >= 3.5.7
Requires:       ethtool
Requires:       iptables
Requires:       iproute2
Requires(pre):  systemd-rpm-macros
Requires(pre):  /usr/sbin/useradd /usr/sbin/groupadd
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
kubeadm is a tool that enables quick and easy deployment of a %{name} cluster.

%package        pause
Summary:        pause binary
Group:          Development/Tools
%description    pause
A pod setup process that holds a pod's namespace.

%package        isolcpu-plugin
Summary:        isolcpu plugin service
Group:          Development/Tools
# Relaxed dependency on kubelet
Requires:       %{name} >= 1.27.3
%description    isolcpu-plugin
A kubelet device plugin for isolcpu resource.

%prep
%autosetup -b0 -b5 -N
%patch -p1 0
%patch -p1 2
cd ../isolcpu-plugin-%{isolcpu_ver}
%patch -p1 1

cd ..
tar xf %{SOURCE1} --no-same-owner
sed -i -e 's|127.0.0.1:4001|127.0.0.1:2379|g' contrib-%{contrib_ver}/init/systemd/environ/apiserver
sed -i '/KUBE_ALLOW_PRIV/d' contrib-%{contrib_ver}/init/systemd/kubelet.service

%build
export FORCE_HOST_GO=y
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

# Build static isolcpu_plugin binary
pushd ../isolcpu-plugin-%{isolcpu_ver}
CGO_ENABLED=0 go build -mod=vendor
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

install -p -D -m 0644 %{SOURCE4} %{buildroot}%{_sysusersdir}/%{name}.sysusers

mkdir -p %{buildroot}%{_tmpfilesdir}
cat << EOF >> %{buildroot}%{_tmpfilesdir}/%{name}.conf
d %{_var}/run/%{name} 0755 kube kube -
EOF

pushd isolcpu-plugin-%{isolcpu_ver}
install -p -m 755 -t %{buildroot}%{_bindir} isolcpu_plugin
install -m 0644 -t %{buildroot}%{_unitdir} isolcpu_plugin.service
popd

%check
export GOPATH=%{_builddir}
go get golang.org/x/tools/cmd/cover
make %{?_smp_mflags} check

%clean
rm -rf %{buildroot}/*

%pre
if [ $1 -eq 1 ]; then
    # Initial installation.
    %sysusers_create_compat %{SOURCE4}
fi

%post
chown -R kube:kube %{_sharedstatedir}/kubelet
chown -R kube:kube %{_var}/run/%{name}
systemctl daemon-reload

%post kubeadm
systemctl daemon-reload
systemctl stop kubelet
systemctl enable kubelet

%post isolcpu-plugin
touch /etc/kubernetes/respect_isolcpus
systemctl daemon-reload
systemctl enable isolcpu_plugin

%preun kubeadm
if [ $1 -eq 0 ]; then
    systemctl stop kubelet
fi

%preun isolcpu-plugin
if [ $1 -eq 0 ]; then
    systemctl stop isolcpu_plugin
fi

%postun
if [ $1 -eq 0 ]; then
    # Package deletion
    systemctl daemon-reload
fi

%postun kubeadm
if [ $1 -eq 0 ]; then
    systemctl daemon-reload
fi

%postun isolcpu-plugin
if [ $1 -eq 0 ]; then
    rm -f /etc/kubernetes/respect_isolcpus
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
%{_unitdir}/kube-apiserver.service
%{_unitdir}/kubelet.service
%{_unitdir}/kube-scheduler.service
%{_unitdir}/kube-controller-manager.service
%{_unitdir}/kube-proxy.service
%{_tmpfilesdir}/%{name}.conf
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
%{_sysusersdir}/%{name}.sysusers

%files kubeadm
%defattr(-,root,root)
%{_bindir}/kubeadm
%{_sysconfdir}/systemd/system/kubelet.service
%{_sysconfdir}/systemd/system/kubelet.service.d/10-kubeadm.conf

%files pause
%defattr(-,root,root)
%{_bindir}/pause-%{archname}

%files isolcpu-plugin
%defattr(-,root,root)
%{_bindir}/isolcpu_plugin
%{_unitdir}/isolcpu_plugin.service

%changelog
* Tue Feb 25 2025 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 1.27.16-1
- Update to 1.27.16, Fixes CVE-2024-5321,fix CVE-2024-10220
* Wed Jan 08 2025 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 1.27.13-8
- Release bump for network_required packages
* Wed Dec 11 2024 Mukul Sikka <mukul.sikka@broadcom.com> 1.27.13-7
- Release bump for SRP compliance
* Thu Sep 19 2024 Mukul Sikka <mukul.sikka@broadcom.com> 1.27.13-6
- Bump version as a part of go upgrade
* Wed Sep 04 2024 Mukul Sikka <mukul.sikka@broadcom.com> 1.27.13-5
- Adding env variable to compile with host go in build section
* Fri Jul 12 2024 Mukul Sikka <mukul.sikka@broadcom.com> 1.27.13-4
- Bump version as a part of go upgrade
* Thu Jun 20 2024 Mukul Sikka <msikka@vmware.com> 1.27.13-3
- Bump version as a part of go upgrade
* Thu Jun 06 2024 Mukul Sikka <mukul.sikka@broadcom.com> 1.27.13-2
- Update release to compile with host go
* Mon Apr 22 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 1.27.13-1
- Update to 1.27.13, fixes CVE-2024-3177
* Wed Mar 13 2024 Mukul Sikka <msikka@vmware.com> 1.27.3-10
- Bump version as a part of go upgrade
* Fri Mar 08 2024 Anmol Jain <anmol.jain@broadcom.com> 1.27.3-9
- Bump version as a part of etcd upgrade
* Tue Nov 21 2023 Piyush Gupta <gpiyush@vmware.com> 1.27.3-8
- Bump up version to compile with new go
* Wed Oct 11 2023 Piyush Gupta <gpiyush@vmware.com> 1.27.3-7
- Bump up version to compile with new go
* Mon Sep 18 2023 Piyush Gupta <gpiyush@vmware.com> 1.27.3-6
- Bump up version to compile with new go
* Thu Sep 07 2023 Alexey Makhalov <amakhalov@vmware.com> 1.27.3-5
- Fix for previous change to apply all patches.
* Wed Aug 23 2023 Alexey Makhalov <amakhalov@vmware.com> 1.27.3-4
- Introduction of vmware.com/isolcpu POD property.
- isolcpus allocations support for RT workloads.
* Tue Aug 08 2023 Mukul Sikka <msikka@vmware.com> 1.27.3-3
- Resolving systemd-rpm-macros for group creation
* Mon Jul 17 2023 Piyush Gupta <gpiyush@vmware.com> 1.27.3-2
- Bump up version to compile with new go
* Tue Jul 04 2023 Prashant S Chauhan <psinghchauha@vmware.com> 1.27.3-1
- Update to 1.27.3, Fixes multiple second level CVEs
* Thu Jun 22 2023 Piyush Gupta <gpiyush@vmware.com> 1.26.1-4
- Bump up version to compile with new go
* Wed May 24 2023 Shivani Agarwal <shivania2@vmware.com> 1.26.1-3
- Bump up version to compile with new etcd
* Wed May 03 2023 Piyush Gupta <gpiyush@vmware.com> 1.26.1-2
- Bump up version to compile with new go
* Thu Mar 16 2023 Prashant S Chauhan <psinghchauha@vmware.com> 1.26.1-1
- Update k8s to 1.26
* Fri Mar 10 2023 Mukul Sikka <msikka@vmware.com> 1.23.8-8
- Use systemd-rpm-macros for user creation
* Thu Mar 09 2023 Piyush Gupta <gpiyush@vmware.com> 1.23.8-7
- Bump up version to compile with new go
* Sun Feb 12 2023 Shreenidhi Shedi <sshedi@vmware.com> 1.23.8-6
- Fix requires
* Thu Nov 24 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.23.8-5
- Bump version as a part of cni upgrade
* Mon Nov 21 2022 Piyush Gupta <gpiyush@vmware.com> 1.23.8-4
- Bump up version to compile with new go
* Wed Oct 26 2022 Piyush Gupta <gpiyush@vmware.com> 1.23.8-3
- Bump up version to compile with new go
* Wed Sep 21 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.23.8-2
- Remove kubectl-extras subpackage
* Fri Jun 17 2022 Piyush Gupta <gpiyush@vmware.com> 1.23.8-1
- Update kubernetes to 1.23.8
* Fri Sep 17 2021 Prashant S Chauhan <psinghchauha@vmware.com> 1.19.15-1
- Update to 1.19.15, Fix CVE-2021-25741
* Tue Sep 07 2021 Keerthana K <keerthanak@vmware.com> 1.19.10-4
- Bump up version to compile with new glibc
* Tue Jun 22 2021 Rishabh Jain <rjain3@vmware.com> 1.19.10-3
- Change 10-kubeadm.conf file permission to 644
* Fri Jun 11 2021 Piyush Gupta<gpiyush@vmware.com> 1.19.10-2
- Bump up version to compile with new go
* Tue May 11 2021 Prashant S Chauhan <psinghchauha@vmware.com> 1.19.10-1
- Update to v1.19.10, fixes CVE-2021-3121. Added patch to fix CVE-2021-25737
* Tue Feb 09 2021 Prashant S Chauhan <psinghchauha@vmware.com> 1.19.7-1
- Update to v1.19.7
* Fri Feb 05 2021 Harinadh D <hdommaraju@vmware.com> 1.18.8-3
- Bump up version to compile with new go
* Fri Jan 15 2021 Piyush Gupta<gpiyush@vmware.com> 1.18.8-2
- Bump up version to compile with new go
* Wed Aug 26 2020 Ashwin H <ashwinh@vmware.com> 1.18.8-1
- Initial version
