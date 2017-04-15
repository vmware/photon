#dont terminate build for unpackaged files.
%define _unpackaged_files_terminate_build 0
%define librepo_name %{name}-%{name}

Summary:        Repodata downloading library
Name:           librepo
Version:        1.7.17
Release:        6%{?dist}
License:        LGPLv2+
URL:            https://github.com/Tojaj/librepo/
Group:          System Environment/Libraries
Source0:        %{name}-%{version}.tar.gz
%define sha1    librepo=e96b735393cd830caca49fe3bf7da767f22d8a8a
Source1:        pygpgme-0.3.tar.gz
%define sha1    pygpgme=f8df35bd2705ac2e1642209fba732e6a42d03fd4
Vendor:         VMware, Inc.
Distribution:   Photon
Requires:       curl-libs, gpgme, libassuan, libgpg-error
Requires:       expat-libs
Requires:       glib
Requires:       openssl

BuildRequires:  cmake
BuildRequires:  glib-devel
BuildRequires:  check
BuildRequires:  expat-devel
BuildRequires:  curl-devel
BuildRequires:  python2-devel
BuildRequires:  python2-libs
BuildRequires:  python2-tools
BuildRequires:  gpgme-devel
BuildRequires:  openssl-devel
BuildRequires:  attr-devel

%description
A library providing C and Python (libcURL like) API for downloading 
linux repository metadata and packages

%package devel
Summary: package config and headers for librepo
Requires: librepo
Requires: curl-devel
Provides: pkgconfig(librepo)

%description devel
Package config and headers for librepo.

%prep
%setup -q -n %{librepo_name}-%{version}
tar xf %{SOURCE1} --no-same-owner

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

%check
easy_install nose flask pyxattr
pushd pygpgme-0.3
python setup.py install
popd

PYTHONPATH=`readlink -f ./librepo/python/python2/` nosetests -s -v tests/python/tests/

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
*   Fri Apr 14 2017 Alexey Makhalov <amakhalov@vmware.com> 1.7.1-6
-   librepo requires expat-libs and curl-libs.
*   Wed Dec 07 2016 Xiaolin Li <xiaolinl@vmware.com> 1.7.1-5
-   BuildRequires curl-devel.
*   Thu Nov 24 2016 Alexey Makhalov <amakhalov@vmware.com> 1.7.1-4
-   BuildRequired attr-devel.
*   Thu Oct 06 2016 ChangLee <changlee@vmware.com> 1.7.1-3
-   Modified %check
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.7.17-2
-   GA - Bump release of all rpms
*   Fri Jan 22 2016 Xiaolin Li <xiaolinl@vmware.com> 1.7.17-1
-   Updated to version 1.7.17
*   Wed Jun 17 2015 Anish Swaminathan <anishs@vmware.com> 1.7.15-1
-   Updated version and split devel package.
*   Tue Dec 30 2014 Priyesh Padmavilasom <ppadmavilasom@vmware.com>
-   initial specfile.

# EOF
