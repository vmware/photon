Summary:	ASN.1 library
Name:		libtasn1
Version:	4.5
Release:	3%{?dist}
License:	GPLv3+ and LGPLv2+
URL:		http://www.gnu.org/software/libtasn1/
Source0:	http://ftp.gnu.org/gnu/libtasn1/%{name}-%{version}.tar.gz
%define sha1 libtasn1=7d648928729ffd38de84fac8b94d3ae0558de472
Group:		System Environment/Libraries
Vendor:		VMware, Inc.
Distribution:	Photon
%description
Libtasn1 library provides Abstract Syntax Notation One (ASN.1, as specified by the X.680 ITU-T recommendation) parsing and structures management, 
and Distinguished Encoding Rules (DER, as per X.690) encoding and decoding functions.

%package devel
Summary:	Development libraries and header files for libtasn1
Requires:	libtasn1
Provides:	pkgconfig(libtasn1)

%description devel
The package contains libraries and header files for
developing applications that use libtasn1.

%prep
%setup -q
%build
./configure \
	--prefix=%{_prefix}
make %{?_smp_mflags}
%install
make DESTDIR=%{buildroot} install
rm %{buildroot}%{_infodir}/*
find %{buildroot}%{_libdir} -name '*.la' -delete
%check
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}
%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig
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
*   Mon Oct 12 2015 Xiaolin Li <xiaolinl@vmware.com> 4.5-3
-   Moving static lib files to devel package.
*   Fri Oct 9 2015 Xiaolin Li <xiaolinl@vmware.com> 4.5-2
-   Removing la files from packages.
*	Fri Jun 19 2015 Divya Thaluru <dthaluru@vmware.com> 4.5-1
-	Initial build. First version

