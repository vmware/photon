Summary:    Low level cryptographic libraries
Name:       nettle
Version:    3.9.1
Release:    1%{?dist}
License:    LGPLv3+ or GPLv2+
URL:        http://www.lysator.liu.se/~nisse/nettle
Group:      Development/Libraries
Vendor:     VMware, Inc.
Distribution:   Photon

Source0: https://ftp.gnu.org/gnu/nettle/%{name}-%{version}.tar.gz
%define sha512 %{name}=5939c4b43cf9ff6c6272245b85f123c81f8f4e37089fa4f39a00a570016d837f6e706a33226e4bbfc531b02a55b2756ff312461225ed88de338a73069e031ced

Provides:   libhogweed.so.6()(64bit)
Provides:   libhogweed.so.6(HOGWEED_6)(64bit)
Provides:   libhogweed.so.6(HOGWEED_INTERNAL_6_0)(64bit)
Provides:   libnettle.so.8()(64bit)
Provides:   libnettle.so.8(NETTLE_8)(64bit)
Provides:   libnettle.so.8(NETTLE_INTERNAL_8_0)(64bit)

Requires:   gmp

%description
GNettle is a cryptographic library that is designed to fit easily in more
or less any context: In crypto toolkits for object-oriented languages
(C++, Python, Pike, ...), in applications like LSH or GNUPG, or even in
kernel space.

%package    devel
Summary:    Development libraries and header files for nettle
Requires:   %{name} = %{version}-%{release}
Provides:   pkgconfig(hogweed)
Provides:   pkgconfig(nettle)

%description devel
The package contains libraries and header files for
developing applications that use nettle.

%prep
%autosetup -p1

%build
%configure --enable-shared --disable-static
%make_build

%install
%make_install %{?_smp_mflags}
rm %{buildroot}%{_infodir}/*

%check
%make_build check

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

%changelog
* Fri Nov 24 2023 Shreenidhi Shedi <sshedi@vmware.com> 3.9.1-1
- Upgrade to v3.9.1
* Wed Aug 24 2022 Shreenidhi Shedi <sshedi@vmware.com> 3.8.1-1
- Upgrade to v3.8.1
* Tue Aug 17 2021 Shreenidhi Shedi <sshedi@vmware.com> 3.7.3-1
- Bump to version 3.7.3 to fix CVE-2021-3580
* Tue Apr 13 2021 Gerrit Photon <photon-checkins@vmware.com> 3.7.2-1
- Automatic Version Bump
* Mon Aug 17 2020 Shreenidhi Shedi <sshedi@vmware.com> 3.6-1
- Upgrade to version 3.6
* Thu Oct 17 2019 Shreenidhi Shedi <sshedi@vmware.com> 3.4.1-1
- Upgrade to version 3.4.1
* Thu Sep 06 2018 Anish Swaminathan <anishs@vmware.com> 3.4-1
- Update version to 3.4
* Sat Apr 15 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.3-1
- Update to 3.3
* Tue Oct 04 2016 ChangLee <changLee@vmware.com> 3.2-3
- Modified %check
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.2-2
- GA - Bump release of all rpms
* Mon Feb 22 2016 XIaolin Li <xiaolinl@vmware.com> 3.2-1
- Updated to version 3.2
* Mon Oct 12 2015 Xiaolin Li <xiaolinl@vmware.com> 3.1.1-2
- Moving static lib files to devel package.
* Thu Jun 18 2015 Divya Thaluru <dthaluru@vmware.com> 3.1.1-1
- Initial build. First version
