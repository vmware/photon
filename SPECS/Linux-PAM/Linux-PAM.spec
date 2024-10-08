Summary:        Linux Pluggable Authentication Modules
Name:           Linux-PAM
Version:        1.6.1
Release:        2%{?dist}
License:        BSD and GPLv2+
URL:            https://github.com/linux-pam/linux-pam
Group:          System Environment/Security
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://github.com/linux-pam/linux-pam/releases/download/v%{version}/%{name}-%{version}.tar.xz
%define sha512 %{name}=ddb5a5f296f564b76925324550d29f15d342841a97815336789c7bb922a8663e831edeb54f3dcd1eaf297e3325c9e2e6c14b8740def5c43cf3f160a8a14fa2ea

Source1: pamtmp.conf
Source2: default-faillock.conf

Patch0: 0001-faillock-add-support-to-print-login-failures.patch

BuildRequires:  libselinux-devel
BuildRequires:  gdbm-devel
BuildRequires:  libxcrypt-devel

Requires: libselinux
Requires: gdbm
Requires: libxcrypt

%define ExtraBuildRequires systemd-rpm-macros

%description
The Linux PAM package contains Pluggable Authentication Modules used to
enable the local system administrator to choose how applications authenticate users.

%package        lang
Summary:        Additional language files for Linux-PAM
Group:          System Environment/Base
Requires:       %{name} = %{version}-%{release}

%description    lang
These are the additional language files of Linux-PAM.

%package        devel
Summary:        Development files for Linux-PAM
Group:          System Environment/Base
Requires:       %{name} = %{version}-%{release}

%description    devel
The Linux-PAM-devel package contains libraries, header files and documentation
for developing applications that use Linux-PAM.

%prep
%autosetup -p1

%build
sh ./configure --host=%{_host} --build=%{_build} \
    $(test %{_host} != %{_build} && echo "--with-sysroot=/target-%{_arch}") \
    CFLAGS="%{optflags}" \
    CXXFLAGS="%{optflags}" \
    --disable-dependency-tracking \
    --prefix=%{_prefix} \
    --exec-prefix=%{_prefix} \
    --bindir=%{_bindir} \
    --sbindir=%{_sbindir} \
    --sysconfdir=%{_sysconfdir} \
    --datadir=%{_datadir} \
    --includedir=%{_includedir}/security \
    --libdir=%{_libdir} \
    --libexecdir=%{_libexecdir} \
    --localstatedir=%{_localstatedir} \
    --sharedstatedir=%{_sharedstatedir} \
    --mandir=%{_mandir} \
    --infodir=%{_infodir} \
    --enable-selinux \
    --docdir=%{_docdir}/%{name}-%{version} \
    --enable-securedir=%{_libdir}/security \
    --enable-db=ndbm

%make_build

%install
%make_install %{?_smp_mflags}
chmod -v 4755 %{buildroot}%{_sbindir}/unix_chkpwd
install -v -dm755 %{buildroot}%{_docdir}/%{name}-%{version}
ln -sfv pam_unix.so %{buildroot}%{_libdir}/security/pam_unix_auth.so
ln -sfv pam_unix.so %{buildroot}%{_libdir}/security/pam_unix_acct.so
ln -sfv pam_unix.so %{buildroot}%{_libdir}/security/pam_unix_passwd.so
ln -sfv pam_unix.so %{buildroot}%{_libdir}/security/pam_unix_session.so

cp %{SOURCE2} %{buildroot}%{_sysconfdir}/security/faillock.conf

install -d -m 755 %{buildroot}/run/faillock
install -m644 -D %{SOURCE1} %{buildroot}%{_tmpfilesdir}/pam.conf

%{find_lang} %{name}

%{_fixperms} %{buildroot}/*

%check
install -v -m755 -d %{_sysconfdir}/pam.d
cat > %{_sysconfdir}/pam.d/other << "EOF"
auth     required       pam_deny.so
account  required       pam_deny.so
password required       pam_deny.so
session  required       pam_deny.so
EOF
%make_build check

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/security/*.conf
%attr(755,root,root) %config(noreplace) %{_sysconfdir}/security/namespace.init
%dir %{_sysconfdir}/security
%{_sysconfdir}/environment
%{_sbindir}/*
%{_libdir}/security/*
%{_libdir}/*.so.*
%{_mandir}/man5/*
%{_mandir}/man8/*
%{_tmpfilesdir}/pam.conf
%{_unitdir}/pam_namespace.service
%dir /run/faillock

%files lang -f Linux-PAM.lang
%defattr(-,root,root)

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/*.so
%{_mandir}/man3/*
%{_docdir}/%{name}-%{version}/*
%{_libdir}/pkgconfig/*.pc

%changelog
* Tue Oct 15 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.6.1-2
- Bump version to use yescrypt
* Mon Jun 03 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.6.1-1
- Upgrade to v1.6.1
* Wed May 17 2023 Shreenidhi Shedi <sshedi@vmware.com> 1.5.3-1
- Upgrade to v1.5.3
* Mon Nov 07 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.5.2-3
- Add a default faillock.conf
* Wed Jul 06 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.5.2-2
- Remove libdb support from pam
* Thu Jun 30 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.5.2-1
- Further fixes to faillock patch
- Upgrade to v1.5.2
* Tue Mar 08 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.5.1-2
- create /var/run/faillock during install
* Mon Apr 12 2021 Gerrit Photon <photon-checkins@vmware.com> 1.5.1-1
- Automatic Version Bump
* Fri Sep 25 2020 Ankit Jain <ankitja@vmware.com> 1.4.0-2
- pam_cracklib has been deprecated.
* Fri Aug 07 2020 Vikash Bansal <bvikas@vmware.com> 1.4.0-1
- Version bump up to 1.4.0
* Mon Apr 20 2020 Alexey Makhalov <amakhalov@vmware.com> 1.3.0-3
- Enable SELinux support
* Thu Nov 15 2018 Alexey Makhalov <amakhalov@vmware.com> 1.3.0-2
- Cross compilation support
* Fri Apr 14 2017 Alexey Makhalov <amakhalov@vmware.com> 1.3.0-1
- Version update.
* Fri Feb 10 2017 Xiaolin Li <xiaolinl@vmware.com> 1.2.1-5
- Added pam_unix_auth.so, pam_unix_acct.so, pam_unix_passwd.so,
- and pam_unix_session.so.
* Wed Dec 07 2016 Xiaolin Li <xiaolinl@vmware.com> 1.2.1-4
- Added devel subpackage.
* Thu May 26 2016 Divya Thaluru <dthaluru@vmware.com> 1.2.1-3
- Packaging pam cracklib module
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.2.1-2
- GA - Bump release of all rpms
* Fri Jan 15 2016 Xiaolin Li <xiaolinl@vmware.com> 1.2.1-1
- Updated to version 1.2.1
* Mon May 18 2015 Touseef Liaqat <tliaqat@vmware.com> 1.1.8-2
- Update according to UsrMove.
* Thu Oct 09 2014 Divya Thaluru <dthaluru@vmware.com> 1.1.8-1
- Initial build. First version
