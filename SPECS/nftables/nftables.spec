Summary:        Netfilter Tables userspace utillites
Name:           nftables
Version:        1.0.6
Release:        1%{?dist}
Group:          Development/Security
Vendor:         VMware, Inc.
Distribution:   Photon
License:        GPLv2
URL:            https://netfilter.org/projects/nftables/
Source0:        %{url}/files/%{name}-%{version}.tar.xz
%define sha512  %{name}=afe08381acd27d39cc94743190b07c579f8c49c4182c9b8753d5b3a0b7d1fe89ed664fdbc19cef1547c3ca4a0c1e32ca4303dba9ec626272fa08c77e88c11119

Source1:        nftables.service
Source2:        nftables.conf
Source3:        nft_ruleset_photon.nft

BuildRequires:  gcc
BuildRequires:  flex
BuildRequires:  bison
BuildRequires:  libmnl-devel
BuildRequires:  gmp-devel
BuildRequires:  readline-devel
BuildRequires:  libnftnl-devel
BuildRequires:  systemd-devel
BuildRequires:  iptables-devel
BuildRequires:  jansson-devel
BuildRequires:  python3-devel
BuildRequires:  libedit-devel

Requires:       libmnl
Requires:       gmp
Requires:       readline
Requires:       libnftnl
Requires:       libedit
Requires:       systemd
Requires:       iptables
Requires:       jansson
Requires:       python3

%description
Netfilter Tables userspace utilities. nftables is a framework by the
Netfilter Project that provides packet filtering, network address
translation (NAT) and other packet mangling. Two of the most common uses
of nftables is to provide

1. firewall
2. NAT

%package        devel
Summary:        Development library for nftables / libnftables
Requires:       %{name} = %{version}-%{release}

%description devel
Development tools and static libraries and header files for the libnftables library.

%package -n     python3-nftables
Summary:        Python module providing an interface to libnftables
Requires:       %{name} = %{version}-%{release}

%description -n python3-nftables
The nftables python module provides an interface to libnftables via ctypes.

%prep
%autosetup -p1

%build
%configure --disable-silent-rules --with-xtables --with-json --disable-man-doc \
           --enable-python --with-python-bin=/usr/bin/python3
%make_build %{?_smp_mflags}

%install
%make_install
find  %{buildroot} -name '*.la' -exec rm -f {} ';'

rm -f  %{buildroot}/%{_libdir}/libnftables.a

mkdir -p  %{buildroot}/%{_unitdir}
cp -a %{SOURCE1}  %{buildroot}/%{_unitdir}/

mkdir -p  %{buildroot}/%{_sysconfdir}/sysconfig
cp -a %{SOURCE2}  %{buildroot}/%{_sysconfdir}/sysconfig/
chmod 600  %{buildroot}/%{_sysconfdir}/sysconfig/nftables.conf

mkdir -m 700 -p  %{buildroot}/%{_sysconfdir}/nftables
cp -a %{SOURCE3}  %{buildroot}/%{_sysconfdir}/nftables
chmod 600  %{buildroot}/%{_sysconfdir}/nftables/*.nft
chmod 700  %{buildroot}/%{_sysconfdir}/nftables

%post
%systemd_post nftables.service

%preun
%systemd_preun nftables.service

%postun
%systemd_postun_with_restart nftables.service

%ldconfig_scriptlets

%files
%defattr(-, root, root)
%license COPYING
%config(noreplace) %{_sysconfdir}/nftables/
%config(noreplace) %{_sysconfdir}/sysconfig/nftables.conf
%{_sbindir}/nft
%{_libdir}/libnftables.so.*
%{_unitdir}/nftables.service
%{_datadir}/doc/nftables/examples/*
%{_datadir}/nftables/*

%files devel
%defattr(-, root, root)
%{_libdir}/libnftables.so
%{_libdir}/pkgconfig/libnftables.pc
%{_includedir}/nftables/libnftables.h

%files -n python3-nftables
%defattr(-, root, root)
%{python3_sitelib}/nftables-*.egg-info
%{python3_sitelib}/nftables/

%changelog
* Wed Jan 04 2023 Susant Sahani <ssahani@vmware.com> 1.0.6-1
- Version bump
* Tue Dec 20 2022 Guruswamy Basavaiah <bguruswamy@vmware.com> 1.0.5-3
- Bump release as a part of readline upgrade
* Fri Dec 02 2022 Prashant S Chauhan <psinghchauha@vmware.com> 1.0.5-2
- Update release to compile with python 3.11
* Tue Aug 30 2022 Susant Sahani <ssahani@vmware.com> 1.0.5-1
- Version bump
* Thu Jun 02 2022 Susant Sahani <ssahani@vmware.com> 1.0.3-1
- Version bump
* Wed Dec 22 2021 Susant Sahani <ssahani@vmware.com> 1.0.1-1
- Version bump
* Mon Aug 02 2021 Susant Sahani <ssahani@vmware.com> 0.9.8-4
- Use ldconfig scriptlets
* Wed May 12 2021 Susant Sahani <ssahani@vmware.com> 0.9.8-3
- Fixed nftables.conf
* Thu Feb 11 2021 Susant Sahani <ssahani@vmware.com> 0.9.8-2
- Add default rule set for photon
* Sun Jan 24 2021 Susant Sahani <ssahani@vmware.com> 0.9.8-1
- Version bump
* Wed Aug 12 2020 Susant Sahani <ssahani@vmware.com> 0.9.6-1
- Initial RPM release
