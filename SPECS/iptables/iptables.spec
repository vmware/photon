%global build_if %{photon_subrelease} >= 92
Summary:        Linux kernel packet control tool
Name:           iptables
Version:        1.8.13
Release:        2%{?dist}
URL:            http://www.netfilter.org/projects/iptables
Group:          System Environment/Security
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        http://www.netfilter.org/projects/iptables/files/%{name}-%{version}.tar.xz

Source1:        %{name}.service
Source2:        %{name}
Source3:        %{name}.stop
Source4:        ip4save
Source5:        ip6save

Source6: license.txt
%include %{SOURCE6}

Requires(post):   systemd
Requires(post):   grep
Requires(preun):  systemd
Requires(postun): systemd

Requires: %{name}-libs = %{version}-%{release}
Requires: %{name}-nft-bin = %{version}-%{release}

BuildRequires:  automake
BuildRequires:  autoconf
BuildRequires:  jansson-devel
BuildRequires:  libmnl-devel
BuildRequires:  libnftnl-devel
BuildRequires:  systemd-devel
BuildRequires:  libpcap-devel

Requires:       libnftnl
Requires:       libmnl
Requires:       jansson
Requires:       alternatives

%description
The next part of this chapter deals with firewalls. The principal
firewall tool for Linux is Iptables. You will need to install
Iptables if you intend on using any form of a firewall.

%package libs
Summary:    Shared libraries provided by iptables
Requires:   libpcap

Conflicts: %{name} < 1.8.9-3%{?dist}

%description libs
%{summary}

%package        nft-bin
Summary:        Minimal binary files for iptables-nft
Requires:       %{name}-libs = %{version}-%{release}

%description    nft-bin
%{summary}

%package        devel
Summary:        Header and development files for iptables
Requires:       %{name}-libs = %{version}-%{release}

%description    devel
It contains the libraries and header files to create applications.

%prep
%autosetup -p1

%build
%configure \
    --disable-silent-rules \
    --with-xtlibdir=%{_libdir}/%{name} \
    --with-pkgconfigdir=%{_libdir}/pkgconfig \
    --enable-libipq \
    --enable-devel  \
    --enable-bpf-compiler \
    --disable-static

%make_build

%install
%make_install %{?_smp_mflags}

# Install daemon scripts
install -vdm755 %{buildroot}%{_unitdir}
install -m 644 %{SOURCE1} %{buildroot}%{_unitdir}
install -vdm755 %{buildroot}%{_sysconfdir}/systemd/scripts
install -m 755 %{SOURCE2} %{buildroot}%{_sysconfdir}/systemd/scripts
install -m 755 %{SOURCE3} %{buildroot}%{_sysconfdir}/systemd/scripts
install -m 644 %{SOURCE4} %{buildroot}%{_sysconfdir}/systemd/scripts
install -m 644 %{SOURCE5} %{buildroot}%{_sysconfdir}/systemd/scripts

