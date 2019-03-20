#dont terminate build for unpackaged files.
%define _unpackaged_files_terminate_build 0
%define librepo_name %{name}-%{name}

Summary:       	Repodata downloading library
Name:          	librepo
Version:       	1.7.17
Release:       	4%{?dist}
License:       	LGPLv2+
URL:           	https://github.com/Tojaj/librepo/
Group:         	System Environment/Libraries
Source0:       	%{name}-%{version}.tar.gz
%define sha1 librepo=e96b735393cd830caca49fe3bf7da767f22d8a8a
Vendor:		VMware, Inc.
Distribution:	Photon
Requires:	curl, gpgme, libassuan, libgpg-error
Requires:	expat
Requires:	glib
BuildRequires:	cmake
BuildRequires:	glib-devel
BuildRequires:	check
BuildRequires:	expat
BuildRequires:	curl
BuildRequires:	python2-devel
BuildRequires:	python2-libs
BuildRequires:	python2-tools
BuildRequires:	gpgme-devel
BuildRequires:	openssl-devel
BuildRequires:	attr

Requires:       openssl

%description
A library providing C and Python (libcURL like) API for downloading 
linux repository metadata and packages

%package devel
Summary: package config and headers for librepo
Requires: librepo
Provides: pkgconfig(librepo)

%description devel
Package config and headers for librepo.

%prep
%setup -q -n %{librepo_name}-%{version}

%build
mkdir build
cd build
cmake -DCMAKE_INSTALL_PREFIX=%{_prefix} -DLIB_INSTALL_DIR=%{_prefix}/lib ..
make %{?_smp_mflags}

%install
mkdir -p %{buildroot}%{_libdir}
mkdir -p %{buildroot}%{_includedir}/librepo
mkdir -p %{buildroot}%{_libdir}/pkgconfig
cp %{_builddir}/%{librepo_name}-%{version}/build/librepo/librepo.so* %{buildroot}%{_libdir}
cp %{_builddir}/%{librepo_name}-%{version}/build/librepo.pc %{buildroot}%{_libdir}/pkgconfig
cp %{_builddir}/%{librepo_name}-%{version}/librepo/*.h %{buildroot}%{_includedir}/librepo

%post 
/sbin/ldconfig

%postun 
/sbin/ldconfig

%files
%defattr(-,root,root)
%{_libdir}/librepo.so*

%files devel
%{_libdir}/pkgconfig/librepo.pc
%{_includedir}/librepo/*.h

%changelog
*   Wed Mar 20 2019 Tapas Kundu <tkundu@vmware.com> 1.7.17-4
-   Bumped up to use latest openssl
* Tue Sep 26 2017 Anish Swaminathan <anishs@vmware.com> 1.7.17-3
- Release bump for expat version update
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.7.17-2
- GA - Bump release of all rpms
* Fri Jan 22 2016 Xiaolin Li <xiaolinl@vmware.com> 1.7.17-1
- Updated to version 1.7.17
* Wed Jun 17 2015 Anish Swaminathan <anishs@vmware.com> 1.7.15-1
- Updated version and split devel package.
* Tue Dec 30 2014 Priyesh Padmavilasom <ppadmavilasom@vmware.com>
- initial specfile.

