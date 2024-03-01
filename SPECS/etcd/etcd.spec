Summary:        Distributed reliable key-value store
Name:           etcd
Version:        3.5.12
Release:        1%{?dist}
License:        Apache License
URL:            https://github.com/etcd-io/etcd/
Group:          System Environment/Security
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        %{name}-%{version}.tar.gz
%define sha512  etcd=6fc8bd64ad63cff71c7645253273418fb3fa262c2da1742dc345576caa733af7cd75acad2f57610c5883e6bf16cffd36bc5a0c89cbbb0793c00c2a4db1c6d14b
Source1:        etcd.service
%ifarch aarch64
Source2:        etcd.sysconfig
%endif

BuildRequires:  go
BuildRequires:  git
Requires(pre):  /usr/sbin/useradd /usr/sbin/groupadd
Requires(postun):/usr/sbin/userdel /usr/sbin/groupdel

%description
A highly-available key value store for shared configuration and service discovery.

%prep
%autosetup -p1

%build
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
install -vdm755 %{buildroot}/var/lib/etcd

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
* Fri Mar 01 2024 Anmol Jain <anmol.jain@broadcom.com> 3.5.12-1
- Version upgrade
* Tue Nov 21 2023 Piyush Gupta <gpiyush@vmware.com> 3.5.9-4
- Bump up version to compile with new go
* Wed Oct 11 2023 Piyush Gupta <gpiyush@vmware.com> 3.5.9-3
- Bump up version to compile with new go
* Fri Aug 18 2023 Piyush Gupta <gpiyush@vmware.com> 3.5.9-2
- Bump up version to compile with new go
* Thu Jul 06 2023 Prashant S Chauhan <psinghchauha@vmware.com> 3.5.9-1
- Update to 3.5.9
* Tue Jun 20 2023 Piyush Gupta <gpiyush@vmware.com> 3.5.1-15
- Bump up version to compile with new go
* Wed May 24 2023 Shivani Agarwal <shivania2@vmware.com> 3.5.1-14
- Fix CVE-2023-32082
* Wed May 10 2023 Mukul Sikka <msikka@vmware.com> 3.5.1-13
- Fix CVE-2021-28235
* Wed May 03 2023 Piyush Gupta <gpiyush@vmware.com> 3.5.1-12
- Bump up version to compile with new go
* Thu Mar 16 2023 Piyush Gupta <gpiyush@vmware.com> 3.5.1-11
- Bump up version to compile with new go
* Tue Dec 20 2022 Piyush Gupta <gpiyush@vmware.com> 3.5.1-10
- Bump up version to compile with new go
* Sun Nov 13 2022 Piyush Gupta <gpiyush@vmware.com> 3.5.1-9
- Bump up version to compile with new go
* Wed Oct 26 2022 Piyush Gupta <gpiyush@vmware.com> 3.5.1-8
- Bump up version to compile with new go
* Thu Sep 15 2022 Piyush Gupta <gpiyush@vmware.com> 3.5.1-7
- Bump up version to compile with new go
* Fri Aug 19 2022 Piyush Gupta <gpiyush@vmware.com> 3.5.1-6
- Bump up version to compile with new go
* Tue Jul 12 2022 Piyush Gupta <gpiyush@vmware.com> 3.5.1-5
- Bump up version to compile with new go
* Sat May 07 2022 Piyush Gupta <gpiyush@vmware.com> 3.5.1-4
- Bump up version to compile with new go
* Tue Feb 22 2022 Piyush Gupta <gpiyush@vmware.com> 3.5.1-3
- Bump up version to compile with new go
* Mon Jan 24 2022 Piyush Gupta <gpiyush@vmware.com> 3.5.1-2
- Bump up version to compile with new go
* Thu Nov 18 2021 Prashant S Chauhan <psinghchauha@vmware.com> 3.5.1-1
- Update to version 3.5.1
* Wed Oct 20 2021 Piyush Gupta <gpiyush@vmware.com> 3.4.13-9
- Bump up version to compile with new go
* Tue Oct 05 2021 Piyush Gupta <gpiyush@vmware.com> 3.4.13-8
- Bump up version to compile with new go
* Wed Sep 08 2021 Nitesh Kumar <kunitesh@vmware.com> 3.4.13-7
- Replacement of ITS suggested words.
* Wed Jun 23 2021 Prashant S Chauhan <psinghchauha@vmware.com> 3.4.13-6
- Change etcd data directory ownership to etcd:etcd as per CIS benchmark
* Fri Jun 11 2021 Piyush Gupta <gpiyush@vmware.com> 3.4.13-5
- Bump up version to compile with new go
* Thu Mar 25 2021 Piyush Gupta<gpiyush@vmware.com> 3.4.13-4
- Bump up version to compile with new go
* Fri Feb 05 2021 Harinadh D <hdommaraju@vmware.com> 3.4.13-3
- Bump up version to compile with new go
* Fri Jan 15 2021 Piyush Gupta<gpiyush@vmware.com> 3.4.13-2
- Bump up version to compile with new go
* Wed Aug 26 2020 Gerrit Photon <photon-checkins@vmware.com> 3.4.13-1
- Automatic Version Bump
* Wed Aug 19 2020 Gerrit Photon <photon-checkins@vmware.com> 3.4.12-1
- Automatic Version Bump
* Mon Jul 27 2020 Gerrit Photon <photon-checkins@vmware.com> 3.4.10-1
- Automatic Version Bump
* Mon Jun 22 2020 Gerrit Photon <photon-checkins@vmware.com> 3.4.9-1
- Automatic Version Bump
* Wed Apr 08 2020 Shreyas B <shreyasb@vmware.com> 3.4.3-2
- Remove vendor dependencies, which is occurs due to Go v1.14.
* Mon Mar 16 2020 Ankit Jain <ankitja@vmware.com> 3.4.3-1
- Update to 3.4.3
* Mon Feb 25 2019 Keerthana K <keerthanak@vmware.com> 3.3.9-2
- Add env variable ETCD_UNSUPPORTED_ARCH=arm64 for arm to start etcd service.
* Fri Sep 21 2018 Sujay G <gsujay@vmware.com> 3.3.9-1
- Bump etcd version to 3.3.9
* Mon Sep 18 2017 Alexey Makhalov <amakhalov@vmware.com> 3.1.5-4
- Remove shadow requires
* Sun Aug 27 2017 Vinay Kulkarni <kulkarniv@vmware.com> 3.1.5-3
- File based configuration for etcd service.
* Wed May 31 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 3.1.5-2
- Provide preset file to deactivate service by default
* Thu Apr 06 2017 Anish Swaminathan <anishs@vmware.com> 3.1.5-1
- Upgraded to version 3.1.5, build from sources
* Fri Sep 2 2016 Xiaolin Li <xiaolinl@vmware.com> 3.0.9-1
- Upgraded to version 3.0.9
* Fri Jun 24 2016 Xiaolin Li <xiaolinl@vmware.com> 2.3.7-1
- Upgraded to version 2.3.7
* Wed May 25 2016 Nick Shi <nshi@vmware.com> 2.2.5-3
- Changing etcd service type from simple to notify
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.2.5-2
- GA - Bump release of all rpms
* Tue Feb 23 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 2.2.5-1
- Upgraded to version 2.2.5
* Tue Jul 28 2015 Divya Thaluru <dthaluru@vmware.com> 2.1.1-2
- Adding etcd service file
* Tue Jul 21 2015 Vinay Kulkarni <kulkarniv@vmware.com> 2.1.1-1
- Update to version etcd v2.1.1
* Tue Mar 10 2015 Divya Thaluru <dthaluru@vmware.com> 2.0.4-1
- Initial build.  First version
