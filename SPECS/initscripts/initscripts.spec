Summary:        Scripts to bring up network interfaces and legacy utilities
Name:           initscripts
Version:        10.17
Group:          System Environment/Base
Release:        4%{?dist}
URL:            https://github.com/fedora-sysv/initscripts
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://github.com/fedora-sysv/initscripts/archive/%{name}-%{version}.tar.gz
%define sha512 %{name}=6c99a7b52b5bc0ced1877a7b2a280b885778bb12e89dc0d606a5b5eda1aa87feecdea6c19803afab01953c9d352c409e59665914832f7107b6b3816d4740594c

Source1: adjtime
Source2: networks

Source3: license.txt
%include %{SOURCE3}

Patch0: 0001-use-systemctl-to-manage-services.patch

Requires: systemd
Requires: iproute2
Requires: util-linux
Requires: findutils

BuildRequires: glib-devel
BuildRequires: python3-devel
BuildRequires: popt-devel
BuildRequires: gettext
BuildRequires: pkg-config
BuildRequires: systemd-devel

Provides: /sbin/service

%description
This package contains the script that activates and deactivates most
network interfaces, some utilities, and other legacy files.

%package -n     netconsole-service
Summary:        Service for initializing of network console logging
Requires:       %{name} = %{version}-%{release}
Requires:       iputils
Requires:       kmod
Requires:       sed

BuildArch:      noarch

%description -n netconsole-service
This packages provides a 'netconsole' service for loading of netconsole kernel
module with the configured parameters. The netconsole kernel module itself then
allows logging of kernel messages over the network.

%package -n     readonly-root
Summary:        Service for configuring read-only root support
Requires:       %{name} = %{version}-%{release}
Requires:       cpio

BuildArch:      noarch

%description -n readonly-root
This package provides script & configuration file for setting up read-only root
support. Additional configuration is required after installation.

%prep
%autosetup -p1

%build
%make_build PYTHON=%{python3}

%install
%make_install %{?_smp_mflags}

%find_lang %{name}

rm -f %{buildroot}%{_sysconfdir}/sysconfig/network-scripts/ifup-ctc

# Additional ways to access documentation:
install -m 0755 -d %{buildroot}%{_docdir}/network-scripts

ln -srv %{buildroot}%{_docdir}/%{name}-%{version}/sysconfig.txt \
       %{buildroot}%{_docdir}/network-scripts/

ln -srv %{buildroot}%{_mandir}/man8/ifup.8 \
       %{buildroot}%{_mandir}/man8/ifdown.8

cp %{SOURCE1} %{SOURCE2} %{buildroot}%{_sysconfdir}/

mkdir -p %{buildroot}%{_sysconfdir}/{rwtab.d,statetab.d} \
         %{buildroot}%{_sysconfdir}/NetworkManager/dispatcher.d

%post
%systemd_post import-state.service loadmodules.service

%preun
%systemd_preun import-state.service loadmodules.service

%postun
%systemd_postun import-state.service loadmodules.service

%post -n netconsole-service
%systemd_post netconsole.service

%preun -n netconsole-service
%systemd_preun netconsole.service

%postun -n netconsole-service
%systemd_postun netconsole.service

%post -n readonly-root
%systemd_post readonly-root.service

%preun -n readonly-root
%systemd_preun readonly-root.service

%postun -n readonly-root
%systemd_postun readonly-root.service

%files -f %{name}.lang
%defattr(-,root,root)
%license COPYING
%doc doc/sysconfig.txt

# NOTE: /etc/sysconfig/ is owned by filesystem package.
%dir %{_sysconfdir}/rc.d
%dir %{_sysconfdir}/rc.d/init.d
%dir %{_sysconfdir}/rc.d/rc[0-6].d
%dir %{_sysconfdir}/sysconfig/modules
%dir %{_libexecdir}/%{name}
%dir %{_libexecdir}/%{name}/legacy-actions
%exclude %{_sysconfdir}/sysconfig/console
%{_sysconfdir}/rc.d/init.d/functions

