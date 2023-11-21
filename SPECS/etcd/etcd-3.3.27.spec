Summary:        Distributed reliable key-value store
Name:           etcd
Version:        3.3.27
Release:        17%{?dist}
License:        Apache License
URL:            https://github.com/etcd-io/etcd/
Group:          System Environment/Security
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        %{name}-%{version}.tar.gz
%define sha512  etcd=a4139b6933e3a257c0048950a19d9ab36d9c49ce72e1403069c49ef57cab6f298d87d725017b4bddfbcaf644e1e891835c543cd16480c5b5866e224948cadb8a
Source1:        etcd.service
%ifarch aarch64
Source2:        etcd.sysconfig
%endif
BuildRequires:  go >= 1.10
BuildRequires:  git
Requires(pre):  /usr/sbin/useradd /usr/sbin/groupadd
Requires(postun):/usr/sbin/userdel /usr/sbin/groupdel

%description
A highly-available key value store for shared configuration and service discovery.

%prep
%autosetup -p1

%build
go mod init github.com/coreos/etcd
go mod tidy
go mod vendor
./build

%install
install -vdm755 %{buildroot}%{_bindir}
install -vdm755 %{buildroot}/%{_docdir}/%{name}-%{version}
install -vdm755 %{buildroot}/lib/systemd/system
%ifarch aarch64
install -vdm 0755 %{buildroot}%{_sysconfdir}/sysconfig
%endif
install -vdm 0755 %{buildroot}%{_sysconfdir}/etcd
install -vpm 0755 -T etcd.conf.yml.sample %{buildroot}%{_sysconfdir}/etcd/etcd-default-conf.yml

chown -R root:root %{buildroot}%{_bindir}
chown -R root:root %{buildroot}/%{_docdir}/%{name}-%{version}

mv %{_builddir}/%{name}-%{version}/bin/etcd %{buildroot}%{_bindir}/
mv %{_builddir}/%{name}-%{version}/bin/etcdctl %{buildroot}%{_bindir}/
mv %{_builddir}/%{name}-%{version}/README.md %{buildroot}/%{_docdir}/%{name}-%{version}/
mv %{_builddir}/%{name}-%{version}/etcdctl/README.md %{buildroot}/%{_docdir}/%{name}-%{version}/README-etcdctl.md
mv %{_builddir}/%{name}-%{version}/etcdctl/READMEv2.md %{buildroot}/%{_docdir}/%{name}-%{version}/READMEv2-etcdctl.md

install -vdm755 %{buildroot}/lib/systemd/system-preset
echo "disable etcd.service" > %{buildroot}/lib/systemd/system-preset/50-etcd.preset

cp %{SOURCE1} %{buildroot}/lib/systemd/system
%ifarch aarch64
cp %{SOURCE2} %{buildroot}/etc/sysconfig/etcd
%endif
install -vdm700 %{buildroot}/var/lib/etcd
eu-elfcompress -q -p -t none %{buildroot}%{_bindir}/*

%pre
getent group %{name} >/dev/null || /usr/sbin/groupadd -r %{name}
getent passwd %{name} >/dev/null || /usr/sbin/useradd --comment "etcd Daemon User" --shell /bin/bash -M -r --groups %{name} --home /var/lib/%{name} %{name}

%post   -p /sbin/ldconfig

%postun
/sbin/ldconfig
if [ $1 -eq 0 ] ; then
    /usr/sbin/userdel %{name}
    /usr/sbin/groupdel %{name}
fi

%clean
rm -rf %{buildroot}/*

%files
%{_bindir}/etcd*
/%{_docdir}/%{name}-%{version}/*
/lib/systemd/system/etcd.service
/lib/systemd/system-preset/50-etcd.preset
%attr(0700,%{name},%{name}) %dir /var/lib/etcd
%config(noreplace) %{_sysconfdir}/etcd/etcd-default-conf.yml
%ifarch aarch64
%config(noreplace) %{_sysconfdir}/sysconfig/etcd
%endif

%changelog
* Tue Nov 21 2023 Piyush Gupta <gpiyush@vmware.com> 3.3.27-17
- Bump up version to compile with new go
* Wed Oct 11 2023 Piyush Gupta <gpiyush@vmware.com> 3.3.27-16
- Bump up version to compile with new go
* Tue Sep 26 2023 Piyush Gupta <gpiyush@vmware.com> 3.3.27-15
- Bump up version to compile with new go
* Fri Aug 18 2023 Piyush Gupta <gpiyush@vmware.com> 3.3.27-14
- Bump up version to compile with new go
* Thu Jun 22 2023 Piyush Gupta <gpiyush@vmware.com> 3.3.27-13
- Bump up version to compile with new go
* Wed May 03 2023 Piyush Gupta <gpiyush@vmware.com> 3.3.27-12
- Bump up version to compile with new go
* Tue Apr 04 2023 Piyush Gupta <gpiyush@vmware.com> 3.3.27-11
- Bump up version to compile with new go
* Tue Dec 20 2022 Piyush Gupta <gpiyush@vmware.com> 3.3.27-10
- Bump up version to compile with new go
* Sun Nov 13 2022 Piyush Gupta <gpiyush@vmware.com> 3.3.27-9
- Bump up version to compile with new go
* Wed Oct 26 2022 Piyush Gupta <gpiyush@vmware.com> 3.3.27-8
- Bump up version to compile with new go
* Thu Sep 15 2022 Piyush Gupta <gpiyush@vmware.com> 3.3.27-7
- Bump up version to compile with new go
* Thu Aug 18 2022 Piyush Gupta <gpiyush@vmware.com> 3.3.27-6
- Bump up version to compile with new go
* Mon May 09 2022 Piyush Gupta <gpiyush@vmware.com> 3.3.27-5
- Bump up version to compile with new go
* Wed Mar 16 2022 Piyush Gupta <gpiyush@vmware.com> 3.3.27-4
- Bump up version to compile with new go
* Tue Feb 22 2022 Piyush Gupta <gpiyush@vmware.com> 3.3.27-3
- Bump up version to compile with new go
* Mon Jan 24 2022 Piyush Gupta <gpiyush@vmware.com> 3.3.27-2
- Bump up version to compile with new go
* Wed Jan 12 2022 Prashant S Chauhan <psinghchauha@vmware.com> 3.3.27-1
- Package etcd 3.3.27
