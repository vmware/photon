Summary:	Boost 
Name:		boost
Version:	1.60.0
Release:	1%{?dist}
License:	Boost Software License V1
URL:		http://www.boost.org/
Group:		System Environment/Security
Vendor:		VMware, Inc.
Distribution:	Photon
Source0:	http://downloads.sourceforge.net/boost/boost_1_60_0.tar.bz2
%define sha1 boost=7f56ab507d3258610391b47fef6b11635861175a
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
%build
./bootstrap.sh --prefix=%{buildroot}%{_prefix}
./b2 %{?_smp_mflags} stage threading=multi link=shared
%install
./b2 install threading=multi link=shared

%check
echo '*** boost check is probably not supported by source, the test-suite will NOT run ***'

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
*	Thu Oct 01 2015 Xiaolin Li <xiaolinl@vmware.com> 1.56.0-2
_	Move header files to devel package.
*	Tue Feb 10 2015 Divya Thaluru <dthaluru@vmware.com> 1.56.0-1
-	Initial build.	First version
