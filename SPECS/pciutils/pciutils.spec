Summary:	System utilities to list pci devices
Name:		pciutils
Version:	3.6.4
Release:	2%{?dist}
License:	GPLv2
URL:		https://www.kernel.org/pub/software/utils/pciutils/
Group:		System Environment/System Utilities
Vendor:		VMware, Inc.
Distribution: Photon
Source0:	https://www.kernel.org/pub/software/utils/pciutils/%{name}-%{version}.tar.gz
%define sha1 pciutils=c99196cf232ecf539a9a63c7da3f9f3500a4955d
%description
The pciutils package contains a set of programs for listing PCI devices, inspecting their status and setting their configuration registers.

%package devel
Summary: Development Libraries for openssl
Group: Development/Libraries
Requires: pciutils = %{version}-%{release}
%description devel
Library files for doing development with pciutils.

%prep
%autosetup

%build
make %{?_smp_mflags} PREFIX=%{_prefix} \
    SHAREDIR=%{_datadir}/misc \
    SHARED=yes

%install
[ %{buildroot} != "/" ] && rm -rf %{buildroot}/*
make DESTDIR=%{buildroot} \
    PREFIX=%{_prefix} \
    SHAREDIR=%{_datadir}/misc \
    SHARED=yes \
    install install-lib
chmod -v 766 %{buildroot}%{_libdir}/libpci.so

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_sbindir}/*
%{_libdir}/*.so.*
%{_datadir}/misc/*
%{_mandir}/*

%files devel
%defattr(-,root,root)
%{_libdir}/pkgconfig/*
%{_libdir}/*.so
%{_includedir}/*

%changelog
*   Thu Nov 11 2021 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 3.6.4-2
-   Add missing ldconfig after library installation.
*   Thu Dec 17 2020 Gerrit Photon <photon-checkins@vmware.com> 3.6.4-1
-   Automatic Version Bump
*   Tue Sep 11 2018 Him Kalyan Bordoloi <bordoloih@vmware.com> 3.6.2-1
-   Upgraded to 3.6.2 version
*   Wed Mar 29 2017 Robert Qi <qij@vmware.com> 3.5.4-1
-   Upgraded to 3.5.4 version.
*   Mon Jul 25 2016 Divya Thaluru <dthaluru@vmware.com> 3.3.1-3
-   Added devel package and removed packaging of debug files
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.3.1-2
-   GA - Bump release of all rpms
*   Thu Jul 2 2015 Sharath George <sharathg@vmware.com> 3.3.1-1
-   Initial build.	First version
