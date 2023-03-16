Summary:        Photon upgrade scripts
Name:           photon-upgrade
Version:        1.0
Release:        3%{?dist}
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
Photon upgrade scripts for updating the packages and
upgrading the Photon OS from 4.0 to 5.0.

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
* Thu Mar 16 2023 Dweep Advani <dadvani@vmware.com> 1.0-3
- Added support for OS upgrade to 5.0 release
* Thu Sep 08 2022 Dweep Advani <dadvani@vmware.com> 1.0-2
- Added feature to install all packages from provided repo
* Mon Aug 29 2022 Dweep Advani <dadvani@vmware.com> 1.0-1
- Initial version
