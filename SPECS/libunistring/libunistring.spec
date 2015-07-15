Summary:	GNU Unicode string library
Name:		libunistring
Version:	0.9.5
Release: 	1%{?dist}
License:	LGPLv3+
Url:		http://www.gnu.org/software/libunistring/
Source0:	http://ftp.gnu.org/gnu/libunistring/%{name}-%{version}.tar.xz
%define sha1 libunistring=ccb81e629380385d682b71c8e96eba4a7ef43af7
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
*	Thu Jun 18 2015 Divya Thaluru <dthaluru@vmware.com> 0.9.5-1
-	Initial build. First version

