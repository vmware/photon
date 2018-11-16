Summary:	Library for the arithmetic of complex numbers
Name:		mpc
Version:	1.1.0
Release:	2%{?dist}
License:	LGPLv3+
URL:		http://www.multiprecision.org
Group:		Applications/System
Vendor:		VMware, Inc.
Distribution:   Photon
Source0:	http://www.multiprecision.org/mpc/download/%{name}-%{version}.tar.gz
Requires:	gmp
%define sha1 mpc=b019d9e1d27ec5fb99497159d43a3164995de2d0

%description
The MPC package contains a library for the arithmetic of complex
numbers with arbitrarily high precision and correct rounding of
the result.

%prep
%setup -q

%build
%configure --disable-silent-rules
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
%{_includedir}/*
%{_libdir}/*.a
%{_libdir}/*.so
%{_libdir}/*.so.*

%changelog
*   Tue Nov 06 2018 Alexey Makhalov <amakhalov@vmware.com> 1.1.0-2
-   Use %configure
*   Mon Sep 10 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 1.1.0-1
-   Update to version 1.1.0
*   Mon Oct 03 2016 ChangLee <changLee@vmware.com> 1.0.3-3
-   Modified check
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.0.3-2
-   GA - Bump release of all rpms
*   Tue Jan 12 2016 Anish Swaminathan <anishs@vmware.com>  1.0.3-1
-   Update version.
*   Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 1.0.2-1
-   Initial build. First version
