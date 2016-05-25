Summary:	Tools and libraries to manipulate EFI variables
Name:		efibootmgr
Version:	0.12
Release:	2%{?dist}
License:	GPLv2
URL:		https://github.com/rhinstaller/efibootmgr/
Group:		System Environment/System Utilities
Vendor:		VMware, Inc.
Distribution: Photon
Source0:	https://github.com/rhinstaller/efibootmgr/releases/download/%{name}-%{version}/%{name}-%{version}.tar.bz2
%define sha1 efibootmgr=eecdacb6eca67bbc318dd03e496f1854214aa79c
BuildRequires: efivar
BuildRequires: pciutils
BuildRequires: zlib
%description
efivar provides a simle CLI to the UEFI variable facility
%prep
%setup -q
%build
make %{?_smp_mflags} PREFIX=%{_prefix} \
    libdir=%{_libdir} \
    bindir=%{_bindir}
%install
[ %{buildroot} != "/"] && rm -rf %{buildroot}/*
mkdir -p %{buildroot}%{_sbindir} %{buildroot}%{_mandir}/man8
install -p --mode 755 src/%{name}/%{name} %{buildroot}%{_sbindir}
gzip -9 -c src/man/man8/%{name}.8 > src/man/man8/%{name}.8.gz
touch -r src/man/man8/%{name}.8 src/man/man8/%{name}.8.gz
install -p --mode 644 src/man/man8/%{name}.8.gz %{buildroot}%{_mandir}/man8
%clean
rm -rf %{buildroot}/*
%files 
%defattr(-,root,root)
%{_sbindir}/%{name}
%{_mandir}/man8/%{name}.8.gz
%changelog
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 	0.12-2
-	GA - Bump release of all rpms
*	Mon Jul 6 2015 Sharath George <sharathg@vmware.com> 0.12-1
-	Initial build.	First version. Install steps from spec file in source.
