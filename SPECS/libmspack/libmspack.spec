Summary:        A library that provides compression and decompression of file formats used by Microsoft
Name:           libmspack
Version:        0.5alpha
Release:        6%{?dist}
License:        LGPLv2+
URL:            http://www.cabextract.org.uk/libmspack/libmspack-0.5alpha.tar.gz
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        http://www.cabextract.org.uk/libmspack/%{name}-%{version}.tar.gz
%define sha1    libmspack=226f19b1fc58e820671a1749983b06896e108cc4
Patch0:         CVE-2017-6419.patch
Patch1:         CVE-2017-11423.patch
Patch2:         CVE-2018-14679-CVE-2018-14680.patch
%description
A library that provides compression and decompression of file formats used by Microsoft

%package        devel
Summary:        Header and development files for libmspack
Requires:       %{name} = %{version}-%{release}
%description    devel
It contains the libraries and header files to create applications.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%build
./configure --prefix=/usr
make %{?_smp_mflags}
%install
make DESTDIR=%{buildroot} install
find %{buildroot}/usr/lib/ -name '*.la' -delete

%check
cd test
./cabd_test

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files 
%defattr(-,root,root)
%{_libdir}/*.so.*

%files  devel
%{_libdir}/pkgconfig/*.pc
%{_includedir}/*
%{_libdir}/*.a
%{_libdir}/*.so

%changelog
*   Fri Nov 16 2018 Sujay G <gsujay@vmware.com> 0.5alpha-6
-   Patch for CVE-2018-14679 & CVE-2018-14680
*   Mon Jul 16 2018 Ajay Kaher <akaher@vmware.com> 0.5alpha-5
-   Patch for CVE-2017-11423
*   Mon May 21 2018 Anish Swaminathan <anishs@vmware.com> 0.5alpha-4
-   Patch for CVE-2017-6419
*   Fri Jun 23 2017 Xiaolin Li <xiaolinl@vmware.com> 0.5alpha-3
-   Add devel package.
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.5alpha-2
-   GA - Bump release of all rpms
*   Fri Jan 22 2016 Xiaolin Li <xiaolinl@vmware.com> 0.5-1
-   Updated to version 0.5
*   Thu Nov 06 2014 Sharath George <sharathg@vmware.com> 0.4-1
    Initial version
