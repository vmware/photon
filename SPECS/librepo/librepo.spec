#dont terminate build for unpackaged files.
%define _unpackaged_files_terminate_build 0
%define librepo_name %{name}-%{name}

Summary:       	Repodata downloading library
Name:          	librepo
Version:       	1.7.15
Release:       	1%{?dist}
License:       	LGPLv2+
URL:           	https://github.com/Tojaj/librepo/
Group:         	System Environment/Libraries
Source0:       	%{name}-%{version}.tar.gz
%define sha1 librepo=a753212f721be8782c8c3aa40e450247676b7649
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

Requires:       openssl-devel

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
* Wed Jun 17 2015 Anish Swaminathan <anishs@vmware.com> 1.7.15-1
- Updated version and split devel package.
* Tue Dec 30 2014 Priyesh Padmavilasom <ppadmavilasom@vmware.com>
- initial specfile.

# EOF
