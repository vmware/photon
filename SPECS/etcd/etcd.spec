Summary:	Etcd-2.0.4
Name:		etcd
Version:	2.0.4
Release:	1
License:	Apache License
URL:		https://github.com/coreos/etcd
Group:		System Environment/Security
Vendor:		VMware, Inc.
Distribution:	Photon
Source0:	https://github.com/coreos/etcd/releases/download/v2.0.4/%{name}-v%{version}-linux-amd64.tar.gz
Requires:	shadow
%description
A highly-available key value store for shared configuration and service discovery.

%prep
%setup -qn %{name}-v%{version}-linux-amd64
%build
%install
install -vdm755 %{buildroot}%{_bindir}
install -vdm755 %{buildroot}/%{_docdir}/%{name}-%{version}

chown -R root:root %{buildroot}%{_bindir}
chown -R root:root %{buildroot}/%{_docdir}/%{name}-%{version}

mv %{_builddir}/%{name}-v%{version}-linux-amd64/etcd %{buildroot}%{_bindir}/
mv %{_builddir}/%{name}-v%{version}-linux-amd64/etcdctl %{buildroot}%{_bindir}/
mv %{_builddir}/%{name}-v%{version}-linux-amd64/etcd-migrate %{buildroot}%{_bindir}/
mv %{_builddir}/%{name}-v%{version}-linux-amd64/README.md %{buildroot}/%{_docdir}/%{name}-%{version}/
mv %{_builddir}/%{name}-v%{version}-linux-amd64/README-etcdctl.md %{buildroot}/%{_docdir}/%{name}-%{version}/

%check
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}
%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig
%clean
rm -rf %{buildroot}/*
%files
%{_bindir}/*
/%{_docdir}/%{name}-%{version}/*
%changelog
*	Tue Mar 10 2015 Divya Thaluru <dthaluru@vmware.com> 2.0.4-1
-	Initial build.	First version
