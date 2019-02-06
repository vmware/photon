Summary:        Crypto Libraries
Name:           libgcrypt
Version:        1.7.6
Release:        5%{?dist}
License:        GPLv2+ and LGPLv2+
URL:            http://www.gnu.org/software/libgcrypt/
Source0:        ftp://ftp.gnupg.org/gcrypt/libgcrypt/%{name}-%{version}.tar.bz2
%define sha1 libgcrypt=d2b9e0f413064cfc67188f80d3cbda887c755a62
Patch0:         CVE-2017-0379.patch
Patch1:         libgcrypt-CVE-2017-9526.patch
Patch2:         libgcrypt-CVE-2018-0495.patch
Patch3:         libgcrypt-CVE-2017-7526.patch
Group:          System Environment/Libraries
Vendor:         VMware, Inc.
BuildRequires:  libgpg-error
Requires:       libgpg-error
Distribution:   Photon

%description
The libgcrypt package contains a general purpose crypto library based on the
code used in GnuPG. The library provides a high level interface to
cryptographic building blocks using an extendable and flexible API.

%package devel
Summary:    Development libraries and header files for libgcrypt
Requires:   libgcrypt

%description devel
The package contains libraries and header files for developing applications
that use libgcrypt.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
./configure \
    --prefix=%{_prefix}
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install
rm %{buildroot}%{_infodir}/*

%check
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}

%post   -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/*.so.*
%{_mandir}/man1/*

%files devel
%defattr(-,root,root)
%{_includedir}/*.h
%{_libdir}/*.so
%{_libdir}/*.la
/usr/share/aclocal/libgcrypt.m4

%changelog
*   Wed Feb 06 2019 Dweep Advani <dadvani@vmware.com> 1.7.6-5
-   Fixed CVE-2017-7526
*   Mon Sep 03 2018 Ankit Jain <ankitja@vmware.com> 1.7.6-4
-   Fix for CVE-2018-0495
*   Thu Oct 19 2017 Xiaolin Li <xiaolinl@vmware.com> 1.7.6-3
-   Fix CVE-2017-9526
*   Tue Oct 17 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.7.6-2
-   Fix CVE-2017-0379
*   Mon Apr 17 2017 Vinay Kulkarni <kulkarniv@vmware.com> 1.7.6-1
-   Update to 1.7.6 to fix CVE-2016-6313.
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.6.5-2
-   GA - Bump release of all rpms
*   Tue Feb 23 2016 Anish Swaminathan <anishs@vmware.com>  1.6.5-1
-   Upgrade to 1.6.5
*   Wed Jun 17 2015 Divya Thaluru <dthaluru@vmware.com> 1.6.3-1
-   Initial build. First version

