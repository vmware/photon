Summary:    C++ port of Junit test framework
Name:       cppunit
Version:    1.12.1
Release:    3%{?dist}
URL:        https://sourceforge.net/projects/cppunit
Group:      Development/Tools
Vendor:     VMware, Inc.
Distribution:   Photon

Source0:    https://sourceforge.net/projects/cppunit/files/%{name}/%{version}/%{name}-%{version}.tar.gz
%define sha512 cppunit=7af3569d028d5fa49106ece281f478cc2757cc5deca8c2512406796a7dbd6473928a1e730f28880467d19c6e59b31e55bf4f92f5cf2498a3a875ab32c5b2a081

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  make
BuildRequires:  gcc
BuildRequires:  libgcc
BuildRequires:  libtool

%description
CppUnit is the C++ port of the famous JUnit framework for unit testing. Test
output is in XML or text format for automatic testing and GUI based for
supervised tests

%package devel
Summary:        cppunit devel
Group:          Development/Tools
%description devel
This contains headers and libs for development with cppunit.

%prep
%autosetup -p1 -n %{name}-%{version}

%build
%configure \
    --disable-silent-rules

%make_build

%install
%make_install %{?_smp_mflags}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/libcppunit-*so.*

%files devel
%defattr(-,root,root)
%{_includedir}/%{name}/*
%{_libdir}/libcppunit.a
%{_libdir}/libcppunit.so
%{_libdir}/pkgconfig*
%{_datadir}/*

%changelog
* Thu Dec 12 2024 HarinadhD <harinadh.dommaraju@broadcom.com> 1.12.1-3
- Release bump for SRP compliance
* Fri Oct 13 2017 Alexey Makhalov <amakhalov@vmware.com> 1.12.1-2
- Use standard configure macros
* Sun Mar 26 2017 Vinay Kulkarni <kulkarniv@vmware.com> 1.12.1-1
- Initial version of cppunit for Photon.
