Summary:	Shared libraries, portable interface
Name:		libtool
Version:	2.4.6
Release:	2%{?dist}
License:	GPLv2
URL:		http://www.gnu.org/software/libtool
Group:		Development/Tools
Vendor:		VMware, Inc.
Distribution: Photon
Source0:		http://ftp.gnu.org/gnu/libtool/%{name}-%{version}.tar.xz
%define sha1 libtool=3e7504b832eb2dd23170c91b6af72e15b56eb94e
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
make %{?_smp_mflags} check

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
%{_datadir}/aclocal/ltversion.m4
%{_datadir}/aclocal/lt~obsolete.m4
%{_datadir}/aclocal/ltdl.m4
%{_datadir}/aclocal/ltsugar.m4
%{_datadir}/aclocal/ltargz.m4
%{_mandir}/man1/libtool.1.gz
%{_mandir}/man1/libtoolize.1.gz
%{_datadir}/libtool/*

%files -n libltdl-devel
%{_includedir}/libltdl/lt_dlloader.h
%{_includedir}/libltdl/lt_system.h
%{_includedir}/libltdl/lt_error.h
%{_includedir}/ltdl.h
%{_libdir}/libltdl.a
%{_libdir}/libltdl.so
%files -n libltdl
%{_libdir}/libltdl.so.7
%{_libdir}/libltdl.so.7.3.1

%changelog
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.4.6-2
-	GA - Bump release of all rpms
*	Wed Jan 13 2016 Xiaolin Li <xiaolinl@vmware.com> 2.4.6-1
-   Updated to version 2.4.6
*	Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 2.4.2-1
-	Initial build.	First version	
