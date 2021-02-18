Summary:       Set of scripts and tools to get compatbility with other distributions.
Name:          distrib-compat
Version:       0.1
Release:       1%{?dist}
License:       GPLv2
URL:           http://photon.org
Group:         System Environment/Base
Vendor:        VMware, Inc.
Distribution:  Photon
Source0:       %{name}-%{version}.tar.bz2
%define sha1 distrib-compat=1826157792bc104a7ca5f3b48ef71a04aa318c8b
Source1:       rc.status
Source2:       90-va-tune-up.conf
Source3:       ifup
Source4:       ifdown
Patch0:        distrib-compat-gen-debuginfo.patch

%description
Set of scripts and tools to get compatbility with other distributions.
It includes: rc.status, startproc, killproc, checkproc, ifup and ifdown.

%prep
%setup -q
%patch0

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
*    Thu Feb 18 2021 Ankit Jain <ankitja@vmware.com> 0.1-1
-    Initial build. First version
