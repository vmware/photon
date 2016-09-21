Summary:        Kubernetes cluster management
Name:           kubernetes
Version:        1.3.7
Release:        1%{?dist}
License:        ASL 2.0
URL:            https://github.com/kubernetes/kubernetes/releases/download/v%{version}
Source0:        https://github.com/GoogleCloudPlatform/kubernetes/releases/download/v%{version}/%{name}-v%{version}.tar.gz
%define sha1 kubernetes-v%{version}.tar.gz=b809b506452fba9df638271c285c049fd0c4abef
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

%build

%install
install -vdm644 %{buildroot}/etc/profile.d
install -vdm755 tmp
tar -C tmp/ -xvf server/kubernetes-server-linux-amd64.tar.gz

install -m 755 -d %{buildroot}%{_bindir}

binaries=(kube-apiserver kube-controller-manager kube-scheduler kube-proxy kubelet kubectl hyperkube)
for bin in "${binaries[@]}"; do
  echo "+++ INSTALLING ${bin}"
  install -p -m 755 -t %{buildroot}%{_bindir} tmp/kubernetes/server/bin/${bin}
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
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}

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
*   Wed Sep 21 2016 Xiaolin Li <xiaolinl@vmware.com> 1.3.7-1
-   Upgraded to version 1.3.7
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
