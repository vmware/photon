Summary:	System utilities to list pci devices
Name:		pciutils
Version:	3.3.1
Release:	3%{?dist}
License:	GPLv2
URL:		https://www.kernel.org/pub/software/utils/pciutils/
Group:		System Environment/System Utilities
Vendor:		VMware, Inc.
Distribution: Photon
Source0:	https://www.kernel.org/pub/software/utils/pciutils/%{name}-%{version}.tar.gz
%define sha1 pciutils=cd93c519307addd542f6fdbcceaefc5a7d7f58bc
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
*	Mon Jul 25 2016 Divya Thaluru <dthaluru@vmware.com> 3.3.1-3
-	Added devel package and removed packaging of debug files
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.3.1-2
-	GA - Bump release of all rpms
*	Thu Jul 2 2015 Sharath George <sharathg@vmware.com> 3.3.1-1
-	Initial build.	First version
