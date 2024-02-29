Summary:        dnf/yum equivalent using C libs
Name:           tdnf
Version:        3.3.11
Release:        1%{?dist}
Vendor:         VMware, Inc.
Distribution:   Photon
License:        LGPLv2.1,GPLv2
URL:            https://github.com/vmware/%{name}
Group:          Applications/RPM

Source0:        https://github.com/vmware/tdnf/archive/refs/tags/%{name}-%{version}.tar.gz
%define sha512  %{name}=0c240a4e86264dcc6f47c3c3e9c99f5378ee18f937c03da17014a6617818655091f0865d22b78a24d697c2ef943d050d33157f764f478ecc3d96b5b770cb2ac8

Patch0:         pool_flag_noinstalledobsoletes.patch

Requires:       rpm-libs >= 4.16.1.3-1
Requires:       curl-libs
Requires:       %{name}-cli-libs = %{version}-%{release}
Requires:       libsolv >= 0.7.19
Requires:       libxml2
Requires:       zlib

BuildRequires:  popt-devel
BuildRequires:  rpm-devel
BuildRequires:  openssl-devel >= 1.1.1
BuildRequires:  libsolv-devel >= 0.7.19
BuildRequires:  curl-devel
BuildRequires:  libxml2-devel
BuildRequires:  zlib-devel
BuildRequires:  systemd
#plugin repogpgcheck
BuildRequires:  gpgme-devel
BuildRequires:  cmake
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools

%if 0%{?with_check}
BuildRequires:  createrepo_c
BuildRequires:  glib >= 2.68.4
BuildRequires:  python3-pip
BuildRequires:  photon-release
BuildRequires:  photon-repos
BuildRequires:  python3-requests
BuildRequires:  python3-urllib3
BuildRequires:  python3-pyOpenSSL
BuildRequires:  python3-pytest
%endif

Obsoletes:      yum
Provides:       yum

%description
%{name} is a yum/dnf equivalent which uses libsolv and libcurl

%define _tdnfpluginsdir %{_libdir}/%{name}-plugins

%package    devel
Summary:    A Library providing C API for %{name}
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}
Requires:   libsolv-devel

%description devel
Development files for %{name}

%package    cli-libs
Summary:    Library providing cli libs for %{name} like clients
Group:      Development/Libraries

%description cli-libs
Library providing cli libs for %{name} like clients.

%package    plugin-repogpgcheck
Summary:    %{name} plugin providign gpg verification for repository metadata
Group:      Development/Libraries
Requires:   gpgme

%description plugin-repogpgcheck
%{name} plugin providign gpg verification for repository metadata

%package    python
Summary:    python bindings for %{name}
Group:      Development/Libraries
Requires:   python3

%description python
python bindings for %{name}

%package automatic
Summary:   %{name} - automated upgrades
Group:     Development/Libraries
Requires:  %{name} = %{version}-%{release}
%{?systemd_requires}

%description automatic
Systemd units that can periodically download package upgrades and apply them.

%prep
%autosetup -p1 -n %{name}-%{version}

%build
%cmake \
  -DCMAKE_BUILD_TYPE=Debug \
  -DBUILD_SHARED_LIBS=OFF \
  -DCMAKE_INSTALL_LIBDIR:PATH=%{_libdir} \
  -DSYSTEMD_DIR=%{_unitdir}

%cmake_build

cd %{__cmake_builddir}
%make_build python

%if 0%{?with_check}
%check
pip3 install flake8
cd %{__cmake_builddir} && make %{?_smp_mflags} check
%endif

%install
%cmake_install
find %{buildroot} -name '*.a' -delete
mkdir -p %{buildroot}/var/cache/%{name} %{buildroot}%{_unitdir}
ln -sf %{name} %{buildroot}%{_bindir}/tyum
ln -sf %{name} %{buildroot}%{_bindir}/yum
ln -sf %{name} %{buildroot}%{_bindir}/tdnfj
mv %{buildroot}%{_libdir}/pkgconfig/tdnfcli.pc %{buildroot}%{_libdir}/pkgconfig/%{name}-cli-libs.pc
mkdir -p %{buildroot}%{_tdnfpluginsdir}/tdnfrepogpgcheck
mv %{buildroot}%{_tdnfpluginsdir}/libtdnfrepogpgcheck.so %{buildroot}%{_tdnfpluginsdir}/tdnfrepogpgcheck/

pushd %{__cmake_builddir}/python
%py3_install
popd
find %{buildroot} -name '*.pyc' -delete

%post
/sbin/ldconfig
%triggerin -- motd
[ $2 -eq 1 ] || exit 0
if [ $1 -eq 1 ]; then
  echo "detected install of %{name}/motd, enabling %{name}-cache-updateinfo.timer" >&2
  systemctl enable %{name}-cache-updateinfo.timer >/dev/null 2>&1 || :
  systemctl start %{name}-cache-updateinfo.timer >/dev/null 2>&1 || :
