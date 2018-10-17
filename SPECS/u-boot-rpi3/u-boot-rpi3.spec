%global security_hardening none
%global debug_package %{nil}
Summary:        U-Boot EFI firmware for the rpi3
Name:		u-boot-rpi3
Version:	2018.09
Release:	5%{?dist}
License:	GPLv2
Url:            http://www.denx.de/wiki/U-Boot
Vendor:		VMware, Inc.
Distribution:	Photon
Source0:        ftp://ftp.denx.de/pub/u-boot/u-boot-%{version}.tar.bz2
%define sha1 u-boot=e43d4fc09395f8cde29d655d35b2bb773e89b444
Source1:        rpi_3_photon_defconfig
Patch0:		0001-XXX-openSUSE-XXX-Load-dtb-from-part.patch
Patch1:		0004-Fix-MMC1-external-SD-slot-on-Samsun.patch
Patch2:		0005-Fix-no-usb.patch
BuildArch:      aarch64

%description
U-Boot is Open Source Firmware.

%prep
%setup -q -n u-boot-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
cp %{SOURCE1} configs/
make %{?_smp_mflags} CROSS_COMPILE= rpi_3_photon_defconfig
make %{?_smp_mflags} CROSS_COMPILE= USE_PRIVATE_LIBGG=yes

%install
install -D -m 0644 u-boot.bin %{buildroot}/boot/esp/u-boot.bin

%files
%defattr(-,root,root)
/boot/esp/*

%changelog
*   Mon Oct 22 2018 Ajay Kaher <akaher@vmware.com> 2018.09-5
-   Adding BuildArch
*   Mon Oct 22 2018 Alexey Makhalov <amakhalov@vmware.com> 2018.09-4
-   Remove bc, swig, python, openssl buildrequires.
-   Remove doc subpackage.
*   Mon Oct 15 2018 Ajay Kaher <akaher@vmware.com> 2018.09-3
-   Set bootdelay to zero in rpi_3_photon_defconfig
*   Mon Oct 08 2018 Ajay Kaher <akaher@vmware.com> 2018.09-2
-   Disable USB to improve boot time.
*   Thu Sep 13 2018 Michelle Wang <michellew@vmware.com> 2018.09-1
-   Version update to 2018.09
*   Wed Jul 25 2018 Ajay Kaher <akaher@vmware.com> 2018.07-1
-   Version update to u-boot-rpi3-2018.07-1
*   Fri Dec 15 2017 Alexey Makhalov <amakhalov@vmware.com> 2017.11-1
-   Based on OpenSuse u-boot-rpi3-2017.11-266.2 from Thu Nov 16 2017
    by guillaume@opensuse.org
