Summary:	Tools and libraries to manipulate EFI variables
Name:		efibootmgr
Version:	15
Release:	1%{?dist}
License:	GPLv2
URL:		https://github.com/rhinstaller/efibootmgr/
Group:		System Environment/System Utilities
Vendor:		VMware, Inc.
Distribution: Photon
Source0:	https://github.com/rhinstaller/efibootmgr/releases/download/%{name}-%{version}/%{name}-%{version}.tar.bz2
%define sha1 efibootmgr=9dc7ca7b14a47fc178a5bb7b9c0a79cc05e2b272
BuildRequires: efivar-devel
BuildRequires: pciutils
BuildRequires: zlib
%description
efibootmgr is a userspace application used to modify the Intel Extensible Firmware Interface (EFI) Boot Manager. This application can create and destroy boot entries, change the boot order, change the next running boot option, and more.
%prep
%setup -q
%build
make %{?_smp_mflags} PREFIX=%{_prefix} EFIDIR=BOOT EFI_LOADER=grubx64.efi \
    libdir=%{_libdir} \
    bindir=%{_bindir}
%install
[ %{buildroot} != "/"] && rm -rf %{buildroot}/*
make DESTDIR=%{buildroot} \
    PREFIX=%{_prefix} EFIDIR=BOOT EFI_LOADER=grubx64.efi \
    install
gzip -9 %{buildroot}%{_mandir}/man8/%{name}.8
gzip -9 %{buildroot}%{_mandir}/man8/efibootdump.8

%clean
rm -rf %{buildroot}/*
%files 
%defattr(-,root,root)
%{_sbindir}/*
%{_mandir}/man8/*
%changelog
*   Fri Apr 14 2017 Alexey Makhalov <amakhalov@vmware.com> 15-1
-   Version update.
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.12-2
-   GA - Bump release of all rpms
*   Mon Jul 6 2015 Sharath George <sharathg@vmware.com> 0.12-1
-   Initial build. First version. Install steps from spec file in source.
