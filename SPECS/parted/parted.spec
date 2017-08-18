Summary:	GNU Parted manipulates partition tables
Name:		parted
Version:	3.2
Release:	5%{?dist}
License:	GPLv3+
URL:		http://ftp.gnu.org/gnu/parted/parted-3.2.tar.xz
Group:		Applications/System
Vendor:		VMware, Inc.
Distribution:	Photon
Source0:	http://ftp.gnu.org/gnu/parted/%{name}-%{version}.tar.xz
%define sha1 parted=8cabb2d6789badec15c857dcc003d0dd931a818b
%description
This is useful for creating space for new operating systems,
reorganizing disk usage, copying data on hard disks and disk imaging.
The package contains a library, libparted, as well as well as a
command-line frontend, parted, which can also be used in scripts.
%prep
%setup -q
%build
./configure \
	--prefix=%{_prefix} \
	--bindir=%{_bindir} \
	--infodir=%{_infodir}/%{name}-%{version} \
	--without-readline \
	--disable-debug \
	--disable-nls \
	--disable-device-mapper
make %{?_smp_mflags}
%install
make DESTDIR=%{buildroot} install

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig
%files 
%defattr(-,root,root)
%{_sbindir}/*
%{_libdir}/*.a
%{_libdir}/*.la
%{_libdir}/*.so
%{_libdir}/*.so.*
%{_libdir}/pkgconfig/*.pc
%{_includedir}/*
%{_infodir}/%{name}-%{version}/*
%{_datadir}/*
%changelog
*       Wed Aug 16 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.2-5
-       Fix summary and description
*       Tue Jun 06 2017 ChangLee <changlee@vmware.com> 3.2-4
-       Remove %check
*       Fri Oct 07 2016 ChangLee <changlee@vmware.com> 3.2-3
-       Modified %check
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.2-2
-	GA - Bump release of all rpms
*	Thu Nov 12 2014 Mahmoud Bassiouny <mbassiouny@vmware.com> 3.2-1
	Initial version
