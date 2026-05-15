%global build_if %{photon_subrelease} >= 92

%define hist_db_dir     %{_libdir}/sysimage/%{name}
%define _tdnfpluginsdir %{_libdir}/%{name}-plugins
%global automatic_services %{name}-automatic.timer %{name}-automatic-notifyonly.timer %{name}-automatic-install.timer

Summary:        dnf/yum equivalent using C libs
Name:           tdnf
Version:        3.6.4
Release:        3%{?buildtag}%{?dist}
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://github.com/vmware/%{name}

Group:          Applications/RPM

Source0:        https://github.com/vmware/tdnf/archive/refs/tags/%{name}-%{version}.tar.gz

Source1:        license.txt
%include %{SOURCE1}

Source2: tdnf.conf

Patch0: 0001-do-not-nuke-RPMBUILD_DIR-in-pytests-since-it-can-be-.patch
Patch1: 0002-check-for-RPMTAG_OPENPGP.patch
Patch2: 0003-ensure-history-db-directory-exists.patch
Patch3: 0004-check-for-history-db-errors.patch
Patch4: 0005-fix-const-qualifier-warning.patch
Patch5: 0006-ignore-history-absent-error-if-a-package-is-already-.patch
Patch6: 0007-add-a-test-for-history-db-not-existing-error-when-pa.patch

Requires:       rpm-libs >= 6.0.1
Requires:       curl-libs
Requires:       expat-libs
Requires:       %{name}-cli-libs = %{version}-%{release}
Requires:       libsolv
Requires:       zlib

BuildRequires:  popt-devel
BuildRequires:  rpm-devel
BuildRequires:  openssl-devel
BuildRequires:  libsolv-devel
BuildRequires:  curl-devel
BuildRequires:  expat-devel
BuildRequires:  sqlite-devel
BuildRequires:  zlib-devel
BuildRequires:  systemd
BuildRequires:  systemd-rpm-macros

#metalink plugin
BuildRequires:  expat-devel

#repogpgcheck plugin
BuildRequires:  gpgme-devel

BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  cmake
%if 0%{?with_check}
BuildRequires:  createrepo_c
BuildRequires:  glib
BuildRequires:  python3-pip
BuildRequires:  photon-release
BuildRequires:  photon-repos
BuildRequires:  python3-requests
BuildRequires:  python3-urllib3
BuildRequires:  python3-pyOpenSSL
BuildRequires:  python3-pytest
BuildRequires:  sudo
%endif

%description
%{name} is a yum/dnf equivalent which uses libsolv and libcurl

%package    devel
Summary:    A Library providing a C API for %{name}
Requires:   %{name} = %{version}-%{release}
Requires:   libsolv-devel

%description devel
Development files for %{name}

%package    pytests
Summary:    Test suite for %{name}
Requires:   %{name} = %{version}-%{release}
Requires:   %{name}-automatic = %{version}-%{release}
Requires:   %{name}-plugin-repogpgcheck = %{version}-%{release}
Requires:   %{name}-plugin-metalink = %{version}-%{release}
Requires:   python3-pytest
Requires:   python3-requests
Requires:   rpm-build
Requires:   build-essential
Requires:   createrepo_c
Requires:   shadow
Requires:   sudo
Requires:   e2fsprogs
Requires:   util-linux
Requires:   findutils

%description pytests
Test suite for %{name}

%package    cli-libs
Summary:    Library providing cli libs for %{name} like clients

%description cli-libs
Library providing cli libs for %{name} like clients.

%package    plugin-metalink
Summary:    tdnf plugin providing metalink functionality for repo configurations
Requires:   gpgme

%description plugin-metalink
tdnf plugin providing metalink functionality for repo configurations

%package    plugin-repogpgcheck
Summary:    %{name} plugin providing gpg verification for repository metadata
Requires:   gpgme

%description plugin-repogpgcheck
%{name} plugin providing gpg verification for repository metadata

%package automatic
Summary:   %{name} - automated upgrades
Requires:  %{name} = %{version}-%{release}
%{?systemd_requires}

%description automatic
Systemd units that can periodically download package upgrades and apply them.

%prep
%autosetup -p1

%build
# set BUILD_WITH_RPM_6X=ON if you are using v6 rpm format
# Check SPECS/rpm/0009-rpm-6.0-rpmformat.patch
%{cmake} \
  -DCMAKE_BUILD_TYPE=Debug \
  -DCMAKE_INSTALL_PREFIX=%{_prefix} \
  -DCMAKE_INSTALL_LIBDIR=%{_libdir} \
  -DSYSTEMD_DIR=%{_unitdir} \
  -DHISTORY_DB_DIR=%{hist_db_dir} \
  -DBUILD_WITH_RPM_6X=OFF

