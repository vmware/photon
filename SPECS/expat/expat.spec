Summary:	An XML parser library
Name:		expat
Version:	2.2.9
Release:	3%{?dist}
License:	MIT
URL:		http://expat.sourceforge.net/
Group:		System Environment/GeneralLibraries
Vendor:		VMware, Inc.
Distribution:	Photon
Source0:        https://sourceforge.net/projects/%{name}/files/%{name}/%{version}/%{name}-%{version}.tar.xz
%define sha1 expat=90a361e4c97f8c469479ffadc0de0b121a911fb5
Requires:       expat-libs = %{version}-%{release}
%description
The Expat package contains a stream oriented C library for parsing XML.

%package    devel
Summary:    Header and development files for expat
Requires:   %{name} = %{version}-%{release}
%description    devel
It contains the libraries and header files to create applications

%package libs
Summary: Libraries for expat
Group:      System Environment/Libraries
%description libs
This package contains minimal set of shared expat libraries.

%package docs
Summary: expat docs
Group: Documentation
Requires: expat = %{version}-%{release}
%description docs
The package contains expat doc files.

%prep
%setup -q
%build

%configure \
	CFLAGS="%{optflags}" \
	CXXFLAGS="%{optflags}" \
	--bindir=%{_bindir} \
	--libdir=%{_libdir} \
	--disable-static
make %{?_smp_mflags}

%install
[ %{buildroot} != "/"] && rm -rf %{buildroot}/*
make DESTDIR=%{buildroot} install
find %{buildroot}/%{_libdir} -name '*.la' -delete
rm -rf %{buildroot}/%{_docdir}/%{name}
%{_fixperms} %{buildroot}/*

%check
make %{?_smp_mflags} check

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%post libs
    # First argument is 1 => New Installation
    # First argument is 2 => Upgrade
    /sbin/ldconfig

%postun libs
    /sbin/ldconfig
    # First argument is 0 => Uninstall
    # First argument is 1 => Upgrade

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_bindir}/*

## TODO: There's some change in man page build path according to release notes.
## https://github.com/libexpat/libexpat/blob/R_2_2_7/expat/Changes
## #158 #263  CMake: Build man page in PROJECT_BINARY_DIR not _SOURCE_DIR
#%{_mandir}/man1/*

%files devel
%{_includedir}/*
%{_libdir}/pkgconfig/*
%{_libdir}/libexpat.so

%files libs
%{_libdir}/libexpat.so.*

%files docs
%defattr(-,root,root)
%doc AUTHORS Changes

%changelog
*   Fri Feb 19 2021 Satya Naga Vasamsetty <svasamsetty@vmware.com> 2.2.9-3
-   Move documents to docs sub-package
*   Mon Oct 05 2020 Tapas Kundu <tkundu@vmware.com> 2.2.9-2
-   Use ldconfig to resolve dependencies for lib
*   Tue Oct 29 2019 Tapas Kundu <tkundu@vmware.com> 2.2.9-1
-   Fix for CVE-2019-15903
*   Thu Oct 17 2019 Shreenidhi Shedi <sshedi@vmware.com> 2.2.7-1
-   Upgrade to version 2.2.7
*   Mon Jul 8 2019 Siddharth Chandrasekaran <csiddharth@vmware.com> 2.2.6-2
-   Add patch for CVE-2018-20843
*   Thu Sep 20 2018 Sujay G <gsujay@vmware.com> 2.2.6-1
-   Bump expat version to 2.2.6
*   Tue Sep 26 2017 Anish Swaminathan <anishs@vmware.com> 2.2.4-1
-   Updating version, fixes CVE-2017-9233,  CVE-2016-9063, CVE-2016-0718
*   Fri Apr 14 2017 Alexey Makhalov <amakhalov@vmware.com> 2.2.0-2
-   Added -libs and -devel subpackages
*   Fri Oct 21 2016 Kumar Kaushik <kaushikk@vmware.com> 2.2.0-1
-   Updating Source/Fixing CVE-2015-1283.
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.1.0-2
-   GA - Bump release of all rpms
*   Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 2.1.0-1
-   Initial build. First version
