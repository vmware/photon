Summary:        Repodata downloading library
Name:           librepo
Version:        1.9.1
Release:        1%{?dist}
License:        LGPLv2+
URL:            https://github.com/Tojaj/librepo/
Group:          System Environment/Libraries
Source0:        %{name}-%{version}.tar.gz
%define sha1    %{name}=195d4b74bca7c761ab890e9af254c53dba8f16b2
Source1:        pygpgme-0.3.tar.gz
%define sha1    pygpgme=f8df35bd2705ac2e1642209fba732e6a42d03fd4
Vendor:         VMware, Inc.
Distribution:   Photon
Requires:       curl-libs, gpgme, libassuan, libgpg-error
Requires:       expat-libs
Requires:       glib
Requires:       openssl
Requires:       curl-devel

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
BuildRequires:  libxml2-devel

%description
A library providing C and Python (libcURL like) API for downloading
linux repository metadata and packages

%package devel
Summary: package config and headers for librepo
Requires: %{name} = %{version}-%{release}
Requires: curl-devel
Requires: expat-devel
Provides: pkgconfig(librepo)
%description devel
Package config and headers for librepo.

%prep
%setup -q
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
cp %{_builddir}/%{name}-%{version}/build/librepo/librepo.so* %{buildroot}%{_libdir}
cp %{_builddir}/%{name}-%{version}/build/librepo.pc %{buildroot}%{_libdir}/pkgconfig
cp %{_builddir}/%{name}-%{version}/librepo/*.h %{buildroot}%{_includedir}/librepo

%check
pushd build/tests
./run_tests.sh
popd

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
*   Fri Sep 21 2018 Ankit Jain <ankitja@vmware.com> 1.9.1-1
-   Updated to version 1.9.1
*   Thu Jun 08 2017 Chang Lee <changlee@vmware.com> 1.7.20-2
-   Updated %check
*   Thu Apr 20 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 1.7.20-1
-   Updated to version 1.7.20
*   Fri Apr 14 2017 Alexey Makhalov <amakhalov@vmware.com> 1.7.17-6
-   Requires expat-libs, expat-devel and curl-libs.
*   Wed Dec 07 2016 Xiaolin Li <xiaolinl@vmware.com> 1.7.17-5
-   BuildRequires curl-devel.
*   Thu Nov 24 2016 Alexey Makhalov <amakhalov@vmware.com> 1.7.17-4
-   BuildRequired attr-devel.
*   Thu Oct 06 2016 ChangLee <changlee@vmware.com> 1.7.17-3
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
