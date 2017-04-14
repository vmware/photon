Summary:        Tool Command Language - the language and library.
Name:           tcl
Version:        8.6.6
Release:        1%{?dist}
URL:            http://tcl.sourceforge.net/
License:        LGPLv2+
Group:          System Environment/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        http://downloads.sourceforge.net/sourceforge/tcl/tcl-core%{version}-src.tar.gz
%define sha1    tcl-core=6a1bc424faeef44fed5e44d32198c7ff4ff05658

BuildRequires:  cmake

%description
Tcl provides a powerful platform for creating integration applications that
tie together diverse applications, protocols, devices, and frameworks.
When paired with the Tk toolkit, Tcl provides the fastest and most powerful
way to create GUI applications that run on PCs, Unix, and Mac OS X.
Tcl can also be used for a variety of web-related tasks and for creating
powerful command languages for applications.

%package devel
Summary: Headers and development libraries for tcl
Group: Development/Libraries
Requires: %{name} = %{version}

%description devel
Headers and development libraries for tcl

%prep
%setup -q -n %{name}%{version}

%build
cd unix
./configure \
       --prefix=%{_prefix}  \
       --mandir=%{_mandir}  \
       --enable-threads     \
       --enable-shared      \
       --enable-symbols
make %{?_smp_mflags}

%install
[ %{buildroot} != "/"] && rm -rf %{buildroot}/*
cd unix
make DESTDIR=%{buildroot} install

%check
cd unix
make test

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/libtcl8.6.so
%{_mandir}/man1/*


%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/pkgconfig/tcl.pc
%{_libdir}/tcl8.6/*
%{_libdir}/tcl8/*
%{_libdir}/tclConfig.sh
%{_libdir}/tclooConfig.sh
%{_libdir}/libtclstub8.6.a
%{_mandir}/mann/*
%{_mandir}/man3/*



%changelog
*   Wed Apr 12 2017 Xiaolin Li <xiaolinl@vmware.com>  8.6.6-1
-   Initial build.  First version
