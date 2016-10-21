Summary:	An XML parser library
Name:		expat
Version:	2.2.0
Release:	1%{?dist}
License:	MIT
URL:		http://expat.sourceforge.net/
Group:		System Environment/GeneralLibraries
Vendor:		VMware, Inc.
Distribution:	Photon
Source0:        https://sourceforge.net/projects/%{name}/files/%{name}/%{version}/%{name}-%{version}.tar.bz2
%define sha1 expat=8453bc52324be4c796fd38742ec48470eef358b3
%description
The Expat package contains a stream oriented C library for parsing XML.
%prep
%setup -q
%build
./configure \
	CFLAGS="%{optflags}" \
	CXXFLAGS="%{optflags}" \
	--prefix=%{_prefix} \
	--bindir=%{_bindir} \
	--libdir=%{_libdir} \
	--disable-static
make %{?_smp_mflags}
%install
[ %{buildroot} != "/"] && rm -rf %{buildroot}/*
make DESTDIR=%{buildroot} install
find %{buildroot}/%{_libdir} -name '*.la' -delete
%{_fixperms} %{buildroot}/*

%check
make %{?_smp_mflags} check

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig
%clean
rm -rf %{buildroot}/*
%files
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/*.so*
%{_libdir}/pkgconfig/*
%{_includedir}/*
%{_mandir}/man1/*
%changelog
*       Fri Oct 21 2016 Kumar Kaushik <kaushikk@vmware.com> 2.2.0-1
-       Updating Source/Fixing CVE-2015-1283.
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.1.0-2
-	GA - Bump release of all rpms
*	Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 2.1.0-1
-	Initial build.	First version
