%ifarch x86_64
%define archname amd64
%endif
%ifarch aarch64
%define archname arm64
%endif

Summary:        Kubernetes cluster management
Name:           kubernetes
Version:        1.10.7
Release:        2%{?dist}
License:        ASL 2.0
URL:            https://github.com/kubernetes/kubernetes/archive/v%{version}.tar.gz
Source0:        kubernetes-%{version}.tar.gz
%define sha1    kubernetes-%{version}.tar.gz=39c24846730ae3902a9ce5b49ec9fce7336441d4
Source1:        https://github.com/kubernetes/contrib/archive/contrib-0.7.0.tar.gz
%define sha1    contrib-0.7.0=47a744da3b396f07114e518226b6313ef4b2203c
Patch0:         k8s-1.10-vke.patch
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon
BuildRequires:  go = 1.9.4
BuildRequires:  rsync
BuildRequires:  which
Requires:       cni
Requires:       ebtables
Requires:       etcd >= 3.0.4
Requires:       ethtool
Requires:       iptables
Requires:       iproute2
Requires(pre):  /usr/sbin/useradd /usr/sbin/groupadd
Requires(postun):/usr/sbin/userdel /usr/sbin/groupdel
Requires:       socat
Requires:       (util-linux or toybox)

%description
Kubernetes is an open source implementation of container cluster management.

%package        kubeadm
Summary:        kubeadm deployment tool
Group:          Development/Tools
Requires:       %{name} = %{version}
%description    kubeadm
kubeadm is a tool that enables quick and easy deployment of a kubernetes cluster.

%package	kubectl-extras
Summary:	kubectl binaries for extra platforms
Group:		Development/Tools
%description	kubectl-extras
Contains kubectl binaries for additional platforms.

%package        pause
Summary:        pause binary
Group:          Development/Tools
%description    pause
A pod setup process that holds a pod's namespace.

%prep -p exit
%setup -qn %{name}-%{version}
cd ..
tar xf %{SOURCE1} --no-same-owner
sed -i -e 's|127.0.0.1:4001|127.0.0.1:2379|g' contrib-0.7.0/init/systemd/environ/apiserver
cd %{name}-%{version}
%patch0 -p1

%build
make
pushd build/pause
mkdir -p bin
gcc -Os -Wall -Werror -static -o bin/pause-%{archname} pause.c
strip bin/pause-%{archname}
popd

%ifarch x86_64
make WHAT="cmd/kubectl" KUBE_BUILD_PLATFORMS="darwin/%{archname} windows/%{archname}"
%endif

%install
install -vdm644 %{buildroot}/etc/profile.d
install -m 755 -d %{buildroot}%{_bindir}
install -m 755 -d %{buildroot}/opt/vmware/kubernetes
install -m 755 -d %{buildroot}/opt/vmware/kubernetes/linux/%{archname}

%ifarch x86_64
install -m 755 -d %{buildroot}/opt/vmware/kubernetes/darwin/%{archname}
install -m 755 -d %{buildroot}/opt/vmware/kubernetes/windows/%{archname}
%endif

binaries=(cloud-controller-manager hyperkube kube-aggregator kube-apiserver kube-controller-manager kubelet kube-proxy kube-scheduler kubectl)
for bin in "${binaries[@]}"; do
  echo "+++ INSTALLING ${bin}"
  install -p -m 755 -t %{buildroot}%{_bindir} _output/local/bin/linux/%{archname}/${bin}
done
install -p -m 755 -t %{buildroot}%{_bindir} build/pause/bin/pause-%{archname}

# kubectl-extras
install -p -m 755 -t %{buildroot}/opt/vmware/kubernetes/linux/%{archname}/ _output/local/bin/linux/%{archname}/kubectl
%ifarch x86_64
install -p -m 755 -t %{buildroot}/opt/vmware/kubernetes/darwin/%{archname}/ _output/local/bin/darwin/%{archname}/kubectl
install -p -m 755 -t %{buildroot}/opt/vmware/kubernetes/windows/%{archname}/ _output/local/bin/windows/%{archname}/kubectl.exe
%endif

# kubeadm install
install -vdm644 %{buildroot}/etc/systemd/system/kubelet.service.d
install -p -m 755 -t %{buildroot}%{_bindir} _output/local/bin/linux/%{archname}/kubeadm
install -p -m 755 -t %{buildroot}/etc/systemd/system build/rpms/kubelet.service
install -p -m 755 -t %{buildroot}/etc/systemd/system/kubelet.service.d build/rpms/10-kubeadm.conf
sed -i '/KUBELET_CGROUP_ARGS=--cgroup-driver=systemd/d' %{buildroot}/etc/systemd/system/kubelet.service.d/10-kubeadm.conf

cd ..
# install config files
install -d -m 0755 %{buildroot}%{_sysconfdir}/%{name}
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

mkdir -p %{buildroot}/%{_lib}/tmpfiles.d
cat << EOF >> %{buildroot}/%{_lib}/tmpfiles.d/kubernetes.conf
d /var/run/kubernetes 0755 kube kube -
EOF

