Summary:	GNU Unicode string library
Name:		libunistring
Version:	0.9.6
Release: 	2%{?dist}
License:	LGPLv3+
Url:		http://www.gnu.org/software/libunistring/
Source0:	http://ftp.gnu.org/gnu/libunistring/%{name}-%{version}.tar.xz
%define sha1 libunistring=d34dd5371c4b34863a880f2206e2d00532effdd6
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
%setup -q
%build
./configure \
	--prefix=%{_prefix}
make %{?_smp_mflags}
%install
make DESTDIR=%{buildroot} install
rm %{buildroot}%{_infodir}/*
%check
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}
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
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.9.6-2
-	GA - Bump release of all rpms
*   Mon Feb 22 2016 XIaolin Li <xiaolinl@vmware.com> 0.9.6-1
-   Updated to version 0.9.6
*	Thu Jun 18 2015 Divya Thaluru <dthaluru@vmware.com> 0.9.5-1
-	Initial build. First version

