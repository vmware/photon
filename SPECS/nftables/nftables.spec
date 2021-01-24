%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Summary:        Netfilter Tables userspace utillites
Name:           nftables
Version:        0.9.8
Release:        1%{?dist}
Group:          Development/Security
Vendor:         VMware, Inc.
Distribution:   Photon
License:        GPLv2
URL:            https://netfilter.org/projects/nftables/
Source0:        %{url}/files/%{name}-%{version}.tar.bz2
%define sha1    nftables=c15ac5552959c8358975f6b3e15757841c6904c8
Source1:        nftables.service
Source2:        nftables.conf

BuildRequires:  gcc
BuildRequires:  flex
BuildRequires:  bison
BuildRequires:  libmnl-devel
BuildRequires:  gmp-devel
BuildRequires:  readline-devel
BuildRequires:  libnftnl-devel
BuildRequires:  systemd
BuildRequires:  iptables-devel
BuildRequires:  jansson-devel
BuildRequires:  python3-devel

Requires:       libmnl
Requires:       gmp
Requires:       readline
Requires:       libnftnl
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
make %{?_smp_mflags}

%install
%make_install
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

rm -f $RPM_BUILD_ROOT/%{_libdir}/libnftables.a

mkdir -p $RPM_BUILD_ROOT/%{_unitdir}
cp -a %{SOURCE1} $RPM_BUILD_ROOT/%{_unitdir}/

mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/sysconfig
cp -a %{SOURCE2} $RPM_BUILD_ROOT/%{_sysconfdir}/sysconfig/
chmod 600 $RPM_BUILD_ROOT/%{_sysconfdir}/sysconfig/nftables.conf

mkdir -m 700 -p $RPM_BUILD_ROOT/%{_sysconfdir}/nftables
chmod 600 $RPM_BUILD_ROOT/%{_sysconfdir}/nftables/*.nft
chmod 700 $RPM_BUILD_ROOT/%{_sysconfdir}/nftables

%post
%systemd_post nftables.service
/sbin/ldconfig

%preun
%systemd_preun nftables.service

%postun
%systemd_postun_with_restart nftables.service
/sbin/ldconfig

%files
%defattr(-, root, root)
%license COPYING
%config(noreplace) %{_sysconfdir}/nftables/
%config(noreplace) %{_sysconfdir}/sysconfig/nftables.conf
%{_sbindir}/nft
%{_libdir}/libnftables.so.*
%{_unitdir}/nftables.service
%{_datadir}/doc/nftables/examples/*

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
* Sun Jan 24 2021 Susant Sahani <ssahani@vmware.com> 0.9.8-1
- Version bump
* Wed Aug 12 2020 Susant Sahani <ssahani@vmware.com> 0.9.6-1
- Initial RPM release
