Summary:        Programs for monitoring processes
Name:           procps-ng
Version:        4.0.4
Release:        3%{?dist}
URL:            https://sourceforge.net/projects/procps-ng
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://sourceforge.net/projects/procps-ng/files/Production/%{name}-%{version}.tar.xz
%define sha512 %{name}=94375544e2422fefc23d7634063c49ef1be62394c46039444f85e6d2e87e45cfadc33accba5ca43c96897b4295bfb0f88d55a30204598ddb26ef66f0420cefb4

Source1: license.txt
%include %{SOURCE1}

BuildRequires: ncurses-devel

Requires: ncurses

Conflicts: toybox < 0.8.2-2

%description
The Procps package contains programs for monitoring processes.

%package devel
Summary:    Header and development files for procps-ng
Requires:   %{name} = %{version}-%{release}

%description devel
It contains the libraries and header files to create applications

%package lang
Summary:    Additional language files for procps-ng
Group:      Applications/Databases
Requires:   %{name} = %{version}-%{release}

%description    lang
These are the additional language files of procps-ng

%prep
%autosetup -p1

%build
if [ %{_host} != %{_build} ]; then
  export ac_cv_func_malloc_0_nonnull=yes
  export ac_cv_func_realloc_0_nonnull=yes
fi

%configure \
   --docdir=%{_docdir}/%{name}-%{version} \
   --disable-static \
   --disable-kill \
   --disable-silent-rules

%make_build

%install
%make_install %{?_smp_mflags}
ln -srv %{buildroot}%{_bindir}/pidof %{buildroot}%{_sbindir}/pidof

rm -rf %{buildroot}%{_mandir}/de/ \
       %{buildroot}%{_mandir}/fr/ \
       %{buildroot}%{_mandir}/pl/ \
       %{buildroot}%{_mandir}/pt_BR/ \
       %{buildroot}%{_mandir}/ro/ \
       %{buildroot}%{_mandir}/sv/ \
       %{buildroot}%{_mandir}/uk/

%find_lang %{name}

%check
%make_build check

%clean
rm -rf %{buildroot}

%ldconfig_scriptlets

%files
%defattr(-,root,root)
%{_bindir}/ps
%{_bindir}/pidof
%{_bindir}/free
%{_bindir}/w
%{_bindir}/pgrep
%{_bindir}/uptime
%{_bindir}/vmstat
%{_bindir}/pmap
%{_bindir}/tload
%{_bindir}/pwdx
%{_bindir}/top
%{_bindir}/slabtop
%{_bindir}/watch
%{_bindir}/pkill
%{_bindir}/pidwait
%{_sbindir}/sysctl
%{_sbindir}/pidof
%_datadir/locale/*
%{_docdir}/procps-ng-*/*
%{_mandir}/man8/*
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root)
%{_includedir}/libproc2/*.h
%{_libdir}/pkgconfig/libproc2.pc
%{_libdir}/*.so
%{_mandir}/man3/*

%files lang -f %{name}.lang
%defattr(-,root,root)

%changelog
* Wed Dec 11 2024 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 4.0.4-3
- Release bump for SRP compliance
* Tue Nov 05 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 4.0.4-2
- Release bump for SRP compliance
* Mon Apr 08 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 4.0.4-1
- Upgrade to v4.0.4
* Tue Jan 16 2024 Srish Srinivasan <srish.srinivasan@broadcom.com> 4.0.0-4
- Patched CVE-2023-4016
* Thu Jun 01 2023 Nitesh Kumar <kunitesh@vmware.com> 4.0.0-3
- Bump version as a part of ncurses upgrade to v6.4
* Thu Mar 30 2023 Shreenidhi Shedi <sshedi@vmware.com> 4.0.0-2
- Remove invalid symlink
* Wed Aug 24 2022 Shreenidhi Shedi <sshedi@vmware.com> 4.0.0-1
- Upgrade to v4.0.0
* Mon Dec 06 2021 Shreenidhi Shedi <sshedi@vmware.com> 3.3.17-1
- Fix file packaging paths
* Tue Jun 30 2020 Gerrit Photon <photon-checkins@vmware.com> 3.3.16-1
- Automatic Version Bump
* Thu Apr 16 2020 Alexey Makhalov <amakhalov@vmware.com> 3.3.15-3
- Do not conflict with toybox >= 0.8.2-2
* Thu Nov 15 2018 Alexey Makhalov <amakhalov@vmware.com> 3.3.15-2
- Cross compilation support
* Fri Aug 10 2018 Tapas Kundu <tkundu@vmware.com> 3.3.15-1
- Upgrade version to 3.3.15.
- Fix for CVE-2018-1122 CVE-2018-1123 CVE-2018-1124 CVE-2018-1125
- Fix for CVE-2018-1126
* Mon Oct 02 2017 Alexey Makhalov <amakhalov@vmware.com> 3.3.12-3
- Added conflicts toybox
* Tue May 02 2017 Anish Swaminathan <anishs@vmware.com> 3.3.12-2
- Add lang package.
* Mon Apr 03 2017 Rongrong Qiu <rqiu@vmware.com> 3.3.12-1
- Upgrade to 3.3.12
* Wed Dec 07 2016 Xiaolin Li <xiaolinl@vmware.com> 3.3.11-5
- Moved man3 to devel subpackage.
* Mon Oct 03 2016 ChangLee <changLee@vmware.com> 3.3.11-4
- Modified %check
* Tue Jun 21 2016 Divya Thaluru <dthaluru@vmware.com> 3.3.11-3
- Added patch to interpret ASCII sequence correctly
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.3.11-2
- GA - Bump release of all rpms
* Thu Jan 21 2016 Anish Swaminathan <anishs@vmware.com> 3.3.11-1
- Upgrade version
* Mon May 18 2015 Touseef Liaqat <tliaqat@vmware.com> 3.3.9-2
- Update according to UsrMove.
* Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 3.3.9-1
- Initial build. First version