elif [ $1 -eq 2 ]; then
  echo "detected upgrade of %{name}, daemon-reload" >&2
  systemctl daemon-reload >/dev/null 2>&1 || :
fi

%preun
%triggerun -- motd
[ $1 -eq 1 ] && [ $2 -eq 1 ] && exit 0
echo "detected uninstall of %{name}/motd, disabling %{name}-cache-updateinfo.timer" >&2
systemctl --no-reload disable %{name}-cache-updateinfo.timer >/dev/null 2>&1 || :
systemctl stop %{name}-cache-updateinfo.timer >/dev/null 2>&1 || :
rm -f /var/cache/%{name}/cached-updateinfo.txt

%postun
/sbin/ldconfig
%triggerpostun -- motd
[ $1 -eq 1 ] && [ $2 -eq 1 ] || exit 0
echo "detected upgrade of %{name}/motd, restarting %{name}-cache-updateinfo.timer" >&2
systemctl try-restart %{name}-cache-updateinfo.timer >/dev/null 2>&1 || :

%post cli-libs
/sbin/ldconfig

%postun cli-libs
/sbin/ldconfig

%global automatic_services %{name}-automatic.timer %{name}-automatic-notifyonly.timer %{name}-automatic-install.timer

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
%{_bindir}/%{name}-cache-updateinfo
%{_libdir}/libtdnf.so.*
%config(noreplace) %{_sysconfdir}/%{name}/%{name}.conf
%config %{_unitdir}/%{name}-cache-updateinfo.service
%config(noreplace) %{_unitdir}/%{name}-cache-updateinfo.timer
%config %{_sysconfdir}/motdgen.d/02-%{name}-updateinfo.sh
%dir /var/cache/%{name}
%{_datadir}/bash-completion/completions/%{name}

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

%files plugin-repogpgcheck
%defattr(-,root,root)
%dir %{_sysconfdir}/%{name}/pluginconf.d
%config(noreplace) %{_sysconfdir}/%{name}/pluginconf.d/tdnfrepogpgcheck.conf
%{_tdnfpluginsdir}/tdnfrepogpgcheck/libtdnfrepogpgcheck.so

%files python
%defattr(-,root,root)
%{python3_sitelib}/*

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
* Tue Apr 30 2024 Oliver Kurth <oliver.kurth@broadcom.com> 3.3.11-1
- update to 3.3.11
- fix multiple --repofrompath options
* Mon Apr 29 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 3.3.9-4
- Add space to list output
* Thu Oct 19 2023 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 3.3.9-3
- Version bump for updated glib
* Mon May 29 2023 Harinadh D <hdommaraju@vmware.com> 3.3.9-2
- Version bump to use curl 8.1.1
* Fri Apr 28 2023 Oliver Kurth <okurth@vmware.com> 3.3.9-1
- update to 3.3.9
- fix segfault when invalid arguments are given to repoquery or reposync
* Fri Mar 31 2023 Harinadh D <hdommaraju@vmware.com> 3.3.8-2
- version bump to use curl 8.0.1
* Tue Mar 14 2023 Oliver Kurth <okurth@vmware.com> 3.3.8-1
- update to 3.3.8
- segfault caused due to missing name param PR #401
- ensure tdnf lock file is removed on application exit PR #403
* Fri Feb 24 2023 Oliver Kurth <okurth@vmware.com> 3.3.7-1
- update to 3.3.7
- fix reinstall on distro-sync (PR 408)
* Wed Feb 15 2023 Oliver Kurth <okurth@vmware.com> 3.3.6-1
- update to 3.3.6
- local package cache optimization (PR 392)
- ulimit fix (PR 393/391)
- reinstall fix (PR 388)
* Fri Jan 6 2023 Oliver Kurth <okurth@vmware.com> 3.3.5-1
- update to 3.3.5 (install obsoleting/providing packages)
* Wed Jan 4 2023 Oliver Kurth <okurth@vmware.com> 3.3.4-1
- fix crash when problems are reported
* Wed Nov 23 2022 Oliver Kurth <okurth@vmware.com> 3.3.3-1
- update to 3.3.3 to fix --excludes option
* Tue Sep 13 2022 Oliver Kurth <okurth@vmware.com> 3.3.2-1
- update to 3.3.2 for the --alldeps option
* Tue May 10 2022 Oliver Kurth <okurth@vmware.com> 3.3.1-1
- update to 3.3.1
* Tue Mar 01 2022 Shreenidhi Shedi <sshedi@vmware.com> 3.2.5-2
- Exclude debug symbols properly
* Tue Feb 22 2022 Oliver Kurth <okurth@vmware.com> 3.2.5-1
- update to 3.2.5
* Fri Feb 11 2022 Oliver Kurth <okurth@vmware.com> 3.2.4-1
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
