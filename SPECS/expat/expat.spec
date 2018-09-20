Summary:	An XML parser library
Name:		expat
Version:	2.2.6
Release:	1%{?dist}
License:	MIT
URL:		http://expat.sourceforge.net/
Group:		System Environment/GeneralLibraries
Vendor:		VMware, Inc.
Distribution:	Photon
Source0:        https://sourceforge.net/projects/%{name}/files/%{name}/%{version}/%{name}-%{version}.tar.bz2
%define sha1 expat=c8947fc3119a797b55485f2f7bdaaeb49cc9df01
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
%clean
rm -rf %{buildroot}/*
%files
%defattr(-,root,root)
%doc AUTHORS Changes
%{_bindir}/*
%{_mandir}/man1/*

%files devel
%{_includedir}/*
%{_libdir}/pkgconfig/*
%{_libdir}/libexpat.so

%files libs
%{_libdir}/libexpat.so.*

%changelog
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
-   Initial build.	First version
