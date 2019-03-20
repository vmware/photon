# FIXME: noarch or generate debuginfo
%define debug_package %{nil}

Summary:        ipmitool - Utility for IPMI control
Name:           ipmitool
Version:        1.8.18
Release:        2%{?dist}
License:        BSD

Group:          System Environment/Utilities
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        %{name}.tar.gz
%define sha1    ipmitool=63d53065160d8863999b876d1761589955328c33
BuildRequires: autoconf
BuildRequires: automake
BuildRequires: libtool
BuildRequires: glib
BuildRequires: glibc
BuildRequires: cmake
BuildRequires: openssl-devel
BuildRequires: curl
Requires:      openssl
Requires:      curl

%description
This package contains a utility for interfacing with devices that support
the Intelligent Platform Management Interface specification.  IPMI is
an open standard for machine health, inventory, and remote power control.

This utility can communicate with IPMI-enabled devices through either a
kernel driver such as OpenIPMI or over the RMCP LAN protocol defined in
the IPMI specification.  IPMIv2 adds support for encrypted LAN
communications and remote Serial-over-LAN functionality.

It provides commands for reading the Sensor Data Repository (SDR) and
displaying sensor values, displaying the contents of the System Event
Log (SEL), printing Field Replaceable Unit (FRU) information, reading and
setting LAN configuration, and chassis power control.

%prep
%setup -q -n %{name}

%build
./bootstrap
./configure --with-kerneldir \
    --with-rpm-distro= \
    --prefix=%{_prefix} \
    --bindir=%{_bindir} \
    --sbindir=%{_sbindir} \
    --datadir=%{_datadir} \
    --includedir=%{_includedir} \
    --libdir=%{_libdir} \
    --mandir=%{_mandir} \
    --sysconfdir=%{_sysconfdir}
make

%install
make DESTDIR=$RPM_BUILD_ROOT install-strip
mkdir -p %{buildroot}/lib/systemd/system

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

%files
%defattr(755,root,root)
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_sbindir}/*
%{_datadir}/ipmitool/*
%{_mandir}/man*/*
%doc %{_datadir}/doc/ipmitool

%changelog
*   Sun Mar 17 2019 Tapas Kundu <tkundu@vmware.com> 1.8.18-2
-   Updated source to build with openssl 1.1.1
*   Fri Aug 25 2017 Xiaolin Li <xiaolinl@vmware.com> 1.8.18-1
-   Initial build.  First version
