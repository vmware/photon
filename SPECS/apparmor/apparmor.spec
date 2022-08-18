Name:           apparmor
Version:        3.1.1
Release:        2%{?dist}
Summary:        AppArmor is an effective and easy-to-use Linux application security system.
License:        GNU LGPL v2.1
URL:            https://launchpad.net/apparmor
Vendor:         VMware, Inc.
Distribution:   Photon
Group:          Productivity/Security

Source0:        https://launchpad.net/%{name}/3.0/%{version}/+download/%{name}-%{version}.tar.gz
%define sha512  %{name}=ece3a0c45fec0477d49c223559ee46b28affeb7da488ba972ae032dc61a27d5e293686a0745da96e2cd3761cf4e0695130c326d42ba6f667d6b5110a824965f5

BuildRequires:  python3
BuildRequires:  perl
BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  swig
BuildRequires:  make
BuildRequires:  gawk
BuildRequires:  which
BuildRequires:  libstdc++
BuildRequires:  libstdc++-devel
BuildRequires:  gcc
BuildRequires:  libgcc
BuildRequires:  libgcc-devel
BuildRequires:  glibc
BuildRequires:  glibc-devel
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  httpd
BuildRequires:  httpd-devel
BuildRequires:  httpd-tools
BuildRequires:  apr
BuildRequires:  apr-util-devel
BuildRequires:  Linux-PAM
BuildRequires:  Linux-PAM-devel
BuildRequires:  dejagnu
BuildRequires:  openssl-devel
BuildRequires:  curl-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml

%if 0%{?with_check}
BuildRequires: python3-pip
%endif

%description
AppArmor is a file and network mandatory access control
mechanism. AppArmor confines processes to the resources allowed by the
systems administrator and can constrain the scope of potential security
vulnerabilities.

%package -n     libapparmor
Summary:        Utility library for AppArmor
License:        GNU LGPL v2.1
Group:          Development/Libraries/C and C++

%description -n libapparmor
This package contains the AppArmor library.

%package -n     libapparmor-devel
Summary:        Development headers and libraries for libapparmor
License:        GNU LGPL v2.1
Group:          Development/Libraries/C and C++
Requires:       libapparmor = %{version}-%{release}

%description -n libapparmor-devel
This package contains development files for libapparmor.

%package -n     apache2-mod_apparmor
Summary:        AppArmor module for apache2
License:        GNU LGPL v2.1
Group:          Productivity/Security

%description -n apache2-mod_apparmor
This provides the Apache module needed to declare various differing
confinement policies when running virtual hosts in the webserver
by using the changehat abilities exposed through libapparmor.

%package        profiles
Summary:        AppArmor profiles that are loaded into the %{name} kernel module
License:        GNU LGPL v2.1
Group:          Productivity/Security
Requires:       %{name}-parser = %{version}-%{release}
Requires:       %{name}-abstractions = %{version}-%{release}

%description    profiles
This package contains the basic AppArmor profiles.

%package        parser
Summary:        AppArmor userlevel parser utility
License:        GNU LGPL v2.1
Group:          Productivity/Security
Requires:       libapparmor = %{version}-%{release}
Requires:       systemd

%description    parser
The AppArmor Parser is a userlevel program that is used to load in
program profiles to the AppArmor Security kernel module.
This package is part of a suite of tools that used to be named
SubDomain.

%package        abstractions
Summary:        AppArmor abstractions and directory structure
License:        GNU LGPL v2.1
Group:          Productivity/Security
Requires:       %{name}-parser = %{version}-%{release}

%description    abstractions
AppArmor abstractions (common parts used in various profiles) and
the /etc/%{name}.d/ directory structure.

%package -n     pam_apparmor
Summary:        PAM module for AppArmor change_hat
License:        GNU LGPL v2.1
Group:          Productivity/Security
Requires:       Linux-PAM
Requires:       Linux-PAM-devel

