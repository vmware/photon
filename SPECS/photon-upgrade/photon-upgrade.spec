Summary:        Photon upgrade scripts
Name:           photon-upgrade
Version:        1.0
Release:        5%{?dist}
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

BuildArch:      noarch

Requires:       tdnf
Requires:       (coreutils or coreutils-selinux)
Requires:       gawk
Requires:       sed

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

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_bindir}/*
%{_libdir}/*

%changelog
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
