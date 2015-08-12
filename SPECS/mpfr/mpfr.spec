Summary:	Functions for multiple precision math
Name:		mpfr
Version:	3.1.2
Release:	1%{?dist}
License:	GPLv3+
URL:		http://www.mpfr.org
Group:		Applications/System
Vendor:		VMware, Inc.
Distribution: Photon
Source0:		http://www.mpfr.org/%{name}-%{version}/%{name}-%{version}.tar.xz
%define sha1 mpfr=03e593cc6e26639ef5e60be1af8dc527209e5172
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
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}
%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig
%files
%defattr(-,root,root)
%{_libdir}/libmpfr.so.4.1.2
%{_libdir}/libmpfr.so.4
%{_docdir}/mpfr-3.1.2/NEWS
%{_docdir}/mpfr-3.1.2/FAQ.html
%{_docdir}/mpfr-3.1.2/examples/version.c
%{_docdir}/mpfr-3.1.2/examples/rndo-add.c
%{_docdir}/mpfr-3.1.2/examples/ReadMe
%{_docdir}/mpfr-3.1.2/examples/sample.c
%{_docdir}/mpfr-3.1.2/examples/divworst.c
%{_docdir}/mpfr-3.1.2/COPYING.LESSER
%{_docdir}/mpfr-3.1.2/TODO
%{_docdir}/mpfr-3.1.2/BUGS
%{_docdir}/mpfr-3.1.2/AUTHORS
%{_docdir}/mpfr-3.1.2/COPYING
%files devel
%{_includedir}/mpf2mpfr.h
%{_includedir}/mpfr.h
%{_libdir}/libmpfr.a
%{_libdir}/libmpfr.so
%changelog
*	Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com>> 3.1.2-1
-	Initial build.	First version
