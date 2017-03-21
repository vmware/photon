Summary:	Boost 
Name:		boost
Version:	1.54.0
Release:	1%{?dist}
License:	Boost Software License V1
URL:		http://www.boost.org/
Group:		System Environment/Security
Vendor:		VMware, Inc.
Distribution:	Photon
Source0:	boost_1_54_0.tar.gz
Patch0:         boost-stdint.patch
%define sha1 boost=069501636097d3f40ddfd996d29748bb23591c53
BuildRequires:	gzip
BuildRequires:	gcc
BuildRequires:  glib
BuildRequires:  glib-devel
BuildRequires:  glibc
BuildRequires:  glibc-devel
BuildRequires:  libstdc++-devel

BuildRequires:  m4
BuildRequires:  cmake
BuildRequires:  automake
BuildRequires:  autoconf
BuildRequires:  bzip2
BuildRequires:  bzip2-devel
BuildRequires:  zlib-devel
BuildRequires:  python2-devel


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
%setup -qn boost_1_54_0
%patch0 -p1

%build

cat >> ./tools/build/v2/user-config.jam << EOF
using gcc : : : <compileflags>-fno-strict-aliasing ;
EOF

./bootstrap.sh                         \
        --prefix=%{_prefix}            \
        --includedir=%{_includedir}    \
        --libdir=%{_libdir}

./b2 %{?_smp_mflags} cxxflags=-std=gnu++11 stage threading=multi link=shared
./b2 %{?_smp_mflags} cxxflags=-std=gnu++11 stage threading=multi link=static

%install
./b2 --prefix=%{buildroot} install threading=multi link=shared

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig
%clean
rm -rf %{buildroot}/*
%files
%defattr(-,root,root)
/lib/libboost_*.so.*

%files devel
/lib/libboost_*.a
/lib/libboost_*.so
/include/boost/*

%changelog
*	Mon Mar 20 2017 Vinay Kulkarni <kulkarniv@vmware.com> 1.54.0-1
-	Initial build.	First version
