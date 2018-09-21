Summary:	Functions for multiple precision math
Name:		mpfr
Version:	4.0.1
Release:	1%{?dist}
License:	GPLv3+
URL:		http://www.mpfr.org
Group:		Applications/System
Vendor:		VMware, Inc.
Distribution:   Photon
Source0:	http://www.mpfr.org/%{name}-%{version}/%{name}-%{version}.tar.gz
%define sha1 mpfr=655e3cf416a0cc9530d9cb3c38dc8839504f0e98
Requires:	gmp
%description
The MPFR package contains functions for multiple precision math.
%package	devel
Summary:	Header and development files for mpfr
Requires:	%{name} = %{version}

%description	devel
It contains the libraries and header files to create applications 

%prep
%setup -q
%build
./configure \
	--prefix=%{_prefix} \
	--enable-thread-safe \
	--docdir=%{_defaultdocdir}/%{name}-%{version} \
	--disable-silent-rules
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install
find %{buildroot}%{_libdir} -name '*.la' -delete
rm -rf %{buildroot}%{_infodir}

%check
make %{?_smp_mflags} check

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig
%files
%defattr(-,root,root)
%{_libdir}/libmpfr.so.*

%files devel
%{_includedir}/mpf2mpfr.h
%{_includedir}/mpfr.h
%{_libdir}/libmpfr.a
%{_libdir}/libmpfr.so
%{_libdir}/pkgconfig/*
%{_docdir}/mpfr-%{version}/NEWS
%{_docdir}/mpfr-%{version}/FAQ.html
%{_docdir}/mpfr-%{version}/examples/version.c
%{_docdir}/mpfr-%{version}/examples/rndo-add.c
%{_docdir}/mpfr-%{version}/examples/ReadMe
%{_docdir}/mpfr-%{version}/examples/sample.c
%{_docdir}/mpfr-%{version}/examples/divworst.c
%{_docdir}/mpfr-%{version}/examples/can_round.c
%{_docdir}/mpfr-%{version}/COPYING.LESSER
%{_docdir}/mpfr-%{version}/TODO
%{_docdir}/mpfr-%{version}/BUGS
%{_docdir}/mpfr-%{version}/AUTHORS
%{_docdir}/mpfr-%{version}/COPYING

%changelog
*       Thu Sep 20 2018 Him Kalyan Bordoloi <bordoloih@vmware.com> 4.0.1-1
-       Update package version
*       Fri Mar 31 2017 Michelle Wang <michellew@vmware.com> 3.1.5-1
-       Update package version
*       Mon Oct 03 2016 ChangLee <changlee@vmware.com> 3.1.3-3
-       Modified %check
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.1.3-2
-	GA - Bump release of all rpms
*       Tue Jan 12 2016 Anish Swaminathan <anishs@vmware.com>  3.1.3-1
-       Update version.
*	Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com>> 3.1.2-1
-	Initial build.	First version