%{_fixperms} %{buildroot}/*

%post
if alternatives --display %{name} 2>/dev/null | grep -q "/usr/sbin/%{name}-legacy"; then
    alternatives --remove %{name} %{_sbindir}/%{name}-legacy
fi
if alternatives --display ip6tables 2>/dev/null | grep -q "/usr/sbin/ip6tables-legacy"; then
    alternatives --remove ip6tables %{_sbindir}/ip6tables-legacy
fi
for target in %{name} \
              ip6tables \
              ebtables \
              arptables; do
  alternatives --install %{_sbindir}/${target} ${target} %{_sbindir}/${target}-nft 30000 \
    --slave %{_sbindir}/${target}-save ${target}-save %{_sbindir}/${target}-nft-save \
    --slave %{_sbindir}/${target}-restore ${target}-restore %{_sbindir}/${target}-nft-restore
done
/sbin/ldconfig
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
# Do alternative remove only in case of uninstall
if [ $1 -eq 0 ]; then
  for target in %{name} \
              ip6tables \
              ebtables \
              arptables; do
  alternatives --remove ${target} %{_sbindir}/${target}-nft
  done
fi
/sbin/ldconfig
%systemd_postun_with_restart %{name}.service

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/systemd/scripts/%{name}
%config(noreplace) %{_sysconfdir}/systemd/scripts/%{name}.stop
%config(noreplace) %{_sysconfdir}/systemd/scripts/ip4save
%config(noreplace) %{_sysconfdir}/systemd/scripts/ip6save
%config(noreplace) %{_sysconfdir}/ethertypes
%{_bindir}/*
%{_sbindir}/*
%{_libdir}/%{name}/*
%{_unitdir}/%{name}.service
%{_mandir}/man1/*
%{_mandir}/man8/*
%exclude %{_sbindir}/ip{,6}tables-legacy*
%exclude %{_sbindir}/xtables-legacy-multi
%exclude %{_bindir}/iptables-xml
%exclude %{_mandir}/man1/iptables-xml*
%exclude %{_mandir}/man8/xtables-legacy*
%exclude %{_datadir}/xtables
%exclude %{_datadir}/xtables/iptables.xslt
%exclude %{_libdir}/iptables/lib{arp,eb}t*
%exclude %{_sbindir}/ip{,6}tables-nft*
%exclude %{_sbindir}/{eb,arp}tables-nft*
%exclude %{_sbindir}/xtables-nft-multi
%exclude %{_libdir}/iptables

%files nft-bin
%defattr(-,root,root)
%{_sbindir}/ip{,6}tables-nft*
%{_sbindir}/{eb,arp}tables-nft*
%{_sbindir}/xtables-nft-multi
%dir %{_libdir}/iptables
%{_libdir}/iptables/*

%files libs
%defattr(-,root,root)
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root)
%{_libdir}/*.so
%{_libdir}/pkgconfig/*
%{_includedir}/*
%{_mandir}/man3/*

%changelog
* Thu Apr 09 2026 Brennan Lamoreaux <brennan.lamoreaux@broadcom.com> 1.8.13-2
- Require alternatives instead of chkconfig
* Wed Mar 25 2026 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 1.8.13-1
- Upgrade to 1.8.13
- Disable legacy variant, iptables-nft is now default
* Tue Oct 28 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.8.9-6
- Move sysctl confs to systemd sysctl hardening conf
* Fri Jul 18 2025 Ankit Jain <ankit-aj.jain@broadcom.com> 1.8.9-5
- Bump up to build with latest jansson
* Wed Dec 11 2024 Tapas Kundu <tapas.kundu@broadcom.com> 1.8.9-4
- Release bump for SRP compliance
* Tue Mar 12 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.8.9-3
- Add libs sub-package
* Fri Oct 06 2023 Shreenidhi Shedi <sshedi@vmware.com> 1.8.9-2
- Remove dead symlink iptables-xml from libdir
* Sun Jan 22 2023 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 1.8.9-1
- Enable arptables
- Upgrade to latest
- Introduce alternatives
* Thu Jun 02 2022 Susant Sahani <ssahani@vmware.com> 1.8.8-1
- Updated to version
* Fri Jul 23 2021 Susant Sahani <ssahani@vmware.com> 1.8.7-3
- Drop ip6tables.service
* Tue Mar 30 2021 Susant Sahani <ssahani@vmware.com> 1.8.7-2
- Set wait option for iptables calls
* Thu Feb 11 2021 Susant Sahani <ssahani@vmware.com> 1.8.7-1
- Updated to version
* Mon Apr 06 2020 Susant Sahani <ssahani@vmware.com> 1.8.4-1
- Updated to version 1.8.4
* Tue Jul 30 2019 Shreyas B. <shreyasb@vmware.com> 1.8.3-1
- Updated to version 1.8.3
* Tue Feb 26 2019 Alexey Makhalov <amakhalov@vmware.com> 1.8.0-2
- Flush ip6tables on service stop
* Mon Sep 10 2018 Ankit Jain <ankitja@vmware.com> 1.8.0-1
- Updated to version 1.8.0
* Thu Aug 10 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.6.1-4
- fix ip4save script for upgrade issues.
* Mon Jul 24 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.6.1-3
- use iptables-restore to reload rules.
* Fri Jun 23 2017 Xiaolin Li <xiaolinl@vmware.com> 1.6.1-2
- Add devel package.
* Tue Mar 28 2017 Dheeraj Shetty <dheerajs@vmware.com> 1.6.1-1
- Updated to version 1.6.1
* Wed Jan 18 2017 Alexey Makhalov <amakhalov@vmware.com> 1.6.0-6
- Flush iptables on service stop
* Tue Aug 30 2016 Anish Swaminathan <anishs@vmware.com> 1.6.0-5
- Change config file properties for iptables script
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.6.0-4
- GA - Bump release of all rpms
* Thu May 05 2016 Kumar Kaushik <kaushikk@vmware.com> 1.6.0-3
- Adding package support in pre/post/un scripts section.
* Thu Apr 21 2016 Divya Thaluru <dthaluru@vmware.com> 1.6.0-2
- Enabled iptable service. Added iptable rule to accept ssh connections by default.
* Fri Jan 15 2016 Xiaolin Li <xiaolinl@vmware.com> 1.6.0-1
- Updated to version 1.6.0
* Thu Dec 10 2015 Xiaolin Li <xiaolinl@vmware.com> 1.4.21-3
- Add systemd to Requires and BuildRequires.
- Use systemctl to enable/disable service.
* Wed May 20 2015 Touseef Liaqat <tliaqat@vmware.com> 1.4.21-2
- Updated group.
* Fri Oct 10 2014 Divya Thaluru <dthaluru@vmware.com> 1.4.21-1
- Initial build. First version
