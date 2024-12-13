%global major_version 5.4

# If you are incrementing major_version, enable bootstrapping and adjust accordingly.
# Version should be the latest prior build. If you don't do this, RPM will break.
%global bootstrap 0
%global bootstrap_major_version 5.3
%global bootstrap_version %{bootstrap_major_version}.6

Summary:        Programming language
Name:           lua
Version:        5.4.6
Release:        3%{?dist}
URL:            http://www.lua.org
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: http://www.lua.org/ftp/%{name}-%{version}.tar.gz
%define sha512 %{name}-%{version}=d90c6903355ee1309cb0d92a8a024522ff049091a117ea21efb585b5de35776191cd67d17a65b18c2f9d374795b7c944f047576f0e3fe818d094b26f0e4845c5

%if 0%{?bootstrap}
Source1: http://www.lua.org/ftp/%{name}-%{bootstrap_version}.tar.gz
%define sha512 %{name}-%{bootstrap_version}=ccc380d5e114d54504de0bfb0321ca25ec325d6ff1bfee44b11870b660762d1a9bf120490c027a0088128b58bb6b5271bbc648400cab84d2dc22b512c4841681
%endif

Source2: license.txt
%include %{SOURCE2}

Patch0: lua-%{version}-shared-library.patch

%if 0%{?bootstrap}
Patch1: lua-%{bootstrap_version}-shared-library.patch
%endif

BuildRequires: readline-devel

Requires: readline
Requires: %{name}-libs = %{version}-%{release}

%description
Lua is a powerful light-weight programming language designed for
extending applications. Lua is also frequently used as a
general-purpose, stand-alone language. Lua is free software.
Lua combines simple procedural syntax with powerful data description
constructs based on associative arrays and extensible semantics. Lua
is dynamically typed, interpreted from bytecodes, and has automatic
memory management with garbage collection, making it ideal for
configuration, scripting, and rapid prototyping.

%package devel
Summary:    Development files for %{name}
Requires:   %{name} = %{version}-%{release}

%description devel
This package contains development files for %{name}.

%package libs
Summary: Libraries for %{name}
Conflicts: %{name} < 5.4.4-5

%description libs
This package contains the shared libraries for %{name}.

%prep
%if 0%{?bootstrap}
# Using autosetup is not feasible
%setup -q -a0 -a1 -n %{name}-%{version}
pushd %{name}-%{bootstrap_version}
sed -i '/#define LUA_ROOT/s:/usr/local/:/usr/:' src/luaconf.h
sed -i 's/CFLAGS= -fPIC -O2 /CFLAGS= -fPIC -O2 -DLUA_COMPAT_MODULE /' src/Makefile
%{__patch} -p1 < %{PATCH1}
popd
%else
# Using autosetup is not feasible
%setup -q
%endif

sed -i '/#define LUA_ROOT/s:/usr/local/:/usr/:' src/luaconf.h
sed -i 's/CFLAGS= -fPIC -O2 /CFLAGS= -fPIC -O2 -DLUA_COMPAT_MODULE /' src/Makefile

%{__patch} -p1 < %{PATCH0}

%build
make VERBOSE=1 %{?_smp_mflags} linux

%if 0%{?bootstrap}
pushd %{name}-%{bootstrap_version}
make VERBOSE=1 %{?_smp_mflags} linux
popd
%endif

%install
lua_make_install() {
  local loc="$1"
  local v1="$2"
  local v2="$3"

  make install %{?_smp_mflags} \
      INSTALL_TOP=${loc} TO_LIB="liblua.so liblua.so.${v1} liblua.so.${v2}" \
      INSTALL_DATA="cp -d" \
      INSTALL_MAN=${loc}/share/man/man1
}

lua_make_install %{buildroot}%{_prefix} %{major_version} %{version}
install -vdm 755 %{buildroot}%{_libdir}/pkgconfig

cat > %{buildroot}%{_libdir}/pkgconfig/%{name}.pc <<- "EOF"
    V=%{major_version}
    R=%{version}
    prefix=%{_prefix}
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

rmdir %{buildroot}%{_libdir}/%{name}/%{major_version} \
      %{buildroot}%{_libdir}/%{name}

%if 0%{?bootstrap}
pushd %{name}-%{bootstrap_version}
mkdir -p %{buildroot}/installdir
lua_make_install %{buildroot}/installdir%{_prefix} %{bootstrap_major_version} %{bootstrap_version}
cp -a %{buildroot}/installdir%{_libdir}/liblua.so.%{bootstrap_version} \
      %{buildroot}/installdir%{_libdir}/liblua.so.%{bootstrap_major_version} \
      %{buildroot}%{_libdir}
rm -rf %{buildroot}/installdir
popd
%endif

%if 0%{?with_check}
%check
make test %{?_smp_mflags}
%endif

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_bindir}/*

%files libs
%defattr(-,root,root)
%{_libdir}/liblua.so.*

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/pkgconfig/%{name}.pc
%{_libdir}/liblua.so
%{_mandir}/*

%changelog
* Thu Dec 12 2024 Ajay Kaher <ajay.kaher@broadcom.com> 5.4.6-3
- Release bump for SRP compliance
* Tue Nov 05 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 5.4.6-2
- Release bump for SRP compliance
* Tue Jun 20 2023 Shreenidhi Shedi <sshedi@vmware.com> 5.4.6-1
- Upgrade to v5.4.6
* Thu Mar 09 2023 Shreenidhi Shedi <sshedi@vmware.com> 5.4.4-5
- Add lua-libs sub package
* Wed Dec 21 2022 Shreenidhi Shedi <sshedi@vmware.com> 5.4.4-4
- Bump version as a part of readline upgrade
* Thu Jul 14 2022 Shreenidhi Shedi <sshedi@vmware.com> 5.4.4-3
- Fix CVE-2022-33099
* Mon Apr 18 2022 Shreenidhi Shedi <sshedi@vmware.com> 5.4.4-2
- Fix CVE-2022-28805
* Thu Mar 24 2022 Shreenidhi Shedi <sshedi@vmware.com> 5.4.4-1
- Upgrade to v5.4.4
* Mon Nov 15 2021 Shreenidhi Shedi <sshedi@vmware.com> 5.4.3-2
- Fix CVE-2021-43519
* Fri May 21 2021 Shreenidhi Shedi <sshedi@vmware.com> 5.4.3-1
- Upgrade to version 5.4.3
* Wed Sep 05 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 5.3.5-1
- Update to version 5.3.5
* Fri Mar 31 2017 Michelle Wang <michellew@vmware.com> 5.3.4-1
- Update package version
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 5.3.2-2
- GA - Bump release of all rpms
* Wed Apr 27 2016 Xiaolin Li <xiaolinl@vmware.com> 5.3.2-1
- Update to version 5.3.2.
* Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 5.2.3-1
- Initial build. First version
