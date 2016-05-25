Summary:	C++ xml parser.
Name:		xerces-c
Version:	3.1.3
Release:	2%{?dist}
License:	Apache License
URL:		http://xerces.apache.org
Group:		Applications/System
Vendor:		VMware, Inc.
Distribution:	Photon
Source0:	http://mirrors.advancedhosters.com/apache//xerces/c/3/sources/%{name}-%{version}.tar.xz
%define sha1 xerces-c=44aa39f8b9ccbfcaf58771634761cbea1084e8f1
%description
Xerces-C++ is a validating XML parser written in a portable subset of C++
%package	devel
Summary:	XML library headers
Group:         	Development/Libraries
Requires:       %{name} = %{version}-%{release}
%description	devel
This package contains development headers and static library for xml parser.
%prep
%setup -q
%build
./configure --prefix=/usr
make %{?_smp_mflags}
%install
make DESTDIR=%{buildroot} install
%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig
%files 
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/*.so

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/pkgconfig/*.pc
%{_libdir}/*.a
%{_libdir}/*.la

%changelog
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 	3.1.3-2
-	GA - Bump release of all rpms
*   Tue Feb 23 2016 Xiaolin Li <xiaolinl@vmware.com> 3.1.3-1
-   Updated to version 3.1.3
*	Thu Aug 13 2015 Divya Thaluru <dthaluru@vmware.com> 3.1.2-1
-	Updating Package to 3.1.2
*	Thu Nov 06 2014 Sharath George <sharathg@vmware.com> 3.1.1
	Initial version
