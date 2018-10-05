%global security_hardening none
%global debug_package %{nil}
Summary:        U-Boot EFI firmware for the rpi3
Name:		u-boot-rpi3
Version:	2018.09
Release:	1%{?dist}
License:	GPLv2
URL:            http://www.denx.de/wiki/U-Boot
Vendor:		VMware, Inc.
Distribution:	Photon
Source0:        ftp://ftp.denx.de/pub/u-boot/u-boot-%{version}.tar.bz2
%define sha1 u-boot=e43d4fc09395f8cde29d655d35b2bb773e89b444
Patch0:		0001-XXX-openSUSE-XXX-Load-dtb-from-part.patch
Patch1:		0004-Fix-MMC1-external-SD-slot-on-Samsun.patch
BuildRequires:  bc
BuildRequires:  openssl-devel
BuildRequires:  python2-devel
BuildRequires:  swig

%description
Das U-Boot (or just "U-Boot" for short) is Open Source Firmware for
Embedded PowerPC, ARM, MIPS and x86 processors.

%package doc
Summary:        Documentation for the U-Boot Firmware
Group:          Documentation/Other
%description doc
Das U-Boot (or just "U-Boot" for short) is Open Source Firmware for
Embedded PowerPC, ARM, MIPS and x86 processors.

%prep
%setup -q -n u-boot-%{version}
%patch0 -p1
%patch1 -p1

%build
make %{?_smp_mflags} CROSS_COMPILE= HOSTCFLAGS="$RPM_OPT_FLAGS" rpi_3_defconfig
echo "CONFIG_OF_LIBFDT_OVERLAY=y" >> .config
make %{?_smp_mflags} CROSS_COMPILE= HOSTCFLAGS="$RPM_OPT_FLAGS" USE_PRIVATE_LIBGG=yes

%install
install -D -m 0644 u-boot.bin %{buildroot}/boot/esp/u-boot.bin

%files
%defattr(-,root,root)
/boot/esp/*
%doc Licenses/gpl-2.0.txt README

%files doc
%defattr(-,root,root)
# Generic documents
%doc doc/README.JFFS2 doc/README.JFFS2_NAND doc/README.commands
%doc doc/README.autoboot doc/README.commands doc/README.console doc/README.dns
%doc doc/README.hwconfig doc/README.nand doc/README.NetConsole doc/README.serial_multi
%doc doc/README.SNTP doc/README.standalone doc/README.update doc/README.usb
%doc doc/README.video doc/README.VLAN doc/README.silent doc/README.POST
# Copy some useful kermit scripts as well
%doc tools/kermit/dot.kermrc tools/kermit/flash_param tools/kermit/send_cmd tools/kermit/send_image
# Now any h/w dependent Documentation
%doc doc/README.ARM-memory-map

%changelog
*   Thu Sep 13 2018 Michelle Wang <michellew@vmware.com> 2018.09-1
-   Version update to 2018.09
*   Wed Jul 25 2018 Ajay Kaher <akaher@vmware.com> 2018.07-1
-   Version update to u-boot-rpi3-2018.07-1
*   Fri Dec 15 2017 Alexey Makhalov <amakhalov@vmware.com> 2017.11-1
-   Based on OpenSuse u-boot-rpi3-2017.11-266.2 from Thu Nov 16 2017
    by guillaume@opensuse.org
