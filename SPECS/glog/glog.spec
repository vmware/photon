Summary:	Google's C++ logging module
Name:		glog
Version:	0.3.4
Release:	1%{?dist}
License:	BSD
URL:		https://github.com/google/glog
Source0:	https://github.com/google/glog/archive/%{name}-v%{version}.tar.gz
%define sha1 glog=69f91cd5a1de35ead0bc4103ea87294b0206a456
Group:		Development/Tools
Vendor:		VMware, Inc.
Distribution: 	Photon
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  make
BuildRequires:  gcc
BuildRequires:  libgcc
BuildRequires:  libtool

%description
Google's C++ logging module

%package devel
Summary:        glog devel
Group:          Development/Tools
%description devel
This contains development tools and libraries for glog.

%package docs
Summary:        glog docs
Group:          Development/Tools
%description docs
The contains glog package doc files.

%prep
%setup -n %{name}-%{version}

%build
./configure \
    --disable-silent-rules \
    --includedir=%{_includedir} \
    --libdir=%{_libdir} \
    --mandir=%{_mandir} \
    --docdir=%{_docdir}
make

%install
make DESTDIR=%{buildroot} install
find %{buildroot} -name '*.la' -delete

%files
%defattr(-,root,root)
%{_libdir}/libglog.so.*

%files devel
%defattr(-,root,root)
%{_includedir}/%{name}/*
%{_libdir}/libglog.a
%{_libdir}/libglog.so
%{_libdir}/pkgconfig/libglog.pc

%files docs
%defattr(-,root,root)
/usr/local/share/doc/%{name}-%{version}/*

%changelog
*    Sat Mar 25 2017 Vinay Kulkarni <kulkarniv@vmware.com> 0.3.4-1
-    Initial version of glog for Photon.
