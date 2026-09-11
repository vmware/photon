%global build_if %{photon_subrelease} >= 91

Summary:        Utilities for file systems, consoles, partitions, and messages
Name:           util-linux
Version:        2.42.3
Release:        1%{?dist}
URL:            http://www.kernel.org/pub/linux/utils/util-linux
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://mirrors.edge.kernel.org/pub/linux/utils/util-linux/v2.42/%{name}-%{version}.tar.xz

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  ncurses-devel
BuildRequires:  pkg-config

%if 0%{?with_check}
BuildRequires:  ncurses-terminfo
BuildRequires:  sudo
%endif

Requires: %{name}-libs = %{version}-%{release}
Requires: logger = %{version}-%{release}
Requires: fsck-bin = %{version}-%{release}

Conflicts: toybox < 0.8.2-2

%description
Utilities for handling file systems, consoles, partitions,
and messages.

%package lang
Summary:    Additional language files for util-linux
Requires:   %{name} = %{version}-%{release}

%description lang
These are the additional language files of util-linux.

%package docs
Summary:    Man pages and documentation for %{name}
Requires:   %{name} = %{version}-%{release}
Conflicts:  %{name} < 2.41.5-3
Conflicts:  logger < 2.41.5-3

%description docs
%{summary}

%package devel
Summary:    Header and library files for util-linux
Requires:   %{name} = %{version}-%{release}
Requires:   pkg-config
Conflicts:  %{name} < 2.41.5-3
Conflicts:  logger < 2.41.5-3

%description devel
These are the header and library files of util-linux.

%package libs
Summary:    library files for util-linux

%description libs
These are library files of util-linux.

%package -n logger
Summary:    Logger utility from util-linux
Conflicts:  %{name} < 2.38-10
Requires:   logger-bin = %{version}-%{release}

%description -n logger
Logger utility from util-linux

%package -n logger-bin
Summary:    Logger utility binary from util-linux
Conflicts:  %{name} < 2.38-10

%description -n logger-bin
Logger utility binary from util-linux

%package -n fsck-bin
Summary:    fsck binary from %{name}
Requires:   %{name}-libs = %{version}-%{release}
Conflicts:  %{name} < 2.41.5-3

%description -n fsck-bin
%{summary}

%prep
%autosetup -p1

%build
export GTKDOCIZE=true
export ADJTIME_PATH=%{_sharedstatedir}/hwclock/adjtime
autoreconf -fiv
%configure \
    --disable-nologin \
    --disable-silent-rules \
    --disable-static \
    --disable-use-tty-group \
    --disable-liblastlog2 \
    --without-python \
    --disable-asciidoc \
    --disable-poman \
    --disable-gtk-doc

%make_build

%install
install -vdm 755 %{buildroot}%{_sharedstatedir}/hwclock
%make_install %{?_smp_mflags}
find %{buildroot} -name '*.la' -delete

%find_lang %{name}

