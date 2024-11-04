Summary:        SELinux binary policy manipulation library
Name:           libsepol
Version:        3.4
Release:        3%{?dist}
Group:          System Environment/Libraries
URL:            http://www.selinuxproject.org
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://github.com/SELinuxProject/selinux/releases/download/%{version}/%{name}-%{version}.tar.gz
%define sha512 %{name}=5e47e6ac626f2bfc10a9f2f24c2e66c4d7f291ca778ebd81c7d565326e036e821d3eb92e5d7540517b1c715466232a7d7da895ab48811d037ad92d423ed934b6

Source1: license.txt
%include %{SOURCE1}

Patch0: fix-validation-of-user.patch

%description
Security-enhanced Linux is a feature of the Linux® kernel and a number
of utilities with enhanced security functionality designed to add
mandatory access controls to Linux.  The Security-enhanced Linux
kernel contains new architectural components originally developed to
improve the security of the Flask operating system. These
architectural components provide general support for the enforcement
of many kinds of mandatory access control policies, including those
based on the concepts of Type Enforcement®, Role-based Access
Control, and Multi-level Security.

libsepol provides an API for the manipulation of SELinux binary policies.
It is used by checkpolicy (the policy compiler) and similar tools, as well
as by programs like load_policy that need to perform specific transformations
on binary policies such as customizing policy boolean settings.

%package        utils
Summary:        SELinux libsepol utilies
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description    utils
The libsepol-utils package contains the utilities

%package    devel
Summary:    Header files and libraries used to build policy manipulation tools
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}
Provides:   pkgconfig(libsepol)

%description    devel
The libsepol-devel package contains the libraries and header files
needed for developing applications that manipulate binary policies.

%prep
%autosetup -p1

%build
# TODO: try to remove CFLAGS on next version update
export CFLAGS="-Werror -Wall -W -Wundef -Wshadow -Wmissing-format-attribute -O2 -fno-semantic-interposition -Wno-error=stringop-truncation"
make %{?_smp_mflags}

%install
mkdir -p %{buildroot}%{_libdir} \
         %{buildroot}%{_includedir} \
         %{buildroot}%{_bindir} \
         %{buildroot}%{_mandir}/man3 \
         %{buildroot}%{_mandir}/man8

make %{?_smp_mflags} DESTDIR="%{buildroot}" LIBDIR="%{_libdir}" SHLIBDIR="%{_lib}" install
# do not package ru man page and man pages for missing tools
rm -rf %{buildroot}%{_mandir}/ru \
       %{buildroot}%{_mandir}/man8/genpolbools.8 \
       %{buildroot}%{_mandir}/man8/genpolusers.8

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files devel
%defattr(-,root,root)
%{_libdir}/libsepol.so
%{_libdir}/libsepol.a
%{_libdir}/pkgconfig/libsepol.pc
%dir %{_includedir}/sepol
%dir %{_includedir}/sepol/policydb
%{_includedir}/sepol/policydb/*.h
%{_includedir}/sepol/*.h
%{_includedir}/sepol/cil/*.h
%{_mandir}/man3/*.3.gz

%files utils
%defattr(-,root,root)
%{_bindir}/*
%{_mandir}/man8/chkcon.8.gz

%files
%defattr(-,root,root)
%{_libdir}/libsepol.so.*

%changelog
* Tue Nov 05 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 3.4-3
- Release bump for SRP compliance
* Fri Sep 16 2022 Shreenidhi Shedi <sshedi@vmware.com> 3.4-2
- Fix user validation
* Sun Aug 21 2022 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 3.4-1
- Upgrade v3.4
* Fri Apr 08 2022 Shreenidhi Shedi <sshedi@vmware.com> 3.3-1
- Upgrade v3.3
* Tue Mar 08 2022 Alexey Makhalov <amakhalov@vmware.com> 3.2-2
- Fix CVE-2021-36084, CVE-2021-36085, CVE-2021-36086
* Tue Apr 13 2021 Gerrit Photon <photon-checkins@vmware.com> 3.2-1
- Automatic Version Bump
* Tue Jan 12 2021 Alexey Makhalov <amakhalov@vmware.com> 3.1-2
- GCC-10 support
* Thu Jul 23 2020 Gerrit Photon <photon-checkins@vmware.com> 3.1-1
- Automatic Version Bump
* Sat Apr 18 2020 Alexey Makhalov <amakhalov@vmware.com> 3.0-1
- Version update.
- Added -utils subpackage.
- Remove systemd dependency.
* Fri Aug 10 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 2.8-1
- Update to version 2.8 to get it to build with gcc 7.3
* Tue Apr 04 2017 Kumar Kaushik <kaushikk@vmware.com> 2.6-1
- Updating version to 2.6
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.5-2
- GA - Bump release of all rpms
* Fri Jan 22 2016 Xiaolin Li <xiaolinl@vmware.com> 2.5-1
- Updated to version 2.5
* Wed Feb 25 2015 Divya Thaluru <dthaluru@vmware.com> 2.4-1
- Initial build. First version
