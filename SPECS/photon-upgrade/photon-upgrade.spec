Summary:        Photon upgrade scripts
Name:           photon-upgrade
Version:        1.0
Release:        4%{?dist}
License:        Apache License
Group:          System Environment/Base
URL:            https://vmware.github.io/photon
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        photon-upgrade.sh
Source1:        constants.sh
Source2:        ph5-to-ph6-upgrade.sh
Source3:        utils.sh
Source4:        common.sh
Source5:        ph5-to-ph6-deprecated-pkgs.txt

BuildArch:      noarch

Requires:       rpm
Requires:       tdnf
Requires:       coreutils
Requires:       gawk
Requires:       sed
Requires:       coreutils >= 9.1-7
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

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_bindir}/*
%{_libdir}/*

%changelog
* Tue Oct 22 2024 Dweep Advani <dweep.advani@broadcom.com> 1.0-4
- Removes validation of repo while updating OS packages
* Fri Jan 12 2024 Dweep Advani <dweep.advani@broadcom.com> 1.0-3
- Enhancements of backup/restore configs, prechecks, logging
* Thu Sep 28 2023 Shreenidhi Shedi <sshedi@vmware.com> 1.0-2
- Reordering service configuration resetting and enhancing pre upgrade package error reporting
* Thu Jun 08 2023 Dweep Advani <dadvani@vmware.com> 1.0-1
- Initial photon-upgrade package for Photon OS 5.0
