Summary:	Programming language
Name:		lua
Version:	5.3.2
Release:	2%{?dist}
License:	MIT
URL:		http://www.lua.org
Group:		Development/Tools
Vendor:		VMware, Inc.
Distribution: Photon
Source0:	ttp://www.lua.org/ftp/%{name}-%{version}.tar.gz
%define sha1 lua=7a47adef554fdca7d0c5536148de34579134a973
Patch0:		lua-5.3.2-shared_library-1.patch
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
	liblua.so.5.3 liblua.so.5.3.2" \
	INSTALL_DATA="cp -d" \
	INSTALL_MAN=%{buildroot}/usr/share/man/man1 \
	install
install -vdm 755 %{buildroot}%{_libdir}/pkgconfig
cat > %{buildroot}%{_libdir}/pkgconfig/lua.pc <<- "EOF"
	V=5.3
	R=5.3.2

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
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 5.3.2${R}-2
-	GA - Bump release of all rpms
*	Wed Apr 27 2016 Xiaolin Li <xiaolinl@vmware.com> 5.3.2-1
-   Update to version 5.3.2.
*	Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 5.2.3-1
-	Initial build.	First version
