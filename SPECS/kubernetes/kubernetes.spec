Summary:        Kubernetes cluster management
Name:           kubernetes
Version:        1.5.2
Release:        1%{?dist}
License:        ASL 2.0
URL:            https://github.com/kubernetes/kubernetes/releases/download/v%{version}
Source0:        https://dl.k8s.io/v1.5.2/kubernetes-server-linux-amd64-v%{version}.tar.gz
%define sha1    kubernetes-server-linux-amd64-v%{version}.tar.gz=4dbdcfa623412dac6be8fd5a4209a1f1423e8d30
Source1:        https://github.com/kubernetes/contrib/archive/contrib-0.7.0.tar.gz
%define sha1 contrib-0.7.0=47a744da3b396f07114e518226b6313ef4b2203c
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon
Requires:       etcd >= 3.0.4
Requires:       shadow

%description
Kubernetes is an open source implementation of container cluster management.

%prep -p exit
%setup -qn %{name}
tar xf %{SOURCE1}
sed -i -e 's|127.0.0.1:4001|127.0.0.1:2379|g' contrib-0.7.0/init/systemd/environ/apiserver

%build

%install
install -vdm644 %{buildroot}/etc/profile.d

install -m 755 -d %{buildroot}%{_bindir}

binaries=(kube-apiserver kube-controller-manager kube-scheduler kube-proxy kubelet kubectl hyperkube)
for bin in "${binaries[@]}"; do
  echo "+++ INSTALLING ${bin}"
  install -p -m 755 -t %{buildroot}%{_bindir} server/bin/${bin}
done

# install config files
install -d -m 0755 %{buildroot}%{_sysconfdir}/%{name}
install -m 644 -t %{buildroot}%{_sysconfdir}/%{name} contrib-0.7.0/init/systemd/environ/*

# install service files
install -d -m 0755 %{buildroot}/usr/lib/systemd/system
install -m 0644 -t %{buildroot}/usr/lib/systemd/system contrib-0.7.0/init/systemd/*.service

# install the place the kubelet defaults to put volumes
install -d %{buildroot}/var/lib/kubelet

%check
export GOPATH=%{_builddir}
go get golang.org/x/tools/cmd/cover
cd kubernetes-e310e619fc1ac4f3238bf5ebe9e7033bf5d47ee2
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

%postun
if [ $1 -eq 0 ]; then
    # Package deletion
    userdel kube
    groupdel kube 
fi

%files
%defattr(-,root,root)
%{_bindir}/*
#%{_mandir}/man1/*
/usr/lib/systemd/system/kube-apiserver.service
/usr/lib/systemd/system/kubelet.service
/usr/lib/systemd/system/kube-scheduler.service
/usr/lib/systemd/system/kube-controller-manager.service
/usr/lib/systemd/system/kube-proxy.service
%dir %{_sysconfdir}/%{name}
%dir /var/lib/kubelet
%config(noreplace) %{_sysconfdir}/%{name}/config
%config(noreplace) %{_sysconfdir}/%{name}/apiserver
%config(noreplace) %{_sysconfdir}/%{name}/controller-manager
%config(noreplace) %{_sysconfdir}/%{name}/proxy
%config(noreplace) %{_sysconfdir}/%{name}/kubelet
%config(noreplace) %{_sysconfdir}/%{name}/scheduler

%changelog
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