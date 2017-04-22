Summary:	C++ port of Junit test framework
Name:		cppunit
Version:	1.12.1
Release:	1%{?dist}
License:	LGPLv2
URL:		https://sourceforge.net/projects/cppunit/
Source0:	https://sourceforge.net/projects/cppunit/files/%{name}/%{version}/%{name}-%{version}.tar.gz
%define sha1 cppunit=f1ab8986af7a1ffa6760f4bacf5622924639bf4a
Group:		Development/Tools
Vendor:		VMware, Inc.
Distribution: 	Photon
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  make
BuildRequires:  gcc
BuildRequires:  libgcc
BuildRequires:  libtool
Requires:       linux
Requires:       make

%description
CppUnit is the C++ port of the famous JUnit framework for unit testing. Test
output is in XML or text format for automatic testing and GUI based for
supervised tests

%prep
%setup -n %{name}-%{version}

%build
./configure \
    --disable-silent-rules \
    --prefix=%{_prefix} \
    --includedir=%{_includedir} \
    --libdir=%{_libdir} \
    --mandir=%{_mandir} \
    --docdir=%{_docdir}
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install
find %{buildroot} -name '*.la' -delete

%files
%defattr(-,root,root)
%{_bindir}/*
%{_includedir}/%{name}/*
%{_libdir}/*
/usr/share/*

%changelog
*    Sun Mar 26 2017 Vinay Kulkarni <kulkarniv@vmware.com> 1.12.1-1
-    Initial version of cppunit for Photon.
