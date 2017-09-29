Summary:    Photon upgrade scripts
Name:       photon-upgrade
Version:    1.0
Release:    2%{?dist}
License:    Apache License
Group:      System Environment/Base
Source0:    photon-upgrade.sh
URL:        https://vmware.github.io/photon/
Vendor:     VMware, Inc.
Distribution:   Photon
BuildArch:  x86_64
Requires:   tdnf

%description
Photon major upgrade scripts. Addresses 1.0 to 2.0 upgrades.

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
*       Fri Sep 29 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.0-2
-       change script to update to new rpm for complex dependencies
*       Wed Jun 28 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.0-1
-       Initial