%description -n pam_apparmor
The pam_apparmor module provides the means for any PAM applications
that call pam_open_session() to automatically perform an AppArmor
change_hat operation in order to switch to a user-specific security
policy.

%package        utils
Summary:        AppArmor User-Level Utilities Useful for Creating AppArmor Profiles
License:        GNU LGPL v2.1
Group:          Productivity/Security
Requires:       libapparmor = %{version}-%{release}
Requires:       audit
Requires:       %{name}-abstractions = %{version}-%{release}

%description    utils
This package contains programs to help create and manage AppArmor
profiles.

%package -n     python3-%{name}
Summary:        Python 3 interface for libapparmor functions
License:        GNU LGPL v2.1
Group:          Development/Libraries/Python
Requires:       libapparmor = %{version}-%{release}
Requires:       python3

%description -n python3-%{name}
This package provides the python3 interface to AppArmor. It is used for python
applications interfacing with AppArmor.

%package -n     perl-%{name}
Summary:        AppArmor module for perl.
License:        GNU LGPL v2.1
Group:          Development/Libraries/Perl
Requires:       libapparmor = %{version}-%{release}

%description -n perl-%{name}
This package contains the AppArmor module for perl.

%prep
%autosetup -p1 -n %{name}-%{version}

%build
#Building libapparmor
cd ./libraries/libapparmor
export LD_LIBRARY_PATH="$LD_LIBRARY_PATH:%{_libdir}"
/sbin/ldconfig
sh ./autogen.sh

%configure \
    --with-perl \
    --with-python

%make_build

#Building Binutils
cd ../../binutils/
%make_build

#Building parser
cd ../parser
export LD_LIBRARY_PATH="$LD_LIBRARY_PATH:%{_libdir}"
export LIBRARY_PATH="$LIBRARY_PATH:%{_libdir}"
echo $LD_LIBRARY_PATH
echo $LIBRARY_PATH
%make_build

#Building Utilities
cd ../utils
%make_build

#Building Apache mod_apparmor
cd ../changehat/mod_apparmor
%make_build

#Building PAM AppArmor
cd ../pam_apparmor
%make_build

#Building Profiles
cd ../../profiles
%make_build

%check
pip3 install pyflakes
export PYTHONPATH=%{python3_sitelib}
export PYTHON=%{python3}
export PYTHON_VERSION=%{python3_version}
export PYTHON_VERSIONS=python3
export LD_LIBRARY_PATH="$LD_LIBRARY_PATH:%{_libdir}"

cd ./libraries/libapparmor
make check %{?_smp_mflags}

cd ../../binutils/
make check %{?_smp_mflags}

cd ../utils
make check %{?_smp_mflags}

%install
export PYTHONPATH=%{python3_sitelib}
export PYTHON=%{python3}
export PYTHON_VERSION=%{python3_version}
export PYTHON_VERSIONS=python3
export LD_LIBRARY_PATH="$LD_LIBRARY_PATH:%{_libdir}"

cd libraries/libapparmor
%make_install %{?_smp_mflags}

cd ../../binutils/
%make_install %{?_smp_mflags}

cd ../parser
%make_install %{?_smp_mflags}
cd ../utils

%make_install %{?_smp_mflags}

cd ../changehat/mod_apparmor
%make_install %{?_smp_mflags}

cd ../pam_apparmor
%make_install %{?_smp_mflags}

cd ../../profiles
%make_install %{?_smp_mflags}

%files -n libapparmor
%defattr(-,root,root)
%{_libdir}/libapparmor.so.*

%post -n libapparmor
/sbin/ldconfig

%postun -n libapparmor
/sbin/ldconfig

