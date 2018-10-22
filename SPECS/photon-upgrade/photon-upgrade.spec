Summary:    Photon upgrade scripts
Name:       photon-upgrade
Version:    1.0
Release:    1%{?dist}
License:    Apache License
Group:      System Environment/Base
Source0:    photon-upgrade.sh
URL:        https://vmware.github.io/photon/
Vendor:     VMware, Inc.
Distribution:   Photon
BuildArch:  noarch
Requires:   tdnf

%description
Photon major upgrade scripts. Addresses 2.0 to 3.0 upgrades.

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
*       Fri Oct 19 2018 Dweep Advani <dadvani@vmware.com> 1.0-1
-       Initial Photon 2.0 to 3.0 upgrade package
