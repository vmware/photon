Summary:	Functions for multiple precision math
Name:		mpfr
Version:	4.0.2
Release:	1%{?dist}
License:	GPLv3+
URL:		http://www.mpfr.org
Group:		Applications/System
Vendor:		VMware, Inc.
Distribution:   Photon
Source0:	http://www.mpfr.org/%{name}-%{version}/%{name}-%{version}.tar.gz
%define sha1 mpfr=ade94aa28e181540763d6698c6c9fae795be8b75
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
%configure \
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
*   Thu Dec 17 2020 Gerrit Photon <photon-checkins@vmware.com> 4.0.2-1
-   Automatic Version Bump
*   Wed Sep 04 2019 Alexey Makhalov <amakhalov@vmware.com> 4.0.1-2
-   Bump up release number to get generic mtune option from gmp.h
*   Thu Sep 20 2018 Him Kalyan Bordoloi <bordoloih@vmware.com> 4.0.1-1
-   Update package version
*   Fri Mar 31 2017 Michelle Wang <michellew@vmware.com> 3.1.5-1
-   Update package version
*   Mon Oct 03 2016 ChangLee <changlee@vmware.com> 3.1.3-3
-   Modified %check
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.1.3-2
-   GA - Bump release of all rpms
*   Tue Jan 12 2016 Anish Swaminathan <anishs@vmware.com>  3.1.3-1
-   Update version.
*   Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com>> 3.1.2-1
-   Initial build. First version
