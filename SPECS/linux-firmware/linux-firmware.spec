%global _firmwarepath    /lib/firmware

Summary:	Linux Firmware
Name:		linux-firmware
Version:	20180823
Release:	1%{?dist}
License:	GPL+ and GPLv2+ and MIT and Redistributable, no modification permitted
URL:		http://www.kernel.org/
Group:		System Environment/Kernel
Vendor:		VMware, Inc.
Distribution:	Photon
Source0:        %{name}-%{version}.tar.gz
%define sha1 linux=dd673517c2f12231442dd481fe8885d288707749
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

%files
%defattr(-,root,root)
%{_firmwarepath}/*

%changelog
*   Thu Aug 23 2018 Alexey Makhalov <amakhalov@vmware.com> 20180823-1
-   Initial version. RPi3 and Dell Edge Gateway 3001 support.
