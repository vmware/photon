Name:           apparmor
Version:        3.1.2
Release:        13%{?dist}
Summary:        AppArmor is an effective and easy-to-use Linux application security system.
License:        GNU LGPL v2.1
URL:            https://launchpad.net/apparmor
Vendor:         VMware, Inc.
Distribution:   Photon
Group:          Productivity/Security

Source0: https://launchpad.net/%{name}/3.1/%{version}/+download/%{name}-%{version}.tar.gz
%define sha512 %{name}=e4fa8e0985472c00d3b68044f4150659787cf15b384b901af32b5aba3f0b2839f33bfe0b0675bf8ea7a1f5727152756a276c75b1dec383a33b92b0a1b8615a11

Patch0: 0001-fix-syslog-ng-profile.patch

BuildRequires: perl
BuildRequires: python3-devel
BuildRequires: swig
BuildRequires: build-essential
BuildRequires: gawk
BuildRequires: which
BuildRequires: libstdc++-devel
BuildRequires: httpd
BuildRequires: httpd-devel
BuildRequires: httpd-tools
BuildRequires: apr
BuildRequires: apr-util-devel
BuildRequires: Linux-PAM-devel
BuildRequires: dejagnu
BuildRequires: openssl-devel
BuildRequires: curl-devel
BuildRequires: python3-setuptools
BuildRequires: python3-xml
BuildRequires: bison

%if 0%{?with_check}
BuildRequires: python3-pip
BuildRequires: python3-pyflakes
BuildRequires: cmake
BuildRequires: dbus-devel
BuildRequires: glib-devel
%endif

Requires: openssl

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
Requires:       %{name}-abstractions = %{version}-%{release}

%description    profiles
This package contains the basic AppArmor profiles.

%package        parser
Summary:        AppArmor userlevel parser utility
License:        GNU LGPL v2.1
Group:          Productivity/Security
Requires:       libapparmor = %{version}-%{release}
Requires:       systemd
Requires:       %{name}-profiles = %{version}-%{release}

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
Requires:       python3-%{name} = %{version}-%{release}
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
pushd ./libraries/libapparmor
sh ./autogen.sh

%configure \
    --with-perl \
    --with-python

%make_build
popd

for target in binutils \
              parser \
              utils \
              changehat/mod_apparmor \
              changehat/pam_apparmor \
              profiles; do
%make_build -C ${target}
done

%install
for target in libraries/libapparmor \
              binutils \
              parser \
              utils \
              changehat/mod_apparmor \
              changehat/pam_apparmor \
              profiles; do
%make_install %{?_smp_mflags} -C ${target}
done

%make_install %{?_smp_mflags} -C parser install-systemd

mv %{buildroot}/lib/* %{buildroot}%{_libdir}
mv %{buildroot}/sbin/* %{buildroot}%{_sbindir}

%check
pip3 install notify2 dbus-python psutil
ln -sfv %{_bindir}/pyflakes %{_bindir}/pyflakes3

for target in libraries/libapparmor \
              binutils \
              utils; do
%make_build check -C ${target}
done

%post -n libapparmor
/sbin/ldconfig

%postun -n libapparmor
/sbin/ldconfig

%preun parser
%systemd_preun %{name}.service

%post parser
%systemd_post %{name}.service

%postun parser
%systemd_postun_with_restart %{name}.service

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)

%files -n libapparmor
%defattr(-,root,root)
%{_libdir}/libapparmor.so.*

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
%{_libdir}/%{name}/profile-load
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/extra-profiles/*

%files parser
%defattr(755,root,root,755)
%{_sbindir}/%{name}_parser
%{_libdir}/%{name}/%{name}.systemd
%{_unitdir}/%{name}.service
%{_libdir}/%{name}/rc.%{name}.functions
%{_bindir}/aa-exec
%{_bindir}/aa-enabled
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
%{_libdir}/security/pam_apparmor.so

%files -n python3-%{name}
%defattr(-,root,root)
%{python3_sitelib}/*

%files -n perl-%{name}
%defattr(-,root,root)
%{perl_vendorarch}/auto/LibAppArmor/
%{perl_vendorarch}/LibAppArmor.pm
%exclude %{perl_archlib}/perllocal.pod

%changelog
* Tue Apr 16 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 3.1.2-13
- Bump version as a part of dbus upgrade
* Fri Apr 05 2024 Nitesh Kumar <nitesh-nk.kumar@broadcom.com> 3.1.2-12
- Version Bump up to consume httpd v2.4.59
* Wed Mar 13 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 3.1.2-11
- sbin.syslog-ng profile fix
* Wed Mar 06 2024 Ashwin Dayanand Kamat <ashwin.kamat@broadcom.com> 3.1.2-10
- Bump version as a part of apr upgrade
* Sun Nov 19 2023 Shreenidhi Shedi <sshedi@vmware.com> 3.1.2-9
- Bump version as a part of openssl upgrade
* Mon Oct 30 2023 Nitesh Kumar <kunitesh@vmware.com> 3.1.2-8
- Bump version as a part of httpd v2.4.58 upgrade
* Fri Sep 29 2023 Nitesh Kumar <kunitesh@vmware.com> 3.1.2-7
- Bump version as a part of apr-util v1.6.3 upgrade
* Tue Apr 11 2023 Guruswamy Basavaiah <bguruswamy@vmware.com> 3.1.2-6
- Added apparmor-parser dependency on apparmor-profiles
* Mon Apr 03 2023 Nitesh Kumar <kunitesh@vmware.com> 3.1.2-5
- Bump version as a part of httpd v2.4.56 upgrade
* Tue Jan 31 2023 Guruswamy Basavaiah <bguruswamy@vmware.com> 3.1.2-4
- Added apparmor-utils dependency on python3-apparmor
* Mon Jan 30 2023 Nitesh Kumar <kunitesh@vmware.com> 3.1.2-3
- Bump version as a part of httpd v2.4.55 upgrade
* Thu Jan 12 2023 Him Kalyan Bordoloi <bordoloih@vmware.com> 3.1.2-2
- Bump up version no. as part of swig upgrade
* Thu Dec 15 2022 Shreenidhi Shedi <sshedi@vmware.com> 3.1.2-1
- Upgrade to v3.1.2
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