%files -n libapparmor-devel
%defattr(-,root,root)
%{_libdir}/libapparmor.a
%{_libdir}/libapparmor.so
%{_libdir}/pkgconfig/libapparmor.pc
%dir %{_includedir}/aalogparse
%dir %{_includedir}/sys
%{_includedir}/aalogparse/*
%{_includedir}/sys/*
%doc %{_mandir}/man2/aa_change_hat.2.gz
%doc %{_mandir}/man2/aa_find_mountpoint.2.gz
%doc %{_mandir}/man2/aa_getcon.2.gz
%doc %{_mandir}/man2/aa_query_label.2.gz
%doc %{_mandir}/man3/aa_features.3.gz
%doc %{_mandir}/man3/aa_kernel_interface.3.gz
%doc %{_mandir}/man3/aa_policy_cache.3.gz
%doc %{_mandir}/man3/aa_splitcon.3.gz

%files -n apache2-mod_apparmor
%defattr(-,root,root)
%{_libdir}/httpd/modules/mod_apparmor.so
%doc %{_mandir}/man8/mod_apparmor.8.gz

%files profiles
%defattr(-,root,root,755)
%dir %{_sysconfdir}/%{name}.d/apache2.d
%config(noreplace) %{_sysconfdir}/%{name}.d/apache2.d/phpsysinfo
%config(noreplace) %{_sysconfdir}/%{name}.d/bin.*
%config(noreplace) %{_sysconfdir}/%{name}.d/sbin.*
%config(noreplace) %{_sysconfdir}/%{name}.d/usr.*
%config(noreplace) %{_sysconfdir}/%{name}.d/local/*
%config(noreplace) %{_sysconfdir}/%{name}.d/samba-*
%config(noreplace) %{_sysconfdir}/%{name}.d/zgrep
/lib/%{name}/profile-load
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/extra-profiles/*

%files parser
%defattr(755,root,root,755)
/sbin/apparmor_parser
/sbin/rcapparmor
/lib/%{name}/rc.%{name}.functions
/lib/%{name}/%{name}.systemd
%{_bindir}/aa-exec
%{_bindir}/aa-enabled
%attr(644,root,root) %{_unitdir}/%{name}.service
%dir %{_sysconfdir}/%{name}
%dir %{_sysconfdir}/%{name}.d
%config(noreplace) %{_sysconfdir}/%{name}/parser.conf
%{_localstatedir}/lib/%{name}
%doc %{_mandir}/man5/%{name}.d.5.gz
%doc %{_mandir}/man5/%{name}.vim.5.gz
%doc %{_mandir}/man7/%{name}.7.gz
%doc %{_mandir}/man8/apparmor_parser.8.gz
%doc %{_mandir}/man1/aa-enabled.1.gz
%doc %{_mandir}/man1/aa-exec.1.gz
%doc %{_mandir}/man2/aa_stack_profile.2.gz

%preun parser
%systemd_preun %{name}.service

%post parser
%systemd_post %{name}.service

%postun parser
%systemd_postun_with_restart %{name}.service

%files abstractions
%defattr(644,root,root,755)
%dir %{_sysconfdir}/%{name}.d/abstractions
%config(noreplace) %{_sysconfdir}/%{name}.d/abstractions/*
%config(noreplace) %{_sysconfdir}/%{name}.d/lsb_release
%config(noreplace) %{_sysconfdir}/%{name}.d/nvidia_modprobe
%dir %{_sysconfdir}/%{name}.d/disable
%dir %{_sysconfdir}/%{name}.d/local
%dir %{_sysconfdir}/%{name}.d/tunables
%dir %{_sysconfdir}/%{name}.d/abi
%config(noreplace) %{_sysconfdir}/%{name}.d/php-fpm
%config(noreplace) %{_sysconfdir}/%{name}.d/tunables/*
%config(noreplace) %{_sysconfdir}/%{name}.d/abi/*
%exclude %{_datadir}/locale

%files utils
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/%{name}/easyprof.conf
%config(noreplace) %{_sysconfdir}/%{name}/logprof.conf
%config(noreplace) %{_sysconfdir}/%{name}/notify.conf
%config(noreplace) %{_sysconfdir}/%{name}/severity.db
%{_sbindir}/aa-*
%{_sbindir}/apparmor_status
%{_bindir}/aa-easyprof
%{_bindir}/aa-features-abi
%{_datadir}/%{name}/easyprof/
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/%{name}.vim
%doc %{_mandir}/man1/aa-features-abi.1.gz
%doc %{_mandir}/man2/aa_change_profile.2.gz
%doc %{_mandir}/man5/logprof.conf.5.gz
%doc %{_mandir}/man8/aa-*.gz
%doc %{_mandir}/man8/apparmor_status.8.gz
%doc %{_mandir}/man7/apparmor_xattrs.7.gz

%files -n pam_apparmor
%defattr(-,root,root,755)
/lib/security/pam_apparmor.so

%files -n python3-%{name}
%defattr(-,root,root)
%{python3_sitelib}/*

%files -n perl-%{name}
%defattr(-,root,root)
%{perl_vendorarch}/auto/LibAppArmor/
%{perl_vendorarch}/LibAppArmor.pm
%exclude %{perl_archlib}/perllocal.pod

%changelog
* Thu Dec 08 2022 Dweep Advani <dadvani@vmware.com> 3.1.1-2
- Perl version upgrade to 5.36.0
* Thu Nov 03 2022 Nitesh Kumar <kunitesh@vmware.com> 3.1.1-1
- Version upgrade to v3.1.1
* Sun Aug 07 2022 Shreenidhi Shedi <sshedi@vmware.com> 3.0.4-3
- Remove .la files
* Mon Jun 20 2022 Nitesh Kumar <kunitesh@vmware.com> 3.0.4-2
- Bump version as a part of httpd v2.4.54 upgrade
* Mon Apr 18 2022 Gerrit Photon <photon-checkins@vmware.com> 3.0.4-1
- Automatic Version Bump
* Tue Oct 19 2021 Shreenidhi Shedi <sshedi@vmware.com> 3.0.3-1
- Upgrade to 3.0.3
* Thu Oct 07 2021 Dweep Advani <dadvani@vmware.com> 3.0.1-3
- Rebuild with upgraded httpd 2.4.50
* Tue Oct 05 2021 Shreenidhi Shedi <sshedi@vmware.com> 3.0.1-2
- Bump version as a part of httpd upgrade
* Mon Apr 12 2021 Gerrit Photon <photon-checkins@vmware.com> 3.0.1-1
- Automatic Version Bump
* Fri Nov 06 2020 Tapas Kundu <tkundu@vmware.com> 3.0.0-3
- Build with python 3.9
* Fri Oct 23 2020 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 3.0.0-2
- Fix build failure in apparmor on linux 5.9-rc7
* Thu Oct 01 2020 Gerrit Photon <photon-checkins@vmware.com> 3.0.0-1
- Automatic Version Bump
* Tue Sep 29 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 2.13.4-2
- openssl 1.1.1
* Wed Aug 26 2020 Gerrit Photon <photon-checkins@vmware.com> 2.13.4-1
- Automatic Version Bump
* Sun Jul 26 2020 Tapas Kundu <tkundu@vmware.com> 2.13-8
- Updated using python 3.8 libs
* Tue Mar 05 2019 Siju Maliakkal <smaliakkal@vmware.com> 2.13-7
- Excluded conflicting perllocal.pod
* Thu Dec 06 2018 Keerthana K <keerthanak@vmware.com> 2.13-6
- Fixed make check failures.
* Fri Oct 05 2018 Tapas Kundu <tkundu@vmware.com> 2.13-5
- Updated using python 3.7 libs
* Wed Oct 03 2018 Keerthana K <keerthanak@vmware.com> 2.13-4
- Depcrecated ruby apparmor package.
- Modified the perl and python path to generic.
* Wed Sep 26 2018 Ajay Kaher <akaher@vmware.com> 2.13-3
- Fix for aarch64
* Thu Sep 20 2018 Keerthana K <keerthanak@vmware.com> 2.13-2
- Updated the ruby packagefor latest version.
* Thu Aug 30 2018 Keerthana K <keerthanak@vmware.com> 2.13-1
- Initial Apparmor package for Photon.
