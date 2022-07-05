Summary:        GNU Parted manipulates partition tables
Name:           parted
Version:        3.5
Release:        1%{?dist}
License:        GPLv3+
URL:            http://ftp.gnu.org/gnu/parted/parted-%{version}.tar.xz
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        http://ftp.gnu.org/gnu/parted/%{name}-%{version}.tar.xz
%define sha512  parted=87fc69e947de5f0b670ee5373a7cdf86180cd782f6d7280f970f217f73f55ee1b1b018563f48954f3a54fdde5974b33e07eee68c9ccdf08e621d3dc0e3ce126a
Patch0:         parted-freelocale.patch
Conflicts:      toybox < 0.8.2-2

%description
This is useful for creating space for new operating systems,
reorganizing disk usage, copying data on hard disks and disk imaging.
The package contains a library, libparted, as well as well as a
command-line frontend, parted, which can also be used in scripts.

%prep
%autosetup -p1

%build
#Add a header to allow building with glibc-2.28 or later
sed -i '/utsname.h/a#include <sys/sysmacros.h>' libparted/arch/linux.c &&

%configure --without-readline --disable-debug \
	   --disable-nls --disable-device-mapper
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} %{?_smp_mflags} install

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
%{_infodir}/*
%{_datadir}/*
%exclude %{_infodir}/dir

%changelog
*  Mon Apr 18 2022 Gerrit Photon <photon-checkins@vmware.com> 3.5-1
-  Automatic Version Bump
*  Tue Apr 13 2021 Gerrit Photon <photon-checkins@vmware.com> 3.4-1
-  Automatic Version Bump
*  Fri Jan 22 2021 Dweep Advani <dadvani@vmware.com> 3.3-2
-  Remove conflict causing /usr/share/info/dir from packaging
*  Thu Jul 09 2020 Gerrit Photon <photon-checkins@vmware.com> 3.3-1
-  Automatic Version Bump
*  Thu Apr 16 2020 Alexey Makhalov <amakhalov@vmware.com> 3.2-8
-  Do not conflict with toybox >= 0.8.2-2
*  Tue Oct 2 2018 Michelle Wang <michellew@vmware.com> 3.2-7
-  Add conflict toybox.
*  Sun Sep 09 2018 Alexey Makhalov <amakhalov@vmware.com> 3.2-6
-  Fix compilation issue against glibc-2.28.
*  Wed Aug 16 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.2-5
-  Fix summary and description.
*  Tue Jun 06 2017 ChangLee <changlee@vmware.com> 3.2-4
-  Remove %check.
*  Fri Oct 07 2016 ChangLee <changlee@vmware.com> 3.2-3
-  Modified %check.
*  Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.2-2
-  GA Bump release of all rpms.
*  Wed Nov 12 2014 Mahmoud Bassiouny <mbassiouny@vmware.com> 3.2-1
-  Initial version.
