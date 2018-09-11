Summary:	Crypto Libraries
Name:		libgcrypt
Version:	1.8.3
Release:	1%{?dist}
License:        GPLv2+ and LGPLv2+
URL:            http://www.gnu.org/software/libgcrypt/
Source0:        ftp://ftp.gnupg.org/gcrypt/libgcrypt/%{name}-%{version}.tar.bz2
%define sha1 libgcrypt=13bd2ce69e59ab538e959911dfae80ea309636e3
Group:		System Environment/Libraries
Vendor:		VMware, Inc.
BuildRequires:	libgpg-error-devel
Requires:	libgpg-error
Distribution:	Photon
%description
The libgcrypt package contains a general purpose crypto library based on the code used in GnuPG. The library provides a high level interface to cryptographic building blocks using an extendable and flexible API.

%package devel
Summary:	Development libraries and header files for libgcrypt
Requires:	%{name} = %{version}-%{release}
Requires:	libgpg-error-devel

%description devel
The package contains libraries and header files for
developing applications that use libgcrypt.

%prep
%setup -q

%build
%configure
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install
rm -rf %{buildroot}%{_infodir}

%check
make %{?_smp_mflags} check

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/*.so.*
%{_mandir}/man1/*

%files devel
%defattr(-,root,root)
%{_includedir}/*.h
%{_datadir}/aclocal/*
%{_libdir}/*.la
%{_libdir}/*.so

%changelog
*   Mon Sep 10 2018 Bo Gan <ganb@vmware.com> 1.8.3-1
-   Update to 1.8.3
*   Tue Oct 10 2017 Vinay Kulkarni <kulkarniv@vmware.com> 1.8.1-1
-   Updated to v1.8.1 to address CVE-2017-0379
*   Tue Apr 04 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 1.7.6-1
-   Udpated to version 1.7.6
*   Thu Nov 24 2016 Alexey Makhalov <amakhalov@vmware.com> 1.6.5-3
-   Required libgpg-error-devel.
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.6.5-2
-   GA - Bump release of all rpms
*   Tue Feb 23 2016 Anish Swaminathan <anishs@vmware.com>  1.6.5-1
-   Upgrade to 1.6.5
*   Wed Jun 17 2015 Divya Thaluru <dthaluru@vmware.com> 1.6.3-1
-   Initial build. First version
