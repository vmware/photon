Summary:        Bourne-Again SHell
Name:           bash
Version:        5.2
Release:        4%{?dist}
License:        GPLv3
URL:            http://www.gnu.org/software/bash
Group:          System Environment/Base
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://ftp.gnu.org/gnu/bash/%{name}-%{version}.tar.gz
%define sha512 %{name}=5647636223ba336bf33e0c65e516d8ebcf6932de8b44f37bc468eedb87579c628ad44213f78534beb10f47aebb9c6fa670cb0bed3b4e7717e5faf7e9a1ef81ae

Source1: dircolors.sh
Source2: extrapaths.sh
Source3: readline.sh
Source4: i18n.sh
Source5: bash.bashrc
Source6: bash_profile
Source7: bashrc
Source8: bash_logout
Source9: post.inc
Source10: postun.inc

Patch0: enable-SYS_BASHRC-SSH_SOURCE_BASHRC.patch

Provides: /bin/sh
Provides: /bin/bash

BuildRequires:  readline

Requires:           readline
Requires(post):     /bin/grep
Requires(post):     /usr/bin/cp
Requires(postun):   /bin/grep
Requires(postun):   /usr/bin/mv

%description
The package contains the Bourne-Again SHell

%package    devel
Summary:    Header and development files for bash
Requires:   %{name} = %{version}-%{release}
%description    devel
It contains the libraries and header files to create applications

%package    lang
Summary:    Additional language files for bash
Group:      System Environment/Base
Requires:   %{name} = %{version}-%{release}
%description lang
These are the additional language files of bash.

%package    docs
Summary:    bash docs
Group:      Documentation
Requires:   %{name} = %{version}-%{release}
%description docs
The package contains bash doc files.

%prep
%autosetup -p1

%build
%configure \
    "CFLAGS=-fPIC" \
    --htmldir=%{_docdir}/%{name}-%{version} \
    --without-bash-malloc \
    --with-installed-readline

%make_build

%install
%make_install %{?_smp_mflags}
ln -sv bash %{buildroot}%{_bindir}/sh
install -vdm 755 %{buildroot}%{_sysconfdir}
install -vdm 755 %{buildroot}%{_sysconfdir}/profile.d
install -vdm 755 %{buildroot}%{_sysconfdir}/skel
rm %{buildroot}%{_libdir}/bash/Makefile.inc

# dircolors.sh
install -D -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/profile.d/dircolors.sh

# extrapaths.sh
install -D -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/profile.d/extrapaths.sh

# readline.sh
install -D -m 644 %{SOURCE3} %{buildroot}%{_sysconfdir}/profile.d/readline.sh

# i18n.sh
install -D -m 644 %{SOURCE4} %{buildroot}%{_sysconfdir}/profile.d/i18n.sh

# bash.bashrc
install -D -m 644 %{SOURCE5} %{buildroot}%{_sysconfdir}/bash.bashrc

# .bash_profile
install -D -m 644 %{SOURCE6} %{buildroot}%{_sysconfdir}/skel/.bash_profile

# .bashrc
install -D -m 644 %{SOURCE7} %{buildroot}%{_sysconfdir}/skel/.bashrc

# .bash_logout
install -D -m 644 %{SOURCE8} %{buildroot}%{_sysconfdir}/skel/.bash_logout

dircolors -p > %{buildroot}%{_sysconfdir}/dircolors
%find_lang %{name}
rm -rf %{buildroot}%{_infodir}

%check
%make_build NON_ROOT_USERNAME=nobody %{?_smp_mflags}

%post
%include %{SOURCE9}

%postun
%include %{SOURCE10}

%files
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/%{name}/*
%{_sysconfdir}/*

%files devel
%defattr(-,root,root)
%{_includedir}/%{name}/*
%{_libdir}/pkgconfig/*

%files lang -f %{name}.lang
%defattr(-,root,root)

%files docs
%defattr(-,root,root)
%{_docdir}/%{name}-%{version}/*
%{_docdir}/%{name}/*
%{_mandir}/*/*

