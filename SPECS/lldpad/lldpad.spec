Summary: Intel LLDP Agent
Name:    lldpad
Version: 1.0.1
Release: 2%{?dist}
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

%build
./bootstrap.sh
%configure --disable-static
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install 
find %{buildroot} -name '*.la' -exec rm -f {} ';'
mkdir -p %{buildroot}/lib/systemd/system
mv %{buildroot}/%{_libdir}/systemd/system/lldpad.service \
   	%{buildroot}/lib/systemd/system/lldpad.service
mv %{buildroot}/%{_libdir}/systemd/system/lldpad.socket  \
	%{buildroot}/lib/systemd/system/lldpad.socket

%preun
/bin/systemctl disable lldpad.socket
%post
/sbin/ldconfig
/bin/systemctl enable lldpad.socket

%postun
/sbin/ldconfig

%files
%defattr(-,root,root)
%{_sbindir}/*
%{_libdir}/liblldp_clif.so.*
/etc/bash_completion.d/*
%{_mandir}/man3/*
%{_mandir}/man8/*
%{_includedir}/*
%{_libdir}/pkgconfig/*.pc
%{_libdir}/liblldp_clif.so
/lib/systemd/system/lldpad.service
/lib/systemd/system/lldpad.socket


%changelog
*   Thu Dec 10 2015 Xiaolin Li <xiaolinl@vmware.com>  1.0.1-2
-   Add systemd to Requires and BuildRequires.
-   The source is based on git://open-lldp.org/open-lldp commit 036e314
-   Use systemctl to enable/disable service.
*	Tue Nov 24 2015 Xiaolin Li <xiaolinl@vmware.com> 1.0.1-1
-   Initial build.  First version
