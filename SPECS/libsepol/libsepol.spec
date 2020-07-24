Summary:        SELinux binary policy manipulation library
Name:           libsepol
Version:        3.1
Release:        1%{?dist}
License:        LGPLv2+
Group:          System Environment/Libraries
Source0:        https://github.com/SELinuxProject/selinux/releases/download/20200710/%{name}-%{version}.tar.gz
%define sha1    libsepol=7f209aae19fdb2da3721a1fe0758c5dc9fc0a866
URL:            http://www.selinuxproject.org
Vendor:         VMware, Inc.
Distribution:   Photon

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
Requires:       libsepol = %{version}-%{release}

%description    utils
The libsepol-utils package contains the utilities

%package	devel
Summary:	Header files and libraries used to build policy manipulation tools
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Provides:	pkgconfig(libsepol)

%description	devel
The libsepol-devel package contains the libraries and header files
needed for developing applications that manipulate binary policies.

%prep
%setup -q

%build
make %{?_smp_mflags}
# TODO: try to remove CFLAGS on next version update
#make %{?_smp_mflags} CFLAGS="-Werror -Wall -W -Wundef -Wshadow -Wmissing-format-attribute -O2 -Wno-error=stringop-truncation"

%install
mkdir -p %{buildroot}/%{_lib}
mkdir -p %{buildroot}/%{_libdir}
mkdir -p %{buildroot}%{_includedir}
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_mandir}/man3
mkdir -p %{buildroot}%{_mandir}/man8
make DESTDIR="%{buildroot}" LIBDIR="%{_libdir}" SHLIBDIR="/%{_lib}" install
# do not package ru man page and man pages for missing tools
rm -rf %{buildroot}%{_mandir}/ru
rm %{buildroot}%{_mandir}/man8/genpolbools.8
rm %{buildroot}%{_mandir}/man8/genpolusers.8


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
%{_bindir}/chkcon
%{_mandir}/man8/chkcon.8.gz

%files
%defattr(-,root,root)
%{_lib}/libsepol.so.1

%changelog
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
