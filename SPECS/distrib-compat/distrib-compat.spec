Summary:	Set of scripts and tools to get compatbility with other distributions.
Name:		distrib-compat
Version:	0.1
Release:	5%{?dist}
License:	GPLv2
URL:		http://photon.org
Group:		System Environment/Base
Vendor:		VMware, Inc.
Distribution:	Photon
Source0:	%{name}-%{version}.tar.bz2
%define sha1 distrib=1826157792bc104a7ca5f3b48ef71a04aa318c8b
Source1:	rc.status
Source2:	90-va-tune-up.conf
%description
Set of scripts and tools to get compatbility with other distributions.
It includes: rc.status, startproc, killproc, checkproc.
%prep
%setup -q
%build
make %{?_smp_mflags}
%install
make DESTDIR=%{buildroot} install
install -d -m 0755 %{buildroot}%{_sysconfdir}/sysctl.d
install -m 0644 %{SOURCE1} %{buildroot}/%{_sysconfdir}
install -m 0644 %{SOURCE2} %{buildroot}%{_sysconfdir}/sysctl.d
touch %{buildroot}/%{_sysconfdir}/sysctl.d/99-compat.conf
chmod 644 %{buildroot}/%{_sysconfdir}/sysctl.d/99-compat.conf
ln -s sysctl.d/99-compat.conf %{buildroot}/%{_sysconfdir}/sysctl.conf
%files
%defattr(-,root,root)
%{_sysconfdir}/*
/sbin/*
%changelog
*       Mon Feb 08 2016 Kumar Kaushik <kaushikk@vmware.com> 0.1-5
-       Replacing rc.status to support re-routing to systemctl config.
*	Mon Dec 14 2015 Alexey Makhalov <amakhalov@vmware.com> 0.1-4
-	Added sysctl.conf as a symlink. Added 90-va-tune-up.conf
*	Tue Dec 1 2015 Alexey Makhalov <amakhalov@vmware.com> 0.1-3
-	rc.status lower case for msg_* output.
*	Mon Nov 30 2015 Alexey Makhalov <amakhalov@vmware.com> 0.1-2
-	rc_status() enhancements.
*	Mon Nov 16 2015 Alexey Makhalov <amakhalov@vmware.com> 0.1-1
-	Initial build.	First version
