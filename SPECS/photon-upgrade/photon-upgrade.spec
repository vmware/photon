Summary:        Photon upgrade scripts
Name:           photon-upgrade
Version:        1.1
Release:        2%{?dist}
Group:          System Environment/Base
URL:            https://vmware.github.io/photon
Vendor:         VMware, Inc.
Distribution:   Photon

BuildArch:      noarch

Source0:        photon-upgrade.sh
Source1:        constants.sh
Source2:        ph5-to-ph6-upgrade.sh
Source3:        utils.sh
Source4:        common.sh
Source5:        ph5-deprecated-pkgs.txt

Source6: license.txt
%include %{SOURCE6}

Source7:       %{name}-completion.sh

Requires:       rpm
Requires:       tdnf
Requires:       gawk
Requires:       sed
Requires:       (coreutils or coreutils-selinux)
Requires:       photon-release
Requires:       findutils
Requires:       util-linux

%description
Provides functionalities to upgrade Photon OS 5.0 to newer release and
update installed packages to the latest available versions in 5.0.

%prep

%build

%install
mkdir -p %{buildroot}%{_bindir} %{buildroot}%{_libdir}/%{name}
install -m550 %{SOURCE0} %{buildroot}%{_bindir}
install -m440 %{SOURCE1} %{buildroot}%{_libdir}/%{name}
install -m440 %{SOURCE2} %{buildroot}%{_libdir}/%{name}
install -m440 %{SOURCE3} %{buildroot}%{_libdir}/%{name}
install -m440 %{SOURCE4} %{buildroot}%{_libdir}/%{name}
install -m440 %{SOURCE5} %{buildroot}%{_libdir}/%{name}
install -D -m 644 %{SOURCE7} %{buildroot}%{_datadir}/bash-completion/completions/%{name}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_bindir}/*
%{_libdir}/*
%{_datadir}/bash-completion/completions/%{name}

%changelog
* Wed Jun 17 2026 Dweep Advani <dweep.advani@broadcom.com> 1.1-2
- Include appliance rpms in --install-all
* Tue Jun 09 2026 Dweep Advani <dweep.advani@broadcom.com> 1.1-1
- Support latest 5.0 package changes
* Fri Dec 12 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.0-9
- Add bash completion script
* Thu Dec 04 2025 Dweep Advani <dweep.advani@broadcom.com> 1.0-8
- Avoid removing deprecated packages during update of OS to avoid any side effects
* Mon Dec 01 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.0-7
- Validate install_all_from repo return value
- Remove replacement package mapping for package updates in same OS version
* Fri Nov 14 2025 Dweep Advani <dweep.advani@broadcom.com> 1.0-6
- Deprecated and replaced packages update
* Wed Dec 11 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.0-5
- Release bump for SRP compliance
* Tue Oct 22 2024 Dweep Advani <dweep.advani@broadcom.com> 1.0-4
- Removes validation of repo while updating OS packages
* Fri Jan 12 2024 Dweep Advani <dweep.advani@broadcom.com> 1.0-3
- Enhancements of backup/restore configs, prechecks, logging
* Thu Sep 28 2023 Shreenidhi Shedi <sshedi@vmware.com> 1.0-2
- Reordering service configuration resetting and enhancing pre upgrade package error reporting
* Thu Jun 08 2023 Dweep Advani <dadvani@vmware.com> 1.0-1
- Initial photon-upgrade package for Photon OS 5.0
