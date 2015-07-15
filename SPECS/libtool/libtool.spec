Summary:	Shared libraries, portable interface
Name:		libtool
Version:	2.4.2
Release:	1%{?dist}
License:	GPLv2
URL:		http://www.gnu.org/software/libtool
Group:		Development/Tools
Vendor:		VMware, Inc.
Distribution: Photon
Source0:		http://ftp.gnu.org/gnu/libtool/%{name}-%{version}.tar.gz
%define sha1 libtool=22b71a8b5ce3ad86e1094e7285981cae10e6ff88
%description
It wraps the complexity of using shared libraries in a 
consistent, portable interface.
%package -n libltdl
Summary:       Shared library files for %{name}
Group:         Development/Libraries
%description -n libltdl
The libtool package contains the GNU libtool, a set of shell scripts which automatically configure UNIX and UNIX-like architectures to generically build shared libraries.
Libtool provides a consistent, portable interface which simplifies the process of using shared libraries.
Shared library files for libtool DLL library from the libtool package.
%package -n libltdl-devel
Summary:       Development files for %{name}
Group:         Development/Libraries
Requires:      libltdl = %{version}
%description -n libltdl-devel
The libtool package contains the GNU libtool, a set of shell scripts which automatically configure UNIX and UNIX-like architectures to generically build shared libraries.
Libtool provides a consistent, portable interface which simplifies the process of using shared libraries.
This package contains static libraries and header files need for development.
%prep
%setup -q
%build
./configure \
	--prefix=%{_prefix} \
	--disable-silent-rules
make %{?_smp_mflags}
%install
make DESTDIR=%{buildroot} install
find %{buildroot}%{_libdir} -name '*.la' -delete
rm -rf %{buildroot}%{_infodir}
%check
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}
%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig
%post -n libltdl
/sbin/ldconfig
%postun -n libltdl
/sbin/ldconfig
%files
%defattr(-,root,root)
%{_bindir}/libtoolize
%{_bindir}/libtool
%{_datadir}/aclocal/ltoptions.m4
%{_datadir}/aclocal/libtool.m4
%{_datadir}/aclocal/argz.m4
%{_datadir}/aclocal/ltversion.m4
%{_datadir}/aclocal/lt~obsolete.m4
%{_datadir}/aclocal/ltdl.m4
%{_datadir}/aclocal/ltsugar.m4
%{_mandir}/man1/libtool.1.gz
%{_mandir}/man1/libtoolize.1.gz
%{_datadir}/libtool/config/compile
%{_datadir}/libtool/config/config.sub
%{_datadir}/libtool/config/ltmain.sh
%{_datadir}/libtool/config/depcomp
%{_datadir}/libtool/config/missing
%{_datadir}/libtool/config/install-sh
%{_datadir}/libtool/config/config.guess
%files -n libltdl-devel
%{_includedir}/libltdl/lt_dlloader.h
%{_includedir}/libltdl/lt_system.h
%{_includedir}/libltdl/lt_error.h
%{_includedir}/ltdl.h
%{_libdir}/libltdl.a
%{_libdir}/libltdl.so
%files -n libltdl
%{_datadir}/libtool/libltdl/*
%{_libdir}/libltdl.so.7
%{_libdir}/libltdl.so.7.3.0

%changelog
*	Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 2.4.2-1
-	Initial build.	First version	
