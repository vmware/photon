%global security_hardening none
%global debug_package %{nil}
Summary:        U-Boot EFI firmware utility for the rpi3
Name:		u-boot-utils
Version:	2019.01
Release:	1%{?dist}
License:	GPLv2
Url:            http://www.denx.de/wiki/U-Boot
Vendor:		VMware, Inc.
Distribution:	Photon
Source0:        ftp://ftp.denx.de/pub/u-boot/u-boot-%{version}.tar.bz2
%define sha1 u-boot=3c4d22eea02032488e1a4cc5da202bb2469cf6fa
Source1:        rpi_3_photon_defconfig
Source2:        fw_env.config
Group:          Development/Tools
BuildArch:      aarch64

%description
U-Boot is Open Source Firmware.

%prep
%setup -q -n u-boot-%{version}

%build
cp %{SOURCE1} configs/
cp %{SOURCE2} .
make %{?_smp_mflags} CROSS_COMPILE= rpi_3_photon_defconfig
make %{?_smp_mflags} CROSS_COMPILE= USE_PRIVATE_LIBGG=yes envtools


%install
install -D -m 0744 tools/env/fw_printenv %{buildroot}/usr/bin/fw_setenv
install -D -m 0644 fw_env.config %{buildroot}/etc/fw_env.config

%files
%defattr(-,root,root)
/etc/fw_env.config
/usr/bin/fw_setenv

%changelog
*   Mon Feb 25 2019 Tapas Kundu <tkundu@vmware.com> 2019.01-1
-   Initial build for 2019.01
