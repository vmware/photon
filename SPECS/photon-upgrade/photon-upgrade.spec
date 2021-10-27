Summary:        Photon upgrade scripts
Name:           photon-upgrade
Version:        1.0
Release:        2%{?dist}
License:        Apache License
Group:          System Environment/Base
Source0:        photon-upgrade.sh
URL:            https://vmware.github.io/photon/
Vendor:         VMware, Inc.
Distribution:   Photon
BuildArch:      noarch
Requires:       tdnf

%description
Photon major upgrade scripts. Addresses 3.0 to 4.0 upgrades.

%prep

%build

%install
mkdir -p %{buildroot}%{_bindir}
install -m755 %{SOURCE0} %{buildroot}%{_bindir}

%post

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{_bindir}/*

%changelog
*   Wed Oct 27 2021 Daniel Casota <dcasota@gmail.com> 1.0-2
-   Fix reboot
*   Mon Oct 12 2020 Dweep Advani <dadvani@vmware.com> 1.0-1
-   Initial Photon 3.0 to 4.0 upgrade package
