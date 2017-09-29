# FIXME: noarch or generate debuginfo
%define debug_package %{nil}

Summary:       Set of scripts and tools to get compatbility with other distributions.
Name:          distrib-compat
Version:       0.1
Release:       10%{?dist}
License:       GPLv2
URL:           http://photon.org
Group:         System Environment/Base
Vendor:        VMware, Inc.
Distribution:  Photon
Source0:       %{name}-%{version}.tar.bz2
%define sha1 distrib-compat=1826157792bc104a7ca5f3b48ef71a04aa318c8b
Source1:      rc.status
Source2:      90-va-tune-up.conf
Source3:      ifup
Source4:      ifdown
%description
Set of scripts and tools to get compatbility with other distributions.
It includes: rc.status, startproc, killproc, checkproc, ifup and ifdown.
%prep
%setup -q
%build
make %{?_smp_mflags}
%install
make DESTDIR=%{buildroot} install
install -d -m 0755 %{buildroot}%{_sysconfdir}/sysctl.d
install -m 0644 %{SOURCE1} %{buildroot}/%{_sysconfdir}
install -m 0644 %{SOURCE2} %{buildroot}%{_sysconfdir}/sysctl.d
install -m 0755 %{SOURCE3} %{buildroot}/sbin
install -m 0755 %{SOURCE4} %{buildroot}/sbin
touch %{buildroot}/%{_sysconfdir}/sysctl.d/99-compat.conf
chmod 644 %{buildroot}/%{_sysconfdir}/sysctl.d/99-compat.conf
ln -s sysctl.d/99-compat.conf %{buildroot}/%{_sysconfdir}/sysctl.conf
%files
%defattr(-,root,root)
%{_sysconfdir}/*
/sbin/*
%changelog
*    Wed Sep 7 2016 Divya Thaluru <dthaluru@vmware.com> 0.1-10
-    Clean up
*    Thu Aug 11 2016 Onkar Deshpande <deshpandeo@vmware.com> 0.1-9
-    Clean up
*    Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.1-8
-    GA - Bump release of all rpms
*    Wed May 04 2016 Mahmoud Bassiouny <mbassiouny@vmware.com> 0.1-7
*    ifup should fail if the assigned IP address exists in the network
*    Tue Mar 29 2016 Vinay Kulkarni <kulkarniv@vmware.com> 0.1-6
-    Do arping only for IPv4 addresses.
*    Thu Feb 11 2016 Mahmoud Bassiouny <mbassiouny@vmware.com> 0.1-5
-    Move ifup and ifdown outside the sources tar.gz
*    Wed Feb 10 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.2-2
-    Add systemctl support in rc.status
*    Sun Feb 7 2016 Mahmoud Bassiouny <mbassiouny@vmware.com> 0.2-1
-    Added ifup and ifdown for NIC interfaces
*    Mon Dec 14 2015 Alexey Makhalov <amakhalov@vmware.com> 0.1-4
-    Added sysctl.conf as a symlink. Added 90-va-tune-up.conf
*    Tue Dec 1 2015 Alexey Makhalov <amakhalov@vmware.com> 0.1-3
-    rc.status lower case for msg_* output.
*    Mon Nov 30 2015 Alexey Makhalov <amakhalov@vmware.com> 0.1-2
-    rc_status() enhancements.
*    Mon Nov 16 2015 Alexey Makhalov <amakhalov@vmware.com> 0.1-1
-    Initial build.    First version
