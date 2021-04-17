Summary:        Low level cryptographic libraries
Name:           nettle
Version:        3.7.2
Release:        1%{?dist}
License:        LGPLv3+ or GPLv2+
URL:            http://www.lysator.liu.se/~nisse/nettle/
Source0:        https://ftp.gnu.org/gnu/nettle/%{name}-%{version}.tar.gz
%define sha1 nettle=d617fbcf8d301dfd887129c3883629d4d097c579
Patch0:         Use-EVP_MD_CTX_create.patch
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
Provides:       libhogweed.so.6()(64bit)
Provides:       libhogweed.so.6(HOGWEED_6)(64bit)
Provides:       libnettle.so.8()(64bit)
Provides:       libnettle.so.8(NETTLE_8)(64bit)
Requires:       gmp

%description
GNettle is a cryptographic library that is designed to fit easily in more
or less any context: In crypto toolkits for object-oriented languages
(C++, Python, Pike, ...), in applications like LSH or GNUPG, or even in
kernel space.

%package devel
Summary:        Development libraries and header files for nettle
Requires:       nettle
Provides:       pkgconfig(hogweed)
Provides:       pkgconfig(nettle)

%description devel
The package contains libraries and header files for
developing applications that use nettle.

%prep
%autosetup -p1

%build
./configure \
        --prefix=%{_prefix} \
        --enable-shared
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
%{_libdir}/*.so.*
%{_bindir}/*

%files devel
%defattr(-,root,root)
%{_includedir}/nettle/*.h
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_libdir}/*.a

%changelog
*   Sat Apr 17 2021 Shreenidhi Shedi <sshedi@vmware.com> 3.7.2-1
-   Bump version to 3.7.2 to fix CVE-2021-20305
*   Mon Apr 13 2020 Shreenidhi Shedi <sshedi@vmware.com> 3.4.1-1
-   Upgrade to version 3.4.1
*   Wed Mar 21 2018 Xiaolin Li <xiaolinl@vmware.com> 3.3-1
-   Update to 3.3, fix CVE-2016-6489
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.2-2
-   GA - Bump release of all rpms
*   Mon Feb 22 2016 XIaolin Li <xiaolinl@vmware.com> 3.2-1
-   Updated to version 3.2
*   Mon Oct 12 2015 Xiaolin Li <xiaolinl@vmware.com> 3.1.1-2
-   Moving static lib files to devel package.
*   Thu Jun 18 2015 Divya Thaluru <dthaluru@vmware.com> 3.1.1-1
-   Initial build. First version
