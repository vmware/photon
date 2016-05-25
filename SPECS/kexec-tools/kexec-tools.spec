Name:           kexec-tools
Summary:        The kexec kdump tools
Version:        2.0.11
Release:        2%{?dist}
License:        GPLv2
Group:          Applications/System
Url:            https://www.kernel.org/doc/Documentation/kdump/kdump.txt
Source0:        https://www.kernel.org/pub/linux/utils/kernel/kexec/%{name}-%{version}.tar.xz
%define sha1 kexec-tools=6160be260ab1ac28d32cdbb751302600cf664691
Patch0:		kexec-tools-disable-test.patch
Vendor:		VMware, Inc.
Distribution:	Photon

BuildRequires:  zlib-devel
BuildRequires:  zlib
Requires:	zlib

%description
kexec-tools allows booting of a linux kernel from the context of a running kernel using kernel's kexec feature

%prep
%setup -q
%patch0 -p1

%build
%configure
make

%install
make install DESTDIR=%{buildroot}

%files
%{_sbindir}/*
%{_mandir}/man8/*
%doc News
%doc COPYING
%doc TODO

%changelog
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.0.11-2
-	GA - Bump release of all rpms
* 	Fri Feb 26 2016 Anish Swaminathan <anishs@vmware.com>  2.0.11-1
- 	Initial version
