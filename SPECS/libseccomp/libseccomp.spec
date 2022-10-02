Summary:      Enhanced seccomp library
Name:         libseccomp
Version:      2.4.0
Release:      3%{?dist}
License:      LGPLv2
Group:        System Environment/Libraries
Url:          https://github.com/seccomp/libseccomp/wiki
Vendor:       VMware, Inc.
Distribution: Photon

Source0:      https://github.com/seccomp/libseccomp/releases/download/v%{version}/%{name}-%{version}.tar.gz
%define sha512 libseccomp=daa4a32c6c2b2f39aa9db1a4606619f9faeffcd2fca00c25ac5cf95d0405639ec21203293be7c8341317a05b18fd9f603a201544457cac91bf034a0bbd4dfc88

%if %{with_check}
BuildRequires: which
%endif

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
Requires: %{name} = %{version}-%{release}

%description devel
The libseccomp-devel package contains the libraries and header files
needed for developing secure applications.

%prep
%autosetup -p1

%build
%configure
make V=1 %{?_smp_mflags}

%install
make V=1 DESTDIR="%{buildroot}" install %{?_smp_mflags}

%check
make check %{?_smp_mflags}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc LICENSE
%doc CREDITS
%doc README.md
%{_libdir}/libseccomp.so.*

%files devel
%{_includedir}/seccomp.h
%{_libdir}/libseccomp.so
%{_libdir}/libseccomp.a
%{_libdir}/pkgconfig/libseccomp.pc
%{_bindir}/scmp_sys_resolver
%{_mandir}/man1/*
%{_mandir}/man3/*

%changelog
* Sun Oct 02 2022 Shreenidhi Shedi <sshedi@vmware.com> 2.4.0-3
- Remove .la files
* Tue Sep 3 2019 Michelle Wang <michellew@vmware.com> 2.4.0-2
- Fix make check for libseccomp
* Fri Mar 29 2019 Michelle Wang <michellew@vmware.com> 2.4.0-1
- Updated to version 2.4.0 for CVE-2019-9893
* Mon Sep 10 2018 Bo Gan <ganb@vmware.com> 2.3.3-1
- Updated to version 2.3.3
* Tue Apr 11 2017 Harish Udaiya KUmar <hudaiyakumar@vmware.com> 2.3.2-1
- Updated to version 2.3.2
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.2.3-2
- GA - Bump release of all rpms
* Sat Jan 16 2016 Fabio Rapposelli <fabio@vmware.com> - 2.2.3-1
- First release of the package
