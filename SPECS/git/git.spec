Summary:        Fast distributed version control system
Name:           git
Version:        2.40.4
Release:        2%{?dist}
License:        GPLv2
URL:            http://git-scm.com
Group:          System Environment/Programming
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://www.kernel.org/pub/software/scm/git/%{name}-%{version}.tar.xz
%define sha512 %{name}=0491d759d9bc44edb705acc30058ba24bf03dc9336ee825680d00c4690a825bdd36b2b2911e7f12889bca9a6a72644ce9b299cc16fe74fd033e74f7f114a4c2f

BuildRequires: curl-devel
BuildRequires: python3-devel
BuildRequires: openssl-devel

Requires: expat
Requires: curl
Requires: openssl

%description
Git is a free and open source, distributed version control system
designed to handle everything from small to very large projects with
speed and efficiency. Every Git clone is a full-fledged repository
with complete history and full revision tracking capabilities, not
dependent on network access or a central server. Branching and
merging are fast and easy to do. Git is used for version control of
files, much like tools such as Mercurial, Bazaar,
Subversion-1.7.8, CVS-1.11.23, Perforce, and Team Foundation Server.

%package lang
Summary:    Additional language files for git
Group:      System Environment/Programming
Requires:   %{name} = %{version}-%{release}
%description lang
These are the additional language files of git.

%package extras
Summary:    Git extra files to support perl, svn, gui, bash etc.
Group:      System Environment/Programming
Requires:   %{name} = %{version}-%{release}
Requires:   perl
Requires:   perl-CGI
Requires:   perl-DBI
Requires:   perl-YAML
Requires:   subversion-perl
Requires:   python3

Conflicts: %{name} < 2.35.6-4

%description extras
These are the supported files for perl interface to the git, core package of git,
graphical interface to git,git tools for interacting with subversion repositories
and git bash completion files.

%prep
%autosetup -p1

%build
%configure --with-gitconfig=%{_sysconfdir}/gitconfig

make %{?_smp_mflags} CFLAGS="%{optflags}" CXXFLAGS="%{optflags}"

