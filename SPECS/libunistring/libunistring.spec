Summary:	GNU Unicode string library
Name:		libunistring
Version:	1.0
Release: 	1%{?dist}
License:	LGPLv3+
Url:		http://www.gnu.org/software/libunistring/
Source0:	http://ftp.gnu.org/gnu/libunistring/%{name}-%{version}.tar.xz
%define sha512  libunistring=70d5ad82722844dbeacdfcb4d7593358e4a00a9222a98537add4b7f0bf4a2bb503dfb3cd627e52e2a5ca1d3da9e5daf38a6bd521197f92002e11e715fb1662d1
Group:		System Environment/Libraries
Vendor:		VMware, Inc.
Distribution:	Photon
%description
libunistring is a library that provides functions for manipulating Unicode strings and for manipulating C strings according to the Unicode standard.

%package devel
Summary:	Development libraries and header files for libunistring
Requires:	libunistring

%description devel
The package contains libraries and header files for
developing applications that use libunistring.

%prep
%autosetup

%build
%configure
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} %{?_smp_mflags} install
rm %{buildroot}%{_infodir}/*

%check
make %{?_smp_mflags} check

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_libdir}/*.so.*
%{_docdir}/%{name}/*
%{_libdir}/*.a
%{_libdir}/*.la

%files devel
%defattr(-,root,root)
%{_includedir}/*.h
%{_includedir}/unistring/*.h
%{_libdir}/*.so

%changelog
* Mon Apr 18 2022 Gerrit Photon <photon-checkins@vmware.com> 1.0-1
- Automatic Version Bump
* Mon Sep 10 2018 Alexey Makhalov <amakhalov@vmware.com> 0.9.10-1
- Version update to fix compilation issue againts glibc-2.28
* Thu Apr 06 2017 Kumar Kaushik <kaushikk@vmware.com> 0.9.7-1
- Updating Version to 0.9.7
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.9.6-2
- GA - Bump release of all rpms
* Mon Feb 22 2016 XIaolin Li <xiaolinl@vmware.com> 0.9.6-1
- Updated to version 0.9.6
* Thu Jun 18 2015 Divya Thaluru <dthaluru@vmware.com> 0.9.5-1
- Initial build. First version.