%{cmake_build}

%install
%{cmake_install}

mkdir -p %{buildroot}{%{_var}/cache/%{name},%{_unitdir}}
ln -sv %{name} %{buildroot}%{_bindir}/tyum
ln -sv %{name} %{buildroot}%{_bindir}/yum
ln -sv %{name} %{buildroot}%{_bindir}/tdnfj

install -vm 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/%{name}

mkdir -p %{buildroot}%{_sysconfdir}/%{name}/protected.d && \
    echo %{name} > %{buildroot}%{_sysconfdir}/%{name}/protected.d/%{name}.conf

find %{buildroot} -name '*.a' -delete

%if 0%{?with_check}
%check
%define _make_output_sync %{nil}
pip3 install flake8
mkdir -p %{_rundir}/user/$(id -u)
%make_build -C %{__cmake_builddir} check
%endif

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%triggerin -- motd
[ $2 -eq 1 ] || exit 0
if [ $1 -eq 2 ]; then
  echo "detected upgrade of %{name}, daemon-reload" >&2
  systemctl daemon-reload &>/dev/null || :
fi
exit 0

%triggerun -- motd
[ $1 -eq 1 ] && [ $2 -eq 1 ] && exit 0
rm -f %{_var}/cache/%{name}/cached-updateinfo.txt

%post cli-libs
/sbin/ldconfig
[ -d %{hist_db_dir} ] || mkdir -p %{hist_db_dir}

%postun cli-libs
/sbin/ldconfig

%post automatic
%systemd_post %{automatic_services}

%preun automatic
%systemd_preun %{automatic_services}

%postun automatic
%systemd_postun_with_restart %{automatic_services}

%files
%defattr(-,root,root,0755)
%{_bindir}/%{name}
%{_bindir}/tyum
%{_bindir}/yum
%{_bindir}/tdnfj
%{_bindir}/%{name}-config
%{_libdir}/libtdnf.so.*
%{_libexecdir}/%{name}/%{name}-history-util
%config(noreplace) %{_sysconfdir}/%{name}/%{name}.conf
%config(noreplace) %{_sysconfdir}/%{name}/protected.d/%{name}.conf
%config %{_sysconfdir}/motdgen.d/02-%{name}-updateinfo.sh
%dir %{_var}/cache/%{name}
%{_datadir}/bash-completion/completions/%{name}

%files pytests
%defattr(-,root,root)
%{_datadir}/%{name}/pytests/
%{_bindir}/jsondumptest

