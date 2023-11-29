Summary:    RELP Library
Name:       librelp
Version:    1.10.0
Release:    5%{?dist}
License:    GPLv3+
URL:        http://www.librelp.com
Group:      System Environment/Libraries
Vendor:     VMware, Inc.
Distribution:   Photon

Source0: http://download.rsyslog.com/librelp/%{name}-%{version}.tar.gz
%define sha512 %{name}=a38840231902bec034edb497166deded7577c989e4f735e406c8488384972925de1ca6132b3080472f7919d2439559c8774c02a49c356e90ad791dfbba2a4865

BuildRequires:  gnutls-devel
BuildRequires:  autogen

Requires:   gnutls

%description
Librelp is an easy to use library for the RELP protocol. RELP (stands
for Reliable Event Logging Protocol) is a general-purpose, extensible
logging protocol.

%package devel
Summary:    Development libraries and header files for librelp
Requires:   %{name} = %{version}-%{release}

%description devel
The package contains libraries and header files for
developing applications that use librelp.

%prep
%autosetup
autoreconf -fiv

%build
%configure
%make_build

%install
%make_install %{?_smp_mflags}

%if 0%{?with_check}
%check
#There are two tests(out of 16) which run under valgrind.
#Currently these two tests just greps for a message output after test.
#If we need to enable valgrind, it needs 'unstripped' version of ld.so
#This is available in glibc-debuginfo which needs to be installed in
#sandbox environment. This needs tdnf package which in turn needs to
#install glibc-debuginfo package (which has unstripped version of ld.so).
#Due to above dependecy overhead which needs more analysis
#and since tests are not using any valgrind functionality,
#disabling valgrind.
sed -i '/VALGRIND_TESTS= \\/d' tests/Makefile.am
sed -i '/duplicate-receiver-vg.sh \\/d' tests/Makefile.am
sed -i '/basic-sessionbreak-vg.sh/d' tests/Makefile.am

make check %{?_smp_mflags}
%endif

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root)
%{_libdir}/*.a
%{_includedir}/*.h
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%changelog
* Wed Nov 29 2023 Shreenidhi Shedi <sshedi@vmware.com> 1.10.0-5
- Bump version as a part of gnutls upgrade
* Tue Sep 13 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.10.0-4
- Remove .la files
* Tue Aug 30 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.10.0-3
- Bump version as a part of gnutls upgrade
* Wed Aug 04 2021 Satya Naga Vasamsetty <svasamsetty@vmware.com> 1.10.0-2
- Bump up release for openssl
* Tue Apr 13 2021 Gerrit Photon <photon-checkins@vmware.com> 1.10.0-1
- Automatic Version Bump
* Tue Nov 24 2020 Shreenidhi Shedi <sshedi@vmware.com> 1.8.0-2
- Fix make check
* Tue Sep 29 2020 Gerrit Photon <photon-checkins@vmware.com> 1.8.0-1
- Automatic Version Bump
* Tue Sep 01 2020 Gerrit Photon <photon-checkins@vmware.com> 1.7.0-1
- Automatic Version Bump
* Mon Jun 22 2020 Shreenidhi Shedi <sshedi@vmware.com> 1.6.0-1
- Upgrade to version 1.6.0
* Mon Aug 19 2019 Shreenidhi Shedi <sshedi@vmware.com> 1.2.17-3
- Further fix for make check
* Tue Nov 20 2018 Ashwin H <ashwinh@vmware.com> 1.2.17-2
- Fix librelp %check
* Tue Sep 11 2018 Keerthana K <keerthanak@vmware.com> 1.2.17-1
- Updated to version 1.2.17
* Tue Apr 11 2017 Harish Udaiy Kumar <hudaiyakumar@vmware.com> 1.2.13-1
- Updated to version 1.2.13
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.2.9-2
- GA - Bump release of all rpms
* Thu Feb 25 2016 Anish Swaminathan <anishs@vmware.com>  1.2.9-1
- Upgrade to 1.2.9
* Thu Jun 18 2015 Divya Thaluru <dthaluru@vmware.com> 1.2.7-1
- Initial build. First version
