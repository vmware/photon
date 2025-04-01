Summary:        library for fast, message-based applications
Name:           zeromq
Version:        4.3.4
Release:        3%{?dist}
URL:            http://www.zeromq.org
License:        LGPLv3+
Group:          System Environment/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        https://github.com/zeromq/libzmq/releases/download/v%{version}/%{name}-%{version}.tar.gz
%define sha512 %{name}=e198ef9f82d392754caadd547537666d4fba0afd7d027749b3adae450516bcf284d241d4616cad3cb4ad9af8c10373d456de92dc6d115b037941659f141e7c0e

Requires:       libstdc++

%description
The 0MQ lightweight messaging kernel is a library which extends the standard
socket interfaces with features traditionally provided by specialised messaging
middleware products. 0MQ sockets provide an abstraction of asynchronous message
queues, multiple messaging patterns, message filtering (subscriptions), seamless
access to multiple transport protocols and more.

%package        devel
Summary:        Header and development files for zeromq
Requires:       %{name} = %{version}-%{release}
%description    devel
It contains the libraries and header files to create applications

%prep
%autosetup -p1

%build
%configure \
    --with-libsodium=no \
    --disable-Werror \
    --disable-static \
    --disable-libbsd

%make_build

%install
%make_install %{?_smp_mflags}
find %{buildroot}%{_libdir} -name '*.la' -delete

%check
%make_build check

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%doc AUTHORS ChangeLog COPYING COPYING.LESSER NEWS
%{_bindir}/*
%{_libdir}/libzmq.so.*

%files devel
%defattr(-,root,root,-)
%{_libdir}/libzmq.so
%{_libdir}/pkgconfig/libzmq.pc
%{_includedir}/
%{_mandir}/*

%changelog
* Fri Apr 18 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 4.3.4-3
- Fix build with newer glibc
* Fri Aug 19 2022 Ajay Kaher <akaher@vmware.com> 4.3.4-2
- fix: build fails with gcc 12
* Fri Jul 09 2021 Nitesh Kumar <kunitesh@vmware.com> 4.3.4-1
- Upgrade to 4.3.4
* Thu Sep 10 2020 Gerrit Photon <photon-checkins@vmware.com> 4.3.3-1
- Automatic Version Bump
* Thu Jun 25 2020 Gerrit Photon <photon-checkins@vmware.com> 4.3.2-1
- Automatic Version Bump
* Mon Jul 22 2019 Siju Maliakkal <smaliakkal@vmware.com> 4.2.3-2
- Apply patch for CVE-2019-13132
* Thu Sep 13 2018 Siju Maliakkal <smaliakkal@vmware.com> 4.2.3-1
- Updated to latest version
* Fri Sep 15 2017 Bo Gan <ganb@vmware.com> 4.1.4-3
- Remove devpts mount
* Mon Aug 07 2017 Chang Lee <changlee@vmware.com> 4.1.4-2
- Fixed %check
* Thu Apr 13 2017 Dheeraj Shetty <dheerajs@vmware.com> 4.1.4-1
- Initial build. First version
