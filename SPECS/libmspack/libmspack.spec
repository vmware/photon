Summary:	A library that provides compression and decompression of file formats used by Microsoft
Name:		libmspack
Version:	0.4alpha
Release:	2%{?dist}
License:	LGPLv2+
URL:		http://www.cabextract.org.uk/libmspack/libmspack-0.4alpha.tar.gz
Group:		Applications/System
Vendor:		VMware, Inc.
Distribution:	Photon
Source0:	http://www.cabextract.org.uk/libmspack/%{name}-%{version}.tar.gz
%define sha1 libmspack=b10249bde64ca387b211fd0bd125fc360377593c
%description
A library that provides compression and decompression of file formats used by Microsoft

%package        devel
Summary:        Development files for libmspack
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Obsoletes:      %{name}-doc < 0.2

%description    devel
The libmspack-devel package contains libraries, header files and documentation
for developing applications that use libmspack.

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
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root)
%{_libdir}/*.a
%{_libdir}/*.la
%{_libdir}/pkgconfig/*.pc
%{_includedir}/*
%{_libdir}/*.so

%changelog
*   Tue Oct 6 2015 Xiaolin Li <xiaolinl@vmware.com> 0.4-2
-   Move header files, and static lib files, and config files to devel package.
*	Thu Nov 06 2014 Sharath George <sharathg@vmware.com> 0.4-1
	Initial version
