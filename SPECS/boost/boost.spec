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

%package        static
Summary:        boost static libraries
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description    static
The boost-static package contains boost static libraries.

%prep
%setup -qn boost_1_60_0

%build
./bootstrap.sh --prefix=%{buildroot}%{_prefix}
./b2 %{?_smp_mflags} stage threading=multi link=shared
./b2 %{?_smp_mflags} stage threading=multi link=static

%install
./b2 install threading=multi link=shared
./b2 install threading=multi link=static

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_libdir}/libboost_*.so.*
%{_libdir}/libboost_*.so

%files devel
%defattr(-,root,root)
%{_includedir}/boost/*

%files static
%defattr(-,root,root)
%{_libdir}/libboost_*.a

%changelog
*   Wed Mar 23 2017 Vinay Kulkarni <kulkarniv@vmware.com> 1.60.0-3
-   Build static libs in additon to shared.
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.60.0-2
-   GA - Bump release of all rpms
*   Wed Apr 27 2016 Xiaolin Li <xiaolinl@vmware.com> 1.60.0-1
-   Update to version 1.60.0.
*   Thu Oct 01 2015 Xiaolin Li <xiaolinl@vmware.com> 1.56.0-2
_   Move header files to devel package.
*   Tue Feb 10 2015 Divya Thaluru <dthaluru@vmware.com> 1.56.0-1
-   Initial build. First version
