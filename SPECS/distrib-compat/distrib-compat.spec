Summary:	Set of scripts and tools to get compatbility with other distributions.
Name:		distrib-compat
Version:	0.1
Release:	1%{?dist}
License:	GPLv2
URL:		http://photon.org
Group:		System Environment/Base
Vendor:		VMware, Inc.
Distribution:	Photon
Source0:	%{name}-%{version}.tar.bz2
%define sha1 distrib=1826157792bc104a7ca5f3b48ef71a04aa318c8b
Source1:	rc.status
%description
Set of scripts and tools to get compatbility with other distributions.
It includes: rc.status, startproc, killproc, checkproc.
%prep
%setup -q
%build
make %{?_smp_mflags}
%install
make DESTDIR=%{buildroot} install
install -d -m 0755 %{buildroot}/%{_sysconfdir}
install -m 0644 %{SOURCE1} %{buildroot}/%{_sysconfdir}
%files
%defattr(-,root,root)
%{_sysconfdir}/*
/sbin/*
%changelog
*	Mon Nov 16 2015 Alexey Makhalov <amakhalov@vmware.com> 0.1-1
-	Initial build.	First version
