Summary:        Photon upgrade scripts
Name:           photon-upgrade
Version:        1.0
Release:        8%{?dist}
License:        Apache License
Group:          System Environment/Base
URL:            https://vmware.github.io/photon
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        photon-upgrade.sh
Source1:        constants.sh
Source2:        ph3-to-ph4-upgrade.sh
Source3:        ph3-to-ph5-upgrade.sh
Source4:        utils.sh
Source5:        common.sh

BuildArch:      noarch

Requires:       tdnf
Requires:       coreutils
Requires:       gawk
Requires:       sed

%description
Photon major upgrade scripts.
Addresses 3.0 to 4.0 and 3.0 to 5.0 upgrades.

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
* Wed May 24 2023 Dweep Advani <dadvani@vmware.com> 1.0-8
- Revamped package to support both 3.0 to 4.0 and 3.0 to 5.0 upgrade
* Wed Apr 19 2023 Dweep Advani <dadvani@vmware.com> 1.0-7
- Changed few exit codes and support for removing named packages pre and post upgrade
* Wed Nov 23 2022 Dweep Advani <dadvani@vmware.com> 1.0-6
- Fix PAM configuration and explicitly enable networkd and resolved
* Thu Sep 08 2022 Dweep Advani <dadvani@vmware.com> 1.0-5
- Added feature to install all packages from provided repo
* Wed Aug 17 2022 Dweep Advani <dadvani@vmware.com> 1.0-4
- Comment out unsupported FipsMode in /etc/ssh/sshd_config
* Thu Jul 21 2022 Dweep Advani <dadvani@vmware.com> 1.0-3
- Added support for appliance upgrade use case
* Fri Jan 14 2022 Dweep Advani <dadvani@vmware.com> 1.0-2
- Updated for 4.0  release udpates
* Mon Oct 12 2020 Dweep Advani <dadvani@vmware.com> 1.0-1
- Initial Photon 3.0 to 4.0 upgrade package