# RC symlinks:
%{_sysconfdir}/rc[0-6].d
%{_sysconfdir}/init.d

%{_bindir}/*
%{_sbindir}/consoletype
%{_sbindir}/genhostid
%{_sbindir}/service
%{_libexecdir}/import-state
%{_libexecdir}/loadmodules
%{_unitdir}/import-state.service
%{_unitdir}/loadmodules.service
%{_libdir}/udev/rename_device
%{_udevrulesdir}/*
%{_mandir}/man1/*
%{_mandir}/man8/service.*

# network-scripts
%doc doc/examples/
%dir %{_sysconfdir}/sysconfig/network-scripts
%{_sysconfdir}/rc.d/init.d/network
%{_sysconfdir}/sysconfig/network-scripts/*
%config(noreplace) %{_sysconfdir}/sysconfig/network-scripts/ifcfg-lo
%config(noreplace) %{_sysconfdir}/networks
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/adjtime

%attr(4755,root,root) %{_sbindir}/usernetctl
%{_mandir}/man8/ifup.*
%{_mandir}/man8/ifdown.*
%{_mandir}/man8/usernetctl.*
%{_docdir}/network-scripts/*

%dir %{_sysconfdir}/NetworkManager
%dir %{_sysconfdir}/NetworkManager/dispatcher.d

%files -n netconsole-service
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/sysconfig/netconsole
%{_libexecdir}/netconsole
%{_unitdir}/netconsole.service

%files -n readonly-root
%defattr(-,root,root)
%dir %{_sharedstatedir}/stateless
%dir %{_sharedstatedir}/stateless/state
%dir %{_sharedstatedir}/stateless/writable
%dir %{_sysconfdir}/rwtab.d
%dir %{_sysconfdir}/statetab.d
%config(noreplace) %{_sysconfdir}/rwtab
%config(noreplace) %{_sysconfdir}/statetab
%config(noreplace) %{_sysconfdir}/sysconfig/readonly-root
%{_libexecdir}/readonly-root
%{_unitdir}/readonly-root.service

%changelog
* Wed Dec 11 2024 Tapas Kundu <tapas.kundu@broadcom.com> 10.17-4
- Release bump for SRP compliance
* Thu Nov 23 2023 Shreenidhi Shedi <sshedi@vmware.com> 10.17-3
- Spec clanups
- Add patch to manage services using systemctl.
* Sat Jan 14 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 10.17-2
- Bump version as a part of gettext upgrade
* Fri Oct 28 2022 Gerrit Photon <photon-checkins@vmware.com> 10.17-1
- Automatic Version Bump
* Mon Apr 18 2022 Gerrit Photon <photon-checkins@vmware.com> 10.16-1
- Automatic Version Bump
* Tue Apr 13 2021 Gerrit Photon <photon-checkins@vmware.com> 10.09-1
- Automatic Version Bump
* Wed Jul 22 2020 Ankit Jain <ankitja@vmware.com> 10.04-1
- Updated to 10.04
* Tue Jun 23 2020 Tapas Kundu <tkundu@vmware.com> 9.70-4
- Build using python3
* Sat Jan 05 2019 Ankit Jain <ankitja@vmware.com> 9.70-3
- Added network configuration to fix "service --status-all"
* Tue Dec 26 2017 Divya Thaluru <dthaluru@vmware.com> 9.70-2
- Fixed return code in /etc/init.d/functions bash script
* Mon Apr 3 2017 Dheeraj Shetty <dheerajs@vmware.com> 9.70-1
- Updated to version 9.70
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 9.65-2
- GA - Bump release of all rpms
* Fri Feb 12 2016 Divya Thaluru <dthaluru@vmware.com> 9.65-2
- Fixing service script to start services using systemctl by default
* Tue Jan 26 2016 Xiaolin Li <xiaolinl@vmware.com> 9.65-1
- Updated to version 9.65
* Mon Jul 20 2015 Divya Thaluru <dthaluru@vmware.com> 9.63-1
- Got Spec file from source tar ball and modified it to be compatible to build in Photon.
