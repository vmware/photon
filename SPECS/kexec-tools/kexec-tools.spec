Name:           kexec-tools
Summary:        The kexec kdump tools
Version:        2.0.17
Release:        1%{?dist}
License:        GPLv2
Group:          Applications/System
Url:            https://www.kernel.org/doc/Documentation/kdump/kdump.txt
Source0:        https://www.kernel.org/pub/linux/utils/kernel/kexec/%{name}-%{version}.tar.xz
%define sha1 kexec-tools=8936b2e0eea3334c656a0004d514ed9795691393
Source1:        kdump.service
Patch0:		kexec-tools-disable-test.patch
Patch1:		0001-kexec-fix-for-Unhandled-rela-relocation-R_X86_64_PLT.patch
Vendor:		VMware, Inc.
Distribution:	Photon

BuildRequires:  zlib-devel
BuildRequires:  zlib
BuildRequires:  systemd
Requires:	zlib

%description
kexec-tools allows booting of a linux kernel from the context of a running kernel using kernel's kexec feature

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%configure
make

%install
make install DESTDIR=%{buildroot}
mkdir -p %{buildroot}/lib/systemd/system/
install -m644 %{SOURCE1} %{buildroot}/lib/systemd/system/kdump.service

%post
%systemd_post kdump.service

%preun
%systemd_preun kdump.service

%postun
%systemd_postun_with_restart kdump.service

%files
%{_sbindir}/*
%{_mandir}/man8/*
/lib/systemd/system/kdump.service
%doc News
%doc COPYING
%doc TODO

%changelog
*   Fri Aug 24 2018 Him Kalyan Bordoloi <bordoloih@vmware.com> 2.0.17-1
-   Updated to version 2.0.17
-   Added patch to handle R_X86_64_PLT relocation
*   Mon Apr 03 2017 Divya Thaluru <dthaluru@vmware.com> 2.0.14-1
-   Updated to version 2.0.14
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.0.11-2
-   GA - Bump release of all rpms
*   Fri Feb 26 2016 Anish Swaminathan <anishs@vmware.com>  2.0.11-1
-   Initial version
