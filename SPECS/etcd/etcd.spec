Summary:	Etcd-2.1.1
Name:		etcd
Version:	2.1.1
Release:	2%{?dist}
License:	Apache License
URL:		https://github.com/coreos/etcd
Group:		System Environment/Security
Vendor:		VMware, Inc.
Distribution:	Photon
Source0:	https://github.com/coreos/etcd/releases/download/v2.1.1/%{name}-v%{version}-linux-amd64.tar.gz
%define sha1 etcd=d90a29e051f8dea2f5bb4200610ccbcec45497d7
Source1:	etcd.service
Requires:	shadow

%description
A highly-available key value store for shared configuration and service discovery.

%prep
%setup -qn %{name}-v%{version}-linux-amd64

%build

%install
install -vdm755 %{buildroot}%{_bindir}
install -vdm755 %{buildroot}/%{_docdir}/%{name}-%{version}
install -vdm755 %{buildroot}/lib/systemd/system

chown -R root:root %{buildroot}%{_bindir}
chown -R root:root %{buildroot}/%{_docdir}/%{name}-%{version}

mv %{_builddir}/%{name}-v%{version}-linux-amd64/etcd %{buildroot}%{_bindir}/
mv %{_builddir}/%{name}-v%{version}-linux-amd64/etcdctl %{buildroot}%{_bindir}/
mv %{_builddir}/%{name}-v%{version}-linux-amd64/README.md %{buildroot}/%{_docdir}/%{name}-%{version}/
mv %{_builddir}/%{name}-v%{version}-linux-amd64/README-etcdctl.md %{buildroot}/%{_docdir}/%{name}-%{version}/

cp %{SOURCE1} %{buildroot}/lib/systemd/system
install -vdm755 %{buildroot}/var/lib/etcd

%check
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}

%post	-p /sbin/ldconfig

%postun	-p /sbin/ldconfig

%clean
rm -rf %{buildroot}/*

%files
%{_bindir}/etcd*
/%{_docdir}/%{name}-%{version}/*
/lib/systemd/system/etcd.service
%dir /var/lib/etcd

%changelog
*	Tue Jul 28 2015 Divya Thaluru <dthaluru@vmware.com> 2.1.1-2
-	Adding etcd service file
*	Tue Jul 21 2015 Vinay Kulkarni <kulkarniv@vmware.com> 2.1.1-1
-	Update to version etcd v2.1.1
*	Tue Mar 10 2015 Divya Thaluru <dthaluru@vmware.com> 2.0.4-1
-	Initial build.	First version
