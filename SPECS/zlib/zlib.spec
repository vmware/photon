Summary:        Compression and decompression routines
Name:           zlib
Version:        1.2.13
Release:        4%{?dist}
URL:            http://www.zlib.net
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: http://www.zlib.net/%{name}-%{version}.tar.xz
%define sha512 %{name}=9e7ac71a1824855ae526506883e439456b74ac0b811d54e94f6908249ba8719bec4c8d7672903c5280658b26cb6b5e93ecaaafe5cdc2980c760fa196773f0725

Source1: license.txt
%include %{SOURCE1}

Patch0:       CVE-2023-45853.patch

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
if [ %{_host} != %{_build} ]; then
  export CC=%{_host}-gcc
  export CXX=%{_host}-g++
  export AR=%{_host}-ar
  export AS=%{_host}-as
  export RANLIB=%{_host}-ranlib
  export LD=%{_host}-ld
  export STRIP=%{_host}-strip
fi

sh ./configure \
    --prefix=%{_prefix} \
    --shared

%make_build

%install
%make_install %{?_smp_mflags}

%if 0%{?with_check}
%check
make %{?_smp_mflags} check
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
* Wed Dec 11 2024 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 1.2.13-4
- Release bump for SRP compliance
* Tue Sep 24 2024 Mukul Sikka <mukul.sikka@broadcom.com> 1.2.13-3
- Bump version to generate SRP provenance file
* Wed Oct 25 2023 Harinadh D <hdommaraju@vmware.com> 1.2.13-2
- fix CVE-2023-45853
* Fri Apr 14 2023 Shreenidhi Shedi <sshedi@vmware.com> 1.2.13-1
- Upgrade to v1.2.13
* Thu Nov 15 2018 Alexey Makhalov <amakhalov@vmware.com> 1.2.11-2
- Cross compilation support
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
