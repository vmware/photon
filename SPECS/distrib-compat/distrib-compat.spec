Summary:       Set of scripts and tools to get compatbility with other distributions.
Name:          distrib-compat
Version:       0.1
Release:       2%{?dist}
License:       GPLv2
URL:           http://photon.org
Group:         System Environment/Base
Vendor:        VMware, Inc.
Distribution:  Photon
Source0:       %{name}-%{version}.tar.bz2
%define sha512 distrib-compat=9e63e33d0dd1506b4395da98c7adb66213ddb8074a4a3d45524904288cab3c70d2abe91a78bfdb8ccce259995f07c4d393a5a4e109553236c957a639074cb463
Source1:       rc.status
Source2:       90-va-tune-up.conf
Source3:       ifup
Source4:       ifdown
Patch0:        distrib-compat-gen-debuginfo.patch

%description
Set of scripts and tools to get compatbility with other distributions.
It includes: rc.status, startproc, killproc, checkproc, ifup and ifdown.

%prep
%autosetup -p1

%build
make %{?_smp_mflags}

%install
make %{?_smp_mflags} DESTDIR=%{buildroot} install
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
%config(noreplace) %{_sysconfdir}/sysctl.d/*.conf
%{_sysconfdir}/sysctl.conf
%{_sysconfdir}/rc.status
/sbin/*

%changelog
* Thu Aug 04 2022 Ankit Jain <ankitja@vmware.com> 0.1-2
- preserve the configuartion
* Thu Feb 18 2021 Ankit Jain <ankitja@vmware.com> 0.1-1
- Initial build. First version
