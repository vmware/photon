Summary:	C++ xml parser.
Name:		xerces-c
Version:	3.1.4
Release:	2%{?dist}
License:	Apache License
URL:		http://xerces.apache.org
Group:		Applications/System
Vendor:		VMware, Inc.
Distribution:	Photon
Source0:	http://mirrors.advancedhosters.com/apache//xerces/c/3/sources/%{name}-%{version}.tar.xz
%define sha1 xerces-c=df52c67ad958460d4357b9305b49fda6876f6975
Requires:	libstdc++
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

%check
make %{?_smp_mflags} check

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
*	Mon Jun 05 2017 Bo Gan <ganb@vmware.com> 3.1.4-2
-	Fix dependency
*	Wed Mar 15 2017 Dheeraj Shetty <dheerajs@vmware.com> 3.1.4-1
-	Upgrade to latest version to handle CVE-2016-2099
*       Wed Oct 05 2016 ChangLee <changlee@vmware.com> 3.1.3-3
-       Modified %check
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.1.3-2
-	GA - Bump release of all rpms
*       Tue Feb 23 2016 Xiaolin Li <xiaolinl@vmware.com> 3.1.3-1
-       Updated to version 3.1.3
*	Thu Aug 13 2015 Divya Thaluru <dthaluru@vmware.com> 3.1.2-1
-	Updating Package to 3.1.2
*	Thu Nov 06 2014 Sharath George <sharathg@vmware.com> 3.1.1
	Initial version
