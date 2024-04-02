Summary:        Photon upgrade scripts
Name:           photon-upgrade
Version:        1.0
Release:        21%{?dist}
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
Source6:        ph3-to-ph4-deprecated-pkgs.txt
Source7:        ph3-to-ph5-deprecated-pkgs.txt

BuildArch:      noarch

Requires:       tdnf
Requires:       rpm
Requires:       coreutils
Requires:       gawk
Requires:       sed
Requires:       photon-release
Requires:       findutils
Requires:       util-linux

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
install -m440 %{SOURCE6} %{buildroot}%{_libdir}/%{name}
install -m440 %{SOURCE7} %{buildroot}%{_libdir}/%{name}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_bindir}/*
%{_libdir}/*

%changelog
* Tue Apr 02 2024 Dweep Advani <dweep.advani@broadcom.com> 1.0-21
- Upgrade to installed package name only whenever possible
- deprecate libnss-ato in 3.0 to 5.0 upgrade
* Tue Mar 12 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.0-20
- Add ktap to deprecated package list
* Fri Mar 01 2024 Dweep Advani <dweep.advani@broadcom.com> 1.0-19
- Support upgrading to apache-tomcat9 in 4.0 from apache-tomcat in 3.0
* Wed Dec 06 2023 Dweep Advani <dadvani@vmware.com> 1.0-18
- Only backup and restore modified config files of erased and reinstalled packages
- Remove pycrypto from replaced packages map
* Mon Nov 27 2023 Dweep Advani <dadvani@vmware.com> 1.0-17
- Enhance handling of extra removed packages and config backup
* Wed Oct 25 2023 Vamsi Krishna Brahmajosuyula <vbrahmajosyula@vmware.com> 1.0-16
- Change default tomcat upgrade target to apache-tomcat10
- Rename apache-tomcat-9 to apache-tomcat9
* Wed Oct 11 2023 Dweep Advani <dadvani@vmware.com> 1.0-15
- Validates repo correctness, timestamp logs and restores config to apache-tomcat-9
* Thu Sep 28 2023 Shreenidhi Shedi <sshedi@vmware.com> 1.0-14
- Handle repmgr, apache-tomcat during OS upgrades
- Add rpm to requires
* Tue Sep 05 2023 Dweep Advani <dadvani@vmware.com> 1.0-13
- Single transaction OS upgrade
* Fri Sep 01 2023 Dweep Advani <dadvani@vmware.com> 1.0-12
- Reordering service configuration resetting and enahncing pre upgrade package error reporting
* Mon Jun 19 2023 Dweep Advani <dadvani@vmware.com> 1.0-11
- Fix stig-hardening issue
* Thu Jun 15 2023 Dweep Advani <dadvani@vmware.com> 1.0-10
- Fix python3-pycrypto remval issue in 3.0 to 5.0 upgrade
* Fri Jun 09 2023 Dweep Advani <dadvani@vmware.com> 1.0-9
- Bug fixes of listing installed packages and updating current release
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
