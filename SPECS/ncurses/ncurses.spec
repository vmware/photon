Summary:	Libraries for terminal handling of character screens
Name:		ncurses
Version:	6.0
Release:	6%{?dist}
License:	MIT
URL:		http://www.gnu.org/software/ncurses
Group:		Applications/System
Vendor:		VMware, Inc.
Distribution: 	Photon
Source0:	ftp://ftp.gnu.org/gnu/ncurses/%{name}-%{version}.tar.gz
%define sha1 ncurses=acd606135a5124905da770803c05f1f20dd3b21c
Patch0:		CVE-2017-10684-CVE-2017-10685.patch
Provides:       libncurses.so.6()(64bit)
%description
The Ncurses package contains libraries for terminal-independent
handling of character screens.

%package compat
Summary: Ncurses compatibility libraries
Group: System Environment/Libraries
Provides: libncurses.so.5()(64bit)

%description compat
This package contains the ABI version 5 of the ncurses libraries for
compatibility.

%package	devel
Summary:	Header and development files for ncurses
Requires:	%{name} = %{version}
Provides:	pkgconfig(ncurses)
%description	devel
It contains the libraries and header files to create applications 
%prep
%setup -q
%patch0 -p1
%build
mkdir v6
pushd v6
ln -s ../configure .
./configure \
	--prefix=%{_prefix} \
	--mandir=%{_mandir} \
	--with-shared \
	--without-debug \
	--enable-pc-files \
	--enable-widec \
	--disable-lp64 \
	--with-chtype='long' \
	--with-mmask-t='long' \
	--disable-silent-rules
make %{?_smp_mflags}
popd
mkdir v5
pushd v5
ln -s ../configure .
./configure \
	--prefix=%{_prefix} \
	--mandir=%{_mandir} \
	--with-shared \
	--without-debug \
	--enable-pc-files \
	--enable-widec \
	--disable-lp64 \
	--with-chtype='long' \
	--with-mmask-t='long' \
	--disable-silent-rules \
	--with-abi-version=5
make %{?_smp_mflags}
popd
%install
make -C v5 DESTDIR=%{buildroot} install.libs
make -C v6 DESTDIR=%{buildroot} install
install -vdm 755 %{buildroot}/%{_lib}
ln -sfv ../..%{_lib}/$(readlink %{buildroot}%{_libdir}/libncursesw.so) %{buildroot}%{_libdir}/libncursesw.so
for lib in ncurses form panel menu ; do \
    rm -vf %{buildroot}%{_libdir}/lib${lib}.so ; \
    echo "INPUT(-l${lib}w)" > %{buildroot}%{_libdir}/lib${lib}.so ; \
    ln -sfv lib${lib}w.a %{buildroot}%{_libdir}/lib${lib}.a ; \
    ln -sfv /lib/pkgconfig/${lib}w.pc %{buildroot}/lib/pkgconfig/${lib}.pc
done
ln -sfv libncurses++w.a %{buildroot}%{_libdir}/libncurses++.a
rm -vf %{buildroot}%{_libdir}/libcursesw.so
echo "INPUT(-lncursesw)" > %{buildroot}%{_libdir}/libcursesw.so
ln -sfv libncurses.so %{buildroot}%{_libdir}/libcurses.so
ln -sfv libncursesw.a %{buildroot}%{_libdir}/libcursesw.a
ln -sfv libncurses.a %{buildroot}%{_libdir}/libcurses.a
install -vdm 755  %{buildroot}%{_defaultdocdir}/%{name}-%{version}
ln -sv %{_lib}/libncursesw.so.6.0 %{buildroot}%{_libdir}/libncurses.so.6
cp -v -R doc/* %{buildroot}%{_defaultdocdir}/%{name}-%{version}
ln -sv %{_lib}/libncursesw.so.5.9 %{buildroot}%{_libdir}/libncurses.so.5

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig
%post compat -p /sbin/ldconfig
%postun compat -p /sbin/ldconfig
%files
%defattr(-,root,root)
%{_bindir}/captoinfo
%{_bindir}/clear
%{_bindir}/tabs
%{_bindir}/tic
%{_bindir}/tset
%{_bindir}/reset
%{_bindir}/infocmp
%{_bindir}/tput
%{_bindir}/infotocap
%{_bindir}/toe
%{_libdir}/lib*.so.6*
%{_datadir}/tabset/*
%{_docdir}/ncurses-6.0/html/*
%{_docdir}/ncurses-6.0/*.doc
%{_mandir}/man7/*
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_mandir}/man3/*
%{_datadir}/terminfo/*
%{_libdir}/terminfo

%files compat
%{_libdir}/lib*.so.5*
%{_bindir}/ncursesw5-config

%files devel
%{_bindir}/ncursesw6-config
%{_includedir}/*.h
%{_libdir}/libncurses.a
%{_libdir}/libformw.a
%{_libdir}/libpanel.a
%{_libdir}/libmenuw.a
/lib/pkgconfig/panelw.pc
/lib/pkgconfig/panel.pc
/lib/pkgconfig/form.pc
/lib/pkgconfig/menu.pc
/lib/pkgconfig/ncursesw.pc
/lib/pkgconfig/ncurses++w.pc
/lib/pkgconfig/menuw.pc
/lib/pkgconfig/formw.pc
/lib/pkgconfig/ncurses.pc
%{_libdir}/libncursesw.a
%{_libdir}/libcursesw.a
%{_libdir}/libncurses++w.a
%{_libdir}/libform.a
%{_libdir}/libcurses.a
%{_libdir}/libpanelw.a
%{_libdir}/libncurses++.a
%{_libdir}/libmenu.a
%{_libdir}/libncursesw.so
%{_libdir}/libpanelw.so
%{_libdir}/libcurses.so
%{_libdir}/libformw.so
%{_libdir}/libmenuw.so
%{_libdir}/libncurses.so
%{_libdir}/libform.so
%{_libdir}/libcursesw.so
%{_libdir}/libpanel.so
%{_libdir}/libmenu.so
%changelog
*   Fri Sep 15 2017 Xiaolin Li <xiaolinl@vmware.com> 6.0-6
-   ncurses-devel provides pkgconfig(ncurses)
*   Thu Jul 06 2017 Dheeraj Shetty <dheerajs@vmware.com> 6.0-5
-   Fix for CVE-2017-10684 and CVE-2017-10685
*   Wed Jun 07 2017 Bo Gan <ganb@vmware.com> 6.0-4
-   Remove ncurses /bin/sh dependency
*   Wed Mar 29 2017 Alexey Makhalov <amakhalov@vmware.com> 6.0-3
-   --with-chtype=long --with-mmask-t=long to avoid type clashes (1838226)
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 6.0-2
-   GA - Bump release of all rpms
*   Wed Apr 27 2016 Xiaolin Li <xiaolinl@vmware.com> 6.0-1
-   Update to version 6.0.
*   Wed Nov 18 2015 Mahmoud Bassiouny <mbassiouny@vmware.com> 5.9-4
-   Package provides libncurses.so.5()(64bit)
*   Tue Nov 10 2015 Mahmoud Bassiouny <mbassiouny@vmware.com> 5.9-3
-   Add libncurses.so.5, and minor fix in the devel package
*   Mon May 18 2015 Touseef Liaqat <tliaqat@vmware.com> 5.9-2
-   Update according to UsrMove.
*   Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 5.9-1
-   Initial build.	First version