%changelog
* Thu Jan 23 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 5.2-4
- Spec cleanups
* Mon Apr 08 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 5.2-3
- Remove umask.sh, have systemd wide common umask value
* Mon May 29 2023 Shreenidhi Shedi <sshedi@vmware.com> 5.2-2
- Remove bash-completion related files
- bash-completion is a new package now
* Mon Jan 09 2023 Susant Sahani <ssahani@vmware.com> 5.2-1
- Update version
* Tue Dec 20 2022 Guruswamy Basavaiah <bguruswamy@vmware.com> 5.1.16-2
- Bump release as a part of readline upgrade
* Wed Aug 24 2022 Shreenidhi Shedi <sshedi@vmware.com> 5.1.16-1
- Upgrade to v5.1.16
* Wed Feb 23 2022 Shreenidhi Shedi <sshedi@vmware.com> 5.0-3
- Fix binary path
* Fri Feb 19 2021 Satya Naga Vasamsetty <svasamsetty@vmware.com> 5.0-2
- Move documents to docs sub-package
* Wed Jul 08 2020 Gerrit Photon <photon-checkins@vmware.com> 5.0-1
- Automatic Version Bump
* Mon Sep 24 2018 Sujay G <gsujay@vmware.com> 4.4.18-1
- Bump bash version to 4.4.18
* Fri Jan 26 2018 Alexey Makhalov <amakhalov@vmware.com> 4.4.12-3
- Run bash_completion only for bash interactive shell
* Mon Dec 11 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 4.4.12-2
- conditionally apply grep color alias
* Mon Nov 13 2017 Xiaolin Li <xiaolinl@vmware.com> 4.4.12-1
- Upstream patch level 12 applied
* Mon Oct 02 2017 Kumar Kaushik <kaushikk@vmware.com> 4.4-6
- Adding security fix for CVE-2017-5932.
* Thu Jun 8 2017 Bo Gan <ganb@vmware.com> 4.4-5
- Fix dependency again
* Wed Jun 7 2017 Divya Thaluru <dthaluru@vmware.com>  4.4-4
- Added /usr/bin/sh and /bin/sh entries in /etc/shells
* Sun Jun 4 2017 Bo Gan <ganb@vmware.com> 4.4-3
- Fix dependency
* Thu Feb 2 2017 Divya Thaluru <dthaluru@vmware.com> 4.4-2
- Modified bash entry in /etc/shells
* Fri Jan 13 2017 Dheeraj Shetty <dheerajs@vmware.com> 4.4-1
- Upgraded version to 4.4
* Tue Jan 10 2017 Divya Thaluru <dthaluru@vmware.com> 4.3.30-7
- Added bash entry to /etc/shells
* Wed Nov 16 2016 Alexey Makhalov <amakhalov@vmware.com> 4.3.30-6
- Add readline requirements
* Fri Aug 19 2016 Alexey Makhalov <amakhalov@vmware.com> 4.3.30-5
- Enable bash completion support
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 4.3.30-4
- GA - Bump release of all rpms
* Tue May 3 2016 Divya Thaluru <dthaluru@vmware.com>  4.3.30-3
- Fixing spec file to handle rpm upgrade scenario correctly
* Thu Mar 10 2016 Divya Thaluru <dthaluru@vmware.com> 4.3.30-2
- Adding compile options to load bash.bashrc file and
  loading source file during non-inetractive non-login shell
* Tue Jan 12 2016 Xiaolin Li <xiaolinl@vmware.com> 4.3.30-1
- Updated to version 4.3.30
* Wed Aug 05 2015 Kumar Kaushik <kaushikk@vmware.com> 4.3-4
- Adding post unstall section.
* Wed Jul 22 2015 Alexey Makhalov <amakhalov@vmware.com> 4.3-3
- Fix segfault in save_bash_input.
* Tue Jun 30 2015 Alexey Makhalov <amakhalov@vmware.com> 4.3-2
- /etc/profile.d permission fix. Pack /etc files into rpm
* Wed Oct 22 2014 Divya Thaluru <dthaluru@vmware.com> 4.3-1
- Initial version
