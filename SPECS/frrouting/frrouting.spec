Summary:        Internet Routing Protocol
Name:           frr
Version:        8.2.2
Release:        2%{?dist}
License:        GPLv2+
URL:            https://frrouting.org/
Group:          System Environment/Daemons
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  bison
BuildRequires:  c-ares-devel
BuildRequires:  python3-devel
BuildRequires:  python3-sphinx
BuildRequires:  systemd
BuildRequires:  flex
BuildRequires:  gcc
BuildRequires:  json-c-devel
BuildRequires:  libcap-devel
BuildRequires:  make
BuildRequires:  ncurses-devel
BuildRequires:  readline-devel
BuildRequires:  texinfo
BuildRequires:  libyang-devel
BuildRequires:  elfutils-devel
BuildRequires:  python3
BuildRequires:  pcre2-devel

%if 0%{?with_check:1}
BuildRequires:  python3-pytest
%endif

Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://github.com/FRRouting/frr/archive/refs/tags/%{name}-%{version}.tar.gz
%define         sha512 frr=52d8e82979823f61ec6f117db1eb41b23fd8ad3197ae3f9d2cfa3ad9d96636a3d2f0b36720b2041a9261c8b639ddd48e46a2351ce41cb596f7dc432cddf29256

%description
FRRouting is a free software that manages TCP/IP based routing
protocol. It takes multi-server and multi-thread approach to resolve
the current complexity of the Internet.

%package        devel
Summary:        Header and development files for frrouting
Requires: %{name} = %{version}-%{release}
%description    devel
It contains the libraries and header files to create applications

%package pythontools
Summary: python tools for frr

%description pythontools
Python Tools

%package python3
Summary: python3 for frr

%description python3
Python3

%prep
%autosetup -p1 -n %{name}-%{name}-%{version}

./bootstrap.sh

sh ./configure --host=%{_host} --build=%{_build} \
    --prefix=%{_prefix} \
    --bindir=%{_bindir} \
    --sbindir=%{_sbindir} \
    --sysconfdir=%{_sysconfdir} \
    --datadir=%{_datadir} \
    --includedir=%{_includedir} \
    --libdir=%{_libdir} \
    --libexecdir=%{_libdir} \
    --localstatedir=%{_localstatedir} \
    --sharedstatedir=%{_sharedstatedir} \
    --mandir=%{_mandir} \
    --infodir=%{_infodir} \
    --with-moduledir=%{_libdir}/frr/modules \
    --disable-static \
    --disable-werror \
    --enable-multipath=64 \
    --enable-ospfclient \
    --enable-ospfapi \
    --enable-irdp \
    --disable-ldpd \
    --enable-fpm \
    --enable-user=frr \
    --enable-vtysh=yes \

%build
make %{?_smp_mflags}

%if 0%{?with_check:1}
%check
make check %{?_smp_mflags}
%endif

%install
make DESTDIR=%{buildroot} install %{?_smp_mflags}

# Remove debian init script if it was installed
rm -f %{buildroot}%{frr_bindir}/frr

# kill bogus libtool filesvoi
rm -vf %{buildroot}%{_libdir}/frr/modules/*.la
rm -vf %{buildroot}%{_libdir}/*.la
rm -vf %{buildroot}%{_libdir}/frr/libyang_plugins/*.la

# install /etc sources
mkdir -p %{buildroot}%{_unitdir}
install -m644 %{_builddir}/%{name}-%{name}-%{version}/tools/frr.service %{buildroot}%{_unitdir}/frr.service
install -p -m 755 tools/frrinit.sh %{_libexecdir}/frr
install -p -m 755 tools/frrcommon.sh %{_libexecdir}/frrcommon.sh
install -p -m 755 tools/watchfrr.sh %{_libexecdir}/watchfrr.sh

# Delete libtool archives
find %{buildroot} -type f -name "*.la" -delete -print

%post
/sbin/ldconfig
%systemd_post frr.service

%preun
%systemd_preun frr.service

%postun/sbin/ldconfig
%systemd_postun_with_restart frr.service

%files
%doc COPYING
%doc doc/mpls
%doc README.md
%{_unitdir}/frr.service
%{_datadir}/*
%{_bindir}/mtracebis
%{_bindir}/vtysh
%{_infodir}/frr.info.gz
%{_libdir}/libfrr.so*
%{_libdir}/libfrrcares*
%{_libdir}/libfrrospf*
%{_libdir}/frr/modules/bgpd_bmp.so
%exclude %{_libdir}/debug
%{_sbindir}/ospfd
%{_sbindir}/bgpd
%{_sbindir}/frr-reload
%{_sbindir}/frrcommon.sh
%{_sbindir}/frrinit.sh
%{_sbindir}/watchfrr.sh
%{_sbindir}/babeld
%{_sbindir}/eigrpd
%{_sbindir}/fabricd
%{_sbindir}/frr
%{_sbindir}/isisd
%{_sbindir}/nhrpd
%{_sbindir}/bfdd
%{_sbindir}/ospf6d
%{_sbindir}/pathd
%{_sbindir}/pbrd
%{_sbindir}/pimd
%{_sbindir}/ripd
%{_sbindir}/ripngd
%{_sbindir}/ssd
%{_sbindir}/staticd
%{_sbindir}/vrrpd
%{_sbindir}/watchfrr
%{_sbindir}/zebra

%files devel
%{_includedir}/frr/*.h
%{_libdir}/lib*.so
%{_datadir}/man/*
%{_libdir}/frr/modules/*.so
%dir %{_includedir}/frr/ospfapi
%{_includedir}/frr/ospfapi/*.h
%{_includedir}/frr/ospfd/*.h
%{_includedir}/frr/eigrpd/*.h
%{_includedir}/frr/bfdd/*.h
%exclude %{_libdir}/debug

%files pythontools
%{_sbindir}/generate_support_bundle.py
%{_sbindir}/frr-reload.py
%{_sbindir}/frr_babeltrace.py
%exclude %{_libdir}/debug

%changelog
*   Wed Apr 20 2022 Roye Eshed <eshedr@vmware.com> 8.2.2-2
-   Removed the path defines and changed the folder defines in the configure portion as well as
-   changed build requirements and added python3 as a subpackage and some fixes for the  configure.
*   Fri Apr 8 2022 Roye Eshed <eshedr@vmware.com> 8.2-1
-   General fixes including changing relative paths to absolute paths and adding commands for frr.service
*   Wed Apr 6 2022 Roye Eshed <eshedr@vmware.com> 8.2-1
-   First Version created. Based off the frrouting Redhat spec file and modified for photon.
-   https://github.com/FRRouting/frr/blob/master/redhat/frr.spec.in
