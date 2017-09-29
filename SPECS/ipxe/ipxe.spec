# FIXME: noarch or generate debuginfo
%define debug_package %{nil}

%global security_hardening none
%global commit          ed0d7c4f6f8db7bda1e74567693a0c525b9cf159
%global shortcommit	%(c=%{commit}; echo ${c:0:7})

Summary:        iPXE open source boot firmware
Name:           ipxe
Version:        ed0d7c4
Release:        2%{?dist}
License:        GPLv2
URL:            http://ipxe.org
Group:          System Environment/Daemons
Vendor:         VMware, Inc.
Distribution:   Photon
#Download URL:  https://git.ipxe.org/ipxe.git/snapshot/ed0d7c4f6f8db7bda1e74567693a0c525b9cf159.tar.gz
Source0:        %{name}-%{version}.tar.gz
%define sha1 ipxe=16db273987f525176d9ca6d97c40eb2076a1b47f

BuildRequires:  binutils
BuildRequires:  binutils-devel
BuildRequires:  cdrkit
BuildRequires:  gcc
BuildRequires:  libgcc
BuildRequires:  libgcc-devel
BuildRequires:  make
BuildRequires:  linux
BuildRequires:  linux-dev
BuildRequires:  perl
BuildRequires:  xz
BuildRequires:  xz-devel
BuildRequires:  zlib
BuildRequires:  zlib-devel

%description
iPXE is the leading open source network boot firmware. It provides a full
PXE implementation enhanced with additional features.

%prep
%setup -q -n %{name}-%{shortcommit}

%build
cd src
make %{_smp_mflags}

%install
[ %{buildroot} != "/"] && rm -rf %{buildroot}/*
mkdir -p %{buildroot}/usr/share/ipxe
install -vDm 644 src/bin/ipxe.{dsk,iso,lkrn,usb} %{buildroot}/usr/share/ipxe/
install -vDm 644 src/bin/*.{rom,mrom} %{buildroot}/usr/share/ipxe/

%check
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}

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
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> ed0d7c4-2
-	GA - Bump release of all rpms
*       Thu Nov 12 2015 Vinay Kulkarni <kulkarniv@vmware.com> ed0d7c4-1
-       Initial build. First version
