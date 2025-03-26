Summary:        Libraries for Transport Independent RPC
Name:           libtirpc
Version:        1.3.3
Release:        4%{?dist}
Group:          System Environment/Libraries
URL:            http://nfsv4.bullopensource.org/
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: http://downloads.sourceforge.net/project/libtirpc/libtirpc/0.3.2/%{name}-%{version}.tar.bz2

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  krb5-devel
BuildRequires:  e2fsprogs-devel

Requires:       krb5

%description
This package contains SunLib's implementation of transport-independent
RPC (TI-RPC) documentation.  This library forms a piece of the base of Open Network
Computing (ONC), and is derived directly from the Solaris 2.3 source.

TI-RPC is an enhanced version of TS-RPC that requires the UNIX System V
Transport Layer Interface (TLI) or an equivalent X/Open Transport Interface
(XTI).  TI-RPC is on-the-wire compatible with the TS-RPC, which is supported
by almost 70 vendors on all major operating systems.  TS-RPC source code
(RPCSRC 4.0) remains available from several internet sites.

%package        devel
Summary:        Development files for the libtirpc library
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       krb5-devel

%description    devel
This package includes header files and libraries necessary for developing programs which use the tirpc library.

%prep
%autosetup -p1

%build
%configure
sed '/stdlib.h/a#include <stdint.h>' -i src/xdr_sizeof.c

%make_build

%install
%make_install %{?_smp_mflags}

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/netconfig
%config(noreplace) %{_sysconfdir}/bindresvport.blacklist
%{_mandir}/man5/*
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root)
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_includedir}/tirpc/*
%{_mandir}/man3/*
%{_libdir}/*.a

%changelog
* Wed Dec 11 2024 Mukul Sikka <mukul.sikka@broadcom.com> 1.3.3-4
- Release bump for SRP compliance
* Fri Jul 28 2023 Srish Srinivasan <ssrish@vmware.com> 1.3.3-3
- Bump version as a part of krb5 upgrade
* Thu Jan 26 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 1.3.3-2
- Bump version as a part of krb5 upgrade
* Thu Sep 29 2022 Gerrit Photon <photon-checkins@vmware.com> 1.3.3-1
- Automatic Version Bump
* Tue Sep 20 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.3.2-2
- Remove .la files
* Mon Apr 18 2022 Gerrit Photon <photon-checkins@vmware.com> 1.3.2-1
- Automatic Version Bump
* Tue Apr 13 2021 Gerrit Photon <photon-checkins@vmware.com> 1.3.1-1
- Automatic Version Bump
* Wed Jul 08 2020 Gerrit Photon <photon-checkins@vmware.com> 1.2.6-1
- Automatic Version Bump
* Thu Nov 15 2018 Alexey Makhalov <amakhalov@vmware.com> 1.1.4-2
- Cross compilation support
* Wed Sep 12 2018 Keerthana K <keerthanak@vmware.com> 1.1.4-1
- Update to version 1.1.4
* Thu Aug 24 2017 Alexey Makhalov <amakhalov@vmware.com> 1.0.1-7
- Fix compilation issue for glibc-2.26
* Thu May 18 2017 Vinay Kulkarni <kulkarniv@vmware.com> 1.0.1-6
- Fix CVE-2017-8779
* Wed Dec 07 2016 Xiaolin Li <xiaolinl@vmware.com> 1.0.1-5
- Moved man3 to devel subpackage.
* Thu Nov 24 2016 Alexey Makhalov <amakhalov@vmware.com> 1.0.1-4
- Required krb5-devel.
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.0.1-3
- GA - Bump release of all rpms
* Mon Feb 08 2016 Anish Swaminathan <anishs@vmware.com>  1.0.1-2
- Added patch for bindresvport denylist
* Fri Jan 15 2016 Xiaolin Li <xiaolinl@vmware.com> 1.0.1-1
- Updated to version 1.0.1
* Thu Jul 23 2015 Divya Thaluru <dthaluru@vmware.com> 0.3.2-1
- Initial version.
