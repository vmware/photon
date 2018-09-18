%global security_hardening none
%global commit          553f4857346faa8c5f6ddf9eced4180924890bfc.tar.bz2
%define debug_package %{nil}

Summary:        iPXE open source boot firmware
Name:           ipxe
Version:        d2063b7
Release:        1%{?dist}
License:        GPLv2
URL:            http://ipxe.org
Group:          System Environment/Daemons
Vendor:         VMware, Inc.
Distribution:   Photon
#Download URL:  https://git.ipxe.org/ipxe.git/snapshot/%{commit}.tar.bz2
Source0:        %{name}-%{version}.tar.bz2
%define sha1 ipxe=1fe9e076528b0d39b828cec94c565fa9d58c8550
BuildRequires:  binutils
BuildRequires:  binutils-devel
BuildRequires:  cdrkit
BuildRequires:  gcc
BuildRequires:  libgcc
BuildRequires:  libgcc-devel
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  xz
BuildRequires:  xz-devel
BuildRequires:  zlib
BuildRequires:  zlib-devel

%description
iPXE is the leading open source network boot firmware. It provides a full
PXE implementation enhanced with additional features.

%prep
%setup -q -n %{name}-%{version}

%build
cd src
make %{_smp_mflags}

%install
[ %{buildroot} != "/"] && rm -rf %{buildroot}/*
mkdir -p %{buildroot}/usr/share/ipxe
install -vDm 644 src/bin/ipxe.{dsk,iso,lkrn,usb} %{buildroot}/usr/share/ipxe/
install -vDm 644 src/bin/*.{rom,mrom} %{buildroot}/usr/share/ipxe/

%files
%defattr(-,root,root)
/usr/share/ipxe/ipxe.dsk
/usr/share/ipxe/ipxe.iso
/usr/share/ipxe/ipxe.lkrn
/usr/share/ipxe/ipxe.usb
/usr/share/ipxe/10222000.rom
/usr/share/ipxe/10500940.rom
/usr/share/ipxe/10ec8139.rom
/usr/share/ipxe/15ad07b0.rom
/usr/share/ipxe/1af41000.rom
/usr/share/ipxe/8086100e.mrom
/usr/share/ipxe/8086100f.mrom
/usr/share/ipxe/808610d3.mrom
/usr/share/ipxe/80861209.rom
/usr/share/ipxe/rtl8139.rom

%changelog
*   Wed Aug 08 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> d2063b7-1
-   Update version to get it to build with gcc 7.3
*   Tue Apr 25 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com>  553f485-2
-   disable debuginfo gen
*   Mon Mar 13 2017 Alexey Makhalov <amakhalov@vmware.com> 553f485-1
-   Version update to build with gcc-6.3
-   Removed linux/linux-devel build-time dependency
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> ed0d7c4-2
-   GA - Bump release of all rpms
*   Thu Nov 12 2015 Vinay Kulkarni <kulkarniv@vmware.com> ed0d7c4-1
-   Initial build. First version
