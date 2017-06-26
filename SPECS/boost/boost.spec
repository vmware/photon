Summary:	Boost 
Name:		boost
Version:	1.60.0
Release:	3%{?dist}
License:	Boost Software License V1
URL:		http://www.boost.org/
Group:		System Environment/Security
Vendor:		VMware, Inc.
Distribution:	Photon
Source0:	http://downloads.sourceforge.net/boost/boost_1_60_0.tar.bz2
%define sha1 boost=7f56ab507d3258610391b47fef6b11635861175a
Patch0:         boost-1.60.0-uninitialized-warning.patch
BuildRequires:	bzip2-devel

%description
Boost provides a set of free peer-reviewed portable C++ source libraries. It includes libraries for 
linear algebra, pseudorandom number generation, multithreading, image processing, regular expressions and unit testing.

%package        devel
Summary:        Development files for boost
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description    devel
The boost-devel package contains libraries, header files and documentation
for developing applications that use boost.

%prep
%setup -qn boost_1_60_0
%patch0 -p1
%build
./bootstrap.sh --prefix=%{buildroot}%{_prefix}
./b2 %{?_smp_mflags} stage threading=multi link=shared
%install
./b2 install threading=multi link=shared
%check
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}
%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig
%clean
rm -rf %{buildroot}/*
%files
%defattr(-,root,root)
%{_libdir}/*.so.*
%{_libdir}/*.so

%files devel
%{_libdir}/*.a
%{_includedir}/*

%changelog
*	Mon Jun 26 2017 Anish Swaminathan <anishs@vmware.com> 1.60.0-3
-	Patch to silence may be used uninitialized warning in lexical_cast
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.60.0-2
-	GA - Bump release of all rpms
*	Wed Apr 27 2016 Xiaolin Li <xiaolinl@vmware.com> 1.60.0-1
-       Update to version 1.60.0.
*	Thu Oct 01 2015 Xiaolin Li <xiaolinl@vmware.com> 1.56.0-2
_	Move header files to devel package.
*	Tue Feb 10 2015 Divya Thaluru <dthaluru@vmware.com> 1.56.0-1
-	Initial build.	First version