%check
export GOPATH=%{_builddir}
go get golang.org/x/tools/cmd/cover
make %{?_smp_mflags} check

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
%{_bindir}/hyperkube
%{_bindir}/kube-aggregator
%{_bindir}/kube-apiserver
%{_bindir}/kube-controller-manager
%{_bindir}/kubelet
%{_bindir}/kube-proxy
%{_bindir}/kube-scheduler
%{_bindir}/kubectl
#%{_bindir}/kubefed
%{_lib}/systemd/system/kube-apiserver.service
%{_lib}/systemd/system/kubelet.service
%{_lib}/systemd/system/kube-scheduler.service
%{_lib}/systemd/system/kube-controller-manager.service
%{_lib}/systemd/system/kube-proxy.service
%{_lib}/tmpfiles.d/kubernetes.conf
%dir %{_sysconfdir}/%{name}
%dir /var/lib/kubelet
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

%files kubectl-extras
%defattr(-,root,root)
/opt/vmware/kubernetes/linux/%{archname}/kubectl
%ifarch x86_64
/opt/vmware/kubernetes/darwin/%{archname}/kubectl
/opt/vmware/kubernetes/windows/%{archname}/kubectl.exe
%endif

%changelog
*   Wed Oct 10 2018 Ajay Kaher <akaher@vmware.com> 1.10.7-2
-   For aarch64 excluded drawin/arm64 and windows/arm64
*   Wed Aug 29 2018 Dheeraj Shetty <dheerajs@vmware.com> 1.10.7-1
-   Update to k8s version 1.10.7 with VKE patch (fbdcc5c) and add
-   kubectl-extras package
*   Thu May 03 2018 Xiaolin Li <xiaolinl@vmware.com> 1.10.2-1
-   Add kubernetes 1.10.2.
*   Tue Jan 30 2018 Ashok Chandrasekar <ashokc@vmware.com> 1.8.1-6
-   Fix password issue in cascade cloud provider.
*   Tue Jan 23 2018 Ashok Chandrasekar <ashokc@vmware.com> 1.8.1-5
-   Add Cascade cloud provider.
*   Wed Nov 15 2017 Alexey Makhalov <amakhalov@vmware.com> 1.8.1-4
-   Aarch64 support
*   Wed Nov 15 2017 Vinay Kulkarni <kulkarniv@vmware.com> 1.8.1-3
-   Specify --kubeconfig to pass in config file.
*   Tue Nov 07 2017 Vinay Kulkarni <kulkarniv@vmware.com> 1.8.1-2
-   Specify API server via kubeconfig file.
*   Wed Nov 01 2017 Vinay Kulkarni <kulkarniv@vmware.com> 1.8.1-1
-   k8s v1.8.1.
*   Mon Sep 18 2017 Alexey Makhalov <amakhalov@vmware.com> 1.7.5-2
-   Requires util-linux or toybox
-   Remove shadow from requires and use explicit tools for post actions
*   Mon Sep 11 2017 Vinay Kulkarni <kulkarniv@vmware.com> 1.7.5-1
-   k8s v1.7.5.
*   Thu Aug 03 2017 Vinay Kulkarni <kulkarniv@vmware.com> 1.7.0-3
-   PhotonOS based k8s pause container.
*   Sat Jul 22 2017 Vinay Kulkarni <kulkarniv@vmware.com> 1.7.0-2
-   Split kubeadm into its own pkg.
*   Fri Jul 14 2017 Vinay Kulkarni <kulkarniv@vmware.com> 1.7.0-1
-   Upgrade kubernetes to v1.7.0.
*   Tue May 09 2017 Vinay Kulkarni <kulkarniv@vmware.com> 1.6.0-3
-   Fix kubernetes dependencies.
*   Thu May 04 2017 Vinay Kulkarni <kulkarniv@vmware.com> 1.6.0-2
-   Include cloud-controller-manager, kube-aggregator binaries.
*   Tue Mar 28 2017 Vinay Kulkarni <kulkarniv@vmware.com> 1.6.0-1
-   Build kubernetes 1.6.0 from source.
*   Mon Feb 13 2017 Vinay Kulkarni <kulkarniv@vmware.com> 1.5.2-3
-   Added kubeadm, kubefed, dns, discovery to package.
*   Fri Jan 27 2017 Xiaolin Li <xiaolinl@vmware.com> 1.5.2-2
-   Added /lib/tmpfiles.d/kubernetes.conf.
*   Thu Jan 19 2017 Xiaolin Li <xiaolinl@vmware.com> 1.5.2-1
-   Upgraded to version 1.5.2
*   Fri Oct 21 2016 Xiaolin Li <xiaolinl@vmware.com> 1.4.4-1
-   Upgraded to version 1.4.4
*   Wed Sep 21 2016 Xiaolin Li <xiaolinl@vmware.com> 1.4.0-1
-   Upgraded to version 1.4.0
*   Fri Jun 24 2016 Xiaolin Li <xiaolinl@vmware.com> 1.2.4-1
-   Upgraded to version 1.2.4
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.1.8-4
-   GA - Bump release of all rpms
*   Wed May 18 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.1.8-3
-   Fix if syntax
*   Thu May 05 2016 Kumar Kaushik <kaushikk@vmware.com> 1.1.8-2
-   Adding support to pre/post/un scripts for package upgrade.
*   Tue Feb 23 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 1.1.8-1
-   Upgraded to version 1.1.8
*   Mon Aug 3 2015 Tom Scanlan <tscanlan@vmware.com> 1.0.2-1
-   bump up to latest release
*   Thu Jul 23 2015 Vinay Kulkarni <kulkarniv@vmware.com> 1.0.1-1
-   Upgrade to kubernetes v1.0.1
*   Tue Mar 10 2015 Divya Thaluru <dthaluru@vmware.com> 0.12.1-1
-   Initial build. First version
