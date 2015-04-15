Summary:	C++ xml parser.
Name:		xerces-c
Version:	3.1.1
Release:	1
License:	Apache License
URL:		http://www.apache.org/dist/xerces/c/3/sources/xerces-c-3.1.1.tar.gz
Group:		Applications/System
Vendor:		VMware, Inc.
Distribution:	Photon
Source0:	http://www.apache.org/dist/xerces/c/3/sources/%{name}-%{version}.tar.gz
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
*	Thu Nov 06 2014 Sharath George <sharathg@vmware.com> 3.1.1
	Initial version
