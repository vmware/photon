Summary:    TCP/IP daemon wrapper package
Name:       tcp_wrappers
Version:    7.6
Release:    9%{?dist}
Group:      System Environment/Networking
Vendor:     VMware, Inc.
Distribution:   Photon
URL:            http://ftp.porcupine.org/pub/security/index.html

Source0:    http://ftp.porcupine.org/pub/security/%{name}_%{version}.tar.gz
%define sha512 %{name}=2d9d003791f8d00912a36ae00579e2b8dd7ad8a7bf8eae259659bcaf5365b150540ff6c93c91765872c76041579b7a02b6e3c64528fb7f8235680399ba1d9dac

Source1: license.txt
%include %{SOURCE1}

# Patch0 is taken from:
# http://www.linuxfromscratch.org/patches/blfs/6.3/tcp_wrappers-7.6-shared_lib_plus_plus-1.patch
Patch0: %{name}-%{version}-shared_lib_plus_plus-1.patch

Requires:       finger
Requires:       libnsl

BuildRequires:  libnsl-devel

%description
The TCP Wrapper package provides daemon wrapper programs that report the name of the client requesting network services and the requested service.

%package devel
Summary:    The libraries and header files needed for tcp_wrappers development.
Requires:   %{name} = %{version}-%{release}
Requires:   libnsl-devel

%description devel
The libraries and header files needed for tcp_wrappers development.

%prep
%autosetup -p1 -n %{name}_%{version}

%build
sed -i -e "s,^extern char \*malloc();,/* & */," scaffold.c
sed -i 's/-O2/-O2 -DUSE_GETDOMAIN/g' Makefile
make REAL_DAEMON_DIR=%{_sbindir} STYLE=-DPROCESS_OPTIONS CC=%{_host}-gcc linux %{?_smp_mflags}

%install
mkdir -p %{buildroot}%{_libdir} \
         %{buildroot}%{_sbindir} \
         %{buildroot}%{_mandir}/man{3,5,8} \
         %{buildroot}%{_includedir}

make DESTDIR=%{buildroot} install %{?_smp_mflags}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

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
* Thu Dec 12 2024 Dweep Advani <dweep.advani@broadcom.com> 7.6-9
- Release bump for SRP compliance
* Sun May 29 2022 Shreenidhi Shedi <sshedi@vmware.com> 7.6-8
- Bump version as a part of libnsl upgrade
* Tue Aug 25 2020 Keerthana K <keerthanak@vmware.com> 7.6-7
- Added HAVE_STRERROR CFLAGS for linux target in Makefile
- to build with glibc v2.32 since sys_errlist and sys_nerr are deprecated.
* Thu Nov 15 2018 Alexey Makhalov <amakhalov@vmware.com> 7.6-6
- Cross compilation support
* Tue Sep 25 2018 Alexey Makhalov <amakhalov@vmware.com> 7.6-5
- Use libnsl
* Mon Sep 18 2017 Dheeraj Shetty <dheerajs@vmware.com> 7.6-4
- Add finger to Requires
* Wed Aug 23 2017 Alexey Makhalov <amakhalov@vmware.com> 7.6-3
- Fix compilation issue for glibc-2.26
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 7.6-2
- GA - Bump release of all rpms
* Fri Aug 28 2015 Divya Thaluru <dthaluru@vmware.com> 7.6-1
- Initial version
