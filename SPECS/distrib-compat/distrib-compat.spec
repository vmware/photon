Summary:       Set of scripts and tools to get compatbility with other distributions.
Name:          distrib-compat
Version:       0.1
Release:       3%{?dist}
License:       GPLv2
URL:           http://photon.org
Group:         System Environment/Base
Vendor:        VMware, Inc.
Distribution:  Photon

Source0:       %{name}-%{version}.tar.bz2
%define sha512  %{name}=9e63e33d0dd1506b4395da98c7adb66213ddb8074a4a3d45524904288cab3c70d2abe91a78bfdb8ccce259995f07c4d393a5a4e109553236c957a639074cb463
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
%make_build

%install
%make_install %{?_smp_mflags} DIR=%{buildroot}%{_sbindir}
install -d -m 0755 %{buildroot}%{_sysconfdir}/sysctl.d
install -m 0644 %{SOURCE1} %{buildroot}%{_sysconfdir}
install -m 0644 %{SOURCE2} %{buildroot}%{_sysconfdir}/sysctl.d
install -m 0755 %{SOURCE3} %{buildroot}%{_sbindir}
install -m 0755 %{SOURCE4} %{buildroot}%{_sbindir}
touch %{buildroot}%{_sysconfdir}/sysctl.d/99-compat.conf
chmod 644 %{buildroot}%{_sysconfdir}/sysctl.d/99-compat.conf
ln -sfv sysctl.d/99-compat.conf %{buildroot}%{_sysconfdir}/sysctl.conf

%files
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/sysctl.d/*.conf
%{_sysconfdir}/sysctl.conf
%{_sysconfdir}/rc.status
%{_sbindir}/*

%changelog
* Thu Aug 04 2022 Ankit Jain <ankitja@vmware.com> 0.1-3
- preserve the configuartion
* Mon Feb 28 2022 Shreenidhi Shedi <sshedi@vmware.com> 0.1-2
- Fix binary path
* Thu Feb 18 2021 Ankit Jain <ankitja@vmware.com> 0.1-1
- Initial build. First version