%install
%make_install DESTDIR=%{buildroot} %{?_smp_mflags}
install -vdm 755 %{buildroot}%{_datadir}/bash-completion/completions
install -m 0644 contrib/completion/git-completion.bash %{buildroot}%{_datadir}/bash-completion/completions/git
%find_lang %{name}
%{_fixperms} %{buildroot}/*

%check
# git expect nonroot user to run tests
chmod g+w . -R
useradd test -G root -m
sudo -u test make %{?_smp_mflags} test

%post
if [ $1 -eq 1 ];then
  # This is first installation.
  git config --system http.sslCAPath %{_sysconfdir}/ssl/certs
  exit 0
fi

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_bindir}/*
%{_datadir}/git-core/templates
%{_datadir}/bash-completion/
%{_libexecdir}/git-core/*
%exclude %{_libexecdir}/git-core/git-svn
%exclude %{_libexecdir}/git-core/git-send-email
%exclude %{_libexecdir}/git-core/git-request-pull
%exclude %{_libexecdir}/git-core/git-p4
%exclude %{_libexecdir}/git-core/git-instaweb
%exclude %{_libexecdir}/git-core/git-filter-branch
%exclude %{_libexecdir}/git-core/git-archimport
%exclude %{_libexecdir}/git-core/git-add--interactive
%exclude %{_libexecdir}/git-core/git-gui--askpass
%exclude %{_libexecdir}/git-core/git-gui
%exclude %{_libexecdir}/git-core/git-citool
%exclude %{_libexecdir}/git-core/git-cvsexportcommit
%exclude %{_libexecdir}/git-core/git-cvsimport
%exclude %{_libexecdir}/git-core/git-cvsserver
%exclude %{_bindir}/git-cvsserver
%exclude %{_datadir}/git-core/templates/hooks/*.sample

%files extras
%defattr(-,root,root)
%{_bindir}/git-cvsserver
%{_libexecdir}/git-core/git-svn
%{_libexecdir}/git-core/git-send-email
%{_libexecdir}/git-core/git-request-pull
%{_libexecdir}/git-core/git-p4
%{_libexecdir}/git-core/git-instaweb
%{_libexecdir}/git-core/git-filter-branch
%{_libexecdir}/git-core/git-archimport
%{_libexecdir}/git-core/git-gui--askpass
%{_libexecdir}/git-core/git-gui
%{_libexecdir}/git-core/git-citool
%{_libexecdir}/git-core/git-cvsexportcommit
%{_libexecdir}/git-core/git-cvsimport
%{_libexecdir}/git-core/git-cvsserver
%{_datadir}/perl5/*
%{_datadir}/git-gui/*
%{_datadir}/gitk/*
%{_datadir}/gitweb/*
%{_datadir}/git-core/templates/hooks/*.sample

%files lang -f %{name}.lang
%defattr(-,root,root)

%changelog
* Mon May 05 2025 Guruswamy Basavaiah <guruswamy.basavaiah@broadcom.com> 2.40.4-2
- Version bump for expat upgrade
* Thu Jan 30 2025 Mukul Sikka <mukul.sikka@broadcom.com> 2.40.4-1
- Version upgrade to v2.40.4
- Fix CVE-2024-52006, CVE-2024-50349
- git-add-interactive got removed
* Wed May 15 2024 Nitesh Kumar <nitesh-nk.kumar@broadcom.com> 2.39.4-1
- Version upgrade to v2.39.4 to remove last commit patches
* Tue May 14 2024 Nitesh Kumar <nitesh-nk.kumar@broadcom.com> 2.39.3-1
- Patched on v2.39.3 to fix following CVE's:
- CVE-2024-32002, CVE-2024-32004, CVE-2024-32020,
- CVE-2024-32021 and CVE-2024-32465
* Thu Feb 29 2024 Anmol Jain <anmol.jain@broadcom.com> 2.35.6-5
- Bump version as a part of expat upgrade
* Wed May 31 2023 Nitesh Kumar <kunitesh@vmware.com> 2.35.6-4
- Adding conflict to git-extras
* Fri May 26 2023 Nitesh Kumar <kunitesh@vmware.com> 2.35.6-3
- Moving bash-completion to main package
* Tue Feb 28 2023 Nitesh Kumar <kunitesh@vmware.com> 2.35.6-2
- Adding subpackage to minimize git dependencies
* Wed Feb 01 2023 Nitesh Kumar <kunitesh@vmware.com> 2.35.6-1
- Upgrade version to 2.35.6 to fix following CVE's:
- CVE-2022-23521, CVE-2022-41903
* Tue Oct 25 2022 Nitesh Kumar <kunitesh@vmware.com> 2.35.5-1
- Upgrade version to 2.35.5
* Thu Jul 28 2022 Nitesh Kumar <kunitesh@vmware.com> 2.30.5-1
- Minor version upgrade to address CVE-2022-29187
* Tue May 10 2022 Nitesh Kumar <kunitesh@vmware.com> 2.30.3-1
- Update version to address CVE-2022-24765
* Thu Dec 09 2021 Prashant S Chauhan <psinghchauha@vmware.com> 2.30.0-7
- Bump up to compile with python 3.10
* Tue Sep 14 2021 Satya Naga Vasamsetty <svasamsetty@vmware.com> 2.30.0-6
- Compatibility for openssl 3.0.0
* Fri Sep 10 2021 Nitesh Kumar <kunitesh@vmware.com> 2.30.0-5
- Fix CVE-2021-40330
* Wed May 26 2021 Shreenidhi Shedi <sshedi@vmware.com> 2.30.0-4
- Bump version as a part of rpm upgrade
* Tue Mar 09 2021 Prashant S Chauhan <psinghchauha@vmware.com> 2.30.0-3
- Fix CVE-2021-21300
* Mon Feb 01 2021 Shreenidhi Shedi <sshedi@vmware.com> 2.30.0-2
- Fix build with new rpm
* Sat Jan 23 2021 Susant Sahani <ssahani@vmware.com> 2.30.0-1
- Update version
* Tue Sep 01 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 2.28.0-2
- Compatibility for openssl 1.1.1
* Sun Aug 09 2020 Gerrit Photon <photon-checkins@vmware.com> 2.28.0-1
- Automatic Version Bump
* Tue Jun 23 2020 Tapas Kundu <tkundu@vmware.com> 2.26.2-2
- Build python3
* Tue May 19 2020 Prashant S Chauhan <psinghchauhan@vmware.com> 2.26.2-1
- Updated to version 2.26.2, fix CVE-2020-11008, CVE-2020-5260
* Mon Apr 27 2020 Prashant S Chauhan <psinghchauha@vmware.com> 2.26.0-2
- Added patch, Fixes CVE-2020-5260
* Wed Apr 01 2020 Susant Sahani <ssahani@vmware.com> 2.26.0-1
- Updated to version 2.26.0
* Tue Feb 12 2019 Prashant S Chauhan <psinghchauha@vmware.com> 2.23.1-1
- Updated to version 2.23.1 . Fixes CVE-2019-1348
* Thu Jan 10 2019 Alexey Makhalov <amakhalov@vmware.com> 2.19.0-3
- Added Requires python2
* Thu Oct 04 2018 Dweep Advani <dadvani@vmware.com> 2.19.0-2
- Using %configure and changing for perl upgrade
* Tue Oct 02 2018 Siju Maliakkal <smaliakkal@vmware.com> 2.19.0-1
- Update to latest version
* Tue Jul 31 2018 Ajay Kaher <akaher@vmware.com> 2.14.2-2
- Excluded the perllocal.pod for aarch64.
* Thu Oct 12 2017 Anish Swaminathan <anishs@vmware.com> 2.14.2-1
- Updated to version 2.14.2, fix CVE-2017-14867
* Mon Aug 21 2017 Rui Gu <ruig@vmware.com> 2.9.3-4
- Fix make check with non-root mode.
* Wed May 31 2017 Xiaolin Li <xiaolinl@vmware.com> 2.9.3-3
- Mass removal python2 from requires.
* Mon Apr 17 2017 Robert Qi <qij@vmware.com> 2.9.3-2
- Update since perl version got updated.
* Mon Apr 10 2017 Danut Moraru <dmoraru@vmware.com> 2.9.3-1
- Updated to version 2.9.3
* Wed Dec 07 2016 Xiaolin Li <xiaolinl@vmware.com> 2.8.1-7
- BuildRequires curl-devel.
* Fri Aug 19 2016 Alexey Makhalov <amakhalov@vmware.com> 2.8.1-6
- Add bash completion file
* Thu May 26 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 2.8.1-5
- Excluded the perllocal.pod log.
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.8.1-4
- GA - Bump release of all rpms
* Wed May 18 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.8.1-3
- Fix if syntax
* Thu May 05 2016 Kumar Kaushik <kaushikk@vmware.com> 2.8.1-2
- Handling the upgrade scenario.
* Fri Apr 15 2016 Anish Swaminathan <anishs@vmware.com> 2.8.1-1
- Updated to version 2.8.1
* Tue Feb 23 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 2.7.1-1
- Updated to version 2.7.1
* Wed Jan 13 2016 Anish Swaminathan <anishs@vmware.com> 2.1.2-2
- Add requires for perl-CGI.
* Fri Apr 3 2015 Divya Thaluru <dthaluru@vmware.com> 2.1.2-1
- Initial build. First version
