Summary:	GNU Ubiquitous Intelligent Language for Extensions
Name:		guile
Version:	2.0.11
Release:	1%{?dist}
License: 	LGPLv3+
URL:		http://www.gnu.org/software/guile/
Source0: 	ftp://ftp.gnu.org/pub/gnu/guile/%{name}-%{version}.tar.gz
Group: 		Development/Languages
Vendor:		VMware, Inc.
Distribution:	Photon
BuildRequires:	libltdl-devel
BuildRequires:	libunistring-devel
BuildRequires:	gc-devel
BuildRequires:	libffi
Requires:	libltdl
Requires:	libunistring
Requires:	gc
Requires:	libffi

%description
GUILE (GNU's Ubiquitous Intelligent Language for Extension) is a library
implementation of the Scheme programming language, written in C.  GUILE
provides a machine-independent execution platform that can be linked in
as a library during the building of extensible programs.
%package devel
Summary:	Development libraries and header files for guile
Requires:	guile
Requires:	libltdl-devel
Requires:	libunistring-devel

%description devel
The package contains libraries and header files for
developing applications that use guile.

%prep
%setup -q
%build
./configure \
	--prefix=%{_prefix} \
	--disable-static
make %{?_smp_mflags}
%install
make DESTDIR=%{buildroot} install
rm %{buildroot}%{_libdir}/*.scm
rm %{buildroot}%{_infodir}/*
%check
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}
%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig
%files
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/*.so.*
%{_libdir}/guile/*
%{_mandir}/man1/*
%{_datadir}/aclocal/*.m4
%{_datadir}/guile/*
%{_libdir}/*.la
%files devel
%defattr(-,root,root)
%{_includedir}/guile/2.0/*.h
%{_includedir}/guile/2.0/libguile/*.h
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%changelog
*	Thu Jun 18 2015 Divya Thaluru <dthaluru@vmware.com> 2.0.11-1
-	Initial build. First version

