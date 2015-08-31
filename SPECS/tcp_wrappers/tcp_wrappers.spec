Summary:	TCP/IP daemon wrapper package
Name:		tcp_wrappers
Version:	7.6
Release:	1%{?dist}
License: 	BSD
Group: 		System Environment/Networking
URL: 		ftp://ftp.porcupine.org/pub/security/index.html
Source0: 	ftp://ftp.porcupine.org/pub/security/%{name}_%{version}.tar.gz
%define sha1 tcp_wrappers=61689ec85b80f4ca0560aef3473eccd9e9e80481
Patch0:		http://www.linuxfromscratch.org/patches/blfs/6.3/tcp_wrappers-7.6-shared_lib_plus_plus-1.patch

%description
The TCP Wrapper package provides daemon wrapper programs that report the name of the client requesting network services and the requested service. 

%package devel
Summary:	The libraries and header files needed for tcp_wrappers development.
Requires: 	%{name} = %{version}-%{release}

%description devel
The libraries and header files needed for tcp_wrappers development.

%prep
%setup -qn %{name}_%{version}
%patch0 -p1

%build
sed -i -e "s,^extern char \*malloc();,/* & */," scaffold.c &&
make REAL_DAEMON_DIR=%{_sbindir}STYLE=-DPROCESS_OPTIONS linux

%install
mkdir -p %{buildroot}%{_libdir}
mkdir -p %{buildroot}%{_sbindir}
mkdir -p %{buildroot}%{_mandir}/man{3,5,8}
mkdir -p %{buildroot}%{_includedir}
make DESTDIR=%{buildroot} install 

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(-, root, root)
%{_libdir}/*.so.*
%{_libdir}/*.a
%{_sbindir}/*
%{_mandir}/man3/*
%{_mandir}/man5/*
%{_mandir}/man8/*

%files devel
%defattr(-, root, root)
%{_libdir}/*.so
%{_includedir}/*.h

%changelog
* Fri Aug 28 2015 Divya Thaluru <dthaluru@vmware.com> 7.6-1
- Initial version

