Summary:      Enhanced seccomp library
Name:         libseccomp
Version:      2.3.2
Release:      1%{?dist}
License:      LGPLv2
Group:        System Environment/Libraries
Source0:      https://github.com/seccomp/libseccomp/releases/download/v%{version}/%{name}-%{version}.tar.gz
%define sha1 libseccomp=6eb7fa147008f4ae189d56c2ea801a619bb08cd0
Url:          https://github.com/seccomp/libseccomp/wiki
Vendor:       VMware, Inc.
Distribution: Photon

%description
The libseccomp library provides an easy to use, platform independent, interface
to the Linux Kernel syscall filtering mechanism: seccomp. The libseccomp API
is designed to abstract away the underlying BPF based syscall filter language
and present a more conventional function-call based filtering interface that
should be familiar to, and easily adopted by application developers.

%package devel
Summary:  Development files used to build applications with libseccomp support
Group:    Development/Libraries
Provides: pkgconfig(libseccomp)

%description devel
The libseccomp-devel package contains the libraries and header files
needed for developing secure applications.

%prep
%setup -q

%build
./configure --prefix="%{_prefix}" --libdir="%{_libdir}"
CFLAGS="%{optflags}" make V=1 %{?_smp_mflags}

%install
rm -rf "%{buildroot}"
mkdir -p "%{buildroot}/%{_libdir}"
mkdir -p "%{buildroot}/%{_includedir}"
mkdir -p "%{buildroot}/%{_mandir}"
make V=1 DESTDIR="%{buildroot}" install

%check
make check

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc LICENSE
%doc CREDITS
%doc README.md
%{_libdir}/libseccomp.so.*
%{_libdir}/libseccomp.a
%{_libdir}/libseccomp.la

%files devel
%{_includedir}/seccomp.h
%{_libdir}/libseccomp.so
%{_libdir}/pkgconfig/libseccomp.pc
%{_bindir}/scmp_sys_resolver
%{_mandir}/man1/*
%{_mandir}/man3/*

%changelog
*	Tue Apr 11 2017 Harish Udaiya KUmar <hudaiyakumar@vmware.com> 2.3.2-1
-	Updated to version 2.3.2
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.2.3-2
-	GA - Bump release of all rpms
* Sat Jan 16 2016 Fabio Rapposelli <fabio@vmware.com> - 2.2.3-1
- First release of the package
