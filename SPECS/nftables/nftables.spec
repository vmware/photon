%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Summary:        Netfilter Tables userspace utillites
Name:           nftables
Version:        1.0.3
Release:        1%{?dist}
Group:          Development/Security
Vendor:         VMware, Inc.
Distribution:   Photon
License:        GPLv2
URL:            https://netfilter.org/projects/nftables/
Source0:        %{url}/files/%{name}-%{version}.tar.bz2
%define sha512  nftables=83252c0275f20243065c4d77dfca4ab2b70b4042c9491fb3323eb60c96f9a6e0d69699a641457f3d629d078269ba62ce766ffdb2ad79c64bd54ad11943819900
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
