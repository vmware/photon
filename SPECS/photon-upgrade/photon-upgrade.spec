Summary:        Photon upgrade scripts
Name:           photon-upgrade
Version:        1.0
Release:        19%{?dist}
License:        Apache License
Group:          System Environment/Base
URL:            https://vmware.github.io/photon
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: photon-upgrade.sh
Source1: constants.sh
Source2: ph4-to-ph5-upgrade.sh
Source3: utils.sh
Source4: common.sh
Source5: ph4-to-ph5-deprecated-pkgs.txt

BuildArch:      noarch

Requires:       (coreutils or coreutils-selinux)
Requires:       gawk
Requires:       sed
Requires:       rpm
Requires:       tdnf
Requires:       photon-release
Requires:       findutils
Requires:       util-linux

%description
Photon upgrade scripts for updating the packages and
upgrading the Photon OS from 4.0 to 5.0.

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
* Wed Apr 03 2024 Dweep Advani <dweep.advani@broadcom.com> 1.0-19
- Prefer upgrading to the same package name when upgrading OS
* Fri Mar 29 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.0-18
- Remove libnss-ato from deprecated package list
- libnss-ato is re-added to Ph5 based on https://github.com/donapieppo/libnss-ato/issues/21
* Fri Mar 22 2024 Dweep Advani <dweep.advani@broadcom.com> 1.0-17
- Fix corner case of cleanup wrongly triggering during 4.0 to 4.0 update
* Tue Mar 12 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.0-16
- Add ktap to deprecated package list
* Fri Feb 16 2024 Dweep Advani <dweep.advani@broadcom.com> 1.0-15
- Add feature to update to other availabe package within 4.0 having different name
* Thu Feb 01 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.0-14
- Add copenapi to deprecated packages list
* Tue Jan 30 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 1.0-13
- Added rubygem-base64, rubygem-drb, rubygem-connection_pool, rubygem-ruby2-keywords
- packages to ph4-to-ph5-deprecated-pkgs list
* Wed Dec 06 2023 Dweep Advani <dadvani@vmware.com> 1.0-12
- Enhance handling of extra removed packages and config backup
* Mon Oct 16 2023 Dweep Advani <dadvani@vmware.com> 1.0-11
- Validates repo correctness, timestamp logs and restores config to apache-tomcat-9
* Tue Oct 10 2023 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 1.0-10
- Add REPOS_OPT to removal step of unsupported packages
* Thu Sep 28 2023 Shreenidhi Shedi <sshedi@vmware.com> 1.0-9
- Handle epmgr, apache-tomcat upgrades
* Mon Sep 04 2023 Dweep Advani <dadvani@vmware.com> 1.0-8
- Reordering service configuration resetting and enahncing pre upgrade package error reporting
* Tue Jun 20 2023 Dweep Advani <dadvani@vmware.com> 1.0-7
- Support --to-ver, --rm-pkgs-pre and --rm-pkgs-post
* Fri Jun 09 2023 Dweep Advani <dadvani@vmware.com> 1.0-6
- Deprecate salt3 for 5.0 and enhance logic for installed package lookup
* Wed May 31 2023 Shreenidhi Shedi <sshedi@vmware.com> 1.0-5
- Revamp scripts
* Thu Apr 20 2023 Dweep Advani <dadvani@vmware.com> 1.0-4
- Fixed issue caused by change in behaviour of tdnf list command
* Thu Mar 16 2023 Dweep Advani <dadvani@vmware.com> 1.0-3
- Added support for OS upgrade to 5.0 release
* Thu Sep 08 2022 Dweep Advani <dadvani@vmware.com> 1.0-2
- Added feature to install all packages from provided repo
* Mon Aug 29 2022 Dweep Advani <dadvani@vmware.com> 1.0-1
- Initial version
