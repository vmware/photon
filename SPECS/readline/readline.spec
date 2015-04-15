Summary:	Command-line editing and history capabilities
Name:		readline
Version:	6.3
Release:	1
License:	GPLv3+
URL:		http://cnswww.cns.cwru.edu/php/chet/readline/rltop.html
Group:		Applications/System
Vendor:		VMware, Inc.
Distribution: 	Photon
Source0:	http://ftp.gnu.org/gnu/readline/%{name}-%{version}.tar.gz
Patch:		http://www.linuxfromscratch.org/patches/lfs/development/readline-6.3-upstream_fixes-3.patch
BuildRequires:	ncurses-devel
%description
The Readline package is a set of libraries that offers command-line
editing and history capabilities.
%package	devel
Summary:	Header and development files for readline
Requires:	%{name} = %{version}
%description	devel
It contains the libraries and header files to create applications 
%prep
%setup -q
sed -i '/MV.*old/d' Makefile.in
sed -i '/{OLDSUFF}/c:' support/shlib-install
%patch -p1
%build
./configure \
	--prefix=%{_prefix} \
	--disable-silent-rules
make SHLIB_LIBS=-lncurses
%install
make DESTDIR=%{buildroot} install
install -vdm 755 %{buildroot}%{_lib}
mv -v %{buildroot}%{_libdir}/lib{readline,history}.so.* %{buildroot}%{_lib}
ln -sfv ../..%{_lib}/$(readlink %{buildroot}%{_libdir}/libreadline.so) %{buildroot}%{_libdir}/libreadline.so
ln -sfv ../..%{_lib}/$(readlink %{buildroot}%{_libdir}/libhistory.so ) %{buildroot}%{_libdir}/libhistory.so
install -vdm 755 %{buildroot}%{_defaultdocdir}/%{name}-%{version}
install -v -m644 doc/*.{ps,pdf,html,dvi} %{buildroot}%{_defaultdocdir}/%{name}-%{version}
rm -rf %{buildroot}%{_infodir}
%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig
%files
%defattr(-,root,root)
%{_lib}/libreadline.so.6
%{_lib}/libhistory.so.6
%{_lib}/libhistory.so.6.3
%{_lib}/libreadline.so.6.3
%{_datadir}/%{name}/hist_purgecmd.c
%{_datadir}/%{name}/rltest.c
%{_datadir}/%{name}/rlversion.c
%{_datadir}/%{name}/rlptytest.c
%{_datadir}/%{name}/rlevent.c
%{_datadir}/%{name}/rl-callbacktest.c
%{_datadir}/%{name}/rlcat.c
%{_datadir}/%{name}/histexamp.c
%{_datadir}/%{name}/rl-fgets.c
%{_datadir}/%{name}/rl.c
%{_datadir}/%{name}/excallback.c
%{_datadir}/%{name}/manexamp.c
%{_datadir}/%{name}/hist_erasedups.c
%{_datadir}/%{name}/fileman.c
%{_docdir}/%{name}/INSTALL
%{_docdir}/%{name}/README
%{_docdir}/%{name}/CHANGES
%{_docdir}/%{name}-%{version}/readline.html
%{_docdir}/%{name}-%{version}/readline.dvi
%{_docdir}/%{name}-%{version}/history.pdf
%{_docdir}/%{name}-%{version}/rluserman.html
%{_docdir}/%{name}-%{version}/rluserman.dvi
%{_docdir}/%{name}-%{version}/history.dvi
%{_docdir}/%{name}-%{version}/readline.ps
%{_docdir}/%{name}-%{version}/history.ps
%{_docdir}/%{name}-%{version}/rluserman.ps
%{_docdir}/%{name}-%{version}/readline.pdf
%{_docdir}/%{name}-%{version}/history_3.ps
%{_docdir}/%{name}-%{version}/readline_3.ps
%{_docdir}/%{name}-%{version}/history.html
%{_docdir}/%{name}-%{version}/rluserman.pdf
%{_mandir}/man3/history.3.gz
%{_mandir}/man3/readline.3.gz
%files devel
%{_includedir}/%{name}/keymaps.h
%{_includedir}/%{name}/history.h
%{_includedir}/%{name}/rlstdc.h
%{_includedir}/%{name}/chardefs.h
%{_includedir}/%{name}/readline.h
%{_includedir}/%{name}/rlconf.h
%{_includedir}/%{name}/rltypedefs.h
%{_includedir}/%{name}/tilde.h
%{_libdir}/libreadline.a
%{_libdir}/libhistory.a
%{_libdir}/libhistory.so
%{_libdir}/libreadline.so
%changelog
*	Wed Oct 22 2014 Divya Thaluru <dthaluru@vmware.com> 6.3-1
-	Initial build.	First version
