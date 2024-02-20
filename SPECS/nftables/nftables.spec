Summary:        Netfilter Tables userspace utillites
Name:           nftables
Version:        1.0.1
Release:        2%{?dist}
Group:          Development/Security
Vendor:         VMware, Inc.
Distribution:   Photon
License:        GPLv2
URL:            https://netfilter.org/projects/nftables

Source0: %{url}/files/%{name}-%{version}.tar.bz2
%define sha512 %{name}=a0db4d82725509d2a9c638ba7ba55547ad7b5138a5fe686b0e90260d6a65e060dd72a470969c1d69e945303bd2bfc33b2021d9f4141b88befefddc61b7afe10d

Source1: %{name}.service
Source2: %{name}.conf
Source3: nft_ruleset_photon.nft

Patch0: nftables-1.0.1-drop-historyh.patch

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
Requires: libmnl
Requires: gmp
Requires: libnftnl
Requires: iptables
Requires: jansson
Requires: libedit

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
%{_libdir}/libnftables.so.*
%{_unitdir}/%{name}.service
%{_presetdir}/10-%{name}.preset
%{_datadir}/doc/%{name}/examples/*
%{_datadir}/%{name}/*

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
* Thu Feb 22 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.0.1-2
- Add preset for nftables service
* Thu Jan 13 2022 Susant Sahani <ssahani@vmware.com> 1.0.1-1
- Version bump
* Thu Dec 09 2021 Prashant S Chauhan <psinghchauha@vmware.com> 0.9.8-4
- Bump up to compile with python 3.10
* Wed May 12 2021 Susant Sahani <ssahani@vmware.com> 0.9.8-3
- Fixed nftables.conf
* Thu Feb 11 2021 Susant Sahani <ssahani@vmware.com> 0.9.8-2
- Add default rule set for photon
* Sun Jan 24 2021 Susant Sahani <ssahani@vmware.com> 0.9.8-1
- Version bump
* Wed Aug 12 2020 Susant Sahani <ssahani@vmware.com> 0.9.6-1
- Initial RPM release
