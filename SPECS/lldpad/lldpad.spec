Summary: Intel LLDP Agent
Name:    lldpad
Version: 1.0.1
Release: 6%{?dist}
License: GPLv2
URL: http://open-lldp.org/
Source: %{name}-%{version}.tar.gz
%define sha1 lldpad=71e35298e926f0c03556cede4861dffa36928500
Group:      System Environment/Daemons
Vendor:     VMware, Inc.
Distribution:  Photon

BuildRequires: libconfig
BuildRequires: libnl-devel
BuildRequires: readline-devel
BuildRequires:  systemd
Requires:       systemd
Requires:      libconfig
Requires:      libnl


%description
The lldpad package comes with utilities to manage an LLDP interface with support for reading and configuring TLVs. TLVs and interfaces are individual controlled allowing flexible configuration for TX only, RX only, or TX/RX modes per TLV.

%prep
%setup -q -n open-lldp-036e314
sed -i "s/AM_CFLAGS = -Wall -Werror -Wextra -Wformat=2/AM_CFLAGS = -Wall -Werror -Wextra -Wformat=2 -std=gnu89 -Wno-implicit-fallthrough -Wno-format-truncation/" Makefile.am
sed -i "s/u8 arglen;/u8 arglen = 0;/g" lldp_util.c

%build
./bootstrap.sh
%configure --disable-static
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install 
find %{buildroot} -name '*.la' -exec rm -f {} ';'
mkdir -p %{buildroot}/lib/systemd/system
mkdir -p %{buildroot}%{_sharedstatedir}/%{name}
mv %{buildroot}/%{_libdir}/systemd/system/lldpad.service \
   	%{buildroot}/lib/systemd/system/lldpad.service
mv %{buildroot}/%{_libdir}/systemd/system/lldpad.socket  \
	%{buildroot}/lib/systemd/system/lldpad.socket

%preun
%systemd_preun lldpad.socket
%post
/sbin/ldconfig
%systemd_post lldpad.socket
%postun
/sbin/ldconfig
%systemd_postun_with_restart lldpad.socket

%files
%defattr(-,root,root)
%{_sbindir}/*
%{_libdir}/liblldp_clif.so.*
/etc/bash_completion.d/*
%dir %{_sharedstatedir}/%{name}
%{_mandir}/man3/*
%{_mandir}/man8/*
%{_includedir}/*
%{_libdir}/pkgconfig/*.pc
%{_libdir}/liblldp_clif.so
/lib/systemd/system/lldpad.service
/lib/systemd/system/lldpad.socket


%changelog
*   Mon Aug 13 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 1.0.1-6
-   Suppress build warnings with gcc 7.3
*   Wed May 25 2016 Anish Swaminathan <anishs@vmware.com> 1.0.1-5
-   Add required folder for service to start
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.0.1-4
-   GA - Bump release of all rpms
*   Thu May 05 2016 Kumar Kaushik <kaushikk@vmware.com>  1.0.1-3
-   Adding support in pre/post/un scripts for upgrade.
*   Thu Dec 10 2015 Xiaolin Li <xiaolinl@vmware.com>  1.0.1-2
-   Add systemd to Requires and BuildRequires.
-   The source is based on git://open-lldp.org/open-lldp commit 036e314
-   Use systemctl to enable/disable service.
*   Tue Nov 24 2015 Xiaolin Li <xiaolinl@vmware.com> 1.0.1-1
-   Initial build.  First version
