Summary:        SELinux library and simple utilities
Name:           libselinux
Version:        3.5
Release:        3%{?dist}
Group:          System Environment/Libraries
Url:            https://github.com/SELinuxProject/selinux/wiki
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        https://github.com/SELinuxProject/selinux/releases/download/%{version}/%{name}-%{version}.tar.gz
%define sha512  %{name}=4e13261a5821018a5f3cdce676f180bb62e5bc225981ca8a498ece0d1c88d9ba8eaa0ce4099dd0849309a8a7c5a9a0953df841a9922f2c284e5a109e5d937ba7

Source1: license.txt
%include %{SOURCE1}

Patch0:         Add-Wno-error-stringop-truncation-to-EXTRA_CFLAGS.patch

BuildRequires:  libsepol-devel = %{version}
BuildRequires:  pcre2-devel
BuildRequires:  swig
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-pip

# this is not really needed to build libselinux
# this is added to avoid a build failure while forming chroot
BuildRequires: util-linux-devel

%define ExtraBuildRequires systemd-rpm-macros

Requires:       pcre2-libs
# libselinux optionally uses libsepol by dlopen it.
# libsepol really needed by highlevel SELinux packages
# such as policycoreutils.
# But libselinux is needed (dynamic linking) by systemd,
# coreutils, pam even if SELinux is disabled,
# just because they were dinamically linked against it.
# Disable libsepol dependency to reduce minimal installation
# size. And install libsepol when we really need SELinux
#Requires:      libsepol

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

libselinux provides an API for SELinux applications to get and set
process and file security contexts and to obtain security policy
decisions.  Required for any applications that use the SELinux API.

%package        utils
Summary:        SELinux libselinux utilies
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description    utils
The libselinux-utils package contains the utilities

%package        devel
Summary:        Header files and libraries used to build SELinux
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       libsepol-devel = %{version}
Requires:       pcre2-devel
Provides:       pkgconfig(%{name})

%description    devel
The libselinux-devel package contains the libraries and header files
needed for developing SELinux applications.

%package        python3
Summary:        SELinux python3 bindings for libselinux
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       python3

%description    python3
The libselinux-python package contains the python3 bindings for developing
SELinux applications.

%prep
%autosetup -p1

%build
%make_build

%install
%make_install %{?_smp_mflags} install install-pywrap \
        SHLIBDIR="%{_libdir}"

mkdir -p %{buildroot}%{_tmpfilesdir}
echo "d /run/setrans 0755 root root" > %{buildroot}%{_tmpfilesdir}/%{name}.conf

rm -rf %{buildroot}%{_mandir}/ru \
       %{buildroot}%{_libdir}/%{name}.a

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%ghost /run/setrans
%{_libdir}/%{name}.so.1
%{_tmpfilesdir}/%{name}.conf

%files utils
%defattr(-,root,root,-)
%{_sbindir}/*
%{_mandir}/man5/*
%{_mandir}/man8/*

%files devel
%defattr(-,root,root,-)
%{_libdir}/%{name}.so
%{_libdir}/pkgconfig/*
%dir %{_includedir}/selinux
%{_includedir}/selinux/*
%{_mandir}/man3/*

%files python3
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
* Tue Nov 05 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 3.5-3
- Release bump for SRP compliance
* Thu Jan 12 2023 Him Kalyan Bordoloi <bordoloih@vmware.com> 3.4-3
- Bump up version no. as part of swig upgrade
* Tue Dec 06 2022 Prashant S Chauhan <psinghchauha@vmware.com> 3.4-2
- Update release to compile with python 3.11
* Sun Aug 21 2022 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 3.4-1
- Upgrade v3.4
* Fri Apr 08 2022 Shreenidhi Shedi <sshedi@vmware.com> 3.3-1
- Upgrade v3.3
* Tue Apr 13 2021 Gerrit Photon <photon-checkins@vmware.com> 3.2-1
- Automatic Version Bump
* Thu Jul 23 2020 Gerrit Photon <photon-checkins@vmware.com> 3.1-1
- Automatic Version Bump
* Mon Jun 22 2020 Tapas Kundu <tkundu@vmware.com> 3.0-3
- Mass removal python2
* Fri Apr 24 2020 Alexey Makhalov <amakhalov@vmware.com> 3.0-2
- Remove libsepol runtime dependency.
* Sat Apr 18 2020 Alexey Makhalov <amakhalov@vmware.com> 3.0-1
- Version update.
* Wed Mar 25 2020 Alexey Makhalov <amakhalov@vmware.com> 2.8-3
- Fix compilation issue with glibc >= 2.30.
* Tue Jan 08 2019 Alexey Makhalov <amakhalov@vmware.com> 2.8-2
- Added BuildRequires python2-devel
* Fri Aug 10 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 2.8-1
- Update to version 2.8 to get it to build with gcc 7.3
* Thu Aug 24 2017 Alexey Makhalov <amakhalov@vmware.com> 2.6-4
- Fix compilation issue for glibc-2.26
* Wed May 31 2017 Xiaolin Li <xiaolinl@vmware.com> 2.6-3
- Include pytho3 packages.
* Mon May 22 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 2.6-2
- Include python subpackage.
* Wed May 03 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 2.6-1
- Upgraded to version 2.6
* Tue May 02 2017 Anish Swaminathan <anishs@vmware.com> 2.5-3
- Remove pcre requires and add requires on pcre-libs
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.5-2
- GA - Bump release of all rpms
* Fri Jan 22 2016 Xiaolin Li <xiaolinl@vmware.com> 2.5-1
- Updated to version 2.5
* Wed Feb 25 2015 Divya Thaluru <dthaluru@vmware.com> 2.4-1
- Initial build.  First version
