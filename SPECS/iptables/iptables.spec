Summary:        Linux kernel packet control tool
Name:           iptables
Version:        1.8.3
Release:        6%{?dist}
License:        GPLv2+
URL:            http://www.netfilter.org/projects/iptables
Group:          System Environment/Security
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        http://www.netfilter.org/projects/iptables/files/%{name}-%{version}.tar.bz2
%define sha512  %{name}-%{version}=84b10080646077cbea78b7f3fcc58c6c6e1898213341c69862e1b48179f37a6820c3d84437c896071f966b61aa6d16b132d91948a85fd8c05740f29be3a0986d
Source1:        %{name}.service
Source2:        %{name}
Source3:        %{name}.stop
Source4:        ip4save
Source5:        ip6save

Patch0:         libebt_nflog.c-initialize-len-flag-fields-to-0.patch

BuildRequires:  jansson-devel
BuildRequires:  libmnl-devel
BuildRequires:  libnftnl-devel
BuildRequires:  systemd
BuildRequires:  bison

Requires:       systemd
Requires:       libmnl
Requires:       libnftnl

%description
The next part of this chapter deals with firewalls. The principal
firewall tool for Linux is Iptables. You will need to install
Iptables if you intend on using any form of a firewall.

%package        devel
Summary:        Header and development files for %{name}
Requires:       %{name} = %{version}-%{release}

%description    devel
It contains the libraries and header files to create applications.

%package -n ebtables-nft
Summary:    A filtering tool for a Linux-based bridging firewall.
Requires:   %{name} = %{version}-%{release}

%description -n ebtables-nft
Ethernet bridge tables is a firewalling tool to transparently filter network
traffic passing a bridge. The filtering possibilities are limited to link
layer filtering and some basic filtering on higher network layers.

This tool is the userspace control for the bridge and ebtables-nft kernel
components (built by default in Fedora kernels).

The ebtables-nft tool can be used together with the other Linux filtering tools,
like %{name}. There are no known incompatibility issues.

%prep
%autosetup -p1

%build
sh ./configure --host=%{_host} --build=%{_build} \
    CFLAGS="%{optflags}" \
    CXXFLAGS="%{optflags}" \
    --program-prefix= \
    --disable-dependency-tracking \
    --prefix=%{_prefix} \
    --exec-prefix= \
    --bindir=%{_bindir} \
    --sbindir=%{_sbindir} \
    --sysconfdir=%{_sysconfdir} \
    --datadir=%{_datadir} \
    --includedir=%{_includedir} \
    --libdir=%{_libdir} \
    --libexecdir=%{_libexecdir} \
    --localstatedir=%{_localstatedir} \
    --sharedstatedir=%{_sharedstatedir} \
    --mandir=%{_mandir} \
    --infodir=%{_infodir} \
    --disable-silent-rules \
    --with-xtlibdir=%{_libdir}/%{name} \
    --with-pkgconfigdir=%{_libdir}/pkgconfig \
    --enable-nftables \
    --enable-libipq \
    --enable-devel

make V=0 %{?_smp_mflags}

%install
[ %{buildroot} != "/" ] && rm -rf %{buildroot}/*
make DESTDIR=%{buildroot} install %{?_smp_mflags}
ln -sfv ../../sbin/xtables-multi %{buildroot}%{_libdir}/%{name}-xml
#   Install daemon scripts
install -vdm755 %{buildroot}%{_unitdir}
install -m 644 %{SOURCE1} %{buildroot}%{_unitdir}
install -vdm755 %{buildroot}%{_sysconfdir}/systemd/scripts
install -m 755 %{SOURCE2} %{buildroot}%{_sysconfdir}/systemd/scripts
install -m 755 %{SOURCE3} %{buildroot}%{_sysconfdir}/systemd/scripts
install -m 644 %{SOURCE4} %{buildroot}%{_sysconfdir}/systemd/scripts
install -m 644 %{SOURCE5} %{buildroot}%{_sysconfdir}/systemd/scripts

find %{buildroot} -name '*.a'  -delete
find %{buildroot} -name '*.la' -delete
%{_fixperms} %{buildroot}/*

%preun
%systemd_preun %{name}.service

%post
/sbin/ldconfig
%systemd_post %{name}.service

%postun
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
%{_bindir}/*
%{_sbindir}/ip*
%{_sbindir}/xtables*
%{_unitdir}/%{name}.service
%{_libdir}/%{name}/libip*.so
%{_libdir}/%{name}/libxt*.so
%{_libdir}/%{name}-xml
%{_libdir}/*.so.*
%{_mandir}/man1/*
%{_mandir}/man8/ip*.gz
%{_mandir}/man8/xtables*.gz

%files devel
%defattr(-,root,root)
%{_libdir}/*.so
%{_libdir}/pkgconfig/*
%{_includedir}/*
%{_mandir}/man3/*

%files -n ebtables-nft
%defattr(-,root,root)
%{_libdir}/%{name}/libebt*.so
%{_libdir}/%{name}/libarpt_mangle.so
%{_sbindir}/ebtables-*
%exclude %{_sbindir}/ebtables
%{_sbindir}/arptables-*
%exclude %{_sbindir}/arptables

%{_sysconfdir}/ethertypes
%{_mandir}/man8/ebtables-nft.8.gz
%{_mandir}/man8/arptables*.gz

%changelog
* Wed Jul 13 2022 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 1.8.3-6
- Do not override legacy ebtables, arptables softlink
* Tue May 17 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.8.3-5
- Fix packaging to remove conflict with arptables package
- Apply HCX team's patch to libebt_nflog.c, arptables
* Thu May 12 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.8.3-4
- Add ebtables-nft sub package
* Wed Mar 31 2021 Susant Sahani <ssahani@vmware.com> 1.8.3-3
- Allow IPv6 RA and DHCP6
* Mon Feb 08 2021 Susant Sahani <ssahani@vmware.com> 1.8.3-2
- Set wait option for iptables-restore calls
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
* Thu Dec 10 2015 Xiaolin Li <xiaolinl@vmware.com>  1.4.21-3
- Add systemd to Requires and BuildRequires.
- Use systemctl to enable/disable service.
* Wed May 20 2015 Touseef Liaqat <tliaqat@vmware.com> 1.4.21-2
- Updated group.
* Fri Oct 10 2014 Divya Thaluru <dthaluru@vmware.com> 1.4.21-1
- Initial build.  First version