%files devel
%defattr(-,root,root)
%{_includedir}/%{name}/*.h
%{_libdir}/libtdnf.so
%{_libdir}/libtdnfcli.so
%exclude %dir %{_libdir}/debug
%{_libdir}/pkgconfig/%{name}.pc
%{_libdir}/pkgconfig/%{name}-cli-libs.pc

%files cli-libs
%defattr(-,root,root)
%{_libdir}/libtdnfcli.so.*

%files plugin-metalink
%defattr(-,root,root)
%dir %{_sysconfdir}/%{name}/pluginconf.d
%config(noreplace) %{_sysconfdir}/%{name}/pluginconf.d/tdnfmetalink.conf
%{_tdnfpluginsdir}/libtdnfmetalink.so

%files plugin-repogpgcheck
%defattr(-,root,root)
%dir %{_sysconfdir}/%{name}/pluginconf.d
%config(noreplace) %{_sysconfdir}/%{name}/pluginconf.d/tdnfrepogpgcheck.conf
%{_tdnfpluginsdir}/libtdnfrepogpgcheck.so

%files automatic
%defattr(-,root,root,0755)
%{_bindir}/%{name}-automatic
%config(noreplace) %{_sysconfdir}/%{name}/automatic.conf
%{_unitdir}/%{name}-automatic.timer
%{_unitdir}/%{name}-automatic.service
%{_unitdir}/%{name}-automatic-install.timer
%{_unitdir}/%{name}-automatic-install.service
%{_unitdir}/%{name}-automatic-notifyonly.timer
%{_unitdir}/%{name}-automatic-notifyonly.service

%changelog
* Fri May 15 2026 Oliver Kurth <oliver.kurth@broadcom.com> 3.6.4-3
- ignore history absent error if a package is already installed
- add a test for history db not existing error when package is installed
* Tue May 05 2026 Oliver Kurth <oliver.kurth@broadcom.com> 3.6.4-2
- ensure history db directory exists
- check for history db errors (SQLITE_BUSY)
- fix 'assignment discards const qualifier' warning
* Thu Apr 16 2026 Oliver Kurth <oliver.kurth@broadcom.com> 3.6.4-1
- update to 3.6.4
* Thu Apr 09 2026 Oliver Kurth <oliver.kurth@broadcom.com> 3.6.3-6
- Remove posttrans action to avoid deadlock with rpm 6
* Wed Mar 25 2026 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 3.6.3-5
- Bump version as a part of rpm upgrade
* Tue Mar 24 2026 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 3.6.3-4
- Fix installs from command line repo
* Fri Mar 13 2026 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 3.6.3-3
- Add connect timeout patch
* Thu Mar 12 2026 Oliver Kurth <oliver.kurth@broadcom.com> 3.6.3-2
- fix obsoletes in snapshots, PR 561
* Tue Jan 27 2026 Oliver Kurth <oliver.kurth@broadcom.com> 3.6.3-1
- update to 3.6.3
* Fri Jan 09 2026 Oliver Kurth <oliver.kurth@broadcom.com> 3.5.16-1
- update to 3.5.16
- nocligpgcheck option and bug fix
* Mon Jan 05 2026 Oliver Kurth <oliver.kurth@broadcom.com> 3.5.15-1
- update to 3.5.15
* Thu Dec 18 2025 Oliver Kurth <oliver.kurth@broadcom.com> 3.5.14-2
- fix snapshot URL
* Fri Nov 21 2025 Oliver Kurth <oliver.kurth@broadcom.com> 3.5.14-1
- update to 3.5.14
- snapshot URL
* Tue Oct 07 2025 Oliver Kurth <oliver.kurth@broadcom.com> 3.5.13-3
- fix forcearch option
* Wed Sep 24 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 3.5.13-2
- Remove updateinfo timer
- MOTD has its own timer now
* Fri Aug 15 2025 Oliver Kurth <oliver.kurth@broadcom.com> 3.5.13-1
- support for substitution variables in files ("vars")
- support for snapshot repositories
* Wed Aug 13 2025 Oliver Kurth <oliver.kurth@broadcom.com> 3.5.12-3
- improve error message when packages are unsigned
* Tue Jul 22 2025 Oliver Kurth <oliver.kurth@broadcom.com> 3.5.12-2
- set clean_requirements_on_remove=1 for STIG compliance
* Fri Jul 11 2025 Oliver Kurth <oliver.kurth@broadcom.com> 3.5.12-1
- update to 3.5.12
- check for unsigned packages when gpgcheck is enabled (PR 525)
- add --forcearch option (PR 524)
* Wed Mar 12 2025 Oliver Kurth <oliver.kurth@broadcom.com> 3.5.11-1
- update to 3.5.11
- fix for SRPM install when binary package is installed #515
* Wed Dec 18 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 3.5.10-1
- Upgrade to v3.5.10
* Thu Dec 12 2024 Dweep Advani <dweep.advani@broadcom.com> 3.5.9-2
- Release bump for SRP compliance
* Tue Oct 15 2024 Oliver Kurth <oliver.kurth@broadcom.com> 3.5.9-1
- update to 3.5.9
- allow unprivileged user to run 'makecache'
- show complex (relational) deps in repoquery
- remove pthread_mutex API
* Tue Jul 16 2024 Oliver Kurth <oliver.kurth@broadcom.com> 3.5.8-1
- update to 3.5.8
- priority fix and output repo information in json (PR #484 and PR #485)
* Tue Jun 25 2024 Oliver Kurth <oliver.kurth@broadcom.com> 3.5.7-1
- update to 3.5.7
- epoch fix
* Fri Feb 23 2024 Nitesh Kumar <nitesh-nk.kumar@broadcom.com> 3.5.6-2
- Bump version as a part of sqlite upgrade to v3.43.2
* Tue Dec 12 2023 Oliver Kurth <oliver.kurth@broadcom.com> 3.5.6-1
- update to 3.5.6
- adds --rpmdefine option and fixes
* Tue Nov 14 2023 Shreenidhi Shedi <sshedi@vmware.com> 3.5.5-2
- Bump version as a part of rpm upgrade
* Fri Aug 25 2023 Oliver Kurth <okurth@vmware.com> 3.5.5-1
- update to 3.5.5
- checksum check for packages and other minor fixes
* Wed Jul 26 2023 Oliver Kurth <okurth@vmware.com> 3.5.4-1
- update to 3.5.4
- fix rpm verbosity default, and fix rpm scriptlet output when json is enabled #438
* Tue Jun 13 2023 Oliver Kurth <okurth@vmware.com> 3.5.3-1
- update to 3.5.3
- fix python test for python >= 3.11 #425
- Fix history rollback for public key and protected packages #430
- Fix error when a repo was disabled because it's unavailable. Fixes #431 #432
- add -pytests package
* Thu May 25 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 3.5.2-4
- Bump version as a part of libxml2 upgrade
* Fri Apr 14 2023 Harinadh D <hdommaraju@vmware.com> 3.5.2-3
- version bump to use curl 8.0.1
* Fri Apr 14 2023 Shreenidhi Shedi <sshedi@vmware.com> 3.5.2-2
- Bump version as a part of zlib upgrade
* Tue Apr 04 2023 Oliver Kurth <okurth@vmware.com> 3.5.2-1
- update to 3.5.2:
- add protected feature (PR #413)
- refactor yes/no question (PR #415)
* Tue Mar 28 2023 Oliver Kurth <okurth@vmware.com> 3.5.1-1
- update to 3.5.1:
- coverity changes
* Tue Mar 14 2023 Oliver Kurth <okurth@vmware.com> 3.5.0-3
- fix segfault when name isn't set in repo (similar to PR #401)
- fix compile warning
* Fri Mar 10 2023 Shreenidhi Shedi <sshedi@vmware.com> 3.5.0-2
- Require openssl-libs
* Thu Mar 09 2023 Oliver Kurth <okurth@vmware.com> 3.5.0-1
- update to 3.5.0
* Tue Jan 31 2023 Oliver Kurth <okurth@vmware.com> 3.4.9-1
- update to 3.4.9:
- limit the number of open files for rpm transactions
  to prevent hangs (PR #391 and #393)
- do not copy packages to cache if they can be accessed through the
  filesystem (PR #392)
* Mon Jan 23 2023 Oliver Kurth <okurth@vmware.com> 3.4.8-1
- update to 3.4.8:
- fix reinstall issue (PR #388)
- fix empty rpm db issue (PR #390)
* Thu Jan 19 2023 Oliver Kurth <okurth@vmware.com> 3.4.7-1
- update to 3.4.7 (configurable db dir)
* Thu Jan 12 2023 Oliver Kurth <okurth@vmware.com> 3.4.6-1
- update to 3.4.6 (coverity)
* Wed Jan 11 2023 Oliver Kurth <okurth@vmware.com> 3.4.5-3
- bump release as part of sqlite update
* Wed Jan 11 2023 Oliver Kurth <okurth@vmware.com> 3.4.5-2
- bump release as part of sqlite update
* Thu Jan 05 2023 Oliver Kurth <okurth@vmware.com> 3.4.5-1
- update to 3.4.5
* Tue Jan 03 2023 Shreenidhi Shedi <sshedi@vmware.com> 3.4.4-2
- Bump version as a part of rpm upgrade
* Fri Dec 09 2022 Oliver Kurth <okurth@vmware.com> 3.4.4-1
- update to 3.4.4
* Fri Dec 02 2022 Prashant S Chauhan <psinghchauha@vmware.com> 3.4.3-2
- Update release to compile with python 3.11
* Thu Nov 17 2022 Oliver Kurth <okurth@vmware.com> 3.4.3-1
- update to 3.4.3
* Thu Oct 27 2022 Oliver Kurth <okurth@vmware.com> 3.4.2-1
- update to 3.4.2
* Tue Oct 18 2022 Oliver Kurth <okurth@vmware.com> 3.4.1-1
- update to 3.4.1
* Wed Sep 28 2022 Shreenidhi Shedi <sshedi@vmware.com> 3.3.2-2
- Bump version as a part of libsolv upgrade
* Tue Sep 13 2022 Oliver Kurth <okurth@vmware.com> 3.3.2-1
- update to 3.3.2 for the --alldeps option
* Sun Jul 03 2022 Shreenidhi Shedi <sshedi@vmware.com> 3.3.1-4
- Bump version as a part of rpm upgrade
* Mon Jun 27 2022 Shreenidhi Shedi <sshedi@vmware.com> 3.3.1-3
- Exclude debug symbols properly
* Fri Jun 17 2022 Shreenidhi Shedi <sshedi@vmware.com> 3.3.1-2
- Spec improvements
* Tue May 10 2022 Oliver Kurth <okurth@vmware.com> 3.3.1-1
- update to 3.3.1
* Mon Feb 21 2022 Oliver Kurth <okurth@vmware.com> 3.2.5-1
- update to 3.2.5
* Thu Feb 03 2022 Oliver Kurth <okurth@vmware.com> 3.2.4-1
- update to 3.2.4
* Wed Dec 22 2021 Oliver Kurth <okurth@vmware.com> 3.2.3-1
- update to 3.2.3
* Fri Dec 10 2021 Oliver Kurth <okurth@vmware.com> 3.2.2-1
- update to 3.2.2
* Thu Dec 09 2021 Prashant S Chauhan <psinghchauha@vmware.com> 3.1.5-4
- Bump up to compile with python 3.10
* Mon Nov 15 2021 Shreenidhi Shedi <sshedi@vmware.com> 3.1.5-3
- Bump version as a part of rpm upgrade
* Mon Nov 08 2021 Satya Naga Vasamsetty <svasamsetty@vmware.com> 3.1.5-2
- openssl 3.0.0 compatibility
* Wed Oct 06 2021 Oliver Kurth <okurth@vmware.com> 3.1.5-1
- update to 3.1.5
- add minversions config option
- make pytests arch independent (does not affect functionality)
* Mon Aug 2 2021 Oliver Kurth <okurth@vmware.com> 3.1.4-1
- update to 3.1.4
- fix configreader key reading logic
* Tue Jun 29 2021 Oliver Kurth <okurth@vmware.com> 3.1.3-1
- update to 3.1.3
* Wed Jun 23 2021 Oliver Kurth <okurth@vmware.com> 3.1.2-1
- update to 3.1.2
* Fri Jun 11 2021 Oliver Kurth <okurth@vmware.com> 3.1.0-3
- rebuild with libsolv 0.7.19
* Thu Jun 03 2021 Shreenidhi Shedi <sshedi@vmware.com> 3.1.0-2
- fix segfaulting when gpgcheck is enabled & no key configured
* Tue Jun 01 2021 Oliver Kurth <okurth@vmware.com> 3.1.0-1
- update to 3.1.0
* Tue Apr 06 2021 Oliver Kurth <okurth@vmware.com> 3.0.2-1
- update to 3.0.2
* Thu Feb 18 2021 Oliver Kurth <okurth@vmware.com> 3.0.0-5
- update to v3.0.0 (GA)
- depend on curl-libs instead of curl
* Wed Feb 10 2021 Shreenidhi Shedi <sshedi@vmware.com> 3.0.0-4
- bump version as a part of rpm upgrade
* Wed Jan 20 2021 Oliver Kurth <okurth@vmware.com> 3.0.0-3
- update to v3.0.0-rc2
* Thu Oct 29 2020 Keerthana K <keerthanak@vmware.com> 3.0.0-2
- Fix coverity scan issues and fedora pytest issue.
* Tue Oct 27 2020 Keerthana K <keerthanak@vmware.com> 3.0.0-1
- Update to v3.0.0-beta
* Sun Sep 06 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 2.1.1-3
- Rebuild with openssl 1.1.1
* Sat Aug 15 2020 Shreenidhi Shedi <sshedi@vmware.com> 2.1.1-2
- Cherry-pick some critical fixes from vmware/tdnf:dev
* Thu Jun 04 2020 Tapas Kundu <tkundu@vmware.com> 2.1.1-1
- Update to 2.1.1
* Tue Mar 24 2020 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.1.0-2
- Fix distroverpkg search to look for provides instead of name
* Thu Feb 20 2020 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.1.0-1
- Update to 2.1.0
* Sun Sep 08 2019 Ankit Jain <ankitja@vmware.com> 2.0.0-11
- Added more rules for skipconflicts and skipobsoletes to check command.
* Fri Mar 15 2019 Ankit Jain <ankitja@vmware.com> 2.0.0-10
- Added skipconflicts and skipobsoletes to check command.
* Thu Mar 14 2019 Keerthana K <keerthanak@vmware.com> 2.0.0-9
- GPGCheck fix on RPM version 4.14.2
* Mon Mar 04 2019 Keerthana K <keerthanak@vmware.com> 2.0.0-8
- makecache and refresh command updates.
* Thu Feb 14 2019 Keerthana K <keerthanak@vmware.com> 2.0.0-7
- Fix to address issues when no repos are enabled.
* Wed Jan 23 2019 Keerthana K <keerthanak@vmware.com> 2.0.0-6
- Fix Memory leak and curl status type.
* Wed Jan 02 2019 Keerthana K <keerthanak@vmware.com> 2.0.0-5
- Added make check.
* Tue Dec 04 2018 Keerthana K <keerthanak@vmware.com> 2.0.0-4
- Add support for libsolv caching.
- Fix bug in tdnf updateinfo command.
- Fix bug on list available command.
* Wed Nov 21 2018 Keerthana K <keerthanak@vmware.com> 2.0.0-3
- Update to 2.0.0 beta release.
* Mon Oct 08 2018 Keerthana K <keerthanak@vmware.com> 2.0.0-2
- Fix bug on tdnf crash when photon-iso repo only enabled without mounting cdrom.
* Fri Feb 09 2018 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.0.0-1
- update to 2.0.0
* Tue Jan 30 2018 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.2.2-3
- patch to error out early for permission issues.
* Tue Oct 10 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.2.2-2
- Fix bug in obsolete protected packages.
* Wed Oct 4 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.2.2-1
- update to v1.2.2
* Sat Sep 30 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.2.1-5
- Output problems while resolving to stderr (instead of stdout)
* Wed Sep 27 2017 Bo Gan <ganb@vmware.com> 1.2.1-4
- Improve suggestion in motd message
* Thu Sep 14 2017 Bo Gan <ganb@vmware.com> 1.2.1-3
- Add suggestion in motd message
* Fri Jul 21 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.2.1-2
- Modify quiet patch.
* Tue Jul 18 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.2.1-1
- Update to v1.2.1
* Tue May 30 2017 Bo Gan <ganb@vmware.com> 1.2.0-5
- Fix cache-updateinfo script again
* Fri May 12 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.2.0-4
- Patch repo refresh to allow quiet flags
* Wed May 10 2017 Bo Gan <ganb@vmware.com> 1.2.0-3
- Fix cache-updateinfo script
* Fri May 05 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.2.0-2
- Fix Requires for cli-libs
* Wed May 03 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.2.0-1
- update to v1.2.0
* Sun Apr 30 2017 Bo Gan <ganb@vmware.com> 1.1.0-5
- Do not write to stdout in motd triggers
* Thu Apr 20 2017 Bo Gan <ganb@vmware.com> 1.1.0-4
- motd hooks/triggers for updateinfo notification
* Fri Apr 14 2017 Dheerajs Shetty <dheerajs@vmware.com> 1.1.0-3
- Adding a patch to compile with latest hawkey version
* Mon Dec 19 2016 Xiaolin Li <xiaolinl@vmware.com> 1.1.0-2
- BuildRequires libsolv-devel.
* Thu Dec 08 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.1.0-1
- update to v1.1.0
* Thu Nov 17 2016 Alexey Makhalov <amakhalov@vmware.com> 1.0.9-3
- Use rpm-libs at runtime
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.0.9-2
- GA - Bump release of all rpms
* Fri May 20 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.0.9-1
- Update to 1.0.9. Contains fixes for updateinfo.
* Wed May 4 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.0.8-3
- Fix link installs, fix devel header dir
* Fri Apr 1 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.0.8-2
- Update version which was missed with 1.0.8-1, apply string limits
* Fri Apr 1 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.0.8-1
- Code scan fixes, autotest path fix, support --releasever
* Thu Jan 14 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.0.7
- Fix return codes on install and check-update
- Add tests for install existing and update
* Wed Jan 13 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.0.6
- Support distroverpkg and add tests to work with make check
* Mon Dec 14 2015 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.0.5
- Support for multiple packages in alter commands
- Support url vars for releasever and basearch
* Fri Oct 2 2015 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.0.4
- Fix upgrade to work without args, Engage distro-sync
- Fix install to resolve to latest available
- Fix formats, fix refresh on download output
* Tue Sep 8 2015 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.0.3
- Fix metadata creation issues. Engage refresh flag.
- Do not check gpgkey when gpgcheck is turned off in repo.
* Thu Jul 23 2015 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.0.2
- Support reinstalls in transaction. Handle non-existent packages correctly.
* Mon Jul 13 2015 Alexey Makhalov <amakhalov@vmware.com> 1.0.1-2
- Create -debuginfo package. Use parallel make.
* Tue Jun 30 2015 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.0.1
- Proxy support, keepcache fix, valgrind leaks fix
* Fri Jan 23 2015 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.0
- Initial build.  First version