%if 0%{?with_check}
%check
chown -R nobody .
# TS_OPT_lsfd_fake -> avoids hangs: requires loopback/IPv6 sockets
# TS_OPT_column_invalid_multibyte_fake -> avoids errors: requires missing C.UTF-8 locale
# TS_OPT_script_fake -> avoids errors: requires PTY (/dev/ptmx) access
# TS_OPT_misc_flock_fake -> avoids hangs: fails on OverlayFS/tmpfs locks
sudo -u nobody /bin/bash -c "
export TS_OPT_lsfd_fake=yes
export TS_OPT_column_invalid_multibyte_fake=yes
export TS_OPT_script_fake=yes
export TS_OPT_misc_flock_fake=yes
make check %{?_smp_mflags}"
%endif

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%dir %{_sharedstatedir}/hwclock
%{_libdir}/libfdisk.so.1*
%{_libdir}/libsmartcols.so.1*
%{_bindir}/*
%{_sbindir}/*
# exclude coresched (license issue)
%exclude %{_bindir}/coresched
%exclude %{_bindir}/logger
%exclude %{_sbindir}/fsck

%files -n logger-bin
%defattr(-,root,root)
%{_bindir}/logger

%files -n logger
%defattr(-,root,root)

%files -n fsck-bin
%defattr(-,root,root)
%{_sbindir}/fsck

%files libs
%defattr(-,root,root)
%{_libdir}/libblkid.so.1*
%{_libdir}/libmount.so.1*
%{_libdir}/libuuid.so.1*

%files lang -f %{name}.lang
%defattr(-,root,root)

%files devel
%defattr(-,root,root)
%{_libdir}/pkgconfig/*.pc
%{_libdir}/*.so
%{_includedir}/*
%{_datadir}/bash-completion/completions/*

%files docs
%defattr(-,root,root)
%{_mandir}/*
%{_docdir}/%{name}/getopt*

%changelog
* Fri Sep 11 2026 Shivani Agarwal <shivani.agarwal@broadcom.com> 2.42.3-1
- Upgrade to v2.42.3
* Thu Sep 10 2026 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 2.41.5-4
- Exclude coresched from packaging
* Wed Sep 09 2026 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 2.41.5-3
- Split package further
- Ship fsck binary as a standalone package
- Move man pages and documentation to docs sub package
- Move bash completions to devel package
* Sat Aug 15 2026 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 2.41.5-2
- Extend to build for 91 and above
* Tue Jun 30 2026 Ankit Jain <ankit-aj.jain@broadcom.com> 2.41.5-1
- Update to v2.41.5
* Mon Jun 15 2026 Mukul Sikka <mukul.sikka@broadcom.com> 2.41.4-3
- Fix CVE-2026-3184
* Fri May 15 2026 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 2.41.4-2
- Extended to build for subrelease 91 and above
* Fri Apr 03 2026 Ajay Kaher <ajay.kaher@broadcom.com> 2.41.4-1
- Update to v2.41.4
* Tue Mar 31 2026 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 2.38-10
- Split logger as a sub package
* Mon Dec 15 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 2.38-9
- Fix CVE-2025-14104
* Tue Aug 26 2025 Guruswamy Basavaiah <guruswamy.basavaiah@broadcom.com> 2.38-8
- Bump version as a part of ncurses upgrade
* Tue Jun 17 2025 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 2.38-7
- Release bump for aarch64 SRP compliance
* Wed Dec 11 2024 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 2.38-6
- Release bump for SRP compliance
* Tue Nov 05 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 2.38-5
- Release bump for SRP compliance
* Fri Mar 22 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 2.38-4
- Fix CVE-2024-28085
* Sat Feb 04 2023 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 2.38-3
- Fix issue with new autoconf
* Wed Dec 21 2022 Shreenidhi Shedi <sshedi@vmware.com> 2.38-2
- Bump version as a part of readline upgrade
* Sun Aug 21 2022 Gerrit Photon <photon-checkins@vmware.com> 2.38-1
- Automatic Version Bump
* Wed Feb 23 2022 Shreenidhi Shedi <sshedi@vmware.com> 2.36-4
- Fix binary path
* Wed Aug 11 2021 Ankit Jain <ankitja@vmware.com> 2.36-3
- Fixes CVE-2021-37600
* Tue Dec 15 2020 Shreenidhi Shedi <sshedi@vmware.com> 2.36-2
- Fix build with new rpm
* Tue Sep 01 2020 Gerrit Photon <photon-checkins@vmware.com> 2.36-1
- Automatic Version Bump
* Thu Jul 09 2020 Gerrit Photon <photon-checkins@vmware.com> 2.35.1-1
- Automatic Version Bump
* Thu Apr 16 2020 Alexey Makhalov <amakhalov@vmware.com> 2.32-3
- Do not conflict with toybox >= 0.8.2-2
* Fri Nov 09 2018 Alexey Makhalov <amakhalov@vmware.com> 2.32-2
- Cross compilation support
* Mon Apr 09 2018 Xiaolin Li <xiaolinl@vmware.com> 2.32-1
- Update to version 2.32, fix CVE-2018-7738
* Wed Dec 27 2017 Anish Swaminathan <anishs@vmware.com> 2.31.1-1
- Upgrade to version 2.31.1.
* Mon Oct 02 2017 Alexey Makhalov <amakhalov@vmware.com> 2.29.2-5
- Added conflicts toybox
* Fri Sep 15 2017 Bo Gan <ganb@vmware.com> 2.29.2-4
- Cleanup check
* Mon Jul 31 2017 Xiaolin Li <xiaolinl@vmware.com> 2.29.2-3
- Fixed rpm check errors.
* Thu Apr 20 2017 Alexey Makhalov <amakhalov@vmware.com> 2.29.2-2
- Added -libs subpackage to strip docker image.
* Wed Apr 05 2017 Xiaolin Li <xiaolinl@vmware.com> 2.29.2-1
- Updated to version 2.29.2.
* Wed Dec 07 2016 Xiaolin Li <xiaolinl@vmware.com> 2.27.1-5
- Moved man3 to devel subpackage.
* Thu Nov 17 2016 Alexey Makhalov <amakhalov@vmware.com> 2.27.1-4
- Disable use tty droup
* Wed Oct 05 2016 ChangLee <changlee@vmware.com> 2.27.1-3
- Modified %check
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.27.1-2
- GA - Bump release of all rpms
* Fri Dec 11 2015 Anish Swaminathan <anishs@vmware.com> 2.27.1-1
- Upgrade version.
* Tue Oct 6 2015 Xiaolin Li <xiaolinl@vmware.com> 2.24.1-3
- Disable static, move header files, .so and config files to devel package.
* Mon May 18 2015 Touseef Liaqat <tliaqat@vmware.com> 2.24.1-2
- Update according to UsrMove.
* Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 2.24.1-1
- Initial build. First version
