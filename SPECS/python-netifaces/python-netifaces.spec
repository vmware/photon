%global debug_package %{nil}
Name:           python3-netifaces
Version:        0.11.0
Release:        2%{?dist}
Summary:        Python library to retrieve information about network interfaces
Group:          Development/Libraries
URL:            http://alastairs-place.net/netifaces/
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://pypi.python.org/packages/source/n/netifaces/netifaces-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
Requires:       python3
Requires:       python3-libs

%description
This package provides a cross platform API for getting address information
from network interfaces.

%prep
%autosetup -n netifaces-%{version}

%build
%{py3_build}

%install
%py3_install

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root,-)
%doc README.rst
%{python3_sitelib}/*

%changelog
*  Wed Dec 11 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 0.11.0-2
-  Release bump for SRP compliance
*  Sun Aug 21 2022 Gerrit Photon <photon-checkins@vmware.com> 0.11.0-1
-  Automatic Version Bump
*  Sat Jun 20 2020 Tapas Kundu <tkundu@vmware.com> 0.10.9-2
-  Mass removal python2
*  Tue Jul 23 2019 Tapas Kundu <tkundu@vmware.com> 0.10.9-1
-  Initial packaging for photon OS
