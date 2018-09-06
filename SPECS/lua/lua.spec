Summary:	Programming language
Name:		lua
Version:	5.3.5
Release:	1%{?dist}
License:	MIT
URL:		http://www.lua.org
Group:		Development/Tools
Vendor:		VMware, Inc.
Distribution: Photon
Source0:	http://www.lua.org/ftp/%{name}-%{version}.tar.gz
%define sha1 lua=112eb10ff04d1b4c9898e121d6bdf54a81482447
Patch0:		lua-5.3.4-shared_library-1.patch
BuildRequires:	readline-devel
Requires:	readline
%description
Lua is a powerful, light-weight programming language designed for extending
applications. Lua is also frequently used as a general-purpose, stand-alone
language. Lua is free software

%package devel
Summary:	Libraries and header files for lua
Requires:	%{name} = %{version}
%description devel
Static libraries and header files for the support library for lua

%prep
%setup -q
%patch0 -p1
sed -i '/#define LUA_ROOT/s:/usr/local/:/usr/:' src/luaconf.h
sed -i 's/CFLAGS= -fPIC -O2 /CFLAGS= -fPIC -O2 -DLUA_COMPAT_MODULE /' src/Makefile
%build
make VERBOSE=1 %{?_smp_mflags} linux

%install
make %{?_smp_mflags} \
	INSTALL_TOP=%{buildroot}/usr TO_LIB="liblua.so \
	liblua.so.5.3 liblua.so.5.3.4" \
	INSTALL_DATA="cp -d" \
	INSTALL_MAN=%{buildroot}/usr/share/man/man1 \
	install
install -vdm 755 %{buildroot}%{_libdir}/pkgconfig
cat > %{buildroot}%{_libdir}/pkgconfig/lua.pc <<- "EOF"
	V=5.3
	R=5.3.4

	prefix=/usr
	INSTALL_BIN=${prefix}/bin
	INSTALL_INC=${prefix}/include
	INSTALL_LIB=${prefix}/lib
	INSTALL_MAN=${prefix}/man/man1
	exec_prefix=${prefix}
	libdir=${exec_prefix}/lib
	includedir=${prefix}/include

	Name: Lua
	Description: An Extensible Extension Language
	Version: ${R}
	Requires: 
	Libs: -L${libdir} -llua -lm
	Cflags: -I${includedir}
EOF
rmdir %{buildroot}%{_libdir}/lua/5.3
rmdir %{buildroot}%{_libdir}/lua

%check
make test

%clean
rm -rf %{buildroot}
%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig
%files
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/liblua.so.*
%{_mandir}/*/*

%files devel
%{_includedir}/*
%{_libdir}/pkgconfig/lua.pc
%{_libdir}/liblua.so

%changelog
*   Wed Sep 05 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 5.3.5-1
-   Update to version 5.3.5
*   Fri Mar 31 2017 Michelle Wang <michellew@vmware.com> 5.3.4-1
-   Update package version
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 5.3.2-2
-   GA - Bump release of all rpms
*   Wed Apr 27 2016 Xiaolin Li <xiaolinl@vmware.com> 5.3.2-1
-   Update to version 5.3.2.
*   Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 5.2.3-1
-   Initial build.	First version
