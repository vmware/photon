Summary:        Compression and decompression routines
Name:           zlib
Version:        1.2.11
Release:        5%{?dist}
URL:            http://www.zlib.net
License:        zlib
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: http://www.zlib.net/%{name}-%{version}.tar.xz
%define sha512  zlib=b7f50ada138c7f93eb7eb1631efccd1d9f03a5e77b6c13c8b757017b2d462e19d2d3e01c50fad60a4ae1bc86d431f6f94c72c11ff410c25121e571953017cb67

Patch0: CVE-2018-25032-1.patch
Patch1: CVE-2018-25032-2.patch
Patch2: CVE-2022-37434.patch
Patch3: CVE-2023-45853.patch

%description
Compression and decompression routines

%package    devel
Summary:    Header and development files for zlib
Requires:   %{name} = %{version}-%{release}

%description    devel
It contains the libraries and header files to create applications
for handling compiled objects.

%prep
%autosetup -p1

%build
sh ./configure \
    --prefix=%{_prefix} \
    --shared

%make_build

%install
%make_install %{?_smp_mflags}

%if 0%{?with_check}
%check
%make_build check
%endif

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_libdir}/libz.so.*

%files devel
%defattr(-,root,root)
%{_includedir}/zconf.h
%{_includedir}/zlib.h
%{_libdir}/pkgconfig/zlib.pc
%{_libdir}/libz.a
%{_libdir}/libz.so
%{_mandir}/man3/zlib.3.gz

%changelog
* Wed Oct 25 2023 Harinadh D <hdommaraju@vmware.com> 1.2.11-5
- Fix CVE-2023-45853
* Mon Jul 17 2023 Shreenidhi Shedi <sshedi@vmware.com> 1.2.11-4
- Fix devel package requires
* Tue Aug 16 2022 Shivani Agarwal <shivania2@vmware.com> 1.2.11-3
- Fix for CVE-2022-37434
* Mon Apr 04 2022 Shivani Agarwal <shivania2@vmware.com> 1.2.11-2
- Fix for CVE-2018-25032
* Wed Apr 05 2017 Xiaolin Li <xiaolinl@vmware.com> 1.2.11-1
- Updated to version 1.2.11.
* Wed Dec 07 2016 Xiaolin Li <xiaolinl@vmware.com> 1.2.8-5
- Moved man3 to devel subpackage.
* Wed Oct 05 2016 ChangLee <changlee@vmware.com> 1.2.8-4
- Modified %check
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.2.8-3
- GA - Bump release of all rpms
* Mon May 18 2015 Touseef Liaqat <tliaqat@vmware.com> 1.2.8-2
- Update according to UsrMove.
* Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 1.2.8-1
- Initial build. First version
