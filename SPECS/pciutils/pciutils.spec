Summary:	System utilities to list pci devices
Name:		pciutils
Version:	3.5.4
Release:	1%{?dist}
License:	GPLv2
URL:		https://www.kernel.org/pub/software/utils/pciutils/
Group:		System Environment/System Utilities
Vendor:		VMware, Inc.
Distribution: Photon
Source0:	https://www.kernel.org/pub/software/utils/pciutils/%{name}-%{version}.tar.gz
%define sha1 pciutils=4fc1ec91181a1211e7af0f1889b14d17dc431532
%description
The pciutils package contains a set of programs for listing PCI devices, inspecting their status and setting their configuration registers.

%package devel
Summary: Development Libraries for openssl
Group: Development/Libraries
Requires: pciutils = %{version}-%{release}
%description devel
Library files for doing development with pciutils.

%prep
%setup -q
%build
make %{?_smp_mflags} PREFIX=%{_prefix} \
    SHAREDIR=%{_datadir}/misc \
    SHARED=yes

%install
[ %{buildroot} != "/"] && rm -rf %{buildroot}/*
make DESTDIR=%{buildroot} \
    PREFIX=%{_prefix} \
    SHAREDIR=%{_datadir}/misc \
    SHARED=yes \
    install install-lib
chmod -v 766 %{buildroot}%{_libdir}/libpci.so

%clean
rm -rf %{buildroot}/*

%files 
%defattr(-,root,root)
%{_sbindir}/*
%{_libdir}/*.so.*
%{_includedir}/*
%{_datadir}/misc/*
%{_mandir}/*

%files devel 
%defattr(-,root,root)
%{_libdir}/pkgconfig/*
%{_libdir}/*.so

%changelog
*	Wed Mar 29 2017 Robert Qi <qij@vmware.com> 3.5.4-1
-	Upgraded to 3.5.4-1 version.
*	Mon Jul 25 2016 Divya Thaluru <dthaluru@vmware.com> 3.3.1-3
-	Added devel package and removed packaging of debug files
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.3.1-2
-	GA - Bump release of all rpms
*	Thu Jul 2 2015 Sharath George <sharathg@vmware.com> 3.3.1-1
-	Initial build.	First version
