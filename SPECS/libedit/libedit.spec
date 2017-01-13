Summary:        NetBSD Editline library (libedit).
Name:           libedit
Version:        3.1
Release:        1%{?dist}
License:        BSD
URL:            http://lldb.llvm.org
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        http://thrysoee.dk/editline/%{name}-20160903-%{version}.tar.gz
%define sha1    libedit=55e327ee4661b13d20ebb411d790f2bb258271cf

%description
Libedit is an autotool- and libtoolized port of the NetBSD Editline library (libedit). This Berkeley-style licensed command line editor library provides generic line editing, history, and tokenization functions, similar to those found in GNU Readline.

%package devel
Summary:        Development headers for libedit
Requires:       %{name} = %{version}-%{release}

%description devel
The libedit-devel package contains libraries, header files and documentation
for developing applications that use libedit.

%prep
%setup -q -n %{name}-20160903-%{version}


%build
%configure --disable-static
make %{?_smp_mflags}

%install
[ %{buildroot} != "/"] && rm -rf %{buildroot}/*
make DESTDIR=%{buildroot} install
find %{buildroot} -name '*.la' -delete

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%check
make %{?_smp_mflags} check

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_libdir}/libedit.so.*
%exclude %{_mandir}/man3/history.3*
%{_mandir}/man[357]/*

%files devel
%{_includedir}/*
%{_libdir}/libedit.so
%{_libdir}/pkgconfig/libedit.pc



%changelog
*   Wed Jan 11 2017 Xiaolin Li <xiaolinl@vmware.com>  3.1-1
-   Initial build.
