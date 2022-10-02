Summary:    GNU Unicode string library
Name:       libunistring
Version:    0.9.10
Release:    2%{?dist}
License:    LGPLv3+
Url:        http://www.gnu.org/software/libunistring/
Group:      System Environment/Libraries
Vendor:     VMware, Inc.
Distribution:   Photon

Source0: http://ftp.gnu.org/gnu/libunistring/%{name}-%{version}.tar.xz
%define sha512 %{name}=01dcab6e05ea4c33572bf96cc0558bcffbfc0e62fc86410cef06c1597a0073d5750525fe2dee4fdb39c9bd704557fcbab864f9645958108a2e07950bc539fe54

%description
libunistring is a library that provides functions for manipulating Unicode strings and for manipulating C strings according to the Unicode standard.

%package devel
Summary:    Development libraries and header files for libunistring
Requires:   %{name} = %{version}-%{release}

%description devel
The package contains libraries and header files for
developing applications that use libunistring.

%prep
%autosetup -p1

%build
%configure
make %{?_smp_mflags}

%install
%make_install %{?_smp_mflags}

rm -rf %{buildroot}%{_infodir}/* \
       %{buildroot}%{_libdir}/*.la

%check
make %{?_smp_mflags} check

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_libdir}/*.so.*
%{_docdir}/%{name}/*
%{_libdir}/*.a

%files devel
%defattr(-,root,root)
%{_includedir}/*.h
%{_includedir}/unistring/*.h
%{_libdir}/*.so

%changelog
* Sun Oct 02 2022 Shreenidhi Shedi <sshedi@vmware.com> 0.9.10-2
- Remove .la files
* Mon Sep 10 2018 Alexey Makhalov <amakhalov@vmware.com> 0.9.10-1
- Version update to fix compilation issue againts glibc-2.28
* Thu Apr 06 2017 Kumar Kaushik <kaushikk@vmware.com> 0.9.7-1
- Updating Version to 0.9.7
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.9.6-2
- GA - Bump release of all rpms
* Mon Feb 22 2016 XIaolin Li <xiaolinl@vmware.com> 0.9.6-1
- Updated to version 0.9.6
* Thu Jun 18 2015 Divya Thaluru <dthaluru@vmware.com> 0.9.5-1
- Initial build. First version
