Summary:	Libraries for terminal handling of character screens
Name:		ncurses
Version:	5.9
Release:	2%{?dist}
License:	MIT
URL:		http://www.gnu.org/software/ncurses
Group:		Applications/System
Vendor:		VMware, Inc.
Distribution: 	Photon
Source0:	ftp://ftp.gnu.org/gnu/ncurses/%{name}-%{version}.tar.gz
%define sha1 ncurses=3e042e5f2c7223bffdaac9646a533b8c758b65b5
%description
The Ncurses package contains libraries for terminal-independent
handling of character screens.
%package	devel
Summary:	Header and development files for ncurses
Requires:	%{name} = %{version}
%description	devel
It contains the libraries and header files to create applications 
%prep
%setup -q
%build
./configure \
	--prefix=%{_prefix} \
	--mandir=%{_mandir} \
	--with-shared \
	--without-debug \
	--enable-pc-files \
	--enable-widec \
	--disable-silent-rules
make %{?_smp_mflags}
%install
make DESTDIR=%{buildroot} install
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
cp -v -R doc/* %{buildroot}%{_defaultdocdir}/%{name}-%{version}
%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig
%files
%defattr(-,root,root)
%{_bindir}/captoinfo
%{_bindir}/ncursesw5-config
%{_bindir}/clear
%{_bindir}/tabs
%{_bindir}/tic
%{_bindir}/tset
%{_bindir}/reset
%{_bindir}/infocmp
%{_bindir}/tput
%{_bindir}/infotocap
%{_bindir}/toe
%{_libdir}/libmenuw.so.5
%{_libdir}/libformw.so.5.9
%{_libdir}/libmenuw.so.5.9
%{_libdir}/libpanelw.so.5
%{_libdir}/libpanelw.so.5.9
%{_libdir}/libformw.so.5
%{_datadir}/tabset/*
%{_docdir}/ncurses-5.9/html/*
%{_docdir}/ncurses-5.9/*.doc
%{_mandir}/man7/*
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_mandir}/man3/*
%{_datadir}/terminfo/*
%{_libdir}/libncursesw.so.5
%{_libdir}/libncursesw.so.5.9
%{_libdir}/libncurses.so
%{_libdir}/libform.so
%{_libdir}/libcursesw.so
%{_libdir}/libpanel.so
%{_libdir}/libmenu.so
%{_libdir}/terminfo

%files devel
%{_includedir}/cursesm.h
%{_includedir}/form.h
%{_includedir}/cursslk.h
%{_includedir}/ncurses.h
%{_includedir}/cursesw.h
%{_includedir}/termcap.h
%{_includedir}/unctrl.h
%{_includedir}/term.h
%{_includedir}/eti.h
%{_includedir}/ncurses_dll.h
%{_includedir}/curses.h
%{_includedir}/cursesapp.h
%{_includedir}/menu.h
%{_includedir}/tic.h
%{_includedir}/panel.h
%{_includedir}/etip.h
%{_includedir}/term_entry.h
%{_includedir}/cursesp.h
%{_includedir}/nc_tparm.h
%{_includedir}/cursesf.h
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
%changelog
*   Mon May 18 2015 Touseef Liaqat <tliaqat@vmware.com> 5.9-2
-   Update according to UsrMove.
*	Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 5.9-1
-	Initial build.	First version
