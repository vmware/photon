Summary:        Photon upgrade scripts
Name:           photon-upgrade
Version:        1.0
Release:        7%{?dist}
License:        Apache License
Group:          System Environment/Base
Source0:        photon-upgrade.sh
URL:            https://vmware.github.io/photon/
Vendor:         VMware, Inc.
Distribution:   Photon
BuildArch:      noarch
Requires:       tdnf
Requires:       coreutils
Requires:       gawk
Requires:       sed

%description
Photon major upgrade scripts. Addresses 3.0 to 4.0 upgrades.

%prep

%build

%install
mkdir -p %{buildroot}%{_bindir}
install -m755 %{SOURCE0} %{buildroot}%{_bindir}

%post

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_bindir}/*

%changelog
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
