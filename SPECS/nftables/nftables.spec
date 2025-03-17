Summary:        Netfilter Tables userspace utillites
Name:           nftables
Version:        1.0.6
Release:        4%{?dist}
Group:          Development/Security
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://netfilter.org/projects/nftables

Source0: %{url}/files/%{name}-%{version}.tar.xz

Source1: %{name}.service
Source2: %{name}.conf
Source3: nft_ruleset_photon.nft

Source4: license.txt
%include %{SOURCE4}

BuildRequires: flex
BuildRequires: bison
BuildRequires: libmnl-devel
BuildRequires: gmp-devel
BuildRequires: readline-devel
BuildRequires: libnftnl-devel
BuildRequires: systemd-devel
BuildRequires: iptables-devel
BuildRequires: jansson-devel
BuildRequires: python3-devel
BuildRequires: libedit-devel

Requires: readline
Requires: systemd
Requires: python3
Requires: %{name}-libs = %{version}-%{release}

%description
Netfilter Tables userspace utilities. nftables is a framework by the
Netfilter Project that provides packet filtering, network address
translation (NAT) and other packet mangling. Two of the most common uses
of nftables is to provide

1. firewall
2. NAT

%package libs
Summary: Shared libs for %{name}
Requires: libmnl
Requires: gmp
Requires: libnftnl
Requires: iptables-libs
Requires: jansson
Requires: libedit

Conflicts: %{name} < 1.0.6-2%{?dist}

%description libs
%{summary}

%package        devel
Summary:        Development library for nftables / libnftables
Requires:       %{name} = %{version}-%{release}

%description devel
Development tools and static libraries and header files for the libnftables library.

%package -n     python3-%{name}
Summary:        Python module providing an interface to libnftables
Requires:       %{name} = %{version}-%{release}

%description -n python3-%{name}
The nftables python module provides an interface to libnftables via ctypes.

%prep
%autosetup -p1

%build
%configure \
    --disable-silent-rules \
    --with-xtables \
    --with-json \
    --disable-man-doc \
    --enable-python \
    --with-python-bin=%{python3} \
    --disable-static

%make_build

%install
%make_install %{?_smp_mflags}

mkdir -p %{buildroot}{%{_unitdir},%{_presetdir}}
cp -a %{SOURCE1} %{buildroot}%{_unitdir}

echo "disable %{name}.service" > %{buildroot}%{_presetdir}/10-%{name}.preset

mkdir -p %{buildroot}%{_sysconfdir}/sysconfig
cp -a %{SOURCE2} %{buildroot}%{_sysconfdir}/sysconfig/
chmod 600 %{buildroot}%{_sysconfdir}/sysconfig/%{name}.conf

mkdir -m 700 -p %{buildroot}%{_sysconfdir}/%{name}
cp -a %{SOURCE3} %{buildroot}%{_sysconfdir}/%{name}
chmod 600 %{buildroot}%{_sysconfdir}/%{name}/*.nft
chmod 700 %{buildroot}%{_sysconfdir}/%{name}

%post
/sbin/ldconfig
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service
/sbin/ldconfig

%files
%defattr(-, root, root)
%license COPYING
%config(noreplace) %{_sysconfdir}/%{name}/
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}.conf
%{_sbindir}/nft
%{_unitdir}/%{name}.service
%{_presetdir}/10-%{name}.preset
%{_datadir}/doc/%{name}/examples/*
%{_datadir}/%{name}/*

%files libs
%defattr(-, root, root)
%{_libdir}/libnftables.so.*

%files devel
%defattr(-, root, root)
%{_libdir}/libnftables.so
%{_libdir}/pkgconfig/libnftables.pc
%{_includedir}/%{name}/libnftables.h

%files -n python3-%{name}
%defattr(-, root, root)
%{python3_sitelib}/%{name}-*.egg-info
%{python3_sitelib}/%{name}/

%changelog
* Thu Dec 12 2024 Ajay Kaher <ajay.kaher@broadcom.com> 1.0.6-4
- Release bump for SRP compliance
* Tue Mar 12 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.0.6-3
- Require iptables-libs
- nftables.service should conflict with iptables.service
* Thu Feb 22 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.0.6-2
- Add libs sub package
- Add preset for nftables service
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
