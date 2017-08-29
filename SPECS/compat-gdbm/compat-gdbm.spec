Summary:	The GNU Database routines compatibility library
Name:		compat-gdbm
Version:	1.8.3
Release:	3%{?dist}
License:	GPLv2+
URL:		http://www.gnu.org/software/gdbm
Group:		System Environment/Libraries
Vendor:		VMware, Inc.
Distribution:	Photon
Source0:	http://ftp.gnu.org/gnu/gdbm/%{name}-%{version}.tar.gz
%define sha1 compat-gdbm=695d8dc0d94cfb3c60165d32ea9b9faccf57e45e

BuildRequires: libtool
%description
The compat-gdbm package contains an older version of gdbm for compatibility purposes.

%package devel
Summary: Development libraries and header files for the gdbm library
Group: Development/Libraries
Conflicts: gdbm-devel
Requires: %{name} = %{version}-%{release}

%description devel
compat-gdbm-devel contains the development libraries and header files for compat-gdbm, the GNU database system. Useful for developing programs using older version of gdbm.

%prep
%setup -q

libtoolize --force --copy
aclocal
autoconf

%build
sed -i 's/$(LIBTOOL) $(INSTALL) -c libgdbm.la $(INSTALL_ROOT)$(libdir)\/libgdbm.la/$(LIBTOOL) $(INSTALL) -c libgdbm.la -o $(INSTALL_ROOT)$(libdir)\/libgdbm.la/g' Makefile.in
sed -i 's/$(INSTALL_ROOT)$(libdir)\/libgdbm_compat.la/ -o $(INSTALL_ROOT)$(libdir)\/libgdbm_compat.la/g' Makefile.in 
%configure --disable-static
make %{?_smp_mflags} LIBTOOL='/usr/bin/libtool --tag=CC'

%install
%makeinstall install-compat LIBTOOL='/usr/bin/libtool --mode=link --tag=CC' INSTALL=/bin/install
cp .libs/libgdbm.so.3* %{buildroot}%{_libdir}
cp .libs/libgdbm_compat.so.3* %{buildroot}%{_libdir}
ln -sf libgdbm.so.3.0.0 %{buildroot}%{_libdir}/libgdbm.so
ln -sf libgdbm_compat.so.3.0.0 %{buildroot}%{_libdir}/libgdbm_compat.so
ln -sf libgdbm.so.3.0.0 %{buildroot}%{_libdir}/libgdbm.so.3
ln -sf libgdbm_compat.so.3.0.0 %{buildroot}%{_libdir}/libgdbm_compat.so.3
find %{buildroot}%{_libdir} -name '*.la' -delete
find %{buildroot}%{_libdir} -name '*.a' -delete
rm -rf %{buildroot}%{_mandir}/man3/*
rm -rf %{buildroot}%{_infodir}

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%doc COPYING NEWS README
%{_libdir}/libgdbm.so.3*
%{_libdir}/libgdbm_compat.so.3*

%files devel
%{_libdir}/libgdbm.so
%{_libdir}/libgdbm_compat.so
%{_includedir}/*.h

%changelog
*	Tue Aug 22 2017 Dheeraj Shetty <dheerajs@vmware.com> 1.8.3-3
-	gdbm-devel conflicts with compat-gdbm-devel
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.8.3-2
-	GA - Bump release of all rpms
*	Fri Nov 13 2015 Anish Swaminathan <anishs@vmware.com> 1.8.3-1
-	Initial build.	First version
