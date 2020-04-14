Summary:        ASN.1 library
Name:           libtasn1
Version:        4.14
Release:        1%{?dist}
License:        GPLv3+ and LGPLv2+
URL:            http://www.gnu.org/software/libtasn1/
Source0:        http://ftp.gnu.org/gnu/libtasn1/%{name}-%{version}.tar.gz
%define sha1    libtasn1=4ce6a70a40f50a2c29a62bbf1c0c5b6e306ca4e3
Group:          System Environment/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon

%description
Libtasn1 library provides Abstract Syntax Notation One (ASN.1, as specified by
the X.680 ITU-T recommendation) parsing and structures management, and
Distinguished Encoding Rules (DER, as per X.690) encoding and decoding
functions.

%package devel
Summary:    Development libraries and header files for libtasn1
Requires:   libtasn1
Provides:   pkgconfig(libtasn1)

%description devel
The package contains libraries and header files for
developing applications that use libtasn1.

%prep
%setup -q

%build
%configure
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install
rm %{buildroot}%{_infodir}/*
find %{buildroot}%{_libdir} -name '*.la' -delete
%check
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}
%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig
%files
%defattr(-,root,root)
%{_libdir}/*.so.*
%{_bindir}/*
%{_mandir}/man1/*
%{_mandir}/man3/*
%files devel
%defattr(-,root,root)
%{_includedir}/*.h
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_libdir}/*.a
%changelog
*   Mon Apr 13 2020 Siddharth Chandrasekran <csiddhath@vmware.com> 4.14-1
-   Update to version 4.14 to fix CVE-2018-1000654
*   Mon Feb 12 2018 Xiaolin Li <xiaolinl@vmware.com> 4.13-1
-   Update to version 4.13 fix CVE-2018-6003.
*   Tue Oct 17 2017 Xiaolin Li <xiaolinl@vmware.com> 4.12-1
-   Update to 4.12 and apply patch for CVE-2017-10790
*   Wed Nov 30 2016 Dheeraj Shetty <dheerajs@vmware.com> 4.7-3
-   Added patch for CVE-2016-4008
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 4.7-2
-   GA - Bump release of all rpms
*   Fri Jan 15 2016 Xiaolin Li <xiaolinl@vmware.com> 4.7-1
-   Updated to version 4.7
*   Mon Oct 12 2015 Xiaolin Li <xiaolinl@vmware.com> 4.5-3
-   Moving static lib files to devel package.
*   Fri Oct 9 2015 Xiaolin Li <xiaolinl@vmware.com> 4.5-2
-   Removing la files from packages.
*   Fri Jun 19 2015 Divya Thaluru <dthaluru@vmware.com> 4.5-1
-   Initial build. First version

