%global debug_package %{nil}
%global __os_install_post %{nil}
%global _firmwarepath    /lib/firmware
%define _binaries_in_noarch_packages_terminate_build   0

Summary:	Linux Firmware
Name:		linux-firmware
Version:	20190205
Release:	1%{?dist}
License:	GPL+ and GPLv2+ and MIT and Redistributable, no modification permitted
URL:		http://www.kernel.org/
Group:		System Environment/Kernel
Vendor:		VMware, Inc.
Distribution:	Photon
Source0:        %{name}-%{version}.tar.gz
%define sha1 linux=505996ad569a99e2b9513cb0d8f227ba4a975991
BuildArch:	noarch

%description
This package includes firmware files required for some devices to operate.

%prep
%setup -q

%build

%install
mkdir -p %{buildroot}%{_firmwarepath}
cp -r brcm %{buildroot}%{_firmwarepath}
cp -r rsi %{buildroot}%{_firmwarepath}
cp rsi_91x.fw %{buildroot}%{_firmwarepath}
cp ppfe_class_ls1012a.elf %{buildroot}%{_firmwarepath}
cp ppfe_tmu_ls1012a.elf %{buildroot}%{_firmwarepath}
cp NXP-Binary-EULA.txt %{buildroot}%{_firmwarepath}
cp -r ath10k %{buildroot}%{_firmwarepath}
cp -r i915 %{buildroot}%{_firmwarepath}
cp -r intel %{buildroot}%{_firmwarepath}
cp iwlwifi-8000C-*.ucode %{buildroot}%{_firmwarepath}

%files
%defattr(-,root,root)
%{_firmwarepath}/*
%changelog
*   Tue Feb 05 2019 Alexey Makhalov <amakhalov@vmware.com> 20190205-1
-   Added ath10k firmware (for ls1012a).
-   Use 1:1 folder layout for ppfe firmware.
*   Wed Jan 09 2019 Alexey Makhalov <amakhalov@vmware.com> 20190109-1
-   Added Compulab Fitlet2 firmware.
*   Thu Nov 29 2018 Srinidhi Rao <srinidhir@vmware.com> 20181129-1
-   Updated pfe firmware files for NXP LS1012A FRWY board
*   Wed Oct 10 2018 Ajay Kaher <akaher@vmware.com> 20181010-1
-   Updated brcm firmwares for Rpi B and Rpi B+
*   Thu Aug 23 2018 Alexey Makhalov <amakhalov@vmware.com> 20180823-1
-   Initial version. RPi3 and Dell Edge Gateway 3001 support.
