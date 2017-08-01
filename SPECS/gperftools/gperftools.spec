Summary:	A fast malloc tool for threads
Name:		gperftools
Version:	2.5
Release:	2%{?dist}
License:	BSD
URL:		https://github.com/gperftools/gperftools
Source0:	https://github.com/gperftools/gperftools/releases/download/%{name}-%{version}/%{name}-%{version}.tar.gz
%define sha1 gperftools=1e7069f23f926df84a541938a8e6078b0aedf218
Group:		Development/Tools
Vendor:		VMware, Inc.
Distribution: 	Photon

%description
gperftools is a collection of a high-performance multi-threaded malloc() implementation, plus some pretty nifty performance analysis tools.

%package devel
Summary:        gperftools devel
Group:          Development/Tools
%description devel
This contains development tools and libraries for gperftools.

%package docs
Summary:        gperftools docs
Group:          Development/Tools
%description docs
The contains gperftools package doc files.

%prep
%setup -q

%build
./configure \
	--prefix=%{_prefix} \
	--docdir=%{_defaultdocdir}/%{name}-%{version}
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install
find %{buildroot} -name '*.la' -delete

%check
TCMALLOC_SAMPLE_PARAMETER=128 && make check

%files
%defattr(-,root,root)
%{_bindir}/pprof
%{_libdir}/libprofiler*.so.*
%{_libdir}/libtcmalloc*.so.*

%files devel
%{_includedir}/google/*
%{_includedir}/gperftools/*
%{_libdir}/libprofiler*.a
%{_libdir}/libprofiler*.so
%{_libdir}/libtcmalloc*.a
%{_libdir}/libtcmalloc*.so
%{_libdir}/pkgconfig/lib*

%files docs
%{_docdir}/%{name}-%{version}/*
%{_mandir}/man1/*

%changelog
*    Mon Jul 31 2017 Vinay Chang Lee <changlee@vmware.com> 2.5-2
-    Fix %check
*    Mon Feb 06 2017 Vinay Kulkarni <kulkarniv@vmware.com> 2.5-1
-    Initial version of gperftools package.
